import { createEmptyCard, fsrs, Rating, type Card, type Grade } from 'ts-fsrs';

export type { Card };
export { Rating };

const scheduler = fsrs({ enable_fuzz: true });

export function newCard(now = new Date()): Card {
  return createEmptyCard(now);
}

/**
 * Map an attempt to an FSRS rating. Grading is binary for now;
 * a wrong answer is "Again", a right one "Good" (or "Hard" if the
 * student reported low confidence).
 */
export function ratingFor(correct: boolean, lowConfidence = false): Grade {
  if (!correct) return Rating.Again;
  return lowConfidence ? Rating.Hard : Rating.Good;
}

export function review(card: Card, rating: Grade, now = new Date()): Card {
  return scheduler.next(card, now, rating).card;
}
