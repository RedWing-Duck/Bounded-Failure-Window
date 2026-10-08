# Pre-registration — Task 10: Stage 3 falsification and completeness

Committed **before** any Task 10 script is written to disk or run. Not edited after its commit.
Failures stay recorded; each is diagnosed post hoc in a separate `*_diag.py` and attributed to the
plan, the code or the criterion. Only genuine code bugs are fixed, each documented in
`t10/RESULTS_t10.md`. Sources under test: `classification/Stage_3_Plan.md` and the task prompt
`classification/Task_10_Stage3_Prompt.md` (both copied unchanged and committed with this file).
"Approach from above" follows the C4 *definition* (Task 8 found the C4 parenthetical reversed).

## Notation
σ²(G, Π) = (Σ + G²/(2Π))/(λ + G); F = Σ/λ; G* = −λ + √(λ² + 2ΣΠ); σ*² = G*/Π; H = Σ/(λ + G∞).
Elasticity ε = ΠG′/G; N = ε(G² + 2λG − 2ΣΠ) − G(λ + G) (Plan A3). x = log10 of the swept variable.
Families along Π: Bayesian cΠ/(Π + Π0) (κ = cλ/(ΣΠ0)); misspecified Kalman −λ′ + √(λ′² + 2Σ′Π)
(F′ = Σ′/λ′, r = Σ/Σ′; computed as 2Σ′Π/(λ′ + √(λ′² + 2Σ′Π))); capped min(gΠ, c); precision-blind
G0; Hill cΠⁿ/(Πⁿ + Π0ⁿ), t = Π/Π0. Matched-variance τ: Var η = v, C_η(u) = v e^{−|u|/τ},
A(τ) = (1 − λτ)²/τ, B = 4(Σ + λv), P = 8Σv/(B + √(B² + 16ΣvA)), P_max = Σv/(Σ + λv), relay
σ²_τ = (Σ + G²vτ/(1 + aτ))/a, a = λ + G.

## The T10 method (mandatory everywhere unless a check says otherwise)
- **Precision.** mpmath, `mp.dps = 50` (60 for re-runs of flagged cases, 100 for the regularized ARE).
- **Turning points.** Sign of the analytic derivative numerator (N for Π sweeps; the analytic
  derivative for Π0, c and τ sweeps) on a log grid of 12 points per decade over x ∈ [−25, 25]
  (τ sweeps: shifted by −log10 λ), **united with the construction breakpoints** of any constructed
  curve (nodes, kinks, envelope crossings). N is treated as 0 when |N| ≤ 1e-40·G(λ + G) (Π sweeps)
  or |derivative| ≤ 1e-40·|σ²|/θ (other sweeps); zero points are skipped. **Adaptive step:** at each
  grid point where |N| has a local minimum and the three neighbouring signs agree, a golden-section
  search for the extremum of sign·N on the two adjacent intervals (to width 1e-30 in x); if it crosses
  zero (beyond the zero tolerance), the two roots are bracketed and refined. Every sign change is
  refined by bisection in x to width 1e-30. Max if + → −, min if − → +.
- **Limits.** σ² at x = ∓80 (shifted), checked against x = ∓70. **Zero limits use absolute
  criteria**: |L| ≤ 1e-30 counts as 0; L ≥ 1e30 counts as +∞. Finite limits must agree between ∓80
  and ∓70 to 1e-30 relative.
- **`classify.py` (shared).** Input: turning points (positions, values, kinds), endpoint limits,
  piece directions (approach directions follow), and σ². Two independent routes:
  (i) **Theorem 1.2**: class from the ordered sequence (L₋, values, L₊) and piece directions only, by
  comparisons (no root-finding); (ii) **direct**: on each monotone piece, bisection of σ² − R² where
  its sign differs at the piece ends; the sorted roots, plus turning points with σ²(t) = R², split the
  domain; each sub-interval is in the failure set iff σ² − R² > 1e-40·R² at its log-midpoint (direct
  evaluation). "R² equals a value" means relative difference ≤ 1e-40. The class from (ii) and its
  component endpoints are reported; **(i) ≠ (ii) is a failure** wherever a class is reported.

