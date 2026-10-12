# Open items at the end of Task 19

Everything not settled when Task 19 closed, with its status and where it is recorded. An item is marked **resolved** only when a
pre-registered check in Tasks 1–19 resolved it; a post-hoc diagnosis, however convincing, leaves it **diagnosed, not re-checked**.

## 1. The conjecture and the open problems

| Item | Status | Recorded in |
|---|---|---|
| Conjecture 6.22: sampled relays D1–D3 have at most two turning points along Δt in every metric | **open** (no proof; no counterexample in Task 12's census, 6,000 sets × 3 metrics, Task 13's audit, or Task 19's D1 scan, 41 × 41 dimensionless grid). Task 19 Part E reduced D1 to two parameters (g = G/λ, ν = 2ΠΣ/λ²) and proved the parity of the number of turning points (post and prior odd iff G > 2FΠ; avg odd iff g² + 4g > 4ν); "at most two" is not proved, D2 and D3 not studied | register 6.22 (status conjecture); source §11 item 1; draft §9.4(1); RESULTS_t19 Part E |
| Proposition 6.20 assumes C2 for D1's prior and avg curves (finitely many turning points), which Conjecture 6.22 would give | **conditional** on an unproved hypothesis (its conclusion was re-checked on 907 sets in T19 H-12.A7, prior half) | Proposition 6.20's statement; Task 13 C4 referee point 7 |
| Open problem: a bound on turning points of two-stage sums | **open** (at most 3 and 4 observed in 2,000 sets each) | source §11 item 2; draft §9.4(2); Numerical result 5.15 |
| Open problem: a necessary condition for monotone optimal error beyond the power family | **open** | source §11 item 3; draft §9.4(3) |
| Open problem: the fixed α–β filter and multivariate models (coupled case) | **open** | source §11 item 4; draft §9.4(4) |
| Open problem: a gain that tracks correlation time | **open**; now in the repository's §11 (Task 19 Part A.3, documentation fix) | source §11 item 5; draft §9.4(5) |
| Open problem: applications | **open**; now in the repository's §11 (Task 19 Part A.3) | source §11 item 6; draft §9.4(6), §1.7 |

## 2. Numerical results: evidence, not proof

| Item | Status | Recorded in |
|---|---|---|
| Numerical result 5.15 (two-stage gains: (max, min, max) in 7 of 2,000; (min, max, min, max) in 63 of 2,000) | numerical | register 5.15; T10.3, T13 C2 rows 8–9 |
| Numerical result 6.21 (census of sampled relays; class lists per family and metric) | numerical | register 6.21; T12 A8, Part C; T13 C2 rows 24–32 |
| Class lists of the sampled relays (synthesis-matrix rows 24–32): excess sets and limits proved, full class sets not | numerical | draft §8.5; `register/matrix.csv` |
| Numerical result 8.1 (blind searches: 10⁶ and 4.4 × 10⁶ classifications; Task 13 audit) | numerical | register 8.1; T10.7, T12 Part C, T13 C2 |
| Numerical result 8.2 (windows of relative width 10⁻⁸ need root-finding) | numerical | register 8.2; T10.5; T19 G4 |

## 3. Citations

| Item | Status | Recorded in |
|---|---|---|
| [26], now Roberts 1959 (Task 19 Part A.1, replacing Saho & Masugi 2016), cited for the variance factor α/(2 − α) | **undetermined**: Roberts's text unreachable from the session; secondary sources credit him with λ/(2 − λ). The §6.3 identity itself holds (T19 G1) | T19 G1 (FAIL, input); `t19/results/g1_citations.md` |
| [29] Jazwinski 1970 and [40] Anderson & Moore 1979 for the §7.4 prediction step | **resolved** at contents scope by T19 G1 (the equation itself not seen in either text) | T19 G1; `g1_citations.md` |
| [21] in §1.6 and §7.1 (observation channels as design variables) | **resolved** by T19 G1 (consistent with the abstract) | T19 G1, H-18.F1-21 |
| [47] in §6.2 and §7.3 (mis-specified time-correlated model error in Kalman smoothing) | **resolved** by T19 H-17.E5 (consistent with the title and abstract) | `t19/results/h17e5_sources.md` |
| [28] dated 1968 in the bib (journal version); the search found the 1967 Harvard report of the same work | noted, not an error | RESULTS_t17, For the author 5.7 |
| The old key `sahomasugi2016` in ten recorded files of Tasks 14, 15 and 17 and in `t19/t19_register.py`'s docstring | **stays** (recorded artifacts are not edited); 0 in live files | T19 G7 (FAIL, criterion / code) |

## 4. External review

| Item | Status | Recorded in |
|---|---|---|
| No result has had review outside the project | **open** | draft §8.5 |
| One independent referee pass inside the project (a separate agent) over the whole Stages 0–4 consolidated document, 14 points, all fixed | done (Task 13 C4); the draft's §8.5 now describes it correctly (**resolved** by T19 G3 / H-18.F3) | `t13/referee_report.md`; RESULTS_t13 C4 |

## 5. Text of chapters 8–9

| Item | Status | Recorded in |
|---|---|---|
| Chapter 8 (Verification) | **open** (document; G3 failed): counts 151 / 32 and §8.5 match the record; §8.2 interchanges the descriptions of route (i) and route (ii); §8.4 lists Task 13 under "no handling of √(x²)", which Task 13's report does not support; the paragraph after §8.4's table omits T16 D2, T16 D6 and T18 F6 from "the other document failures" | RESULTS_t19 G3; `t19/results/g3_examples.md` |
| Chapter 9 (Discussion and Limits) | **open** (document; G4 failed): 21 of 22 claims match; §9.2's Hill condition c/(FΠ₀) > 4 holds for n = 2 only | RESULTS_t19 G4; `t19/results/g4_claims.md` |
| Theorem 2.2's proof in the thesis render | **resolved**: the draft now carries the Task 13 referee's closing sentences (kind (a), and 10,000 random cases, T19 G2); the thesis render imports it (G7) | RESULTS_t19 G2, G7 |

## 6. Checks that failed and were not resolved by a later check

Each failure is recorded with its diagnosis in its task's report and in Appendix D.

| Task | Failure | Attribution | Status |
|---|---|---|---|
| 6 | C5 peak locations to 3 s.f. | criterion | **resolved** by T19 H-6.C5 |
| 9 | T9.2 ARE route; T9.5 monotonicity flags | criterion | **resolved** by T19 H-9.2, H-9.5 |
| 10 | T10.1 symbolic (2 items); T10.5 pair birth; T10.6 zero-limit shape | criterion / route; criterion; criterion | **resolved** by T19 H-10.1a, H-10.1b, H-10.5, H-10.6 |
| 10 | T10.2 A1.3 as specified | criterion (plan's construction) | **resolved** by T10.2 A1.3 supplementary (PASS) |
| 11 | T11.3 classes | criterion | **resolved** by T19 H-11.3 |
| 12 | Symbolic A5; A7 minimum below F; A8 regression | code; criterion; prediction | **resolved** by T19 H-12.A5, H-12.A7, H-12.A8 |
| 13 | Part A symbolic (2 of 68); A2 numerical; D reproduction | criterion / route; code; code / criterion | **resolved** by T19 H-13.A-sym, H-13.A2, H-13.D |
| 13 | C2 row 8 | document | corrected in Task 13 (Proposition 5.14, proved) |
| 13 | C2 row 12 | code | **not resolved**: T19 H-13.C2-12 failed (criterion: its 10⁻³⁰⁰ tolerance is finer than the stored limit's precision, about 10⁻²⁵); the class at the exact limit is All by Theorem 2.2(2) |
| 13 | C1 numbers, first run | document, code | **resolved** by C1 after the fixes (PASS) |
| 14 | C4 paper render reproduces v1 | criterion | **resolved** by T19 H-14.C4 |
| 14 | C9 bibliography | input / criterion | **resolved** by T15 C1 (PASS) |
| 14 | C10 reproduction dry-run resolver | code | **resolved** by T15 C13 (PASS; listed as diagnosed in Task 18's inventory) and T19 H-14.C10 |
| 15 | C4 [n] rendering | criterion / code | **resolved** by T16 D7 (PASS) |
| 15 | C10 phrase check | criterion | **resolved** by T17 E7 (PASS) |
| 16 | D1 items 2(b), 9 | code | **resolved** by T19 H-16.D1 |
| 16 | D2 statements | document / criterion | 2.5 and 2.7: **resolved** by T17 E2; 3.1 and 3.5: **resolved** by T19 H-16.D2 |
| 16 | D6 legacy labels | criterion / document | **resolved** by T17 E7 (PASS) |
| 17 | E1 items 3 and 6; E3; E4 | code; document | **resolved** by T18 F1 |
| 17 | E5 [47] in §7.3 | document | **resolved** by T19 H-17.E5 |
| 18 | F1 ([47] scope; [21] in §1.6) | code; document | **resolved** by T19 H-17.E5 and G1 (H-18.F1-21) |
| 18 | F2 counts | code | **resolved** by T19 G3 recount (H-18.F2) |
| 18 | F3 §8.5 referee sentence | document | **resolved** by T19 G3 (H-18.F3) |
| 18 | F6 appendices | code; document | **resolved** by T19 G6 (H-18.F6) |
| 19 | G1 citations ([26] undetermined) | input | open (§3) |
| 19 | G3 chapter 8 | code; document | open (§5) |
| 19 | G4 chapter 9 (Hill condition) | document | open (§5) |
| 19 | G7 old key in recorded files | criterion; code | stays (§3) |
| 19 | H-13.C2-12 | criterion | open (row 13 C2 above) |

## 7. Recount through Task 19

| Task | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Checks with a verdict | 12 | 3 | 8 | 0 | 0 | 6 | 15 | 5 | 7 | 10 | 11 | 13 | 15 | 11 | 13 | 8 | 7 | 7 | 31 | 182 |
| Failed | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 4 | 1 | 3 | 5 | 3 | 2 | 3 | 4 | 4 | 5 | 37 |

Tasks without pass criteria: 4 and 5. Failures by attribution over the 38 failure lines of Appendix D, each kind a line names counted
once ("route" and "plan's construction" as criterion): criterion 19, code 14, document 13, input 2, prediction 1.
