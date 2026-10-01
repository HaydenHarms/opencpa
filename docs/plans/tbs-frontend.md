# Plan: task-based simulations (TBS)

Status: milestones 1–3 (API, player UI, three verified simulations) are on `main`, merged 2026-09-29 at Hayden's request and approved by him for now on 2026-09-30. Remaining: the review gate on the three simulations, and research tasks. Written as roadmap item 2 in `CLAUDE.md`.

## Why now

Task-based simulations are about half of the FAR score. The MCQ bank now touches every FAR content group, so the next most valuable thing for a student is practising the other half of the exam. Most of the plumbing already exists: `packages/schema` defines `TbsItem` with `numeric`, `journal_entry` and `research` tasks plus markdown exhibits, and `packages/engine` already grades all three (`gradeTask`, with partial credit for journal entries). What is missing is a public projection, API routes, the UI, and content.

## Scope

**In:** a simulation list and player on the web app; the three existing task types; exhibits; grading and review through the existing attempts and FSRS tables; three original FAR simulations to exercise every task type.

**Out for now:** document-review (drop-down edit) tasks, spreadsheet-style free-form workpapers, timers and exam-day mode, importing the 34 legacy simulations (a later content milestone, each one rebuilt and verified like an MCQ batch).

## Design

### Schema (`packages/schema`)
- Add `PublicTbs` and `toPublicTbs(t)`: keeps `id`, `type`, `blueprint`, `title`, `scenario`, `exhibits`, and for each task its `id`, `type`, `prompt`, `points`, plus `accounts` (journal entries) and `unit` (numeric). Strips `answer`, `explanation` and `tolerance`. Unit tests in `index.test.ts` assert that no answer field survives, mirroring `toPublicMcq`.
- Add a TBS rule to the content validator: every task has an explanation, points total to a whole number, and research answers use the `ASC xxx-xx-xx-x` form.

### API (`apps/api`)
- `GET /simulations?section=` and `GET /simulations/:id`: public projections only.
- `POST /me/simulations/:id/attempts` with `{ responses: Record<taskId, TaskResponse>, durationMs? }`. Grades each task with `gradeTask`, stores one `attempts` row per simulation (`earned` and `possible` summed, `response` holding the per-task JSON), updates the FSRS card with a rating from the score (for example at least 75% = Good, 50–75% = Hard, under 50% = Again), and returns per-task results with answers and explanations. No migration is needed: the existing tables already hold `earned`, `possible` and a JSON `response`.
- Journal-entry amounts travel as whole cents, matching the schema.

### Web (`apps/web`)
- New route `/simulations` (list, filtered by section like Practice) and `/simulations/:id` (player).
- Player layout: scenario and a task list on the left; an exhibits panel with tabs on the right (stacked on phones). One task visible at a time with previous/next, and a submit-all button, as on the exam.
- **Numeric task:** a currency input that accepts `1,234.56` or `(1,234)` and converts to cents; percent and unit tasks use plain number inputs.
- **Journal entry task:** a grid of rows with an account drop-down (from `task.accounts`), debit and credit inputs, add and remove row buttons, and running debit and credit totals that flag an unbalanced entry before submission.
- **Research task:** a citation input with the expected format shown as placeholder text (`ASC 842-20-30-1`).
- **Exhibits:** markdown with tables. Render with a small markdown library (`marked`, tables only, raw HTML disabled). Content is ours, but disabling HTML keeps the page safe if that ever changes.
- After submission: per-task score, the correct answer, and the explanation; journal-entry rows marked matched or missing.

### Content
- Write three original FAR simulations in `scripts/batches/far-tbs-01.py` (same pipeline as MCQ batches: compute every number in code, blind verification, review gate). Candidates: (1) lessee finance lease — journal entries at commencement and year-end plus a numeric year-2 expense; (2) bank reconciliation — numeric adjusted balance plus the adjusting entries; (3) contingencies — a research task plus a numeric accrual.
- **Open issue — research answers.** A research task needs an exact paragraph citation, and the quality bar forbids unverified paragraph cites. Before shipping research tasks, confirm each cited paragraph against the Codification (the FASB basic view is free with registration) and record how it was checked in the review report. Until then, ship simulations with numeric and journal-entry tasks only.

## Milestones and acceptance

1. **Schema and API (done)** — `toPublicTbs` with tests; `gradeSimulation` and `ratingForScore` in the engine with tests; three routes; engine tests for `gradeTask` edge cases (wrong type, empty journal lines, tolerance). Acceptance: `pnpm test` and `pnpm typecheck` pass; `GET /simulations/:id` returns no answer fields (tested).
2. **Player UI** — list and player pages, three task components, exhibits. Acceptance: a simulation can be completed end to end in `pnpm dev`; the journal grid blocks nothing but warns on an unbalanced entry; the layout works at phone width.
3. **Content** — three verified FAR simulations through blind verification and the review gate. Acceptance: gate average at least ~80% with no major-revision items.
4. **Deploy and smoke test** — confirm the live API serves the simulations without answers, and that a submission records an attempt and schedules a review.

UI changes should be reviewed by Hayden in a preview deployment before they go to `main`, since the site is live.

## Milestone 1 notes

- `GET /simulations`, `GET /simulations/:id` and `POST /me/simulations/:id/attempts` are in `apps/api/src/index.ts`. The attempt route validates responses with zod (journal amounts are whole cents, at most 20 lines), grades with `gradeSimulation`, rates the review card with `ratingForScore`, and stores the attempt through the same `saveAttempt` helper the MCQ route now uses.
- Smoke-tested on a local worker with a temporary simulation: the public projection carried no answers or explanations, and a partially correct submission scored 2 of 3 and scheduled a review. No simulations ship yet, so the live `/simulations` list is empty until milestone 3.
- `/me/review/due` still returns MCQs only; simulations due for review can be added with the player UI.
