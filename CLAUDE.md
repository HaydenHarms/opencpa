# OpenCPA — context for Claude Code

Open-source CPA exam study platform. Owner: Hayden Harms (accounting student, CPA track, Texas). Live at https://opencpa.pages.dev.

## Architecture (all deployed, working)

| Piece   | Where                                                    | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web     | `apps/web`: React + Vite + React Router                  | Cloudflare Pages project `opencpa`. It rebuilds on every push to `main`. The env var `VITE_API_URL=https://opencpa-api.haydenharms.workers.dev` is baked in at build time.                                                                                                                                                                                                                                                                                                                                                                               |
| API     | `apps/api`: Hono on Cloudflare Workers (`opencpa-api`)   | Deployed by the GitHub Actions `deploy-api` job on push to `main`, after the checks pass.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| DB      | Cloudflare D1 `opencpa` (id in `apps/api/wrangler.toml`) | Migrations live in `apps/api/migrations/` and CI applies them (`wrangler d1 migrations apply --remote`). `0001_init`, `0002_sessions` (practice sessions, plus `attempts.session_id`), `0003_connector_tokens`, `0004_variants` (`attempts.variant`, `practice_sessions.variants`) `0005_topic_sessions` (`practice_sessions.topic`), `0006_accounts` (`auth_sessions`, `auth_tokens`, `users.github_login`), `0007_session_modes` and `0008_drop_session_modes` (added, then removed, `practice_sessions.mode`) exist; CI applies anything new on push. |
| Schema  | `packages/schema` (zod)                                  | Source of truth for content: MCQ, plus TBS with `journal_entry` / `numeric` / `research` / `select` tasks.                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Engine  | `packages/engine`                                        | Grading (JE partial credit), FSRS scheduling via ts-fsrs, recency-weighted mastery by blueprint area.                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Content | `content/<section>/<id>.yaml`                            | One item per file. Only `review.status: reviewed` items are served. `pnpm content:build` bundles them into the API.                                                                                                                                                                                                                                                                                                                                                                                                                                      |

- **CORS:** the API only accepts origins listed in `ALLOWED_ORIGINS` (`wrangler.toml`), and wildcards like `https://*.opencpa.pages.dev` are supported. If a custom domain is added, it goes there too, and `VITE_API_URL` changes with it.
- **Identity:** signed out, an anonymous UUID stored in the browser and sent as `X-OpenCPA-User`. Signed in (GitHub or emailed link), a session token sent as `Authorization: Bearer`; signing in moves the device's progress into the account. Design and Hayden's setup steps: `docs/accounts.md`. Providers stay hidden until their Worker secrets exist (`GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET`; `RESEND_API_KEY`/`EMAIL_FROM`, which needs a custom domain).
- **Secrets:** GitHub repo secrets `CLOUDFLARE_API_TOKEN` (Workers Scripts Edit + D1 Edit) and `CLOUDFLARE_ACCOUNT_ID`.

Commands: `pnpm install`, `pnpm dev`, `pnpm test`, `pnpm typecheck`, `pnpm content:validate`, `pnpm db:migrate:local`, `python3 scripts/batches/lint.py` (the deterministic item lint).

## Principles (non-negotiable)

- **Original content only.** Nothing from AICPA released questions, Becker, UWorld, Gleim or Roger. Content is CC BY-SA; code is MIT.
- **The tutor explains, it never grades.** Grading stays deterministic in `packages/engine`.
- **Answers never reach the browser before an attempt.** `toPublicMcq` strips the answer, rationales and explanation.
- **Students bring their own Claude** through the connector, with their own Claude account, so OpenCPA never pays for model calls and hosting stays on Cloudflare's free tier. There is no in-app tutor and no API-key option (Hayden dropped both on 2026-10-02); the connector is the only Claude integration.
- Keep the stack simple. Don't add frameworks without a reason.

## Current state (as of 2026-10-01)

