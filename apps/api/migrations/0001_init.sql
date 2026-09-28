-- Students. Until OAuth lands, `id` is an anonymous device id generated in the browser.
CREATE TABLE users (
  id          TEXT PRIMARY KEY,
  github_id   TEXT UNIQUE,
  email       TEXT UNIQUE,
  display_name TEXT,
  created_at  INTEGER NOT NULL DEFAULT (unixepoch() * 1000)
);

-- Every answer a student submits. Items live in the repo; we store only their id
-- plus the blueprint tags at attempt time so mastery survives content edits.
CREATE TABLE attempts (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_id     TEXT NOT NULL,
  section     TEXT NOT NULL,
  area        TEXT NOT NULL,
  response    TEXT NOT NULL,          -- JSON of what the student entered
  earned      REAL NOT NULL,
  possible    REAL NOT NULL,
  correct     INTEGER NOT NULL,       -- 0/1
  duration_ms INTEGER,
  created_at  INTEGER NOT NULL DEFAULT (unixepoch() * 1000)
);
CREATE INDEX attempts_user_time ON attempts(user_id, created_at DESC);
CREATE INDEX attempts_user_area ON attempts(user_id, section, area);

-- FSRS spaced-repetition state, one card per (student, item).
CREATE TABLE review_cards (
  user_id        TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_id        TEXT NOT NULL,
  due            INTEGER NOT NULL,    -- epoch ms
  stability      REAL NOT NULL,
  difficulty     REAL NOT NULL,
  elapsed_days   INTEGER NOT NULL,
  scheduled_days INTEGER NOT NULL,
  reps           INTEGER NOT NULL,
  lapses         INTEGER NOT NULL,
  state          INTEGER NOT NULL,    -- 0 New, 1 Learning, 2 Review, 3 Relearning
  last_review    INTEGER,
  PRIMARY KEY (user_id, item_id)
);
CREATE INDEX review_cards_due ON review_cards(user_id, due);
