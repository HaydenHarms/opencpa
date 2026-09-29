import { NavLink, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Practice from './pages/Practice';
import Progress from './pages/Progress';
import Simulation from './pages/Simulation';
import Simulations from './pages/Simulations';

export default function App() {
  return (
    <div className="shell">
      <header className="nav">
        <NavLink to="/" className="brand">
          OpenCPA
        </NavLink>
        <nav>
          <NavLink to="/practice">Practice</NavLink>
          <NavLink to="/simulations">Simulations</NavLink>
          <NavLink to="/progress">Progress</NavLink>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/simulations" element={<Simulations />} />
          <Route path="/simulations/:id" element={<Simulation />} />
          <Route path="/progress" element={<Progress />} />
        </Routes>
      </main>
    </div>
  );
}
