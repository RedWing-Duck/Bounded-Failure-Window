# Task 13 — finalize Stages 0–4: results

Pre-registration `classification/PREREG_t13.md`, commit **296a797**; code and results commit **d683915**. Python 3.13.16, mpmath 1.3.0, SymPy 1.14.0, 4 CPUs.

| Check | Verdict | Counts / worst errors | Runtime (s) |
|---|---|---|---|
| Part A symbolic (A1, A2, A4, A5, A7, A8) | **FAIL** | 66/68 items; failing: 2 product of the roots -sFr < 0 (so f' > 0 at the positive root); 6 (1 - x s'/s)(2/s) - 1 - 2 e^{-2x}(sinh 2x - 2x)/s^2 == 0. Diagnosis: both identities verified by a rewrite route (yes) | 6 |
| A-reg: Tasks 8–12 symbolic regression | **PASS** | 178/178 items; T8 35/35, T9 27/27, T10 26/26, T11 23/23, T12 67/67; documented fallbacks used 3 | 39 |
| A1 numerical (10,000 sets, 100 digits) | **PASS** | failures 0; min dM/dx 1.41e-46 |  |
| A2 numerical (same sets) | **FAIL** | failures {'Pbar(mu) = Pbar(M)': 277} (auxiliary cross-check only; diagnosis: 0 remain at higher precision, pre-registered links 0 failures) |  |
| A3 numerical (10,000 sets, 100 digits) | **PASS** | violations 0; min dP_a/dx 1.36e-18, min dP_b/dx 3.89e-14 |  |
| A3 symbolic attempt (pre-registered script) | unresolved | automated verdict 'unresolved' (float leak; coefficient-sign rule only) |  |
| A3 exact completion of the resultant route | **PASS** | 22 checks |  |
| A3 closed form (referee point 5) | **PASS** | a0 = -a1; p = 2/(1 + sqrt(1 + 2u/k)), k = (1+u) x coth(x/2) - 2u increasing |  |
| A4 numerical (10,000 curves, 0 < β < 2) | **PASS** | turning points {'max': 10000}; max Φ_τ residual 5.88e-28; Φ_ττ closed vs direct 0 | 1648 |
| A5 regression + 5,000 Hill sets (real n) | **PASS** | Π0_pair: n = 1.5: 30.2430947474 (rel 9.03e-13), n = 2: 31.4750497595 (rel 1.25e-12), n = 3: 37.8200022316 (rel 8.2e-13), n = 4: 44.1796834278 (rel 4.07e-13), n = 8: 62.7113145769 (rel 5.09e-13); mismatches 0 of 5000 (pair predicted in 2469) | 3222 |
| A7 numerical (10,000 sets, 60 digits) | **PASS** | failures 0; min (V − P)/P 8.29e-16 | 15 |
| C1 numbers, first run | **FAIL** | failing entries 6 (4 document: 0.0099504 truncated; 2 code: parser) |  |
| C1 numbers, after the fixes | **PASS** | 198 literals; 81 registry entries (42 formulas); 117 identifiers; unmatched 0 |  |
| C2 classes (42 rows × 1,000 sets × 100 tolerances) | **FAIL** | rows passing 40/42; classifications 4,200,000; flagged 1037; persisting 122 | 13624 |
| C3 references and labels | **PASS** | 73 results, 158 references, 0 errors |  |
| C4 independent referee | record | 14 points, all valid, all fixed (dispositions below) |  |
| D reproduction (Tasks 8–12 reports) | **FAIL** | T8: identical; T9: identical; T11: identical; T12: 1 issues; not reproduced: ['10'] |  |

**Pre-registered checks that FAIL:** Part A symbolic (A1, A2, A4, A5, A7, A8); A2 numerical (same sets); C1 numbers, first run; C2 classes (42 rows × 1,000 sets × 100 tolerances); D reproduction (Tasks 8–12 reports). Each is diagnosed below.

## Part A outcomes

| Item | Outcome | New label (consolidated document) |
|---|---|---|
| A1 Prop. 2.6(b), optimal M-P prior increasing | **proved** (verified: every step symbolic, 10,000 sets with 0 failures) | Theorem 32(b) |
| A2 Num. 2.6c, optimal M-P time average increasing | **proved** (new route via $P^+ = F/(1+\mu)$; final bound $\sinh 2x \ge 2x$) | Theorem 32(c) |
| A3 Num. 2.8 / 4.10a, integrate-and-dump monotone | **proved** (exact resultant route completed post hoc; closed form $p = 2/(1 + \sqrt{1 + 2u/k(x)})$ found in response to the referee) | Theorem 35 |
| A4 Num. 4.6a, power family unimodal for $0 < \beta < 2$ | **proved** (every critical point is a strict maximum: $\Phi_{\tau\tau} = P^2(\beta + (2-\beta)\lambda^2\tau^2)/\tau^3$) | Theorem 25 |
| A5 Conj. 3.10, Hill gain every $n > 1$ | **proved** for every real $n > 1$ (Descartes on a cubic with signs $+, ?, -, -$) | Theorem 56 |
| A6 Conj. 2.11, sampled relays at most two turning points | **unresolved** (no route; evidence below) | Conjecture 38 |
| A7 Num. 3.5 (Stage 2), strict gap $P < V$ | **proved** (orthogonality fails through the $e^{-u/\tau}$ term; compactness) | Proposition 20 |
| A8 Conj. 4.11, non-linear causal garblings | **proved** for additive stationary Gaussian noise (fixed-lag limit + frequency localization; referee found no gap) | Theorem 69 |

