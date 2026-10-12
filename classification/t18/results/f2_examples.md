# F2: the §8.4 attribution table against the recorded failures (manual, after the recorded run on f77ab8f)

Sources: each task's RESULTS/REPORT check table and diagnosis; the Appendix D render (Tasks 1–17).

| §8.4 row | Example in the draft | Task's recorded failure | Attribution in the task's report | Real failure, right task? | Note |
|---|---|---|---|---|---|
| Criterion | peak positions to 3 figures from a 0.4 % grid (T6) | T6 C5 peak locations to 3 s.f. | criterion | yes | — |
| Criterion | the limits at β ≥ 2 (T11.3) | T11.3 classes (two routes) | criterion | yes | — |
| Criterion | a zero tolerance too coarse for the prior's dip (T12) | T12 A7 minimum below F and two rays | criterion | yes | — |
| Code | SymPy cannot denest √(x²) or decide some signs (T10) | T10.1 symbolic (2 items) | **criterion / route** | yes | the report attributes it to the criterion and the pre-registered route, not to code |
| Code | … (T13) | T13 Part A symbolic (2 of 68) | **criterion / route** | yes | as above |
| Code | … (T16) | T16 D1 (2 of 9 items) | code | yes | — |
| Code | `sympy.limit` on the D2 coefficient (T12) | T12 symbolic A5 | code | yes | — |
| Code | double precision at a cancellation (T9.5) | T9.5 monotonicity and ordering | **criterion** (float64 resolution) | yes | the report attributes it to the criterion |
| Code | … (T13) | T13 A2 numerical (277 sets) | code (precision loss) | yes | — |
| Document | a class (1, 0, 1) stated for sums of Bayesian stages that cannot occur (T13) | T13 C2 row 8 | document | yes | — |
| Document | four truncated worked values (T13) | T13 C1 first run: "4 document: 0.0099504 truncated" | document (4), code (2) | yes | four **occurrences** of one truncated value (0.0099504 for 0.0099505), not four different values |
| Document | in the thesis draft, an incomplete proof, a miscounted number of test values, a mislabelled range and a sentence that claimed more than its source (T17) | T17 E1 (item 6), E3, E4, E5 | E1 code / document; E3, E4, E5 document | yes | — |
| Input | two bibliography entries attached to no result, and DOIs unreachable (T14) | T14 C9 | input / criterion | yes | — |
| Prediction | the quick-check values in the Task 12 prompt (T12) | T12 A8 qualitative regression | prediction | yes | — |

**Every example is a real failure of the named task.** Three examples sit in the "Code" row although their reports attribute them
to the criterion (T10.1, T13 Part A symbolic: "criterion / route"; T9.5: "criterion"). §8.4's own words for that row ("the checking
route could not do the computation") describe them fairly, but the attribution differs from the record.

**Every Appendix D failure maps to a listed attribution.** 28 failure bullets (Tasks 6, 9–17); each names criterion, code,
document, input or prediction, or "route" / "plan's construction (criterion as pre-registered)", which the reports place under the
criterion. The recorded automatic mapper missed four lines that end without " — " (diagnosis, `t18_diag.json`); all four name
"criterion" or "document … code".

**Counts.** Recorded parser: 143 checks with a verdict, 28 failed, Tasks 4 and 5 without criteria. The one-check difference is
Task 2's T2.1c, whose verdict cell reads "PASS (info)": the recorded parser required the cell to equal "PASS". Read as the
pre-registered rule says ("says PASS or FAIL"), the total is 144 (`t18_diag.json`). T2.1c is labelled informational; the draft's
144 counts it.
