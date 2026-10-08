# Pre-registration — Task 11: Stage 4 (optimality theorem, spectral dominance, power family, causality counterexample)

Committed **before** any Task 11 script is written to disk or run; not edited after its commit. Failures stay recorded,
are diagnosed post hoc in separate `*_diag.py` scripts and attributed to the document, the code or the criterion. Only
genuine code bugs are fixed, each documented in `t11/RESULTS_t11.md`. Source under test:
`classification/Stage_4_Optimality_Results.md` (copied unchanged, committed with this file). The Task 10 shared
classifier (`t10/classify.py`, two routes) and T10 turning-point method are reused unchanged; "approach from above" is
the C4 definition.

## Notation and model
F = Σ/λ; σ*²(Π) = 2Σ/(λ + √(λ² + 2ΣΠ)). OU noise with spectrum S_{β,τ}(ω) = Kτ^β/(1 + τ²ω²), Var η = v(τ) = (K/2)τ^{β−1}.
Optimal error P = 2C/(B + √(B² + 4AC)), A = (1 − λτ)²/τ, B = 4(Σ + λv), C = 4Σv (the Stage 3 matched-variance quadratic
with v = v(τ)). Stage 2 (β = 0, K = 1/Π) differenced filter as in Task 9. Delay: P(d) = F − e^{−2λd}(F − σ*²).
Integrate-and-dump sampling as in T11.6 below.

## Common method (Task 9–10 lessons, mandatory)
- mpmath, dps 50 (60 for flagged re-runs, 100 for the regularized ARE). Turning points by sign changes of an analytic
  derivative (SymPy `diff`, lambdified to mpmath) with the T10 method (12 points/decade on x = log10 θ ∈ [−25, 25] shifted by
  −log10 λ for τ, plus breakpoints, adaptive golden-section step at local minima of |derivative|, bisection to width 1e-30,
  zero tolerance 1e-40·|P|/θ). Never by differences of P.
- **Endpoint limits come from proved asymptotes**, not from evaluation at fixed x (derivations below). The direct route's
  outer bisection brackets are extended to x where the proved bound puts P within 1e-40 (relative to F) of its limit:
  for a zero limit governed by √(C/A) ∝ τ^{β/2} (τ → 0) or τ^{β/2 − 1} (τ → ∞), x_end = ∓(40 + 10)/(e/2) − log10 λ with e = β
  resp. 2 − β (and at least ∓80); for the limit F at τ → 0 when β < 0, x_end = −(40 + 10)/|β| − log10 λ (at least −80);
  otherwise ∓80. A numerical consistency check of P at x_end against the limit (absolute 1e-30 for 0, relative 1e-20 for
  finite limits) is reported, not used.
- **SymPy route:** `simplify`; else `simplify(together(expand))`; else, for each √X, replace X by `factor(X)` (allowed to
  factor radicands, Task 10 lesson) and repeat; else single-√ remainder. Exact 0 required; no numeric fallback. Sign claims
  via SymPy assumptions on an identity whose right side is manifestly signed.
- **Regularization:** ε scaled per set, ε₀ = R_v/(λ + 1/τ)² with R_v = 2Σ + 2v/τ, ε_j = ε₀·10^(−4j), j = 2, 3, …, until the
  relative step change < 1e-12 (≤ 25 steps; non-convergence is a failure).
- **Folds (if any appear):** position and value exponents pre-registered separately as 1/2 and 3/2 (none is tested here).
- Seeds: T11.2 11002, T11.3 11003, T11.4 11004, T11.5 11005, T11.6 11006.

## Proved limits for the power family (used by the classifier)
From P ≤ √(C/A) = √(2ΣK)τ^{β/2}/|1 − λτ| (T11.1(c)) and P ≥ 0; and, where v → ∞, P → C/B → F (B² dominates 4AC when
4AC/B² → 0, i.e. Σ/(λ²vτ) → 0; vτ = (K/2)τ^β):
| β | L₋ (τ → 0) | L₊ (τ → ∞) | predicted classes |
|---|---|---|---|
| β < 0 | F (vτ → ∞) | 0 (bound) | lower ray, Empty |
| β = 0 | σ*²(1/K) (Stage 2) | 0 | lower ray, Empty |
| 0 < β < 2 | 0 (bound) | 0 (bound) | (0,0,k), k ≥ 1, or Empty |
| β = 2 | 0 (bound) | F (vτ → ∞) | upper ray, Empty |
| β > 2 | 0 (bound) | F | upper ray, Empty |