## T10.1 — Symbolic (`t10_symbolic.py`), every item exactly 0, no numeric fallback
Route per item (as Task 9): `simplify`; else `simplify(together(expand))`; else single-√
remainder. Items:
- (a) Elasticity: with G = G(Π) a SymPy Function, dσ²/dΠ − G·N/(2Π²(λ+G)²) ≡ 0.
- (b) Bayesian: with G as the variable, Π = Π0G/(c − G), ε = 1 − G/c (checked: Π G′/G with
  G = cΠ/(Π+Π0) equals 1 − G/c): c·N + G(G² + 2λG + 2ΣΠ0 − λc) ≡ 0.
- (c) Misspecified: Π = (G² + 2λ′G)/(2Σ′), ε = (G + 2λ′)/(2(G + λ′)) (checked from G(Π)):
  2(G + λ′)N/G + [(1+r)G² + 4rλ′G − 2λλ′ + 4rλ′²] ≡ 0; constant term + 2λλ′(1 − 2F/F′) ≡ 0
  (so, with positive leading and linear coefficients, one positive root iff F′ > 2F).
- (d) Capped linear branch: d/dΠ σ²(gΠ, Π) − g(gλ/2 − Σ)/(λ + gΠ)² ≡ 0; and σ²(2FΠ, Π) − F ≡ 0.
- (e) Hill n = 2: N − t·Q(t)/(1 + t²)³ ≡ 0 (Π = Π0t), i.e. the positive factor is t/(1+t²)³;
  Q − [c t(−(λ+c)t⁴ + (c+2λ)t² + 3λ) − 4ΣΠ0(1+t²)²] ≡ 0.
- (f) Realizability: σ²(G₊, Π) − v ≡ 0; disc − Π(Πv² + 2λv − 2Σ) ≡ 0;
  Πv² + 2λv − 2Σ − Π(v − σ*²)(v + (λ + √(λ²+2ΣΠ))/Π) ≡ 0; Πσ*² − G* ≡ 0 (so G₊ ≥ Πv ≥ G* when
  v ≥ σ*²).
- (g) Forced ray: σ*²(π_R) − R² ≡ 0 at π_R = 2λ(F − R²)/R⁴ (for 0 < R² < F).
- (h) Matched variance: −τR_v·[−2λP + 2Σ − (hP + 2Σ)²/R_v] − [AP² + 4(Σ+λv)P − 4Σv] ≡ 0 with
  h = 1/τ − λ, R_v = 2Σ + 2v/τ (factor −τR_v); A(τ) − A(1/(λ²τ)) ≡ 0; P|_{A=0} − Σv/(Σ+λv) ≡ 0;
  τ₋τ₊ − 1/λ² ≡ 0 (roots of P = R², i.e. λ²τ² − (2λ + A_R)τ + 1 = 0, A_R = (4Σv − BR²)/R⁴);
  Lyapunov X₁₁ − σ²_τ ≡ 0 for A = [[−a, G], [0, −1/τ]], Q = diag(2Σ, 2v/τ); X₂₂ − v ≡ 0;
  rationalized P satisfies the quadratic.
**PASS** iff all items reduce to 0.

## T10.2 — Realizability (`t10_realize.py`), λ = 1, Σ = 0.01
- **Construction.** v = max(v₀, w) with v₀ = σ*² + ½σ*²(F − σ*²)/F (strictly between σ*² and F,
  decreasing, → F from below at 0, → 0 at ∞) and w piecewise linear in x with nodes at x = 6, 7, …:
  hi = 2R², lo = R²/2; node list ([hi] if ℓ) + [lo] + [hi, lo]·k + ([hi] if u); left tail for x < 6:
  ℓ = 1 → w increases towards 3R² as x → −∞ (w = 3R² − (3R² − w(6))e^{x−6}); ℓ = 0 → w = w(6)e^{x−6}
  → 0; right tail likewise (u = 1 → 3R², u = 0 → 0). "All": nodes [2R², 2.5R², 2R²], both tails → 3R².
  G = G₊(v, Π). Targets: k = 0…5, all (ℓ, u), and All, at R² ∈ {0.5F, 0.99F, F, 1.01F, 3F}; targets
  with ℓ = 0 at R² < F go to the forbidden test.
