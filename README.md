# OpenCPA

**An open-source CPA exam study platform with an AI tutor built in.**

OpenCPA is a free, community-maintained alternative to commercial CPA review courses. It pairs an adaptive question engine and realistic task-based simulations with a personal AI tutor powered by Claude.

> Status: early scaffolding. FAR is the first section in development.

---

## Features (planned)

- **Blueprint-aligned content.** Every question and simulation is tagged to the AICPA blueprint by section (FAR, AUD, REG, plus BAR/ISC/TCP), content area, and skill level.
- **Adaptive review.** Spaced repetition (FSRS) schedules individual items, and results roll up into a mastery map by blueprint area so you can see your weak spots at a glance.
- **Task-based simulations (TBS).** Interactive journal-entry grids, spreadsheet exhibits, and authoritative-literature research tasks, all graded deterministically.
- **AI tutor.** Claude explains why an answer is right, why a distractor is tempting, and creates fresh variants to check that the concept stuck. The tutor explains; it never grades.
- **Exam-day mode.** Timed testlets modeled on the real exam interface, with a calculator, flag-for-review, and a literature panel.
- **Bring your own key.** Use your own Anthropic API key for the tutor, so the project stays free to host and free to use.

## Architecture

| Layer    | Tech                             |
| -------- | -------------------------------- |
| Frontend | React + Vite on Cloudflare Pages |
| API      | Hono on Cloudflare Workers       |
| Database | Cloudflare D1 (SQLite)           |
| Storage  | Cloudflare R2 (exhibits, media)  |
| Auth     | GitHub OAuth / email magic link  |
| Tutor    | Claude API (tool use)            |

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

## Contributing

Contributions are welcome, especially new questions, simulations, and explanations reviewed by CPAs or CPA candidates. See [CONTRIBUTING.md](CONTRIBUTING.md) for the content format and review checklist.

## Disclaimer

OpenCPA is not affiliated with the AICPA, NASBA, or any state board of accountancy. "CPA" is used descriptively. Content is for study purposes only.

## License

Code: MIT. Content: CC BY-SA 4.0.
