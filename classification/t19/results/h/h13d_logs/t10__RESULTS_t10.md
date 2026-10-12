# Task 10 — Stage 3 falsification and completeness: results

Tests `classification/Stage_3_Plan.md` against `classification/Task_10_Stage3_Prompt.md`. Pre-registration `classification/PREREG_t10.md`, commit **da3d826**; code and results commit **cbe96fe**. Total measured script runtime: **13958 s** on 4 CPUs (Python 3.13.16, mpmath 1.3.0, SymPy 1.14.0).

| Check | Verdict | Counts / worst errors | Runtime (s) |
|---|---|---|---|
| T10.1 symbolic | **FAIL** | 24/26 items reduce to 0 by the fixed route; failing: G(Pi(G)) - G == 0 for Pi = (G^2 + 2 lam' G)/(2 Sig'); sigma*^2(pi_R) - R^2 == 0 | 2 |
| T10.2 realizability: every class | **PASS** | 101/101 targets realized (both routes, G ≥ 0, continuous, σ² = v) | 90 |
| T10.2 forbidden classes | **PASS** | 24/24 blocked |  |
| T10.2 A1.3 as specified (Gaussian bumps, G₊) | **FAIL** | k windows in all five; G → 0 and G²/Π → 0 at 1e-12; **G(1e12)/G(1e11) − 1 = 9** (G₊ diverges) |  |
| T10.2 A1.3 supplementary (compact bumps, G₊ → G₋ at Π_c) | **PASS** | all five pass; G(1e12)/G(1e11) − 1 = 6e-10, branch jump 0 |  |
| T10.3 census | **PASS** | bayes: 2000 sets, TP hist {'1': 906, '0': 1094}, fails 0; misspec: 2000 sets, TP hist {'1': 892, '0': 1108}, fails 0; capped: 2000 sets, TP hist {'0': 1092, '1': 908}, fails 0; blind: 2000 sets, TP hist {'0': 2000}, fails 0; hill: 10000 sets, TP hist {'2': 4868, '0': 5132}, fails 0; parts {'families': True, 'targeted': True, 'regression': True} | 8232 |
| T10.4 mixed class (Hill) | **PASS** | 4868 two-TP sets, 77888 tolerances, failing sets 0 | 3064 |
| T10.5 degeneracies | **FAIL** | equal_maxima pass; inflection pass; plateau pass; pair_birth FAIL; narrow pass | 74 |
| T10.6 matched-variance τ | **FAIL** | routes pass; shape FAIL; classes pass; relay pass; mc pass; regression pass | 199 |
| T10.7 blind search | **PASS** | 1,000,000 classifications; flagged in float64 3; persisting at 60 digits 0 | 2280 |

**Pre-registered checks that FAIL:** T10.1 symbolic; T10.2 A1.3 as specified (Gaussian bumps, G₊); T10.5 degeneracies; T10.6 matched-variance τ. Every one is traced below to the pre-registered criterion or to SymPy's simplification route, not to the plan. The only plan-level issue they expose is a gap in the A1.3 argument (the upper-branch inverse alone cannot give a convergent gain), which the pre-registered branch-following construction closes.

## Plain statements

- **Is any prediction in the Plan falsified?** No. A1 (realizability, forced lower ray, exact class sets), A3 (elasticity lemma and the Bayesian and misspecified-Kalman reductions), A4 (Bayesian, misspecified Kalman, capped, precision-blind and Hill turning-point bounds, including the Hill mixed class), A5 (equal-height maxima, inflection, plateau, pair birth with zero-width band) and A6 (the optimal filter windows along matched-variance τ) all hold in every tested case. A1.3 holds, but only with the branch-switching construction, not with G₊ as the plan writes it (see diagnosis).
- **Was any class outside the predicted set found?** No: 1,000,000 classifications in the blind search, 3 flagged in float64, 0 persisting at 60 digits; no route disagreements anywhere in T10.2–T10.7.

## Diagnoses of the failures

### T10.1: two items not reduced by the fixed SymPy route (route limitation; identities hold)

