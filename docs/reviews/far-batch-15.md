# Review report: FAR batch 15

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**13 items**, all written from scratch in `scripts/batches/far-batch-15.py`, all Area II (Select Balance
Sheet Accounts) and all numeric with three variants each (39 variants), so the batch adds 52 problems.
Every variant family moves the key's letter. Built as one slice of batches 15-17 (45 Application and
Analysis items closing the skill-mix gap batch 14 left: Remembering and Understanding over its 15% cap
until these land); the other slices cover different tasks and ids.

**Status: revision 2, written as `status: draft`.** The first version failed both the blind verifier and
the review gate (47.4% average, 8 major items, 4 wrong keys). Revision 2 rebuilds eight items and revises
the other five (details under "Review gate" below). The builder now writes `status: draft`, so none of the
13 items is served until the blind verifier and the gate pass again; switch `STATUS` in the builder to
`"reviewed"` then. None of these ids was ever served, so the ids are kept even where an item was rebuilt.

## Plan

Nine Analysis items spread across six Area II Analysis tasks, preferring the tasks with the fewest
existing items, each changing at least two of the scenario's component events against every existing item
on its task and using a stem format none of them uses. Four Application items on four of the twelve
eligible Area II Application tasks, chosen to spread across different accounts: cloud computing
(ASU 2018-15/2025-06), exit-cost timing, bond interest with detachable warrants, and a debt covenant.

The table shows revision 2.

