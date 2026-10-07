# Review report: FAR simulations batch 01

**Standard:** AICPA _Uniform CPA Examination Blueprints_, effective January 2026.

**3 simulations**, written from scratch (`scripts/batches/far-tbs-01.py`), with numeric and journal-entry tasks only. Research tasks wait until cited paragraphs can be checked against the Codification (see `docs/plans/tbs-frontend.md`).

## Current version (revision 2)

| Simulation                          | Blueprint task                                                                     | Skill       | Tasks                                   |
| ----------------------------------- | ---------------------------------------------------------------------------------- | ----------- | --------------------------------------- |
| `far-tbs-lessee-accounting-0001`    | III.F Calculate lessee assets and liabilities and prepare journal entries          | Application | 2 journal entries, 4 numeric (9 points) |
| `far-tbs-bank-reconciliation-0002`  | II.A Reconcile the cash balance per the bank statement to the general ledger       | Analysis    | 3 numeric, 1 journal entry (6 points)   |
| `far-tbs-income-tax-provision-0002` | III.D Calculate income tax expense and deferred taxes; prepare the provision entry | Application | 5 numeric, 1 journal entry (8 points)   |

Revision 2 replaced the three revision-1 simulations with new ones under new ids, because student progress is keyed to the id:

- **Lessee.** A six-year lease with a purchase option that Ridge is reasonably certain to exercise. The candidate has to judge the classification from the facts, include the option price in the liability, and amortize over the nine-year economic life. The exhibits include data to reject: fair value, an 8% bank quote, the 9-period and annuity-due factors, and third-party maintenance.
- **Bank reconciliation.** It's now built from source documents: the May reconciliation, the June bank statement, the June cash journals and three supporting documents. The candidate finds the deposits in transit, the outstanding checks (including a May check still outstanding), a bank error and a book error.
- **Income tax provision.** Year 2 with opening deferred balances and an enacted rate change. It adds unearned rent (a deferred tax asset), a nondeductible fine, estimated payments recorded as prepaid taxes, net presentation of the deferred balances, and two irrelevant items (a taxable gain and dividends).

Every amount is computed in the script with `Decimal`, rounded half up, and stored in cents. The script asserts that the bank and book sides of the reconciliation agree. Currency tasks accept ±$1, and every scenario says how to round.

**Grader change (in the same commit).** `gradeJournalEntry` now nets each account to one signed amount before matching, in both the key and the response. A correct entry scores the same whether it is split, gross or combined. The schema requires one line per account in each key.

## Review gate

| Run        | Average pass likelihood | Verdicts | Outcome                                                                                                                                                                                                       |
| ---------- | ----------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Revision 1 | 69% (66 / 68 / 74)      | 3 minor  | Failed the ~80% bar. No key was wrong. The grader rejected correct entries, the exhibits did the candidate's sorting, and the bank reconciliation reused the template of `far-cash-bank-reconciliation-0001`. |
| Revision 2 | 79.7% (76 / 79 / 84)    | 3 minor  | All 17 keys matched. The reviewer confirmed from the blueprint PDF that the bank reconciliation task is marked Analysis. It found two required fixes and expected about 84% with them applied.                |

Fixes applied after the revision 2 gate:

| Simulation        | Finding                                                                                                                                                                   | Fix                                                                                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lessee (required) | The task wording ("record only the payment; amortization separately", "amortization expense on the right-of-use asset") told the candidate the lease was a finance lease. | Task 2 now asks for the December 31 entries "for the lease payment and any related amortization or expense", with Lease expense kept as the operating-lease trap. Task 3 asks for the right-of-use asset's carrying amount. |
| Lessee            | Task 6 (total lease cost) was the sum of two other tasks, so one error cost two points.                                                                                   | Replaced with the financing cash outflow for the lease. The scenario states that Ridge reports initial direct costs as investing.                                                                                           |
| Lessee            | A private company could elect a risk-free discount rate.                                                                                                                  | The scenario says Ridge is a public business entity.                                                                                                                                                                        |
| Bank (required)   | "Correct cash balance" could include the $300 petty cash fund.                                                                                                            | Now asks for the adjusted balance of the checking account.                                                                                                                                                                  |
| Bank              | The scenario said the bank had confirmed its error.                                                                                                                       | Removed. Exhibit 4 (the deposit slip, the supplier's invoice and the customer's remittance advice) now carries the evidence.                                                                                                |
| Tax               | "Taxable income far above its future deductions" all but stated the valuation-allowance conclusion.                                                                       | Replaced with projected pretax income of about $700,000 a year.                                                                                                                                                             |
| Tax               | A candidate booking one net deferred movement would lose most of the entry.                                                                                               | The prompt says Keane keeps separate deferred tax asset and liability accounts.                                                                                                                                             |

## Blind verification

- **Revision 1:** all answers matched. The entry-structure findings that led to the grader change are recorded in git history.
- **Revision 2:** all 16 answers matched. Its required fixes were applied before the gate:
  - Task 6 now says "lease cost, as ASC 842 defines it".
  - The tax entry now says to apply the estimated payments.
  - The simulations got new ids, so that `lessee-finance` no longer shows in the URL.
- **Revision 2 after the gate fixes:** all 16 tasks were re-solved blind and every answer matched, with no required fixes. The bank statement running balances, the book rollforward and Exhibit 4 all tie.

## Still to do

- Hayden's review of the player UI.
- **A `select` (dropdown) task type.** Real simulations use many classification cells, such as lease type, permanent or temporary difference, and which side of the reconciliation an item belongs on. Without them, authors drift toward prompts that leak the classification.
- **Next simulation batch** (about seven more to reach ten):
  - It needs an Area I simulation first: cash flows, a wholly owned consolidation worksheet, or finding and correcting errors in a draft statement.
  - Then bonds with a partial retirement, contingencies and subsequent events from a legal letter, a receivables reconciliation with expected credit losses, and a multi-element revenue contract.
  - At least four of them should be Analysis.
