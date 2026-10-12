# F4: chapter 9's claims, each with its source (manual, after the recorded run on f77ab8f; computed values in t18_checks.json F4)

| # | § | Claim | Source | Verdict |
|---|---|---|---|---|
| 1 | 9.1 | The shape of a failure set is fixed by the endpoint limits, turning-point values and two approach directions | Theorem 2.2(4) | matches |
| 2 | 9.1 | Every white-noise relay variance is σ²/F = 𝒱(ν, q) along a path; floor crossing q = 2; optimal filter = lower envelope | Theorem 3.2, Corollary 3.3, Proposition 3.5 | matches |
| 3 | 9.1 | Along precision the model forbids only a variance below the optimum; further restrictions belong to the gain family | Theorem 5.1, Corollaries 5.2–5.3, §5.2–5.5 | matches |
| 4 | 9.1 | Causal ordering ⇒ optimal filter cannot do worse; no optimal windows along ordered sweeps | Theorem 7.2, Corollary 7.3 | matches |
| 5 | 9.1 | Spectral test for additive Gaussian noise; sharp in the power family; sufficient not necessary; must be causal | Theorem 7.6, Theorem 7.8, Proposition 7.13, Counterexample 7.12 | matches |
| 6 | 9.1 | Diagnostic: window, two rays or mixed class along an ordered sweep certifies a miscalibrated filter | Corollary 7.4 | matches |
| 7 | 9.2 | Window conditions κ > 2 (Bayesian weight), F′ > 2F (misspecified Kalman), g > 2F (capped), ρ > 2 or λ′ < λ/2 (moving floor, relative tolerance) | Propositions 5.8, 5.9, 5.10, 6.25, 6.26 (source statements in t18_checks.json) | matches |
| 8 | 9.2 | "Below that threshold the relay never windows" | the same propositions: strictly decreasing (5.8, 5.9, 5.10) or no window (6.25, 6.26) below the threshold | matches for the families listed. The Hill gain is not listed: its window condition is c/(FΠ₀) > 4, i.e. sup q > 2 (Theorem 3.4), and it has a window component in the mixed class below that (Proposition 5.13); "all have the same form" holds for the listed families only |
| 9 | 9.2 | Peak 9.3F (Bayesian weight) and 17.6F (misspecified Kalman) at over-weighting ratio 100 | recomputed: 9.2875272, 17.575054 (both round as printed); §5.3 text after Proposition 5.9 | matches; the parenthesis cites Proposition 5.9 only, but the Bayesian value comes from Proposition 5.8's formula (same paragraph of §5.3) |
| 10 | 9.2 | Hill mixed band median relative width 5 × 10⁻⁴ | `t10_4.json` band_rel_median 4.98 × 10⁻⁴; Proposition 5.13's paragraph | matches |
| 11 | 9.2 | Windows of relative width 10⁻⁸ occur | Numerical result 8.2 (source: 20/20 curves, 55 windows; T10.5) | matches |
| 12 | 9.2 | A grid-based check would miss them | Numerical result 8.2: a 10⁴-point log grid found none | matches |
| 13 | 9.2 | Prior dips as small as 10^(−32,880,317) | `t12/RESULTS_t12.md` ("between 10^-32880317 and 10^-17") | matches |
| 14 | 9.2 | Time-averaged dip 0.125 % in the worked example | recomputed: avg(200) = 0.0099875, dip 0.125 % (Task 17 E3 also) | matches |
| 15 | 9.3 | Scalar, stationary, linear scope | §1.7 | matches |
| 16 | 9.3 | Ornstein–Uhlenbeck signal throughout; chapter 2 applies to any curve | §3.1, §7.1 setting; Theorem 2.2's hypotheses C1–C6 | matches |
| 17 | 9.3 | Theorem 7.6 needs additive stationary Gaussian noise; Theorem 7.2 does not | statements of 7.5–7.6 and 7.2 | matches |
| 18 | 9.3 | Conventions: Σ half the diffusion intensity; samples carry 1/(ΠΔt); absolute or relative tolerance; time average primary; Theorem 6.19 depends on the noise scaling | Proposition 3.1 and §1.7; §6.3; §6.6; §6.3; §6.4 ("The statement depends on the scaling r = 1/(ΠΔt)") | matches |
| 19 | 9.3 | One parameter at a time; Theorem 2.2 does not describe multi-parameter regions | C1 (domain an interval) | matches |
| 20 | 9.4 (1) | Conjecture 6.22; census found no exception; mixed exponential rates defeat polynomial methods | repository §11 item 1 | matches |
| 21 | 9.4 (2) | Bound on turning points of two-stage sums; Corollary 5.4; natural sums open | repository §11 item 2 | matches (the draft omits the evidence line "at most 3 and 4 turning points in 2,000 sets") |
| 22 | 9.4 (3) | Necessary condition for monotone optimal error | repository §11 item 3 | matches |
| 23 | 9.4 (4) | Two-state α–β filter; decoupled multivariate splits; mixing case open | repository §11 item 4 | matches |
| 24 | 9.4 (5) | A gain that tracks correlation time: every gain along τ is set by precision alone | §6.1 ("The relay's gain is set by precision alone") | sourced in the draft; **not in the repository's open-problems section** |
| 25 | 9.4 (6) | Applications: none worked out | §1.7 ("applied relevance studies, which chapter 9 lists as future work") | sourced in the draft; **not in the repository's open-problems section** |

**Verdict.** Every claim has a source in the repository or the draft and matches it. Two notes: the "same form" claim (8) holds for
the families listed, not for the Hill gain; open problems 5 and 6 are new relative to the repository's §11 (which has items 1–4).
