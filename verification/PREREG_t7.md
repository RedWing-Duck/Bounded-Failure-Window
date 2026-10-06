# Pre-registration — Task 7: revision checks

Committed **before** any Task 7 script is written to disk or run. This file is not edited
after its commit. A criterion that turns out to be badly posed is reported as such, not
changed. If an identity is wrong, what SymPy actually returns is reported verbatim.

Notation: the prior precision formerly called P is Π₀ (`Pi_0` in code, $\Pi_0$ in plot
labels). F = Σ/λ, κ = (c/Π₀)/F. Worked example: λ = c = 1, Σ = 0.01, so Π₀ = 100/κ.

## Conventions used by every criterion
- **Symbolic identity.** PASS if `sympy.simplify(lhs − rhs) == 0`. If the simplification
  does not return 0, the identity is evaluated at 20 random rational points: each
  positive symbol is drawn log-uniformly in [1e-2, 1e2], φ is drawn uniformly in
  (0.01, 0.99) and L uniformly in (0.001, 0.999), using `numpy.random.default_rng(7003)`.
  Values are converted to exact rationals and evaluated with `evalf(50)`. It passes if
  |lhs − rhs| ≤ 1e-12·max(|lhs|, |rhs|). The verdict is then labelled
  "PASS (numeric only)". Which route was used is always reported.
- **"Match to n significant figures".** |computed − stated| ≤ 0.5·10^(floor(log10|stated|) − n + 1).
  This is the same convention as T1.9: a half unit in the n-th significant figure of
  the stated value. A value stated as "1.000" counts as 4 s.f.
- Seeds: T7.1(e) 7001, T7.1(f) 7002, symbolic fallback 7003. No stochastic simulation
  is run in Task 7.

## T7.1 — discrete-time identity (`t7_discrete_symbolic.py`)
Plant h_{k+1} = φh_k + w (var q, 0<φ<1); y = h + v (var r = 1/Π_d); fixed gain L ∈ [0,1];
s = 1 − φ²; F = q/(1 − φ²). Predicted error e⁻_{k+1} = φ[(1−L)e⁻_k + L v_k] − w_k.

- (a) The stationary second moment is derived from the recursion: square it, take
  expectations with e⁻_k, v_k, w_k independent and zero-mean, and solve the fixed point
  M = E[(e⁻_{k+1})²] for M. Check: M − (φ²L²r + q)/(1 − φ²(1−L)²) ≡ 0.
- (b) The posterior error (1−L)e⁻ + Lv is squared and its expectation taken. Check:
  S − ((1−L)²M + L²r) ≡ 0.
- (c) S − F − (M − F)/φ² ≡ 0.
- (d) `sympy.factor(M − F)` is reported verbatim. Check: M − F − φ²L[L(r(1−φ²)+q) − 2q] /
  [(1−φ²)(1+φ(1−L))(1−φ(1−L))] ≡ 0.
- (e) Algebraic part: L(r s + q) − 2q − (2−L)·r·s·(L/(2−L) − F·Π_d) ≡ 0 with Π_d = 1/r.
  The prefactors φ²L, (2−L)rs, (1−φ²), (1+φ(1−L)) and (1−φ(1−L)) must be shown
  positive for 0<φ<1 and 0<L≤1. SymPy assumption queries are used after the
  substitutions φ = 1/(1+u) and L = 1/(1+w), with u, w > 0, which cover 0<φ<1 and
  0<L<1; L = 1 is checked by direct substitution.
  Together these give M > F ⇔ L/(2−L) > F Π_d. Numeric part: 10,000 random sets
  (seed 7001; φ ~ U(0.01, 0.99); q, r log-uniform in [1e-3, 1e3]; L ~ U(0.001, 0.999)),
  evaluated in exact rational arithmetic (`fractions.Fraction` of the float draws).
  PASS iff 0 mismatches between (M > F) and (L/(2−L) > F Π_d).
