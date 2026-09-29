import { useEffect, useRef, useState } from 'react';
import type { PublicMcq } from '@opencpa/schema';
import { api, SECTIONS, type Revealed, type Session, type SessionStatus } from '../api';

const SIZES = [10, 25, 50];

function savedSection(): string {
  try {
    return localStorage.getItem('opencpa:section') ?? 'FAR';
  } catch {
    return 'FAR';
  }
}

export default function Practice() {
  const [section, setSection] = useState(savedSection);
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [error, setError] = useState<string | null>(null);

  function load(s: string) {
    setStatus(null);
    setSession(null);
    setError(null);
    api.currentSession(s).then((st) => {
      setStatus(st);
      setSession(st.session);
    }, fail);
  }

  function fail(e: Error) {
    setError(e.message);
  }

  useEffect(() => {
    try {
      localStorage.setItem('opencpa:section', section);
    } catch {
      // Remembering the tab is only a convenience.
    }
    load(section);
  }, [section]);

  async function start(size: number) {
    setError(null);
    try {
      setSession(await api.startSession(section, size));
    } catch (e) {
      fail(e as Error);
    }
  }

  return (
    <section>
      <div className="tabs">
        {SECTIONS.map((s) => (
          <button key={s} className={s === section ? 'active' : ''} onClick={() => setSection(s)}>
            {s}
          </button>
        ))}
      </div>

      {error && <p className="error">Couldn’t reach the API: {error}</p>}
      {!status && !error && <p className="muted">Loading…</p>}
      {status && !session && <StartPanel section={section} status={status} onStart={start} />}
      {session && (
        <SessionRunner
          key={session.id}
          session={session}
          onError={fail}
          onNew={() => {
            // Show the start panel; the unfinished session is abandoned only when a new one starts.
            setSession(null);
            setStatus(null);
            api.currentSession(section).then(setStatus, fail);
          }}
        />
      )}
    </section>
  );
}

function StartPanel({
  section,
  status,
  onStart,
}: {
  section: string;
  status: SessionStatus;
  onStart: (size: number) => void;
}) {
  if (status.poolSize === 0)
    return (
      <p className="muted">
        No reviewed {section} questions yet. They’re being added — check back soon.
      </p>
    );

  if (status.nextKind === 'diagnostic')
    return (
      <article className="card">
        <h2>Start with a diagnostic</h2>
        <p>
          Your first {section} session is a {status.diagnosticSize}-question diagnostic drawn from
          across the blueprint. After that, each session leans toward the topics you miss most and
          brings back questions when they’re due for review.
        </p>
        <button className="button" onClick={() => onStart(status.diagnosticSize)}>
          Start the diagnostic
        </button>
      </article>
    );

  const sizes = SIZES.filter((n) => n < status.poolSize);
  sizes.push(Math.min(status.poolSize, SIZES[SIZES.length - 1]!));
  return (
    <article className="card">
      <h2>New {section} session</h2>
      <p className="muted">
        A mix of topics across the blueprint, weighted toward your weak spots and the questions due
        for review. Your place is saved as you go.
      </p>
      <div className="row-start">
        {[...new Set(sizes)].map((n) => (
          <button key={n} className="button" onClick={() => onStart(n)}>
            {n} questions
          </button>
        ))}
      </div>
    </article>
  );
}

function SessionRunner({
  session,
  onError,
  onNew,
}: {
  session: Session;
  onError: (e: Error) => void;
  onNew: () => void;
}) {
  const { items } = session;
  const [answered, setAnswered] = useState(session.answered);
  const [index, setIndex] = useState(() => {
    const i = items.findIndex((q) => !session.answered[q.id]);
    return i === -1 ? items.length : i;
  });
  const [selected, setSelected] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const started = useRef(Date.now());

  const q = items[index];
  const result = q ? answered[q.id] : undefined;
  const label = session.kind === 'diagnostic' ? 'Diagnostic' : 'Practice session';

  async function submit() {
    if (!q || !selected || busy) return;
    setBusy(true);
    try {
      const r = await api.attempt(q.id, selected, Date.now() - started.current, session.id);
      setAnswered((a) => ({ ...a, [q.id]: r }));
    } catch (e) {
      onError(e as Error);
    } finally {
      setBusy(false);
    }
  }

  function next() {
    setIndex((i) => i + 1);
    setSelected(null);
    started.current = Date.now();
  }

  if (!q) return <Summary session={session} answered={answered} onNew={onNew} />;

  return (
    <>
      <div className="row">
        <span className="meta">
          {label} · question {index + 1} of {items.length}
        </span>
        <button
          className="link"
          onClick={() => {
            if (confirm('End this session and start a new one? Your answers so far still count.'))
              onNew();
          }}
        >
          New session
        </button>
      </div>
      <div className="progress">
        <span style={{ width: `${(Object.keys(answered).length / items.length) * 100}%` }} />
      </div>
      <Question
        q={q}
        selected={result?.selected ?? selected}
        result={result}
        onSelect={setSelected}
      />
      {!result ? (
        <button className="button" disabled={!selected || busy} onClick={submit}>
          Submit
        </button>
      ) : (
        <button className="button" onClick={next}>
          {index + 1 < items.length ? 'Next question' : 'See results'}
        </button>
      )}
    </>
  );
}

