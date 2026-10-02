/**
 * Library: browse every exam, drill into its blueprint topics, practice any topic, and
 * look up any question in the archive. Every answer here is a normal attempt, so it feeds
 * mastery, review scheduling and the Progress page.
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import type { PublicTbs } from '@opencpa/schema';
import {
  api,
  SECTION_NAMES,
  type LibraryEntry,
  type LibraryQuestion,
  type LibrarySection,
  type LibraryTopic,
  type Revealed,
  type Session,
  type SessionStatus,
} from '../api';
import { Question, SessionRunner, StartPanel } from './Practice';
import { makeSearch } from '../search';

const pct = (x: number) => `${Math.round(x * 100)}%`;
const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? '' : 's'}`;
const topicPath = (section: string, topic: string) =>
  `/library/${section}/topic/${encodeURIComponent(topic)}`;
const simPath = (section: string, id: string) => `/library/${section}/sim/${id}`;

function useLibrary() {
  const [data, setData] = useState<LibrarySection[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api.library().then(setData, (e: Error) => setError(e.message));
  }, []);
  return { data, error };
}

function Crumbs({ section, topic }: { section?: string; topic?: string }) {
  return (
    <p className="meta crumbs">
      <Link to="/library">Library</Link>
      {section && (
        <>
          {' / '}
          {topic ? <Link to={`/library/${section}`}>{section}</Link> : section}
        </>
      )}
      {section && topic && <> / {topic}</>}
    </p>
  );
}

function Meter({ value }: { value: number | null }) {
  return (
    <span className="meter-row">
      <span className="bar">
        <span style={{ width: `${Math.round((value ?? 0) * 100)}%` }} />
      </span>
      {value === null ? 'Not started' : pct(value)}
    </span>
  );
}

let searchIndex: Promise<ReturnType<typeof makeSearch>> | null = null;
/** The search index loads once per page load, on first use. */
function loadSearch() {
  searchIndex ??= api.searchIndex().then(makeSearch);
  searchIndex.catch(() => (searchIndex = null));
  return searchIndex;
}

/**
 * Library search box. With a query it shows ranked topics and questions instead of the
 * page's tiles; `children` render when the box is empty.
 */
