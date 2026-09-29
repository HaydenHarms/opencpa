import { useEffect, useState } from 'react';
import { api, type ConnectorStatus } from '../api';

const when = (ms: number | null) => (ms ? new Date(ms).toLocaleString() : 'not yet');

/** Connect Claude: make a personal connector link and explain how to add it in Claude. */
export default function Claude() {
  const [status, setStatus] = useState<ConnectorStatus | null>(null);
  const [url, setUrl] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.connector().then(setStatus, (e: Error) => setError(e.message));
  }, []);

  async function makeLink() {
    if (status?.connected && !confirm('Make a new link? The old one will stop working in Claude.'))
      return;
    try {
      const r = await api.newConnectorLink();
      setUrl(r.url);
      setCopied(false);
      setStatus(await api.connector());
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function disconnect() {
    if (!confirm('Disconnect Claude? Your link will stop working.')) return;
    try {
      setStatus(await api.disconnect());
      setUrl(null);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function copy() {
    if (!url) return;
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
    } catch {
      // Clipboard can be blocked; the link is selectable in the box.
    }
  }

  return (
    <section className="prose">
      <h1>Study with Claude</h1>
      <p>
        Keep OpenCPA open in one tab and Claude in another. Once you connect them, Claude can see
        the question you just answered, your choice, the answer key and explanation, and your weak
        topics, so you can ask it things like “why was my answer wrong?” without copying anything
        over. It uses your own Claude account.
      </p>
      <p className="muted">
        Claude sees only your OpenCPA answers and progress. It can’t see answers to questions you
        haven’t attempted, and it can’t change anything here. Grading stays with OpenCPA.
      </p>

      {error && <p className="error">Something went wrong: {error}</p>}
      {!status && !error && <p className="muted">Loading…</p>}

      {status && (
        <article className="card">
          <h2>1. Your connector link</h2>
          {url ? (
            <>
              <p>
                Copy this link now. For your security it’s shown only once; you can always make a
                new one.
              </p>
              <div className="copy-row">
                <input readOnly value={url} onFocus={(e) => e.target.select()} />
                <button className="button" onClick={copy}>
                  {copied ? 'Copied' : 'Copy'}
                </button>
              </div>
              <p className="warn">
                Treat it like a password: anyone with the link can read your OpenCPA progress.
              </p>
            </>
          ) : status.connected ? (
            <p>
              You have a link (made {when(status.createdAt)}; last used by Claude{' '}
              {when(status.lastUsedAt)}). Lost it? Make a new one; the old one stops working.
            </p>
          ) : (
            <p>Make a personal link that Claude will use to read your OpenCPA progress.</p>
          )}
          <div className="row-start">
            <button className="button" onClick={makeLink}>
              {status.connected ? 'Make a new link' : 'Make my link'}
            </button>
            {status.connected && (
              <button className="link" onClick={disconnect}>
                Disconnect
              </button>
            )}
          </div>
        </article>
      )}

      <article className="card">
        <h2>2. Add it to Claude</h2>
        <ol>
          <li>
            Open <a href="https://claude.ai/settings/connectors">Settings → Connectors</a> in Claude
            (on the web or in the desktop app).
          </li>
          <li>
            Choose <b>Add custom connector</b>, name it <b>OpenCPA</b>, paste your link as the URL,
            and add it.
          </li>
          <li>In a new chat, make sure OpenCPA is turned on in the tools menu.</li>
        </ol>
        <p className="muted">
          Custom connectors are available on paid Claude plans; the free plan may limit them. Once
          added on the web, the connector also works in Claude’s mobile apps.
        </p>
      </article>

      <article className="card">
        <h2>3. Ask away</h2>
        <ul>
          <li>“Why did I get my last OpenCPA question wrong?”</li>
          <li>“Give me a hint on my current OpenCPA question, but don’t tell me the answer.”</li>
          <li>“Walk me through the journal entry in the simulation I just did.”</li>
          <li>“What are my weakest FAR topics, and what should I review first?”</li>
        </ul>
      </article>
    </section>
  );
}
