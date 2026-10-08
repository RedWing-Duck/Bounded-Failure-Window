# Pre-registration — Task 9: Stage 2 correlation-time sweep

Committed **before** any Task 9 script is written to disk or run. This file is not edited after
its commit. If a check fails, the failure stays recorded; it is diagnosed and attributed to the
document, the code or the criterion. Only genuine code bugs are fixed, each documented in
`t9/RESULTS_t9.md`. Classes are computed by root-finding on monotone pieces, never by grid
membership.

Source under test: `classification/Stage_2_Tau_Sweep_Results.md` (copied unchanged, committed
with this file). Conventions C1–C6 and Theorem 1.2 are from `Stage_0_1_Classification_Results.md`;
"approach from above" follows the C4 *definition* (σ² > L on the adjacent piece), not the C4
parenthetical, which Task 8 found reversed. Nothing in `verification/` is modified.

## Notation (as in the document)
a = λ + G; F = Σ/λ; relay σ²(τ) = (1/a)(Σ + G²/(2Π(1 + aτ))) (Lemma 2.1);
V_w = (Σ + G²/(2Π))/(λ + G); H_G = Σ/(λ + G); τ_R = (1/a)(G²/(2Π(aR² − Σ)) − 1);
τ_F = (1/a)(G/(2FΠ) − 1); G* = −λ + √(λ² + 2ΣΠ); σ*² = G*/Π;
h = 1/τ − λ; R_v = 2Σ + 1/(Πτ²); b = 4Στ + 2λ/Π; D = b² + 8Σ(1 − λτ)²/Π;
P(τ) = 4Σ/(Π(b + √D)) (Proposition 3.1);
τ*_R = (2λR² − 4Σ + √Δ)/(2λ²R²), Δ = 16Σ² − 16λΣR² + 8λ²(Σ − λR²)/Π;
V(τ) = inf_{G ≥ 0} σ²(G, τ).
Worked example: λ = c = 1, Σ = 0.01, Π = Π0 = 1, G = cΠ/(Π + Π0) = 0.5.

## Common conventions
- **4 s.f. match**: |computed − stated| ≤ 0.5·10^(floor(log10|stated|) − 3).
- **mp** = mpmath with `mp.dps = 60`. "Equal" for tolerances vs critical values in the
  classifier: relative difference ≤ 1e-40.
- **Random parameter sets**: λ, Σ, Π, G each log-uniform on [1e-3, 1e3] (six decades).
  Seeds: T9.2 `default_rng(9002)`; T9.4/T9.5 `default_rng(9004)` (the same 2,000 sets for both);
  T9.6 `default_rng(9006)`. T9.2 also draws λτ log-uniform on [1e-3, 1e3] (from the same RNG,
  after λ, Σ, Π, G).

