/**
 * The Claude connector: a remote MCP server that lets Claude (in the Claude apps, added
 * as a custom connector) look up what a student is working on and explain it.
 *
 * It never calls a model and never grades. Answers are shown only for items the
 * student has already attempted, the same rule the website follows.
 */
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js';
import { CfWorkerJsonSchemaValidator } from '@modelcontextprotocol/sdk/validation/cfworker';
import { z } from 'zod';
import {
  toPublicMcq,
  toPublicTbs,
  type Item,
  type JournalLine,
  type TbsItem,
} from '@opencpa/schema';
import { masteryByArea, masteryByTopic } from '@opencpa/engine';
import { byId } from './content';
import {
  reveal,
  revealSimulation,
  sessionItemIds,
  type Responses,
  type SessionRow,
} from './sessions';

const INSTRUCTIONS = `OpenCPA is a free CPA exam study site. The student practices questions and simulations there, then asks you about them here.

- When the student says "this question", "the one I just did" or similar, call get_last_attempt (what they just answered) or get_current_question (what is on their screen and not yet answered).
- Before an attempt you only get the public question. Help with hints and the relevant concept, but don't work out or reveal the answer unless the student asks you to.
- After an attempt you get the answer key, the rationale for every choice and the official explanation. Explain why the student's choice was wrong (or right), using that material.
- OpenCPA grades answers; you don't. If you think a key is wrong, say so and explain why, but don't tell the student they were marked unfairly without checking the rationale.
- Cite ASC/GASB topics the way the explanation does. Don't invent paragraph numbers.`;

type Attempt = {
  item_id: string;
  response: string;
  correct: number;
  earned: number;
  possible: number;
  created_at: number;
};

const iso = (ms: number) => new Date(ms).toISOString();
const dollars = (cents: number | undefined) => (cents ?? 0) / 100;

/** Simulation amounts are stored in cents; show dollars so Claude doesn't misread them. */
function tbsInDollars(item: TbsItem, revealed: ReturnType<typeof revealSimulation>) {
  const unitOf = new Map(item.tasks.map((t) => [t.id, t.type === 'numeric' ? t.unit : null]));
  const lines = (l: { account: string; debit?: number; credit?: number }[]) =>
    l.map((x) => ({ account: x.account, debit: dollars(x.debit), credit: dollars(x.credit) }));
  return {
    score: `${revealed.earned} of ${revealed.possible} points`,
    tasks: item.tasks.map((t) => {
      const r = revealed.tasks.find((x) => x.id === t.id)!;
      const given = revealed.responses[t.id];
      const cents = unitOf.get(t.id) === 'cents';
      return {
        id: t.id,
        prompt: t.prompt,
        points: `${r.earned} of ${r.possible}`,
        studentAnswer:
          given?.type === 'numeric'
            ? cents
              ? given.value / 100
              : given.value
            : given?.type === 'journal_entry'
              ? lines(given.lines)
              : given?.type === 'research'
                ? given.citation
                : '(no answer)',
        correctAnswer:
          t.type === 'numeric'
            ? cents
              ? t.answer / 100
              : t.answer
            : t.type === 'journal_entry'
              ? lines(t.answer as JournalLine[])
              : t.answer,
        explanation: t.explanation,
      };
    }),
  };
}

/** The public view of an item, with amounts in simulations shown as written. */
function publicItem(item: Item) {
  if (item.type === 'mcq') return toPublicMcq(item);
  const t = toPublicTbs(item);
  return { ...t, note: 'Numeric answers with unit "cents" are entered in dollars on the site.' };
}

/** Everything an attempt reveals about an item, for Claude to explain. */
function attemptDetail(item: Item, a: Attempt) {
  const when = iso(a.created_at);
  if (item.type === 'mcq') {
    const { selected } = JSON.parse(a.response) as { selected: string };
    const r = reveal(item, selected, !!a.correct);
    return {
      id: item.id,
      type: 'multiple choice',
      blueprint: item.blueprint,
      answeredAt: when,
      stem: item.stem,
      choices: item.choices.map((c) => ({ id: c.id, text: c.text, rationale: c.rationale })),
      studentChoice: r.selected,
      correctAnswer: r.answer,
      studentWasCorrect: r.correct,
      explanation: r.explanation,
    };
  }
  const r = revealSimulation(item, JSON.parse(a.response) as Responses);
  return {
    id: item.id,
    type: 'simulation',
    blueprint: item.blueprint,
    answeredAt: when,
    title: item.title,
    scenario: item.scenario,
    exhibits: item.exhibits,
    ...tbsInDollars(item, r),
  };
}

const text = (value: unknown) => ({
  content: [{ type: 'text' as const, text: JSON.stringify(value, null, 2) }],
});

