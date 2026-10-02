# OpenCPA — context for Claude Code

Open-source CPA exam study platform. Owner: Hayden Harms (accounting student, CPA track, Texas). Live at https://opencpa.pages.dev.

## Architecture (all deployed, working)

| Piece   | Where                                                    | Notes                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web     | `apps/web`: React + Vite + React Router                  | Cloudflare Pages project `opencpa`. It rebuilds on every push to `main`. The env var `VITE_API_URL=https://opencpa-api.haydenharms.workers.dev` is baked in at build time.                                                                                                                                                                                                       |
| API     | `apps/api`: Hono on Cloudflare Workers (`opencpa-api`)   | Deployed by the GitHub Actions `deploy-api` job on push to `main`, after the checks pass.                                                                                                                                                                                                                                                                                        |
| DB      | Cloudflare D1 `opencpa` (id in `apps/api/wrangler.toml`) | Migrations live in `apps/api/migrations/` and CI applies them (`wrangler d1 migrations apply --remote`). `0001_init`, `0002_sessions` (practice sessions, plus `attempts.session_id`), `0003_connector_tokens`, `0004_variants` (`attempts.variant`, `practice_sessions.variants`) and `0005_topic_sessions` (`practice_sessions.topic`) exist; CI applies anything new on push. |
| Schema  | `packages/schema` (zod)                                  | Source of truth for content: MCQ, plus TBS with `journal_entry` / `numeric` / `research` / `select` tasks.                                                                                                                                                                                                                                                                       |
| Engine  | `packages/engine`                                        | Grading (JE partial credit), FSRS scheduling via ts-fsrs, recency-weighted mastery by blueprint area.                                                                                                                                                                                                                                                                            |
| Content | `content/<section>/<id>.yaml`                            | One item per file. Only `review.status: reviewed` items are served. `pnpm content:build` bundles them into the API.                                                                                                                                                                                                                                                              |

- **CORS:** the API only accepts origins listed in `ALLOWED_ORIGINS` (`wrangler.toml`), and wildcards like `https://*.opencpa.pages.dev` are supported. If a custom domain is added, it goes there too, and `VITE_API_URL` changes with it.
- **Identity:** for now it's an anonymous UUID stored in the browser and sent as `X-OpenCPA-User`. There are no real accounts yet.
- **Secrets:** GitHub repo secrets `CLOUDFLARE_API_TOKEN` (Workers Scripts Edit + D1 Edit) and `CLOUDFLARE_ACCOUNT_ID`.

Commands: `pnpm install`, `pnpm dev`, `pnpm test`, `pnpm typecheck`, `pnpm content:validate`, `pnpm db:migrate:local`, `python3 scripts/batches/lint.py` (the deterministic item lint).

## Principles (non-negotiable)

- **Original content only.** Nothing from AICPA released questions, Becker, UWorld, Gleim or Roger. Content is CC BY-SA; code is MIT.
- **The tutor explains, it never grades.** Grading stays deterministic in `packages/engine`.
- **Answers never reach the browser before an attempt.** `toPublicMcq` strips the answer, rationales and explanation.
- **Students bring their own Claude**, through the connector with their own Claude account (or later their own API key), so OpenCPA never pays for model calls and hosting stays on Cloudflare's free tier.
- Keep the stack simple. Don't add frameworks without a reason.

## Current state (as of 2026-10-01)

- **Live:** web, API, D1 (migrations 0001–0005), practice sessions with adaptive selection and a 20-question diagnostic, the Library (topic browsing, archive, in-browser search), the simulations player (`/simulations`, incl. `select` tasks) and the Claude connector (MCP, four read-only tools at `/mcp/<token>`). Design notes and API routes: `docs/history.md`.
- **Variants:** `McqItem.variants` holds new-number versions; sessions rotate through them. Every numeric FAR MCQ has three, except `far-accounting-errors-0002`, `far-contingencies-0005`, `far-debt-covenant-0001`, `far-revenue-allocation-0003`. Simulations have none yet.
- **Bank:** 300 FAR MCQs (13.7% / 49.3% / 37.0% by skill, 35.7% / 35.3% / 29.0% by area) with 744 variants, 1,044 problems in all; 25 BAR MCQs; 3 FAR simulations. `python3 scripts/far-coverage.py` prints the blueprint tasks with fewer than two items: after batches 12 and 13, 100 of 113 have two or more, and the 13 left are all Remembering and Understanding (13.7%, cap 15%).
- **Gate record:** every batch has passed the review gate (FAR 82–90%, BAR 01 84%, simulations 79.7%, no major items). Per-batch results: `docs/reviews/` and `docs/history.md`.
- **Claude leads this project.** Hayden has asked Claude to decide priorities and run the pipeline end to end, then report outcomes.
- **Workflow: commit straight to `main`. No branches, no PRs** (Hayden's instruction). Run the blind verifier and the checks _before_ committing; apply review-agent findings in follow-up commits.

## Content work

**Before drafting, verifying or reviewing any content, read `docs/content-pipeline.md`.** It holds the source pool, the quality bar the review agent grades against, the scaling tactics (parallel slices, variants, families, stratified gate) and the per-batch steps. Every batch passes an independent review agent (`docs/prompts/review-agent.md`): average estimated pass likelihood of at least ~80% and no major-revision items.

## Roadmap (next, in order)

Hayden's direction (2026-09-29): finish FAR completely before any more BAR, AUD, REG or discipline content. Steps 1–3 (practice sessions, the Claude connector, variants) are done; specs in `docs/history.md`. Still open on the connector: what custom connectors allow on the Free plan, and Hayden's cost decision on an in-app tutor (`POST /me/tutor`) or a Claude Code plugin.

4. **Finish FAR.** "Done" means every representative task in the 2026 FAR blueprint has at least two reviewed MCQs, numeric items carry variants, about 10+ simulations across all three areas have passed the gate, and the skill and area mix is inside the blueprint ranges.
   - FAR batches 12 and 13 (built in parallel) closed every one-item Application task. FAR batch 14 closes the 13 remaining Remembering and Understanding tasks; to keep that skill under 15%, pair them with about 15 Application and Analysis items (Analysis at 40%+ of the batch), leaning toward Area III (29.0%).
   - Write further batches from the `far-coverage.py` gaps until every task has two items; add each new id to the map in the same commit.
   - Write the next simulation batches (use the `select` task type for classification choices).
5. **Other sections, after FAR is done.** BAR batch 02 first (gaps in `docs/reviews/bar-batch-01.md`; lean toward Area I and II Analysis). BAR targets: Area I 40–50%, II 35–45%, III 10–20%; R&U 10–20%, Application 45–55%, Analysis 30–40%. Then AUD and REG, then the disciplines.
6. **Advanced settings** letting users weight questions toward strengths or weaknesses; brainstorm others.
7. **Accounts** (GitHub OAuth or email magic link), moving anonymous progress into the account.
8. **Before any publicity:** rate limiting, a UI redesign (Hayden wants it less bland) and a custom domain.
9. Exam-day mode.

## Working with Hayden

- He wants changes pushed directly to `main`, with no branches. For each change, give him a short summary plus the changed file(s) as individual files, never a zip.
- Actions logs may not be readable from your session. Public run and job status is available at `https://api.github.com/repos/HaydenHarms/opencpa/actions/runs`; for the actual error text, ask Hayden for a screenshot of the failing step.
- Explain Cloudflare/GitHub dashboard steps click by click.
