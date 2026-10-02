import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import type { PublicMcq, PublicTbs } from '@opencpa/schema';
import {
  api,
  errorMessage,
  type Exam,
  type ExamReport,
  type ExamResponse,
  type ExamStatus,
  type ExamSummary,
  type ExamTally,
  type Revealed,
  type SimulationReveal,
  type TaskResponse,
} from '../api';
import { Question } from './Practice';
import { SimulationPlayer } from './Simulation';

/** 3:59:07, or 12:05 under an hour. */
export function clockText(ms: number) {
  const total = Math.max(0, Math.ceil(ms / 1000));
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  const pad = (n: number) => String(n).padStart(2, '0');
  return h ? `${h}:${pad(m)}:${pad(s)}` : `${m}:${pad(s)}`;
}

const pct = (x: number) => `${Math.round(x * 100)}%`;
const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`;
const dateText = (ms: number) =>
  new Date(ms).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });

/** The Mock exam page: what to expect, the exam in progress, and past exams. */
export default function ExamPage() {
  const section = (useParams().section ?? 'FAR').toUpperCase();
  const navigate = useNavigate();
  const [status, setStatus] = useState<ExamStatus | null>(null);
  const [exam, setExam] = useState<Exam | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.examStatus(section).then(setStatus, (e: Error) => setError(errorMessage(e)));
  }, [section]);

  const finished = (id: string) => navigate(`/exam/${section}/${id}`);

  async function run(load: () => Promise<Exam>) {
    setBusy(true);
    setError(null);
    try {
      const e = await load();
      if (e.status === 'active') setExam(e);
      else finished(e.id);
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setBusy(false);
    }
  }

  if (exam) return <ExamRunner initial={exam} onFinished={finished} />;
  if (error) return <p className="error">Couldn’t load the mock exam: {error}</p>;
  if (!status) return <p className="muted">Loading…</p>;

  const { layout, active } = status;
  const simsPerExam = layout?.testlets
    .filter((t) => t.kind === 'tbs')
    .reduce((s, t) => s + t.count, 0);

  return (
    <section className="prose">
      <p className="meta crumbs">
        <Link to="/practice">Practice</Link> / Mock exam
      </p>
      <h1>{section} mock exam</h1>
      {!layout ? (
        <p>
          There’s no {section} mock exam yet. FAR comes first; other sections follow once they have
          enough questions and simulations.
        </p>
      ) : (
        <>
          <p>
            A full-length practice exam in the real exam’s format, timed, and scored at the end.
          </p>
          {active && (
            <article className="card resume">
              <h2>Exam in progress</h2>
              <p>
                Testlet {active.current + 1} of {layout.testlets.length},{' '}
                {clockText(active.clock.remainingMs)} left
                {active.clock.paused ? ' (paused)' : active.clock.onBreak ? ' (on a break)' : ''}.
                {!active.clock.paused &&
                  !active.clock.onBreak &&
                  ' The clock is running, as on the real exam.'}
              </p>
              <button
                className="button"
                disabled={busy}
                onClick={() => run(() => api.exam(active.id))}
              >
                Resume the exam
              </button>
            </article>
          )}
          <article className="card">
            <h2>What to expect</h2>
            <ul>
              <li>
                <b>{layout.testlets.length} testlets:</b> {testletList(layout.testlets)}.
              </li>
              <li>
                <b>{layout.minutes / 60} hours</b>, counting down. The clock runs on our server:
                leaving the page doesn’t stop it, but you can come back and pick up where you left
                off.
              </li>
              <li>
                <b>An optional {layout.breakMinutes}-minute break</b> after testlet{' '}
                {layout.breakAfter}. It doesn’t count against your time; minutes past{' '}
                {layout.breakMinutes} do.
              </li>
              <li>
                <b>Within a testlet</b> you can move freely, change answers, flag items for review
                and strike out choices. <b>Submitting a testlet locks it</b>: there’s no going back.
              </li>
              <li>
                <b>Nothing is graded or shown until the end.</b> Then you get your score, a
                breakdown by area, topic and skill, and every item with its answer and explanation.
              </li>
              <li>
                <b>Pause</b> if you’re interrupted. The items are hidden while paused, and the
                report shows how long and how often you paused, so you can tell a real-conditions
                run from a paused one.
              </li>
            </ul>
          </article>
          <p className="muted">
            Multiple choice and simulations count 50/50, as on the real exam. There’s no 0–99 score:
            the AICPA’s scaling isn’t public, so any number we gave would be made up. On the real
            exam, testlet 2 gets harder or easier depending on how testlet 1 went; here both are
            drawn the same way, since our questions don’t have calibrated difficulty yet.
          </p>
          {simsPerExam !== undefined && status.freshSimulations < simsPerExam && (
            <p className="muted">
              You’ve had {status.simulations - status.freshSimulations} of the {status.simulations}{' '}
              {section} simulations in earlier mock exams, so some in this one will repeat.
            </p>
          )}
          <button
            className="button"
            disabled={busy}
            onClick={() => {
              if (
                active &&
                !confirm(
                  'Start over? The exam in progress ends; the testlets you submitted still count toward your progress.',
                )
              )
                return;
              void run(() => api.startExam(section));
            }}
          >
            {active ? 'Start a new exam' : 'Start the exam'}
          </button>
          <p className="meta">The {layout.minutes / 60}-hour clock starts as soon as you begin.</p>
        </>
      )}
      {status.history.length > 0 && (
        <>
          <h2>Past mock exams</h2>
          <ExamHistory rows={status.history} />
        </>
      )}
    </section>
  );
}

/** "25 and 25 multiple-choice questions, then 2, 3 and 2 simulations". */
function testletList(testlets: { kind: 'mcq' | 'tbs'; count: number }[]) {
  const runs: { kind: 'mcq' | 'tbs'; counts: number[] }[] = [];
  for (const t of testlets) {
    const last = runs[runs.length - 1];
    if (last?.kind === t.kind) last.counts.push(t.count);
    else runs.push({ kind: t.kind, counts: [t.count] });
  }
  const and = (n: number[]) =>
    n.length > 1 ? `${n.slice(0, -1).join(', ')} and ${n[n.length - 1]}` : String(n[0]);
  return runs
    .map(
      (r) => `${and(r.counts)} ${r.kind === 'mcq' ? 'multiple-choice questions' : 'simulations'}`,
    )
    .join(', then ');
}

export function ExamHistory({ rows }: { rows: ExamSummary[] }) {
  return (
    <table className="mastery">
      <thead>
        <tr>
          <th>Date</th>
          <th>Multiple choice</th>
          <th>Simulations</th>
          <th>Combined</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id}>
            <td>
              <Link to={`/exam/${r.section}/${r.id}`}>
                {r.section} · {dateText(r.startedAt)}
              </Link>
              <div className="meta">
                {r.pauses ? `Paused ${plural(r.pauses, 'time')}` : 'No pauses'}
                {r.endedBy === 'time' ? ' · time ran out' : ''}
              </div>
            </td>
            <td>{pct(r.mcqPct)}</td>
            <td>{pct(r.simPct)}</td>
            <td>
              <b>{pct(r.combined)}</b>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

/** Strike-outs are a scratchpad: kept in this browser only, per exam. */
function useStrikes(examId: string) {
  const key = `opencpa:exam-strikes:${examId}`;
  const [strikes, setStrikes] = useState<Record<string, string[]>>(() => {
    try {
      return JSON.parse(localStorage.getItem(key) ?? '{}') as Record<string, string[]>;
    } catch {
      return {};
    }
  });
  function toggle(itemId: string, choice: string) {
    setStrikes((s) => {
      const list = s[itemId] ?? [];
      const next = {
        ...s,
        [itemId]: list.includes(choice) ? list.filter((c) => c !== choice) : [...list, choice],
      };
      try {
        localStorage.setItem(key, JSON.stringify(next));
      } catch {
        // Only a convenience.
      }
      return next;
    });
  }
  return [strikes, toggle] as const;
}

const isAnswered = (r: ExamResponse | undefined) =>
  !!r && ('selected' in r ? !!r.selected : Object.keys(r).length > 0);

/**
 * The exam screen. It covers the site's header and nav, keeps a local countdown in step with
 * the server's clock, and saves responses and flags a moment after each change.
 */
function ExamRunner({ initial, onFinished }: { initial: Exam; onFinished: (id: string) => void }) {
  const [exam, setExam] = useState(initial);
  const [received, setReceived] = useState(Date.now());
  const [now, setNow] = useState(Date.now());
  const [responses, setResponses] = useState(initial.responses);
  const [flags, setFlags] = useState(initial.flags);
  const [index, setIndex] = useState(0);
  const [confirming, setConfirming] = useState(false);
  const [skipBreak, setSkipBreak] = useState(false);
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [strikes, toggleStrike] = useStrikes(initial.id);
  /** Changes not yet sent to the server. */
  const pending = useRef(false);
  const latest = useRef({ responses, flags });
  latest.current = { responses, flags };
  const timeUpSent = useRef(false);

  /** Take the server's view of the exam, replacing local answers with what it saved. */
  function apply(e: Exam) {
    setExam(e);
    setReceived(Date.now());
    setResponses(e.responses);
    setFlags(e.flags);
    pending.current = false;
    if (e.status !== 'active') onFinished(e.id);
  }

  /** A 409 carries the exam as it now stands (ended, paused elsewhere…); show that. */
  function recover(err: unknown) {
    const text = (err as Error).message.replace(/^\d+ /, '');
    try {
      const body = JSON.parse(text) as { error?: string; exam?: Exam };
      if (body.exam) {
        apply(body.exam);
        setError(body.error ?? null);
        return;
      }
    } catch {
      // Not JSON.
    }
    setError(errorMessage(err));
  }

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);

  async function save() {
    if (!pending.current) return;
    pending.current = false;
    setSaving(true);
    try {
      const { responses: r, flags: f } = latest.current;
      const res = await api.saveExam(exam.id, exam.current, r, f);
      setExam((e) => ({ ...e, clock: res.clock }));
      setReceived(Date.now());
      setError(null);
    } catch (e) {
      recover(e);
    } finally {
      setSaving(false);
    }
  }

  useEffect(() => {
    if (!pending.current) return;
    const t = setTimeout(() => void save(), 800);
    return () => clearTimeout(t);
  }, [responses, flags]);

  function setResponse(id: string, r: ExamResponse | null) {
    pending.current = true;
    setResponses((prev) => {
      const next = { ...prev };
      if (r) next[id] = r;
      else delete next[id];
      return next;
    });
  }

  function toggleFlag(id: string) {
    pending.current = true;
    setFlags((f) => (f.includes(id) ? f.filter((x) => x !== id) : [...f, id]));
  }

  async function act(action: 'pause' | 'resume' | 'break/start' | 'break/end') {
    setBusy(true);
    try {
      await save();
      apply(await api.examAction(exam.id, action));
      setError(null);
    } catch (e) {
      recover(e);
    } finally {
      setBusy(false);
    }
  }

  async function submit() {
    setBusy(true);
    setConfirming(false);
    try {
      const { responses: r, flags: f } = latest.current;
      apply(await api.submitTestlet(exam.id, exam.current, r, f));
      setIndex(0);
      setError(null);
      window.scrollTo(0, 0);
    } catch (e) {
      recover(e);
    } finally {
      setBusy(false);
    }
  }

  // The local countdown, from the server's last reading.
  const c = exam.clock;
  const elapsed = now - received;
  const breakLeft = c.onBreak ? c.breakRemainingMs - elapsed : 0;
  const remaining = c.paused
    ? c.remainingMs
    : c.onBreak
      ? c.remainingMs - Math.max(0, elapsed - c.breakRemainingMs)
      : c.remainingMs - elapsed;

  // Out of time: submit the open testlet as it stands (the server ends the exam).
  useEffect(() => {
    if (remaining > 0 || timeUpSent.current || exam.status !== 'active') return;
    timeUpSent.current = true;
    void (async () => {
      if (exam.clock.onBreak) await api.examAction(exam.id, 'break/end').catch(() => null);
      await submit();
    })();
  }, [remaining <= 0]);

  const testlet = exam.testlets[exam.current]!;
  const items = exam.items ?? [];
  const item = items[Math.min(index, items.length - 1)];
  const kindLabel = testlet.kind === 'mcq' ? 'Question' : 'Simulation';
  const unanswered = items.flatMap((it, i) => (isAnswered(responses[it.id]) ? [] : [i + 1]));
  const flagged = items.flatMap((it, i) => (flags.includes(it.id) ? [i + 1] : []));

  const bar = (
    <div className="exam-bar">
      <b>{exam.section} mock exam</b>
      <span>
        Testlet {exam.current + 1} of {exam.testlets.length}
      </span>
      {item && !c.paused && !c.onBreak && (
        <span>
          {kindLabel} {index + 1} of {items.length}
        </span>
      )}
      <span className={`timer ${remaining < 5 * 60_000 ? 'low' : ''}`} aria-label="Time left">
        {clockText(remaining)}
      </span>
      <span className="meta">{saving || pending.current ? 'Saving…' : 'Saved'}</span>
      {!c.paused && !c.onBreak && (
        <button className="link" disabled={busy} onClick={() => act('pause')}>
          Pause
        </button>
      )}
    </div>
  );

  let body;
  if (c.paused) {
    body = (
      <article className="card exam-hold">
        <h2>Paused</h2>
        <p>
          The clock is stopped with {clockText(c.remainingMs)} left. The items stay hidden until you
          resume.
        </p>
        <p className="meta">
          Paused {plural(c.pauses, 'time')} so far. The report will show it, so you can tell this
          run from one under real conditions.
        </p>
        <button className="button" disabled={busy} onClick={() => act('resume')}>
          Resume
        </button>
      </article>
    );
  } else if (c.onBreak) {
    body = (
      <article className="card exam-hold">
        <h2>Break</h2>
        {breakLeft > 0 ? (
          <p>
            <span className="timer">{clockText(breakLeft)}</span> of break left. It doesn’t count
            against your exam time.
          </p>
        ) : (
          <p className="warn">
            Your break is over: the exam clock is running again ({clockText(-breakLeft)} past the
            break so far).
          </p>
        )}
        <button className="button" disabled={busy} onClick={() => act('break/end')}>
          Back to the exam
        </button>
      </article>
    );
  } else if (c.breakAvailable && !skipBreak) {
    body = (
      <article className="card exam-hold">
        <h2>Testlet {exam.current} submitted</h2>
        <p>
          You can take an optional {exam.layout.breakMinutes}-minute break now. It doesn’t count
          against your time; minutes past {exam.layout.breakMinutes} do. The break is only offered
          here.
        </p>
        <div className="row-start">
          <button className="button" disabled={busy} onClick={() => act('break/start')}>
            Take the break
          </button>
          <button className="link" onClick={() => setSkipBreak(true)}>
            Skip it and start testlet {exam.current + 1}
          </button>
        </div>
      </article>
    );
  } else if (!item) {
    body = <p className="muted">Loading…</p>;
  } else {
    const isFlagged = flags.includes(item.id);
    body = (
      <>
        <nav className="exam-nav" aria-label={`Testlet ${exam.current + 1} items`}>
          {items.map((it, i) => (
            <button
              key={it.id}
              className={[
                i === index ? 'current' : '',
                isAnswered(responses[it.id]) ? 'answered' : '',
                flags.includes(it.id) ? 'flagged' : '',
              ].join(' ')}
              aria-label={`${kindLabel} ${i + 1}${isAnswered(responses[it.id]) ? ', answered' : ''}${flags.includes(it.id) ? ', flagged' : ''}`}
              onClick={() => setIndex(i)}
            >
              {i + 1}
            </button>
          ))}
          <span className="meta">
            {items.length - unanswered.length} of {items.length} answered
            {flagged.length ? ` · ${flagged.length} flagged` : ''}
          </span>
        </nav>
        {item.type === 'mcq' ? (
          <ExamQuestion
            q={item}
            selected={(responses[item.id] as { selected?: string } | undefined)?.selected ?? null}
            struck={strikes[item.id] ?? []}
            onSelect={(id) => setResponse(item.id, { selected: id })}
            onStrike={(id) => toggleStrike(item.id, id)}
          />
        ) : (
          <SimulationPlayer
            key={item.id}
            sim={item}
            crumb={
              <>
                Simulation {index + 1} of {items.length}
              </>
            }
            initialResponses={responses[item.id] as Record<string, TaskResponse> | undefined}
            onResponses={(r) => setResponse(item.id, Object.keys(r).length ? r : null)}
          />
        )}
        <div className="row">
          <button className="link" disabled={index === 0} onClick={() => setIndex(index - 1)}>
            ← Previous
          </button>
          <button className="link" onClick={() => toggleFlag(item.id)}>
            {isFlagged ? '⚑ Flagged (remove)' : '⚐ Flag for review'}
          </button>
          <button
            className="link"
            disabled={index >= items.length - 1}
            onClick={() => setIndex(index + 1)}
          >
            Next →
          </button>
        </div>
        {confirming ? (
          <article className="card exam-confirm">
            <h2>Submit testlet {exam.current + 1}?</h2>
            <p>Once submitted, you can’t come back to it.</p>
            {unanswered.length > 0 && (
              <p className="warn">
                Unanswered: {kindLabel.toLowerCase()} {unanswered.join(', ')}.
              </p>
            )}
            {flagged.length > 0 && <p>Flagged for review: {flagged.join(', ')}.</p>}
            <div className="row-start">
              <button className="button" disabled={busy} onClick={() => void submit()}>
                {exam.current === exam.testlets.length - 1
                  ? 'Submit and finish the exam'
                  : 'Submit testlet'}
              </button>
              <button className="link" onClick={() => setConfirming(false)}>
                Keep working
              </button>
            </div>
          </article>
        ) : (
          <button className="button" disabled={busy} onClick={() => setConfirming(true)}>
            Submit testlet {exam.current + 1}…
          </button>
        )}
      </>
    );
  }

  return (
    <div className="exam-screen">
      {bar}
      <div className="exam-body">
        {error && <p className="error">{error}</p>}
        {body}
      </div>
    </div>
  );
}

/** A multiple-choice question as the exam shows it: pick one, strike out others, no feedback. */
function ExamQuestion({
  q,
  selected,
  struck,
  onSelect,
  onStrike,
}: {
  q: PublicMcq;
  selected: string | null;
  struck: string[];
  onSelect: (id: string) => void;
  onStrike: (id: string) => void;
}) {
  return (
    <article className="card">
      <p className="stem">{q.stem}</p>
      <ol className="choices">
        {q.choices.map((c) => {
          const out = struck.includes(c.id);
          return (
            <li key={c.id} className="exam-choice">
              <button
                className={`choice ${c.id === selected ? 'picked' : ''} ${out ? 'struck' : ''}`}
                aria-pressed={c.id === selected}
                onClick={() => onSelect(c.id)}
              >
                <b>{c.id}.</b> {c.text}
              </button>
              <button
                className="link strike"
                aria-pressed={out}
                title={out ? 'Restore this choice' : 'Strike out this choice'}
                onClick={() => onStrike(c.id)}
              >
                {out ? 'Restore' : 'Strike'}
              </button>
            </li>
          );
        })}
      </ol>
    </article>
  );
}

/** Questions and simulations scored 50/50, or whichever the row has. */
const rowScore = (t: ExamTally) => {
  const q = t.total ? t.right / t.total : null;
  const s = t.possible ? t.earned / t.possible : null;
  return q !== null && s !== null ? (q + s) / 2 : (q ?? s ?? 0);
};

function ReportTable({
  title,
  rows,
  weights,
}: {
  title: string;
  rows: ExamTally[];
  weights?: boolean;
}) {
  return (
    <table className="mastery">
      <thead>
        <tr>
          <th>{title}</th>
          <th>Questions</th>
          <th>Simulation points</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((t) => (
          <tr key={t.name}>
            <td>
              {t.name}
              {weights && t.weight != null && (
                <div className="meta">Blueprint weight about {t.weight}%</div>
              )}
            </td>
            <td>{t.total ? `${t.right} of ${t.total}` : '—'}</td>
            <td>{t.possible ? `${t.earned} of ${t.possible}` : '—'}</td>
            <td>
              <div className="bar">
                <span style={{ width: pct(rowScore(t)) }} />
              </div>
              {pct(rowScore(t))}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

/** The score report, with every item's key and explanation. */
export function ExamReportPage() {
  const { section = 'FAR', id = '' } = useParams();
  const [report, setReport] = useState<ExamReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [testlet, setTestlet] = useState(0);
  const [open, setOpen] = useState<number | null>(null);

  useEffect(() => {
    api.examReport(id).then(setReport, (e: Error) => setError(errorMessage(e)));
  }, [id]);

  if (error) return <p className="error">Couldn’t load the report: {error}</p>;
  if (!report) return <p className="muted">Loading…</p>;

  const r = report;
  const list = r.review[testlet] ?? [];
  const shown = open === null ? null : list[open];
  const kind = r.layout.testlets[testlet]?.kind;

  return (
    <section className="exam-report">
      <p className="meta crumbs">
        <Link to="/practice">Practice</Link> / <Link to={`/exam/${section}`}>Mock exam</Link> /{' '}
        {dateText(r.startedAt)}
      </p>
      <h1>
        {r.section} mock exam: {pct(r.combined)}
      </h1>
      <div className="tiles">
        <div className="card">
          <p className="meta">Multiple choice</p>
          <p className="tile-code">{pct(r.mcqPct)}</p>
          <p className="meta">
            {r.mcq.right} of {r.mcq.total} correct
          </p>
        </div>
        <div className="card">
          <p className="meta">Simulations</p>
          <p className="tile-code">{pct(r.simPct)}</p>
          <p className="meta">
            {r.sim.earned} of {r.sim.possible} points
          </p>
        </div>
        <div className="card">
          <p className="meta">Combined (50/50)</p>
          <p className="tile-code">{pct(r.combined)}</p>
          <p className="meta">As the real exam weights them</p>
        </div>
      </div>
      <p className="muted">
        No 0–99 score: the AICPA’s scaling isn’t public, so any number we gave would be made up.
        {r.endedBy === 'time' &&
          ' Time ran out: the open testlet was submitted as it stood, and later testlets scored zero.'}
      </p>

      <h2>Time</h2>
      <p>
        {clockText(r.usedMs)} used of {r.layout.minutes / 60}:00:00.{' '}
        {r.pauses
          ? `Paused ${plural(r.pauses, 'time')} for ${clockText(r.pausedMs)} in all, so not quite real exam conditions.`
          : 'No pauses: real exam conditions.'}
      </p>
      <table className="mastery">
        <thead>
          <tr>
            <th>Testlet</th>
            <th>Items</th>
            <th>Time used</th>
          </tr>
        </thead>
        <tbody>
          {r.testlets.map((t, i) => (
            <tr key={i}>
              <td>Testlet {i + 1}</td>
              <td>{plural(t.count, t.kind === 'mcq' ? 'question' : 'simulation')}</td>
              <td>{t.usedMs === null ? 'Not reached' : clockText(t.usedMs)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>By blueprint area</h2>
      <ReportTable title="Area" rows={r.byArea} weights />
      <h2>By skill</h2>
      <ReportTable title="Skill" rows={r.bySkill} />
      <h2>By topic</h2>
      <ReportTable title="Topic" rows={[...r.byTopic].sort((a, b) => rowScore(a) - rowScore(b))} />

      <h2>Review</h2>
      <div className="tabs">
        {r.review.map((_, i) => (
          <button
            key={i}
            className={i === testlet ? 'active' : ''}
            onClick={() => {
              setTestlet(i);
              setOpen(null);
            }}
          >
            Testlet {i + 1}
          </button>
        ))}
      </div>
      <nav className="exam-nav" aria-label="Review items">
        {list.map((x, i) => {
          const full =
            x.item.type === 'mcq'
              ? x.result.correct
              : (x.result as SimulationReveal).earned === (x.result as SimulationReveal).possible;
          return (
            <button
              key={x.item.id}
              className={[
                i === open ? 'current' : '',
                !x.answered ? '' : full ? 'right' : 'wrong',
                x.flagged ? 'flagged' : '',
              ].join(' ')}
              onClick={() => setOpen(i === open ? null : i)}
            >
              {i + 1}
            </button>
          );
        })}
      </nav>
      <p className="meta">
        Green: right. Red: wrong or partial. Plain: not answered. A flag marks the items you
        flagged.
      </p>
      {shown && (
        <>
          <p className="meta">
            {kind === 'mcq' ? 'Question' : 'Simulation'} {open! + 1}
            {shown.flagged ? ' · you flagged this one' : ''}
            {!shown.answered ? ' · not answered' : ''}
          </p>
          {shown.item.type === 'mcq' ? (
            <Question
              q={shown.item}
              selected={(shown.result as Revealed).selected || null}
              result={shown.result as Revealed}
              onSelect={() => undefined}
            />
          ) : (
            <SimulationPlayer
              key={shown.item.id}
              sim={shown.item as PublicTbs}
              crumb={<>Simulation · {shown.item.blueprint.topic}</>}
              previous={shown.result as SimulationReveal}
            />
          )}
        </>
      )}
    </section>
  );
}
