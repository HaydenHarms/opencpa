-- Claude connector links. The link carries a random token; only its SHA-256 hash is kept.
-- One link per student: making a new one replaces the old one.
CREATE TABLE connector_tokens (
  token_hash   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  created_at   INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
  last_used_at INTEGER
);
