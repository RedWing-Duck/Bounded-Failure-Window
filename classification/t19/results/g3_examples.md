# G3 (B3): chapter 8 readings (manual, after the recorded run)

## §8.4 table: each example against the named task's report

| Row | Example | Task's recorded failure and attribution | Real and correctly labelled? |
|---|---|---|---|
| Criterion | peak positions to 3 figures from a 0.4% grid (T6) | T6 C5, criterion (`verification/REPORT.md`) | yes |
| Criterion | limits at β ≥ 2 (T11.3) | T11.3 classes, criterion (pre-registered limits/brackets) | yes |
| Criterion | a zero tolerance too coarse for the prior's dip (T12) | T12 A7, criterion | yes |
| Criterion | SymPy routes with no handling of √(x²) (T10, T13) | T10.1, criterion/route: "no √(square) handling" — yes. T13 Part A symbolic, criterion/route: "The sign of −sFr … is not decided by SymPy's assumptions because 1 − e^{−2x} is not known positive; the A2 identity with sinh is not reduced" — no square root is involved | **T10 yes; T13 no** (T13's route failures were an undecided sign and an unrewritten sinh, not √(x²); the draft follows RESULTS_t16's parenthetical "the cause of the Task 10 and Task 13 route failures too", which T13's own report does not support) |
| Criterion | double-precision flags (T9.5) | T9.5, criterion (float64 resolution) | yes |
| Code | SymPy could not decide a sign or denest √(x²) (T16) | T16 D1, code | yes |
| Code | a sample point below its equality tolerance (T13) | T13 C2 row 12, code | yes |
| Code | a dry-run path resolver (T14) | T14 C10, code | yes |
| Code | `sympy.limit` on the D2 coefficient (T12) | T12 symbolic A5, code | yes |
| Code | precision loss at a cancellation (T13, T17) | T13 A2 numerical, code; T17 E1 item 3 (50-digit test of M < F), code | yes |
| Document | a class (1, 0, 1) stated for sums of Bayesian stages, which cannot occur (T13) | T13 C2 row 8, document | yes |
| Document | a truncated worked value, in four places (T13) | T13 C1 first run: "4 document: 0.0099504 truncated" (one value, four occurrences) | yes |
| Document | an incomplete proof, a miscounted number of test values, a mislabelled range and a sentence that claimed more than its source (T17) | T17 E1 item 6 (Corollary 7.4's proof), E3 (β count), E4 (range label), E5 ([47] sentence), all document | yes |
| Input | two bibliography entries attached to no result, and DOIs unreachable from the session (T14) | T14 C9, input / criterion | yes |
| Prediction | the quick-check values in the Task 12 prompt (T12) | T12 A8, prediction | yes |

**§8.4 examples: one mismatch** (the T13 half of the √(x²) example). Attribution: document.

Outside the pre-registered sub-criteria (reported, not part of the verdict): the paragraph after the table lists "the other document
failures" as T13's truncated value, T17's four, and T18's §1.6 citation range and §8.5 referee description. Appendix D records three
further failures with a document attribution that the paragraph omits: T16 D2 (document / criterion), T16 D6 (criterion / document)
and T18 F6 (code / document, the Appendix D rewording).

## Coverage of Appendix D failures (Tasks 1–18)

The recorded run parsed 33 failure lines and flagged 2 as uncovered: "T10.2 A1.3 as specified: plan's construction (criterion as
pre-registered); …" and "C1 numbers, first run: document (4, …) and code (2, parser); …". Both carry attributions in the five
kinds (plan's construction = criterion; document and code). The parser looked for the attribution between ": " and " —", and these
two lines use parentheses instead (attribution: **code**). Read as pre-registered, every failure is covered.

## §8.2

- "There was one persistent disagreement between the routes, row 12 of the Task 13 audit (§4.1), and the fault was in route (ii): a
  sample point fell below its equality tolerance at an exact limit." The recorded scan of every results JSON finds one persisting
  count, `t13_audit_classes.json` row 12 (122 cases), attributed in RESULTS_t13 to route (ii)'s sample point. **Matches.**
- "Route (i) finds every crossing of R² by root-finding on the monotone pieces between turning points, using the critical values of
  Theorem 2.2. Route (ii) samples the curve and reads off its components, with an equality tolerance at the critical values." In
  `t10/classify.py` (and PREREG_t10, "route (i) Theorem 1.2 on the turning-point sequence; route (ii) direct root-finding"), route (i)
  applies the Theorem 2.2 rule to the turning-point values with no root-finding, and route (ii) is the root-finding route (roots of
  f − R² on each monotone piece, then sign tests at points between the roots, with the equality tolerance). **Does not match**: the
  descriptions are interchanged in their main mechanism (root-finding belongs to route (ii)). The sentence "Every classification in
  this thesis therefore rests on route (i)" inherits the error. Attribution: document.

## §8.5

"One independent referee pass was made inside the project: a separate agent read the whole consolidated Stages 0–4 document and
raised 14 points, all of which were fixed (Task 13)." `t13/referee_report.md`: a separate agent given only
`Stages_0_4_Consolidated.md`; 14 numbered points; RESULTS_t13 C4 "14 points, all valid, all fixed". Every other referee mention in the
repository refers to this pass. **Matches.** (Task 18's pre-registration disclosure called it "twelve numbered points"; the report
has 14.)

## Recount

151 checks with a verdict and 32 failures for Tasks 1–18, Tasks 4 and 5 without criteria; the only qualified verdict is T2.1c
"PASS (info)". **Matches.**

**G3 verdict: FAIL** (coverage sub-part: code; §8.4 T13 example and §8.2 route descriptions: document). H-18.F2 (recount) and H-18.F3
(§8.5) pass.