A6 evidence (C2 rows 24–32, 9,000 new curves): maximum number of turning points per row dt D1 post: 1, dt D1 prior: 2, dt D1 avg: 2, dt D2 post: 2, dt D2 prior: 1, dt D2 avg: 1, dt D3 post: 1, dt D3 prior: 2, dt D3 avg: 1; Task 12: 6,000 sets × 3 metrics, never more than two.

## Plain statements

- **Did any result in Stages 0–4 change?** No theorem or proposition was overturned; one matrix class list was corrected (row 8, below). Labels changed where Part A proved something (six items became theorems or propositions; A1 verified). The audit and the referee found document errors that are now corrected and logged: a truncated worked value (0.0099504 → 0.0099505), D2's unstated requirement $c < 2$ (with $c = 3$ the excess set is all of $(0,\infty)$, not a lower ray), the condition column of rows 25–26 ("two rays iff $G > 2F\Pi$" is only "if"), missing equality rows (optimal prior/avg at $R^2 = \sigma_\star^2$; capped gain at $g = 2F$), and several missing hypotheses (C2 in Proposition 36, continuity in Corollary 66, windows in Corollary 59). One class list changed: the C2 audit of row 8 (two-stage Bayesian) never observed the stated $(1,0,1)$, and the post-hoc diagnosis proved it impossible (Theorem 6 addendum: for increasing $G$ with $G/\Pi$ strictly decreasing, every interior minimum exceeds $F$); row 8's set is corrected (change log row 45). The pre-registered C2 verdict for row 8 stays FAIL.
- **Did any class outside the stated sets appear?** No out-of-set class appeared in 4,200,000 classifications. Two rows failed the pre-registered rule for other reasons (diagnoses 7–8): row 8 (Pi bayes2): out of set [], missing ['(1, 0, 1)'], persisting 0; row 12 (Pi0 monotone): out of set [], missing [], persisting 122
- **What remains open?** Conjecture 38 (sampled relays have at most two turning points), Numerical result 58 (two-stage gains), a necessary condition for monotone optimal error beyond the power family, and Stage 6 (α–β, multivariate). Consolidated Section 11 states each with its evidence.

## Diagnoses and fixes

