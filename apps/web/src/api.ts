import type { PublicMcq } from '@opencpa/schema';

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

export interface AttemptResult {
  correct: boolean;
  answer: string;
  explanation: string;
  rationales: Record<string, string>;
  nextDue: string;
}

export interface Mastery {
  section: string;
  area: string;
  attempts: number;
  score: number;
}

export const api = {
  questions: (section?: string) =>
    call<PublicMcq[]>(`/questions${section ? `?section=${section}` : ''}`),
  attempt: (itemId: string, selected: string, durationMs: number) =>
    call<AttemptResult>('/me/attempts', {
      method: 'POST',
      body: JSON.stringify({ itemId, selected, durationMs }),
    }),
  mastery: () => call<Mastery[]>('/me/mastery'),
};

export const SECTIONS = ['FAR', 'AUD', 'REG', 'BAR', 'ISC', 'TCP'] as const;
