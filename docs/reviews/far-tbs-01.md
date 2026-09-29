# Review report: FAR simulations batch 01

**3 simulations**, written from scratch (`scripts/batches/far-tbs-01.py`), with numeric and journal-entry tasks only. Research tasks wait until cited paragraphs can be checked against the Codification (see `docs/plans/tbs-frontend.md`).

| Simulation | Blueprint task | Skill | Tasks |
| --- | --- | --- | --- |
| `far-tbs-lessee-finance-0001` | III.F Calculate lessee assets and liabilities and prepare journal entries | Application | 2 journal entries, 2 numeric (6 points) |
| `far-tbs-bank-reconciliation-0001` | II.A Reconcile the bank balance to the general ledger | Analysis | 1 numeric, 1 compound journal entry (4 points) |
| `far-tbs-income-tax-provision-0001` | III.D Calculate income tax expense and prepare the provision entry | Application | 2 numeric, 1 journal entry (5 points) |

Every amount is computed in the script with `Decimal`, rounded half up, and stored in cents. The script asserts that the bank and book sides of the reconciliation agree.

**End-to-end test:** on a local worker, `GET /simulations` returned the three simulations with no answer, tolerance or explanation fields, and a fully correct submission of the tax provision scored 5 of 5.

## Blind verification

A separate agent solved every task from the scenario, exhibits, prompts and account lists only. All answers matched. Fixes applied:

| Simulation | Finding | Fix |
| --- | --- | --- |
| Income tax provision (required) | ASC 740 lets deferred tax assets and liabilities of the same jurisdiction be offset, so a netted entry would be marked wrong by the exact-match grader; deferred expense and the DTA were both $6,300 | Prompt says to record the DTA and DTL separately; warranty accrual changed to $40,000 so the amounts differ (DTA $8,400, deferred expense $4,200) |
| Bank reconciliation (required) | A split cash debit and credit is a correct entry the grader would reject; check #884 did not say it paid an account payable | Prompt asks for the net change in Cash as one line; exhibit says the check paid an account payable |
| Finance lease | A candidate might fold amortization into the payment entry | Prompt says to record only the payment |

The verifier read the bank reconciliation as Application; it stays Analysis because it maps to the FAR task "Reconcile the cash balance per the bank statement to the general ledger," which the blueprint marks Analysis.

**Still to do:** the review gate on these three, and Hayden's review of the player UI (branch `tbs-ui`, not yet merged).