function LibrarySearch({ section, children }: { section?: string; children: React.ReactNode }) {
  const [query, setQuery] = useState('');
  const [search, setSearch] = useState<ReturnType<typeof makeSearch> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const results = useMemo(
    () => (search && query.trim() ? search(query, section) : null),
    [search, query, section],
  );

  function begin() {
    if (!search)
      loadSearch().then(
        // Wrapped, because React would treat a bare function as a state updater.
        (fn) => setSearch(() => fn),
        (e: Error) => setError(e.message),
      );
  }

  return (
    <>
      <input
        className="search"
        type="search"
        placeholder={
          section
            ? `Search ${section} topics and questions…`
            : 'Search topics and questions, e.g. fixed assets, DTL, ASC 842, lawsuit…'
        }
        value={query}
        onFocus={begin}
        onChange={(e) => {
          begin();
          setQuery(e.target.value);
        }}
      />
      {error && <p className="error">Search isn’t available right now: {error}</p>}
      {!query.trim() ? (
        children
      ) : !results ? (
        <p className="muted">Loading search…</p>
      ) : results.topics.length === 0 && results.items.length === 0 ? (
        <p className="muted">
          Nothing matches “{query}”. Try a broader term or a related one (for example “leases”
          instead of a specific lease clause).
        </p>
      ) : (
        <>
          {results.topics.length > 0 && (
            <>
              <h3 className="area-head">Topics</h3>
              <div className="tiles">
                {results.topics.map((t) => (
                  <Link
                    key={t.section + t.topic}
                    to={topicPath(t.section, t.topic)}
                    className="card tile"
                  >
                    <span className="meta">
                      {t.section} · {t.area}
                    </span>
                    <b>{t.topic}</b>
                    <span className="meta">
                      {t.matches
                        ? `${plural(t.matches, 'matching item')} of ${t.items}`
                        : `Related topic · ${plural(t.items, 'item')}`}
                    </span>
                  </Link>
                ))}
              </div>
            </>
          )}
          {results.items.length > 0 && (
            <>
              <h3 className="area-head">Questions</h3>
              <ul className="sim-list">
                {results.items.map(({ doc }) => (
                  <li key={doc.id}>
                    <Link
                      to={
                        doc.type === 'tbs'
                          ? simPath(doc.section, doc.id)
                          : `/library/${doc.section}/q/${doc.id}`
                      }
                      className="card sim-link"
                    >
                      <span>
                        {doc.type === 'tbs' && <b>Simulation · </b>}
                        {doc.title ??
                          (doc.text.length > 160
                            ? doc.text.slice(0, 157).trimEnd() + '…'
                            : doc.text)}
                      </span>
                      <span className="meta">
                        {doc.section} · {doc.topic} · {doc.skill}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </>
          )}
        </>
      )}
    </>
  );
}

/** /library — one tile per exam section. */
export function LibraryHome() {
  const { data, error } = useLibrary();
  if (error) return <p className="error">Couldn’t load the library: {error}</p>;
  if (!data) return <p className="muted">Loading…</p>;
  return (
    <section>
      <h2>Library</h2>
      <p className="muted">
        Every exam, every blueprint topic, every reviewed question and every simulation. Pick an
        exam to browse its topics and simulations, practice one topic, or look up any question
        you’ve answered.
      </p>
      <LibrarySearch>
        <div className="tiles">
          {data.map((s) => {
            const total = s.questions + s.simulations;
            return (
              <Link
                key={s.section}
                to={`/library/${s.section}`}
                className={`card tile ${total ? '' : 'empty'}`}
              >
                <span className="tile-code">{s.section}</span>
                <b>{SECTION_NAMES[s.section]}</b>
                <span className="meta">
                  {total
                    ? `${plural(s.questions, 'question')} · ${plural(s.simulations, 'simulation')} · ${plural(s.topics.length, 'topic')}`
                    : 'Coming soon'}
                </span>
                {total > 0 && (
                  <>
                    <span className="meta">
                      Seen {s.seen} of {total}
                    </span>
                    <div className="progress">
                      <span style={{ width: `${(s.seen / total) * 100}%` }} />
                    </div>
                  </>
                )}
              </Link>
            );
          })}
        </div>
      </LibrarySearch>
    </section>
  );
}

/** The section's simulations, as a flat list. */
function SectionSimulations({ section }: { section: string }) {
  const [sims, setSims] = useState<PublicTbs[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setSims(null);
    setError(null);
    api.simulations(section).then(setSims, (e: Error) => setError(e.message));
  }, [section]);

  if (error) return <p className="error">Couldn’t load simulations: {error}</p>;
  if (!sims) return <p className="muted">Loading…</p>;
  if (sims.length === 0)
    return <p className="muted">No reviewed {section} simulations yet. They’re being written.</p>;
  return (
    <ul className="sim-list">
      {sims.map((t) => (
        <li key={t.id}>
          <Link to={simPath(section, t.id)} className="card sim-link">
            <b>{t.title}</b>
            <span className="meta">
              {t.blueprint.topic} · {plural(t.tasks.length, 'task')} ·{' '}
              {plural(
                t.tasks.reduce((n, task) => n + task.points, 0),
                'point',
              )}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}

/** /simulations/:id (the old address) — send to the simulation's place in the Library. */
export function LegacySimulationRedirect() {
  const { id = '' } = useParams();
  const [to, setTo] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    api.simulation(id).then(
      (sim) => setTo(simPath(sim.blueprint.section, sim.id)),
      (e: Error) => setError(e.message),
    );
  }, [id]);
  if (error) return <p className="error">Couldn’t load this simulation: {error}</p>;
  return to ? <Navigate to={to} replace /> : <p className="muted">Loading…</p>;
}

/** /library/:section — the section's topics, grouped by blueprint area, and its simulations. */
export function LibrarySectionPage() {
  const { section = '' } = useParams();
  const { data, error } = useLibrary();
  const [view, setView] = useState<'topics' | 'simulations'>('topics');
  if (error) return <p className="error">Couldn’t load the library: {error}</p>;
  if (!data) return <p className="muted">Loading…</p>;
  const s = data.find((x) => x.section === section.toUpperCase());
  if (!s) return <p className="error">No exam called {section}.</p>;

  const areas = new Map<string, LibraryTopic[]>();
  for (const t of s.topics) areas.set(t.area, [...(areas.get(t.area) ?? []), t]);

  return (
    <section>
      <Crumbs section={s.section} />
      <h2>
        {s.section} · {SECTION_NAMES[s.section]}
      </h2>
      {s.topics.length === 0 ? (
        <p className="muted">No reviewed {s.section} questions yet. They’re being written.</p>
      ) : (
        <p className="muted">
          {plural(s.topics.length, 'topic')} · seen {s.seen} of {s.questions + s.simulations} items
          {s.accuracy !== null && <> · {pct(s.accuracy)} correct overall</>}
        </p>
      )}
      {s.topics.length > 0 && (
        <LibrarySearch section={s.section}>
          {s.simulations > 0 && (
            <div className="tabs">
              <button
                className={view === 'topics' ? 'active' : ''}
                onClick={() => setView('topics')}
              >
                Topics {s.topics.length}
              </button>
              <button
                className={view === 'simulations' ? 'active' : ''}
                onClick={() => setView('simulations')}
              >
                Simulations {s.simulations}
              </button>
            </div>
          )}
          {view === 'simulations' && s.simulations > 0 ? (
            <SectionSimulations section={s.section} />
          ) : (
            [...areas].map(([area, topics]) => (
              <div key={area}>
                <h3 className="area-head">{area}</h3>
                <div className="tiles">
                  {topics.map((t) => (
                    <Link key={t.topic} to={topicPath(s.section, t.topic)} className="card tile">
                      <b>{t.topic}</b>
                      <span className="meta">
                        {plural(t.questions, 'question')}
                        {t.simulations > 0 && ` · ${plural(t.simulations, 'simulation')}`}
                      </span>
                      <span className="meta">
                        Seen {t.seen} of {t.questions + t.simulations}
                      </span>
                      <Meter value={t.mastery} />
                    </Link>
                  ))}
                </div>
              </div>
            ))
          )}
        </LibrarySearch>
      )}
    </section>
  );
}

type Filter = 'all' | 'new' | 'missed' | 'correct';

/** /library/:section/topic/:topic — practice the topic, and the archive of its items. */
export function LibraryTopicPage() {
  const { section: rawSection = '', topic = '' } = useParams();
  const section = rawSection.toUpperCase();
  const [status, setStatus] = useState<SessionStatus | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  /** Whether the session runner is showing. Landing on the topic page shows the topic, with a resume card. */
  const [open, setOpen] = useState(false);
  const [entries, setEntries] = useState<LibraryEntry[] | null>(null);
  const [filter, setFilter] = useState<Filter>('all');
  const [error, setError] = useState<string | null>(null);
  const fail = (e: Error) => setError(e.message);

  function load() {
    setStatus(null);
    setEntries(null);
    api.currentSession(section, { topic }).then((st) => {
      setStatus(st);
      setSession(st.session);
    }, fail);
    api.libraryItems(section, topic).then(setEntries, fail);
  }
  useEffect(load, [section, topic]);

  async function start(size: number) {
    setError(null);
    try {
      setSession(await api.startSession(section, size, { topic }));
      setOpen(true);
    } catch (e) {
      fail(e as Error);
    }
  }

  if (session && open)
    return (
      <section>
        <Crumbs section={section} topic={topic} />
        <button
          className="link"
          onClick={() => {
            // Leave the session without ending it; it resumes from the topic page.
            setOpen(false);
            load();
          }}
        >
          ← Back to {topic}
        </button>
        <SessionRunner
          key={session.id}
          session={session}
          onError={fail}
          onNew={() => {
            setSession(null);
            setOpen(false);
            load();
          }}
        />
        {error && <p className="error">{error}</p>}
      </section>
    );

  const shown = (entries ?? []).filter((e) =>
    filter === 'all'
      ? true
      : filter === 'new'
        ? e.attempts === 0
        : filter === 'missed'
          ? e.lastCorrect === false
          : e.lastCorrect === true,
  );
  const count = (f: Filter) =>
    (entries ?? []).filter((e) =>
      f === 'new' ? !e.attempts : f === 'missed' ? e.lastCorrect === false : e.lastCorrect === true,
    ).length;

  return (
    <section>
      <Crumbs section={section} topic={topic} />
      <h2>{topic}</h2>
      {error && <p className="error">Couldn’t reach the API: {error}</p>}
      {!status && !error && <p className="muted">Loading…</p>}
      {session && session.status === 'active' && (
        <article className="card resume">
          <h2>Session in progress</h2>
          <p className="muted">
            {Object.keys(session.answered).length} of {session.items.length} answered. Pick up where
            you left off, or start a new session below (your answers so far still count).
          </p>
          <button className="button" onClick={() => setOpen(true)}>
            Resume session
          </button>
        </article>
      )}
      {status && (
        <StartPanel
          section={topic}
          status={status}
          onStart={start}
          title={`Practice ${topic}`}
          blurb="A session on this topic only, starting with questions you haven’t seen or are due for review. Your answers count toward your overall progress."
        />
      )}

      {entries && entries.length > 0 && (
        <>
          <h3 className="area-head">Question archive</h3>
          <div className="tabs">
            {(['all', 'new', 'missed', 'correct'] as const).map((f) => (
              <button key={f} className={f === filter ? 'active' : ''} onClick={() => setFilter(f)}>
                {f === 'all'
                  ? `All ${entries.length}`
                  : f === 'new'
                    ? `Unanswered ${count('new')}`
                    : f === 'missed'
                      ? `Missed ${count('missed')}`
                      : `Correct ${count('correct')}`}
              </button>
            ))}
          </div>
          {shown.length === 0 && <p className="muted">Nothing here yet.</p>}
          <ul className="sim-list">
            {shown.map((e) => (
              <li key={e.id}>
                <Link
                  to={e.type === 'tbs' ? simPath(section, e.id) : `/library/${section}/q/${e.id}`}
                  className="card sim-link"
                >
                  <span>
                    {e.type === 'tbs' && <b>Simulation · </b>}
                    {e.title}
                  </span>
                  <span className="meta">
                    {e.blueprint.skill} ·{' '}
                    {e.attempts === 0 ? (
                      'Not answered yet'
                    ) : (
                      <>
                        {plural(e.attempts, 'attempt')} · last{' '}
                        <span className={e.lastCorrect ? 'right-text' : 'wrong-text'}>
                          {e.type === 'tbs' && e.lastScore !== null
                            ? pct(e.lastScore)
                            : e.lastCorrect
                              ? 'correct'
                              : 'missed'}
                        </span>
                      </>
                    )}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

/** /library/:section/q/:id — one archive question: review the last attempt or answer it. */
export function LibraryQuestionPage() {
  const { section = '', id = '' } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState<LibraryQuestion | null>(null);
  const [mode, setMode] = useState<'review' | 'answer'>('review');
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<Revealed | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const started = useRef(Date.now());

  function load() {
    setData(null);
    setResult(null);
    setSelected(null);
    api.libraryQuestion(id).then(
      (d) => {
        setData(d);
        setMode(d.last ? 'review' : 'answer');
        started.current = Date.now();
      },
      (e: Error) => setError(e.message),
    );
  }
  useEffect(load, [id]);

  async function submit() {
    if (!data || !selected || busy) return;
    setBusy(true);
    try {
      setResult(
        await api.attemptOutsideSession(
          id,
          selected,
          Date.now() - started.current,
          data.item.variant,
        ),
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  if (error) return <p className="error">Couldn’t load this question: {error}</p>;
  if (!data) return <p className="muted">Loading…</p>;
  const { item, last } = data;
  const topic = item.blueprint.topic;
  const back = (
    <button className="link" onClick={() => navigate(topicPath(section.toUpperCase(), topic))}>
      ← Back to {topic}
    </button>
  );

  return (
    <section>
      <Crumbs section={section.toUpperCase()} topic={topic} />
      <p className="meta">
        {data.attempts === 0
          ? 'You haven’t answered this one yet.'
          : `Answered ${plural(data.attempts, 'time')} · ${data.correct} correct`}
      </p>
      {mode === 'review' && last ? (
        <>
          <p className="meta">Your last attempt, {new Date(last.at).toLocaleDateString()}:</p>
          <Question q={last.item} selected={last.selected} result={last} onSelect={() => {}} />
          <div className="row">
            {back}
            <button className="button" onClick={() => setMode('answer')}>
              Answer it again{item.variant !== last.item.variant ? ' (new numbers)' : ''}
            </button>
          </div>
        </>
      ) : (
        <>
          <Question
            q={item}
            selected={result?.selected ?? selected}
            result={result ?? undefined}
            onSelect={setSelected}
          />
          <div className="row">
            {back}
            {result ? (
              <button className="button" onClick={load}>
                Done
              </button>
            ) : (
              <button className="button" disabled={!selected || busy} onClick={submit}>
                Submit
              </button>
            )}
          </div>
        </>
      )}
    </section>
  );
}
