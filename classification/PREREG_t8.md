# Pre-registration — Task 8: Stage 0–1 classification checks

Committed **before** any Task 8 script is written to disk or run. This file is not edited
after its commit. A criterion that turns out to be badly posed is reported as such, not
changed. Only genuine bugs are fixed, and each fix is documented in the report. If a stated
result is wrong, what is actually found is reported; agreement is not forced. If an identity
is not confirmed, what SymPy actually returns is reported verbatim.

Source under test: `classification/Stage_0_1_Classification_Results.md` (copied unchanged,
committed together with this file). Nothing in `verification/` is modified.

## Notation
λ, Σ > 0; F = Σ/λ; σ²(G, Π) = (Σ + G²/(2Π)) / (λ + G);
G*(Π) = −λ + √(λ² + 2ΣΠ); σ*²(Π) = G*/Π; s = √(λ² + 2ΣΠ).
Prior sweep: G = cΠ/(Π + Π0), θ = Π0 ∈ (0, ∞), fixed Π, c.
V_c = σ²(c, Π); Π_A = c(c + 2λ)/(2Σ); Π_B = cλ/(2Σ).
Coupling sweep: K = Π/(Π + Π0), G = cK, θ = c ∈ (0, ∞), fixed Π, Π0.
Paper 1 precision sweep: θ = Π, G = cΠ/(Π + Π0), fixed Π0; H = Σ/(λ + c).
Worked example: λ = c = 1, Σ = 0.01 (F = 0.01, H = 0.005; Paper 1 example Π0 = 1, κ = 100).

## Conventions used by every criterion
- **Symbolic identity.** PASS if `sympy.simplify(lhs − rhs) == 0` (symbols declared positive).
  Otherwise the identity is evaluated at 20 random rational points (each positive symbol
  log-uniform in [1e-2, 1e2], `numpy.random.default_rng(8001)`, floats converted to exact
  rationals, `evalf(50)`); it passes if |lhs − rhs| ≤ 1e-12·max(|lhs|, |rhs|, 1e-300), labelled
  "PASS (numeric only)". Which route was used is always reported, and the non-zero SymPy
  output is printed verbatim.
- **Sign / inequality claims** are proved by an identity that writes the quantity as a product
  or quotient of factors each of which SymPy's assumption system reports positive (or
  negative) for positive symbols. If SymPy cannot decide a factor's sign, that is reported, and
  the claim is checked at the same 20 random points (labelled numeric only).
- **"Match to n significant figures"**: |computed − stated| ≤ 0.5·10^(floor(log10|stated|) − n + 1).
  Stated values are taken from the task specification (4 s.f.); "50" and "150" are taken as
  50.00 and 150.0.

## The classifier (shared by T8.1(h), T8.3–T8.5)
Input: σ²(θ) on (0, ∞) and its derivative dσ²/dθ (supplied analytically by the chain rule
∂σ²/∂G · dG/dθ, with ∂σ²/∂G the Lemma 3.1 expression that T8.1(a) verifies; for T8.5, the
exact derivative of the piecewise-linear function). All root-finding is done in x = log10 θ.
1. **Turning points.** Sign of the derivative on a log grid of 40 points per decade over
   θ ∈ [1e-60, 1e60] (4801 points); grid points where the derivative evaluates to exactly 0
   are skipped; each sign change between consecutive non-zero points is refined with
   `scipy.optimize.brentq` (xtol 1e-14 in x). Max if + → −, min if − → +.
2. **Endpoint limits.** L₋ = σ²(1e-250), L₊ = σ²(1e250); a non-finite value or one above 1e200
   is +∞. Sanity check: σ²(1e-200) and σ²(1e200) must agree with them to 1e-9 relative (or
   also be +∞); any disagreement is reported.
3. **Pieces.** Each monotone piece's direction is the derivative sign on its grid points; its
   end values are the limits / turning-point values. The approach direction at an end follows
   from the direction of the adjacent piece (C4).
