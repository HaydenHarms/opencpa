import { NavLink, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Practice from './pages/Practice';
import Progress from './pages/Progress';

export default function App() {
  return (
    <div className="shell">
      <header className="nav">
        <NavLink to="/" className="brand">
          OpenCPA
        </NavLink>
        <nav>
          <NavLink to="/practice">Practice</NavLink>
          <NavLink to="/progress">Progress</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/progress" element={<Progress />} />
        </Routes>
      </main>
    </div>
  );
}