- **Checks per realized target:** G ≥ 0 at every grid point and breakpoint; G continuous
  (|G(b(1+1e-30)) − G(b(1−1e-30))| ≤ 1e-20·max(G(b), 1e-30) at every breakpoint b); |σ²(G, Π) − v| ≤
  1e-40·v at every grid point; both routes return the target class.
  **PASS (every class)** iff all ℓ = 1 targets and All are realized at R² ∈ {0.5F, 0.99F} and all targets
  at R² ∈ {F, 1.01F, 3F}: 2 × 13 + 3 × 25 = 101 constructions.
- **Forbidden.** For each ℓ = 0 target at R² ∈ {0.5F, 0.99F}, the unclipped w (v = w, no max with
  v₀) has v ≤ R² near 0; check the discriminant Πv² + 2λv − 2Σ < 0 at Π = π_R/2 (and that π_R/2 lies
  where v ≤ R²). **PASS** iff 100% blocked.
- **A1.3 (as specified).** Bayesian curve v_B at κ = 1.5 (Π0 = cλ/(κΣ), c = 1), plus k = 1…5 Gaussian
  bumps 0.5F·exp(−(x − x_j)²/(2·0.15²)), x_j = −5, −4, …; inverted with **G₊** (the plan's inverse).
  Checks: G(1e-12) < 1e-9 and G(1e-12)²/1e-12 < 1e-9; |G(1e12)/G(1e11) − 1| ≤ 1e-6; k windows at
  R² = 1.25F (both routes). **PASS** iff all five k pass.
  *A priori note (from algebra, before any run):* G₊ ≥ Πv and v → H > 0, so G₊ → ∞ like 2HΠ; the
  convergence check is expected to **fail**. The plan's A1.3 needs the lower branch at large Π.
- **A1.3 supplementary (branch-following, pre-registered, reported separately).** Same, but with
  compactly supported C∞ bumps 0.5F·exp(1 − 1/(1 − ((x − x_j)/0.4)²)) and G = G₊ for Π ≤ Π_c, G = G₋ =
  Πv − √(…) for Π > Π_c, where Π_c solves G_B(Π) = G*(Π) (v_B = σ*² there, so the branches meet).
  Checks: as above plus |G₊(Π_c) − G₋(Π_c)| ≤ 1e-30·G*(Π_c) and G₋ ≥ 0 on Π > Π_c.

## T10.3 — Turning-point census (`t10_census.py`), seed 10003
Parameters log-uniform on [1e-2, 1e2] (four decades). 2,000 sets per family (Hill: 2,000 per n ∈
{1.5, 2, 3, 4, 8}). Targeted sets: 20 random base sets each at κ = 2(1+δ), F′/F = 2(1+δ), g = 2F(1+δ),
δ ∈ {0, ±1e-3, ±1e-6, ±1e-9}; Hill at λ = c = 1, Σ = 0.01, Π0 = Π0_pair(n)(1 ± δ), δ ∈ {1e-3, 1e-6}.
- **Bayesian PASS:** 0 TPs iff κ ≤ 2; exactly one max iff κ > 2, at Π = Π0G_r/(c − G_r),
  G_r = −λ + √(λ² + λc − 2ΣΠ0), to relative 1e-10.
- **Misspecified PASS:** 0 iff F′ ≤ 2F; one max iff F′ > 2F at the positive root of the quadratic
  (Π = (G² + 2λ′G)/(2Σ′)) to 1e-10; regression (λ = 1, Σ = 0.01): (λ′, Σ′) = (1, 0.05): Π = 19.610,
  value 0.01351; (0.5, 0.1): Π = 7.4380, value 0.03025 (half a unit in the last stated digit).
- **Capped PASS:** g < 2F: 0 TPs and derivative < 0 on every grid point; g > 2F: exactly one max at
  c/g (1e-10); g = 2F: |σ² − F| ≤ 1e-48·F at every grid point with Π ≤ c/g, and 0 TPs.
- **Precision-blind PASS:** 0 TPs, derivative < 0 everywhere on the grid, L₋ = +∞.
- **Hill PASS:** no set has 1, 3 or ≥ 4 TPs; every 2-TP set is (min, max) in that order. Cross-check
  for n = 2: the number of positive roots of Q(t) by `sympy.Poly.count_roots(0, oo)` on exact rationals
  of the float parameters must equal the method's count (a disagreement is a census failure).
  Regression (n = 2, λ = c = 1, Σ = 0.01): Π0 = 5: min 0.3348 (0.0099852), max 6.9817 (0.024858);
  Π0 = 26: min 10.723 (0.0095911), max 25.283 (0.0098730) (half a unit in the last digit).
  Window onset (n = 2): the Π0 where M = F, by bisection on M(Π0) − F, equals cλ/(4Σ) = 25 to 1e-8.
- **Reported, not pass/fail:** Π0_pair(n) for each n (double-root system N = ∂N/∂Π = 0 by `findroot`,
  cross-checked by bisection on the TP count to 1e-10); all transitions of the TP count found by
  scanning Π0 ∈ [1e-4, 1e4]. Hill proof support: discriminant of Q in α = λ/c, β = ΣΠ0/c² (factored),
  and the attempt via the plan's substitution Q = c t·P₄(t) − 4ΣΠ0(1+t²)²: the numerator of
  d/dt[t P₄/(1+t²)²] and its Descartes sign count in u = t².
- **Exploratory census (record only):** two-channel Bayesian and two-channel Hill (n = 2 each),
  Π02/Π01 log-uniform on [10, 1e6], other parameters as above, 2,000 sets each: TP histogram, sets
  with ≥ 2 maxima.
**T10.3 PASS** iff the Bayesian, misspecified, capped, precision-blind and Hill criteria (including
regression values and the n = 2 cross-check) all pass.

## T10.4 — Mixed class in the Hill family (`t10_mixed.py`)
All T10.3 Hill sets with 2 TPs (min m, max M), lo = max(m, H), hi = min(M, F). Tolerances: 10
interior points lo + (i + ½)(hi − lo)/10; lo and hi exactly; lo(1 ± 1e-6), hi(1 ± 1e-6).
Predicted class (explicit enumeration for the sequence F(below) → m → M → H(above)): lower ray iff
R² < F; upper ray iff R² ≤ H; the hump exists iff R² < M; it joins the lower ray iff R² < m and the
upper ray iff R² ≤ H; All iff everything joins; k = 1 iff the hump exists and joins neither.
(Interior: (1, 0, 1).) **PASS** iff both routes equal the prediction at every tolerance. Reported:
relative band width (hi − lo)/F (median, min, max) and the fraction of 2-TP sets with M < F.

## T10.5 — Degeneracies (`t10_degenerate.py`), seed 10005, λ = 1, Σ = 0.01
- **Equal-height maxima:** A1 construction with nodes [lo, M₂, lo, M₂, lo] (M₂ = 2F, lo = 0.25F),
  tails → 0 (ℓ = u = 0). PASS iff class (0, 0, 2) at M₂(1 − 1e-6) and Empty at M₂ and M₂(1 + 1e-6).
- **Inflection:** A1 curve with nodes x = 6 (lo), 7 (peak P = 3F), 8 (A + B), cubic A − B(x − 9)³ on
  [8, 10] (A = 1.5F, B = 0.5F; stationary inflection at x = 9), 11 (lo); smoothed copy with the cubic
  replaced by A − B[(x−9)³ + 0.1(x−9)]/1.1. PASS iff both have the same TP list (up to 1e-20 in value)
  and identical classes (both routes) at 1,000 tolerances log-uniform on [½·min, 2·max] of their
  finite critical values.
- **Plateau:** capped, λ = c = 1, Σ = 0.01, g = 2F. Predicted: R² = F(1 − 1e-6): lower ray (1, 0, 0)
  with right end > c/g; R² = F: Empty; R² = F(1 + 1e-6): Empty. PASS iff both routes agree with this.
- **Pair birth:** Hill n = 2 at λ = c = 1, Σ = 0.01; Π0 = Π0_pair(1 − δ), δ = 10^(−6…−12) (7 values,
  the side where the pair exists; at Π0_pair(1 + 1e-6) the TP count is reported). M − m and the TP
  separation |x_M − x_m| from the T10 method. PASS iff M − m → 0 monotonically in δ and the
  least-squares slope of log(M − m) vs log δ lies in [0.4, 0.6].
  *A priori note:* at a fold, positions separate like δ^{1/2} but the values like δ^{3/2}; the
  slope for M − m is expected near 1.5, so this criterion is expected to **fail**. The slope of
  |x_M − x_m| (expected 0.5) is reported alongside.
- **Narrow windows:** 20 A1 curves (seed 10005), each with k ∈ {1…5} spikes of relative width 1e-8 in
  Π (triangular in x, half-width ½·log10(1 + 1e-8), peak 2R², R² = 1.01F, base lo = R²/2) at random
  x ∈ [6, 15] at least 0.5 apart. PASS iff the root-finding classifier returns k windows in all 20 (both
  routes) with each component width within [0.5, 2]×1e-8 relative. Reported: windows hit by a
  10⁴-point log grid on x ∈ [−25, 25] (grid membership, for comparison only).
**T10.5 PASS** iff all five sub-checks pass.

## T10.6 — Optimal filter along matched-variance τ (`t10_tau.py`), seed 10006
1,000 sets, λ, Σ, v log-uniform on [1e-2, 1e2]; per set τ: one random λτ log-uniform on [1e-4, 1e4],
and λτ = 1, 1 − 1e-12, 1 + 1e-12 (4,000 evaluations).
- **Three routes for P:** (1) rationalized Plan quadratic (mp); (2) regularized ARE, y = s + η + √ε w,
  state (s, η), A = diag(−λ, −1/τ), Q = diag(2Σ, 2v/τ), C = [1, 1], solved in mp (dps 100) by the stable
  Hamiltonian subspace at ε_j = ε₀·10^(−4j), j = 2, 3, …, ε₀ = (2Σ + 2v/τ)/(λ + 1/τ)², until the
  relative change between consecutive j is < 1e-12 (at most j = 25; non-convergence is a failure);
  (3) closed-form causal Wiener: S_y = k²(β² − s²)/((λ² − s²)(1 − τ²s²)), k² = 2Στ² + 2vτ, β² =
  (2Σ + 2vτλ²)/k², causal part A_W/(s + λ), A_W = 2Σ(1 + λτ)/(k(β + λ)), MMSE = Σ/λ − A_W²/(2λ).
  **PASS** iff the three agree pairwise to relative 1e-8 in all 4,000 evaluations.
- **Shape PASS:** analytic dP/dτ (SymPy) has exactly one sign change (+ → −), at τ = 1/λ to relative
  1e-10; P(1/λ) = P_max to 1e-40 relative; P(τ) = P(1/(λ²τ)) to 1e-12 at the random τ; zero limits:
  P < 1e-6·P_max at λτ = 1e∓12.
  *A priori note:* at λτ = 1e-12, P ≈ 2e-6·√(Σv/λ), so P/P_max ≈ 2e-6(Σ + λv)/√(λΣv) ≥ 4e-6 for all
  parameters: the zero-limit criterion as specified is expected to **fail** in every set.
  Supplementary (reported, not part of the verdict): P < 1e-6·P_max at λτ = 1e∓24, and P(λτ = 10^∓2j)
  falls like (λτ)^{±1/2} (log-slope within 1e-3 of ±0.5 at j = 6).
- **Classes PASS:** at R² ∈ {1e-3·P_max, 0.5P_max, 0.9P_max, P_max(1 − 1e-6)}: window (0, 0, 1) with
  τ₋τ₊ = 1/λ² to 1e-10 (route (ii) endpoints); at R² ∈ {P_max, P_max(1 + 1e-6), 1.5P_max}: Empty.
  Both routes.
- **Relay PASS** (G log-uniform on [1e-2, 1e2] per set): 0 TPs and derivative > 0 at every grid point;
  L₋ = H_G and L₊ = (Σ + G²v/a)/a to 1e-30; relay ≥ P at 200 log-spaced λτ ∈ [1e-6, 1e6].
- **Monte Carlo PASS** (λ = 1, Σ = 0.01, v = 0.05, G = 0.5, τ ∈ {0.1, 1, 10}, seed 10061): T9 design
  (Euler–Maruyama, dt = min(τ/100, 2e-3), 2,000 trajectories, burn-in 10·max(τ, 1), window
  20·max(τ, 1)), dη = −η dt/τ + √(2v dt/τ)ξ, differenced filter with R_v = 2Σ + 2v/τ; all six
  (2 filters × 3 τ) with SE ≤ 2% and |estimate − formula| ≤ 3 SE.
- **Regression PASS:** v = 0.05, λ = 1, Σ = 0.01: P(1) = 0.0083333, P(0.3) = 0.0079078,
  P(0.01) = P(100) = 0.0034559 (half a unit in the last digit).
**T10.6 PASS** iff all six parts pass.

## T10.7 — Blind search (`t10_blind.py`), seed 10007
10,000 curves × 100 tolerances = 10⁶ classifications. Curves (parameters log-uniform on [1e-2, 1e2]):
Π-sweeps — Bayesian 1,000, misspecified 1,000, capped 1,000, precision-blind 500, Hill 2,000 (400 per
n); Bayesian Π0-sweep 1,000 and c-sweep 1,000; τ, matched zero-frequency power (Stage 2) relay 625 and
optimal 625; τ, matched variance relay 625 and optimal 625. Tolerances: 50 log-uniform on
[½·min, 2·max] of the curve's finite positive critical values; 50 near-critical: a random critical
value c, R² = c (10 of 50) or c(1 + u·1e-6), u ~ U(−1, 1).
Predicted class sets: Π Bayesian {All, lower ray, window, Empty}; Π misspecified {lower ray, window,
Empty}; Π capped {All, lower ray, window, Empty}; Π precision-blind {All, lower ray}; Π Hill {All,
lower ray, (1,0,1), two rays, window, Empty}; Π0 Bayesian {All, two rays, upper ray, lower ray, Empty};
c Bayesian {All, two rays, upper ray}; τ matched-ZF relay {All, lower ray, Empty}; τ matched-ZF
optimal {lower ray, Empty}; τ matched-variance relay {All, upper ray, Empty}; τ matched-variance
optimal {window, Empty}.
Method: TPs by the T10 method (mp, dps 50, cached per curve); route (i) as above; **route (ii) in
float64 for speed** (brentq in x, xtol 1e-14; equality at 1e-12 relative). Every case where the class
is outside the predicted set or (i) ≠ (ii) is re-run with both routes in mp (dps 60); only cases that
persist are counted. **PASS** iff 0 persisting out-of-set classes and 0 persisting disagreements.

## Figures (`t10/figs/`, PNG + PDF; palette #2a78d6, #eb6834, #1baf7a, #4a3aa7 with line styles)
F1 realizability (σ*² envelope with the forbidden region shaded, F, a 3-window curve, failure set
shaded at 1.25F; inset: forced lower ray (0, π_R) at R² = 0.9F); F2 Hill n = 2, Π0 ∈ {5, 20, 25, 26,
40}, inset near F with m, M and the band; F3 Hill phase diagram (n = 2, λ = c = 1; Π0 vs Σ log–log,
regions from the positive-root count of Q(t), colour log10 band width); F4 peak M/F vs κ (Bayesian) and
F′/F (misspecified, λ′ = 1), x ∈ (2, 100], value and ratio annotated at x = 100; F5 matched-variance P(τ)
with window shaded at 0.8P_max and τ = 1/λ marked, relay at G = 0.5.

## Report
`t10/RESULTS_t10.md` by `make_results_t10.py` from `t10/results/*.json`: one row per check with
verdict, counts, worst errors, runtime; this file's hash and the code hash; diagnosis sections; plan
wording/formula errors; Hill proof-support output verbatim; exploratory census tables; plain statements
on whether any plan prediction is falsified and whether any out-of-set class was found.

## Notes made before any code (from algebra by hand; to be confirmed or refuted by the run)
1. Plan A4 calls Q(t) a "sextic"; Q is a quintic (t·Q is the sextic numerator of N(1+t²)³).
2. A1.3: with the plan's G₊ inverse, G₊ ≥ Πv → ∞ whenever v → H > 0; Paper 1 regularity
   (G → G∞ finite) needs the lower branch G₋ at large Π, joined to G₊ at a point where v touches σ*².
3. Pair birth: the task's O(√distance) for M − m conflicts with a fold (positions ~ δ^{1/2}, values
   ~ δ^{3/2}).
4. The T10.6 absolute zero-limit criterion at λτ = 1e∓12 cannot be met (P/P_max ≥ 4e-6 there).
5. Hill n = 2 proof route: Q > 0 ⇔ φ(t) = c t P₄(t)/(4(1+t²)²) > ΣΠ0; if φ is unimodal on t > 0,
   Q has at most two positive roots. To be checked symbolically in T10.3 proof support.
