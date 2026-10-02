import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <section className="hero">
      <h1>Study for the CPA exam, free and in the open.</h1>
      <p>
        Blueprint-aligned questions and simulations, spaced repetition that finds your weak spots,
        and Claude, through your own account, to explain the why. Every question is open source and
        reviewed.
      </p>
      <Link to="/practice" className="button">
        Start practicing
      </Link>
    </section>
  );
}
