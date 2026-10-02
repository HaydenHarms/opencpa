import { useEffect, useRef, useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { AUTH_EVENT, api, errorMessage, setSession, type Account, type AuthStatus } from '../api';

/** The sign-in methods on offer and the signed-in account, refreshed when either changes. */
export function useAuthStatus() {
  const [status, setStatus] = useState<AuthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const refresh = () =>
      api.authStatus().then(
        (s) => {
          setStatus(s);
          setError(null);
        },
        (e) => setError(errorMessage(e)),
      );
    refresh();
    window.addEventListener(AUTH_EVENT, refresh);
    return () => window.removeEventListener(AUTH_EVENT, refresh);
  }, []);
  return { status, error };
}

export const accountName = (a: Account) => a.displayName ?? a.githubLogin ?? a.email ?? 'Account';

/** /account: sign in, or see who you're signed in as and sign out. */
export default function AccountPage() {
  const { status, error } = useAuthStatus();
  return (
    <section className="prose">
      <h1>{status?.account ? 'Your account' : 'Sign in'}</h1>
      {error && <p className="error">Something went wrong: {error}</p>}
      {!status && !error && <p className="muted">Loading…</p>}
      {status && (status.account ? <SignedIn account={status.account} /> : <SignIn {...status} />)}
    </section>
  );
}

function SignIn({ github, email }: AuthStatus) {
  const [address, setAddress] = useState('');
  const [sentTo, setSentTo] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function withGithub() {
    setBusy(true);
    setError(null);
    try {
      window.location.assign((await api.githubStart()).url);
    } catch (e) {
      setError(errorMessage(e));
      setBusy(false);
    }
  }

  async function withEmail(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api.emailStart(address);
      setSentTo(address.trim());
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <p>
        Sign in to keep your progress on every device. Everything you’ve done on this device so far
        moves into your account.
      </p>
      {!github && !email && <p className="muted">Sign-in isn’t available yet. Check back soon.</p>}
      {error && <p className="error">{error}</p>}
      {github && (
        <article className="card">
          <h2>GitHub</h2>
          <button className="button" onClick={withGithub} disabled={busy}>
            Continue with GitHub
          </button>
        </article>
      )}
      {email && (
        <article className="card">
          <h2>Email</h2>
          {sentTo ? (
            <>
              <p>
                Check your inbox: we sent a sign-in link to <b>{sentTo}</b>. It works once, for 15
                minutes.
              </p>
              <button className="link" onClick={() => setSentTo(null)}>
                Use a different address
              </button>
            </>
          ) : (
            <form onSubmit={withEmail}>
              <p>We’ll email you a link. No password needed.</p>
              <div className="copy-row">
                <input
                  type="email"
                  required
                  autoComplete="email"
                  placeholder="you@example.com"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                />
                <button className="button" disabled={busy}>
                  Email me a link
                </button>
              </div>
            </form>
          )}
        </article>
      )}
    </>
  );
}

function SignedIn({ account }: { account: Account }) {
  const [busy, setBusy] = useState(false);
  async function signOut() {
    setBusy(true);
    try {
      await api.signOut();
    } finally {
      setSession(null);
    }
  }
  return (
    <article className="card">
      <h2>{accountName(account)}</h2>
      <ul>
        {account.githubLogin && <li>GitHub: @{account.githubLogin}</li>}
        {account.email && <li>Email: {account.email}</li>}
        <li>Member since {new Date(account.createdAt).toLocaleDateString()}</li>
      </ul>
      <p className="muted">
        Your progress, review schedule and Claude connector link are saved to this account.
      </p>
      <button className="button" onClick={signOut} disabled={busy}>
        Sign out
      </button>
    </article>
  );
}

const fragment = (key: string) => new URLSearchParams(window.location.hash.slice(1)).get(key);

/** Remove the URL fragment so a sign-in code or token doesn't linger in history. */
function clearFragment() {
  if (window.location.hash)
    window.history.replaceState(null, '', window.location.pathname + window.location.search);
}

const GITHUB_ERRORS: Record<string, string> = {
  denied: 'GitHub sign-in was cancelled.',
  github: 'GitHub sign-in didn’t work. Try again in a moment.',
};

/** /signin/done: where the GitHub round trip lands, with a one-time code to swap for a session. */
export function SigninDone() {
  const [state, setState] = useState<'working' | 'done' | string>('working');
  const started = useRef(false);
  useEffect(() => {
    if (started.current) return;
    started.current = true;
    const code = fragment('code');
    const error = fragment('error');
    clearFragment();
    if (!code) {
      setState(GITHUB_ERRORS[error ?? ''] ?? 'This sign-in link is incomplete.');
      return;
    }
    api.exchange(code).then(
      (s) => {
        setSession(s.token);
        setState('done');
      },
      (e) => setState(errorMessage(e)),
    );
  }, []);
  return <SigninResult state={state} />;
}

/**
 * /signin/email: the link in the sign-in email. It asks for a click before using the token,
 * so an email scanner that opens links can't use it up.
 */
export function SigninEmail() {
  const [token] = useState(() => fragment('token'));
  useEffect(clearFragment, []);
  const [state, setState] = useState<'ready' | 'working' | 'done' | string>(
    token ? 'ready' : 'This sign-in link is incomplete. Ask for a new one.',
  );
  async function finish() {
    setState('working');
    try {
      setSession((await api.emailVerify(token!)).token);
      setState('done');
    } catch (e) {
      setState(errorMessage(e));
    }
  }
  if (state === 'ready')
    return (
      <section className="prose">
        <h1>Sign in</h1>
        <p>Finish signing in to OpenCPA on this device.</p>
        <button className="button" onClick={finish}>
          Sign in
        </button>
      </section>
    );
  return <SigninResult state={state} />;
}

function SigninResult({ state }: { state: string }) {
  return (
    <section className="prose">
      <h1>Sign in</h1>
      {state === 'working' && <p className="muted">Signing you in…</p>}
      {state === 'done' && (
        <>
          <p>You’re signed in. Your progress on this device is now part of your account.</p>
          <Link to="/practice" className="button">
            Keep practicing
          </Link>
        </>
      )}
      {state !== 'working' && state !== 'done' && (
        <>
          <p className="error">{state}</p>
          <Link to="/account">Back to sign in</Link>
        </>
      )}
    </section>
  );
}