- (f) (M + rs)(M + 2r) − 2rs(M + r) − (M² + rM(2−s)) ≡ 0. Then, eliminating q with the
  Riccati equation M = φ²Mr/(M+r) + q (q = M(M+rs)/(M+r)):
  ½FΠ_d − L*/(2−L*) − M²(M + r(2−s))/(2rs(M+r)(M+2r)) ≡ 0, with L* = M/(M+r). The
  right-hand side must be positive (M, r > 0; 2 − s = 1 + φ² > 0), which proves
  L*/(2−L*) < ½FΠ_d. Numeric part: 20,000 random sets (seed 7002; φ ~ U(0.01, 0.99);
  q, r log-uniform in [1e-3, 1e3]), M from the stable root of
  M² + M(rs − q) − qr = 0, in float64. PASS iff every ratio [L*/(2−L*)]/(½FΠ_d) < 1.
  The maximum ratio is reported; it is expected to approach 1 from below as q/r → 0.
  Informational: substituting L* into (a) recovers the Riccati M.
- (g) With φ = e^{−λΔt}, q = Σ(1−φ²)/λ, Π_d = ΠΔt and L = GΔt, the condition
  D = L/(2−L) − FΠ_d is expanded in Δt. Check: the leading term is Δt·(G/2 − FΠ),
  i.e. the series coefficient of Δt¹ minus (G/2 − FΠ) ≡ 0 and the Δt⁰ term ≡ 0.
  So the leading-order condition is G > 2FΠ.
- T7.1 PASS iff (a)–(g) all pass.

## T7.2 — continuous-time closed-form checks (`t7_continuous_checks.py`)
- (a) The positive root p of 0 = 2Σ − 2λp − Πp² satisfies pΠ − (−λ + sqrt(λ²+2ΣΠ)) ≡ 0,
  p − 2Σ/(λ + sqrt(λ²+2ΣΠ)) ≡ 0, and p equals closed form (2) evaluated at G = G*.
- (b) "Exact root of Proposition 4" is interpreted as the positive root of
  AΠ² + BΠ + C = 0 with A = 2Π₀Σ + c² + cλ, B = 4Π₀²Σ, C = Π₀²(2Π₀Σ − cλ). When no
  positive root exists (κ ≤ 2), M = F, the supremum reached as Π → 0. Expected M/F at
  κ = 2, 3, 5, 10, 20, 50, 100: 1.000, 1.036, 1.175, 1.584, 2.432, 5.000, 9.288. Each must
  match to 4 s.f.
- (c) κ = 50, Π₀ = 2, in SymPy rationals: Π* == 4/3 and M == 1/20 exactly (structural
  equality after `nsimplify`-free rational arithmetic).
- (d) `scipy.optimize.brentq` on M(κ) − 0.05 over κ ∈ [2.5, 1000] (xtol 1e-14) gives
  |κ_root − 50| ≤ 1e-8. In addition, M(κ) is strictly increasing on
  `logspace(log10 2.5, 3, 10001)`, which justifies "smallest".
- (e) Hill gain G = cΠ²/(Π²+Π₀²), grid `logspace(-6, 6, 600001)`, with
  max_Π [σ²(Π) − F] evaluated directly in float64. The cancellation-free form from
  T1.8 is reported too. Π₀ = 24: the maximum must be > 0 and match 1.40e-4 to 3 s.f.
  Π₀ = 26: the maximum must be ≤ 1e-15. Π₀ = 25: reported only; the boundary is
  expected to give ≈ 0.
- T7.2 PASS iff (a)–(e) all pass.

