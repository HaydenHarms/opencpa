/**
 * Accounts: sign in with GitHub or an emailed link.
 *
 * The web app and the API are on different sites, so there are no cookies. Signing in ends
 * with the browser holding a random session token, sent as `Authorization: Bearer <token>`;
 * only its SHA-256 hash is stored. A browser that isn't signed in keeps using its anonymous
 * device id (`X-OpenCPA-User`), and signing in moves that device's progress into the account.
 *
 * Both providers are optional. GitHub needs the Worker secrets GITHUB_CLIENT_ID and
 * GITHUB_CLIENT_SECRET; email needs RESEND_API_KEY and EMAIL_FROM. `GET /auth/status`
 * tells the web app which ones are set up.
 */
import { Hono, type Context } from 'hono';
import { z } from 'zod';
import { hashToken, newToken } from './mcp';

export type Env = {
  DB: D1Database;
  ALLOWED_ORIGINS: string;
  GITHUB_CLIENT_ID?: string;
  GITHUB_CLIENT_SECRET?: string;
  RESEND_API_KEY?: string;
  EMAIL_FROM?: string;
};

const MINUTE = 60_000;
const DAY = 24 * 60 * MINUTE;
/** A session lasts this long after it was last used. */
const SESSION_TTL = 180 * DAY;
const GITHUB_STATE_TTL = 10 * MINUTE;
const EMAIL_LINK_TTL = 15 * MINUTE;
const LOGIN_CODE_TTL = 2 * MINUTE;
/** Emailed links: per address per EMAIL_LINK_TTL, and for the whole site per day (Resend's free tier is 100/day). */
const EMAIL_PER_ADDRESS = 3;
const EMAIL_PER_DAY = 90;

/** ALLOWED_ORIGINS entries are exact origins or wildcards like https://*.opencpa.pages.dev. */
export function originAllowed(origin: string, allowed: string): boolean {
  return allowed.split(',').some((raw) => {
    const rule = raw.trim();
    if (!rule.includes('*')) return rule === origin;
    const re = new RegExp(
      '^' + rule.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace('*', '[a-z0-9-]+') + '$',
    );
    return re.test(origin);
  });
}

const anonId = z.string().uuid();
const bearer = (header: string | undefined) => header?.match(/^Bearer\s+(\S+)$/i)?.[1] ?? null;

/**
 * The account a bearer token belongs to, or null if the token is unknown or expired.
 * Each use (at most once a day) pushes the expiry out again.
 */
export async function sessionUser(
  db: D1Database,
  ctx: { waitUntil(promise: Promise<unknown>): void },
  authorization: string | undefined,
): Promise<string | null> {
  const token = bearer(authorization);
  if (!token) return null;
  const hash = await hashToken(token);
  const now = Date.now();
  const row = await db
    .prepare(
      'SELECT user_id, last_used_at FROM auth_sessions WHERE token_hash = ? AND expires_at > ?',
    )
    .bind(hash, now)
    .first<{ user_id: string; last_used_at: number | null }>();
  if (!row) return null;
  if ((row.last_used_at ?? 0) < now - DAY)
    ctx.waitUntil(
      db
        .prepare('UPDATE auth_sessions SET last_used_at = ?, expires_at = ? WHERE token_hash = ?')
        .bind(now, now + SESSION_TTL, hash)
        .run(),
    );
  return row.user_id;
}

type TokenRow = {
  anon_id: string | null;
  email: string | null;
  user_id: string | null;
  return_to: string | null;
};

/** Store a single-use sign-in token and return it. Rows older than a day are cleared out. */
async function issue(
  db: D1Database,
  kind: string,
  ttl: number,
  fields: Partial<TokenRow>,
): Promise<string> {
  const token = newToken();
  const now = Date.now();
  await db.batch([
    db.prepare('DELETE FROM auth_tokens WHERE created_at < ?').bind(now - DAY),
    db
      .prepare(
        'INSERT INTO auth_tokens (token_hash, kind, anon_id, email, user_id, return_to, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
      )
      .bind(
        await hashToken(token),
        kind,
        fields.anon_id ?? null,
        fields.email ?? null,
        fields.user_id ?? null,
        fields.return_to ?? null,
        now + ttl,
      ),
  ]);
  return token;
}

/**
 * Use up a token: it works once, before it expires. The row stays (expired) until the daily
 * clear-out so the email rate limits can count it.
 */
async function consume(db: D1Database, kind: string, token: string): Promise<TokenRow | null> {
  return db
    .prepare(
      `UPDATE auth_tokens SET expires_at = 0 WHERE token_hash = ? AND kind = ? AND expires_at > ?
       RETURNING anon_id, email, user_id, return_to`,
    )
    .bind(await hashToken(token), kind, Date.now())
    .first<TokenRow>();
}

