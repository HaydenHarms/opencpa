# Review report: FAR batch 15

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**13 items**, all written from scratch in `scripts/batches/far-batch-15.py`, all Area II (Select Balance
Sheet Accounts) and all numeric with three variants each (39 variants), so the batch adds 52 problems.
Every variant family moves the key's letter. Built as one slice of batches 15-17 (45 Application and
Analysis items closing the skill-mix gap batch 14 left: Remembering and Understanding over its 15% cap
until these land); the other slices cover different tasks and ids.

## Plan

Nine Analysis items spread across six Area II Analysis tasks, preferring the tasks with the fewest
existing items (II.A.b and II.A.c, at four each, get two items; II.B.c, II.C.c and II.D.f, at five each,
get the rest), each changing at least two of the scenario's component events against every existing item
on its task and using a stem format none of them uses. Four Application items on four of the twelve
eligible Area II Application tasks (all tied at two items apiece except II.I.a, at four, which was
skipped), chosen to spread across different accounts rather than stack on investments: cloud computing
(ASU 2018-15/2025-06), exit-cost timing, bond interest with detachable warrants, and a debt covenant.

| Item | Blueprint task | Skill |
| --- | --- | --- |
| `far-cash-bank-reconciliation-0006` | II.A.b Reconcile the bank balance to the general ledger (note collected, card-processor discount fee, stopped check) | Analysis |
| `far-cash-bank-reconciliation-0007` | II.A.b (bank error depositing another customer's item, uncredited interest, a stale-but-still-outstanding check) | Analysis |
| `far-cash-unreconciled-0004` | II.A.c Investigate unreconciled cash balances to determine an adjustment (misdirected wire, stop-payment fee, duplicate petty-cash disbursement) | Analysis |
| `far-cash-unreconciled-0005` | II.A.c (auto-debited insurance premium, a deposit posted to the wrong journal, a counterfeit bill) | Analysis |
| `far-receivables-rollforward-0006` | II.B.c Prepare a rollforward of trade receivables (recourse factoring as a secured borrowing, a bill-and-hold order, a rebate netted against collections) | Analysis |
| `far-receivables-rollforward-0007` | II.B.c (customer credit balances netted against receivables, a late cutoff on a return, a recovery that never touched AR) | Analysis |
| `far-inventory-rollforward-0006` | II.C.c Prepare a rollforward of inventory (goods held on consignment in, inventory pledged as loan collateral, a lost purchase discount) | Analysis |
| `far-inventory-rollforward-0007` | II.C.c (abnormal spoilage, goods in a customs bonded warehouse, an unbilled volume rebate) | Analysis |
| `far-ppe-rollforward-0006` | II.D.f Prepare a rollforward of PP&E (sales tax/delivery capitalized, a land-improvements reclass with no net effect, shipping insurance wrongly capitalized) | Analysis |
| `far-intangibles-cloud-computing-0002` | II.F.c Calculate the carrying amount of purchased software and cloud computing arrangements | Application |
| `far-exit-costs-0003` | II.G.c Calculate exit or disposal liabilities and their timing | Application |
| `far-bonds-premium-0002` | II.H.1c Calculate interest expense on notes and bonds (bonds issued with detachable warrants) | Application |
| `far-debt-covenant-0003` | II.H.2a Perform debt covenant calculations (interest coverage) | Application |

- **Batch mix:** by skill, 0 / 4 / 9 (0% / 31% / 69%); by area, all Area II (100%). The batch is a
  deliberately Analysis-heavy, single-area slice; it is meant to be merged with batches 16-17 (which cover
  Area III and more of the Application mix) before the lead recomputes the bank-wide skill and area mix.
- **Variants:** 39. Items plus variants: 52.
- **Version-0 key letters:** B 6, C 7 (A and D don't land on version 0 this slice, by chance of where each
  key falls after ascending sort; both letters do appear once the variants are included). All versions:
  A 3, B 20, C 24, D 5.
- **Coverage:** `python scripts/far-coverage.py` reports all 113 FAR blueprint tasks at two or more items
  (347 FAR MCQs) once this batch's mapping lines are added to `scripts/far-coverage.py` alongside it.

## Process

Built from scratch against `docs/content-pipeline.md` and `scripts/batches/far-batch-13.py`'s structure
(one builder per family, parameter set 0 is the reviewed item, sets 1-3 its variants, a 4-distractor pool
per family with a different three shown per version so the key's letter moves, Decimal ROUND_HALF_UP
arithmetic throughout). Before drafting, read every existing item on each target task so this batch's
items change at least two component events from each one and avoid the "subledger totals $X, general
ledger shows $Y; the controller finds" opener (and "controller finds"/"controller investigates" generally)
that recurs across the existing cash, receivables, inventory and PP&E items and that batch 13's gate
flagged for reuse within a task.

Two self-inflicted near-duplicates surfaced on the first `audit()` run and were fixed before anything was
written: `far-intangibles-cloud-computing-0002`'s setup sentence was nearly verbatim from
`far-intangibles-cloud-computing-0001` ("has no right to take possession... reasonably certain to
exercise its option to renew the contract for 2 more years. Before the software became ready..."); it was
rewritten in different words and the renewal/go-live parameters were changed off the matching values. The
two new receivables-rollforward items then shared a 14-word run with each other (the colon-list rollforward
preamble and the closing question, both lifted from the same older template); `far-receivables-rollforward
-0007` was rewritten as prose with a different closing question. `audit()` and the deterministic lint
(`scripts/batches/lint.py`, run with the tag-versus-task check live once this batch's ids were mapped in
`scripts/far-coverage.py`) both return zero warnings on these ids; the only prints are informational
`NOTE ... [key_in_stem]` lines, where a scenario fact that needs no adjustment happens to equal the key
(`cash-unreconciled-0004`, `-0005`, `exit-costs-0003`), which the quality bar treats as a prompt to look,
not a defect. `npx tsx scripts/content.ts validate` passes (393 reviewed files).

Judgment calls:
- `far-debt-covenant-0003` asks for an interest-coverage ratio (net income plus interest and taxes, as the
  loan agreement defines it, excluding an asset-sale gain and adding back a restructuring charge) rather
  than reusing either existing debt-covenant item's leverage or funded-debt/EBITDA ratio.
- `far-bonds-premium-0002` adds a relative-fair-value allocation between bonds and detachable warrants
  (ASC 470-20-25) before the effective-interest computation, so the item tests a judgment
  (`far-bonds-premium-0001` and `far-debt-noninterest-note-0001` don't) in addition to the arithmetic.
- `far-exit-costs-0003` uses termination benefits that don't require future service (recognized in full at
  the communication date under ASC 420-10-25-4), the opposite condition from both existing exit-cost items,
  which require staying until closure; a contract-termination fee and a relocation cost, both not yet
  recognized at year-end, are distractor bait.
- `far-ppe-rollforward-0006` and `far-cash-bank-reconciliation-0007` each include one fact that requires no
  dollar adjustment (an intra-PP&E reclassification; a check mailed before year-end that stays outstanding
  however long it takes to clear) as a distractor rather than a reconciling item, to test whether the
  student knows when *not* to adjust.
- `far-intangibles-cloud-computing-0002` asks for the net capitalized implementation asset rather than
  total Year 1 expense (what both existing items in this task ask for), so amortization over the
  term-plus-renewal period is itself a tested step; it cites ASU 2025-06 and notes the result for a pure
  hosting arrangement is unchanged, matching `far-intangibles-cloud-computing-0001`'s citation.

## Blind verification

TODO: run `docs/prompts/blind-verifier.md` against
`C:\Users\harms\AppData\Local\Temp\claude\opencpa-gate\b15\b15-blind.md` (52 versions, stems and lettered
choices only) and reconcile against `b15-keys.json` in the same directory.

## Review gate

TODO: this batch is all Analysis or Analysis-adjacent in scope and sits on tasks new to a two-item state
(II.A.b/A.c/B.c/C.c/D.f already had 4-5 items, but every new item here changes component events, so by the
stratified policy every one of the 9 Analysis items is gated in full). Of the 4 Application items,
`far-intangibles-cloud-computing-0002` (ASU 2018-15/2025-06) and `far-bonds-premium-0002` (ASC 470-20
warrants, a template new to the bank) should also run in full; `far-exit-costs-0003` and
`far-debt-covenant-0003` are candidates for the one-in-three Application sample once combined with
batches 16-17's Application items.
