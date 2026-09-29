# OpenCPA — context for Claude Code

Open-source CPA exam study platform. Owner: Hayden Harms (accounting student, CPA track, Texas). Live at https://opencpa.pages.dev.

## Architecture (all deployed, working)

| Piece   | Where                                                    | Notes                                                                                                                                                                      |
| ------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web     | `apps/web`: React + Vite + React Router                  | Cloudflare Pages project `opencpa`. It rebuilds on every push to `main`. The env var `VITE_API_URL=https://opencpa-api.haydenharms.workers.dev` is baked in at build time. |
| API     | `apps/api`: Hono on Cloudflare Workers (`opencpa-api`)   | Deployed by the GitHub Actions `deploy-api` job on push to `main`, after the checks pass.                                                                                  |
| DB      | Cloudflare D1 `opencpa` (id in `apps/api/wrangler.toml`) | Migrations live in `apps/api/migrations/` and CI applies them (`wrangler d1 migrations apply --remote`). `0001_init` has already been applied.                             |
| Schema  | `packages/schema` (zod)                                  | Source of truth for content: MCQ, plus TBS with `journal_entry` / `numeric` / `research` tasks.                                                                            |
| Engine  | `packages/engine`                                        | Grading (JE partial credit), FSRS scheduling via ts-fsrs, recency-weighted mastery by blueprint area.                                                                      |
| Content | `content/<section>/<id>.yaml`                            | One item per file. Only `review.status: reviewed` items are served. `pnpm content:build` bundles them into the API.                                                        |

- **CORS:** the API only accepts origins listed in `ALLOWED_ORIGINS` (`wrangler.toml`), and wildcards like `https://*.opencpa.pages.dev` are supported. If a custom domain is added, it goes there too, and `VITE_API_URL` changes with it.
- **Identity:** for now it's an anonymous UUID stored in the browser and sent as `X-OpenCPA-User`. There are no real accounts yet.
- **Secrets:** GitHub repo secrets `CLOUDFLARE_API_TOKEN` (Workers Scripts Edit + D1 Edit) and `CLOUDFLARE_ACCOUNT_ID`.

Commands: `pnpm install`, `pnpm dev`, `pnpm test`, `pnpm typecheck`, `pnpm content:validate`, `pnpm db:migrate:local`.

## Principles (non-negotiable)

- **Original content only.** Nothing from AICPA released questions, Becker, UWorld, Gleim or Roger. Content is CC BY-SA; code is MIT.
- **The tutor explains, it never grades.** Grading stays deterministic in `packages/engine`.
- **Answers never reach the browser before an attempt.** `toPublicMcq` strips the answer, rationales and explanation.
- **Bring your own key** for the Claude tutor, so hosting stays on Cloudflare's free tier.
- Keep the stack simple. Don't add frameworks without a reason.

## Current state (as of 2026-09-28)

- Scaffold, deploy pipeline and database are all live.
- **FAR batch 01** (25 reviewed MCQs) is on branch `content/far-batch-01`, waiting for Hayden to open and merge the PR. The review report is at `docs/reviews/far-batch-01.md`, and the generator is `scripts/batches/far-batch-01.py`.

## Content pipeline: how to do a batch

**Source pool:** the legacy bank lives in the repo `HaydenHarms/haydenharms.com`, file `cpa-study.html`. Line 340 (`const EXAMS = [...]`) holds about 700 MCQs across FAR/AUD/REG/BAR/ISC/TCP, and `TBS_DATA` holds 34 simulations. They were AI-generated.

- Treat the bank as **brainstorming material only.** Its structure and topics are _not_ a format to follow. Every item is rebuilt into our schema.
- **Known quality problems:** wrong distractor math (10 of 25 needed rebuilding in batch 01), items with two correct answers or none, a wrong TBS answer key (FAR TBS 1, task 2), and topics filed under FAR that now belong in BAR (pensions, consolidations/business combinations, derivatives/hedging, R&D, sale-leaseback, lease modifications).
- Ideas can also come from scratch, where the bank is thin.

**Per batch (~25 items):**

1. **Triage.** Only take items that fall inside the section's _current_ AICPA blueprint.
2. **Re-solve every item** and compute _every_ number, including each distractor, in code. A distractor's rationale must name an error that actually produces that number.
3. **Write it in the schema:** a rationale for every choice, `review.references` (ASC/GASB/IRC paragraph), a blueprint `area`/`topic`/`skill`, and `review.asOf` for anything tied to a tax year.
4. **Balance answer positions.** Use the `place_answers()` helper in the batch script; without it, keys cluster on A.
5. **Blind verification.** Run ONE separate subagent that sees only stems and choices (no key, no repo access to content) and solves every item, doing its arithmetic in code. Reconcile any disagreement and fix any flagged problems. Use a single verifier for independence; don't parallelize the drafting across agents.
6. **Branch and PR.** Put each batch on a `content/<section>-batch-NN` branch with a review report at `docs/reviews/<section>-batch-NN.md` (process, problems found in the source, exclusions, fixes). Hayden merges it.

Blueprint areas used for FAR: `Area I — Financial Reporting`, `Area II — Select Balance Sheet Accounts`, `Area III — Select Transactions`. Topic strings follow the blueprint wording (e.g., "Revenue recognition", "Lessee accounting", "State and local government concepts"). Check the current AICPA blueprints for the other sections before tagging.

## Roadmap (next, in order)

1. More FAR batches. Next priorities: inventory, receivables, debt/bonds, cash, intangibles, accounting changes/errors, subsequent events, fair value, and more government/NFP. Legacy coverage is thin here, so expect to write more explanations from scratch.
2. The other sections, including a BAR set built from the topics moved out of FAR.
3. TBS frontend: a journal-entry grid, numeric and research task UIs, and exhibits. Then import the vetted simulations.
4. Accounts (GitHub OAuth / email magic link), migrating anonymous progress to the account.
5. Claude tutor at `POST /me/tutor` (currently a 501 stub), using the student's own API key. Give it tools for the current item, recent misses and generating a variant.
6. Before any publicity: rate limiting, a UI redesign (the current UI is intentionally plain; Hayden wants it less bland) and a custom domain.
7. Exam-day mode.

## Working with Hayden

- He wants changes pushed directly. For each change, give him a short summary plus the changed file(s) as individual files, never a zip.
- Actions logs may not be readable from your session. Public run and job status is available at `https://api.github.com/repos/HaydenHarms/opencpa/actions/runs`; for the actual error text, ask Hayden for a screenshot of the failing step.
- Pull requests may have to be opened by Hayden through a compare link if no GitHub API token is available.
- Explain Cloudflare/GitHub dashboard steps click by click.
