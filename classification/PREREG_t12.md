# Pre-registration — Task 12: completing Stage 2 (Δt and Σ sweeps) with Stage 3/4 checks

Committed **before** any Task 12 script is written to disk or run; not edited after its commit. Failures stay recorded,
are diagnosed post hoc in separate `*_diag.py` and attributed to the prediction, the code or the criterion. Only genuine
code bugs are fixed, each documented in `t12/RESULTS_t12.md`. Sources: the Task 12 prompt (Parts A–C), the Stage 0–4
documents in `classification/`. Nothing in `verification/` is modified.

**Disclosure (protocol: anything seen before the run that bears on an outcome).** Before writing this file a float64
one-liner evaluated the A2 root and the D1 post curve at the A8 regression point (λ = 1, Σ = 0.01, Π = 1, G = 0.5):
Δt_E = 100.0 (to float precision) and max post ≈ 0.20457 at Δt ≈ 2.465 (post(1) = 0.16631). The prompt's quick check
("maximum of about 0.166 near Δt ≈ 1"; "avg crosses F near Δt ≈ 50") therefore looks wrong on both counts: 0.166 is
post(1), not the maximum, and A1–A2 put the avg crossing at Δt_E = 100. The pre-registered regression criteria below
are the prompt's values; they are expected to fail for these reasons.

## Notation
F = Σ/λ; σ²(G, Π) = (Σ + G²/(2Π))/(λ + G); σ*²(Π) = 2Σ/(λ + √(λ² + 2ΣΠ)); u = 2ΣΠ/λ²; g = G/λ.
M-P: a = e^{−λΔt}, s = 1 − a², q = Fs, r = 1/(ΠΔt) (Π_d = ΠΔt), φ = F/r = FΠΔt. Fixed gain L (0 < L < 2):
P⁺ = ((1−L)²q + L²r)/(1 − (1−L)²a²), P⁻ = a²P⁺ + q, P̄ = F − (F − P⁺)s/(2λΔt).
D1: L = 1 − e^{−GΔt}. D2: L = cΠ_d/(Π_d + Π0), 0 < c < 2. D3: L = m/(1 + m) where m = M′/r′ is the positive root of
m² + s(1 − ψ)m − sψ = 0 with r′ = r/ρ and ψ = F/r′ = ρφ (steady discrete Kalman gain for noise variance r/ρ).
Optimal: D3 with ρ = 1 (L = M/(M + r), M² + M(rs − q) − qr = 0). M-I: Task 11 closed form (`t11_common.samp_metrics`).

## Common method (Tasks 9–11, mandatory)
- mpmath dps 50 (60 for flagged re-runs). Turning points: sign changes of the SymPy-derived analytic derivative of each
  metric in its sweep variable (lambdified to mpmath), T10 method (12 points/decade on x = log10 θ ∈ [−25, 25], shifted:
  Δt by −log10 λ, Σ by log10(λ²/(2Π)) so that u = 10^x, plus breakpoints, adaptive golden-section step at local minima of
  |derivative|, bisection to 1e-30, zero tolerance 1e-40·|metric|/θ). Never by differences.
- Two-route classifier of Tasks 10–11 (`t10/classify.py`), unchanged. Limits from the proved asymptotics below; outer
  brackets x_end; zero limits absolute (|·| ≤ 1e-30), infinite limits ≥ 1e30.
- SymPy route: `simplify`; else `simplify(together(expand))`; else factor radicands; else single-√ remainder; exact 0,
  no numeric fallback. Sign claims via identities with manifestly signed right sides; where SymPy cannot decide, the
  item is reported "unresolved" with numerical evidence (dps 60 derivative signs on 400 log points × 1,000 random sets).
- Fold exponents (if a fold is studied): positions 1/2, values 3/2.
- Random parameters log-uniform over four decades: λ, Σ, Π, G, Π0, ρ, λ′ ∈ [1e-2, 1e2]; c = 2·10^U, U ~ U(−4, 0)
  (c ∈ [2e-4, 2)). Seeds: A-symbolic none; A6 numerics 12006; A8 census 12008; A9 12009; Part B census 12020;
  Part C 12100.
- No Monte Carlo in this task (none is requested), so no common-random-number statements are needed.

