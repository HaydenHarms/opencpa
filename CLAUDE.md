# OpenCPA — context for Claude Code

Open-source CPA exam study platform. Owner: Hayden Harms (accounting student, CPA track, Texas). Live at https://opencpa.pages.dev.

## Architecture (all deployed, working)

| Piece   | Where                                                    | Notes                                                                                                                                                                      |
| ------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web     | `apps/web`: React + Vite + React Router                  | Cloudflare Pages project `opencpa`. It rebuilds on every push to `main`. The env var `VITE_API_URL=https://opencpa-api.haydenharms.workers.dev` is baked in at build time. |
| API     | `apps/api`: Hono on Cloudflare Workers (`opencpa-api`)   | Deployed by the GitHub Actions `deploy-api` job on push to `main`, after the checks pass.                                                                                  |
| DB      | Cloudflare D1 `opencpa` (id in `apps/api/wrangler.toml`) | Migrations live in `apps/api/migrations/` and CI applies them (`wrangler d1 migrations apply --remote`). `0001_init`, `0002_sessions` (practice sessions, plus `attempts.session_id`) and `0003_connector_tokens` exist; CI applies anything new on push.                             |
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
- **Students bring their own Claude**, through the connector with their own Claude account (or later their own API key), so OpenCPA never pays for model calls and hosting stays on Cloudflare's free tier.
- Keep the stack simple. Don't add frameworks without a reason.

## Current state (as of 2026-09-29)

