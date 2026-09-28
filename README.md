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

| Layer     | Tech                                   |
|-----------|----------------------------------------|
| Frontend  | SvelteKit on Cloudflare Pages          |
| API       | Hono on Cloudflare Workers             |
| Database  | Cloudflare D1 (SQLite) + Drizzle ORM   |
| Storage   | Cloudflare R2 (exhibits, media)        |
| Auth      | GitHub OAuth / email magic link        |
| Tutor     | Claude API (tool use)                  |

```
opencpa/
├── apps/
│   ├── web/          # SvelteKit frontend
│   └── api/          # Hono Worker API + tutor endpoints
├── packages/
│   ├── engine/       # FSRS scheduling, grading, mastery rollups
│   └── schema/       # Shared content + DB types (zod)
├── content/
│   ├── far/          # Questions & simulations as Markdown/YAML
│   ├── aud/
│   └── reg/
└── docs/
```

## Content

All content lives in `content/` as plain files, so contributions are just pull requests. CI validates each item against the schema.

```yaml
id: far-leases-0001
section: FAR
area: "Select transactions — Leases"
skill: Application
type: mcq
stem: >
  A lessee signs a 5-year lease ...
choices: [ ... ]
answer: B
explanation: >
  ...
```

**Original content only.** Do not submit AICPA-released questions or material from commercial review providers (Becker, UWorld, Gleim, etc.). They are copyrighted.

## Getting started

```bash
git clone https://github.com/HaydenHarms/opencpa.git
cd opencpa
pnpm install
pnpm dev
```

## Contributing

Contributions are welcome, especially new questions, simulations, and explanations reviewed by CPAs or CPA candidates. See `CONTRIBUTING.md` (coming soon).

## Disclaimer

OpenCPA is not affiliated with the AICPA, NASBA, or any state board of accountancy. "CPA" is used descriptively. Content is for study purposes only.

## License

Code: MIT. Content: CC BY-SA 4.0.