## Endpoint limits and brackets (derivations; used by the classifier)
Δt → 0 (x → −∞): expand with L = Gx + ℓ₂x² + O(x³), x = Δt. By hand (to be checked symbolically in A5):
P⁺ = σ²(G, Π) + c₁x + O(x²), c₁ = [G(λG/Π − 2Σ) + δ(G/Π − σ²)]/(2(λ + G)), δ = G² + 2ℓ₂;
P⁻ = σ² + (c₁ + 2λ(F − σ²))x + …, P̄ = σ² + (c₁ + λ(F − σ²))x + …, and λ(F − σ²) = −G(λG/Π − 2Σ)/(2(λ + G)).
- D1 (ℓ₂ = −G²/2, δ = 0): post coefficient c₁ = G(λG/Π − 2Σ)/(2(λ+G)) (sign of G − 2FΠ), prior −c₁, **avg 0 at first
  order** (second order computed by SymPy series and reported).
- D2 (G = cΠ/Π0, ℓ₂ = −G²/c, δ = G²(c − 2)/c): coefficients from the formula.
- D3: L ≈ G_ρΔt with G_ρ = −λ + √(λ² + 2ρΣΠ); coefficients by SymPy series (reported).
- Optimal: limit σ*²; coefficients by SymPy series.
Deviation from the Δt → 0 limit is O(Δt·rate) with rate ≤ 1e6 on the box, so x_lo = −80 − log10 λ puts every metric
within 1e-70 relative of its limit.
Δt → ∞: a² = e^{−2λΔt} is negligible; r → 0 like 1/(ΠΔt).
- D1: L → 1; P⁺ = ((1−L)²q + L²r)/(1 − …) ≈ r → 0 (absolute); P⁻ − F = a²(P⁺ − F) → 0 super-exponentially; P̄ − F =
  (P⁺ − F)s/(2λΔt) ~ −F/(2λΔt) → F from below.
- D2: L → c with L − c ≈ −cΠ0/(ΠΔt); P⁺ → (1−c)²F with P⁺ − (1−c)²F ≈ c[c + 2(1−c)FΠ0]/(ΠΔt) (direction = its sign;
  c = 1 gives limit 0, absolute); P⁻, P̄ → F from below (P⁺ → (1−c)²F < F).
- D3: L → 1, 1 − L ≈ r/(ρF); P⁺ ≈ r → 0; P⁻, P̄ → F from below.
- Optimal: P⁺ → 0 like r; P⁻, P̄ → F from below.
All deviations at ∞ are O(1/Δt) or faster, so x_hi = 80 − log10 λ suffices (1e-76 relative or absolute).
Σ sweeps (x = log10 u): every limit's deviation is O(u) at u → 0 or O(u^{−1/2}) at u → ∞ (B3–B5: rel ~ (1+ρ)/w),
so x_end = ∓80 suffices (u^{−1/2} = 1e-40 at x = 80).

## Part A predictions and checks
- **A1 [prove]** P⁺ − F = L(2−L)[L r/(2−L) − F]/(1 − (1−L)²a²) (so P⁺ > F ⇔ L/(2−L) > FΠ_d, independent of a);
  P⁻ − F − a²(P⁺ − F) ≡ 0; P̄ − F − (P⁺ − F)s/(2λΔt) ≡ 0; fixed-gain P⁺ formula from the recursion.
- **A2 [prove]** (1 − e^{−x})/(1 + e^{−x}) − tanh(x/2) ≡ 0; h(x) = tanh(x/2)/x, h′(x) = (x − sinh x)/(2x² cosh²(x/2)) with
  x − sinh x < 0 for x > 0 (series with positive coefficients); lim_{x→0} h = 1/2. Hence excess set = (0, Δt_E) iff
  G > 2FΠ, else ∅. Numerical: on 1,000 random D1 sets the classifier's excess set at R² = F (post metric) equals the
  prediction, with Δt_E (root of tanh(GΔt/2) = FΠΔt) matching the component end to 1e-12.
