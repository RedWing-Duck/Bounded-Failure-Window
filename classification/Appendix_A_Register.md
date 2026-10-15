# Appendix A. Register of results

Rendered from `register/results.yaml` (freeze v1, Task 14). Numbers are thesis numbers: one counter per chapter, shared by all result types. Verification task identifiers are listed in `register/tasks.yaml`; earlier labels are in `register/crosswalk.md`.

| No. | Type | Result | Key | Verified by | Status |
|---|---|---|---|---|---|
| 2.1 | Proposition | Topological realisability | `topological-realizability` | T8.5 | proved |
| 2.2 | Theorem | Critical-tolerance theorem | `critical-tolerance` | T8.1, T8.3, T9–T13 classifiers | proved |
| 2.3 | Definition | Critical-value signature and stratification | `signature` | — | definition |
| 2.4 | Theorem | Plateaus (C2′) | `plateaus` | T10.5 | proved |
| 2.5 | Corollary | Equal-height maxima | `equal-height-maxima` | T10.5 | proved |
| 2.6 | Corollary | Degenerate stationary points | `degenerate-points` | T10.5 | proved |
| 2.7 | Proposition | Pair birth | `pair-birth` | T10.5 (with diagnosis) | proved |
| 2.8 | Corollary | Reparameterisation (orientation swaps ℓ and h) | `reparameterisation` | T15 C11 | proved |
| 2.9 | Proposition | Structural stability at a fixed tolerance | `structural-stability` | T15 C12 | proved |
| 3.1 | Proposition | Stationary variance; constant-gain filter equivalence | `stationary-variance` | T1, T2 | proved |
| 3.2 | Theorem | Normal form σ²/F = V(ν,q) | `normal-form` | T14 G | proved |
| 3.3 | Corollary | Excess identity σ² > F ⇔ q > 2 | `excess-identity` | T1, T8.1 | proved |
| 3.4 | Theorem | Window theorem (sup q > 2); optimal monotone along Π | `window-theorem` | T1, T3, T4, T13 C2 | proved |
| 3.5 | Proposition | Optimal gain and envelope V⋆ = q⋆ | `optimal-envelope` | T1, T7 | proved |
| 3.6 | Lemma | Single minimum in the gain | `single-minimum-gain` | T8.1 | proved |
| 3.7 | Lemma | Elasticity form (path derivative) | `elasticity` | T10.1 | proved |
| 4.1 | Theorem | Monotone gain sweeps cannot window | `monotone-gain-sweeps` | T8.4, T13 C2 | proved |
| 4.2 | Proposition | Prior precision: endpoints and extrema | `prior-endpoints` | T8.1, T8.2 | proved |
| 4.3 | Proposition | Prior precision: classification | `prior-classification` | T8.3, T13 C2 | proved |
| 4.4 | Proposition | Coupling: endpoints and extrema | `coupling-endpoints` | T8.1, T8.2 | proved |
| 4.5 | Proposition | Coupling: classification | `coupling-classification` | T8.3, T13 C2 | proved |
| 5.1 | Theorem | Gain realisability | `realizability` | T10.1, T10.2 | proved |
| 5.2 | Corollary | Forced lower ray | `forced-lower-ray` | T10.1 (factor-radicand route), T10.2 | proved |
| 5.3 | Corollary | Exact class set along precision | `exact-class-set` | T10.2 | proved |
| 5.4 | Corollary | Unbounded windows for regular gains | `unbounded-windows` | T10.2 (supplementary) | proved |
| 5.5 | Corollary | What regularity pins | `regularity-pins` | T10 (derivation) | proved |
| 5.6 | Lemma | Excess components | `excess-components` | T8.1 (Corollary 3.3, excess identity) | proved |
| 5.7 | Lemma | Bounded gains approach H from above | `bounded-gain-limit` | T10.3, T10.7 | proved |
| 5.8 | Proposition | Bayesian-weight gain along precision (onset κ > 2; four regimes) | `bayesian-weight` | T1, T3, T7, T10.3, T10.7, T13 C2 | proved |
| 5.9 | Proposition | Misspecified Kalman gain | `misspecified-kalman` | T10.1, T10.3, T13 C2 | proved |
| 5.10 | Proposition | Capped gain | `capped-gain` | T10.3, T10.5, T13 C2 | proved |
| 5.11 | Proposition | Precision-blind gain | `precision-blind` | T4, T10.3, T13 C2 | proved |
| 5.12 | Theorem | Hill gain for every real n > 1 | `hill-turning-points` | T4, T7, T10.1, T10.3 ($n = 2$), T13 A5 | proved |
| 5.13 | Proposition | Hill classification and the mixed class | `hill-classification` | T10.4, T13 C2 | proved |
| 5.14 | Proposition | No mixed class when G/Π decreases | `no-mixed-decreasing-ratio` | T13 C2 (row-8 diagnosis, t13_audit_classes_diag2.py) | proved |
| 5.15 | Numerical result | Two-stage gains | `two-stage-gains` | T10.3, T13 C2 | numerical |
| 6.1 | Lemma | Relay variance at matched power (with coloured excess condition) | `tau-relay-variance` | T4, T6, T9.1 | proved |
| 6.2 | Proposition | Relay monotone in τ | `tau-relay-monotone` | T9.1, T9.4 | proved |
| 6.3 | Proposition | Relay classification along τ | `tau-relay-classes` | T9.4, T13 C2 | proved |
| 6.4 | Proposition | Optimal error along τ (closed form) | `tau-optimal-error` | T9.1, T9.2 (Wiener route; ARE route via diagnosis) | proved |
| 6.5 | Corollary | Normalised optimal error P/F | `tau-optimal-normal-form` | T14 G | proved |
| 6.6 | Theorem | Optimal error decreases in τ | `tau-optimal-monotone` | T9.1, T9.5 | proved |
| 6.7 | Proposition | Optimal classification along τ | `tau-optimal-classes` | T9.4, T13 C2 | proved |
| 6.8 | Proposition | Best constant-gain relay | `tau-best-constant-gain` | T9.5 (with mp diagnosis) | proved |
| 6.9 | Proposition | Strict gap P < V | `tau-strict-gap` | T13 A7 | proved |
| 6.10 | Proposition | Optimal filter at matched variance | `matched-variance-optimal` | T10.6, T13 C2 | proved |
| 6.11 | Counterexample | The optimal filter can window | `optimal-can-window` | T10.6 | proved |
| 6.12 | Proposition | Relay at matched variance | `matched-variance-relay` | T10.6, T13 C2 | proved |
| 6.13 | Proposition | Discrete excess condition L/(2 − L) > FΠ_d for 0 ≤ L < 2 | `discrete-excess` | T4, T7 | proved |
| 6.14 | Lemma | Shared excess set (M-P) | `shared-excess-set` | T12 | proved |
| 6.15 | Proposition | D1 tanh lemma | `d1-excess` | T12 | proved |
| 6.16 | Proposition | D2 excess set (0 < c < 2) | `d2-excess` | T12 | proved |
| 6.17 | Proposition | D3 excess set; onset ρ > 2 + ν | `d3-excess` | T12 | proved |
| 6.18 | Proposition | Endpoint limits along Δt | `dt-endpoint-limits` | T12 (with series-route diagnosis) | proved |
| 6.19 | Theorem | Optimal M-P along Δt: posterior ↓; prior ↑; averaged ↑ | `dt-optimal-mp` | T12 (a), T13 A1, A2 (b), (c) | proved |
| 6.20 | Proposition | Two rays from an over-weighted sampled relay | `dt-two-rays` | T12 (with diagnosis) | proved |
| 6.21 | Numerical result | Census of sampled relays | `dt-relay-census` | T12, T13 C2 | numerical |
| 6.22 | Conjecture | At most two turning points (sampled relays) | `dt-two-turning-points` | T12, T13 A6, C2 | conjecture |
| 6.23 | Lemma | Σ scaling | `sigma-scaling` | T12 | proved |
| 6.24 | Proposition | Σ-independent gain | `sigma-independent-gain` | T12, T13 C2 | proved |
| 6.25 | Proposition | Σ-tracking gain with over-trust ρ | `sigma-overtrust` | T12, T13 C2 | proved |
| 6.26 | Proposition | Σ-tracking gain with misspecified λ′ | `sigma-misspecified-lambda` | T12, T13 C2 | proved |
| 6.27 | Proposition | Optimal filter along Σ | `sigma-optimal` | T12, T13 C2 | proved |
| 6.28 | Proposition | Signal sweeps (Σ and λ): optimal monotone | `signal-sweeps` | T11.1 | proved |
| 7.1 | Definition | Causal garbling | `causal-garbling` | — | definition |
| 7.2 | Theorem | Monotonicity under causal garbling | `causal-monotonicity` | T11.1, T11.2 | proved |
| 7.3 | Corollary | No optimal windows along causal orderings | `no-optimal-windows` | T11 | proved |
| 7.4 | Corollary | Diagnostic | `diagnostic` | T11 | proved |
| 7.5 | Proposition | Spectral dominance | `spectral-dominance` | T11.1, T11.3 | proved |
| 7.6 | Theorem | Causal; pathwise and spectral orderings coincide (Gaussian) | `gaussian-orderings-coincide` | T13 A8 | proved |
| 7.6a | Lemma | Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6) | `whole-path-garbling` | — | to-verify |
| 7.7 | Proposition | Which studied sweeps are ordered | `sweeps-ordered` | T11.1, T11.3 | proved |
| 7.8 | Theorem | Sharpness in the power family | `power-family-sharpness` | T11.3 (with diagnosis), T13 C2 | proved |
| 7.9 | Theorem | Unimodality for 0 < β < 2 | `power-family-unimodal` | T13 A4, T11.3 (numerical) | proved |
| 7.10 | Proposition | Duality | `power-family-duality` | T11.1, T11.3 | proved |
| 7.11 | Proposition | Latency | `latency` | T11.4, T13 C2 | proved |
| 7.12 | Counterexample | Pathwise ordering is not enough | `pathwise-not-enough` | T11.4 | proved |
| 7.13 | Proposition | Ordering sufficient; not necessary | `ordering-not-necessary` | T11.5 | proved |
| 7.14 | Corollary | Integrate-and-dump; nested grids | `mi-nested` | T11.6 | proved |
| 7.15 | Theorem | Integrate-and-dump on the continuum | `mi-continuum` | T13 A3, T11.6, T12 | proved |
| 7.16 | Proposition | M-P is not a causal-garbling family | `mp-not-ordered` | T12 | proved |
| 8.1 | Numerical result | Narrow windows need root-finding | `narrow-windows` | T10.5 | numerical |
| 8.2 | Numerical result | Blind searches find no unpredicted class | `blind-searches` | T10.7, T12 Part C, T13 C2 | numerical |