## The classifier (`t9/t9_common.py`, all in mp)
Input: σ²(τ) and dσ²/dτ (analytic; for P the derivative is SymPy's `diff` of the Proposition 3.1
expression, lambdified to mpmath — not the document's dD/dτ formula).
1. Turning points: sign of the derivative at 200 log-spaced τ in [1e-6, 1e6]/λ; each sign change
   is refined by bisection in log10 τ to width 1e-32. Max if + → −, min if − → +.
2. Endpoint limits: L₋ = σ²(1e-80/λ), L₊ = σ²(1e80/λ), checked against τ = 1e∓70/λ to 1e-40
   relative (failures reported).
3. Pieces and failure set exactly as in Task 8 (PREREG_t8.md): from piece end values and
   directions; each crossing found by bisection in log10 τ on its monotone piece to width
   1e-32; adjacent parts join iff σ²(t) > R² strictly at the shared turning point.
4. Class (ℓ, u, k) or All (C5). Component endpoints are reported.

## T9.1 — Symbolic (`t9/t9_symbolic.py`); every item must reduce to exactly 0
Route (fixed, reported per item): (1) `sp.simplify(e) == 0`; else (2)
`sp.simplify(sp.together(sp.expand(e))) == 0`; else (3) if e contains one square root √X:
replace √X by a symbol u, take the numerator of `together`, and require its remainder modulo
u² − X (`sp.rem` in u) to simplify to 0. **No numeric fallback**: if all three fail, the item
FAILS and SymPy's simplified output is reported verbatim. All symbols positive.
- (a) **Lemma 2.1, independent route.** State (x, η): A = [[−a, G], [0, −1/τ]], noise intensities
  Q = diag(2Σ, 1/(Πτ²)) (independent). Solve A X + X Aᵀ + Q = 0 for symmetric X with
  `sp.solve` (3 unknowns). Check X₁₁ − σ²(τ) ≡ 0 and X₂₂ − 1/(2Πτ) ≡ 0. Also
  ∫₋∞^∞ C_η(u) du = 1/Π (`sp.integrate`) and the OU transform of C_η equals S_η.
- (b) σ² − F − G(λG/(2Π(1+aτ)) − Σ)/(λa) ≡ 0; λG/(2Π(1+aτ)) − Σ − (λ/2)(G/Π − 2F(1+aτ))/(1+aτ) ≡ 0
  (so the zero is G/Π = 2F(1+aτ)); dσ²/dτ + G²/(2Π(1+aτ)²) ≡ 0 (strictly decreasing for G > 0).
- (c) σ²(τ_R) − R² ≡ 0; σ²(τ_F) − F ≡ 0; τ_R|_{R²=F} − τ_F ≡ 0; aτ_R + 1 − G²/(2Π(aR² − Σ)) ≡ 0;
  a·τ_R·2Π(aR² − Σ) − 2Πa(V_w − R²) ≡ 0 (so for R² > H_G, i.e. aR² − Σ > 0, τ_R > 0 ⇔ R² < V_w).
- (d) **Riccati expansion.** With Ric = −2λP + 2Σ − (hP + 2Σ)²/R_v:
  −τ²·R_v·Ric − [(1 − λτ)²P² + bP − 2Σ/Π] ≡ 0. (The document says "multiplying by τ²"; the
  factor −R_v is needed; this is reported as a wording point if the check passes only with it.)
  Also τ²·(S² − QR_v) + 2Σ/Π ≡ 0 and τ²·(2hS + 2λR_v) − b ≡ 0 with S = Q = 2Σ.
- (e) Rationalized root: (1 − λτ)²P² + bP − 2Σ/Π ≡ 0 at P = 4Σ/(Π(b + √D)); and at λτ = 1,
  P − (2Σ/Π)/b ≡ 0.
- (f) dD/dτ − (32Σ²τ + 16Σλ²τ/Π) ≡ 0; dD/dτ − (8Σb − 16Σλ(1 − λτ)/Π) ≡ 0.
- (g) Limits (`sp.limit`): P(0⁺) − G*/Π ≡ 0; lim τP − 1/(Π(1 + √(1 + λ²/(2ΣΠ)))) ≡ 0;
  relay lim_{τ→0} − V_w ≡ 0 and lim_{τ→∞} − H_G ≡ 0.
- (h) τ*_R: the Proposition 3.1 quadratic with P = R², τ = τ*_R is ≡ 0 (since P is its unique
  positive root, this gives P(τ*_R) = R²). Supporting: the quadratic in τ has leading coefficient
  λ²R⁴, discriminant − R⁴Δ ≡ 0, and constant term R⁴ + 2λR²/Π − 2Σ/Π − (R² − G*/Π)(R² + (λ + √(λ²+2ΣΠ))/Π) ≡ 0
  (negative iff R² < σ*²).
- (i) τ → 0 in Lemma 2.1 gives Paper 1's white-noise formula (Σ + G²/(2Π))/(λ + G).
**T9.1 PASS** iff every item reduces to 0.

## T9.2 — Independent optimal filter (`t9/t9_filter.py`)
- **ARE route.** State (s, η): A = diag(−λ, −1/τ), Q = diag(2Σ, 1/(Πτ²)), C = [1, 1],
  measurement intensity ε. `scipy.linalg.solve_continuous_are(A.T, C.T, Q, [[ε]])` gives the
  filter covariance; P_ε = its (s, s) entry. ε ∈ {1e-4, 1e-6, 1e-8, 1e-10} (absolute, as
  specified). Extrapolation: the cubic polynomial in √ε through the four points, evaluated at 0.
  Compared with P(τ) from Proposition 3.1 evaluated in mp.
- Sets: 1,000 random sets (λ, Σ, Π from the ranges above; G unused; λτ log-uniform on
  [1e-3, 1e3]); the same 1,000 sets at τ = 1/λ exactly; the worked example at τ = 1.
  **PASS (ARE)** iff relative error ≤ 1e-5 in every one of the 2,001 cases.
- **Diagnostic only (not a pass criterion):** the same with scaled ε_k = 10^(−k)·ε₀,
  k = 4, 6, 8, 10, ε₀ = (2Σ + 1/(Πτ²))/(λ + 1/τ)², reported to separate "ε not small for these
  parameters" from a formula error if the primary check fails.
- **Wiener route.** At the worked example (λ = 1, Σ = 0.01, Π = 1) and τ ∈ {0.1, 1, 10}:
  S_y(ω) = 2Σ/(ω² + λ²) + (1/Π)/(1 + τ²ω²). The numerator polynomial in s = iω is factored
  numerically (`numpy.roots`), the minimum-phase factor S_y⁺ formed from its left-half-plane
  roots, [S_s/S_y⁻]₊ obtained from the partial-fraction residues at the left-half-plane poles
  (mp), and MMSE = Σ/λ − (1/2π)∫|[S_s/S_y⁻]₊(iω)|² dω by `mpmath.quad`. **PASS (Wiener)** iff
  relative error ≤ 1e-6 vs P(τ) at all three τ.
**T9.2 PASS** iff both parts pass.

## T9.3 — Worked-example values (`t9/t9_values.py`), 4 s.f.
V_w = 0.09000, H_G = 0.006667, τ_F = 16.00, σ²(1) = 0.04000, σ²(10) = 0.01188,
σ²(16) = 0.01000, σ*² = 0.009950, P(1) = 0.009804, P(10) = 0.006781. τ_F by bisection on
σ² − F (mp), the rest by direct evaluation (mp). Additionally (document, Section 3.4): V(1) ≈
0.00990, checked to 3 s.f. (|V − 0.00990| ≤ 0.5e-5), V by the T9.5 method.
**PASS** iff all ten match.

## T9.4 — Classification tables (`t9/t9_classify.py`)
For each of the 2,000 sets (seed 9004) and, additionally, for each set with G replaced by
2FΠ·(1 + δ), δ ∈ {−1e-6, 0, +1e-6} (8,000 parameter sets in all):
- **Proposition 2.3 (relay)**, tolerances: H_G/2; H_G; H_G(1 ± 1e-6); (H_G + V_w)/2;
  V_w; V_w(1 ± 1e-6); 1.5V_w; F.
  Predicted class from the table with the exact (mp) comparison of R² with H_G and V_w:
  R² ≤ H_G → All; H_G < R² < V_w → lower ray (0, τ_R); R² ≥ V_w → Empty. At R² = F:
  lower ray (0, τ_F) iff G > 2FΠ, else Empty.
- **Proposition 3.3 (optimal)**, tolerances: σ*²·1e-3; σ*²/2; σ*²; σ*²(1 ± 1e-6); 1.5σ*².
  Predicted: R² < σ*² → lower ray (0, τ*_R); R² ≥ σ*² → Empty.
- Endpoints: every lower ray's right end must match τ_R (relay; τ_F at R² = F) or τ*_R
  (optimal), evaluated in mp from the closed forms, to relative 1e-8.
**PASS** iff every class equals the prediction and every endpoint matches. Counts reported.

## T9.5 — Monotonicity and ordering (`t9/t9_order.py`)
Same 2,000 sets. 200 log-spaced τ in [1e-6, 1e6]/λ.
- Relay σ² and P: number of interior extrema (sign changes of the analytic derivative, refined
  by bisection) must be 0 in every set.
- P(τ) ≤ σ²_relay(τ) at every grid τ (mp; the set's own G).
- V(τ): float64; bracket on a 401-point grid of log10 G ∈ [log10 λ − 20, log10 λ + 20], then
  `minimize_scalar(method="bounded")` on the bracketing interval (xatol 1e-12 in log10 G);
  V = min(that minimum, 1/(2Πτ)) (the G → ∞ limit). Must be strictly decreasing along the grid
  and ≥ P (P converted to float64) at every grid τ.
- **Numerical result, not a pass/fail on the document:** min over all samples of V − P and of
  (V − P)/P, the τ and parameters where attained, and whether V − P ≤ 0 ever occurs.
**PASS** iff zero extrema, zero P > σ² violations, V strictly decreasing and V ≥ P everywhere.

## T9.6 — Adversarial (`t9/t9_adversarial.py`)
- (a) **Linear case.** Worked example and 100 random sets (seed 9006): λτ = 1 + k·1e-13,
  k = −10…10 (τ = that/λ in mp, then rounded to float64). float64 rationalized P vs mp P:
  PASS iff relative error ≤ 1e-12 everywhere. The naive root (−b + √(b² + 8Σ(1−λτ)²/Π))/(2(1−λτ)²)
  in float64 is reported (relative error; at exactly λτ = 1 it is 0/0), and scanned over
  |1 − λτ| = 10^(−16…−1) at the worked example: reported is the largest |1 − λτ| at which its
  relative error exceeds 1e-6 (informational).
- (b) **Extremes.** λ = Π = 1, Σ ∈ {1e-12, 1e12} (ΣΠ/λ² = 1e∓12), τ ∈ {1e-9, 1e9},
  G ∈ {1e-3, 1, 1e3}: float64 rationalized P and float64 Lemma 2.1 vs mp to relative 1e-12;
  the classifier's classes for the T9.4 tolerance lists equal the predictions. PASS iff all hold.
- (c) **Near-critical tolerances.** Worked example: R² = c(1 ± δ) for c ∈ {H_G, V_w, σ*²},
  δ ∈ {1e-6, 1e-9, 1e-12}: classes equal the predictions. PASS iff all match.
- (d) **G → 0⁺.** Worked example with G = 10^(−k), k = 1…12; R² ∈ {F(1 − 1e-3), F(1 − 1e-6),
  F, F(1 + 1e-6)}. Reported: the class at each (G, R²). PASS iff for every k ≥ 8 the classes are
  All, All, Empty, Empty (the G = 0 case).
- (e) **Monte Carlo.** Worked example, τ ∈ {0.1, 1, 10}; seed 9061. Euler–Maruyama with
  dt = min(τ/100, 2e-3); 2,000 independent trajectories; burn-in 10·max(τ, 1), averaging window
  20·max(τ, 1). Relay: dx = (−a x + Gη)dt + √(2Σ dt)·ξ. Optimal (differenced) filter: s, η as
  above, z dt = Δy + y dt/τ, dŝ = −λŝ dt + K(z dt − hŝ dt), K = (hP + 2Σ)/R_v, P from
  Proposition 3.1. Estimate = mean over trajectories of each trajectory's time-average of x²
  (resp. (s − ŝ)²); SE = std/√2000. **PASS** iff in all six cases SE ≤ 2% of the formula and
  |estimate − formula| ≤ 3 SE.
**T9.6 PASS** iff (a)–(e) pass.

## Figure (`t9/t9_figure.py`)
`t9/fig_t9_tau.png`, 300 dpi: relay σ²(τ) (G = 0.5) and P(τ) at the worked example against
log τ; horizontal lines F, H_G, σ*² (and V_w). Not a pass criterion.

## Report
`t9/RESULTS_t9.md`: one row per check with pass/fail, counts, runtime, this file's commit hash
and the code commit hash, and every bug, wording or formula error found, stating whether any
class changes. `t9/run_t9.sh` reproduces everything.

## Notes made before any code (from reading the document)
- Proposition 2.2's proof says the approach directions "follow from C4 for a decreasing
  function". The stated directions (V_w from below, H_G from above) agree with the C4
  definition but not with the C4 parenthetical (reversed, Task 8).
- Proposition 3.1's proof says "multiplying by τ²"; the Riccati right-hand side must be
  multiplied by −τ²R_v to give the quadratic. Checked in T9.1(d).