- Misspecified inverse G(Π(G)) − G: SymPy leaves √(G**2 + 2*G*lambda1 + lambda1**2). Factoring the radicand gives (G + lambda1)**2 and the expression reduces to 0.
- Forced ray σ*²(π_R) − R²: the radicand is (R2*lambda - 2*Sigma)**2/R2**2; its square root equals (2Σ − λR²)/R² only when R² < 2F, which positive-symbol assumptions cannot express. With R² = F/(1 + w), w > 0, and the inner radicand factored as (2*w + 1)**2, it reduces to 0.
- Attribution: **criterion / route** (no √(square) handling in the pre-registered route). Plan: correct.

### T10.2: A1.3 as specified (attribution: plan's construction; criterion as pre-registered)

G₊ = Πv + √(…) ≥ Πv and v → H > 0, so G₊/Π → 2H: Π = 1e+06: G₊/(2HΠ) = 0.9999833339, Π = 1e+09: G₊/(2HΠ) = 0.9999999833, Π = 1e+12: G₊/(2HΠ) = 1.0000000000. The lower branch G₋ equals the Bayesian gain and converges. The pre-registered supplementary construction (compactly supported bumps, G₊ for Π ≤ Π_c and G₋ beyond, where v_B touches σ*²) passes all five k, with branch jump 0 and G(1e12)/G(1e11) − 1 = 6e-10. **A1.3's claim is true; its proof must switch to the lower branch at an envelope touch point, and bumps must not cover that point (Gaussian tails do).**

### T10.5: pair-birth exponent (attribution: criterion)

Slope of log(M − m) vs log δ = **1.5000**; slope of the turning-point separation = 0.5000. Diagnosis (`t10_degenerate_diag.py`, δ to 1e-14): slopes 1.50007 and 0.50002, and (M − m)/sep³ is constant (0.00542983). At a fold the positions separate like δ^(1/2) and the values like δ^(3/2). The pre-registered [0.4, 0.6] applies to positions, not to M − m. The band still closes continuously (M − m → 0 monotonically), as the plan says.

### T10.6: zero-limit criterion (attribution: criterion)

P/P_max at λτ = 1e∓12 is at least 3.99999e-06 in every set (pre-registered prediction: ≥ 4e-6); it equals the asymptote 2e-6(Σ + λv)/√(λΣv) to 0.00039. The supplementary check (P < 1e-6 P_max at λτ = 1e∓24, log-slopes ±0.5 within 1e-3) passes in 1000/1000 sets. P → 0 at both ends, as A6 states.

## Bugs found and fixed (documented)

1. **Onset prediction at δ = 0 (T10.3, found in a 20-set smoke run, fixed before the full run).** The prediction compared κ > 2 in floating mp arithmetic; at κ = 2 exactly the computed κ rounded above 2 and wrongly expected a maximum. Targeted sets now take the side from the sign of δ. The method's counts were correct.
2. **Plateau tolerance (T10.5, found in the full run, fixed and re-run).** The capped curve was built from the float Σ = 0.01 (= 0.0100000000000000002 in binary) while F was the decimal 0.01, so R² = F sat 2e-17 below the plateau and both routes (correctly, for that R²) returned a lower ray. F is now taken from the curve's own parameters; the re-run passes. Commit message records the fix.
3. Same float/decimal mismatch, no effect on any verdict: the Hill window-onset bisection compares M with the decimal F (result 25 to 1e-8 regardless) and the double-root refinement of Π0_pair uses decimal Σ (agrees with the bisection to ~1e-12).

## Wording and formula points in `Stage_3_Plan.md`

1. **A4: "Hill sextic".** Q(t) is a quintic; t·Q(t) is the sextic (N = t·Q(t)/(1 + t²)³, T10.1(e)).
2. **A1.3: "G = G₊(v(Π), Π) is continuous and realizes v" used for regular schedules.** True for realizability, but G₊ → ∞ whenever v → H > 0, so Paper 1 regularity (G → G∞ finite) needs the lower branch beyond an envelope touch point (diagnosis above).
3. **A3: "for a strictly increasing gain with inverse Π(G)".** The identity dσ²/dΠ = G·N/(2Π²(λ+G)²) holds for any differentiable G(Π) > 0 (T10.1(a)); monotonicity is only needed to write N as a function of G.
4. **A4 Hill: "Proposition if A3's sextic can be tamed".** It can (proof support below).
5. **Task prompt (not the plan):** the pair-birth exponent and the λτ = 1e∓12 zero-limit threshold are mis-set (diagnoses above).