## T11.1 — Symbolic (`t11_symbolic.py`), every item reduces to 0
(a) ∂_τ log S − [β/τ − 2τω²/(1+τ²ω²)] ≡ 0; 2/τ − 2τω²/(1+τ²ω²) − 2/(τ(1+τ²ω²)) ≡ 0 with the last term positive (so the
second term is < 2/τ). (b) β = 0, K = 1/Π: S_{τ1} − S_{τ2} − |H_ξ(iω)|² ≡ 0 with |H_ξ(iω)|² = H_ξ(iω)H_ξ(−iω) from
Prop. 4.5(b). (c) 2C/√(4AC) − √(C/A) ≡ 0; √(C/A) − √(2ΣK)τ^{β/2}/|1 − λτ| ≡ 0 at v = (K/2)τ^{β−1} (checked on λτ < 1 and
λτ > 1 separately via τ = 1/(λ(1+w)) and τ = (1+w)/λ, w > 0); B + √(B²+4AC) − √(4AC) > 0 (so P ≤ √(C/A)). (d) Duality:
A(τ) − A(1/(λ²τ)) ≡ 0 and v_{β,K}(τ) − v_{2−β,Kλ^{2−2β}}(1/(λ²τ)) ≡ 0, hence P_{β,K}(τ) − P_{2−β,Kλ^{2−2β}}(1/(λ²τ)) ≡ 0.
(e) With Cov(s(t), s(t−d)) = F e^{−λd}: Var(s(t) − e^{−λd}s(t−d)) − F(1 − e^{−2λd}) ≡ 0; e^{−2λd}σ*² + F(1 − e^{−2λd}) −
[F − e^{−2λd}(F − σ*²)] ≡ 0. (f) ∂_Σσ*² > 0; ∂_λσ*² < 0 at fixed Σ; 2F/(1 + √(1 + 2FΠ/λ)) − σ*²|_{Σ=Fλ} ≡ 0 and its
∂_λ > 0 at fixed F (each via an identity with a manifestly signed right side).
**PASS** iff all items reduce to 0 / have the stated sign.

## T11.2 — Garbling realized (`t11_garble.py`), Monte Carlo, seed 11002
λ = 1, Σ = 0.01, Π = 1, (τ1, τ2) ∈ {(0.5, 2), (1, 10)}. Euler–Maruyama, dt = min(τ1, 1/λ)/200; 4,000 independent
trajectories; burn-in 10·max(τ2, 1); averaging window 40·max(τ1, 1). State: s, η_{τ2} (OU, Var 1/(2Πτ2)), and ξ from
H_ξ(s) = c s/((1+τ1 s)(1+τ2 s)), c = √((τ2² − τ1²)/Π), realized as ξ = c/(τ1τ2(b − a))·(b x_b − a x_a), a = 1/τ1,
b = 1/τ2, ẋ_a = −a x_a + w, ẋ_b = −b x_b + w (one unit white noise w). Y′ = s + η_{τ2} + ξ, y_{τ2} = s + η_{τ2}.
(i) Autocovariance of n = η_{τ2} + ξ at u ∈ {0, τ1/2, τ1, 2τ1} (per-trajectory time averages of n(t)n(t−u), SE across
trajectories) within 3 SE of e^{−|u|/τ1}/(2Πτ1), with SE ≤ 1% of C(0) = 1/(2Πτ1). (ii) The Stage 2 differenced filter for
τ1 run on Y′ (z dt = ΔY′ + Y′dt/τ1, gain (hP + 2Σ)/R_v) has MSE within 3 SE of P(τ1), SE ≤ 1%. (iii) MSE₁(Y′) −
MSE₂(y_{τ2}) > 3·SE of the per-trajectory difference (common random numbers). **PASS** iff (i)–(iii) hold for both pairs.

## T11.3 — Power family (`t11_power.py`), seed 11003
β grid: k/20 for k = −40…80 (exact rationals), plus {0, 2} ± {1e-6, 1e-3}: 129 values. 300 sets per β: λ, Σ, K
log-uniform on [1e-2, 1e2].
- **Turning points PASS:** 0 for every β ≤ 0 and every β ≥ 2; ≥ 1 for every 0 < β < 2 with the first a maximum.
- **Unimodality (record only):** histogram of turning-point counts for 0 < β < 2 (answers Numerical result 4.6a).
- **Limits.** For every set with 0 < β < 2 and ρ ∈ {1e-10, 1e10} (λτ = ρ): P(ρ/λ) ≤ √(C/A)(ρ/λ) (PASS required). The
  "bound below 1e-3·max P" check is applied to a set and end **iff** √(C/A)(ρ/λ) < 1e-3·P(1/λ) (computable before the
  run; P(1/λ) = C/B at A = 0 ≤ max P); there P(ρ/λ) < 1e-3·max_τ P is required. Derivation of which β satisfy this for
  **every** set in the box: the ratio √(C/A)/P(1/λ) = 2ρ^{β/2}[√(Σ/(λv₁)) + √(λv₁/Σ)]/|1 − ρ| with v₁ = (K/2)λ^{1−β},
  and |log10(λv₁/Σ)| ≤ 8.301 − 2β on the box. Hence: at ρ = 1e-10 it applies to every set iff β > 1.2419 (grid: β ≥ 1.25,
  and 2 − 1e-3, 2 − 1e-6); at ρ = 1e10 iff β < 0.6371 (grid: β ≤ 0.6 with β > 0, and 1e-6, 1e-3). Other β: per set.
