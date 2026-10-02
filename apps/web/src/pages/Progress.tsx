import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, type ExamSummary, type LibrarySection, type Mastery } from '../api';
import { ExamHistory } from './Exam';

export default function Progress() {
  const [rows, setRows] = useState<Mastery[] | null>(null);
  const [library, setLibrary] = useState<LibrarySection[] | null>(null);
  const [exams, setExams] = useState<ExamSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fail = (e: Error) => setError(e.message);
    api.mastery().then(setRows, fail);
    api.library().then(setLibrary, fail);
    api.examHistory().then(setExams, () => setExams([]));
  }, []);

  if (error) return <p className="error">Couldn’t load progress: {error}</p>;
  if (!rows || !library) return <p className="muted">Loading…</p>;
  if (rows.length === 0)
    return (
      <p className="muted">
        Answer a few questions in <Link to="/practice">Practice</Link> or the{' '}
        <Link to="/library">Library</Link> and your mastery will show up here.
      </p>
    );

  const started = library.filter((s) => s.attempts > 0);

  return (
    <section>
      <h2>Coverage</h2>
      <table className="mastery">
        <thead>
          <tr>
            <th>Section</th>
            <th>Items seen</th>
            <th>Attempts</th>
            <th>Correct</th>
          </tr>
        </thead>
        <tbody>
          {started.map((s) => {
            const total = s.questions + s.simulations;
            return (
              <tr key={s.section}>
                <td>
                  <Link to={`/library/${s.section}`}>{s.section}</Link>
                </td>
                <td>
                  <div className="bar">
                    <span style={{ width: `${total ? (s.seen / total) * 100 : 0}%` }} />
                  </div>
                  {s.seen} of {total}
                </td>
                <td>{s.attempts}</td>
                <td>{s.accuracy === null ? '—' : `${Math.round(s.accuracy * 100)}%`}</td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {exams.length > 0 && (
        <>
          <h2>Mock exams</h2>
          <ExamHistory rows={exams} />
        </>
      )}

      <h2>Mastery by blueprint area</h2>
      <table className="mastery">
        <thead>
          <tr>
            <th>Section</th>
            <th>Area</th>
            <th>Attempts</th>
            <th>Mastery</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.section + r.area}>
              <td>{r.section}</td>
              <td>{r.area}</td>
              <td>{r.attempts}</td>
              <td>
                <div className="bar">
                  <span style={{ width: `${Math.round(r.score * 100)}%` }} />
                </div>
                {Math.round(r.score * 100)}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {started.map((s) => {
        const topics = s.topics
          .filter((t) => t.mastery !== null)
          .sort((a, b) => a.mastery! - b.mastery! || b.attempts - a.attempts);
        return (
          <div key={s.section}>
            <h2>{s.section} mastery by topic</h2>
            <p className="muted">Weakest first. Pick a topic to practice it in the Library.</p>
            <table className="mastery">
              <thead>
                <tr>
                  <th>Topic</th>
                  <th>Seen</th>
                  <th>Mastery</th>
                </tr>
              </thead>
              <tbody>
                {topics.map((t) => (
                  <tr key={t.topic}>
                    <td>
                      <Link to={`/library/${s.section}/topic/${encodeURIComponent(t.topic)}`}>
                        {t.topic}
                      </Link>
                    </td>
                    <td>
                      {t.seen} of {t.questions + t.simulations}
                    </td>
                    <td>
                      <div className="bar">
                        <span style={{ width: `${Math.round(t.mastery! * 100)}%` }} />
                      </div>
                      {Math.round(t.mastery! * 100)}%
                      <div className="meta">
                        {t.correct} of {t.attempts} correct
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      })}
    </section>
  );
}