function buildServer(db: D1Database, userId: string) {
  const server = new McpServer(
    { name: 'opencpa', version: '0.1.0' },
    { instructions: INSTRUCTIONS, jsonSchemaValidator: new CfWorkerJsonSchemaValidator() },
  );

  server.registerTool(
    'get_last_attempt',
    {
      title: 'Last answered item',
      description:
        "The student's most recent answers on OpenCPA (newest first), each with the full question, the student's answer, the answer key, every choice's rationale and the official explanation.",
      inputSchema: {
        count: z
          .number()
          .int()
          .min(1)
          .max(5)
          .optional()
          .describe('How many recent answers (default 1)'),
      },
      annotations: { readOnlyHint: true },
    },
    async ({ count }) => {
      const { results } = await db
        .prepare(
          'SELECT item_id, response, correct, earned, possible, created_at FROM attempts WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT ?',
        )
        .bind(userId, count ?? 1)
        .all<Attempt>();
      const out = results.flatMap((a) => {
        const item = byId.get(a.item_id);
        return item ? [attemptDetail(item, a)] : [];
      });
      return text(out.length ? out : { message: 'The student has not answered anything yet.' });
    },
  );

  server.registerTool(
    'get_current_question',
    {
      title: 'Current question',
      description:
        "The item on the student's screen in their active practice session, which they have not answered yet. Public fields only: no answer key.",
      inputSchema: {},
      annotations: { readOnlyHint: true },
    },
    async () => {
      const row = await db
        .prepare(
          "SELECT * FROM practice_sessions WHERE user_id = ? AND status = 'active' ORDER BY created_at DESC LIMIT 1",
        )
        .bind(userId)
        .first<SessionRow>();
      if (!row) return text({ message: 'The student has no practice session in progress.' });
      const ids = sessionItemIds(row);
      const { results } = await db
        .prepare('SELECT DISTINCT item_id FROM attempts WHERE session_id = ?')
        .bind(row.id)
        .all<{ item_id: string }>();
      const done = new Set(results.map((r) => r.item_id));
      const index = ids.findIndex((id) => !done.has(id));
      if (index === -1) return text({ message: 'Every item in the current session is answered.' });
      return text({
        session: {
          section: row.section,
          kind: row.kind,
          position: `${index + 1} of ${ids.length}`,
        },
        item: publicItem(byId.get(ids[index]!)!),
      });
    },
  );

  server.registerTool(
    'get_question',
    {
      title: 'Look up a question',
      description:
        "Any OpenCPA item by id. Includes the answer key and the student's latest answer only if the student has already attempted it.",
      inputSchema: { id: z.string().describe('Item id, e.g. far-leases-0001') },
      annotations: { readOnlyHint: true },
    },
    async ({ id }) => {
      const item = byId.get(id);
      if (!item) return text({ error: `No item with id ${id}.` });
      const a = await db
        .prepare(
          'SELECT item_id, response, correct, earned, possible, created_at FROM attempts WHERE user_id = ? AND item_id = ? ORDER BY created_at DESC, id DESC LIMIT 1',
        )
        .bind(userId, id)
        .first<Attempt>();
      return text(
        a
          ? attemptDetail(item, a)
          : {
              attempted: false,
              note: 'Not attempted yet, so no answer key.',
              item: publicItem(item),
            },
      );
    },
  );

  server.registerTool(
    'get_my_progress',
    {
      title: 'Study progress',
      description:
        "The student's mastery by blueprint area and topic (recency-weighted accuracy), their weakest topics, and their most recent misses.",
      inputSchema: {
        section: z
          .enum(['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP'])
          .optional()
          .describe('Limit to one exam section'),
      },
      annotations: { readOnlyHint: true },
    },
    async ({ section }) => {
      const { results } = await db
        .prepare(
          `SELECT item_id, section, area, correct, created_at FROM attempts
           WHERE user_id = ? AND (?2 IS NULL OR section = ?2) ORDER BY created_at DESC`,
        )
        .bind(userId, section ?? null)
        .all<{
          item_id: string;
          section: string;
          area: string;
          correct: number;
          created_at: number;
        }>();
      if (!results.length) return text({ message: 'No answers yet.' });
      const withTopic = results.flatMap((r) => {
        const item = byId.get(r.item_id);
        return item ? [{ ...r, topic: item.blueprint.topic }] : [];
      });
      const counts = new Map<string, number>();
      for (const r of withTopic) counts.set(r.topic, (counts.get(r.topic) ?? 0) + 1);
      const topics = [
        ...masteryByTopic(
          withTopic.map((r) => ({ topic: r.topic, correct: !!r.correct, at: r.created_at })),
        ),
      ]
        .map(([topic, score]) => ({
          topic,
          attempts: counts.get(topic)!,
          mastery: Math.round(score * 100),
        }))
        .sort((a, b) => a.mastery - b.mastery);
      return text({
        totalAnswers: results.length,
        byArea: masteryByArea(
          results.map((r) => ({
            section: r.section,
            area: r.area,
            correct: !!r.correct,
            at: r.created_at,
          })),
        ).map((m) => ({ ...m, score: Math.round(m.score * 100) })),
        weakestTopics: topics.slice(0, 5),
        allTopics: topics,
        recentMisses: withTopic
          .filter((r) => !r.correct)
          .slice(0, 10)
          .map((r) => ({ id: r.item_id, topic: r.topic, answeredAt: iso(r.created_at) })),
        note: 'mastery is a 0-100 recency-weighted accuracy. Use get_question with an id for details.',
      });
    },
  );

  return server;
}

/** Handle one MCP request for a student. Stateless: a fresh server and transport per request. */
export async function handleMcp(request: Request, db: D1Database, userId: string) {
  const server = buildServer(db, userId);
  const transport = new WebStandardStreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true,
  });
  await server.connect(transport);
  return transport.handleRequest(request);
}

/** Connector links carry a random token; only its SHA-256 hash is stored. */
export async function hashToken(token: string) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(token));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function newToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}
