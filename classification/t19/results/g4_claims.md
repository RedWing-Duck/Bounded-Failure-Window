# G4 (B4): chapter 9 claim table (manual, after the recorded run; computed values from t19_checks.json)

| § | Claim (current wording) | Source | Verdict |
|---|---|---|---|
| 9.1 | the shape is fixed by endpoint limits, turning-point values and two approach directions | Theorem 2.2(4) | matches |
| 9.1 | normal form σ²/F = 𝒱(ν, q); floor crossing q = 2; optimal filter the lower envelope | Theorem 3.2, Corollary 3.3, ch. 3 | matches |
| 9.1 | along precision the model rules out only a variance below the optimum | Theorem 5.1, Corollary 5.2 | matches |
| 9.1 | "for additive Gaussian noise the ordering is decided by the spectra (Theorem 7.6)" | register 7.6 "Causal; pathwise and spectral orderings coincide (Gaussian)" | matches |
| 9.1 | sufficient but not necessary in general; "sharp within the power-normalised family (Theorem 7.8)"; garbling must be causal | 7.13 (ordering not necessary), register 7.8 "Sharpness in the power family", Prop. 7.11 / Cex. 7.12 | matches |
| 9.1 | a window, two rays or mixed class along an ordered sweep shows miscalibration (Corollary 7.4) | Corollary 7.4 | matches |
| 9.2 | κ > 2, F′ > 2F, g > 2F, ρ > 2 or λ′ < λ/2; below threshold never window | Props 5.8, 5.9, capped gain, 6.25, 6.26 (register statements) | matches |
| 9.2 | Hill: "its window class needs sup q > 2, that is c/(FΠ₀) > 4" | sup q = (c/(FΠ₀))·sup_t t^(n−1)/(1 + tⁿ); for n = 2 the sup is 1/2 and the equivalence holds (symbolic); for n = 1.5, 3, 4 the threshold on c/(FΠ₀) is 3.780, 3.780, 3.510, and the equivalence fails in 15, 11, 24 of 1,000 random sets near the threshold. §5.4 defines the Hill gain for every real n > 1; the sentence names no n | **does not match as written** (holds for n = 2, the case of the §3 table and Prop. 5.13's worked example) |
| 9.2 | "below that threshold it can still produce a window component inside the mixed class (Proposition 5.13)" | Prop. 5.13 worked example n = 2: 25 ≤ Π₀ < 31.475, sup q = 100/(2Π₀) ≤ 2 (2.0 at 25, 1.589 at 31.475; Π₀^pair = 31.4750 in T10) | matches |
| 9.2 | peaks 9.3F and 17.6F at ratio 100 (Propositions 5.8 and 5.9) | recomputed 9.2875272 and 17.575054; 5.8 Bayesian weight, 5.9 misspecified Kalman | matches |
| 9.2 | Hill mixed band median relative width 5 × 10⁻⁴ (Prop. 5.13) | t10_4.json 4.98 × 10⁻⁴ | matches |
| 9.2 | windows of relative width 10⁻⁸ occur (Numerical result 8.2) | t10_5.json narrow: 20 of 20 curves, 55 windows | matches |
| 9.2 | prior dips as small as 10^(−32,880,317) (§6.5) | RESULTS_t12 | matches |
| 9.2 | time-averaged dip 0.125 % in the worked example | recomputed (avg(200) = 0.0099875) | matches |
| 9.2 | "the grid of Numerical result 8.2 missed every window of width 10⁻⁸" | t10_5.json: grid windows found 0 of 55 | matches |
| 9.3 | scalar, stationary, linear; OU signal; Theorem 7.6 needs Gaussian noise, 7.2 does not; conventions (§3.1, §6.3, §6.6, time average); one parameter at a time | the cited sections and statements | matches |
| 9.4(1) | Conjecture 6.22; census found no exception; mixes two exponential rates with 1/Δt | source §11 item 1; register 6.22 | matches |
| 9.4(2) | "at most 3 … Bayesian stages and at most 4 … Hill stages" in 2,000 random sets per family; Corollary 5.4; open | t10 two-stage census: bayes2 max 3 (7 sets), hill2 max 4 (63 sets), 2,000 each; source §11 item 2 | matches |
| 9.4(3) | sharp in the power family, not necessary in general (Prop. 7.13) | source §11 item 3 | matches |
| 9.4(4) | "A decoupled multivariate model is expected to split into scalar copies; the coupled case is open" | stated as an expectation; source §11 item 4 ("should split") | matches (expectation, not a result) |
| 9.4(5) | a gain that tracks correlation time | source §11 item 5 (Part A.3) | matches |
| 9.4(6) | applications | source §11 item 6 (Part A.3) | matches |

**G4 verdict: FAIL** — one claim does not match as written: the Hill equivalence sup q > 2 ⇔ c/(FΠ₀) > 4 holds for n = 2 only, and
§9.2 states it for the Hill gain without n. Attribution: document (correction: "for n = 2, c/(FΠ₀) > 4").
