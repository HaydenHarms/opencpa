import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import type { PublicTbs } from '@opencpa/schema';
import { api, SECTIONS } from '../api';

export default function Simulations() {
  const [section, setSection] = useState<string>('FAR');
  const [sims, setSims] = useState<PublicTbs[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setSims(null);
    setError(null);
    api.simulations(section).then(setSims, (e: Error) => setError(e.message));
  }, [section]);

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
      {!sims && !error && <p className="muted">Loading…</p>}
      {sims && sims.length === 0 && (
        <p className="muted">
          No reviewed {section} simulations yet. They’re being written — check back soon.
        </p>
      )}
      {sims && sims.length > 0 && (
        <ul className="sim-list">
          {sims.map((t) => (
            <li key={t.id}>
              <Link to={`/simulations/${t.id}`} className="card sim-link">
                <b>{t.title}</b>
                <span className="meta">
                  {t.blueprint.topic} · {t.tasks.length} task{t.tasks.length === 1 ? '' : 's'} ·{' '}
                  {t.tasks.reduce((n, task) => n + task.points, 0)} points
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