1. **Part A symbolic, two route failures (attribution: criterion/route).** The sign of $-sFr$ (A1 item 2) is not decided by SymPy's assumptions because $1 - e^{-2x}$ is not known positive; the A2 identity with $\sinh$ is not reduced by the pre-registered routes. Both reduce to 0 after `rewrite(exp)` / an explicit positive series (`t13_partA_symbolic_diag.py`).
2. **Code bug (fixed before the recorded run of the symbolic script).** A2 item 4 had a sign typo ($-E\cdot G$ for $+E\cdot G$) contradicting the pre-registered identity; fixed, then the script was re-run (66/68).
3. **A2 numerical (attribution: code).** The auxiliary cross-check $\bar P(\mu) = \bar P(M)$ to 1e-80 (not a pre-registered link) failed in 277 sets, all at $\lambda\Delta t \ge 26.6$, because $F - M$ cancels about $2x/\ln 10$ digits. With $100 + 2x/\ln 10 + 30$ digits all agree to 3.93e-133 (`t13_partA_numeric_diag.py`). Every pre-registered A2 link had 0 failures.
4. **A3 (attribution: code; outcome completed post hoc).** The pre-registered attempt script leaked floats (Python integer division) and its automatic verdict only checked coefficient signs of polynomials in $(x, E, u)$, so it reported 'unresolved'. Completing the same resultant route in exact arithmetic (`t13_A3_proof.py`) shows the resultant is $4u^2x^2(u+1)^2(E-1)^4(E^2 + 2xE - 1)^2$ and $E^2 + 2xE - 1 = -2e^{-x}(\sinh x - x) < 0$ on $E = e^{-x}$, so the derivative never vanishes. The referee's request to print the quadratic then exposed $a_0 = -a_1$ and a closed form (`t13_A3_closed.py`, 11/11), which proves monotonicity and both limits directly. `t13_A3_limits.py` (a series attempt at the limits) is superseded: SymPy's limit route failed at $x \to \infty$, which the closed form settles.
5. **C1 first run (attribution: document 4, code 2).** $G^\star = \sigma_\star^2$ at $\Pi = 1$ is 0.00995049…, stated as 0.0099504 (truncated; T8.2 checked 4 s.f.); corrected to 0.0099505 everywhere (change log row 29). The parser mis-read plain `10^{12}` (code); fixed. After the referee fixes the registry was extended to the new literals (three entries) and the run repeated: PASS.
6. **compare_repro.py (code, before any recorded comparison).** A `|z|` inside a table cell shifted the runtime column, and reports not yet regenerated in the worktree were compared with themselves; fixed (last-cell masking; only tasks in the replay's runtime logs are compared).
7. **C2 row 12, Pi0 monotone (attribution: code).** 122 persisting disagreements in 23 sets, all at $R^2$ exactly $L_-$ on increasing curves whose approach to $L_-$ is exponentially flat ($\tanh$, $\exp$ shapes). With no split point, route (ii) tests one point ($P_0 = 1$), where $f - R^2$ is below its 1e-40 relative equality tolerance, so it reads Empty; at $P_0 = 10\Pi$ the gap is positive in every case, and the failure set is All, as route (i) says. No document change.
8. **C2 row 8, two-stage Bayesian (attribution: document).** $(1,0,1)$ was never observed (0 in 1,000 sets, 0 in 400,000 further screened draws). Proved impossible post hoc (Theorem 6 addendum, `t13_audit_classes_diag2.py`); row 8's stated set corrected (change log row 45). The pre-registered verdict stays FAIL.

## C2 class audit

| # | Row | Stated | Observed classes | Turning points | Flagged | Persisting | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Pi optimal | Empty, lower ray | {'Empty': 55032, 'lower ray': 44968} | {'none': 1000} | 0 | 0 | **PASS** |
| 2 | Pi bayes | All, Empty, lower ray, window | {'Empty': 26496, 'All': 26376, 'lower ray': 34375, 'window': 12753} | {'none': 578, 'max': 422} | 0 | 0 | **PASS** |
| 3 | Pi misspec | Empty, lower ray, window | {'Empty': 43703, 'lower ray': 38341, 'window': 17956} | {'none': 558, 'max': 442} | 0 | 0 | **PASS** |
| 4 | Pi capped | All, Empty, lower ray, window | {'All': 25801, 'window': 13676, 'Empty': 25867, 'lower ray': 34656} | {'max': 439, 'none': 561} | 0 | 0 | **PASS** |
| 5 | Pi blind | All, lower ray | {'All': 54821, 'lower ray': 45179} | {'none': 1000} | 0 | 0 | **PASS** |
| 6 | Pi hill2 | (1, 0, 1), All, Empty, lower ray, window | {'All': 25135, 'Empty': 25296, 'window': 12644, '(1, 0, 1)': 4722, 'lower ray': 32203} | {'min-max': 460, 'none': 540} | 10 | 0 | **PASS** |
| 7 | Pi hilln | (1, 0, 1), All, Empty, lower ray, window | {'Empty': 25105, 'All': 25042, 'lower ray': 30973, '(1, 0, 1)': 5328, 'window': 13552} | {'none': 519, 'min-max': 467, 'max': 14} | 47 | 0 | **PASS** |
| 8 | Pi bayes2 | (0, 0, 2), (1, 0, 1), All, Empty, lower ray, window | {'window': 13416, 'Empty': 23419, 'lower ray': 39871, 'All': 23209, '(0, 0, 2)': 85} | {'max': 437, 'none': 557, 'max-min-max': 6} | 0 | 0 | **FAIL** |
| 9 | Pi hill2stage | (0, 0, 2), (1, 0, 1), (1, 0, 2), All, Empty, lower ray, window | {'lower ray': 37902, 'Empty': 21806, 'All': 22372, '(1, 0, 1)': 5140, 'window': 12341, '(0, 0, 2)': 409, '(1, 0, 2)': 30} | {'min-max': 429, 'min-max-min-max': 44, 'none': 527} | 10 | 0 | **PASS** |
| 10 | Pi0 bayes | All, Empty, lower ray, two rays, upper ray | {'All': 24788, 'Empty': 26866, 'upper ray': 17835, 'two rays': 12104, 'lower ray': 18407} | {'none': 405, 'min': 595} | 0 | 0 | **PASS** |
| 11 | c bayes | All, two rays, upper ray | {'upper ray': 32734, 'All': 27282, 'two rays': 39984} | {'min': 1000} | 0 | 0 | **PASS** |
| 12 | Pi0 monotone | All, Empty, lower ray, two rays, upper ray | {'Empty': 26366, 'upper ray': 19071, 'All': 24492, 'two rays': 11837, 'lower ray': 18234} | {'min': 576, 'none': 424} | 439 | 122 | **FAIL** |
| 13 | tau ZF relay | All, Empty, lower ray | {'Empty': 30985, 'All': 31060, 'lower ray': 37955} | {'none': 1000} | 0 | 0 | **PASS** |
| 14 | tau ZF optimal | Empty, lower ray | {'Empty': 55148, 'lower ray': 44852} | {'none': 1000} | 0 | 0 | **PASS** |
| 15 | tau var relay | All, Empty, upper ray | {'upper ray': 34840, 'All': 32570, 'Empty': 32590} | {'none': 1000} | 0 | 0 | **PASS** |
| 16 | tau var optimal | Empty, window | {'Empty': 54805, 'window': 45195} | {'max': 1000} | 0 | 0 | **PASS** |
| 17 | power beta<=0 | Empty, lower ray | {'Empty': 55034, 'lower ray': 44966} | {'none': 1000} | 0 | 0 | **PASS** |
| 18 | power 0<beta<2 | Empty, window | {'window': 44982, 'Empty': 55018} | {'max': 1000} | 0 | 0 | **PASS** |
| 19 | power beta>=2 | Empty, upper ray | {'Empty': 54970, 'upper ray': 45030} | {'none': 1000} | 0 | 0 | **PASS** |
| 20 | delay | All, Empty, window | {'All': 41030, 'Empty': 31331, 'window': 27639} | {'max': 1000} | 0 | 0 | **PASS** |
| 21 | dt opt post | Empty, lower ray | {'Empty': 55022, 'lower ray': 44978} | {'none': 1000} | 0 | 0 | **PASS** |
| 22 | dt opt prior | All, Empty, upper ray | {'All': 32597, 'Empty': 32955, 'upper ray': 34448} | {'none': 1000} | 0 | 0 | **PASS** |
| 23 | dt opt avg | All, Empty, upper ray | {'All': 32414, 'Empty': 32799, 'upper ray': 34787} | {'none': 1000} | 65 | 0 | **PASS** |
| 24 | dt D1 post | Empty, lower ray, window | {'lower ray': 39820, 'Empty': 45422, 'window': 14758} | {'none': 548, 'max': 452} | 0 | 0 | **PASS** |
| 25 | dt D1 prior | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | {'lower ray': 20251, 'All': 28529, 'Empty': 28590, 'two rays': 3784, 'upper ray': 18285, '(0, 1, 1)': 561} | {'min': 178, 'none': 769, 'max-min': 53} | 151 | 0 | **PASS** |
| 26 | dt D1 avg | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | {'lower ray': 19202, 'All': 25167, 'Empty': 26233, 'two rays': 10635, 'upper ray': 18720, '(0, 1, 1)': 43} | {'min': 541, 'none': 455, 'max-min': 4} | 0 | 0 | **PASS** |
| 27 | dt D2 post | (1, 0, 1), All, Empty, lower ray, two rays, upper ray, window | {'All': 30541, 'Empty': 30926, 'upper ray': 9832, 'window': 5918, 'lower ray': 19647, 'two rays': 2779, '(1, 0, 1)': 357} | {'max': 381, 'none': 503, 'min-max': 90, 'min': 26} | 0 | 0 | **PASS** |
| 28 | dt D2 prior | All, Empty, lower ray, two rays, upper ray | {'All': 33791, 'two rays': 3411, 'Empty': 34366, 'lower ray': 7670, 'upper ray': 20762} | {'min': 177, 'none': 823} | 72 | 0 | **PASS** |
| 29 | dt D2 avg | All, Empty, lower ray, two rays, upper ray | {'Empty': 33642, 'All': 32994, 'upper ray': 21377, 'two rays': 5231, 'lower ray': 6756} | {'none': 714, 'min': 286} | 34 | 0 | **PASS** |
| 30 | dt D3 post | Empty, lower ray, window | {'lower ray': 42560, 'Empty': 49817, 'window': 7623} | {'none': 759, 'max': 241} | 0 | 0 | **PASS** |
| 31 | dt D3 prior | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | {'All': 30977, 'Empty': 30846, 'lower ray': 7943, 'two rays': 3670, 'upper ray': 25434, '(0, 1, 1)': 1130} | {'min': 129, 'none': 766, 'max-min': 105} | 85 | 0 | **PASS** |
| 32 | dt D3 avg | All, Empty, lower ray, two rays, upper ray | {'Empty': 30864, 'All': 29225, 'upper ray': 25835, 'lower ray': 6266, 'two rays': 7810} | {'none': 606, 'min': 394} | 124 | 0 | **PASS** |
| 33 | dt MI a | All, Empty, upper ray | {'Empty': 32561, 'All': 32141, 'upper ray': 35298} | {'none': 1000} | 0 | 0 | **PASS** |
| 34 | dt MI b | All, Empty, upper ray | {'All': 32332, 'upper ray': 35464, 'Empty': 32204} | {'none': 1000} | 0 | 0 | **PASS** |
| 35 | Sigma B2 abs | All, upper ray | {'upper ray': 45048, 'All': 54952} | {'none': 1000} | 0 | 0 | **PASS** |
| 36 | Sigma B2 rel | All, lower ray | {'All': 55178, 'lower ray': 44822} | {'none': 1000} | 0 | 0 | **PASS** |
| 37 | Sigma B3 abs | upper ray | {'upper ray': 100000} | {'none': 1000} | 0 | 0 | **PASS** |
| 38 | Sigma B3 rel | Empty, lower ray, window | {'window': 16814, 'Empty': 44427, 'lower ray': 38759} | {'max': 433, 'none': 567} | 0 | 0 | **PASS** |
| 39 | Sigma B4 abs | upper ray | {'upper ray': 100000} | {'none': 1000} | 0 | 0 | **PASS** |
| 40 | Sigma B4 rel | Empty, lower ray, window | {'Empty': 46072, 'window': 13392, 'lower ray': 40536} | {'max': 458, 'none': 542} | 0 | 0 | **PASS** |
| 41 | Sigma B5 abs | upper ray | {'upper ray': 100000} | {'none': 1000} | 0 | 0 | **PASS** |
| 42 | Sigma B5 rel | Empty, lower ray | {'Empty': 54781, 'lower ray': 45219} | {'none': 1000} | 0 | 0 | **PASS** |

Failing rows: row 8: missing ['(1, 0, 1)'], out of set [], persisting 0; row 12: missing [], out of set [], persisting 122. Diagnosis in `t13_audit_classes_diag.json` if present and below.

`t13_audit_classes_diag.json`: Row 12: 122 persisting cases in 23 sets; R2 exactly L- in all: True; curves monotone increasing: True; f - R2 at the single point route (ii) samples is positive but at most 2.49e-41 relative, below the 1e-40 equality tolerance, so route (ii) reads equality and returns Empty; at P0 = 10 Pi the gap is at least 0.00217 and positive in all (True). The failure set is All (route i). Attribution: code (route ii sample point). Row 8: (1, 0, 1) confirmed by both routes in 0 of the top screened sets under the pre-registered distribution (0 screen hits in 200000 draws) and in 0 with stage separation 1e6-1e12 (0 hits).

`t13_audit_classes_diag2.json`: Row 8: proved that f' < 0 wherever f <= F for any positive increasing gain with G/Pi strictly decreasing, which includes every sum of Bayesian stages; so interior minima exceed F and (1, 0, k), k >= 1, cannot occur. SymPy steps: {'(1) derivative identity': True, '(2) f <= F iff 2 Pi Sig >= lam G': True, '(3) bracket bound': True, "(4) Bayes stage Pi G' - G": True}; smallest m/F over the 6 row-8 interior minima: 1.0057874128546869. Attribution: document (row 8's stated set wrongly includes (1, 0, 1)). All checks pass: True.

## Independent referee (C4): report and dispositions

The referee was a separate agent that had not seen the derivation history. It received only
`Stages_0_4_Consolidated.md` (the draft as committed at `5ac589c`, after the C1 fix) and the instruction to report
(a) proof steps it cannot follow or believes wrong, (b) claims stronger than their proofs, (c) missing equality cases.
Its report is reproduced verbatim below, followed by my disposition of each point.

## Report (verbatim)

```
REFEREE REPORT

I read only Stages_0_4_Consolidated.md. I re-derived the algebra of each result named in the brief and spot-checked the worked examples with mpmath/sympy in scratch. These all reproduce: V(1), P(1), P(10), the misspecified-Kalman peak 17.575 and ratio 1.892, the D1 maximum 0.20457 at Δt = 2.4645, the avg dip 0.0099875 at Δt = 200, and Π0^pair for n = 1.5, 2, 3, 4. I found no error in the core proofs of Theorems 2, 25, 32(b),(c), 56 or 69, or in Propositions 9–12, 20, 41, 42 or 71. The real problems are two wrong class or condition claims (D2 and the D1-avg row), several unproved assumptions or limits, and a few equality cases.

1. [a/b] Proposition 29, plus Proposition 31's D2 row and synthesis rows 27–29. The results silently assume c < 2. For c > 2 the D2 gain L tends to c > 2, the excess test L/(2−L) > φ is no longer equivalent to P⁺ > F, and the formula for Δt_E has a negative denominator. Counterexample (λ = 1, Σ = 0.01, Π = Π0 = 1, c = 3, so κ = 300 > 2): P⁺/F = 233, 77, 12.7, 4.9 at Δt = 1, 10, 100, 1000, and post → (1−c)²F = 4F > F. The excess set is all of (0, ∞), not a lower ray. Prior and avg also tend to F from above, not from below as Proposition 31 states. From L(L(r+F) − 2F) > 0, for c > 2 the excess set is All when κ > 2, and the upper ray Δt > (2FΠ0 − c)/((c−2)FΠ) when κ < 2. Suggested fix: state 0 < c < 2 (with c ≤ 1 if under-relaxation is intended) in the D2 definition, or add the c ≥ 2 cases.

2. [a] Synthesis row 26 (D1 avg, "as row 25": 2R iff G > 2FΠ) is false in the "only if" direction. Counterexample: λ = 1, Σ = 0.01, Π = 1, G = 0.019 < 2FΠ = 0.02. avg/F is 0.999068 at Δt → 0, rises to 0.999165 near Δt = 10, falls to 0.998652 near Δt = 158, then returns to 1 from below. For R²/F in (0.998652, 0.999068) the failure set is two rays. Proposition 36 proves only the "if" direction. For row 25 (prior) the "only if" is not proved either; I found no counterexample in a quick scan. Suggested fix: say "2R if G > 2FΠ" and list the extra 2R cases as numerical (Numerical result 37).

3. [b] Theorem 6: "every R² ∈ (F, sup σ²) then gives a window". Read as class (0,0,1), this contradicts Corollary 48, which gives regular gains with k windows at R² = 1.25F. The proof only supports ℓ = u = 0 with k ≥ 1. Suggested fix: "gives a failure set of class (0,0,k), k ≥ 1 (a single window when σ² has one interior maximum, e.g. Proposition 7)".

4. [c] Section 6.2 "Optimal classes" (prior and avg), and by analogy the M-I rows 33–34. The text says "All (R² < σ*²), upper ray, …". At R² = σ*² the curve starts at σ*² and increases strictly, so it approaches from above and the class is All; the equality row is missing or implicitly wrong. Suggested fix: "All (R² ≤ σ*²), upper ray (σ*² < R² < F), Empty (R² ≥ F)", which matches the convention used in Propositions 15, 23 and 71.

5. [b] Theorem 35 and rows 33–34. The proof is not checkable from this document, which calls itself self-contained:
   - "Task 11's quadratic" (a2, a1, a0) is never written down, so the leading coefficient, the product of roots, the claim "the cleared quadratic equals its leading coefficient at p = 1" and the resultant cannot be verified.
   - The endpoint limits for M-I (σ*² as Δt → 0, F as Δt → ∞, and their approach directions) are proved nowhere; Proposition 31 covers M-P only. Rows 33–34 are nonetheless declared "complete".

   The resultant step itself is valid, and E² + 2xE − 1 = −2e^{−x}(sinh x − x) checks. Suggested fix: print the quadratic, prove the two limits, then keep the resultant argument.

6. [b/c] Proposition 30 (D3). No proof appears in the document. The excess-set formula agrees with a direct computation in 2,000 random cases, so it is probably right. Two specific problems:
   - "Census shape: lower ray or Empty" is a numerical observation placed inside a "Proposition (proved)".
   - The onset "iff ρ > 2 + u" is drawn from the small-Δt limit, but at ρ = 2 + u the first- and second-order terms cancel exactly. With x = λΔt, the expression s(1−φ)(ρ(1+φ)−2) − 4φ equals −u(3u² + 6u + 4)x³/6 + O(x⁴). So the equality case needs this cubic term; it does hold (no excess near 0), but the stated argument does not show it.

   Suggested fix: add the expansion; prove or relabel the shape claim.

7. [b] Proposition 36 ("two rays, or (1,1,k)") and Corollary 66. Both use C2 or C2′ (finitely many turning points or plateaus, continuity) without establishing it:
   - For the sampled relays, finiteness is exactly the open Conjecture 38.
   - For an arbitrary causally ordered sweep, P is only shown non-increasing. Without continuity a superlevel set can be (θ₋, x], which is not open (C3), and Theorem 3 needs finitely many plateaus.

   Suggested fix: state "assuming C2" in Proposition 36. In Corollary 66, say "an initial segment", or add continuity of P as a hypothesis.

8. [a, minor] Corollary 48: "each bump crosses 1.25F exactly twice" is not justified. v_B is strictly decreasing, so v_B plus a unimodal bump need not be unimodal; on the rising flank v can wiggle across 1.25F more than twice. Suggested fix: define v directly on each bump interval as strictly increasing then strictly decreasing, keeping it ≥ v_B and smooth at the support ends (for example by requiring b′ > |v_B′| on the rising flank).

9. [b] Corollary 59 (equal-height maxima). "Just below M2 both count in k" fails if either maximum's component reaches an end. Example: L₋ > M2 with no dip below R² between θ₋ and the first maximum; that maximum then lies in the lower ray. Suggested fix: add the hypothesis that both maxima lie in windows, which is the equality condition of Theorem 2(c).

10. [b, minor] Theorem 2(d) and the equality rows of Propositions 10 and 12. The proof of (d) points to the construction in (a), which assumes R² ∉ C. At interior critical tolerances the rule that is needed (a minimum with value R² is removed and splits a component; a maximum with value R² contributes nothing) is used, for example "the domain minus Π0*", but never stated. The extension is immediate, since {σ² > R²} on each piece is determined for every R², but it should be written. Also, the approach directions in (d) are redundant: they are determined by the ordered sequence under C2.

11. [b, wording] Proposition 9, first bullet: "L₋ = V_c and L₊ = F, approached from below" reads as if both limits are approached from below. This contradicts the second bullet (V_c from above when c ≤ G*). Suggested fix: "L₊ = F, approached from below; V_c's direction: see below."

12. [b, minor] Proposition 33. "By Theorem 65 an ordering would move all metrics the same way" needs one unstated step. Theorem 65 gives a pointwise-in-t inequality between two cyclostationary error curves with different periods. Post and prior are the minimum and supremum of each curve over its own period, and avg is the time mean. Then P_θ₂ ≤ P_θ₁ pointwise gives min ≤ min, sup ≤ sup and mean ≤ mean. Suggested fix: add this sentence.

13. [b, minor] Theorem 69 and its Reading. The Reading says causal ordering, pathwise (Blackwell) ordering and spectral dominance "coincide", but the theorem lists only (i)–(iii). The proof of (i) ⇒ (ii) uses only the two-sided smoothing inequality, which any non-causal garbling also gives, so pathwise ⇒ (ii) does follow. It should be stated as part (iv). The frequency-localization step should also say it normalises |ĝ|² by L and uses the approximate-identity lemma at Lebesgue points; the ±ω0 cross terms vanish because ω0 ≠ 0 and spectra are even. The argument is otherwise sound.

14. [c, minor] Proposition 54, case g = 2F. The parenthetical "lower ray for R² < F, Empty at R² ≥ F" omits All for R² ≤ H. The final class list is correct. Suggested fix: "All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F)".

Points checked and found correct:
- Theorem 2 (a)–(c) and Theorem 3.
- Propositions 7, 9–12, including every equality row (P1–P3, Π = Π_A, Π = Π_B, R² = σ*², R² = F), and Theorem 8.
- Lemma 13, Propositions 14–19, Proposition 20 (orthogonality, the a = 1/τ case, the G → ∞ endpoint, compactness), Proposition 21 and Theorem 24 (including the β = 0 and β = 2 limits).
- Theorem 25: the identity Φ_ττ = P²(β + (2−β)λ²τ²)/τ³ checks, and so does the "two strict maxima enclose a minimum" argument.
- Theorem 32 (a), (b), (c): every displayed identity checks.
- Propositions 41–43: formulas, w_M, derivative numerators, and the equality cases ρ = 2 and λ′ = λ/2.
- Propositions 53 and 57 (both tables, with R² = m and M = F handled correctly).
- Theorem 56: the R(T) coefficients, Descartes' rule, the n = 2 factorisation and φ*.
- Propositions 68 and 70, Proposition 71 (including All at R² ≤ σ*²) and Proposition 73.
- Every other row of the synthesis matrix agrees with its cited result.

Overall: The analytic core is sound. The critical-tolerance theorem, the design-sweep and τ-sweep classifications with their equality rows, the strict gap, β-unimodality, M-P monotonicity, the general-n Hill theorem and the spectral characterisation of causal garblings all survive a line-by-line check, and every worked number I recomputed is right. The errors sit in the Δt (sampled-filter) section and the synthesis matrix. D2 needs an unstated c < 2 (c = 3 is a counterexample), and row 26's "2R iff G > 2FΠ" is false for avg (G = 0.019 is a counterexample). Theorem 35 depends on a quadratic the document never prints and on M-I endpoint limits proved nowhere. Proposition 30 and the class claims for sampled relays mix proved and numerical statements. Theorem 6, Corollaries 48, 59 and 66, Proposition 36, and the optimal prior/avg equality row need small rewording or added hypotheses. None of this touches the main theorems, but items 1, 2 and 5 should be fixed before the paper relies on rows 25–34.
```

## Dispositions

All 14 points are **valid**. Points 1, 2 and 6 were reproduced independently before acting (`t12_common` at 40 digits: D2 with
c = 3 gives P⁺/F = 233.1, 77.36, 12.7, 4.886 at Δt = 1, 10, 100, 1000 and a prior that tends to F from above; D1 avg with
G = 0.019 has a maximum at Δt = 17.805 (avg/F = 0.999186) and a minimum at Δt = 149.47 (0.9986504) after starting at 0.9990677;
SymPy gives the ρ = 2 + u expansion −u(3u² + 6u + 4)x³/6). Every fix is logged in the document's change log (rows 31–44).

| # | Valid? | Fix |
|---|---|---|
| 1 | valid (document error) | D2 now requires $0 < c < 2$ in the model definition (all Task 12 and Task 13 draws had $c < 2$); the $c \ge 2$ cases are stated as a remark (All for $\kappa > 2$, upper ray otherwise). |
| 2 | valid (document error) | Rows 25–26: "2R if $G > 2F\Pi$ (Proposition 36); also found for $G \le 2F\Pi$ in avg (Numerical result 37)". The class lists were already correct. |
| 3 | valid | Theorem 6: "a failure set of class $(0,0,k)$, $k \ge 1$". |
| 4 | valid (missing equality row) | Optimal prior/avg classes and rows 22–23, 33–34: All ($R^2 \le \sigma_\star^2$). |
| 5 | valid | Theorem 35 rewritten with the quadratic printed. The referee's request led to a shorter proof: $a_0 = -a_1$ exactly, so $p = 2/(1 + \sqrt{1 + 2u/k(x)})$ with $k(x) = (1+u)x\coth(x/2) - 2u$, strictly increasing from 2 to $\infty$; this gives monotonicity and both limits. Verified in `t13_A3_closed.py` (11/11). The resultant argument is kept as a second route. |
| 6 | valid | Proposition 30 now has a proof (via Lemma 27 and the D3 quadratic) and the cubic term at $\rho = 2 + u$; the census shape moved to Numerical result 37. |
| 7 | valid | Proposition 36 states "assuming C2"; Corollary 66 adds continuity of $P$ (and C2′ for the class statement) and otherwise says "an initial segment". |
| 8 | valid | Corollary 48's construction now defines $v$ on each bump support as strictly increasing then strictly decreasing, $\ge v_B$, smooth at the support ends. |
| 9 | valid | Corollary 59 adds the hypothesis that both maxima lie in windows. |
| 10 | valid | Theorem 2(d) proof now states the rule at interior critical tolerances; notes that the approach directions follow from the sequence under C2. |
| 11 | valid (wording) | Proposition 9 first bullet reworded. |
| 12 | valid | Proposition 33 adds the min/sup/mean step. |
| 13 | valid | Theorem 69 adds (iv) pathwise (non-causal) Blackwell ordering, and the localization detail. |
| 14 | valid (missing equality row) | Proposition 54's $g = 2F$ case lists All for $R^2 \le H$. |

## Reproducibility (Part D)

Clean checkout: `git worktree` of the repository, replayed with `reproduce_all.sh` in four invocations: Task 8; Tasks 9–12 (restarted after a container restart interrupted the first run during Task 9; it stopped at Task 10, below); Tasks 11–12; Task 13 on the final commit. Task 10's runtime is the sum of its scripts' logged runtimes.

| Task | Runtime (s) |
|---|---|
| 8 | 327 |
| 9 | 807 |
| 10 | 14845 |
| 11 | 5117 |
| 12 | 11312 |
| 13 | 8894 |

Total measured wall time 41302 s (11.5 h) on 4 CPUs. The Tasks 8–12 replay shared the CPUs with this run's Task 13 audits (hence Task 10 at 2.5x and Task 12 at 1.3x the original); the Task 13 replay ran alone; manifest with SHA-256 of 204 output files in `results/repro_manifest.json`. A reviewer with 4 CPUs and nothing else running should expect the original runtimes (Task 8 161 s, Task 9 631 s, Task 10 5861 s, Task 11 4394 s, Task 12 8935 s) plus Task 13's 8894 s: about 8.0 h for Tasks 8–13.

**Task 13: PASS.** The full Task 13 replay (every script, including the complete 42-row C2 audit, on commit 08a63bb in a fresh worktree) gives 56/56 result files identical to this run after masking runtimes and paths (`compare_t13.py`); the ten figures' PNG and caption files are byte-identical. Files only in this run: t13_audit_classes_n3.json, t13_audit_numbers_run1.json, t13_partA_numeric_A4_A5_A7.json (records of the first C1 run, the N = 3 smoke run and the second Part A numeric invocation, merged in the comparison).

**Task 10: FAIL as pre-registered** (the replay stopped with an error, so no report was regenerated). Diagnosis (`repro_t10_diag.py`): Task 10 (attribution: code, Task 10's run script). t10/run_t10.sh omits t10_realize_diag.py; make_results_t10.py needs its t10_2_diag.json. After running it in the clean checkout (0 s), make_results_t10.py exit code 0; comparison with the committed RESULTS_t10.md: 1 issues, verdicts identical True.

Pre-registered comparison (`compare_repro.py`): Task 8 PASS; Task 9 PASS; Task 10 not reproduced; Task 11 PASS; Task 12 FAIL (1 issues, verdicts identical True).

Diagnosis of the comparison failures (`repro_compare_diag.py`): Task 12: 1 difference(s), verdicts identical True, all on the provenance runtime line True (attribution: criterion; the masking covers runtime numbers but not the list of script names, which differs because the original runs were separate invocations).

Task 12 differences: {"kind": "text", "line": 191, "committed": "Results come from separate invocations of the committed scripts (symbolic and A#/A# directly; A# Part B, Part C, diagnosis and figures as one chain). `run_t#sh` reproduces everything in one pass. Runtime per script (s): t#_a# # t#_sigma # t#_diag # t#_figu

## Deliverables

- `classification/Stages_0_4_Consolidated.md`: the single source document (73 results, change log of 45 corrections).
- `classification/Roadmap_v3.md`: status, open problems, final matrix, Stages 5–6, Paper 2 outline, novelty check.
- `classification/figs_paper2/`: ten figures (PNG + PDF + caption each; `README.md` lists them).
- `classification/reproduce_all.sh`, `t13/compare_repro.py`, `t13/run_t13.sh`.
- `t13/literature_check.md` (queries and sources), `t13/referee_report.md`.

## Provenance

This run's results come from separate invocations (Part A numerics in two after a container restart; C1 re-run after fixes; diagnoses after the failures). Runtime per script in the single-pass Task 13 replay (s): t13_partA_symbolic 5.6, t13_partA_symbolic_diag 0.8, t13_regression_symbolic 32.3, t13_partA_numeric 2128.9, t13_partA_numeric_diag 5.5, t13_A3_attempt 0.8, t13_A3_proof 1.7, t13_A3_closed 114.8, t13_A3_limits 3.5, t13_audit_numbers 2.2, t13_audit_refs 0.6, t13_audit_classes 6461.0, t13_audit_classes_diag 44.1, t13_audit_classes_diag2 73.4, t13_figures_paper2 18.0. Commits after 08a63bb (the replay's) change only post-hoc diagnosis, comparison and report-building scripts.