- **Classes (both routes):** 10 tolerances per set: 7 log-uniform on [1e-3·P_ref, 2·P_ref], P_ref(1 − 1e-6), P_ref,
  P_ref(1 + 1e-6), with P_ref = max_τ P for 0 < β < 2 (the turning-point maximum) and P_ref = the finite nonzero limit
  otherwise. PASS: β ≤ 0 → lower ray or Empty; β ≥ 2 → upper ray or Empty; 0 < β < 2 → (0,0,k) with k ≥ 1, or Empty;
  and route (i) = route (ii) everywhere.
- **Duality PASS:** 1,000 random (β ∈ [−2, 4], K, λ, Σ, λτ ∈ [1e-10, 1e10]) in mpmath: relative difference ≤ 1e-30.
- **Independent route PASS:** β ∈ {−1, 0.5, 1.5, 3}, 100 sets each (λ, Σ, K as above, λτ log-uniform on [1e-4, 1e4]) plus
  λτ = 1 for each set: regularized ARE (mp, dps 100, scaled ε, convergence < 1e-12) and closed-form causal Wiener
  (S_y = 2Σ/(λ²+ω²) + 2vτ/(1+τ²ω²), k² = 2Στ² + 2vτ, β_W² = (2Σ + 2vτλ²)/k², A_W = 2Σ(1+λτ)/(k(β_W+λ)),
  MMSE = Σ/λ − A_W²/(2λ)) agree with the quadratic to relative 1e-8.
- **Spectral dominance PASS:** for β on the 0.25 grid in [−2, 4] (25 values), 1,000 random pairs τ1 < τ2 (λτ log-uniform on
  [1e-10, 1e10], K and λ as above): signs of S_{τ1} − S_{τ2} (mp, full spectra) on a 10-per-decade log ω grid over
  ω ∈ [1e-40, 1e40] (|difference| ≤ 1e-40·max(S) counts as 0): no sign change for β ≤ 0 or β ≥ 2; exactly one for
  0 < β < 2, and the bracketing grid interval contains the analytic crossing ω*² = (τ2^β − τ1^β)/(τ1²τ2²(τ1^{β−2} − τ2^{β−2})).
**T11.3 PASS** iff all PASS parts hold (unimodality is record only).

## T11.4 — Delay counterexample (`t11_delay.py`), seed 11004
- **MC PASS:** λ = 1, Σ = 0.01, Π = 1, d ∈ {0, 0.2, 1/e, 1}; dt = 1e-3, delay = round(d/dt) steps (compared with P at the
  realized delay); 2,000 trajectories, burn-in 10, window 20; steady Kalman–Bucy filter (gain G* = Πσ*²) on y_d,
  estimate e^{−λd}ŝ; all four within 3 SE of P(d), SE ≤ 1%.
- **Sweep PASS:** θ-curve P(d(θ)), d = θe^{−θ}, analytic derivative; classes (both routes) at R² = σ*² + q(P(1/e) − σ*²),
  q ∈ {0.1, 0.5, 0.9}: window (0,0,1) with θ₋e^{−θ₋} = θ₊e^{−θ₊} to relative 1e-12; at P(1/e) and P(1/e)(1 + 1e-6): Empty.
- **Regression PASS:** P(0) = 0.0099505, P(1/e) = 0.0099763 (half a unit in the last digit).

## T11.5 — Ordering not necessary (`t11_notnec.py`), seed 11005
β = 1; 1,000 sets (λ, Σ, K as above), τ1 < τ2 log-uniform in (1/λ, 100/λ). **PASS** iff P(τ2) < P(τ1) in all and the
spectra have exactly one sign change in all (T11.3 grid method).