function Question({
  q,
  selected,
  result,
  onSelect,
}: {
  q: PublicMcq;
  selected: string | null;
  result: Revealed | undefined;
  onSelect: (id: string) => void;
}) {
  return (
    <article className="card">
      <p className="meta">
        {q.blueprint.topic} · {q.blueprint.skill}
      </p>
      <p className="stem">{q.stem}</p>
      <ol className="choices">
        {q.choices.map((c) => {
          const state = result
            ? c.id === result.answer
              ? 'right'
              : c.id === selected
                ? 'wrong'
                : ''
            : c.id === selected
              ? 'picked'
              : '';
          return (
            <li key={c.id}>
              <button
                className={`choice ${state}`}
                disabled={!!result}
                onClick={() => onSelect(c.id)}
              >
                <b>{c.id}.</b> {c.text}
              </button>
              {result && <p className="rationale">{result.rationales[c.id]}</p>}
            </li>
          );
        })}
      </ol>
      {result && (
        <>
          <p className={result.correct ? 'right-text' : 'wrong-text'}>
            {result.correct ? 'Correct.' : `Not quite — the answer is ${result.answer}.`}
          </p>
          <p>{result.explanation}</p>
        </>
      )}
    </article>
  );
}

interface Tally {
  name: string;
  right: number;
  total: number;
}

function tally(
  items: PublicMcq[],
  answered: Record<string, Revealed>,
  key: (q: PublicMcq) => string,
) {
  const m = new Map<string, Tally>();
  for (const q of items) {
    const r = answered[q.id];
    if (!r) continue;
    const t = m.get(key(q)) ?? { name: key(q), right: 0, total: 0 };
    t.total++;
    if (r.correct) t.right++;
    m.set(t.name, t);
  }
  return [...m.values()];
}

function Summary({
  session,
  answered,
  onNew,
}: {
  session: Session;
  answered: Record<string, Revealed>;
  onNew: () => void;
}) {
  const byArea = tally(session.items, answered, (q) => q.blueprint.area).sort((a, b) =>
    a.name.localeCompare(b.name),
  );
  const byTopic = tally(session.items, answered, (q) => q.blueprint.topic).sort(
    (a, b) => a.right / a.total - b.right / b.total || b.total - a.total,
  );
  const right = byArea.reduce((s, t) => s + t.right, 0);
  const total = byArea.reduce((s, t) => s + t.total, 0);
  const weak = byTopic.filter((t) => t.right < t.total).slice(0, 3);
  const pct = (t: { right: number; total: number }) =>
    t.total ? Math.round((t.right / t.total) * 100) : 0;

  return (
    <article className="card">
      <p className="meta">{session.kind === 'diagnostic' ? 'Diagnostic' : 'Session'} complete</p>
      <h2>
        {right} of {total} correct ({pct({ right, total })}%)
      </h2>
      {weak.length > 0 && (
        <p>
          {session.kind === 'diagnostic'
            ? 'Your next sessions will lean toward '
            : 'Worth another look: '}
          {weak.map((t) => t.name).join(', ')}.
        </p>
      )}
      <TallyTable title="By blueprint area" rows={byArea} pct={pct} />
      <TallyTable title="By topic" rows={byTopic} pct={pct} />
      <button className="button" onClick={onNew}>
        Start a new session
      </button>
    </article>
  );
}

function TallyTable({
  title,
  rows,
  pct,
}: {
  title: string;
  rows: Tally[];
  pct: (t: Tally) => number;
}) {
  return (
    <table className="mastery">
      <thead>
        <tr>
          <th>{title}</th>
          <th>Correct</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((t) => (
          <tr key={t.name}>
            <td>{t.name}</td>
            <td>
              {t.right} of {t.total}
            </td>
            <td>
              <div className="bar">
                <span style={{ width: `${pct(t)}%` }} />
              </div>
              {pct(t)}%
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
