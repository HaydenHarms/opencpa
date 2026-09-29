import type { JournalLine, PublicMcq, PublicTbs } from '@opencpa/schema';

const BASE = import.meta.env.VITE_API_URL ?? '/api';

/** Anonymous device id until accounts land. */
function userId(): string {
  try {
    let id = localStorage.getItem('opencpa:user');
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem('opencpa:user', id);
    }
    return id;
  } catch {
    return ((window as unknown as { __opencpaUser?: string }).__opencpaUser ??=
      crypto.randomUUID());
  }
}

async function call<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(BASE + path, {
    ...init,
    headers: { 'Content-Type': 'application/json', 'X-OpenCPA-User': userId(), ...init?.headers },
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
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
  status: 'active' | 'completed' | 'abandoned';
  createdAt: number;
  completedAt: number | null;
  /** Questions and simulations, in serving order. */
  items: (PublicMcq | PublicTbs)[];
  /** Results for the items already answered, keyed by item id. */
  answered: Record<string, Revealed | SimulationReveal>;
}

/** A session length on offer and the simulations that come with it. */
export interface SessionOption {
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
  | { type: 'research'; citation: string };

export interface TaskResult {
  id: string;
  earned: number;
  possible: number;
  correct: boolean;
  answer: number | string[] | JournalLine[];
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

export const api = {
  questions: (section?: string) =>
    call<PublicMcq[]>(`/questions${section ? `?section=${section}` : ''}`),
  attempt: (itemId: string, selected: string, durationMs: number, sessionId?: string) =>
    call<AttemptResult>('/me/attempts', {
      method: 'POST',
      body: JSON.stringify({ itemId, selected, durationMs, sessionId }),
    }),
  currentSession: (section: string) =>
    call<SessionStatus>(`/me/sessions/current?section=${section}`),
  startSession: (section: string, size: number) =>
    call<Session>('/me/sessions', { method: 'POST', body: JSON.stringify({ section, size }) }),
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
