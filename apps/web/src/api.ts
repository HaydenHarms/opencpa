import type { JournalLine, PublicMcq, PublicTbs } from '@opencpa/schema';

const BASE = import.meta.env.VITE_API_URL ?? '/api';

const DEVICE_KEY = 'opencpa:user';
const SESSION_KEY = 'opencpa:session';
const memory: Record<string, string | undefined> = {};

function load(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return memory[key] ?? null;
  }
}

function store(key: string, value: string | null) {
  try {
    if (value === null) localStorage.removeItem(key);
    else localStorage.setItem(key, value);
  } catch {
    memory[key] = value ?? undefined;
  }
}

/** The anonymous device id, used while signed out. */
function deviceId(): string {
  let id = load(DEVICE_KEY);
  if (!id) {
    id = crypto.randomUUID();
    store(DEVICE_KEY, id);
  }
  return id;
}

/** Fired whenever this browser signs in or out, so the nav and pages can refresh. */
export const AUTH_EVENT = 'opencpa:auth';

/**
 * Sign this browser in or out. Either way the device starts over with a fresh anonymous id:
 * signing in moved the old one's progress into the account, and signing out shouldn't leave
 * the account's progress on screen.
 */
export function setSession(token: string | null) {
  store(SESSION_KEY, token);
  store(DEVICE_KEY, null);
  window.dispatchEvent(new Event(AUTH_EVENT));
}

export const signedIn = () => !!load(SESSION_KEY);

async function call<T>(path: string, init?: RequestInit, retried = false): Promise<T> {
  const token = load(SESSION_KEY);
  const res = await fetch(BASE + path, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : { 'X-OpenCPA-User': deviceId() }),
      ...init?.headers,
    },
  });
  if (res.status === 401 && !retried) {
    // An expired session, or a device id that now belongs to an account: carry on signed out.
    const body = (await res
      .clone()
      .json()
      .catch(() => null)) as { signedOut?: boolean } | null;
    if (body?.signedOut) {
      setSession(null);
      return call<T>(path, init, true);
    }
  }
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
}

/** Errors from the sign-in endpoints carry a sentence meant for the student. */
export function errorMessage(e: unknown): string {
  const text = (e as Error).message.replace(/^\d+ /, '');
  try {
    const { error } = JSON.parse(text) as { error?: unknown };
    if (typeof error === 'string') return error;
  } catch {
    // Not JSON.
  }
  return text;
}

export interface Account {
  githubLogin: string | null;
  email: string | null;
  displayName: string | null;
  createdAt: number;
}

/** Which sign-in methods the API has set up, and who is signed in (null if no one). */
export interface AuthStatus {
  github: boolean;
  email: boolean;
  account: Account | null;
}

export interface NewSession {
  token: string;
  expiresAt: number;
}

/** What an answered question reveals. */
export interface Revealed {
  selected: string;
  correct: boolean;
  answer: string;
  explanation: string;
  rationales: Record<string, string>;
}

export interface AttemptResult extends Revealed {
  nextDue: string;
  sessionComplete: boolean;
}

export interface Session {
  id: string;
  section: string;
  kind: 'diagnostic' | 'practice';
  /** Set when the session covers one blueprint topic (started from the Library). */
  topic: string | null;
  /** Practice keeps questions and simulations apart; a Library topic session mixes them. */
  mode: SessionMode | 'mixed';
  status: 'active' | 'completed' | 'abandoned';
  createdAt: number;
  completedAt: number | null;
  /** Questions and simulations, in serving order. */
  items: (PublicMcq | PublicTbs)[];
  /** Results for the items already answered, keyed by item id. */
  answered: Record<string, Revealed | SimulationReveal>;
}

/** The two kinds of Practice session, matching the exam's two kinds of testlet. */
export type SessionMode = 'questions' | 'simulations';

/** A session length on offer and the simulations that come with it. */
export interface SessionOption {
  /** What to send as `size` to start it: questions, or simulations in a simulations session. */
  size: number;
  questions: number;
  simulations: number;
}

export interface SessionStatus {
  session: Session | null;
  nextKind: 'diagnostic' | 'practice';
  diagnostic: SessionOption;
  options: SessionOption[];
  poolSize: number;
}

/** Whether the student has a Claude connector link. Times are epoch ms. */
export interface ConnectorStatus {
  connected: boolean;
  createdAt: number | null;
  lastUsedAt: number | null;
}

export interface Mastery {
  section: string;
  area: string;
  attempts: number;
  score: number;
}

/** What the student submits for one simulation task. Journal amounts are whole cents. */
export type TaskResponse =
  | { type: 'numeric'; value: number }
  | { type: 'journal_entry'; lines: { account: string; debit?: number; credit?: number }[] }
  | { type: 'research'; citation: string }
  | { type: 'select'; choices: Record<string, string> };

export interface TaskResult {
  id: string;
  earned: number;
  possible: number;
  correct: boolean;
  /** A select task's key is the correct option per row id. */
  answer: number | string[] | JournalLine[] | Record<string, string>;
  explanation: string;
}

/** What a submitted simulation reveals, including the student's own responses. */
export interface SimulationReveal {
  earned: number;
  possible: number;
  correct: boolean;
  tasks: TaskResult[];
  responses: Record<string, TaskResponse>;
}