/**
 * Move an anonymous device's progress into an account, then delete the device row.
 * Attempts and practice sessions move as they are. Where both have a review card for the
 * same item, the more recently reviewed one wins. Where both have an unfinished session for
 * the same section (or Library topic), the older one is abandoned, and the same for unfinished
 * mock exams in the same section. The device's Claude
 * connector link moves too, unless the account already has one.
 * Does nothing unless `from` is an anonymous device row.
 */
export async function mergeInto(db: D1Database, from: string, to: string) {
  if (from === to) return;
  const source = await db
    .prepare('SELECT github_id, email FROM users WHERE id = ?')
    .bind(from)
    .first<{ github_id: string | null; email: string | null }>();
  if (!source || source.github_id || source.email) return;
  const run = (sql: string) => db.prepare(sql).bind(from, to);
  const fromOnly = (sql: string) => db.prepare(sql).bind(from);
  await db.batch([
    run(
      `UPDATE practice_sessions SET status = 'abandoned'
       WHERE user_id IN (?1, ?2) AND status = 'active' AND EXISTS (
         SELECT 1 FROM practice_sessions p
         WHERE p.user_id IN (?1, ?2) AND p.user_id != practice_sessions.user_id
           AND p.status = 'active' AND p.section = practice_sessions.section
           AND p.topic IS practice_sessions.topic AND p.created_at > practice_sessions.created_at)`,
    ),
    run('UPDATE practice_sessions SET user_id = ?2 WHERE user_id = ?1'),
    run(
      `UPDATE exams SET status = 'abandoned', finished_at = unixepoch() * 1000
       WHERE user_id IN (?1, ?2) AND status = 'active' AND EXISTS (
         SELECT 1 FROM exams e
         WHERE e.user_id IN (?1, ?2) AND e.user_id != exams.user_id
           AND e.status = 'active' AND e.section = exams.section AND e.started_at > exams.started_at)`,
    ),
    run('UPDATE exams SET user_id = ?2 WHERE user_id = ?1'),
    run('UPDATE attempts SET user_id = ?2 WHERE user_id = ?1'),
    run(
      `INSERT INTO review_cards (user_id, item_id, due, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, last_review)
       SELECT ?2, item_id, due, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, last_review
       FROM review_cards WHERE user_id = ?1
       ON CONFLICT(user_id, item_id) DO UPDATE SET
         due = excluded.due, stability = excluded.stability, difficulty = excluded.difficulty,
         elapsed_days = excluded.elapsed_days, scheduled_days = excluded.scheduled_days,
         reps = excluded.reps, lapses = excluded.lapses, state = excluded.state, last_review = excluded.last_review
       WHERE COALESCE(excluded.last_review, 0) > COALESCE(review_cards.last_review, 0)`,
    ),
    fromOnly('DELETE FROM review_cards WHERE user_id = ?1'),
    run(
      `UPDATE connector_tokens SET user_id = ?2
       WHERE user_id = ?1 AND NOT EXISTS (SELECT 1 FROM connector_tokens WHERE user_id = ?2)`,
    ),
    fromOnly('DELETE FROM users WHERE id = ?1 AND github_id IS NULL AND email IS NULL'),
  ]);
}

/** Finish signing in: move the device's progress into the account and start a session. */
async function startSession(db: D1Database, userId: string, anon: string | null) {
  if (anon) await mergeInto(db, anon, userId);
  const token = newToken();
  const expiresAt = Date.now() + SESSION_TTL;
  await db
    .prepare('INSERT INTO auth_sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)')
    .bind(await hashToken(token), userId, expiresAt)
    .run();
  return { token, expiresAt };
}

const githubReady = (env: Env) => !!(env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET);
const emailReady = (env: Env) => !!(env.RESEND_API_KEY && env.EMAIL_FROM);

type Ctx = Context<{ Bindings: Env }>;

/** The web origin making the request, if it's one the API serves. */
function webOrigin(c: Ctx): string | null {
  const origin = c.req.header('Origin');
  return origin && originAllowed(origin, c.env.ALLOWED_ORIGINS) ? origin : null;
}

function deviceId(c: Ctx): string | null {
  const parsed = anonId.safeParse(c.req.header('X-OpenCPA-User'));
  return parsed.success ? parsed.data : null;
}

export const auth = new Hono<{ Bindings: Env }>();

/** Which sign-in methods are set up, and the signed-in account (null if signed out). */
auth.get('/status', async (c) => {
  const userId = await sessionUser(c.env.DB, c.executionCtx, c.req.header('Authorization'));
  const account = userId
    ? await c.env.DB.prepare(
        'SELECT github_login, email, display_name, created_at FROM users WHERE id = ?',
      )
        .bind(userId)
        .first<{
          github_login: string | null;
          email: string | null;
          display_name: string | null;
          created_at: number;
        }>()
    : null;
  return c.json({
    github: githubReady(c.env),
    email: emailReady(c.env),
    account: account && {
      githubLogin: account.github_login,
      email: account.email,
      displayName: account.display_name,
      createdAt: account.created_at,
    },
  });
});

