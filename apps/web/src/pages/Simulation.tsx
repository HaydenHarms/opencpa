import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import type { JournalLine, PublicTbs, PublicTbsTask } from '@opencpa/schema';
import {
  api,
  type SimulationResult,
  type SimulationReveal,
  type TaskResponse,
  type TaskResult,
} from '../api';

type JeRow = { account: string; debit: string; credit: string };
type Draft = { numeric: string; lines: JeRow[]; citation: string; picks: Record<string, string> };

const emptyRow = (): JeRow => ({ account: '', debit: '', credit: '' });
const emptyDraft = (): Draft => ({
  numeric: '',
  lines: [emptyRow(), emptyRow()],
  citation: '',
  picks: {},
});

/** Parse "1,234.56", "$1,234" or "(1,234)" (negative). Returns null for blank or invalid input. */
export function parseAmount(raw: string): number | null {
  const s = raw.trim().replace(/[$,\s]/g, '');
  if (!s) return null;
  const neg = /^\(.*\)$/.test(s);
  const n = Number(neg ? s.slice(1, -1) : s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const toCents = (n: number) => Math.round(n * 100);
const dollars = (cents: number) =>
  (cents / 100).toLocaleString('en-US', { style: 'currency', currency: 'USD' });

function toResponse(task: PublicTbsTask, d: Draft): TaskResponse | undefined {
  switch (task.type) {
    case 'numeric': {
      const n = parseAmount(d.numeric);
      if (n === null) return undefined;
      return { type: 'numeric', value: task.unit === 'cents' ? toCents(n) : n };
    }
    case 'journal_entry': {
      const lines = d.lines
        .filter((l) => l.account && (l.debit.trim() || l.credit.trim()))
        .map((l) => ({
          account: l.account,
          debit: toCents(Math.abs(parseAmount(l.debit) ?? 0)),
          credit: toCents(Math.abs(parseAmount(l.credit) ?? 0)),
        }));
      return lines.length ? { type: 'journal_entry', lines } : undefined;
    }
    case 'research':
      return d.citation.trim() ? { type: 'research', citation: d.citation.trim() } : undefined;
    case 'select': {
      const choices = Object.fromEntries(
        task.rows.filter((r) => d.picks[r.id]).map((r) => [r.id, d.picks[r.id]!]),
      );
      return Object.keys(choices).length ? { type: 'select', choices } : undefined;
    }
  }
}

/** Exhibits are markdown; render paragraphs and pipe tables only (no raw HTML). */
function Exhibit({ body }: { body: string }) {
  const blocks = body.trim().split(/\n\s*\n/);
  return (
    <>
      {blocks.map((block, i) => {
        const lines = block.split('\n').filter((l) => l.trim());
        if (lines.every((l) => l.trim().startsWith('|'))) {
          const cells = (l: string) =>
            l
              .trim()
              .replace(/^\||\|$/g, '')
              .split('|')
              .map((c) => c.trim());
          const rows = lines.filter((l) => !/^\|?[\s:|-]+\|?$/.test(l.trim())).map(cells);
          const [head, ...rest] = rows;
          return (
            <table key={i} className="exhibit-table">
              <thead>
                <tr>
                  {head?.map((c, j) => (
                    <th key={j}>{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rest.map((r, k) => (
                  <tr key={k}>
                    {r.map((c, j) => (
                      <td key={j}>{c}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          );
        }
        return <p key={i}>{lines.join(' ')}</p>;
      })}
    </>
  );
}

function JournalGrid({
  accounts,
  rows,
  onChange,
  disabled,
}: {
  accounts: string[];
  rows: JeRow[];
  onChange: (rows: JeRow[]) => void;
  disabled: boolean;
}) {
  const set = (i: number, patch: Partial<JeRow>) =>
    onChange(rows.map((r, j) => (j === i ? { ...r, ...patch } : r)));
  const total = (k: 'debit' | 'credit') =>
    rows.reduce((s, r) => s + toCents(Math.abs(parseAmount(r[k]) ?? 0)), 0);
  const dr = total('debit');
  const cr = total('credit');
  return (
    <div className="je">
      <table className="je-grid">
        <thead>
          <tr>
            <th>Account</th>
            <th>Debit</th>
            <th>Credit</th>
            <th aria-label="Remove row" />
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td>
                <select
                  value={r.account}
                  disabled={disabled}
                  onChange={(e) => set(i, { account: e.target.value })}
                >
                  <option value="">Select an account</option>
                  {accounts.map((a) => (
                    <option key={a} value={a}>
                      {a}
                    </option>
                  ))}
                </select>
              </td>
              <td>
                <input
                  inputMode="decimal"
                  value={r.debit}
                  disabled={disabled}
                  onChange={(e) => set(i, { debit: e.target.value })}
                />
              </td>
              <td>
                <input
                  inputMode="decimal"
                  value={r.credit}
                  disabled={disabled}
                  onChange={(e) => set(i, { credit: e.target.value })}
                />
              </td>
              <td>
                {rows.length > 1 && !disabled && (
                  <button
                    className="link"
                    aria-label="Remove row"
                    onClick={() => onChange(rows.filter((_, j) => j !== i))}
                  >
                    ×
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td>Totals</td>
            <td>{dollars(dr)}</td>
            <td>{dollars(cr)}</td>
            <td />
          </tr>
        </tfoot>
      </table>
      {!disabled && (
        <button className="link" onClick={() => onChange([...rows, emptyRow()])}>
          + Add a line
        </button>
      )}
      {dr !== cr && (dr > 0 || cr > 0) && (
        <p className="warn">
          Debits and credits don’t balance yet ({dollars(Math.abs(dr - cr))} off).
        </p>
      )}
    </div>
  );
}

/** One drop-down per row, as in the exam's option-list tasks. After grading, each row shows the key. */
function SelectRows({
  task,
  picks,
  onChange,
  result,
}: {
  task: Extract<PublicTbsTask, { type: 'select' }>;
  picks: Record<string, string>;
  onChange: (picks: Record<string, string>) => void;
  result?: TaskResult;
}) {
  const key = result?.answer as Record<string, string> | undefined;
  return (
    <table className="select-grid">
      <tbody>
        {task.rows.map((r) => {
          const mark = key ? (picks[r.id] === key[r.id] ? 'right-text' : 'wrong-text') : '';
          return (
            <tr key={r.id}>
              <td>{r.label}</td>
              <td>
                <select
                  aria-label={r.label}
                  className={mark}
                  value={picks[r.id] ?? ''}
                  disabled={!!result}
                  onChange={(e) => onChange({ ...picks, [r.id]: e.target.value })}
                >
                  <option value="">Select an option</option>
                  {r.options.map((o) => (
                    <option key={o} value={o}>
                      {o}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

function Answer({ task, result }: { task: PublicTbsTask; result: TaskResult }) {
  if (task.type === 'journal_entry') {
    const lines = result.answer as JournalLine[];
    return (
      <table className="je-grid">
        <tbody>
          {lines.map((l, i) => (
            <tr key={i}>
              <td>{l.account}</td>
              <td>{l.debit ? dollars(l.debit) : ''}</td>
              <td>{l.credit ? dollars(l.credit) : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
  if (task.type === 'research') return <p>{(result.answer as string[]).join(' or ')}</p>;
  if (task.type === 'select') {
    const key = result.answer as Record<string, string>;
    return (
      <ul>
        {task.rows.map((r) => (
          <li key={r.id}>
            {r.label}: {key[r.id]}
          </li>
        ))}
      </ul>
    );
  }
  const n = result.answer as number;
  return <p>{task.unit === 'cents' ? dollars(n) : task.unit === 'percent' ? `${n}%` : n}</p>;
}

/** Rebuild the input drafts from a submitted response, to show a finished simulation again. */
function draftFrom(task: PublicTbsTask, r: TaskResponse | undefined): Draft {
  const d = emptyDraft();
  const amount = (cents: number | undefined) => (cents ? String(cents / 100) : '');
  if (r?.type === 'numeric')
    d.numeric = String(task.type === 'numeric' && task.unit === 'cents' ? r.value / 100 : r.value);
  if (r?.type === 'journal_entry')
    d.lines = r.lines.map((l) => ({
      account: l.account,
      debit: amount(l.debit),
      credit: amount(l.credit),
    }));
  if (r?.type === 'research') d.citation = r.citation;
  if (r?.type === 'select') d.picks = { ...r.choices };
  return d;
}

/** The standalone simulation page, reached from the Simulations list. */
export default function Simulation() {
  const { id = '' } = useParams();
  const [sim, setSim] = useState<PublicTbs | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.simulation(id).then(setSim, (e: Error) => setError(e.message));
  }, [id]);

  if (error) return <p className="error">Couldn’t load this simulation: {error}</p>;
  if (!sim) return <p className="muted">Loading…</p>;
  return (
    <SimulationPlayer
      key={sim.id}
      sim={sim}
      crumb={
        <>
          <Link to="/simulations">Simulations</Link> · {sim.blueprint.section} ·{' '}
          {sim.blueprint.topic}
        </>
      }
    />
  );
}

/**
 * Work through and submit one simulation. Inside a practice session it is given the
 * session id, and the previous result when the student comes back to a finished one.
 */
export function SimulationPlayer({
  sim,
  crumb,
  sessionId,
  previous,
  onSubmitted,
}: {
  sim: PublicTbs;
  crumb: ReactNode;
  sessionId?: string;
  previous?: SimulationReveal;
  onSubmitted?: (r: SimulationResult) => void;
}) {
  const [error, setError] = useState<string | null>(null);
  const [current, setCurrent] = useState(0);
  const [exhibit, setExhibit] = useState(0);
  const [drafts, setDrafts] = useState<Record<string, Draft>>(() =>
    Object.fromEntries(sim.tasks.map((t) => [t.id, draftFrom(t, previous?.responses[t.id])])),
  );
  const [result, setResult] = useState<SimulationReveal | null>(previous ?? null);
  const [submitting, setSubmitting] = useState(false);
  const started = useRef(Date.now());

  const task = sim.tasks[current]!;
  const draft = drafts[task.id] ?? emptyDraft();
  const update = (patch: Partial<Draft>) =>
    setDrafts({ ...drafts, [task.id]: { ...draft, ...patch } });
  const taskResult = result?.tasks.find((t) => t.id === task.id);
  const answered = sim.tasks.filter((t) => toResponse(t, drafts[t.id] ?? emptyDraft())).length;

  async function submit() {
    if (!sim) return;
    const responses: Record<string, TaskResponse> = {};
    for (const t of sim.tasks) {
      const r = toResponse(t, drafts[t.id] ?? emptyDraft());
      if (r) responses[t.id] = r;
    }
    setSubmitting(true);
    try {
      const r = await api.submitSimulation(
        sim.id,
        responses,
        Date.now() - started.current,
        sessionId,
      );
      setResult(r);
      onSubmitted?.(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="sim">
      {error && <p className="error">Couldn’t submit: {error}</p>}
      <p className="meta">{crumb}</p>
      <h2>{sim.title}</h2>
      <p>{sim.scenario}</p>

      <div className="sim-body">
        <div className="sim-tasks">
          <div className="tabs">
            {sim.tasks.map((t, i) => {
              const r = result?.tasks.find((x) => x.id === t.id);
              return (
                <button
                  key={t.id}
                  className={`${i === current ? 'active' : ''} ${r ? (r.correct ? 'right-text' : 'wrong-text') : ''}`}
                  onClick={() => setCurrent(i)}
                >
                  Task {i + 1}
                </button>
              );
            })}
          </div>
          <article className="card">
            <p className="meta">
              Task {current + 1} of {sim.tasks.length} · {task.points} point
              {task.points === 1 ? '' : 's'}
            </p>
            <p className="stem">{task.prompt}</p>

            {task.type === 'numeric' && (
              <label className="field">
                {task.unit === 'cents'
                  ? 'Amount ($)'
                  : task.unit === 'percent'
                    ? 'Percent'
                    : 'Value'}
                <input
                  inputMode="decimal"
                  placeholder={task.unit === 'cents' ? 'e.g. 12,500 or (1,200)' : ''}
                  value={draft.numeric}
                  disabled={!!result}
                  onChange={(e) => update({ numeric: e.target.value })}
                />
              </label>
            )}
            {task.type === 'journal_entry' && (
              <JournalGrid
                accounts={task.accounts}
                rows={draft.lines}
                disabled={!!result}
                onChange={(lines) => update({ lines })}
              />
            )}
            {task.type === 'select' && (
              <SelectRows
                task={task}
                picks={draft.picks}
                result={taskResult}
                onChange={(picks) => update({ picks })}
              />
            )}
            {task.type === 'research' && (
              <label className="field">
                Citation
                <input
                  placeholder="e.g. ASC 842-20-30-1"
                  value={draft.citation}
                  disabled={!!result}
                  onChange={(e) => update({ citation: e.target.value })}
                />
              </label>
            )}

            {taskResult && (
              <div className="task-result">
                <p className={taskResult.correct ? 'right-text' : 'wrong-text'}>
                  {taskResult.earned} of {taskResult.possible} point
                  {taskResult.possible === 1 ? '' : 's'}
                </p>
                <p className="meta">Answer</p>
                <Answer task={task} result={taskResult} />
                <p>{taskResult.explanation}</p>
              </div>
            )}

            <div className="row">
              <button
                className="link"
                disabled={current === 0}
                onClick={() => setCurrent(current - 1)}
              >
                ← Previous
              </button>
              <button
                className="link"
                disabled={current === sim.tasks.length - 1}
                onClick={() => setCurrent(current + 1)}
              >
                Next →
              </button>
            </div>
          </article>

          {!result ? (
            <button className="button" disabled={submitting} onClick={submit}>
              {submitting
                ? 'Grading…'
                : `Submit simulation (${answered} of ${sim.tasks.length} answered)`}
            </button>
          ) : (
            <p className={result.correct ? 'right-text' : ''}>
              Score: {result.earned} of {result.possible} points.
              {'nextDue' in result &&
                ` Next review ${new Date(result.nextDue as string).toLocaleDateString()}.`}
            </p>
          )}
        </div>

        {sim.exhibits.length > 0 && (
          <aside className="sim-exhibits card">
            <div className="tabs">
              {sim.exhibits.map((e, i) => (
                <button
                  key={i}
                  className={i === exhibit ? 'active' : ''}
                  onClick={() => setExhibit(i)}
                >
                  {e.title}
                </button>
              ))}
            </div>
            <Exhibit body={sim.exhibits[exhibit]!.body} />
          </aside>
        )}
      </div>
    </section>
  );
}