## Hill n = 2 proof support (verbatim SymPy output; not pass/fail)

Reduced quintic (α = λ/c, β = ΣΠ0/c², Q/c²):

```
3*alpha*t - 4*beta*t**4 - 8*beta*t**2 - 4*beta + t**5*(-alpha - 1) + t**3*(2*alpha + 1)
```

Discriminant in t, factored:

```
-16*(alpha**4 + alpha**3 + 4*beta**2)*(6912*alpha**4 + 13824*alpha**3 - 73728*alpha**2*beta**2 + 7776*alpha**2 - 147456*alpha*beta**2 + 864*alpha - 65536*beta**4 - 69120*beta**2 + 27)
```

The first factor α⁴ + α³ + 4β² is positive, so root-count changes happen only on the zero set of the second factor (the pair-birth locus).

Substitution route: phi(t) = t P4(t)/(1+t^2)^2, Q = c t P4 - 4 Sigma Pi0 (1+t^2)^2, so Q > 0 iff c phi/4 > Sigma Pi0. Numerator of dφ/dt, factored:

```
-(t**4 + 6*t**2 - 3)*(c*t**2 + lambda*t**2 + lambda)
```

In u = t²: -c*u**3 - 6*c*u**2 + 3*c*u - lambda*u**3 - 7*lambda*u**2 - 3*lambda*u + 3*lambda (coefficients -c - lambda, -6*c - 7*lambda, 3*c - 3*lambda, 3*lambda).

**Reading (to be written up as a proof):** dφ/dt has the sign of −(t⁴ + 6t² − 3), whose only positive root is t*² = 2√3 − 3 for every λ, c. So φ rises on (0, t*) and falls after it; Q > 0 exactly where cφ(t)/4 > ΣΠ0, which is an interval or empty. Hence Q has 0 or 2 positive roots (1 only at tangency): the Hill n = 2 curve has no turning point or a minimum followed by a maximum, and the pair exists iff ΣΠ0 < cφ(t*)/4, with φ(t*) = t*·P₄(t*)/(1 + t*²)².
Check at λ = c = 1, Σ = 0.01: closed form Π0_pair = 31.4750497595392; numerical (T10.3) 31.4750497595392; relative difference 5.63e-17.

## T10.3 details

| family | sets | turning-point histogram | failures |
|---|---|---|---|
| bayes | 2000 | {'1': 906, '0': 1094} | 0 |
| misspec | 2000 | {'1': 892, '0': 1108} | 0 |
| capped | 2000 | {'0': 1092, '1': 908} | 0 |
| blind | 2000 | {'0': 2000} | 0 |
| hill | 10000 | {'2': 4868, '0': 5132} | 0 |

Hill by n: n = 1.5: {'2': 881, '0': 1119}; n = 2: {'0': 1039, '2': 961}; n = 3: {'0': 1045, '2': 955}; n = 4: {'0': 984, '2': 1016}; n = 8: {'2': 1055, '0': 945}. Exact root-count disagreements (n = 2): 0. Max position error vs the A3 roots: Bayesian 6.04e-31, misspecified 6.02e-31.

Targeted onset sets: bayes pass (140); misspec pass (140); capped pass (140); hill pass (20).

| n | Π0_pair (λ = c = 1, Σ = 0.01) | bisection vs double-root rel. diff |
|---|---|---|
| 1.5 | 30.2430947474 | 4.04e-12 |
| 2 | 31.4750497595 | 2.56e-12 |
| 3 | 37.8200022316 | 1.07e-12 |
| 4 | 44.1796834278 | 6.28e-13 |
| 8 | 62.7113145769 | 3.99e-12 |

Every n has exactly one transition (2 → 0 turning points) on Π0 ∈ [1e-4, 1e4].