## T7.3 — specification of Task 4a (`t7_specify_4a.py`, no new simulation)
Writes `results/t7_4a_spec.txt` in plain language. It covers the plant, the
precision definitions and their mapping to Π_d and the continuous Π, what
"slope ratio" meant operationally, and prior vs posterior. These facts are
taken from `t4a_discrete.py` and `results/t4a.json`.
- **Criterion.** The miscalibrated steady-state gain is recomputed independently of
  the t4a code, using the Riccati of T7.1(f) with assumed process noise k·q. The
  closed-form posterior variance S_L of T7.1(a,b) is then maximised over Π_d with
  `scipy.optimize.minimize_scalar` (bounded, log10 Π_d ∈ [−3, 4], xatol 1e-10).
  "Proposition 6's closed form" is interpreted as T7.1(a,b). For k = 3, 10, 100 the
  peaks must match the reported 0.01075, 0.02224 and 0.1837, read from
  `results/t4a.json`, to 3 s.f.
- **Informational decomposition** of the k = 100 peak (0.1837) against the continuous
  κ = 100 peak (0.0929). Each figure is computed as stated:
  (i) the continuous κ implied by the 4a mapping. dL/dΠ_d at 0 maps to dG/dΠ, since
  L = GΔt and Π_d = ΠΔt, so κ_cont = k.
  (ii) The continuous closed-form (2) peak with the Bayesian-weight gain at that κ.
  (iii) The discrete Δt = 0.05 posterior peak of the Bayesian-weight gain
  (L = Δt·cΠ/(Π+Π₀), Π = Π_d/Δt): the Δt effect on the paper's model.
  (iv) The continuous closed-form (2) peak with the gain that the 4a filter
  converges to as Δt → 0 (Kalman–Bucy gain under assumed noise kΣ:
  G = −λ + sqrt(λ² + 2kΣΠ)): the gain-shape effect.
  (v) The 4a filter's prior (M) peak at Δt = 0.05.
  (vi) The 4a filter's posterior peak at Δt ∈ {0.05, 0.01, 0.001}, showing convergence.
  The cause is attributed to mapping, Δt, prior vs posterior, or anything else
  according to these numbers.

## T7.4 — figures (`t7_figures.py`, no simulation)
No titles. 300 dpi. Designed for a 6.5-inch text width, so 72 % ≈ 4.7 in wide, with
8–9 pt fonts. Same palette and spine style as the existing figures.
- `figures/fig1_paired.png`: the content of Figure 1a, using the saved points in
  `results/t3.json`. Labels "Π₀ = 1 (κ = 100)", "Π₀ = 100 (κ = 1)", "optimal". It has an
  inset showing the closed-form calibrated − optimal variance on a log x-axis.
- `figures/fig2_regimes.png`: the content of Figure 1b, relabelled with Π₀. This is
  "the existing Figure 2" in the revised numbering.
- `figures/fig3_peak_vs_kappa.png`: M/F against κ ∈ [1, 1000], log–log, closed form.
  It has a horizontal line at R²/F = 5, vertical markers at κ = 2 and κ = 50, and points
  at the κ values of T7.2(b), taken to be the Section 4 table.
- Pass (checked by script): the three files exist, are 300 dpi, are 4.7 in wide, and
  have no axes titles. Visual review is by eye.

## T7.5 — runtime
`t7_runtime.py`, which is not part of `run_all.sh` to avoid recursion, copies
`verification/` to a temporary directory and times the full `run_all.sh`, Task 7
included, there. This leaves the committed results and earlier REPORT sections
untouched. It records the wall time per script and in total. It also checks that every
regenerated `results/*.json` equals the committed one after removing `runtime_s`
fields; this check is informational. Pass: run completes with exit code 0.

## T7.6 — report
`t7_report.py` writes `results/t7.txt` (PASS/FAIL per criterion with measured values, the
T7.1(d) factorisation and T7.1(f) difference in LaTeX, the T7.3 specification and
explanation). It appends or replaces only the section "Task 7 — revision checks" at the
end of REPORT.md, with the 7-character prereg hash and the 7-character hash of the
commit holding the Task 7 scripts and results. The report section is committed after
that commit, because a file cannot contain its own commit hash. Task 7 is added to
`run_all.sh`.