4. **Failure set for a tolerance R².** Per piece, from its end values only: whole piece if
   R² < (smaller end value), or R² equal to it (open piece, strict inequality); empty if
   R² ≥ (larger end value); otherwise a one-sided sub-piece adjacent to the larger end, whose
   end is found by brentq on σ² − R² in x on that piece (unbounded pieces bracketed out to
   1e∓250). Two adjacent pieces' parts join iff both reach the shared turning point and
   σ²(t) > R² strictly. "R² equal to a value v" means |R² − v| ≤ 1e-12·|v| (needed because the
   classifier's own limits and turning values are floating point); ±1e-6 relative offsets
   are far outside this band.
5. **Class** (ℓ, u, k) as in C5, or "All" when one component reaches both ends.
No class is ever decided by whether grid points lie in the failure set.

## T8.1 — Analytic (SymPy) — `t8_symbolic.py`
- (a) ∂σ²/∂G − (G² + 2λG − 2ΣΠ)/(2Π(λ+G)²) ≡ 0.
- (b) The roots of G² + 2λG − 2ΣΠ (`sympy.solve`) are exactly {−λ + s, −λ − s}; −λ − s is
  negative; −λ + s − 2ΣΠ/(λ + s) ≡ 0 with 2ΣΠ/(λ + s) positive, so exactly one positive root,
  equal to G*. σ²(G*, Π) − G*/Π ≡ 0. F − G*/Π − 2Σ²Π/(λ(λ + s)²) ≡ 0 with the right-hand side
  positive, so G*/Π < F for all positive λ, Σ, Π.
- (c) σ²(G, Π) − F − G(λG/(2Π) − Σ)/(λ(λ+G)) ≡ 0; `solve` of the numerator in G gives exactly
  {0, 2FΠ}.
- (d) G(Π0*) − G* ≡ 0 at Π0* = Π(c/G* − 1);
  c − G* − 2Σ(Π_A − Π)/(c + λ + s) ≡ 0 (denominator positive, so c > G* ⇔ Π < Π_A);
  c − 2FΠ − 2F(Π_B − Π) ≡ 0 (so c > 2FΠ ⇔ Π < Π_B);
  Π_A − Π_B − c(c + λ)/(2Σ) ≡ 0 with the right-hand side positive (Π_B < Π_A);
  V_c − F − c(c − 2FΠ)/(2Π(λ + c)) ≡ 0 (so V_c > F ⇔ c > 2FΠ).
- (e) c*K − G* ≡ 0 and c* − (Π+Π0)(s − λ)/Π ≡ 0 at c* = G*/K; c_F − 2F(Π+Π0) ≡ 0 at
  c_F = 2FΠ/K, and σ²(c_F K, Π) − F ≡ 0.
- (f) `sympy.limit`: prior sweep Π0 → 0⁺ gives V_c and Π0 → ∞ gives F; coupling sweep
  c → 0⁺ gives F and c → ∞ gives ∞.
- (g) Prior sweep: lim_{Π0→∞} Π0²·dσ²/dΠ0 − cΠΣ/λ² ≡ 0 (positive, so dσ²/dΠ0 > 0 near ∞:
  F from below); lim_{Π0→0} dσ²/dΠ0 + c(c² + 2λc − 2ΣΠ)/(2Π²(λ+c)²) ≡ 0, which by (d) is
  negative iff c > G*. Coupling: lim_{c→0} dσ²/dc + KΣ/λ² ≡ 0 (negative: F from below).
- (h) Paper 1 precision sweep at the worked example, Π0 = 1 (κ = 100): the classifier finds
  exactly one turning point, a maximum, with Π* = 0.6867 and M = 0.09288 (each to 4 s.f.);
  L₋ = F approached from above and L₊ = H approached from above (sequence F, M, H). The
  classifier then reproduces the four-regime table (All for R² ≤ H; lower ray for H < R² ≤ F;
  window for F < R² < M; Empty for R² ≥ M) at: H, F, M exactly; each ×(1 ± 1e-6); and one
  interior tolerance per regime (H/2, (H+F)/2, (F+M)/2, 1.5M).
- **T8.1 PASS** iff (a)–(h) all pass. Route (simplify / numeric only) reported per identity.

## T8.2 — Worked-example values — `t8_values.py`
Expected, 4 s.f.: Π_B = 50, Π_A = 150.
Π = 1: G* = 0.009950, Π0* = 99.50, σ*² = 0.009950, V_c = 0.2550.
Π = 60: Π0* = 64.16, σ*² = 0.008054, V_c = 0.009167.
Π = 500: no interior extremum; V_c = 0.005500.
Coupling, Π = Π0 = 1: c* = 0.01990, σ*² = 0.009950, c_F = 0.04000.
Method: G* from the closed form; Π0*, σ*² (prior) and c*, σ*² (coupling) from
`scipy.optimize.minimize_scalar(method="bounded")` over x = log10 θ ∈ [−6, 6], xatol 1e-12,
(argmin and minimum value); V_c = σ²(c, Π); c_F by brentq on σ² − F over c ∈ (c*, 1e6).
"No interior extremum" at Π = 500: the classifier finds no turning point AND the bounded
minimizer's argmin lies within 1e-6 (in x) of the lower bound −6. PASS iff every value matches.

## T8.3 — Classification tables — `t8_classify.py`
Cases at the worked example: P1 Π = 500, P2 Π = 60, P3 Π = 1 (prior sweep); coupling at
Π = Π0 = 1. Critical tolerances: the closed forms σ*², V_c, F. For each case:
- one tolerance strictly inside every non-degenerate row: midpoint of a bounded range; half the
  upper end for a range unbounded below (R² < x or R² ≤ x); 1.5× the lower end for a range
  unbounded above;
- every critical tolerance exactly (expected class from the table's equality rows / the
  approach-direction rule);
- every critical tolerance × (1 − 1e-6) and × (1 + 1e-6).
Expected classes:
- P1: V_c: All; V_c(1−δ): All; V_c(1+δ): upper ray; F: Empty; F(1−δ): upper ray; F(1+δ): Empty.
- P2: σ*²: two rays; σ*²(1−δ): All; σ*²(1+δ): two rays; V_c: upper ray; V_c(1−δ): two rays;
  V_c(1+δ): upper ray; F: Empty; F(1−δ): upper ray; F(1+δ): Empty.
- P3: σ*²: two rays; σ*²(1−δ): All; σ*²(1+δ): two rays; F: lower ray; F(1−δ): two rays;
  F(1+δ): lower ray; V_c: Empty; V_c(1−δ): lower ray; V_c(1+δ): Empty.
- Coupling: σ*²: two rays; σ*²(1−δ): All; σ*²(1+δ): two rays; F: upper ray; F(1−δ): two
  rays; F(1+δ): upper ray. Also: at R² = F the upper ray starts at c_F (1e-9 relative); at the
  interior tolerance 1.5F it starts at c_R ≥ c_F; at R² = σ*² the two rays meet at c*, and in
  P2/P3 at Π0* (1e-6 relative).
- Boundary Π = Π_B = 50 (P2 type): V_c = F (to 1e-12 relative); expected σ*²: two rays,
  σ*²(1±δ): All / two rays; F = V_c: Empty; F(1−δ): two rays; F(1+δ): Empty; interior
  (σ*² + F)/2: two rays. No tested tolerance gives upper ray (the row is empty).
- Boundary Π = Π_A = 150 (P1 type, c = G*): no turning point found; V_c = σ*²; V_c: All;
  V_c(1−δ): All; V_c(1+δ): upper ray; F: Empty; F(1±δ): upper ray / Empty; interior rows as P1.
**PASS** iff every predicted class matches.

## T8.4 — Theorem 3.2, adversarial — `t8_no_window.py`
Seed 8004 (`numpy.random.default_rng(8004)`). 20,000 parameter sets, λ, Σ, Π, c, Π0 each
log-uniform on [1e-3, 1e3]. Five sweeps per set: prior sweep (θ = Π0), coupling sweep (θ = c),
and, swept in Π0 at fixed Π: G = c·tanh(Π/Π0), G = c(1 − exp(−Π/Π0)), G = cΠ²/(Π² + Π0²).
Tolerances per sweep (10): every finite critical tolerance the classifier itself finds (limits
and turning-point values), each × (1 − 1e-6) and × (1 + 1e-6), and the rest random,
log-uniform on [min/2, 2·max] of those critical values. **PASS** iff no failure set has k ≥ 1
(no window, no mixed class) in any of the 100,000 sweeps × 10 tolerances. Reported: case
counts, class counts, the number of interior local maxima found (expected 0), and if any is
found the smallest gap |σ²(t_max) − R²|; any limit sanity-check failures.

## T8.5 — Proposition 1.1 realizability — `t8_realize.py`
For every ℓ, u ∈ {0, 1} and k ∈ {0, …, 4} (20 classes): a function piecewise linear in
s = θ/(1+θ) ∈ (0, 1) with node values ([2] if ℓ) + [0] + [2, 0]·k + ([2] if u), at equally
spaced s from 0 to 1 (the first and last nodes are the limits at θ → 0, ∞); a single node [0]
is extended to [0, 0.5]. All: nodes [3, 2, 3]. R² = 1. **PASS** iff the classifier returns the
intended class for all 21.

## T8.6 — Figure — `t8_figures.py`
`classification/figures/fig_t8_sweeps.png`, 300 dpi, no title; three panels with log x-axes:
prior sweep at Π = 1, prior sweep at Π = 500, coupling sweep at Π = Π0 = 1. Horizontal lines
F, σ*², V_c where finite and relevant; vertical lines Π0*, c*, c_F where they exist. Not a
pass/fail criterion beyond the file being produced.

## T8.7 — Report
`classification/results/t8.txt` (PASS/FAIL per criterion with measured values and any
SymPy output that differs, verbatim); `classification/REPORT.md` generated from the results,
with this file's commit hash and the final commit hash (7 characters) and total runtime;
`classification/run_all.sh`.
