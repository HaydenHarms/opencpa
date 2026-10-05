# Jev pilot report: `typesafe.jsonl`

295 successful calls (0 error rows skipped); 391,442 input / 217,321 output tokens; mean latency 0.15s.

## Check: giveaway

Positives: 11 flawed 'before' items. AUC vs fixed versions 0.60, vs controls 0.76; paired: before scored higher than its own fix in 5/9 pairs (2 ties).

| threshold | catch (95% CI) | false alarm on fixed versions | false alarm on controls |
|---|---|---|---|
| p(yes) >= 0.3 | 100% (11/11; 74-100) | 100% (9/9; 70-100) | 100% (60/60; 94-100) |
| p(yes) >= 0.5 | 100% (11/11; 74-100) | 100% (9/9; 70-100) | 98% (59/60; 91-100) |
| p(yes) >= 0.7 | 82% (9/11; 52-95) | 89% (8/9; 56-98) | 63% (38/60; 51-74) |
| p(yes) >= 0.9 | 18% (2/11; 5-48) | 11% (1/9; 2-44) | 7% (4/60; 3-16) |

## Check: form_cue

Positives: 7 flawed 'before' items. AUC vs fixed versions 0.72, vs controls 0.95; paired: before scored higher than its own fix in 5/7 pairs (0 ties).

| threshold | catch (95% CI) | false alarm on fixed versions | false alarm on controls |
|---|---|---|---|
| p(yes) >= 0.3 | 100% (7/7; 65-100) | 100% (7/7; 65-100) | 30% (18/60; 20-43) |
| p(yes) >= 0.5 | 71% (5/7; 36-92) | 43% (3/7; 16-75) | 3% (2/60; 1-11) |
| p(yes) >= 0.7 | 0% (0/7; 0-35) | 0% (0/7; 0-35) | 0% (0/60; 0-6) |
| p(yes) >= 0.9 | 0% (0/7; 0-35) | 0% (0/7; 0-35) | 0% (0/60; 0-6) |

## Check: ambiguity

Positives: 5 flawed 'before' items. AUC vs fixed versions 0.44, vs controls 0.44; paired: before scored higher than its own fix in 2/5 pairs (0 ties).

| threshold | catch (95% CI) | false alarm on fixed versions | false alarm on controls |
|---|---|---|---|
| p(yes) >= 0.3 | 0% (0/5; 0-43) | 20% (1/5; 4-62) | 33% (20/60; 23-46) |
| p(yes) >= 0.5 | 0% (0/5; 0-43) | 0% (0/5; 0-43) | 0% (0/60; 0-6) |
| p(yes) >= 0.7 | 0% (0/5; 0-43) | 0% (0/5; 0-43) | 0% (0/60; 0-6) |
| p(yes) >= 0.9 | 0% (0/5; 0-43) | 0% (0/5; 0-43) | 0% (0/60; 0-6) |

## Combined screen (any of giveaway / form_cue / ambiguity)

Positives: 22 flawed items carrying at least one of those defects. 'Cleared' = no check fired, i.e. the item could skip the review agent.

| threshold | catch | controls cleared | fixed versions cleared | unlabelled 'before' items flagged |
|---|---|---|---|---|
| 0.3 | 100% (22/22; 85-100) | 0% (0/60; 0-6) | 0% (0/20; 0-16) | 100% (34/34; 90-100) |
| 0.5 | 100% (22/22; 85-100) | 2% (1/60; 0-9) | 0% (0/20; 0-16) | 100% (34/34; 90-100) |
| 0.7 | 86% (19/22; 67-95) | 37% (22/60; 26-49) | 10% (2/20; 3-30) | 74% (25/34; 57-85) |
| 0.9 | 9% (2/22; 3-28) | 93% (56/60; 84-97) | 90% (18/20; 70-97) | 18% (6/34; 8-34) |

## Skill level (Score)

Agreement with the assigned tag on fixed versions and controls: 84% (108/128; 77-90).
Disagreement with the wrong tag on flawed 'before' items (what the gate retagged): 43% (3/7; 16-75).

| tag | agreement |
|---|---|
| Analysis | 72% (26/36; 56-84) |
| Application | 93% (69/74; 85-97) |
| Remembering and Understanding | 72% (13/18; 49-88) |

## Blueprint task mapping (FAR, 113 options)

Top-1 agreement with the coverage map: 74% (70/95; 64-81); same blueprint area: 98% (93/95; 93-99).
The map is Claude-made, not ground truth, so a disagreement can be Jev being right; see the list below.

| confidence >= | items covered | agreement among covered |
|---|---|---|
| 0.5 | 86% (82/95; 78-92) | 82% (67/82; 72-89) |
| 0.7 | 74% (70/95; 64-81) | 89% (62/70; 79-94) |
| 0.9 | 58% (55/95; 48-67) | 93% (51/55; 83-97) |

Disagreements at confidence >= 0.7 (check by hand):

- `far-ratios-0002` (after): map says I.F.c, Jev says I.F.e (0.93)
- `far-investments-equity-securities-0001` (after): map says II.E.1d, Jev says II.E.1b (0.70)
- `far-payables-cutoff-0001` (after): map says II.G.d, Jev says II.G.b (0.98)
- `far-contingencies-0003` (control): map says III.B.c, Jev says III.B.b (0.71)
- `far-ppe-rollforward-0001` (control): map says II.D.f, Jev says II.D.b (0.97)
- `far-income-taxes-nol-0001` (control): map says III.D.c, Jev says III.D.d (0.85)
- `far-intangibles-impairment-0001` (control): map says II.F.b, Jev says II.D.c (0.97)
- `far-contingencies-0002` (control): map says III.B.c, Jev says III.B.b (0.78)