- **Live:** web, API, D1 (migrations 0001–0008), practice sessions with adaptive selection and a 20-question diagnostic (questions and simulations on separate tabs, as the exam separates its testlets), the Library (topic browsing, archive, in-browser search), the simulations player (inside the Library at `/library/<section>/sim/<id>`, incl. `select` tasks), the Claude connector (MCP, four read-only tools at `/mcp/<token>`), and accounts (GitHub sign-in, account deletion, `/privacy` and `/terms`). Design notes and API routes: `docs/history.md`.
- **Variants:** `McqItem.variants` holds new-number versions; sessions rotate through them. Every numeric FAR MCQ has three (variants 10 covered the last four). Simulations have none yet.
- **Bank:** 318 FAR MCQs (17.0% / 46.5% / 36.5% by skill, 38.1% / 34.6% / 27.4% by area) with 771 variants, 1,089 problems in all; 25 BAR MCQs; 21 FAR simulations (Area I 6, II 7, III 8). Every one of the 113 FAR blueprint tasks has two or more MCQs (`python3 scripts/far-coverage.py`). Remembering and Understanding is over its 15% cap until batches 15-17 (Application and Analysis, built but on hold) land.
- **Gate record:** every batch has passed the review gate (FAR 82–90%, BAR 01 84%, simulations 79.7%, 85.0%, 83.2% and 81.8%, no major items). Per-batch results: `docs/reviews/` and `docs/history.md`.
- **Claude leads this project.** Hayden has asked Claude to decide priorities and run the pipeline end to end, then report outcomes.
- **Workflow: commit straight to `main`. No branches, no PRs** (Hayden's instruction). Run the blind verifier and the checks _before_ committing; apply review-agent findings in follow-up commits.

## Content work

**Before drafting, verifying or reviewing any content, read `docs/content-pipeline.md`.** It holds the source pool, the quality bar the review agent grades against, the scaling tactics (parallel slices, variants, families, stratified gate) and the per-batch steps. Every batch passes an independent review agent (`docs/prompts/review-agent.md`): average estimated pass likelihood of at least ~80% and no major-revision items.

## Roadmap (next, in order)

Hayden's direction (2026-09-29): finish FAR completely before any more BAR, AUD, REG or discipline content. Steps 1–3 (practice sessions, the Claude connector, variants) are done; specs in `docs/history.md`. Still open on the connector: what custom connectors allow on the Free plan.

4. **Finish FAR.** "Done" means every representative task in the 2026 FAR blueprint has at least two reviewed MCQs, numeric items carry variants, about 10+ simulations across all three areas have passed the gate, and the skill and area mix is inside the blueprint ranges.
   - FAR batch 14 closed the last 13 one-item tasks (all Remembering and Understanding). Batches 15-17 (45 Application and Analysis items in Areas II and III, built, awaiting verification) bring that skill back under 15%; simulations follow `docs/plans/far-simulations.md` (far-tbs-02 to far-tbs-04, one per area, are done; next far-tbs-05, Area I).
   - Write further batches from the `far-coverage.py` gaps until every task has two items; add each new id to the map in the same commit.
   - Write the next simulation batches (use the `select` task type for classification choices).
5. **Other sections, after FAR is done.** BAR batch 02 first (gaps in `docs/reviews/bar-batch-01.md`; lean toward Area I and II Analysis). BAR targets: Area I 40–50%, II 35–45%, III 10–20%; R&U 10–20%, Application 45–55%, Analysis 30–40%. Then AUD and REG, then the disciplines.
6. **Advanced settings** letting users weight questions toward strengths or weaknesses; brainstorm others.
7. **Accounts: done except email** (`docs/accounts.md`). GitHub sign-in, moving device progress into the account, account and device-data deletion, a Privacy Policy (`/privacy`) and Terms of Use (`/terms`) are live; update those pages whenever the data stored or the services used change. Email sign-in is built but waits for a custom domain (step 8), since Resend needs a verified domain.
8. **Before any publicity:** rate limiting, a UI redesign (Hayden wants it less bland) and a custom domain.
9. **Exam-day mode** (`docs/plans/exam-mode.md`): Phase A (questions and simulations on separate tabs in a session) is done; next Phase B (timed mock exams), then Phase C (literature panel and research tasks).

## Working with Hayden

- He wants changes pushed directly to `main`, with no branches. For each change, give him a short summary plus the changed file(s) as individual files, never a zip.
- Actions logs may not be readable from your session. Public run and job status is available at `https://api.github.com/repos/HaydenHarms/opencpa/actions/runs`; for the actual error text, ask Hayden for a screenshot of the failing step.
- Explain Cloudflare/GitHub dashboard steps click by click.
