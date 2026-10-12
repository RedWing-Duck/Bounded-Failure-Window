# Task 12 — completing Stage 2 (Δt and Σ sweeps) with Stage 3/4 checks: results

Pre-registration `classification/PREREG_t12.md`, commit **6e09e88**; code and results commit **82edc1b**. Total measured script runtime **9635 s** on 4 CPUs (Python 3.13.16, mpmath 1.3.0, SymPy 1.14.0).

| Check | Verdict | Counts / worst errors | Runtime (s) |
|---|---|---|---|
| Symbolic identities and signs (A1–A6, B1–B5) | **FAIL** | 66/67 items; failing: D2 post at dt->oo: lim dt (P+ - (1-c)^2 F) - c[c + 2(1-c) F Pi0]/Pi == 0 | 16 |
| A2 D1 excess set at R² = F (1,000 sets) | **PASS** | 1000/1000 match; non-empty predicted 470; max rel. error of Δt_E 1.14e-30 |  |
| A3 D2 excess set at R² = F (1,000 sets) | **PASS** | 1000/1000 match; non-empty predicted 183; max rel. error of Δt_E 1.13e-30 |  |
| A4 D3 excess set vs exact condition (1,000 sets) | **PASS** | 1000/1000 agree; membership disagreements 0 of 201514 test points; onset predicted (ρ > 2 + u) 257, observed 257; shapes {'Empty': 743, 'lower ray': 257} |  |
| A6 regression (optimal M-P, 5 s.f.) | **PASS** | post(1) = 0.0098858451 (stated 0.0098858); avg(1) = 0.0099506471 (stated 0.0099506); post(10) = 0.0090909091 (stated 0.0090909); avg(10) = 0.0099545455 (stated 0.0099545); post(100) = 0.005 (stated 0.0050000); avg(100) = 0.009975 (stated 0.0099750) |  |
| A6 numerical monotonicity (record) | record | 400,000 points × 3 metrics, λΔt ∈ [1e-8, 1e8]: violations {'post': 0, 'prior': 0, 'avg': 0}; Δt → 0 max rel. dev. from σ*² 2.2e-57 |  |
| A7 minimum below F and two rays (D1, G > 2FΠ) | **FAIL** | prior 366/907 (no minimum found 538), avg 907/907 (no minimum found 0) |  |
| A8 census: route (i) = route (ii) | **PASS** | sets with a disagreement: D1 post 0, D1 prior 0, D1 avg 0, D2 post 0, D2 prior 0, D2 avg 0, D3 post 0, D3 prior 0, D3 avg 0 | 3045 |
| A8 qualitative regression (prompt's values) | **FAIL** | post single max True, value within 2% of 0.166 False, at Δt within ×2 of 1 False; avg crossing within ×1.5 of 50 False; then min below F, back from below True |  |
| A9 regression vs Task 11 (1e-12) | **PASS** | max rel. error 8.59e-17 |  |
| A9 numerical monotonicity (record) | record | 400,000 points × 2 metrics, λΔt ∈ [1e-8, 1e8]: violating sets 0; SymPy sign attempt: (a) unresolved, (b) unresolved | 122 |
| A10 pairs (Δt, 2Δt) | **PASS** | post(2Δt) < post(Δt) in 1000/1000, avg(2Δt) > avg(Δt) in 1000/1000 | 79 |
| B2, B3, B5 census (2,000 sets each, both conventions) | **PASS** | B2 abs: 2000/2000; B2 rel: 2000/2000; B3 abs: 2000/2000; B3 rel: 2000/2000; B5 abs: 2000/2000; B5 rel: 2000/2000; max error of the maximum's position 6.05e-31 |  |
| B4 census (2,000 sets, both conventions) | **PASS** | B4 abs: 2000/2000; B4 rel: 2000/2000; max error of the maximum's position 6.05e-31 | 2912 |
| Part C blind search (22 combos) | **PASS** | 4,400,000 classifications; flagged 1109; persisting 0 | 3340 |

**Pre-registered checks that FAIL:** Symbolic identities and signs (A1–A6, B1–B5); A7 minimum below F and two rays (D1, G > 2FΠ); A8 qualitative regression (prompt's values). Each is diagnosed below.

## Plain statements

- **Is any prediction falsified?** Yes, two, both disclosed in the pre-registration before the run: (1) the prompt's A4 conjecture "the D3 excess set is non-empty as Δt → 0 iff ρ > 2" is false at fixed Π; the onset is ρ > 2 + u, u = 2ΣΠ/λ² (proved, and confirmed on every census set; counterexamples below); (2) the prompt's A8 quick-check values (post maximum ≈ 0.166 near Δt ≈ 1; avg crossing F near Δt ≈ 50) are wrong: the maximum is 0.20457 at Δt = 2.4645 and the crossing is at Δt_E = 100 exactly (by A1–A2). No theorem or proposition-level claim of the prompt is contradicted otherwise.
- **Did any class outside the predicted sets appear?** No: Part C found no persisting out-of-set class or route disagreement. The A8 census itself recorded mixed classes (0, 1, 1), (1, 0, 1) (they define the D-family allowed sets in Part C).
- **Open Stage 2 entries:** monotonicity of the optimal M-P prior and avg along Δt (A6; numerical only); M-I optimal monotonicity along Δt (A9, Numerical result 4.10a; numerical only); exact turning-point counts for the D1–D3 relay families along Δt (census only, no proof); the number of minima of D1 prior/avg (census only).

## [prove] items: outcome

| Item | Outcome | Basis |
|---|---|---|
| A1 shared excess set | proved | SymPy identities (A1, 5/5) |
| A2 D1 excess set (0, Δt_E) iff G > 2FΠ | proved | tanh lemma, h′ < 0 (series of sinh x − x), lim h = 1/2; numerics 1,000/1,000 |
| A3 D2 excess set iff κ > 2, closed-form Δt_E | proved | identity for L/(2−L); numerics |
| A4 exact D3 condition φ < 1 and s(1−φ)(ρ(1+φ)−2) > 4φ | proved | Q(T) identity; census agreement |
| A4 prompt conjecture (onset iff ρ > 2) | **disproved** | Δt → 0 limit of the condition is ρ − 2 − u; counterexamples below |
| A5 endpoint limits and first-order coefficients | proved | SymPy limits/series; D2 post O(1/Δt) coefficient by the series route (diagnosis) |
| A6 post strictly decreasing | proved | P⁺ = F/(1 + μ), μ increasing in φ and φ/s (SymPy) |
| A6 prior and avg strictly increasing | unresolved | no sign proof found; 0 violations on 400,000 points |
| A7 interior minimum below F, two rays | proved | A5 limits (σ²(G,Π) > F at 0, F from below at ∞) and continuity |
| A9 M-I monotonicity | unresolved | SymPy sign undecided; 0 violations on 400,000 points |
| A10 M-P is not a causal-garbling family along Δt | proved | post strictly decreasing (A6) and avg − F ~ −F/(2λΔt) increasing at large Δt (A5) |
| B1 scaling lemma | proved | SymPy |
| B2 Σ-independent gain | proved | SymPy signs, limits |
| B3 single maximum iff ρ > 2 at w_M | proved | SymPy identities, parabola argument |
| B4 abs increasing; rel single maximum iff λ′ < λ/2 | proved | SymPy identities, parabola argument; census |
| B5 optimal | proved | SymPy |

Derivations recorded verbatim by `t12_symbolic.py`:

- `[record] sinh x - x series (all coefficients positive: x - sinh x < 0 for x > 0): xx**11/39916800 + xx**9/362880 + xx**7/5040 + xx**5/120 + xx**3/6`
- `[record] lim_{dt->0} [s(1-phi)(rho(1+phi)-2) - 4 phi]/(2 lam dt) with phi = (u/4)(2 lam dt): rho - u - 2  (> 0 iff rho > 2 + u)`
- `[record] D1 avg second-order coefficient (verbatim): -G**2*(G**2 + 4*G*lambda - 8*Pi*Sigma)/(24*Pi*(G + lambda))`
- `[record] proof: post strictly decreasing (PROVED): phi = F Pi dt and w = phi/s = F Pi dt/(1 - e^{-2 lam dt}) are strictly increasing in dt (e^y > 1 + y); mu increases strictly in both; P+ = F/(1 + mu), so P+ is strictly decreasing.`
- `[record] prior and avg (attempt): P- = F - a^2 F mu/(1+mu) and avg = F - F mu/(1+mu) * s/(2 lam dt): a decreasing factor times an increasing one; no sign proof found by this route -> reported as unresolved unless the numerical evidence says otherwise.`
- `[record] single maximum iff rho > 2: numerator is a downward parabola in w with value 2(rho-2) at w = 1 and vertex at (rho-1)/(1+rho) < 1: one root in (1, oo) iff rho > 2, none otherwise (PROVED).`
- `[record] single maximum iff lam' < lam/2: numerator -G^2 - 2 lam' G + lam' (lam - 2 lam'): downward parabola, value lam'(lam - 2 lam') at G = 0, vertex at G = -lam' < 0: one positive root iff lam > 2 lam' (PROVED); G increases with Sigma.`

**A7 argument.** For D1 with G > 2FΠ, prior and avg tend to σ²(G, Π) > F as Δt → 0 (A5; σ²(G,Π) > F ⇔ G > 2FΠ) and to F from below as Δt → ∞ (prior − F = a²(P⁺ − F) and avg − F = (P⁺ − F)s/(2λΔt) with P⁺ → 0). Both are continuous, so each crosses F and attains an interior minimum below F; for R² between that minimum and F the failure set contains a neighbourhood of 0 and of ∞ but not the minimiser: two rays (ℓ = u = 1), or (1,1,k) with several minima.

**A10 argument and explanation.** If fine ⪯_c coarse (or the reverse) held along Δt, Theorem 4.2 would order every pointwise optimal error the same way. But post(2Δt) < post(Δt) for all Δt (A6, proved) while avg(2Δt) > avg(Δt) for all large Δt (avg − F ~ −F/(2λΔt)), so neither direction holds. *Why:* each sample of M-P carries the signal with variance 1/(ΠΔt), so a longer interval makes every individual sample more precise and the error just after an update falls; but samples get sparser, so the error grows more between updates and the prior and time-averaged errors rise.

## A8 census (2,000 sets per family, seed 12008)

| Family | Metric | Turning-point histogram | Classes (10 tolerances per set) | Route disagreements |
|---|---|---|---|---|
| D1 | post | {'none': 1093, 'max': 907} | {'Empty': 9154, 'lower ray': 8135, 'window': 2711} | 0 |
| D1 | prior | {'none': 1521, 'min': 369, 'max-min': 110} | {'All': 5594, 'upper ray': 3472, 'Empty': 5993, 'lower ray': 3640, 'two rays': 1309, '(0, 1, 1)': 212} | 0 |
| D1 | avg | {'none': 924, 'min': 1070, 'max-min': 6} | {'All': 4540, 'upper ray': 3432, 'Empty': 5603, 'lower ray': 3269, 'two rays': 3155, '(0, 1, 1)': 13} | 0 |
| D2 | post | {'none': 986, 'max': 778, 'min-max': 167, 'min': 69} | {'Empty': 5957, 'lower ray': 3864, 'All': 5693, 'upper ray': 2315, 'window': 1610, 'two rays': 744, '(1, 0, 1)': 151} | 0 |
| D2 | prior | {'none': 1670, 'min': 330} | {'All': 6741, 'upper ray': 4056, 'Empty': 7011, 'lower ray': 1317, 'two rays': 875} | 0 |
| D2 | avg | {'none': 1457, 'min': 543} | {'All': 6317, 'upper ray': 4104, 'Empty': 6728, 'lower ray': 1257, 'two rays': 1594} | 0 |
| D3 | post | {'none': 1482, 'max': 518} | {'Empty': 10058, 'lower ray': 8443, 'window': 1499} | 0 |
| D3 | prior | {'none': 1525, 'min': 264, 'max-min': 211} | {'All': 6019, 'upper ray': 4488, 'Empty': 6473, 'lower ray': 1638, 'two rays': 1368, '(0, 1, 1)': 436} | 0 |
| D3 | avg | {'none': 1146, 'min': 854} | {'All': 5101, 'upper ray': 4578, 'Empty': 6037, 'two rays': 2589, 'lower ray': 1695} | 0 |

A4 shapes of the D3 excess set at R² = F (post): {'Empty': 743, 'lower ray': 257}. Max |E|/scale of the exact condition at the classifier's ends: 2.22e-29.

## Part B census (2,000 sets each, seed 12020)

| Family | Convention | Turning points | Predicted maxima | Classes | Out of set | Disagreements |
|---|---|---|---|---|---|---|
| B2 | abs | {'none': 2000} | 0 | {'All': 10919, 'upper ray': 9081} | 0 | 0 |
| B2 | rel | {'none': 2000} | 0 | {'All': 10951, 'lower ray': 9049} | 0 | 0 |
| B3 | abs | {'none': 2000} | 0 | {'upper ray': 20000} | 0 | 0 |
| B3 | rel | {'none': 1144, 'max': 856} | 856 | {'Empty': 9087, 'lower ray': 7838, 'window': 3075} | 0 | 0 |
| B4 | abs | {'none': 2000} | 0 | {'upper ray': 20000} | 0 | 0 |
| B4 | rel | {'none': 1153, 'max': 847} | 847 | {'Empty': 9355, 'lower ray': 8293, 'window': 2352} | 0 | 0 |
| B5 | abs | {'none': 2000} | 0 | {'upper ray': 20000} | 0 | 0 |
| B5 | rel | {'none': 2000} | 0 | {'Empty': 10998, 'lower ray': 9002} | 0 | 0 |

## Part C blind search (seed 12100)

| Combo | Curves | Classifications | Classes | Allowed | Flagged | Persisting |
|---|---|---|---|---|---|---|
| opt post | 1000 | 200,000 | {'lower ray': 89904, 'Empty': 110096} | Empty, lower ray | 0 | 0 |
| opt prior | 1000 | 200,000 | {'All': 65018, 'Empty': 65013, 'upper ray': 69969} | All, Empty, upper ray | 0 | 0 |
| opt avg | 1000 | 200,000 | {'upper ray': 69722, 'All': 65116, 'Empty': 65162} | All, Empty, upper ray | 193 | 0 |
| D1 post | 1000 | 200,000 | {'Empty': 90139, 'lower ray': 79601, 'window': 30260} | Empty, lower ray, window | 0 | 0 |
| D1 prior | 1000 | 200,000 | {'lower ray': 40509, 'Empty': 56055, 'All': 55205, 'two rays': 8923, 'upper ray': 38119, '(0, 1, 1)': 1189} | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | 234 | 0 |
| D1 avg | 1000 | 200,000 | {'Empty': 52935, 'lower ray': 41269, 'All': 49062, 'two rays': 22188, 'upper ray': 34505, '(0, 1, 1)': 41} | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | 0 | 0 |
| D2 post | 1000 | 200,000 | {'All': 60757, 'Empty': 62177, 'lower ray': 38002, 'upper ray': 21031, 'two rays': 5874, 'window': 11506, '(1, 0, 1)': 653} | (1, 0, 1), All, Empty, lower ray, two rays, upper ray, window | 0 | 0 |
| D2 prior | 1000 | 200,000 | {'All': 68169, 'Empty': 69193, 'upper ray': 39425, 'lower ray': 17060, 'two rays': 6153} | All, Empty, lower ray, two rays, upper ray | 151 | 0 |
| D2 avg | 1000 | 200,000 | {'All': 65752, 'two rays': 11850, 'Empty': 68056, 'lower ray': 13333, 'upper ray': 41009} | All, Empty, lower ray, two rays, upper ray | 22 | 0 |
| D3 post | 1000 | 200,000 | {'Empty': 99585, 'window': 15787, 'lower ray': 84628} | Empty, lower ray, window | 0 | 0 |
| D3 prior | 1000 | 200,000 | {'All': 61449, 'Empty': 62505, 'upper ray': 48247, 'lower ray': 17522, 'two rays': 8220, '(0, 1, 1)': 2057} | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | 234 | 0 |
| D3 avg | 1000 | 200,000 | {'upper ray': 50647, 'Empty': 60856, 'All': 58496, 'lower ray': 13479, 'two rays': 16522} | All, Empty, lower ray, two rays, upper ray | 275 | 0 |
| MI a | 1000 | 200,000 | {'Empty': 65238, 'upper ray': 69680, 'All': 65082} | All, Empty, upper ray | 0 | 0 |
| MI b | 1000 | 200,000 | {'All': 64733, 'Empty': 63892, 'upper ray': 71375} | All, Empty, upper ray | 0 | 0 |
| B2 abs | 1000 | 200,000 | {'upper ray': 90152, 'All': 109848} | All, upper ray | 0 | 0 |
| B2 rel | 1000 | 200,000 | {'lower ray': 89815, 'All': 110185} | All, lower ray | 0 | 0 |
| B3 abs | 1000 | 200,000 | {'upper ray': 200000} | All, upper ray | 0 | 0 |
| B3 rel | 1000 | 200,000 | {'Empty': 89254, 'lower ray': 77576, 'window': 33170} | Empty, lower ray, window | 0 | 0 |
| B4 abs | 1000 | 200,000 | {'upper ray': 200000} | All, upper ray | 0 | 0 |
| B4 rel | 1000 | 200,000 | {'Empty': 94889, 'lower ray': 82379, 'window': 22732} | Empty, lower ray, window | 0 | 0 |
| B5 abs | 1000 | 200,000 | {'upper ray': 200000} | All, upper ray | 0 | 0 |
| B5 rel | 1000 | 200,000 | {'Empty': 109910, 'lower ray': 90090} | Empty, lower ray | 0 | 0 |

## Synthesis-matrix rows

| Sweep | Filter | Metric / convention | Classes | Label |
|---|---|---|---|---|
| Δt (M-P) | optimal | post | lower ray, Empty | Theorem (A6 post) |
| Δt (M-P) | optimal | prior, avg | All, upper ray, Empty | Numerical result (monotonicity unresolved) |
| Δt (M-P) | D1 | post | Empty, lower ray, window | Proposition (excess set, A2); other classes Numerical result |
| Δt (M-P) | D1 | prior | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | Proposition (excess set, A2; two rays exist, A7); other classes Numerical result |
| Δt (M-P) | D1 | avg | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | Proposition (excess set, A2; two rays exist, A7); other classes Numerical result |
| Δt (M-P) | D2 | post | (1, 0, 1), All, Empty, lower ray, two rays, upper ray, window | Proposition (excess set, A3); other classes Numerical result |
| Δt (M-P) | D2 | prior | All, Empty, lower ray, two rays, upper ray | Proposition (excess set, A3); other classes Numerical result |
| Δt (M-P) | D2 | avg | All, Empty, lower ray, two rays, upper ray | Proposition (excess set, A3); other classes Numerical result |
| Δt (M-P) | D3 | post | Empty, lower ray, window | Proposition (exact excess condition, A4); other classes Numerical result |
| Δt (M-P) | D3 | prior | (0, 1, 1), All, Empty, lower ray, two rays, upper ray | Proposition (exact excess condition, A4); other classes Numerical result |
| Δt (M-P) | D3 | avg | All, Empty, lower ray, two rays, upper ray | Proposition (exact excess condition, A4); other classes Numerical result |
| Δt (M-I) | optimal | (a), (b) | All, upper ray, Empty | Numerical result (4.10a; unresolved) |
| Σ | B2 (Σ-independent gain) | absolute | All, upper ray | Theorem |
| Σ | B2 | relative | All, lower ray | Theorem |
| Σ | B3 (Σ-tracking, over-trust ρ) | absolute | upper ray | Theorem |
| Σ | B3 | relative | lower ray, Empty (ρ ≤ 2); lower ray, window, Empty (ρ > 2) | Theorem |
| Σ | B4 (misspecified λ′) | absolute | upper ray | Theorem |
| Σ | B4 | relative | lower ray, Empty (λ′ ≥ λ/2); lower ray, window, Empty (λ′ < λ/2) | Theorem |
| Σ | B5 (optimal) | absolute | upper ray | Theorem |
| Σ | B5 | relative | lower ray, Empty | Theorem |

## Diagnoses of failures

### Symbolic: A5 'D2 post at Δt → ∞' (attribution: code — the SymPy check route)

`sympy.limit` returns 0 for lim Δt(P⁺ − (1−c)²F). Exact route (`t12_symbolic_diag.py`): replace e^{−2λΔt} by 0 (beyond all orders), set Δt = 1/t and take t → 0: limit `-c*(2*Pi_0*Sigma*c - 2*Pi_0*Sigma - c*lambda)/(Pi*lambda)`, difference from the pre-registered c[c + 2(1−c)FΠ0]/Π: 0. mp (dps ≥ 100) on 200 random sets: worst relative error dt=1e10: 4.55e-07, dt=1e20: 4.55e-17, dt=1e40: 4.55e-37 — O(1/Δt). The asymptotic used by the classifier is correct.

### A7 (attribution: criterion — the pre-registered zero tolerance is too coarse for the prior dip)

In 538 of 907 D1 sets with G > 2FΠ the T10 method found no minimum of the prior below F (avg: 0). Past Δt_E, prior − F = e^{−2λΔt}(P⁺ − F) and d prior/dΔt = e^{−2λΔt}·g(Δt), g = 2λ(F − P⁺) + dP⁺/dΔt; the pre-registered zero tolerance 1e-40·|prior|/θ treats the derivative as zero once e^{−2λΔt} is below about 1e-40, so the sign change is never seen. Scanning the sign of g instead (`t12_diag.py`) finds a minimum in 590 of the 590 sets it scanned (the 538 without a minimum plus those whose minimum equals F in double precision; number of minima {'1': 590}), at λΔt in [17.4, 3.79e+07] with relative dip (F − prior)/F between 10^-32880317 and 10^-17. The existence claim (A7, proved above) holds; the dips are real but far below any practical tolerance. avg sets missed: 0. In 3 further sets a minimum below F was found but the class at (min + F)/2 came out lower ray: their relative dips are 2.74e-41, 4.72e-41, 2.5e-41, below the classifier's equality tolerance 1e-40, so R² = (min + F)/2 is treated as equal to F (same cause).

### A8 qualitative regression (attribution: prediction — the prompt's quick-check numbers)

post rises from σ²(0.5, 1) = 0.09 to a single maximum 0.204573 at Δt = 2.4645; post(1) = 0.166278 (the prompt's 0.166). avg crosses F at Δt = 100 (= Δt_E of A2, exactly 100 to 20 digits), then reaches a minimum (min at 200: 0.0099875) and returns to F from below. Classes: window at R² = 0.12 (window), two rays between the minimum and F (two rays). The qualitative picture of the prompt is right; its numbers are not.

### A4 conjecture (attribution: prediction)

Among the 1000 D3 sets, ρ > 2 in 435; 178 have 2 < ρ ≤ 2 + u, where the conjecture predicts an excess set at small Δt and the exact condition does not. Observed: ρ > 2 without onset in 178 sets; onset observed 257 = predicted by ρ > 2 + u 257.

## Implementation notes and deviations

1. **Lambdify with common-subexpression elimination** (`cse=True`) for the Δt metrics and derivatives, added before any pre-registered run: about 5× faster for D3/optimal; values unchanged (checked on the smoke set).
2. **Tolerances for curves without a finite positive critical value** (B3–B5 absolute: monotone 0 → ∞; not covered by the pre-registration): R² drawn as values of the curve itself at u log-uniform on [1e-20, 1e20] (10 in Part B, 200 in Part C).
3. **A2–A4 numerical checks** use the first 1,000 A8 census sets of each family (seed 12008; the pre-registration gave no separate seed). A10 pairs continue the A6 stream (seed 12006) after the 1,000 A6 sets.
4. **A8 was restarted** a few minutes into its first run to also save the per-set excess end points (for figure H3); later the census, Σ sweep and blind search were relaunched as one detached chain after the first launch hit the session's background time limit. No partial results were used.
5. **Bug fixed (code):** `t12_blind.py` first imported `classify` before `t12_common` had put `t10/` on the path; the first chain run of the blind search crashed at import (0.1 s, no results). Import order fixed in commit `4189376`, smoke-tested on 2 curves per combo, then run in full. In the full run, 1109 flagged float cases were all resolved by the dps-60 re-run.
6. **Figures** were regenerated after the chain with two layout fixes (H2 legend placement; H3 closed-form curves extended to 1e6 and the D2 curve started at κ = 2); data unchanged.
7. **A4 membership check:** 201 log-spaced points over λΔt ∈ [1e-20, 1e20] plus midpoints between, and one decade beyond, the classifier's ends; points within 1e-8 (in log10) of an end skipped.

## Figures

`figs/H1_optimal_MP`, `H2_D1_G05`, `H3_onset_maps`, `H4_B3_relative`, `H5_B2_B3_abs_rel` (PNG + PDF).

![H1_optimal_MP](figs/H1_optimal_MP.png)

![H2_D1_G05](figs/H2_D1_G05.png)

![H3_onset_maps](figs/H3_onset_maps.png)

![H4_B3_relative](figs/H4_B3_relative.png)

![H5_B2_B3_abs_rel](figs/H5_B2_B3_abs_rel.png)

## Provenance

Results come from separate invocations of the committed scripts (symbolic and A6/A9 directly; A8, Part B, Part C, diagnosis and figures as one chain). `run_t12.sh` reproduces everything in one pass. Runtime per script (s): t12_symbolic 16, t12_symbolic_diag 3, t12_a8 3045, t12_dt 79, t12_mi 122, t12_sigma 2912, t12_blind 3340, t12_diag 104, t12_figures 14.