auth.post('/signout', async (c) => {
  const token = bearer(c.req.header('Authorization'));
  if (token)
    await c.env.DB.prepare('DELETE FROM auth_sessions WHERE token_hash = ?')
      .bind(await hashToken(token))
      .run();
  return c.json({ signedOut: true });
});

/* ---------- GitHub ---------- */

/** Step 1: the web app asks where to send the student; the answer is GitHub's consent page. */
auth.post('/github/start', async (c) => {
  if (!githubReady(c.env)) return c.json({ error: 'GitHub sign-in is not set up' }, 503);
  const returnTo = webOrigin(c);
  if (!returnTo) return c.json({ error: 'unknown origin' }, 400);
  const state = await issue(c.env.DB, 'github_state', GITHUB_STATE_TTL, {
    anon_id: deviceId(c),
    return_to: returnTo,
  });
  const url = new URL('https://github.com/login/oauth/authorize');
  url.search = new URLSearchParams({
    client_id: c.env.GITHUB_CLIENT_ID!,
    redirect_uri: `${new URL(c.req.url).origin}/auth/github/callback`,
    scope: 'user:email',
    state,
  }).toString();
  return c.json({ url: url.toString() });
});

/**
 * Step 2: GitHub sends the student here. Look up (or create) the account, then send the
 * student back to the web app with a one-time code in the URL fragment, which the web app
 * swaps for a session at POST /auth/exchange.
 */
auth.get('/github/callback', async (c) => {
  const state = c.req.query('state');
  const row = state ? await consume(c.env.DB, 'github_state', state) : null;
  if (!row?.return_to)
    return c.text('This sign-in attempt expired. Go back to OpenCPA and try again.', 400);
  const back = (fragment: string) => c.redirect(`${row.return_to}/signin/done#${fragment}`);
  const code = c.req.query('code');
  if (!code) return back('error=denied');

  try {
    const profile = await githubProfile(
      c.env,
      code,
      `${new URL(c.req.url).origin}/auth/github/callback`,
    );
    const userId = await githubAccount(c.env.DB, profile);
    const loginCode = await issue(c.env.DB, 'login_code', LOGIN_CODE_TTL, {
      user_id: userId,
      anon_id: row.anon_id,
    });
    return back(`code=${loginCode}`);
  } catch (e) {
    console.error('GitHub sign-in failed', e);
    return back('error=github');
  }
});

/** Step 3: swap the one-time code for a session. */
auth.post('/exchange', async (c) => {
  const body = z
    .object({ code: z.string().min(1).max(100) })
    .safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: 'missing code' }, 400);
  const row = await consume(c.env.DB, 'login_code', body.data.code);
  if (!row?.user_id) return c.json({ error: 'This sign-in link expired. Try again.' }, 400);
  return c.json(await startSession(c.env.DB, row.user_id, row.anon_id));
});

type GithubProfile = { id: string; login: string; name: string | null; email: string | null };

async function githubProfile(env: Env, code: string, redirectUri: string): Promise<GithubProfile> {
  const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: redirectUri,
    }),
  });
  const { access_token } = (await tokenRes.json()) as { access_token?: string };
  if (!access_token) throw new Error(`token exchange failed (${tokenRes.status})`);
  const gh = (path: string) =>
    fetch(`https://api.github.com${path}`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
        Accept: 'application/vnd.github+json',
        'User-Agent': 'OpenCPA',
      },
    });
  const [userRes, emailsRes] = await Promise.all([gh('/user'), gh('/user/emails')]);
  if (!userRes.ok) throw new Error(`GitHub /user returned ${userRes.status}`);
  const user = (await userRes.json()) as { id: number; login: string; name: string | null };
  const emails = emailsRes.ok
    ? ((await emailsRes.json()) as { email: string; primary: boolean; verified: boolean }[])
    : [];
  const primary = emails.find((e) => e.primary && e.verified)?.email;
  return {
    id: String(user.id),
    login: user.login,
    name: user.name,
    email: primary ? normalizeEmail(primary) : null,
  };
}

/**
 * The account for a GitHub user: the one already linked to it, else the account with the
 * same verified email (which gets linked), else a new one.
 */
