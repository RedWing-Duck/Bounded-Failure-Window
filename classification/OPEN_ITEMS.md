# Open items at the end of the cycle (Tasks 1–18)

Everything not settled when Task 18 closed, with its status and where it is recorded. An item is marked **resolved** only when a
pre-registered check in Tasks 1–18 resolved it; a post-hoc diagnosis, however convincing, leaves it **diagnosed, not re-checked**.

## 1. The conjecture and the open problems

| Item | Status | Recorded in |
|---|---|---|
| Conjecture 6.22: sampled relays D1–D3 have at most two turning points along Δt in every metric | **open** (no proof; no counterexample in Task 12's census, 6,000 sets × 3 metrics, or Task 13's audit) | register 6.22 (status conjecture); `source/Stages_0_4_Source.md` §11 item 1; draft §9.4(1) |
| Proposition 6.20 assumes C2 for D1's prior and avg curves (finitely many turning points), which Conjecture 6.22 would give | **conditional** on an unproved hypothesis | Proposition 6.20's statement; Task 13 C4 referee point 7 |
| Open problem: a bound on turning points of two-stage sums | **open** (at most 3 and 4 observed in 2,000 sets each) | source §11 item 2; draft §9.4(2); Numerical result 5.15 |
| Open problem: a necessary condition for monotone optimal error beyond the power family | **open** | source §11 item 3; draft §9.4(3) |
| Open problem: the fixed α–β filter and multivariate models (mixing case) | **open** | source §11 item 4; draft §9.4(4) |
| Open problem: a gain that tracks correlation time | **open**; in the draft only, not in the repository's §11 | draft §9.4(5); RESULTS_t18 F4 |
| Open problem: applications | **open**; in the draft only, not in the repository's §11 | draft §9.4(6), §1.7; RESULTS_t18 F4 |

## 2. Numerical results: evidence, not proof

| Item | Status | Recorded in |
|---|---|---|
| Numerical result 5.15 (two-stage gains: (max, min, max) in 7 of 2,000; (min, max, min, max) in 63 of 2,000) | numerical | register 5.15; T10.3, T13 C2 rows 8–9 |
| Numerical result 6.21 (census of sampled relays; class lists per family and metric) | numerical | register 6.21; T12 A8, Part C; T13 C2 rows 24–32 |
| Class lists of the sampled relays (synthesis-matrix rows 24–32): excess sets and limits proved, full class sets not | numerical | draft §8.5; `register/matrix.csv` |
| Numerical result 8.1 (blind searches: 10⁶ and 4.4 × 10⁶ classifications; Task 13 audit) | numerical | register 8.1; T10.7, T12 Part C, T13 C2 |
| Numerical result 8.2 (windows of relative width 10⁻⁸ need root-finding) | numerical | register 8.2; T10.5 |

## 3. Citations not settled

| Item | Status | Recorded in |
|---|---|---|
| [26] Saho & Masugi 2016, cited (§6.3) for the variance factor α/(2 − α) of an exponentially weighted average | **undetermined**: full text unreachable; summaries show α–β–γ trackers with acceleration measurements, no α/(2 − α). Candidate replacements: Roberts 1959 (doi:10.1080/00401706.1959.10489860), Kalata 1984. Author's decision | T17 E5 (S1); `t18/results/a5_sources.md` |
| [29] Jazwinski 1970, cited (§7.4) for the prediction covariance of a delayed estimate | **undetermined**: contents show Chapter 7 "Linear Filtering Theory" with a continuous–discrete filter section; the delayed-state statement not confirmed. Candidates: Anderson & Moore 1979; Gelb 1974. Author's decision | T17 E5 (S12); `t18/results/a5_sources.md` |
| [21] still cited, as "[21–23]", for monotonicity under garbling in §1.6 (fixed in §7.1, not in §1.6) | **open** (document) | RESULTS_t18 F1 |
| [28] dated 1968 in the bib (journal version); the search found the 1967 Harvard report of the same work | noted, not an error | RESULTS_t17, For the author 5.7 |

## 4. External review

| Item | Status | Recorded in |
|---|---|---|
| No result has had review outside the project | **open** | draft §8.5 |
| One independent referee pass inside the project (a separate agent) over the whole Stages 0–4 consolidated document, 14 points, all fixed; Theorem 7.6 among the results read | done (Task 13 C4); the draft's §8.5 describes it as a pass on Theorem 7.6 only | `t13/referee_report.md`; RESULTS_t13 C4; RESULTS_t18 F3 |

