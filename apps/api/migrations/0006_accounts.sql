-- Accounts. An account is a `users` row with a GitHub id and/or an email (the columns exist
-- since 0001). Anonymous device ids stay `users` rows with neither; signing in moves a device's
-- progress into the account and deletes the device row.
ALTER TABLE users ADD COLUMN github_login TEXT;

-- Signed-in browsers. The browser holds a random token; only its SHA-256 hash is kept.
CREATE TABLE auth_sessions (
  token_hash   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at   INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
  expires_at   INTEGER NOT NULL,
  last_used_at INTEGER
);
CREATE INDEX auth_sessions_user ON auth_sessions(user_id);

-- Short-lived, single-use sign-in steps, also stored as SHA-256 hashes:
--   github_state  the OAuth `state` for one GitHub round trip
--   email_link    the token in an emailed sign-in link
--   login_code    what the GitHub callback hands the web app to swap for a session
CREATE TABLE auth_tokens (
  token_hash TEXT PRIMARY KEY,
  kind       TEXT NOT NULL,
  anon_id    TEXT,          -- the device whose progress moves into the account
  email      TEXT,          -- email_link: the address being verified
  user_id    TEXT,          -- login_code: the account signed into
  return_to  TEXT,          -- github_state: the web origin to send the student back to
  created_at INTEGER NOT NULL DEFAULT (unixepoch() * 1000),
  expires_at INTEGER NOT NULL
);
CREATE INDEX auth_tokens_email ON auth_tokens(kind, email, created_at);