- **A3 [prove]** identity for L/(2−L); Δt_E = (c − 2FΠ0)/((2−c)FΠ) iff κ > 2; numerical check as in A2 on 1,000 D2 sets.
- **A4 [census + prove]** Derived by hand: by A1, excess ⇔ L/(2−L) > φ ⇔ m(1 − φ) > 2φ; with T = 2φ/(1 − φ) and the D3
  quadratic Q(m) = m² + s(1 − ρφ)m − sρφ (ψ = ρφ), m > T ⇔ Q(T) < 0, i.e. excess ⇔ **φ < 1 and
  s(1 − φ)(ρ(1 + φ) − 2) > 4φ** (s = 1 − e^{−2λΔt}, φ = FΠΔt). Δt → 0 limit: excess at small Δt ⇔ ρ > 2 + u (= 2(1 + ΣΠ/λ²)), **not ρ > 2**.
  The prompt's conjecture ("non-empty iff ρ > 2 as Δt → 0") is therefore expected to be **false at fixed Π** (true only
  in the further limit u → 0). Checks: the exact condition verified symbolically; on 1,000 random D3 sets the excess set
  (classifier at R² = F, post) is reported (shape: lower ray / ∅ / other) and compared with the exact condition evaluated
  on the boundaries found; onset at Δt → 0 compared with ρ > 2 + u. Pass for the census part: the classifier's excess set
  agrees with the exact condition in every set.
- **A5 [prove]** limits of the table via `sympy.limit`/series (D1, D2 both ends; D3 and optimal: Δt → 0 limit σ²(G_ρ, Π)
  and σ*², ∞ limits as above); first-order coefficients c₁ above checked symbolically; D1 avg second-order coefficient
  reported verbatim.
- **A6 [prove/record]** Optimal M-P: DARE identity; P⁺ = Mr/(M + r); limits σ*² (Δt → 0, all metrics), 0 / F / F
  (Δt → ∞). Monotonicity (post ↓, prior ↑, avg ↑): SymPy sign attempt, else unresolved with numerical evidence (1,000
  sets × 400 points, dps 60, seed 12006). **Regression PASS** (5 s.f., half a unit in the 5th digit), λ = 1, Σ = 0.01,
  Π = 1: post(1) = 0.0098858, avg(1) = 0.0099506; post(10) = 0.0090909, avg(10) = 0.0099545; post(100) = 0.0050000,
  avg(100) = 0.0099750.
- **A7 [prove]** For D1 with G > 2FΠ: P̄ and P⁻ → σ²(G, Π) > F at Δt → 0 and → F from below at ∞ (A5), so each has an
  interior minimum below F; for R² ∈ (min, F) the failure set has ℓ = u = 1 and is not All. Numerical: on all A8 D1 sets
  with G > 2FΠ, for prior and avg: existence of a minimum < F and the class at R² = (min + F)/2 ∈ {two rays} (or
  (1,1,k) recorded); number of minima censused.