## T11.6 — Sampling interval (`t11_sampling.py`), seed 11006
Model dy = s dt + Π^{−1/2}dW, z_k = (1/Δt)∫ dy over the k-th interval. Exact discretization with the interval integral
I reset each sample: s_k = φs_{k−1} + w₁, I_k = ((1 − φ)/λ)s_{k−1} + w₂, φ = e^{−λΔt},
Var w₁ = F(1 − φ²), Cov(w₁, w₂) = (2Σ/λ²)[(1 − φ) − (1 − φ²)/2], Var w₂ = (2Σ/λ²)[Δt − 2(1 − φ)/λ + (1 − φ²)/(2λ)],
z_k = I_k/Δt + v_k, Var v_k = 1/(ΠΔt). Steady-state posterior variance p of s_k: the positive root of
h²p² + (r_e(1 − φ²) − q₁₁h² + 2φhg)p − (q₁₁r_e − g²) = 0 with h = (1 − φ)/(λΔt), r_e = q₂₂/Δt² + 1/(ΠΔt), g = q₁₂/Δt
(scalar reduction of the 2-state filter). Metrics: (a) P̄_a = p; (b) P̄_b = p(1 − φ²)/(2λΔt) + F(1 − (1 − φ²)/(2λΔt)).
- **Internal check PASS:** on 20 random sets the scalar p equals the fixed point of the full 2-state discrete Kalman
  iteration (mp, iterated to 1e-40) to relative 1e-30, and the Q entries equal a Van Loan matrix-exponential computation
  (mp) to 1e-30.
- **MC validation PASS:** λ = 1, Σ = 0.01, Π = 1, Δt ∈ {0.1, 1, 5}: fine-step Euler–Maruyama (dt = min(Δt, 1/λ)/200),
  2,000 trajectories, burn-in 20, window 200 (rounded to whole intervals); the steady-state discrete filter on simulated
  z_k; (a) at sample times and (b) averaged over all fine steps, each within 3 SE of the closed forms, SE ≤ 2%.
- **Cor. 4.9 PASS:** 1,000 random sets (λ, Σ, Π log-uniform on [1e-2, 1e2], λΔt log-uniform on [1e-3, 1e2]),
  m = 2…10: P̄(mΔt) ≥ P̄(Δt)(1 − 1e-12) for (a) and for (b).
- **Continuum (record only):** 1,000 random sets, 400 log-spaced λΔt in [1e-3, 1e2]: sign of dP̄/dΔt (mp, dps 60,
  `mp.diff` of the closed form) for (a) and (b); report every non-positive derivative (i.e. any non-monotone case) and the
  limit P̄_a(λΔt = 1e-8)/σ*² − 1.
**T11.6 PASS** iff the internal check, MC validation and Cor. 4.9 parts pass.

## Figures (`t11/figs/`, PNG + PDF; palette #2a78d6, #eb6834, #1baf7a, #4a3aa7 plus line styles)
G1 power-family phase diagram (β vs log10 λτ, colour P/max_τ P at λ = 1, Σ = 0.01, K = 1; turning-point locus from the mp
method; vertical lines β = 0, 2 labelled "ordered" / "spectra cross"; β = 0 (Stage 2) and β = 1 (Stage 3) marked);
G2 spectra S_{τ1}, S_{τ2} (τ1 = 0.5, τ2 = 2, K = 1) for β = 0 and β = 1 side by side; G3 P(d(θ)) vs θ with the q = 0.5 window
shaded; G4 P̄_a and P̄_b vs Δt (λ = 1, Σ = 0.01, Π = 1) with nested chains 0.01·2^k and 0.01·3^k marked.

## Report
`t11/RESULTS_t11.md` from `make_results_t11.py`; one row per check with verdict, worst errors, runtime, hashes; diagnoses;
the T11.3 unimodality histogram as the answer to Numerical result 4.6a; the T11.6 continuum answer; wording/formula errors;
plain statements on whether any theorem/proposition is contradicted and whether any out-of-set class appeared.

## Notes made before any code (by hand)
1. Prop. 4.5(c): "Theorem 4.2 shows the family is not causally ordered by any garbling." Non-monotone P rules out a causal
   order *along τ* for the whole family; it does not by itself rule out pairwise causal orders against the τ direction
   (Theorem 4.2 only gives P(θ2) ≤ P(θ1) for θ1 ⪯ θ2). Wording to check, not a computation.
2. Corollary numbering: Corollary 4.10 appears before 4.9 (wording).
3. Spectral crossing in the power family: S_{τ1} − S_{τ2} has the sign of (τ1^β − τ2^β) + ω²τ1²τ2²(τ1^{β−2} − τ2^{β−2}),
   linear in ω², so at most one crossing for any β; exactly one iff 0 < β < 2 (τ1 ≠ τ2). Consistent with Thm 4.6.
4. Corollary 4.3 cites "Theorem 3.13" (plateaus) from Stage 3 results, which this verification does not have; not checked.