## 5. Rough-draft text

| Item | Status | Recorded in |
|---|---|---|
| Chapter 8 (Verification) | **rough draft**; checked in Task 18 F2–F3: counts match post hoc (144, 28, Tasks 4 and 5); §8.4's "Code" row holds three failures the reports attribute to the criterion; §8.4's "four truncated worked values" are four occurrences of one value; §8.5's referee sentence does not match the record | draft §8; RESULTS_t18 |
| Chapter 9 (Discussion and Limits) | **rough draft**; checked in Task 18 F4: every claim sourced and matching; the "same form" window claim holds for the listed families (not the Hill gain); open problems 5–6 are new relative to the repository | draft §9; RESULTS_t18 |
| Draft's Theorem 2.2 proof (now in the thesis render) omits the closing sentences the Task 13 referee added to the repository's proof (the rule at an interior critical tolerance; approach directions determined by the sequence) | **open** (document; the paper render keeps the repository's proof) | RESULTS_t18, For the author 6 |

## 6. Checks that failed and were not resolved by a later check

Each failure below is recorded with its diagnosis in its task's report and in Appendix D. "Diagnosed" means the report attributes
it and, where relevant, shows the claim holds; no later pre-registered check re-ran it.

| Task | Failure | Attribution | Status |
|---|---|---|---|
| 6 | C5 peak locations to 3 s.f. | criterion | diagnosed |
| 9 | T9.2 ARE route; T9.5 monotonicity flags | criterion | diagnosed |
| 10 | T10.1 symbolic (2 items); T10.5 pair birth; T10.6 zero-limit shape | criterion / route; criterion; criterion | diagnosed |
| 10 | T10.2 A1.3 as specified | criterion (plan's construction) | **resolved** by T10.2 A1.3 supplementary (PASS) |
| 11 | T11.3 classes | criterion | diagnosed (limits corrected in the diagnosis) |
| 12 | Symbolic A5 (sympy.limit); A7 minimum below F; A8 regression | code; criterion; prediction | diagnosed |
| 13 | Part A symbolic (2 of 68); A2 numerical; C2 row 8; C2 row 12; D reproduction | criterion / route; code; document; code; code / criterion | diagnosed (row 8 led to Proposition 5.14, proved in Task 13) |
| 13 | C1 numbers, first run | document, code | **resolved** by C1 after the fixes (PASS) |
| 14 | C4 paper render reproduces v1 | criterion | diagnosed (accepted in Task 15) |
| 14 | C9 bibliography | input / criterion | **resolved** by T15 C1 (PASS) |
| 14 | C10 reproduction dry-run resolver | code | diagnosed |
| 15 | C4 [n] rendering | criterion / code | **resolved** by T16 D7 (PASS) |
| 15 | C10 phrase check | criterion | **resolved** by T17 E7 (PASS), after T16 D6 failed |
| 16 | D1 items 2(b), 9 | code | diagnosed (both hold post hoc) |
| 16 | D2 statements | document / criterion | 2.5 and 2.7: **resolved** by T17 E2 (PASS); 3.1 and 3.5: diagnosed (thesis-only imports in Task 17, not re-compared) |
| 16 | D6 legacy labels | criterion / document | **resolved** by T17 E7 (PASS) |
| 17 | E1 item 3 (P⁻ < F at 50 digits) | code | **resolved** by T18 F1 (identity and adaptive-precision test) |
| 17 | E1 item 6 (Corollary 7.4's proof) | document | **resolved** by T18 F1 |
| 17 | E3 β count | document | **resolved** by T18 F1 (draft); repository label corrected in Task 18 Part B |
| 17 | E4 range label | document | **resolved** by T18 F1 |
| 17 | E5 [47] in §7.3 | document | diagnosed: the corrected sentences say "model error" (T18 F1 post hoc); the recorded F1 sub-check failed on scope |
| 18 | F1 (the [47] scope; [21] in §1.6) | code; document | [47]: diagnosed; [21]: **open** |
| 18 | F2 counts | code | diagnosed (144 with T2.1c's "PASS (info)") |
| 18 | F3 §8.5 referee sentence | document | **open** |
| 18 | F6 appendices | code (Appendix A, math delimiters); document (Appendix D's Task 17 entry reworded in the draft) | Appendix A: diagnosed; Appendix D wording: **open** |
