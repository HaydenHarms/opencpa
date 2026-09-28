# Content

One item per file, named after its id: `content/far/far-leases-0001.yaml`.

- Items are validated against `packages/schema` on every push (`pnpm content:validate`).
- Only items with `review.status: reviewed` are served to students. Drafts stay in the repo until they pass review.
- Currency amounts in simulations are whole **cents** (`$5,800.00` → `580000`).

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the review checklist and full examples.