Regression values: misspec (1.0, 0.05): pass; misspec (0.5, 0.1): pass; Hill n=2 Pi0=5.0: pass; Hill n=2 Pi0=26.0: pass; Hill n=2 window onset (M = F): pass.

## Exploratory census (record only)

| family | sets | turning-point histogram | kind sequences | ≥ 2 maxima |
|---|---|---|---|---|
| bayes2 | 2000 | {'0': 1094, '1': 899, '3': 7} | {'-': 1094, 'max': 899, 'max,min,max': 7} | 7 |
| hill2 | 2000 | {'2': 899, '0': 1038, '4': 63} | {'min,max': 899, '-': 1038, 'min,max,min,max': 63} | 63 |

Both semi-natural families produce curves with two maxima: two-channel Bayesian (max, min, max) in 7/2000 and two-channel Hill (min, max, min, max) in 63/2000, i.e. multi-window (and, for Hill, mixed multi-window) classes are reachable by sums of two natural stages. Examples (parameters in `results/t10_3.json`):

- bayes2: lam = 48.1, Sig = 0.0198, c1 = 0.2514, c2 = 74.41, Pi01 = 0.03213, Pi02 = 2460; kinds ['max', 'min', 'max']; values 0.0055879, 0.00071809, 0.0037822
- bayes2: lam = 16.76, Sig = 0.01805, c1 = 1.211, c2 = 91.64, Pi01 = 0.07771, Pi02 = 4638; kinds ['max', 'min', 'max']; values 0.13759, 0.0033698, 0.0050537
- hill2: lam = 29.45, Sig = 0.02795, c1 = 0.0308, c2 = 0.2386, Pi01 = 0.017, Pi02 = 47.99; kinds ['min', 'max', 'min', 'max']; values 0.00094908, 0.0012557, 0.00095046, 0.00095225
- hill2: lam = 0.5124, Sig = 0.6744, c1 = 2.845, c2 = 33.59, Pi01 = 0.03118, Pi02 = 5.978; kinds ['min', 'max', 'min', 'max']; values 1.3153, 17.513, 1.5379, 1.657

## T10.4 details

4868 Hill sets with two turning points (by n: {'1.5': 881, '2': 961, '3': 955, '4': 1016, '8': 1055}), 77,888 tolerances, both routes equal the prediction at every one. Band width (min(M,F) − max(m,H))/F: median 0.000498, min 4.43e-22, max 0.962. Lower band edge is m in 4868 sets and H in 0 (m > H always here); upper edge is M (M < F) in 787 sets (fraction 0.162) and F in 4081.

## T10.5 details

- Equal-height maxima: M2(1-1e-6): (0, 0, 2) / (0, 0, 2); M2: Empty / Empty; M2(1+1e-6): Empty / Empty
- Inflection vs smoothed: same turning points True, class mismatches 0 over 1000 tolerances, route disagreements 0.
- Plateau (capped, g = 2F): F(1-1e-6): lower ray / lower ray; F: Empty / Empty; F(1+1e-6): Empty / Empty (prediction: lower ray past c/g, Empty, Empty).
- Pair birth (Hill n = 2, Π0_pair = 31.4750497595392): turning points at Π0_pair(1 + 1e-6): 0.
- Narrow windows (relative width 1e-8): classifier correct in 20/20 curves (55 windows); a 10⁴-point log grid on x ∈ [−25, 25] hits 0 of them.

## T10.6 details

- Three routes: 4000 evaluations, max pairwise relative difference 1.01e-14, ARE converged in all (at most 10 ε-steps).
- Shape: core failures 0; max turning-point position error 8.81e-51; max symmetry error 4.87e-51; peak error 0.
- Classes: failing sets 0 (window with τ₋τ₊ = 1/λ² below P_max, Empty at and above).
- Relay: failing sets 0 (increasing, limits H_G and (Σ + G²v/a)/a, relay ≥ P).
- Regression: P(1) = 0.0083333333 (stated 0.0083333); P(0.3) = 0.0079077634 (stated 0.0079078); P(0.01) = 0.003455929 (stated 0.0034559); P(100) = 0.003455929 (stated 0.0034559)

