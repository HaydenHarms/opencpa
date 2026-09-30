# OpenCPA

**An open-source CPA exam study platform with an AI tutor built in.**

OpenCPA is a free, community-maintained alternative to commercial CPA review courses. It pairs an adaptive question engine and realistic task-based simulations with a personal AI tutor powered by Claude.

**Live:** [opencpa.pages.dev](https://opencpa.pages.dev)

> **Status: alpha.** The platform is deployed end to end (site, API, database, CI). The question bank grows in reviewed batches, FAR first: today there are 150 FAR questions (with about 300 new-number versions), 3 FAR simulations and 25 BAR questions. AUD, REG, ISC and TCP come after FAR is complete. The long-term goal is about 2,000 questions per section.

---

## Features

**Live now**

- **Practice sessions.** Pick a section and a length; the server builds a session that mixes blueprint areas by weight, brings back questions when they're due for review and leans toward your weak topics. Your first session in a section is a short diagnostic, and leaving the page never loses your place.
- **Question versions.** Numeric questions come in several versions with different numbers, so a repeat is a new problem, not a memorized answer.
- **Library.** Browse every exam by blueprint area and topic, practice any single topic, and look up any question in the archive (unanswered, missed, correct). Answers stay hidden until you've attempted a question.
- **Progress.** Coverage by section ("seen 12 of 150"), mastery by blueprint area, and mastery by topic, weakest first.
- **Simulations.** Task-based simulations with exhibits, journal-entry grids, numeric and research tasks, graded deterministically with partial credit.
- **Study with Claude.** Add OpenCPA as a connector in your own Claude account, and Claude can look up the question you just answered and explain it, using the official rationale. It explains; it never grades.

**Planned**

- **Blueprint-aligned content.** Every question and simulation is tagged to the AICPA blueprint by section (FAR, AUD, REG, plus BAR/ISC/TCP), content area, and skill level.
- **Adaptive review.** Spaced repetition (FSRS) schedules individual items, and results roll up into a mastery map by blueprint area so you can see your weak spots at a glance.
- **More simulation task types,** starting with dropdown (select) tasks.
- **Exam-day mode.** Timed testlets modeled on the real exam interface, with a calculator, flag-for-review, and a literature panel.
- **In-app tutor** using your own Anthropic API key, so the project stays free to host and free to use.
- **Advanced settings** for weighting practice toward your strengths or weaknesses.

## Architecture

| Layer    | Tech                                                                   |
| -------- | ---------------------------------------------------------------------- |
| Frontend | React + Vite on Cloudflare Pages                                       |
| API      | Hono on Cloudflare Workers                                             |
| Database | Cloudflare D1 (SQLite)                                                 |
| Tutor    | Remote MCP connector on the API; students use their own Claude account |
| Storage  | Cloudflare R2 (planned: exhibits, media)                               |
| Auth     | Anonymous device id today; GitHub OAuth / email magic link planned     |

```
opencpa/
├── apps/
│   ├── web/          # React + Vite frontend
│   └── api/          # Hono Worker API, D1 migrations
├── packages/
│   ├── engine/       # Grading, FSRS scheduling, mastery rollups
│   └── schema/       # Content schema (zod), shared types
├── content/          # One YAML file per question/simulation
│   ├── far/  aud/  reg/
│   └── bar/  isc/  tcp/
└── scripts/          # Content validation + bundling
```

## Roadmap

- [x] Monorepo scaffold: React site, Hono API, D1 database, content schema, CI
- [x] Deployed to Cloudflare (Pages + Workers + D1) with automatic deploys from `main`
- [x] First reviewed FAR batch (~25 questions)
- [x] Practice sessions with adaptive selection and a diagnostic
- [x] Claude connector: study with your own Claude account
- [x] Question versions (new numbers on every numeric FAR question)
- [x] Task-based simulations (journal-entry grid, numeric, research)
- [x] Library: browse by exam and topic, topic practice, question archive
- [ ] Finish FAR: two or more reviewed questions for every blueprint task, about 10 simulations
- [ ] Remaining sections, in reviewed batches (BAR, then AUD and REG, then ISC and TCP)
- [ ] Advanced practice settings
- [ ] Accounts (GitHub / email) so progress syncs across devices
- [ ] In-app tutor (bring your own Claude API key)
- [ ] Rate limiting, UI redesign, custom domain
- [ ] Exam-day mode

## Content

All content lives in `content/` as plain files, so contributions are just pull requests. CI validates each item against the schema.

```yaml
id: far-leases-0001
type: mcq
blueprint:
  section: FAR
  area: Area II — Select Balance Sheet Accounts
  topic: Leases
  skill: Application
review:
  status: draft # only "reviewed" items are served
  references: [ASC 842-20-30-1]
stem: >
  A lessee signs a 5-year lease ...
choices:
  - { id: A, text: '$84,248', rationale: 'Correct: $20,000 × 4.2124.' }
  - ...
answer: A
explanation: >
  ...
```

**Original content only.** Do not submit AICPA-released questions or material from commercial review providers (Becker, UWorld, Gleim, etc.). They are copyrighted.

## Getting started

```bash
git clone https://github.com/HaydenHarms/opencpa.git
cd opencpa
pnpm install
pnpm db:migrate:local   # create the local D1 database
pnpm dev                # web on :5173, API on :8787
```

Requires Node 22+ and pnpm 10+. `pnpm test` runs the engine and schema tests; `pnpm content:validate` checks every content file.

## Deployment

Pushes to `main` deploy automatically:

- **Site:** Cloudflare Pages builds `apps/web` (build command `pnpm --filter @opencpa/web build`, output `apps/web/dist`). Set `VITE_API_URL` to the API's address and `NODE_VERSION=22`.
- **API:** GitHub Actions runs the checks, applies any new D1 migrations, and deploys the Worker. Needs the repo secrets `CLOUDFLARE_API_TOKEN` (Workers Scripts Edit + D1 Edit) and `CLOUDFLARE_ACCOUNT_ID`.
- **Allowed origins:** the API only accepts browser requests from the origins in `ALLOWED_ORIGINS` (`apps/api/wrangler.toml`). Add any new domain there.

Forking to run your own instance? Create your own D1 database, put its id in `apps/api/wrangler.toml`, and follow the same steps.

## Contributing

Contributions are welcome, especially new questions, simulations, and explanations reviewed by CPAs or CPA candidates. See [CONTRIBUTING.md](CONTRIBUTING.md) for the content format and review checklist.

## Disclaimer

OpenCPA is not affiliated with the AICPA, NASBA, or any state board of accountancy. "CPA" is used descriptively. Content is for study purposes only.

## License

Code: MIT. Content: CC BY-SA 4.0.
