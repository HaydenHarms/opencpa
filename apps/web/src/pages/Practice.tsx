import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import type { PublicMcq, PublicTbs } from '@opencpa/schema';
import {
  api,
  SECTIONS,
  type Revealed,
  type Session,
  type SessionMode,
  type SessionOption,
  type SessionStatus,
  type SimulationReveal,
} from '../api';
import { SimulationPlayer } from './Simulation';

function saved(key: string, fallback: string): string {
  try {
    return localStorage.getItem(key) ?? fallback;
  } catch {
    return fallback;
  }
}

function remember(key: string, value: string) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // Remembering the tab is only a convenience.
  }
}

const MODES: { id: SessionMode; label: string }[] = [
  { id: 'questions', label: 'Questions' },
  { id: 'simulations', label: 'Simulations' },
];

export default function Practice() {
  const [section, setSection] = useState(() => saved('opencpa:section', 'FAR'));
  const [mode, setMode] = useState<SessionMode>(() =>
    saved('opencpa:practice-mode', 'questions') === 'simulations' ? 'simulations' : 'questions',
  );
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [error, setError] = useState<string | null>(null);

  function load() {
    setStatus(null);
    setSession(null);
    setError(null);
    api.currentSession(section, { mode }).then((st) => {
      setStatus(st);
      setSession(st.session);
    }, fail);
  }

  function fail(e: Error) {
    setError(e.message);
  }

  useEffect(() => {
    remember('opencpa:section', section);
    remember('opencpa:practice-mode', mode);
    load();
  }, [section, mode]);

  async function start(size: number) {
    setError(null);
    try {
      setSession(await api.startSession(section, size, { mode }));
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
      <div className="tabs">
        {MODES.map((m) => (
          <button
            key={m.id}
            className={m.id === mode ? 'active' : ''}
            onClick={() => setMode(m.id)}
          >
            {m.label}
          </button>
        ))}
      </div>

      {error && <p className="error">Couldn’t reach the API: {error}</p>}
      {!status && !error && <p className="muted">Loading…</p>}
      {status && !session && (
        <StartPanel section={section} status={status} onStart={start} mode={mode} />
      )}
      {session && (
        <SessionRunner
          key={session.id}
          session={session}
          onError={fail}
          onNew={() => {
            // Show the start panel; the unfinished session is abandoned only when a new one starts.
            setSession(null);
            setStatus(null);
            api.currentSession(section, { mode }).then(setStatus, fail);
          }}
        />
      )}
    </section>
  );
}

export function StartPanel({
  section,
  status,
  onStart,
  title,
  blurb,
  mode = 'questions',
}: {
  section: string;
  status: SessionStatus;
  onStart: (size: number) => void;
  /** A Practice simulations session; Library topic sessions leave this as 'questions'. */
  mode?: SessionMode;
  /** Library topic sessions override the heading and description. */
  title?: string;
  blurb?: string;
}) {
  if (status.poolSize === 0)
    return (
      <p className="muted">
        No reviewed {section} {mode === 'simulations' ? 'simulations' : 'questions'} yet. They’re
        being added — check back soon.
      </p>
    );

  if (status.nextKind === 'diagnostic')
    return (
      <article className="card">
        <h2>Start with a diagnostic</h2>
        <p>
          Your first {section} session is a diagnostic drawn from across the blueprint:{' '}
          {describe(status.diagnostic)}. After that, each session leans toward the topics you miss
          most and brings back questions when they’re due for review.
        </p>
        <button className="button" onClick={() => onStart(status.diagnostic.size)}>
          Start the diagnostic
        </button>
      </article>
    );

  return (
    <article className="card">
      <h2>
        {title ?? `New ${section} ${mode === 'simulations' ? 'simulation session' : 'session'}`}
      </h2>
      <p className="muted">
        {blurb ??
          (mode === 'simulations'
            ? 'Simulations from across the blueprint, as on the exam’s simulation testlets, weighted toward your weak spots and the ones due for review.'
            : 'Multiple-choice questions from across the blueprint, as on the exam’s question testlets, weighted toward your weak spots and the items due for review.')}{' '}
        Your place is saved as you go.
      </p>
      <div className="row-start">
        {status.options.map((o) => (
          <button key={o.size} className="button" onClick={() => onStart(o.size)}>
            {describe(o)}
          </button>
        ))}
      </div>
    </article>
  );
}

const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`;

export function describe(o: SessionOption) {
  if (!o.questions) return plural(o.simulations, 'simulation');
  return o.simulations
    ? `${plural(o.questions, 'question')} + ${plural(o.simulations, 'simulation')}`
    : plural(o.questions, 'question');
}

export function SessionRunner({
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
  const label =
    session.kind === 'diagnostic'
      ? 'Diagnostic'
      : session.topic
        ? `Topic practice · ${session.topic}`
        : session.mode === 'simulations'
          ? 'Simulation session'
          : 'Practice session';

  async function submit() {
    if (!q || q.type !== 'mcq' || !selected || busy) return;
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
    window.scrollTo(0, 0);
  }

  if (!q) return <Summary session={session} answered={answered} onNew={onNew} />;

  const done = !!answered[q.id];
  const upcoming = items[index + 1];
  const nextButton = (
    <button className="button" onClick={next}>
      {!upcoming ? 'See results' : upcoming.type === 'tbs' ? 'Next: simulation' : 'Next question'}
    </button>
  );

  return (
    <>
      <div className="row">
        <span className="meta">
          {label} · {index + 1} of {items.length}
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
      {q.type === 'tbs' ? (
        <>
          <SimulationPlayer
            key={q.id}
            sim={q}
            crumb={<>Simulation · {q.blueprint.topic}</>}
            sessionId={session.id}
            previous={answered[q.id] as SimulationReveal | undefined}
            onSubmitted={(r) => setAnswered((a) => ({ ...a, [q.id]: r }))}
          />
          {done && nextButton}
        </>
      ) : (
        <>
          <Question
            q={q}
            selected={(answered[q.id] as Revealed | undefined)?.selected ?? selected}
            result={answered[q.id] as Revealed | undefined}
            onSelect={setSelected}
          />
          {done ? (
            nextButton
          ) : (
            <button className="button" disabled={!selected || busy} onClick={submit}>
              Submit
            </button>
          )}
        </>
      )}
    </>
  );
}

export function Question({
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
          <p className="meta">
            Still unsure? <Link to="/claude">Talk it through with Claude</Link>.
          </p>
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

function tally(items: PublicMcq[], answered: Session['answered'], key: (q: PublicMcq) => string) {
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
  answered: Session['answered'];
  onNew: () => void;
}) {
  const questions = session.items.filter((i): i is PublicMcq => i.type === 'mcq');
  const sims = session.items.filter((i): i is PublicTbs => i.type === 'tbs');
  const byArea = tally(questions, answered, (q) => q.blueprint.area).sort((a, b) =>
    a.name.localeCompare(b.name),
  );
  const byTopic = tally(questions, answered, (q) => q.blueprint.topic).sort(
    (a, b) => a.right / a.total - b.right / b.total || b.total - a.total,
  );
  const right = byArea.reduce((s, t) => s + t.right, 0);
  const total = byArea.reduce((s, t) => s + t.total, 0);
  const missedSimTopics = sims
    .filter((s) => {
      const r = answered[s.id] as SimulationReveal | undefined;
      return r && r.earned < r.possible;
    })
    .map((s) => s.blueprint.topic);
  const weak = [
    ...new Set([
      ...byTopic.filter((t) => t.right < t.total).map((t) => t.name),
      ...missedSimTopics,
    ]),
  ].slice(0, 3);
  const pct = (t: { right: number; total: number }) =>
    t.total ? Math.round((t.right / t.total) * 100) : 0;
  const simRows: Tally[] = sims.map((s) => {
    const r = answered[s.id] as SimulationReveal | undefined;
    return { name: s.title, right: r?.earned ?? 0, total: r?.possible ?? 0 };
  });
  const simPoints = {
    right: simRows.reduce((s, t) => s + t.right, 0),
    total: simRows.reduce((s, t) => s + t.total, 0),
  };

  return (
    <article className="card">
      <p className="meta">{session.kind === 'diagnostic' ? 'Diagnostic' : 'Session'} complete</p>
      {questions.length > 0 ? (
        <h2>
          {right} of {total} questions correct ({pct({ right, total })}%)
        </h2>
      ) : (
        <h2>
          {simPoints.right} of {plural(simPoints.total, 'point')} ({pct(simPoints)}%)
        </h2>
      )}
      {sims.length > 0 && questions.length > 0 && (
        <p className="muted">
          Simulations: {simPoints.right} of {plural(simPoints.total, 'point')} ({pct(simPoints)}%)
        </p>
      )}
      {weak.length > 0 && (
        <p>
          {session.kind === 'diagnostic'
            ? 'Your next sessions will lean toward '
            : 'Worth another look: '}
          {weak.join(', ')}.
        </p>
      )}
      {questions.length > 0 && (
        <>
          <TallyTable title="By blueprint area" rows={byArea} pct={pct} />
          <TallyTable title="By topic" rows={byTopic} pct={pct} />
        </>
      )}
      {sims.length > 0 && <TallyTable title="Simulations" unit="points" rows={simRows} pct={pct} />}
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
  unit = 'correct',
}: {
  title: string;
  rows: Tally[];
  pct: (t: Tally) => number;
  unit?: 'correct' | 'points';
}) {
  return (
    <table className="mastery">
      <thead>
        <tr>
          <th>{title}</th>
          <th>{unit === 'points' ? 'Points' : 'Correct'}</th>
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
