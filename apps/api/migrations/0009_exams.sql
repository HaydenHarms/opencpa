-- Mock exams (docs/plans/exam-mode.md, Phase B). One row per exam. Items are graded and written
-- to `attempts` (session_id = the exam id) as each testlet is submitted; keys are shown only once
-- the exam is finished.
CREATE TABLE exams (
  id               TEXT PRIMARY KEY,
  user_id          TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  section          TEXT NOT NULL,
  status           TEXT NOT NULL DEFAULT 'active', -- 'active' | 'finished' | 'abandoned'
  testlets         TEXT NOT NULL,                  -- JSON: item ids per testlet
  variants         TEXT NOT NULL,                  -- JSON: { itemId: version served }
  current          INTEGER NOT NULL DEFAULT 0,     -- index of the open testlet
  responses        TEXT NOT NULL DEFAULT '{}',     -- JSON: { itemId: saved response }
  flags            TEXT NOT NULL DEFAULT '[]',     -- JSON: flagged item ids
  testlet_used     TEXT NOT NULL DEFAULT '[]',     -- JSON: clock time used when each testlet was submitted
  started_at       INTEGER NOT NULL,
  break_started_at INTEGER,
  break_ended_at   INTEGER,
  paused_at        INTEGER,
  paused_ms        INTEGER NOT NULL DEFAULT 0,
  pauses           INTEGER NOT NULL DEFAULT 0,
  finished_at      INTEGER,
  ended_by         TEXT                            -- 'submitted' | 'time'
);
CREATE INDEX exams_user ON exams(user_id, section, status);
