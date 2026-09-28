import { useEffect, useRef, useState } from 'react';
import type { PublicMcq } from '@opencpa/schema';
import { api, SECTIONS, type AttemptResult } from '../api';

export default function Practice() {
  const [section, setSection] = useState<string>('FAR');
  const [questions, setQuestions] = useState<PublicMcq[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<AttemptResult | null>(null);
  const started = useRef(Date.now());

  useEffect(() => {
    setQuestions(null);
    setError(null);
    setIndex(0);
    setResult(null);
    setSelected(null);
    api.questions(section).then(setQuestions, (e: Error) => setError(e.message));
  }, [section]);

  const q = questions?.[index];

  async function submit() {
    if (!q || !selected) return;
    try {
      setResult(await api.attempt(q.id, selected, Date.now() - started.current));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  function next() {
    setIndex((i) => i + 1);
    setSelected(null);
    setResult(null);
    started.current = Date.now();
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
      {!questions && !error && <p className="muted">Loading…</p>}
      {questions && questions.length === 0 && (
        <p className="muted">
          No reviewed {section} questions yet. They’re being added — check back soon.
        </p>
      )}
      {questions && questions.length > 0 && !q && <p>You’ve finished this set. Nice work.</p>}

      {q && (
        <article className="card">
          <p className="meta">
            {q.blueprint.topic} · {q.blueprint.skill} · {index + 1} of {questions!.length}
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
                    onClick={() => setSelected(c.id)}
                  >
                    <b>{c.id}.</b> {c.text}
                  </button>
                  {result && <p className="rationale">{result.rationales[c.id]}</p>}
                </li>
              );
            })}
          </ol>
          {!result ? (
            <button className="button" disabled={!selected} onClick={submit}>
              Submit
            </button>
          ) : (
            <>
              <p className={result.correct ? 'right-text' : 'wrong-text'}>
                {result.correct ? 'Correct.' : `Not quite — the answer is ${result.answer}.`}
              </p>
              <p>{result.explanation}</p>
              <button className="button" onClick={next}>
                Next question
              </button>
            </>
          )}
        </article>
      )}
    </section>
  );
}
