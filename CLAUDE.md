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
- **FAR batch 01** (25 reviewed MCQs) is merged and live (PR #1). Hayden's separate review agent then graded it (accuracy fine, but too easy and a few real defects). The fixes are on branch `content/far-batch-01-revisions`, awaiting merge. See `docs/reviews/far-batch-01.md` for the findings and the fixes. **Lesson: batch 01 was merged before the quality review. From batch 02 on, the review agent runs on the PR and its findings are applied on the same branch before Hayden merges.**

## Content pipeline: how to do a batch

**Source pool:** the legacy bank lives in the repo `HaydenHarms/haydenharms.com`, file `cpa-study.html`. Line 340 (`const EXAMS = [...]`) holds about 700 MCQs across FAR/AUD/REG/BAR/ISC/TCP, and `TBS_DATA` holds 34 simulations. They were AI-generated.

- Treat the bank as **brainstorming material only.** Its structure and topics are _not_ a format to follow. Every item is rebuilt into our schema.
- **Known quality problems in the bank:** wrong distractor math (10 of 25 needed rebuilding in batch 01), items with two correct answers or none, a wrong TBS answer key (FAR TBS 1, task 2), obsolete rules (pre-ASU 2016-14 NFP), and topics that now belong in BAR (pensions, consolidations/business combinations, derivatives/hedging, R&D, sale-leaseback, lease modifications).
- Write from scratch wherever the bank is thin. That is often better than repairing a weak item.

### Quality bar (what the review agent grades against)

Batch 01 passed the answer-key checks but scored about 67% average estimated pass likelihood, so these are now hard requirements:

1. **Difficulty.** At least half of each batch must be multi-step (2–4 adjustments or judgments), the way real FAR items are. Pure recall and one-step arithmetic are the minority.
2. **Skill mix.** Follow the blueprint. FAR targets Remembering and Understanding 5–15%, Application 45–55%, Analysis 35–45%. Tag honestly: Analysis means the student must evaluate or compare, not just compute.
3. **Coverage.** Follow blueprint weights, not availability. FAR: Area I 30–40%, Area II 30–40%, Area III 25–35%. Keep a running topic tally in the review report. Gaps after batch 01: cash, receivables, intangibles, debt, accounting changes and error corrections, subsequent events, fair value.
4. **No giveaway stems.** Never name the classification the student must determine ("meets the criteria," "not constrained," "reasonably possible"). Describe the facts and let the student classify.
5. **State every fact and election needed.** If GAAP permits alternatives (for example, retirement of stock charged wholly to retained earnings, or a release policy), the stem must fix the entity's choice. Otherwise a second answer is defensible.
6. **Distractors.** Every wrong choice maps to a specific, nameable student error, and for numeric items the number must actually result from that error. A distractor that is a _permitted alternative_ is a defect unless the stem excludes it. Deliberately using the superseded rule as a distractor is fine.
7. **Standards currency.** The stem and the key must never rely on a rule a recent ASU eliminated. When an item touches a recently changed area (2015-11 inventory, 2016-02 leases, 2016-13 credit losses, 2016-14 NFP, 2018-13 fair value, etc.), confirm the current rule from FASB, GASB, AICPA, or SEC public sources.
8. **Choice format.** Numeric choices are listed in ascending order (the AICPA convention), and the key's position simply falls out of that. Only word-answer items get the rotated key position. The correct word answer must not be the longest or most qualified choice. `finalize()` and `audit()` in `scripts/batches/common.py` enforce this. Do not hand-shuffle.
9. **Citations.** Paragraph-level ASC/GASB cites must be checked against the Codification or original standard. If you cannot verify a paragraph, cite the Subtopic instead. Batch 01's paragraph cites were written from memory and are unverified.
10. **Stems are plain text.** The Practice page shows the stem as one paragraph, so no tables or line-break formatting. Put multi-item data in prose until the exhibits UI exists.

### Per batch (~25 items)

1. **Plan coverage first.** Pick topics from the blueprint gaps and the skill mix, then find or write items.
2. **Draft** in a script `scripts/batches/<section>-batch-NN.py` that imports `mcq`, `finalize`, `audit`, `write_items` from `common.py`. For each item: re-solve it and compute _every_ number, including each distractor, in code; write a rationale for every choice; add `review.references` and a blueprint `area`/`topic`/`skill`; add `review.asOf` for anything tied to a tax year.
3. **Blind verification.** Run ONE separate subagent using `docs/prompts/blind-verifier.md`, fed a file with stems and choices only (no key, no rationales, no access to content files). Reconcile every disagreement and apply every required fix. It is good at arithmetic and at some second-answer and currency problems, but it is not the quality gate.
4. **Branch and PR.** Put each batch on a `content/<section>-batch-NN` branch, with a review report at `docs/reviews/<section>-batch-NN.md` (process, problems found in the source, exclusions, fixes, the topic and skill tallies). Do not merge until step 5.
5. **Quality review.** Hayden runs his review agent on the branch. Apply its findings with a follow-up commit on the same branch, re-run the blind verifier on any item that changed, note the changes in the report, then Hayden merges.

Retired items are deleted from `content/` (git history keeps them), and a replacement gets a new id. Never reuse an id for a different question, because student progress is keyed to it.

Blueprint areas used for FAR: `Area I — Financial Reporting`, `Area II — Select Balance Sheet Accounts`, `Area III — Select Transactions`. Topic strings follow the blueprint wording (e.g., "Revenue recognition", "Lessee accounting", "State and local government concepts", "Inventory"). Check the current AICPA blueprints for the other sections before tagging. Blueprints are at https://www.aicpa-cima.com (search "CPA exam blueprints").

## Roadmap (next, in order)

1. More FAR batches, driven by the coverage gaps above (cash, receivables, intangibles, debt, accounting changes and errors, subsequent events, fair value) and by raising difficulty and Analysis-level items. Legacy coverage is thin here, so write from scratch. Decision pending with Hayden: whether to also rewrite the ~10 single-step items left in batch 01.
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
