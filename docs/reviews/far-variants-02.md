# FAR variants 02

**Standard:** AICPA *Uniform CPA Examination Blueprints*, effective January 2026.

**What this adds:** 36 variants, three for each of 12 numeric items from FAR batches 03 and 04. With the item itself, each question now has four versions.

## Method

`scripts/batches/far-variants-02.py` uses the same method as variants 01:

- a builder writes each question from parameters;
- parameter set 0 must rebuild the reviewed item word for word, and all 12 did;
- `audit()` checks every version.

**New in this batch: distractor pools.** Variants 01 kept the same three errors in every version. Because choices are sorted in ascending order, the key landed on the same letter in 12 of 13 families. Here each family has four or five distractors, each tied to a named student error, and each version shows a different three. The script refuses to write a family if the key has the same letter in all four versions.

| Item | Area | Key letters by version | New distractor errors |
| --- | --- | --- | --- |
| `far-performance-metrics-0001` | I | D C D C | preferred dividends included in the payout ratio |
| `far-cash-flows-0006` | I | B B C A | dividends received left out; gain on the sale added |
| `far-income-statement-0003` | I | B A C B | tax netted against the write-down only; write-down reported alone |
| `far-balance-sheet-0003` | I | C B D C | noncontrolling interest deducted from equity |
| `far-receivables-rollforward-0001` | II | C B D C | change in receivables reversed |
| `far-inventory-rollforward-0001` | II | B C B C | freight-in subtracted |
| `far-ppe-rollforward-0001` | II | A A C B | depreciation expense used as accumulated depreciation removed |
| `far-exit-costs-0001` | II | B A C A | the post-year-end months recognized instead |
| `far-ppe-impairment-0002` | II | C B D C | building's excess split equally between the machines |
| `far-ppe-interest-capitalization-0001` | II | C A B C | total (not weighted) expenditures; all interest incurred |
| `far-nfp-agent-transfers-0001` | III | A B A B | the gift with variance power left out |
| `far-revenue-licenses-0001` | III | A B A B | software license spread over the support term |

Where the numbers allowed, versions also change direction, not just size. One rollforward variant has a gain on disposal instead of a loss, and two receivables variants have balances that fall instead of rise.

## Blind verification

One verifier agent solved all 36 variants from the stems and choices only:

- It matched the key on all 36, with high confidence.
- It found no second defensible answer, no arithmetic error and no renumbering that changes which rule applies.
- It could name the error behind every distractor.
- It confirmed that the checks the builders assert held in every version:
  - service periods are longer than notice periods (exit costs);
  - the building's loss cap binds (group impairment);
  - capitalized interest stays below interest incurred (interest capitalization).

| Finding | Fix |
| --- | --- |
| Required: "a eight-year license" (revenue licenses, variant 3) | The builder now chooses "a" or "an". |
| Optional: "dividends on an equity investment" could be misread as equity-method dividends, which can be a return *of* investment (investing). No choice matched that reading. | Now reads "dividends on an investment in equity securities", in the reviewed item (`far-batch-04.py`) and in every version. |
| Optional: the "depreciation expense used as accumulated depreciation removed" distractor is the least intuitive error in the PP&E rollforward pool. | Kept. It is nameable, and its rationale says what the student did. |