| τ | filter | MC | SE | formula | z |
|---|---|---|---|---|---|
| 0.1 | relay | 0.00740118 | 4.4e-05 (0.60%) | 0.0073913 | +0.22 |
| 0.1 | optimal | 0.00680165 | 3.6e-05 (0.54%) | 0.0067813 | +0.56 |
| 1.0 | relay | 0.0100251 | 7.1e-05 (0.71%) | 0.01 | +0.35 |
| 1.0 | optimal | 0.00825511 | 5.6e-05 (0.67%) | 0.00833333 | -1.39 |
| 10.0 | relay | 0.0119292 | 4.6e-05 (0.39%) | 0.011875 | +1.18 |
| 10.0 | optimal | 0.00678939 | 1.9e-05 (0.28%) | 0.0067813 | +0.42 |

## T10.7 details

| sweep | curves | classifications | classes found | predicted set | flagged | persisting |
|---|---|---|---|---|---|---|
| Pi bayes | 1000 | 100,000 | {'Empty': 26919, 'All': 26753, 'window': 12629, 'lower ray': 33699} | All, Empty, lower ray, window | 0 | 0 |
| Pi misspec | 1000 | 100,000 | {'window': 18145, 'Empty': 43801, 'lower ray': 38054} | Empty, lower ray, window | 0 | 0 |
| Pi capped | 1000 | 100,000 | {'Empty': 25640, 'lower ray': 35331, 'All': 25719, 'window': 13310} | All, Empty, lower ray, window | 0 | 0 |
| Pi blind | 500 | 50,000 | {'lower ray': 22493, 'All': 27507} | All, lower ray | 0 | 0 |
| Pi hill | 2000 | 200,000 | {'All': 49370, 'lower ray': 63706, 'Empty': 49373, 'window': 26242, '(1, 0, 1)': 11309} | (1, 0, 1), All, Empty, lower ray, two rays, window | 3 | 0 |
| Pi0 bayes | 1000 | 100,000 | {'upper ray': 18670, 'Empty': 26725, 'All': 24916, 'lower ray': 17717, 'two rays': 11972} | All, Empty, lower ray, two rays, upper ray | 0 | 0 |
| c bayes | 1000 | 100,000 | {'upper ray': 32994, 'All': 27990, 'two rays': 39016} | All, two rays, upper ray | 0 | 0 |
| tau ZF relay | 625 | 62,500 | {'lower ray': 23193, 'All': 19722, 'Empty': 19585} | All, Empty, lower ray | 0 | 0 |
| tau ZF optimal | 625 | 62,500 | {'Empty': 34337, 'lower ray': 28163} | Empty, lower ray | 0 | 0 |
| tau var relay | 625 | 62,500 | {'Empty': 20322, 'All': 20425, 'upper ray': 21753} | All, Empty, upper ray | 0 | 0 |
| tau var optimal | 625 | 62,500 | {'Empty': 34501, 'window': 27999} | Empty, window | 0 | 0 |

Predicted classes that never occurred: Hill 'two rays' (needs m < H; in every Hill set here m > H) and none else.

## Figures

`figs/F1_realizability`, `F2_hill_family`, `F3_hill_phase`, `F4_peak_heights`, `F5_matched_variance` (PNG + PDF).
F4 at x = 100: Bayesian M/F = 9.2875, misspecified M/F = 17.5751, ratio 1.8923 (Paper 1's exploratory value: about 2).

![F1](figs/F1_realizability.png)

![F2](figs/F2_hill_family.png)

![F3](figs/F3_hill_phase.png)

![F4](figs/F4_peak_heights.png)

![F5](figs/F5_matched_variance.png)

## Provenance

Results come from separate invocations of the committed scripts (census first, then T10.4–T10.7 in sequence; T10.5 re-run after bug 2; T10.1, T10.2 and the figures re-run for logs). `run_t10.sh` reproduces everything in one go (about 1.6 h on 4 CPUs). Runtime per script (s): t10_symbolic 2, t10_symbolic_diag 1, t10_realize 90, t10_census 8232, t10_mixed 3064, t10_degenerate 74, t10_degenerate_diag 6, t10_tau 199, t10_tau_diag 1, t10_blind 2280, t10_figures 9.
