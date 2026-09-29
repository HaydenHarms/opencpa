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
  items: PublicMcq[];
  /** Results for the questions already answered, keyed by item id. */
  answered: Record<string, Revealed>;
}

export interface SessionStatus {
  session: Session | null;
  nextKind: 'diagnostic' | 'practice';
  diagnosticSize: number;
  poolSize: number;
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

export interface SimulationResult {
  earned: number;
  possible: number;
  correct: boolean;
  tasks: TaskResult[];
  nextDue: string;
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
  simulations: (section?: string) =>
    call<PublicTbs[]>(`/simulations${section ? `?section=${section}` : ''}`),
  simulation: (id: string) => call<PublicTbs>(`/simulations/${encodeURIComponent(id)}`),
  submitSimulation: (id: string, responses: Record<string, TaskResponse>, durationMs: number) =>
    call<SimulationResult>(`/me/simulations/${encodeURIComponent(id)}/attempts`, {
      method: 'POST',
      body: JSON.stringify({ responses, durationMs }),
    }),
};

export const SECTIONS = ['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP'] as const;