async function githubAccount(db: D1Database, p: GithubProfile): Promise<string> {
  const displayName = p.name || p.login;
  const linked = await db
    .prepare('SELECT id FROM users WHERE github_id = ?')
    .bind(p.id)
    .first<{ id: string }>();
  if (linked) {
    await db
      .prepare(
        'UPDATE users SET github_login = ?, display_name = COALESCE(display_name, ?) WHERE id = ?',
      )
      .bind(p.login, displayName, linked.id)
      .run();
    return linked.id;
  }
  if (p.email) {
    const byEmail = await db
      .prepare('SELECT id, github_id FROM users WHERE email = ?')
      .bind(p.email)
      .first<{ id: string; github_id: string | null }>();
    if (byEmail && !byEmail.github_id) {
      await db
        .prepare(
          'UPDATE users SET github_id = ?, github_login = ?, display_name = COALESCE(display_name, ?) WHERE id = ?',
        )
        .bind(p.id, p.login, displayName, byEmail.id)
        .run();
      return byEmail.id;
    }
    // The email belongs to an account linked to a different GitHub user: don't claim it.
    if (byEmail) p = { ...p, email: null };
  }
  const id = crypto.randomUUID();
  await db
    .prepare(
      'INSERT INTO users (id, github_id, github_login, email, display_name) VALUES (?, ?, ?, ?, ?)',
    )
    .bind(id, p.id, p.login, p.email, displayName)
    .run();
  return id;
}

/* ---------- Email ---------- */

const normalizeEmail = (email: string) => email.trim().toLowerCase();
const emailBody = z.object({ email: z.string().trim().email().max(254) });

/** Step 1: email the student a sign-in link to the web app. */
auth.post('/email/start', async (c) => {
  if (!emailReady(c.env)) return c.json({ error: 'Email sign-in is not set up' }, 503);
  const returnTo = webOrigin(c);
  if (!returnTo) return c.json({ error: 'unknown origin' }, 400);
  const body = emailBody.safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: 'Enter a valid email address.' }, 400);
  const email = normalizeEmail(body.data.email);
  const db = c.env.DB;

  const now = Date.now();
  const [perAddress, perDay] = await db.batch<{ n: number }>([
    db
      .prepare(
        "SELECT COUNT(*) AS n FROM auth_tokens WHERE kind = 'email_link' AND email = ? AND created_at > ?",
      )
      .bind(email, now - EMAIL_LINK_TTL),
    db
      .prepare("SELECT COUNT(*) AS n FROM auth_tokens WHERE kind = 'email_link' AND created_at > ?")
      .bind(now - DAY),
  ]);
  if ((perAddress?.results[0]?.n ?? 0) >= EMAIL_PER_ADDRESS)
    return c.json(
      { error: 'Too many links sent to that address. Wait a few minutes and try again.' },
      429,
    );
  if ((perDay?.results[0]?.n ?? 0) >= EMAIL_PER_DAY)
    return c.json(
      {
        error:
          'OpenCPA has sent its email limit for today. Try again tomorrow, or sign in with GitHub.',
      },
      429,
    );

  const token = await issue(db, 'email_link', EMAIL_LINK_TTL, { email });
  const link = `${returnTo}/signin/email#token=${token}`;
  const sent = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${c.env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: c.env.EMAIL_FROM,
      to: [email],
      subject: 'Your OpenCPA sign-in link',
      text: `Sign in to OpenCPA:\n\n${link}\n\nThe link works once, for 15 minutes. If you didn't ask for it, ignore this email.`,
      html: `<p>Sign in to OpenCPA:</p><p><a href="${link}">Sign in</a></p><p style="color:#666">The link works once, for 15 minutes. If you didn't ask for it, ignore this email.</p>`,
    }),
  });
  if (!sent.ok) {
    console.error('Resend failed', sent.status, await sent.text());
    return c.json({ error: 'The email could not be sent. Try again later.' }, 502);
  }
  return c.json({ sent: true });
});

/**
 * Step 2: the student opens the link and confirms on the web page, which posts the token
 * here. (The page asks for a click so a mail scanner that opens links can't use it up.)
 * The progress that moves into the account is the confirming device's.
 */
auth.post('/email/verify', async (c) => {
  const body = z
    .object({ token: z.string().min(1).max(100) })
    .safeParse(await c.req.json().catch(() => null));
  if (!body.success) return c.json({ error: 'missing token' }, 400);
  const db = c.env.DB;
  const row = await consume(db, 'email_link', body.data.token);
  if (!row?.email)
    return c.json(
      { error: 'This sign-in link has expired or was already used. Ask for a new one.' },
      400,
    );
  const existing = await db
    .prepare('SELECT id FROM users WHERE email = ?')
    .bind(row.email)
    .first<{ id: string }>();
  let userId = existing?.id;
  if (!userId) {
    userId = crypto.randomUUID();
    await db.prepare('INSERT INTO users (id, email) VALUES (?, ?)').bind(userId, row.email).run();
  }
  return c.json(await startSession(db, userId, deviceId(c)));
});
