import { Link, NavLink, Route, Routes } from 'react-router-dom';
import AccountPage, { SigninDone, SigninEmail, useAuthStatus } from './pages/Account';
import Claude from './pages/Claude';
import { Privacy, Terms } from './pages/Legal';
import Home from './pages/Home';
import {
  LibraryHome,
  LibraryQuestionPage,
  LibrarySectionPage,
  LibraryTopicPage,
} from './pages/Library';
import Practice from './pages/Practice';
import Progress from './pages/Progress';
import Simulation from './pages/Simulation';
import Simulations from './pages/Simulations';

export default function App() {
  const { status } = useAuthStatus();
  return (
    <div className="shell">
      <header className="nav">
        <NavLink to="/" className="brand">
          OpenCPA
        </NavLink>
        <nav>
          <NavLink to="/practice">Practice</NavLink>
          <NavLink to="/simulations">Simulations</NavLink>
          <NavLink to="/library">Library</NavLink>
          <NavLink to="/progress">Progress</NavLink>
          <NavLink to="/claude">Claude</NavLink>
          <NavLink to="/account">{status?.account ? 'Account' : 'Sign in'}</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/simulations" element={<Simulations />} />
          <Route path="/simulations/:id" element={<Simulation />} />
          <Route path="/library" element={<LibraryHome />} />
          <Route path="/library/:section" element={<LibrarySectionPage />} />
          <Route path="/library/:section/topic/:topic" element={<LibraryTopicPage />} />
          <Route path="/library/:section/q/:id" element={<LibraryQuestionPage />} />
          <Route path="/progress" element={<Progress />} />
          <Route path="/claude" element={<Claude />} />
          <Route path="/account" element={<AccountPage />} />
          <Route path="/signin/done" element={<SigninDone />} />
          <Route path="/signin/email" element={<SigninEmail />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/terms" element={<Terms />} />
        </Routes>
      </main>
      <footer className="footer">
        <span>OpenCPA is free and open source. Not affiliated with the AICPA or NASBA.</span>
        <span>
          <Link to="/terms">Terms</Link>
          <Link to="/privacy">Privacy</Link>
          <a href="https://github.com/HaydenHarms/opencpa">GitHub</a>
        </span>
      </footer>
    </div>
  );
}