- Scaffold, deploy pipeline and database are all live.
- **Claude connector (roadmap step 2) is built; Hayden's real-account test is pending.** `src/mcp.ts` is a stateless remote MCP server at `/mcp/<token>` (official `@modelcontextprotocol/sdk`, web-standard Streamable HTTP transport, JSON responses, `CfWorkerJsonSchemaValidator` because Workers forbid Ajv's code generation). It has four read-only tools: `get_last_attempt`, `get_current_question` (public fields only), `get_question` (key only if the student attempted it) and `get_my_progress`. Simulation amounts are shown in dollars. Tokens live in `connector_tokens` (migration 0003), stored as SHA-256 hashes, one per student. `GET/POST/DELETE /me/connector` show, rotate or revoke the link, and the site's `/claude` page walks students through adding it. Session helpers shared by the API and MCP code are in `src/sessions.ts`.
- **Practice sessions (roadmap step 1) are done:** `POST /me/sessions`, `GET /me/sessions/current`, `GET /me/sessions/:id`, and `sessionId` on `POST /me/attempts`. Selection rules are in `packages/engine/src/selection.ts`, with tests: area quotas by blueprint weight; within an area, due reviews first, then unseen items leaning toward weak topics, then recently seen items; picks rotate across topics. A student's first session in a section is a 20-question diagnostic with one item per topic. Sessions include simulations, about one per eight questions (`simulationCount`; the FAR exam has 50 MCQs and 7 simulations), picked by the same rules and spread evenly through the session (`spreadThrough`). Exam-day mode will use the exam's order instead. The Practice page resumes an active session and ends with a summary by area and topic, plus simulation points.
- **FAR batch 01** (25 reviewed MCQs) is live on `main`, after three revisions driven by independent quality reviews (history in `docs/reviews/far-batch-01.md`). Revision 3 applied the second review: two items moved to BAR, five-choice items cut to four, giveaway wording removed, and Analysis items written in the blueprint's own task frames.
- **BAR batch 01** (25 items) passed the review gate: 84% average estimated pass likelihood, 15 exam-ready, 10 minor, 0 major; fixes applied. Mix 12% / 56% / 32% by skill (Application one over) and 44% / 44% / 12% by area. Gaps for BAR batch 02 are listed in `docs/reviews/bar-batch-01.md`.
- **FAR batch 05** (25 items) passed the review gate: 82% average estimated pass likelihood, 16 exam-ready, 9 minor, 0 major; the main findings are applied (two items replaced). The **125-item FAR MCQ bank** is 12% / 50% / 38% by skill and 35% / 34% / 31% by area.
- **FAR batch 04** (25 items) passed the review gate after one major fix: 83% average estimated pass likelihood, 13 exam-ready, 11 minor; all findings applied. The **100-item FAR bank** is 12% / 50% / 38% by skill and 35% / 34% / 31% by area, inside every blueprint range.
- **Simulations:** the API, the player UI (`/simulations`) and three blind-verified FAR simulations are live on `main` (merged at Hayden's request; he may ask to revert the UI). Their review gate is still to run.
- **FAR batch 03** (25 items, all new) passed the review gate: 84% average estimated pass likelihood, 23 exam-ready, 2 minor, 0 major; minor findings applied. The 75-item FAR bank is 9% / 53% / 37% by skill and 35% / 35% / 31% by area, all within the blueprint ranges.
- **FAR batch 02** (25 items, all new) passed the review gate on the first run: 85% average estimated pass likelihood, 22 exam-ready, 3 minor, 0 major. The minor findings are applied. The 50-item FAR bank is 8% / 56% / 36% by skill (Application one item over its range) and 34% / 36% / 30% by area.
- **FAR batch 01 passed the review gate** (revision 3: 84% average estimated pass likelihood, 18 exam-ready, 7 minor, 0 major). The gate's minor findings were applied in revision 3b; skill mix after honest retagging is 2 / 14 / 9 (8% / 56% / 36%), area mix 8 / 9 / 8.
- **Claude leads this project.** Hayden has asked Claude to decide priorities and run the pipeline end to end, then report outcomes. Every batch passes an independent review agent (`docs/prompts/review-agent.md`) before it counts as done: average estimated pass likelihood of at least ~80% and no major-revision items.
- **Workflow: commit straight to `main`. No branches, no PRs** (Hayden's instruction). Because nothing sits on a branch for review first, run the blind verifier and the checks *before* committing, and apply Hayden's review-agent findings in follow-up commits.

## Content pipeline: how to do a batch

**Source pool:** the legacy bank lives in the repo `HaydenHarms/haydenharms.com`, file `cpa-study.html`. Line 340 (`const EXAMS = [...]`) holds about 700 MCQs across FAR/AUD/REG/BAR/ISC/TCP, and `TBS_DATA` holds 34 simulations. They were AI-generated.

- Treat the bank as **brainstorming material only.** Its structure and topics are _not_ a format to follow. Every item is rebuilt into our schema.
- **Known quality problems in the bank:** wrong distractor math (10 of 25 needed rebuilding in batch 01), items with two correct answers or none, a wrong TBS answer key (FAR TBS 1, task 2), obsolete rules (pre-ASU 2016-14 NFP), and topics that now belong in BAR (see the scope list under the quality bar).
- Write from scratch wherever the bank is thin. That is often better than repairing a weak item.

### Quality bar (what the review agent grades against)

**Standard:** the AICPA *Uniform CPA Examination Blueprints*, effective January 2026 ([PDF](https://assets.ctfassets.net/rb9cdnjh59cm/71s84dkfo3KEsoLlz4vv6G/f4314469ec5368b5b4dd0d0184f00a71/CPA_Exam_Blueprints_2026.pdf)). Record the edition in each review report, and re-check scope whenever AICPA publishes a new one.

These are hard requirements:

1. **Blueprint scope, per task.** Match every item to a specific representative task in the current blueprint for its section, not just a topic name, and check the skill level fits that task. FAR-versus-BAR traps under the 2026 blueprint:
   - **FAR:** consolidated financial statements with wholly-owned subsidiaries and noncontrolling interests (prepare, adjust, correct); foreign-currency *transaction* gains and losses; finite-lived intangibles, purchased software and cloud computing arrangements; state and local government *concepts only* (recall measurement focus and basis of accounting, determine the appropriate fund); lessee accounting; the revenue five-step model and NFP contributions.
   - **BAR:** goodwill and other indefinite-lived intangibles; business combinations (acquisition-date accounting, including recording NCI); VIEs and deeper NCI topics; functional currency and foreign-currency *translation*; internally developed software; stock compensation; R&D; derivatives and hedging; lessor accounting; Regulation S-X/S-K and segments; employee benefit plan statements; all government calculations (government-wide versus fund amounts, nonexchange revenue, interfund activity, budgetary accounting). Legacy-bank topics that belong here: pensions, business combinations, derivatives, R&D, sale-leaseback, lease modifications.
2. **Skill mix.** FAR targets Remembering and Understanding 5–15%, Application 45–55%, Analysis 35–45%. Tag honestly, using the blueprint's task verbs:
   - **Analysis** = detect, investigate and correct discrepancies in a draft statement or schedule; reconcile a subledger (or bank statement) to the general ledger and determine the adjustment; derive the impact of an error correction, accounting change or transaction (including on the statement of cash flows); review documentation (for example, a legal letter) to decide recognition versus disclosure. Hard multi-step arithmetic alone is Application. So is "adjust ... to correct identified errors" when the stem tells the student what the error is: for Analysis, give the draft figures and supporting facts and let the student find the errors.
   - **Tag by the blueprint's own skill mark for the task, not by difficulty.** Many FAR topics have no Analysis task at all (for example EPS, the statement of comprehensive income, equity transactions, the NFP statement of activities, lessee accounting, revenue, fair value, income taxes), so an item on those topics is Application at most. Analysis tasks are mainly the "detect, investigate and correct discrepancies" and "derive the impact" tasks on the Area I statements (balance sheet, income statement, changes in equity, cash flows, consolidated statements), comparing the notes with the statements, the Area II subledger and bank reconciliations (cash, receivables, inventory, PP&E, payables), deriving the impact of accounting changes and error corrections, and reviewing documentation for contingencies. "Adjust ... to correct identified errors" tasks (including the NFP statements) and "Determine the appropriate fund(s)" are Application. The skill marks are drawn as graphics in the PDF, so check the column position when in doubt.
   - **Remembering and Understanding** = recalling one rule, even when it is dressed in a scenario. A task the blueprint marks Remembering and Understanding (for example modification versus extinguishment, lease classification criteria) stays that level even when the item computes something.
   - **BAR:** targets Remembering and Understanding 10–20%, Application 45–55%, Analysis 30–40%. The BAR blueprint tests Analysis only in Areas I and II, so an Area III (state and local government) item is never Analysis. An item tagged Analysis must ask the student to interpret, compare or choose, not only compute, even when its task is marked Analysis.
3. **Difficulty.** At least half of each batch is multi-step (2–4 adjustments or judgments). Pure recall and one-step arithmetic are the minority.
4. **Coverage.** Follow blueprint weights, not availability. FAR: Area I 30–40%, Area II 30–40%, Area III 25–35%. Keep a running topic tally in the review report.
5. **No giveaways.** The stem never states what the student must decide. That covers classification labels ("meets the criteria," "reasonably possible," "has commercial substance," "distinct"), stated conclusions about measurement evidence ("more clearly evident"), required presentations ("presents as a deduction"), and definition wording ("more than remote but less than likely"). Describe the facts and let the student classify. Stated assessment conclusions ("indicates impairment") are giveaways too. A consolidation or correction item whose stem lists the balances to eliminate or the errors to fix is Application, not Analysis. Don't recite a standard's criteria as a checklist either; leave at least one condition for the candidate to judge from facts. In compare-the-notes items, give draft figures for every note offered as a choice, and don't describe only the item that turns out to be wrong.
6. **State every fact and election needed, but a policy must not be the solution.** Wherever the Codification says an entity *may* do something (for example ASC 810-10-45-18 on allocating upstream profit eliminations), the stem names the entity's choice. If GAAP permits alternatives, the stem fixes the entity's choice briefly and by name ("allocates the excess between APIC and retained earnings"), not as a step-by-step procedure, and the difficulty goes somewhere else. Name the method rather than "the maximum extent GAAP permits": a later ASU can add a method that changes what "maximum" means (ASU 2025-12 did exactly this for share retirements).
7. **Ask exactly one unambiguous question.** Where a balance has both gross and net movements, say "net change in," not "increase in." Every choice, including paired and word choices, must answer the question as asked (same period, same statement line), so none can be ruled out on form alone.
8. **Distractors.** Every wrong choice maps to a specific, nameable student error, and for numeric items the number must actually result from that error. Prefer distractors that come from one error, not two at once. A distractor that is a _permitted alternative_ is a defect unless the stem excludes it. Deliberately using the superseded rule as a distractor is fine. Round every computed amount half up (use `Decimal` with `ROUND_HALF_UP`, not Python's `round()`, which rounds half to even). In a reconciliation item, at least one reconciling item must change the key, or the reconciliation is decoration. Before drafting, search `content/` for the amounts, dates and phrasing you plan to use, so a new item doesn't echo an existing one. Check for duplicates by concept and number set, not just wording, and don't reuse the same stem and choice template for a topic that already has one. Don't build a choice set from combinations of the same two conditions, or put the key in a mirror pair that differs only by the key's qualifier.
9. **Standards currency.** The stem and the key never rely on a rule a recent ASU eliminated. When an item touches a recently changed area (2015-11 inventory, 2016-02 leases, 2016-13 credit losses, 2016-14 NFP, 2017-04 goodwill, 2018-07 nonemployee share-based payments, 2018-08 NFP contributions, 2018-13 fair value, 2018-15 cloud computing, 2020-06 convertibles, 2025-05 credit-loss practical expedient for current receivables, 2025-06 internal-use software, 2025-12 codification improvements including an APIC-only method for share retirements, 2026-01 paid-in-kind preferred dividends), confirm the current rule from FASB, GASB, AICPA, or SEC public sources. When a new ASU creates an election, the stem must say whether the entity elects it. Where early adoption is permitted, check that the old and new rules give the same answer, or fix which one applies.
10. **Choice format.** Exactly four choices, A–D (the schema and `audit()` both enforce this). Numeric choices are in ascending order (the AICPA convention), and the key's position falls out of that. Paired numeric choices ("$30,000 gain; equipment $250,000") lead with a dollar amount and sort on each amount in turn. Avoid clustering distractors from the same error family within a few hundred dollars of the key; spread them across different errors. Only word-answer items get the rotated key position. The correct word answer must not be the longest or most qualified choice. `finalize()` and `audit()` in `scripts/batches/common.py` enforce this. Do not hand-shuffle.
11. **Citations.** Paragraph-level ASC/GASB cites must be checked against the Codification or original standard. If you cannot verify a paragraph, cite the Subtopic instead.
12. **Stems are plain text.** The Practice page shows the stem as one paragraph, so no tables or line-break formatting. Put multi-item data in prose until the exhibits UI exists.

### Per batch (~25 items)

1. **Plan coverage first.** Pick topics from the blueprint gaps and the skill mix, then find or write items.
2. **Draft** in a script `scripts/batches/<section>-batch-NN.py` that imports `mcq`, `finalize`, `audit`, `write_items` from `common.py`. For each item: re-solve it and compute _every_ number, including each distractor, in code; write a rationale for every choice; add `review.references` and a blueprint `area`/`topic`/`skill`; add `review.asOf` for anything tied to a tax year.
3. **Blind verification.** Run ONE separate subagent using `docs/prompts/blind-verifier.md`, fed a file with stems and choices only (no key, no rationales, no access to content files). Reconcile every disagreement and apply every required fix. It is good at arithmetic and at some second-answer and currency problems, but it is not the quality gate.
4. **Commit to `main`.** Write the review report at `docs/reviews/<section>-batch-NN.md` (process, problems found in the source, exclusions, fixes, the topic and skill tallies), run `pnpm content:validate`, then commit and push directly to `main`. No branches.
5. **Quality review (the gate).** Run a fresh review agent with `docs/prompts/review-agent.md` on what landed. Apply its findings in a follow-up commit to `main`, re-run the blind verifier on any item that changed, and note the changes in the report. Repeat until the batch averages at least ~80% estimated pass likelihood with no major-revision items.

Retired items are deleted from `content/` (git history keeps them), and a replacement gets a new id. Never reuse an id for a different question, because student progress is keyed to it.

Blueprint areas used for FAR: `Area I — Financial Reporting`, `Area II — Select Balance Sheet Accounts`, `Area III — Select Transactions`. For BAR: `Area I — Business Analysis`, `Area II — Technical Accounting and Reporting`, `Area III — State and Local Governments`. Topic strings follow the current blueprint wording (e.g., "Statement of cash flows", "Consolidated financial statements", "Trade receivables", "Intangible assets", "Debt (Notes and bonds payable)", "Fair value measurements", "Lessee accounting", "Measurement focus and basis of accounting", "Purpose of funds"; for BAR, "Indefinite-lived intangible assets, including goodwill" and "Nonexchange revenue transactions"). Check the current AICPA blueprints for the other sections before tagging.

## Roadmap (next, in order)

Hayden's direction (2026-09-29): finish FAR completely before any more BAR, AUD, REG or discipline content, and fix how practice works before adding more questions.

1. **Practice sessions and adaptive question selection. Done 2026-09-29** (see Current state). Before this, the Practice page served every item in the same fixed order and lost its place whenever the student left the tab.
   - **Sessions:** the student picks a section and a length (for example 10, 25 or 50 questions). The server builds the session, stores it in D1, and saves progress after every answer, so leaving the page and coming back resumes where the student was. A finished session shows a summary (score, by area and topic).
   - **Selection:** each session mixes topics across the section's blueprint areas, roughly in proportion to the blueprint weights. Within a topic, pick items the student needs most: FSRS items that are due first, then the weakest topics by mastery, then unseen items chosen at random (never the same fixed order). Keep the rule in `packages/engine` with tests.
   - **Diagnostic:** a student's first session in a section is a short diagnostic (about 20 questions, spread evenly across topics), so the selection has data to work from.
2. **Claude connector (MCP), the first tutor. Built 2026-09-29; confirm on Hayden's Claude account, including what the Free plan allows.** Students keep OpenCPA open in one tab and the Claude app (claude.ai, desktop or mobile) in another, with OpenCPA added as a custom connector. Claude looks up what the student just did and explains it. The student's own Claude subscription pays for Claude inside Anthropic's own app, which the terms allow. OpenCPA pays nothing, because our server only answers lookups.
   - **Why this route:** Anthropic's terms allow Claude Free, Pro and Max sign-ins only in Claude's own apps, so a third-party app can't bill a student's subscription. An in-app tutor would need the student's API key or Hayden paying for API use.
   - **Endpoint:** a remote MCP server at `/mcp` on the existing Worker, with no model calls of its own. The tools:
     - `get_last_attempt`: the item the student just answered, their choice, the key, the rationales and the explanation.
     - `get_question`: any item by id. The key is included only if the student has already attempted it, so Claude can't spoil unanswered items.
     - `get_my_progress`: weak areas and topics, and recent misses.
     - After step 1, `get_current_question`, so Claude can give hints before the student answers (public fields only).
   - **Linking Claude to the student (experiment):** a "Connect Claude" button on the site shows a personal connector URL carrying a secret token tied to the student's anonymous id. Treat that token like a password: it can be revoked and regenerated. Replace it with OAuth once accounts exist.
   - **Test** on Hayden's own Claude account: answer items on the site, then ask Claude about them. Confirm what custom connectors allow on the Free plan before counting on free-plan students.
   - **The tutor explains; it never grades.** Grading stays in `packages/engine`.
   - **Later options,** pending Hayden's cost decision: an in-app tutor at `POST /me/tutor`, either hosted (Hayden pays, with a daily cap per student and Turnstile) or using the student's own API key; and a Claude Code plugin for students who already use Claude Code.
3. **Question variants.** The legacy tool rotated the numbers across four versions of each question so students couldn't memorize answers.
   - Add optional `variants` to the MCQ schema: each variant has its own stem, choices, answer, rationales and explanation. Word-answer items don't need variants.
   - Progress stays keyed to the item id. The API serves a different variant on each attempt and records which one it served.
   - The batch scripts already compute every number in code, so they generate the variants too. Every variant goes through `audit()` and the blind verifier.
   - New FAR batches ship with variants. Retrofit the existing numeric FAR items in batches.
4. **Finish FAR.** "Done" means all of the following:
   - every representative task in the 2026 FAR blueprint has at least two reviewed MCQs;
   - numeric items carry variants;
   - there are about 10 or more simulations across all three areas, each through the review gate;
   - the bank's skill and area mix is inside the blueprint ranges.

   In order:
   - Run the review gate on the three live simulations and act on Hayden's UI feedback.
   - Write **FAR batch 06**, covering the gaps named in `docs/reviews/far-batch-05.md`: fund determination, the NFP statement of financial position, NFP cash flows and notes, amortized-cost investments and debt covenants. Go light on revenue, with about three Remembering and Understanding items at most.
   - Write further batches until every blueprint task is covered.
   - Write the next simulation batches.
5. **Other sections, after FAR is done.**
   - BAR batch 02 comes first. Its gaps are in `docs/reviews/bar-batch-01.md`; lean toward Area I and II Analysis items to bring Application back under 55%. BAR targets: Area I 40–50%, II 35–45%, III 10–20%; Remembering and Understanding 10–20%, Application 45–55%, Analysis 30–40%.
   - Then AUD and REG, then the disciplines.
6. **Accounts** (GitHub OAuth or email magic link), moving a student's anonymous progress into their account.
7. **Before any publicity:** rate limiting, a UI redesign (the current UI is intentionally plain, and Hayden wants it less bland) and a custom domain.
8. Exam-day mode.

## Working with Hayden

- He wants changes pushed directly to `main`, with no branches. For each change, give him a short summary plus the changed file(s) as individual files, never a zip.
- Actions logs may not be readable from your session. Public run and job status is available at `https://api.github.com/repos/HaydenHarms/opencpa/actions/runs`; for the actual error text, ask Hayden for a screenshot of the failing step.
- Explain Cloudflare/GitHub dashboard steps click by click.