export interface SimulationResult extends SimulationReveal {
  nextDue: string;
  sessionComplete: boolean;
}

export interface LibraryTopic {
  area: string;
  topic: string;
  questions: number;
  simulations: number;
  /** Items in the topic the student has answered at least once. */
  seen: number;
  attempts: number;
  /** Attempts answered correctly (simulations count when fully correct). */
  correct: number;
  /** Recency-weighted accuracy (0–1), or null before any attempt. */
  mastery: number | null;
}

export interface LibrarySection {
  section: string;
  questions: number;
  simulations: number;
  seen: number;
  attempts: number;
  accuracy: number | null;
  topics: LibraryTopic[];
}

export interface LibraryEntry {
  id: string;
  type: 'mcq' | 'tbs';
  blueprint: PublicMcq['blueprint'];
  title: string;
  attempts: number;
  lastCorrect: boolean | null;
  lastScore: number | null;
  lastAt: number | null;
}

export interface LibraryQuestion {
  item: PublicMcq;
  attempts: number;
  correct: number;
  last: (Revealed & { item: PublicMcq; at: number }) | null;
}

/** One item in the Library search index (public text only). */
export interface SearchDoc {
  id: string;
  type: 'mcq' | 'tbs';
  section: string;
  area: string;
  topic: string;
  skill: string;
  title: string | null;
  text: string;
  refs: string[];
}

const q = (params: Record<string, string | undefined>) => {
  const s = new URLSearchParams(
    Object.entries(params).filter((e): e is [string, string] => !!e[1]),
  ).toString();
  return s ? `?${s}` : '';
};

export const api = {
  authStatus: () => call<AuthStatus>('/auth/status'),
  githubStart: () => call<{ url: string }>('/auth/github/start', { method: 'POST' }),
  exchange: (code: string) =>
    call<NewSession>('/auth/exchange', { method: 'POST', body: JSON.stringify({ code }) }),
  emailStart: (email: string) =>
    call<{ sent: true }>('/auth/email/start', { method: 'POST', body: JSON.stringify({ email }) }),
  emailVerify: (token: string) =>
    call<NewSession>('/auth/email/verify', { method: 'POST', body: JSON.stringify({ token }) }),
  signOut: () => call<{ signedOut: true }>('/auth/signout', { method: 'POST' }),
  deleteMyData: () => call<{ deleted: true }>('/me/account', { method: 'DELETE' }),
  questions: (section?: string) =>
    call<PublicMcq[]>(`/questions${section ? `?section=${section}` : ''}`),
  attempt: (itemId: string, selected: string, durationMs: number, sessionId?: string) =>
    call<AttemptResult>('/me/attempts', {
      method: 'POST',
      body: JSON.stringify({ itemId, selected, durationMs, sessionId }),
    }),
  /** Pass a topic for a Library topic session, or a mode for a Practice session. */
  currentSession: (section: string, scope: { topic?: string; mode?: SessionMode } = {}) =>
    call<SessionStatus>(`/me/sessions/current${q({ section, ...scope })}`),
  startSession: (
    section: string,
    size: number,
    scope: { topic?: string; mode?: SessionMode } = {},
  ) =>
    call<Session>('/me/sessions', {
      method: 'POST',
      body: JSON.stringify({ section, size, ...scope }),
    }),
  attemptOutsideSession: (itemId: string, selected: string, durationMs: number, variant: number) =>
    call<AttemptResult>('/me/attempts', {
      method: 'POST',
      body: JSON.stringify({ itemId, selected, durationMs, variant }),
    }),
  searchIndex: () => call<SearchDoc[]>('/library/search-index'),
  library: () => call<LibrarySection[]>('/me/library'),
  libraryItems: (section: string, topic?: string) =>
    call<LibraryEntry[]>(`/me/library/items${q({ section, topic })}`),
  libraryQuestion: (id: string) =>
    call<LibraryQuestion>(`/me/library/items/${encodeURIComponent(id)}`),
  mastery: () => call<Mastery[]>('/me/mastery'),
  connector: () => call<ConnectorStatus>('/me/connector'),
  newConnectorLink: () => call<{ url: string }>('/me/connector', { method: 'POST' }),
  disconnect: () => call<ConnectorStatus>('/me/connector', { method: 'DELETE' }),
  simulations: (section?: string) =>
    call<PublicTbs[]>(`/simulations${section ? `?section=${section}` : ''}`),
  simulation: (id: string) => call<PublicTbs>(`/simulations/${encodeURIComponent(id)}`),
  submitSimulation: (
    id: string,
    responses: Record<string, TaskResponse>,
    durationMs: number,
    sessionId?: string,
  ) =>
    call<SimulationResult>(`/me/simulations/${encodeURIComponent(id)}/attempts`, {
      method: 'POST',
      body: JSON.stringify({ responses, durationMs, sessionId }),
    }),
};

export const SECTIONS = ['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP'] as const;

export const SECTION_NAMES: Record<string, string> = {
  FAR: 'Financial Accounting and Reporting',
  AUD: 'Auditing and Attestation',
  REG: 'Taxation and Regulation',
  BAR: 'Business Analysis and Reporting',
  ISC: 'Information Systems and Controls',
  TCP: 'Tax Compliance and Planning',
};