| Item | Blueprint task | What it tests (revision 2) | Skill |
| --- | --- | --- | --- |
| `far-cash-bank-reconciliation-0006` | II.A.b Reconcile the bank balance to the general ledger | Note collected (principal plus interest), card-processor fee, a stopped check that is still on the outstanding list *and* still recorded as a disbursement | Analysis |
| `far-cash-bank-reconciliation-0007` | II.A.b | Bank error (another customer's deposit), uncredited interest, an unrecorded automatic payment, a postdated customer check counted in deposits in transit and in book cash | Analysis |
| `far-cash-unreconciled-0004` | II.A.c Investigate unreconciled cash balances to determine an adjustment | Asks for the cash shortage left after correcting both sides: a deposit double-counted as in transit (bank side), a misdirected wire and a duplicate petty-cash check (book side) | Analysis |
| `far-cash-unreconciled-0005` | II.A.c | Asks how much, and in which direction, the general ledger is misstated: a bank encoding error on a check (bank side), auto-debited insurance, a deposit entered in the disbursements journal, a counterfeit bill (book side) | Analysis |
| `far-receivables-rollforward-0006` | II.B.c Prepare a rollforward of trade receivables | Control-account postings: a transfer of receivables that fails ASC 860-10-40-5(b) (secured borrowing), a bill-and-hold invoice that isn't a receivable, showroom cash sales posted through AR (no net effect) | Analysis |
| `far-receivables-rollforward-0007` | II.B.c | Customer credit balances netted in the subledger total, a late-entered December return, a recovery that never touched AR | Analysis |
| `far-inventory-rollforward-0006` | II.C.c Prepare a rollforward of inventory | Asks for corrected purchases: consigned-in goods entered as purchases, net-method discounts lost charged to purchases, an unrecorded December purchase return, in-transit FOB shipping point goods correctly included | Analysis |
| `far-inventory-rollforward-0007` | II.C.c | Asks for the net adjustment to the perpetual balance: worthless damaged stock, an unrecorded purchase in a bonded warehouse, a volume rebate split between goods on hand and goods sold (ASC 705-20) | Analysis |
| `far-ppe-rollforward-0006` | II.D.f Prepare a rollforward of PP&E | Asks for corrected additions: an overweight-load fine and post-installation insurance wrongly capitalized, transit insurance wrongly expensed, a new parking lot posted to buildings (no effect on the total) | Analysis |
| `far-intangibles-cloud-computing-0002` | II.F.c Calculate the carrying amount of purchased software and cloud computing arrangements | Two modules going live on different dates, each amortized over the hosting term remaining at its own go-live; a renewal management hasn't decided on; process redesign expensed | Application |
| `far-exit-costs-0003` | II.G.c Calculate exit or disposal liabilities and their timing | Severance needing no further service (full accrual), stay bonuses (ratable), a contract fee not yet triggered by notice, employee relocation (as incurred) | Application |
| `far-bonds-premium-0002` | II.H.1c Calculate interest expense on notes and bonds | Bonds with detachable warrants issued April 1: relative-fair-value allocation, effective rate on the allocated amount, one full period plus a year-end accrual. The item is now a discount item; the id keeps "premium" because ids are never renamed | Application |
| `far-debt-covenant-0003` | II.H.2a Perform debt covenant calculations | Asks how far defined EBIT could fall before breaching an interest-coverage covenant; an impairment loss on assets still in use is not a loss on a sale | Application |

- **Batch mix (unchanged by the revision):** by skill, 0 / 4 / 9 (0% / 31% / 69%); by area, all Area II
  (100%). The batch is a deliberately Analysis-heavy, single-area slice, meant to be merged with batches
  16-17 before the lead recomputes the bank-wide skill and area mix.
- **Topic tally:** cash 4 (2 reconciliations, 2 unreconciled differences), rollforwards 5 (receivables 2,
  inventory 2, PP&E 1), cloud computing 1, exit costs 1, bonds 1, debt covenant 1.
- **Variants:** 39. Items plus variants: 52.
- **Key letters (revision 2):** version 0: B 7, C 6. All versions: A 3, B 22, C 25, D 2.
- **Coverage:** `python3 scripts/far-coverage.py` reports all 113 FAR blueprint tasks at two or more items.

## Process

Built from scratch against `docs/content-pipeline.md` (one builder per family, parameter set 0 is the
item and sets 1-3 its variants, a 4-5 distractor pool per family with a different three shown per version
so the key's letter moves, Decimal ROUND_HALF_UP arithmetic throughout).

Revision 2 checks, all run 2026-10-05:
- `audit()` (including the deterministic lint): 0 warnings. `python3 scripts/batches/lint.py` reports no
  finding on any batch 15 id or on `far-intangibles-cloud-computing-0001`.
- `python3 scripts/far-coverage.py` passes; `pnpm content:validate` passes.
- The builder now asserts that no company name or short name repeats within the batch, and that no short
  name is a stray fragment ("St", "Indian", "Bugle"); multi-word places carry an explicit short name
  (`s="St Keverne"`).
- Independent re-solve: a separate script parses the facts out of each written stem (it does not import
  the builder) and recomputes the key for all 52 versions, plus the 4 versions of cloud-computing-0001.
  For the two bank reconciliations it solves the bank side and the book side separately; for the bond item
  it also checks that the stated effective rate amortizes the allocated carrying amount to face at
  maturity. 64 checks, 0 mismatches.

## Blind verification

First run (revision 1): one blind verifier, stems and choices only. It agreed with the key on 6 items
(bank-reconciliation-0006 and -0007, unreconciled-0004 and -0005, debt-covenant-0003, exit-costs-0003,
cloud-computing-0002, receivables-rollforward-0007) and raised defects on the rest:

| Item | Verifier's finding | Required fix |
| --- | --- | --- |
| bonds-premium-0002 | Facts contradict each other: 7.4% doesn't price the bonds at the stated $950,000, and 7.4% isn't the effective rate on the $907,250 allocated amount (6.26% is). The correct answer, about $56,919, isn't offered. Two variant distractors match no error. | Make the rate consistent with the allocated amount; replace the unexplained distractors. |
| inventory-rollforward-0006 | Wrong key: under the net method, discounts lost are expensed, not added back to inventory. v3 doesn't offer the correct answer. The stem never says whether the consigned goods were recorded as purchases. "St" short name. | Drop or rework the discount fact; state how the consigned goods were recorded. |
| inventory-rollforward-0007 | Two defensible answers: the stem doesn't say whether the bonded-warehouse purchase was recorded. Also missing that the rebated goods are still on hand (ASC 705-20). | State both facts. |
| ppe-rollforward-0006 | v3 doesn't offer the correct answer ($2,706,000); "resurface" reads as a repair. | Add the correct answer; say "pave a new parking lot". |
| receivables-rollforward-0006 | Recourse alone doesn't make the transfer a borrowing (ASC 860-10-40-5), so the sale answer is defensible; the rebate sentence reads two ways. "St" short name. | Add a fact that defeats a sale condition; rewrite the rebate. |
| cash-unreconciled-0004, -0005 | Giveaway: the key equals the adjusted bank balance stated in the stem. 0005 prints "$-1,400" and uses "St". | Add a bank-side error or change the ask; fix format and name. |
| cash-bank-reconciliation-0006 | "The bank statement also lists deposits in transit" is wrong: a bank statement can't list them. | Reword. |

Its report also covered `far-ratios-0008`, `far-comprehensive-income-0005` and
`far-investments-amortized-cost-0002` (batch 14 revisions); those belong to batch 14 and aren't part of
this revision.

Second run (revision 2): pending. Input: `b15r/b15-blind.md` in the session's gate scratch folder (52
versions, stems and lettered choices only; keys in `b15r/b15-keys.json`), plus `b15r/cloud-0001-blind.md`
for the four versions of `far-intangibles-cloud-computing-0001`, whose key this revision changes.

## Review gate

First run (revision 1): a fresh review agent gated all 13 items in full and checked all 39 variants.
**Average estimated pass likelihood 47.4%** (batch 14: 86.3%). Verdicts: 0 exam-ready, 5 minor, 8 major.
Four keys were wrong and two items depended on an unstated fact. The batch failed.

| Item | Gate verdict (pass likelihood) | Finding | Fix in revision 2 |
| --- | --- | --- | --- |
| bonds-premium-0002 | Major (15%), wrong key | Scenario contradicts itself; effective rate not consistent with the allocated amount; two implausible distractors; "premium" id on a discount item. | **Rebuilt.** The stem no longer quotes a market yield. It gives both fair values and the proceeds, and states the effective rate measured on the bonds' share of the proceeds; the builder derives the proceeds from that rate, asserts the allocated amount equals the present value at that rate within $1, and asserts it amortizes to face within $10. Proceeds sit 2% below the two fair values combined. New events: April 1 issue with a year-end accrual (one full period plus 3 months), so the format differs from bonds-premium-0001. Distractors: total proceeds as carrying amount, bonds' own fair value as carrying amount, stated interest only, no year-end accrual. The swapped-allocation distractor is gone. Id kept (never served); it is now a discount item. |
| cash-bank-reconciliation-0006 | Minor (70%) | The bank side alone gave the key; "bank statement lists deposits in transit". | The stopped check is now on the bookkeeper's outstanding list as well as in the disbursements, so both sides need a judgment. The note now has principal and interest (new single-error distractor), and amounts were enlarged so no distractor sits within a few dollars of the key. "The bookkeeper's reconciliation lists deposits in transit..." |
| cash-bank-reconciliation-0007 | Minor (62%) | The book side alone gave the key; weak "remove the uncashed check" distractor; a variant distractor came from no error. | Added a postdated customer check counted in both deposits in transit and book cash, and an unrecorded automatic payment, so each side needs a judgment. Dropped the stale-check fact and its distractor, and the "corrects neither" distractor. Every distractor is now one error. |
| cash-unreconciled-0004 | Major (45%), giveaway | Key equals the stated adjusted bank balance. | **Rebuilt.** New ask (the cash shortage left after correcting both sides) and a bank-side error (a deposit already on the statement counted again as in transit). Events changed from 0001-0003: the shortage write-off and the double-counted deposit are new. |
| cash-unreconciled-0005 | Major (40%), giveaway | Same giveaway; every sign in the explanation equation reversed; a rationale that described no computation; "$-1,400"; "St". | **Rebuilt.** New ask (size and direction of the ledger's misstatement, choices such as "$1,250 understated" and "$240 overstated") and a bank-side error (a check encoded at the wrong amount). The explanation chains true arithmetic on both sides. Company renamed St Keverne Marine Co. |
| debt-covenant-0003 | Minor (76%) | One-step; the threshold was decoration; repeated company names. | New ask: how far defined EBIT could fall before breaching, so the threshold drives the answer. Added an impairment loss on a line still in use, which the "sales of long-lived assets" exclusion doesn't cover (a classification judgment). |
| exit-costs-0003 | Minor (80%) | Explanation misstated the contract-termination rule; events overlapped exit-costs-0002; variants used a two-error distractor. | Explanation now cites ASC 420-10-25-11 correctly (recognized when terminated under the contract's terms, here by written notice not yet sent). Events changed: a call center, a cleaning contract not yet terminated, stay bonuses recognized ratably, and employee (not equipment) relocation. Every distractor is a single error. |
| intangibles-cloud-computing-0002 | Major (30%), wrong key | Amortized six years from go-live, past the arrangement's end (should be the remaining term); near-duplicate of cloud-computing-0001; wrong reasoning in a rationale. | **Rebuilt.** Two modules go live on different dates; each is amortized from its own ready-for-use date over the term remaining then. The renewal is one management hasn't decided on, so it is excluded. Business-process redesign replaces 0001's cost categories. Distractors: full term from go-live, amortizing from the contract start, both modules from the first go-live, including the renewal, capitalizing the redesign. |
| inventory-rollforward-0006 | Major (15%), wrong key | Net-method discounts lost are not inventory; template shared with 0005 and 0007. | **Rebuilt.** New ask (corrected purchases). The discount fact is now a genuine error (discounts lost charged to purchases); consigned goods are stated to have been entered as purchases; added an unrecorded December purchase return and an in-transit FOB shipping point purchase that is correctly included (distractor). |
| inventory-rollforward-0007 | Major (45%) | Missing facts (was the bonded-warehouse purchase recorded; are rebated goods on hand); wrong citations; "billed" a rebate. | **Rebuilt.** New ask (net adjustment to the perpetual balance, increase or decrease). The stem says the bonded-warehouse purchase wasn't recorded; the rebate is allocated, with the share on goods on hand given (new distractor: taking the whole rebate out of inventory); "issued the credit memo"; cites ASC 705-20 and ASC 330-10-35. |
| ppe-rollforward-0006 | Major (15%), wrong key | Transit insurance is capitalized, not expensed; "resurfacing" reads as a repair; v3 lacked the correct answer; template same as ppe-rollforward-0004. | **Rebuilt.** New ask (corrected additions). Transit insurance now appears as an error the other way (expensed, should be capitalized); added an overweight-load fine and post-installation insurance, both wrongly capitalized; the parking lot is a new lot "where there was none before". |
| receivables-rollforward-0006 | Major (45%) | Recourse alone doesn't decide sale accounting; ambiguous rebate; template matched receivables-rollforward-0005. | **Rebuilt.** New format (control-account postings). The agreement forbids the bank from selling or pledging the accounts, which fails ASC 860-10-40-5(b). The bill-and-hold invoice is payable 30 days after delivery, so there is no unconditional right to payment either. The rebate is replaced by showroom cash sales posted through both sides of AR (no net effect, a distractor). |
| receivables-rollforward-0007 | Minor (78%) | "Netted ... rather than reported separately" stated the error; unclear whether cash collected included the recovery. | The stem now gives the subledger's debit and credit balance totals, says the preliminary figure agrees with their net, and says the cash collected figure excludes the recovery. |

Batch-level findings also applied: every short-name truncation ("St", "Indian", "Bugle") and every repeated
company name (Wadebridge, Bodmin, Padstow, Mevagissey, and Delabole, which also appeared in an existing
item) is gone, and the builder now enforces this.

**Related live item, `far-intangibles-cloud-computing-0001` (Lark).** The gate's remaining-term point
applies to it too: its key amortized $180,000 over five years from July 1, which runs six months past the
arrangement's December 31, Year 5 end. It was fixed in its builder (`scripts/batches/far-variants-09.py`,
`cloud_costs`, with the base text mirrored in `scripts/batches/far-batch-01.py`): amortization is now over
the 54 months remaining at go-live. Keys changed: v0 $93,000 to $95,000, v1 $151,000 to $153,273, v2
$75,000 to $76,667, v3 $125,000 to $127,000. The old key ($93,000) is now version 0's central-twist
distractor ("a full five years from July 1"), and the stem adds "running from that date". This item is
live and reviewed, so its changed key needs the blind verifier before commit.

Gate findings not applied as suggested, and why:
- Bonds: the gate offered "make the stand-alone bond fair value equal the PV at the quoted yield". The stem
  no longer quotes a yield at all. Under relative-fair-value allocation the effective rate on the bonds'
  share always exceeds the bonds' own market yield when the proceeds are below the two fair values
  combined, so quoting both invites the same contradiction. Stating only the effective rate on the
  allocated amount is consistent and still makes the allocation the tested step.
- Bonds: the gate suggested renaming the id. Ids are kept (the task instructions, and none was served);
  the "premium" id now holds a discount item, noted in the plan table.
- Receivables-0006: the gate suggested replacing the rebate with "cash sales posted to the AR collections
  line" as an error. The revision uses cash sales posted to both sides of AR, which has no net effect, as a
  trap with its own distractor; the item already has two errors that change the key.
- PP&E-0006: the gate suggested dropping the transit-insurance fact. It is kept, reversed, because the
  correct treatment (capitalize) is worth testing, and genuine period costs (a fine, insurance after
  installation) were added beside it.

Suggested additions to the quality bar from the gate (section 4 of its report) are for the lead to decide;
the shared docs and scripts weren't edited in this revision.
