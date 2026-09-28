import { useEffect, useState } from 'react';
import { api, type Mastery } from '../api';

export default function Progress() {
  const [rows, setRows] = useState<Mastery[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.mastery().then(setRows, (e: Error) => setError(e.message));
  }, []);

  if (error) return <p className="error">Couldn’t load progress: {error}</p>;
  if (!rows) return <p className="muted">Loading…</p>;
  if (rows.length === 0)
    return (
      <p className="muted">
        Answer a few questions and your mastery by blueprint area will show up here.
      </p>
    );

  return (
    <section>
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
    </section>
  );
}
