-- Practice sessions: a fixed list of questions the student works through, saved as they go.
CREATE TABLE practice_sessions (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  section      TEXT NOT NULL,
  kind         TEXT NOT NULL,          -- 'diagnostic' | 'practice'
  status       TEXT NOT NULL DEFAULT 'active', -- 'active' | 'completed' | 'abandoned'
  item_ids     TEXT NOT NULL,          -- JSON array of item ids, in serving order
  created_at   INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
  completed_at INTEGER
);
CREATE INDEX practice_sessions_user ON practice_sessions(user_id, section, status);

-- Which session an attempt belongs to (NULL for attempts made outside a session).
ALTER TABLE attempts ADD COLUMN session_id TEXT;
CREATE INDEX attempts_session ON attempts(session_id);