- **A8 [census]** D1, D2, D3 × {post, prior, avg}: 2,000 random sets each (seed 12008): turning-point histograms (kinds
  sequence), 10 tolerances per set — every finite critical value exactly, ×(1 ± 1e-6), the rest log-uniform on
  [½·min, 2·max] — both routes. **PASS** iff route (i) = route (ii) everywhere. Reported: classes found per (family,
  metric), any mixed / multi-window class, proofs attempted where the pattern is clean.
  **Qualitative regression (prompt's values, pre-registered as given):** D1, λ = 1, Σ = 0.01, Π = 1, G = 0.5: post has a
  single maximum with value within 2% of 0.166 at Δt within a factor 2 of 1; avg crosses F at Δt within a factor 1.5 of
  50, then has a minimum below F and returns to F from below. *Expected to fail (disclosure above): the maximum is
  ≈ 0.2046 at Δt ≈ 2.46 and the crossing is at Δt_E = 100.*
- **A9 [prove/record]** M-I optimal monotonicity on the continuum: SymPy sign attempt on the scalar closed form; else
  unresolved, with numerical evidence (1,000 sets × 400 points, dps 60, seed 12009) and regression against Task 11:
  `samp_metrics` at λ = 1, Σ = 0.01, Π = 1, Δt ∈ {0.1, 1, 5} must equal Task 11's `results/t11_6.json` formula values to
  1e-12 relative.
- **A10 [prove]** Argument via Theorem 4.2: if fine ⪯_c coarse (or coarse ⪯_c fine), the pointwise errors would be
  ordered at every t; A6's opposite monotonicities of post (at shared sample times) and avg (time average) contradict
  both directions, so M-P is not a causal-garbling family along Δt. Verified numerically for 1,000 random pairs
  (Δt, 2Δt): post(2Δt) < post(Δt) and avg(2Δt) > avg(Δt). Plus the two-sentence explanation.
- Figures H1–H3 as specified.

## Part B predictions (all [prove] by SymPy identities/signs unless marked)
- **B1** σ²/F − (1 + g²/u)/(1 + g) ≡ 0.
- **B2** absolute affine increasing, limit G²/(2Π(λ+G)) at Σ → 0 (from above), ∞ at ∞ → classes All, upper ray;
  relative strictly decreasing ∞ → 1/(1+g) → All, lower ray; excess (r = 1) ⇔ Σ < λG/(2Π).
- **B3** G = λ(w − 1), w = √(1 + ρu); σ²Π/λ − [(w²−1)/ρ + (w−1)²]/(2w) ≡ 0 and its w-derivative
  (1 + 1/ρ)/2 − (1 − 1/ρ)/(2w²) > 0 for w > 1; σ²/F − [(1+ρ)w + 1 − ρ]/(w(w+1)) ≡ 0; derivative numerator
  −(1+ρ)w² + 2(ρ−1)w + (ρ−1), value 2(ρ − 2) at w = 1, so one maximum on w > 1 iff ρ > 2 at
  w_M = [(ρ−1) + √(2ρ(ρ−1))]/(1+ρ). Note: in absolute terms the limit at Σ → 0 is 0, so "All" cannot occur for R² > 0
  (predicted set contains it; not a contradiction).
- **B4 [census + prove]** Derived by hand: with G = −λ′ + √(λ′² + 2ΣΠ), Σ = (G² + 2λ′G)/(2Π); absolute
  σ² = G(G + λ′)/(Π(λ + G)) with d/dG ∝ G² + 2λG + λλ′ > 0 (strictly increasing, 0 → ∞: upper ray only); relative
  σ²/F = 2λ(G + λ′)/((G + 2λ′)(G + λ)) with derivative numerator −G² − 2λ′G + λλ′ − 2λ′², so a single maximum iff
  **λ′ < λ/2** (i.e. Σ/λ′ > 2F), else strictly decreasing from 1. Census (2,000 sets, seed 12020): turning points and
  classes both conventions; PASS iff counts match this prediction and routes agree.
- **B5** ρ = 1 of B3: relative 2/(1 + √(1+u)) decreasing (lower ray, Empty); absolute increasing (upper ray).
- Census for B2, B3 (ρ ∈ [1e-2, 1e2]), B5: 2,000 sets each, both conventions, 10 tolerances, both routes; PASS iff
  turning-point counts and classes match B2/B3/B5 and routes agree. Relative tolerances r drawn as for absolute.
- Figures H4, H5 as specified.

## Part C — blind search
Combos: Δt sweep: {optimal, D1, D2, D3} × {post, prior, avg}, M-I optimal × {(a), (b)}; Σ sweep: {B2, B3, B4, B5} ×
{absolute, relative} — 22 combos. Per combo 1,000 curves × 200 tolerances = 2×10⁵ classifications: 100 log-uniform on
[½·min, 2·max] of finite positive critical values, 100 near-critical (20 exact, 80 within ±1e-6 relative). Route (i) mp
(dps 50 turning points), route (ii) float64 with mp re-run (dps 60) of every case that is flagged (route disagreement, or
class outside the allowed set). Allowed set per combo = predicted classes (optimal M-P post {lower ray, Empty}; optimal
prior/avg and M-I {All, upper ray, Empty}; B2 abs {All, upper ray}, rel {All, lower ray}; B3/B4 abs {upper ray, All},
rel {lower ray, window, Empty}; B5 abs {upper ray, All}, rel {lower ray, Empty}; D1–D3: the classes recorded by the A8
census for that (family, metric)). **PASS** iff 0 persisting out-of-set classes and 0 persisting disagreements.

## Report
`t12/RESULTS_t12.md` from `make_results_t12.py`: rows per check with verdict, worst errors, runtimes, hashes; for each
[prove] item proved / disproved / unresolved with the derivation verbatim; census tables; synthesis-matrix rows labelled
Theorem / Proposition / Numerical result / Conjecture; plain statements (falsified predictions, out-of-set classes, open
Stage 2 entries).
