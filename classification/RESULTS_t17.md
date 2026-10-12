# Results — Task 17: chapters 6–7 and the new §2.5 statements against the repository; repository sync items

- Pre-registration: `classification/PREREG_t17.md`, commit **d23797b**.
- Artifacts checked: commit **81e977c**. E1–E4, E6 and E7 ran once on it (6 s; `t17/results/t17_checks.log`, `.time`); E5's evidence was gathered after that run with the session's web search.
- Results: raw outputs **ddbceb6**; manual readings and post-hoc diagnosis **04315a3**; this report follows.

## Checks

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| E1 New proof steps (A1) | **FAIL** | 7 of 9 items hold; item 3 not shown in the recorded run (50-digit precision; holds exactly and at adequate precision post hoc); item 6: Corollary 7.4's proof as written does not cover two clauses | 3.45 |
| E2 Statements (A2) | **PASS** | 48 results: 30 without a difference, 18 with a wording-level difference (all kind a); no kind (b), (c) or (d) | 0.21 |
| E3 Numbers (A3) | **FAIL** | 87 of 88 values match; mismatch: T11.3 values of beta (printed 37, source 129.0) | 0.66 |
| E4 Cross-references (A4) | **FAIL** | 48 citation groups, 0 unresolved; first citation in order for [1]–[53]; 425 typed references, 1 wrong type (Prop. 6.10–6.12: 6.11 type is Counterexample, not Proposition); 34 table labels exist; 12 figure references, 0 unknown | 0.13 |
| E5 Prior-work sentences (A4) | **FAIL** | 13 sentences: 10 supported, 1 claims more (§7.3, [47]), 2 undetermined (titles and search summaries only; abstracts unreachable) | — |
| E6 Escaped citations (B.1) | **PASS** | 0 escaped groups in any render; 17 citations = baseline 15 + 2 from the new thesis-only texts | 0.59 |
| E7 Legacy labels (B.3) | **PASS** | 0 flagged; 85 figure labels exempt, Appendix E included; 1 'Paper 1' (Appendix D's quotation, reported) | 0.07 |

**Pre-registered checks that FAIL:** E1, E3, E4, E5. Each stays a failure; diagnoses below.

## Diagnoses

- **E1 item 3 (attribution: code).** The numeric test of "the optimal prior M < F" ran at 50 digits. Where e^(−2λΔt) < 10⁻⁵⁰ (large λΔt in the log-uniform draw) F − M = O(F·e^(−2λΔt)) is below working precision and M = F numerically: 102 of 1,000 sets, every printed example with M = F to all printed digits. Exactly, the steady prior is the positive root of an upward parabola f with f(0) < 0 and f(F) = F²a² > 0, so M < F; and the same test with the precision raised above 2λΔt/ln 10 digits (seed 17003, the spare) gives 0 of 1,000. Every symbolic part of item 3 reduced to 0 in the recorded run.
- **E1 item 6 (attribution: document).** Corollary 7.4 is true, but its proof ("Corollary 7.3, and Proposition 7.7(a)") does not cover the exclusion of All along precision, which needs σ⋆² → 0 (Proposition 3.5), nor the last clause, which is Theorem 5.1 (named in the statement). See `t17/results/e1_item6_review.md`.
- **E3 (attribution: document).** "Theorem 7.8: T11.3 over 37 values of β": Task 11 ran 129 values (β = k/20, k = −40…80, plus {0, 2} ± {10⁻⁶, 10⁻³}, as its pre-registration says). The "37" is in the repository's own label of Theorem 7.8 (`source/Stages_0_4_Source.md`) and was carried into the draft. This was seen while locating the sources, after the pre-registration commit (PREREG_t17 disclosure 8).
- **E4 (attribution: document).** §6.7's summary table cites "Prop. 6.10–6.12"; 6.11 is a Counterexample. The pre-registered rule requires every member of a typed range to have the type.
- **E5 (attribution: document).** §7.3 says coloured measurement noise is a standard setting "for analysing mis-specified time correlation [47]"; [47] studies time-correlated **model error** in Kalman smoothers. §6.2's wording ("time-correlated errors") is supported. Two further sentences are undetermined because no abstract could be reached (doi.org and Crossref are refused by the session's network policy).

## Disclosure

- Before the recorded run each check was run once with its output discarded (only to see that it ran), and the E3 source anchors and the E2 extraction were checked for completeness (all found). No code error appeared; nothing was changed.
- While locating the E3 sources (after the pre-registration commit) the "37 vs 129" discrepancy was seen; the check was not changed.
- E1 item 6, E2's classification and E5 are manual readings after the recorded run (`t17/results/`).

## Files changed

- `register/render.py` (thesis-only overrides, thesis render only); new `register/thesis_overrides.yaml`.
- New `source/thesis_only/`: `stationary-variance.md` (3.1), `optimal-envelope.md` (3.5, 3.6 and their proof), `plateaus.md`, `equal-height-maxima.md`, `degenerate-points.md`, `pair-birth.md` (2.4–2.7), `discrete-excess.md` (6.13); `normal-form.md` and `tau-optimal-normal-form.md` with citations unescaped. `source/Stages_0_4_Source.md` unchanged.
- Renders: `Stages_0_4_Thesis.md`, `Appendix_D_Verification.md` (draft layout; Tasks 15–17 entries), `Appendix_E_Reproduction.md` (T17 row and chain step).
- `t15/make_appendix_de.py` (Appendix D layout, Task 15–17 failures, chain).
- New: `t17/make_thesis_only_t17.py`, `t17/t17_checks.py`, `t17/t17_diag.py`, `t17/make_results_t17.py`, `t17/input/`, `t17/results/`.

## For the author

### 1. A1: the new proof steps

| Item | Verdict | Evidence |
|---|---|---|
| 1 Cor 6.5 | holds | Πb = 2λ(1 + νt) and Π²D = 4λ²((1 + νt)² + ν(1 − t)²) reduce to 0; with Π√D = 2λ√(…) (both positive) P/F reduces to the stated form; t = 0 gives 2/(1 + √(1 + ν)). |
| 2 Lemma 6.1 normal form | holds | σ²/F − 𝒱_τ reduces to 0; σ² − F = (G/a)(G/(2Π(1 + aτ)) − F), so σ² > F iff q > 2(1 + aτ); 0 counterexamples in 1,000. |
| 3 Prop 6.13 | holds post hoc; not shown in the recorded run (code) | P⁻ from P⁻ = a²P⁺ + q, P⁺ = (1 − L)²P⁻ + L²r; the numerator a²L(Lr − F(2 − L)); P⁺ − F = (P⁻ − F)/a²; L⋆/(2 − L⋆) = P⁻/(P⁻ + 2r): all reduce to 0; P⁻ > F iff L/(2 − L) > φ: 0 counterexamples. The optimal prior's M < F was not shown at 50 digits for 102 sets with e^(−2λΔt) < 10⁻⁵⁰; it holds exactly (f(F) = F²a² > 0) and at adequate precision (diagnosis). |
| 4 Lemma 6.14 | holds | the identity and the definition of P̄ as the time average of e^(−2λt)P⁺ + F(1 − e^(−2λt)) reduce to 0. |
| 5 Lemma 6.23 | holds | σ²/F = (1 + g²/u)/(1 + g) reduces to 0; (Σ, Π) pairs with equal u give equal σ²/F to 10⁻⁴⁰ (1,000 sets); u is a bijection of Σ and of Π, so the relative failure sets coincide. |
| 6 Cor 7.4 | fails as written | fails as written: the proof does not cover the exclusion of All (needs σ⋆² → 0) or the last clause (Theorem 5.1); the corollary itself is true. |
| 7 Prop 2.7 | holds | roots ±√(bδ); ∫ a(x² − bδ) between them = −(4/3)a(bδ)^(3/2): residual 0. |
| 8 Thm 7.8 bound | holds | B > 0 gives B + √(B² + 4AC) > 2√(AC), so P < √(C/A); 0 counterexamples; C/A = 2ΣKτ^β/(1 − λτ)² reduces to 0. |
| 9 Prop 7.10 | holds | A(1/(λ²τ)) = A(τ) and v_(2−β, Kλ^(2−2β))(1/(λ²τ)) = v_(β,K)(τ) reduce to 0; P equal to 10⁻³⁵ in 1,000 sets with β ∈ (−3, 5). |

### 2. A2: statements

No difference beyond typography in: 2.4, 2.6, 6.1, 6.2, 6.3, 6.6, 6.7, 6.8, 6.10, 6.12, 6.14, 6.15, 6.16, 6.17, 6.18, 6.19, 6.20, 6.21, 6.22, 6.24, 6.25, 6.26, 6.28, 7.2, 7.3, 7.4, 7.9, 7.10, 7.13, 7.15.

No difference of kind (b), (c) or (d). The wording-level differences (all kind a):

**2.5, kind (a).** The equality condition is cited as Theorem 2.2(3); the repository writes Theorem 2.2(c). The draft numbers Theorem 2.2's parts (1)-(4), the repository (a)-(d).

- Draft: (the equality condition of Theorem 2.2(3))
- Repository: (the equality condition of Theorem 2.2(c))

**2.7, kind (a).** The draft states what "nondegenerate fold" means (in a local coordinate x, dσ²/dθ ≈ a(x² − bδ), a, b ≠ 0) and the side of birth (bδ > 0); the repository says "through a nondegenerate fold of N" at distance δ from θ₀. Same result, written out.

- Draft: Suppose a minimum–maximum pair is born as a family parameter passes δ = 0 through a nondegenerate fold: near the birth point, in a local coordinate x, dσ²/dθ ≈ a(x² − bδ) with a, b ≠ 0. Then for bδ > 0 the turning-point positions separate like δ^(1/2) and the values like M − m ~ δ^(3/2) …
- Repository: If a minimum–maximum pair is born at θ₀ through a nondegenerate fold of N, then at distance δ from θ₀ the turning-point positions separate like δ^{1/2} and the values like M − m ~ δ^{3/2} …

**6.4, kind (a).** The draft cites [27, 28, 45] for measurement differencing inside the statement; the repository attaches the same citations in the register.

- Draft: With measurement differencing [27, 28, 45], z = ẏ + y/τ, …
- Repository: With measurement differencing (z = ẏ + y/τ), …

**6.5, kind (a).** Same formula. The repository has it inside the thesis-only §3.8 text (no separate labelled statement); the draft states it as Corollary 6.5 with a proof.

- Draft: With ν = 2ΣΠ/λ² and t = λτ, P/F = 2/(1 + νt + √((1 + νt)² + ν(1 − t)²))
- Repository: P/F = 2/(1 + νt + √((1 + νt)² + ν(1 − t)²)) … The second formula is the optimal filter along τ (Corollary 6.5)

**6.9, kind (a).** The draft adds the reading "no constant-gain relay is optimal under coloured noise", which is what P < V = inf over G says.

- Draft: P(τ) < V(τ) for every τ > 0: no constant-gain relay is optimal under coloured noise.
- Repository: P(τ) < V(τ) for every τ > 0.

**6.11, kind (a).** The repository's title carries "analytic;" and quotes "the starting study's" claim; content identical.

- Draft: The statement "the optimal filter never produces a window" holds along precision …
- Repository: The starting study's "the optimal filter never produces a window" holds along precision …

**6.13, kind (a).** Restated in the M-P notation of §6.3 (a² for ϕ², P⁻ for M_L, P⁺ for S_L, φ = FΠΔt for FΠ_d, Δt > 0 for Π_d > 0). The draft does not restate S_L = (1 − L)²M_L + L²r (it is §6.3's fixed-gain formula for P⁺) and adds the gain range 0 ≤ L < 2 (the register title has it).

- Draft: For a fixed gain 0 ≤ L < 2, the prior error is P⁻ = (a²L²r + q)/(1 − a²(1 − L)²), P⁺ − F = (P⁻ − F)/a², and P⁻ > F iff P⁺ > F iff L/(2 − L) > φ. The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < φ/2 for every Δt > 0.
- Repository: M_L = (ϕ²L²r + q)/(1 − ϕ²(1 − L)²), S_L = (1 − L)²M_L + L²r, S_L − F = (M_L − F)/ϕ², and M_L > F ⟺ S_L > F ⟺ L/(2 − L) > FΠ_d. The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < ½FΠ_d for every Π_d > 0. (manuscript, Paper 1, Proposition 6, p. 7)

**6.23, kind (a).** Title "(Σ scaling)" vs "(scaling)"; statement identical.

- Draft: Lemma 6.23 (Σ scaling). σ²/F = (1 + g²/u)/(1 + g). …
- Repository: Lemma 6.23 (scaling). σ²/F = (1 + g²/u)/(1 + g). …

**6.27, kind (a).** The draft names the quantity (σ⋆² increasing; σ⋆²/F = 2/(1 + √(1 + u))); the repository leaves it implicit under the title "optimal".

- Draft: Absolute: σ⋆² is increasing from 0, class upper ray. Relative: σ⋆²/F = 2/(1 + √(1 + u)) is decreasing, classes lower ray and Empty.
- Repository: Absolute: increasing from 0, class upper ray. Relative: 2/(1 + √(1 + u)) is decreasing, classes lower ray, Empty.

**7.1, kind (a).** Same definition; the draft adds an informal gloss after it.

- Draft: … and (s, Y′) has the same joint law as (s, Y_θ₁). In words: the worse observations can be manufactured from the better ones as they arrive …
- Repository: … such that (s, Y′) =d (s, Y_θ₁).

**7.5, kind (a).** "white components written as constant densities" vs "white components in integrated form as constant densities"; "realises" vs "realizes".

- Draft: (white components written as constant densities)
- Repository: (white components in integrated form as constant densities)

**7.6, kind (a).** Title only ("the orderings coincide for Gaussian noise" vs "non-linear causal garblings add nothing"); the four equivalent conditions are the same.

- Draft: Theorem 7.6 (the orderings coincide for Gaussian noise). … the following are equivalent: (i) … (iv) …
- Repository: Theorem 7.6 (non-linear causal garblings add nothing). … the following are equivalent: (i) … (iv) …

**7.7, kind (a).** Title "(which studied sweeps are ordered)" vs "(the sweeps studied)"; the draft drops the parenthesis "(real for τ₂ > τ₁)" after the garbling filter, which is implied by τ₂ > τ₁ in (b).

- Draft: The garbling noise is the second-order process S_ξ(ω) = … , H_ξ(s) = …
- Repository: The garbling noise has S_ξ(ω) = … , H_ξ(s) = …, a second-order process (real for τ₂ > τ₁).

**7.8, kind (a).** Title only ("sharpness in the power family" vs "sharpness of the ordering condition").

- Draft: Theorem 7.8 (sharpness in the power family).
- Repository: Theorem 7.8 (sharpness of the ordering condition).

**7.11, kind (a).** The draft writes the window band explicitly in the class list (σ⋆² < R² < P(1/e)); the repository gives it in the previous sentence.

- Draft: The classes along θ are All (R² ≤ σ⋆²), window (σ⋆² < R² < P(1/e)) and Empty (R² ≥ P(1/e)).
- Repository: Classes along θ: All (R² ≤ σ⋆²), window, Empty (R² ≥ P(1/e)).

**7.12, kind (a).** The repository's title carries "analytic;"; "not monotone" vs "non-monotone".

- Draft: Counterexample 7.12 (pathwise ordering is not enough). …
- Repository: Counterexample 7.12 (analytic; pathwise ordering is not enough). …

**7.14, kind (a).** "the average of the m fine samples completed by the time it is taken" vs "… completed by the time it is" (the repository's sentence is truncated).

- Draft: each coarse M-I sample is the average of the m fine samples completed by the time it is taken: a causal garbling.
- Repository: each coarse M-I sample is the average of m fine samples completed by the time it is, a causal garbling.

**7.16, kind (a).** The repository's statement contains its argument; the draft states "ordered in neither direction" and gives the same argument as a proof.

- Draft: Along Δt, the point-sampled model is ordered in neither direction.
- Repository: In neither direction: by Theorem 7.2 an ordering would give a pointwise-in-t inequality … but post falls while prior and avg rise (Theorem 6.19).

**Proofs.** Results whose draft carries a proof where the repository source has none (from a2_pairs.md). The prompt names 6.9 and 7.4; 6.9 has a proof in the repository source too. Results: 6.5, 6.13, 6.14, 6.20, 6.23, 7.4, 7.7, 7.14, 7.16.

**Edits named in the prompt.** 6.13 in the M-P notation: equivalent (above). 6.9 and 7.4 carry proofs in the draft: 7.4's is incomplete as written (A1 item 6); 6.9's matches the repository's. 7.6's title: wording only.

### 3. A3: numbers

| # | Value | Printed | Computed or stored | Source | Match |
|---|---|---|---|---|---|
| 1 | V_w | 0.09 | 0.09 | Prop. 6.2 | yes |
| 1 | H_G | 0.0066667 | 0.00666666666667 | Prop. 6.2 | yes |
| 1 | tau_F | 16 | 16.0 | Prop. 6.3 | yes |
| 1 | sigma^2(1) | 0.04 | 0.04 | Lemma 6.1 | yes |
| 1 | sigma^2(10) | 0.011875 | 0.011875 | Lemma 6.1 | yes |
| 1 | sigma^2(16) | 0.01 | 0.01 | Lemma 6.1 | yes |
| 2 | sigma*^2 | 0.0099505 | 0.00995049383621 | Prop. 6.4 at tau -> 0 | yes |
| 2 | P(1) | 0.0098039 | 0.00980392156863 | Prop. 6.4 | yes |
| 2 | P(10) | 0.0067813 | 0.00678130331424 | Prop. 6.4 | yes |
| 2 | V(1) | 0.0099010 | 0.00990098767242 | min over G of Lemma 6.1 at tau = 1 (interior minimum vs the G -> infinity limit) | yes |
| 3 | post at dt -> 0 | 0.09 | 0.09 | M-P formula | yes |
| 3 | post maximum | 0.20457 | 0.204573403878 | M-P formula | yes |
| 3 | argmax | 2.4645 | 2.46449931597 | M-P formula | yes |
| 3 | post at dt -> infinity is 0 | -> 0 | yes | M-P formula | yes |
| 3 | dt_E = 100 to 20 digits | 100 | yes | tanh lemma root 99.99999999999999999996143 | yes |
| 3 | avg at dt = 200 | 0.0099875 | 0.0099875 | M-P formula | yes |
| 3 | dip at dt = 200 | 0.125% | 0.00125 | M-P formula | yes |
| 3 | avg minimiser (reported; the draft says 'at dt = 200') | 200 | 200.0 | M-P formula | yes |
| 4 | D2 c = 3: P+ > F at every dt (2,000-point grid) | P+ > F | yes | M-P formula | yes |
| 4 | D2 c = 3: P+ -> 4F | 4 | 4.00000888 | M-P formula at dt = 1e8 | yes |
| 5 | P(0) | 0.0099505 | 0.00995049383621 | Prop. 7.11 | yes |
| 5 | P(1/e) | 0.0099763 | 0.00997627953209 | Prop. 7.11 | yes |
| 6 | G = 0.019 avg: maximum then minimum | max, min | yes | sign sequence [1, -1, 1] | yes |
| 6 | minimum below the starting value | below start | yes | M-P formula | yes |
| 7 | 178 of 1,000 (2 < rho <= 2 + u, no onset) | 178 | 178.0 | t12/RESULTS_t12.md | yes |
| 7 | sets per family | 2000 | 2000.0 | t12_a8.json N | yes |
| 7 | 6,000 sets | 6000 | 6000.0 | t12_a8.json sets | yes |
| 7 | x 3 metrics | 3 | 3.0 | t12/RESULTS_t12.md A8 row (metrics listed) | yes |
| 7 | D3 excess set at R2 = F: lower ray or Empty | 1000 | 1000.0 | t12 A4 shapes | yes |
| 8 | 1,000 tolerances (degenerate point) | 1000 | 1000.0 | t10/RESULTS_t10.md | yes |
| 8 | exponent (values) | 1.50007 | 1.50007 | t10/RESULTS_t10.md | yes |
| 8 | exponent (positions) | 0.50002 | 0.50002 | t10/RESULTS_t10.md | yes |
| 9 | T9.4 classifications | 80000 | 80000.0 | t9 RESULTS | yes |
| 9 | T9.2 Wiener route agreement | 2 × 10^-17 | 2.1e-17 | t9 RESULTS T9.2 (max of the three) | yes |
| 9 | T9.5 flags: not strictly decreasing | 285 | 285.0 | t9 RESULTS | yes |
| 9 | T9.5 flags: V < P | 13 | 13.0 | t9 RESULTS | yes |
| 9 | T13 A7 sets | 10000 | 10000.0 | t13 RESULTS | yes |
| 9 | T13 A7 digits | 60 | 60.0 | t13 RESULTS | yes |
| 9 | T10.6 three routes | 1.0 × 10^-14 | 1.01e-14 | t10 RESULTS | yes |
| 9 | T10.6 shape exact to 1e-50 | <= 10^-50 | yes | t10_6.json shape.max_pos_rel_err | yes |
| 10 | A2 D1 sets matching | 1000 | 1000.0 | t12 RESULTS | yes |
| 10 | A3 D2 sets matching | 1000 | 1000.0 | t12 RESULTS | yes |
| 10 | A2 dt_E to 1e-30 | 1 × 10^-30 | 1.14e-30 | t12 | yes |
| 10 | A4 sets agreeing | 1000 | 1000.0 | t12 RESULTS | yes |
| 10 | A4 membership tests | 201514 | 201514.0 | t12 RESULTS | yes |
| 10 | T13 A1 sets | 10000 | 10000.0 | t13 RESULTS | yes |
| 10 | T13 A1 digits | 100 | 100.0 | t13 RESULTS | yes |
| 10 | T12 A6 points | 400000 | 400000.0 | t12 RESULTS | yes |
| 11 | B4 census sets | 2000 | 2000.0 | t12 RESULTS | yes |
| 11 | maximum's position error | 6 × 10^-31 | 6.05e-31 | t12 RESULTS | yes |
| 12 | T11.3 spectral pairs | 25000 | 25000.0 | t11 RESULTS | yes |
| 12 | T11.3 values of beta | 37 | 129.0 | t11_3.json by_beta (distinct beta) | **no** |
| 12 | T13 A4 curves | 10000 | 10000.0 | t13 RESULTS | yes |
| 12 | T11 unimodality curves | 12900 | 12900.0 | t11 RESULTS | yes |
| 12 | T11.3 duality | 8 × 10^-51 | 7.79e-51 | t11 RESULTS | yes |
| 12 | T11.4 Monte Carlo |z| | 1.91 | 1.91 | t11 RESULTS | yes |
| 12 | T11.5 sets | 1000 | 1000.0 | t11 RESULTS | yes |
| 12 | T11.6 pairs | 9000 | 9000.0 | t11 RESULTS | yes |
| 12 | T13 A3 closed form and limits 11 of 11 | 11 | 11.0 | t13 RESULTS | yes |
| 12 | T13 A3 sets | 10000 | 10000.0 | t13 RESULTS | yes |
| 12 | T11.6 continuum points | 400000 | 400000.0 | t11_6.json | yes |
| 12 | T12 A9 points | 400000 | 400000.0 | t12 RESULTS | yes |
| 12 | T12 A10 pairs | 1000 | 1000.0 | t12 RESULTS | yes |
| 13 | audit row 13 is 'tau ZF relay…' | tau ZF relay | yes | row name 'tau ZF relay' | yes |
| 13 | audit row 14 is 'tau ZF optimal…' | tau ZF optimal | yes | row name 'tau ZF optimal' | yes |
| 13 | audit row 15 is 'tau var relay…' | tau var relay | yes | row name 'tau var relay' | yes |
| 13 | audit row 16 is 'tau var optimal…' | tau var optimal | yes | row name 'tau var optimal' | yes |
| 13 | audit row 17 is 'power…' | power | yes | row name 'power beta<=0' | yes |
| 13 | audit row 18 is 'power…' | power | yes | row name 'power 0<beta<2' | yes |
| 13 | audit row 19 is 'power…' | power | yes | row name 'power beta>=2' | yes |
| 13 | audit row 20 is 'delay…' | delay | yes | row name 'delay' | yes |
| 13 | audit row 24 is 'dt…' | dt | yes | row name 'dt D1 post' | yes |
| 13 | audit row 25 is 'dt…' | dt | yes | row name 'dt D1 prior' | yes |
| 13 | audit row 26 is 'dt…' | dt | yes | row name 'dt D1 avg' | yes |
| 13 | audit row 27 is 'dt…' | dt | yes | row name 'dt D2 post' | yes |
| 13 | audit row 28 is 'dt…' | dt | yes | row name 'dt D2 prior' | yes |
| 13 | audit row 29 is 'dt…' | dt | yes | row name 'dt D2 avg' | yes |
| 13 | audit row 30 is 'dt…' | dt | yes | row name 'dt D3 post' | yes |
| 13 | audit row 31 is 'dt…' | dt | yes | row name 'dt D3 prior' | yes |
| 13 | audit row 32 is 'dt…' | dt | yes | row name 'dt D3 avg' | yes |
| 13 | audit row 35 is 'Sigma…' | Sigma | yes | row name 'Sigma B2 abs' | yes |
| 13 | audit row 36 is 'Sigma…' | Sigma | yes | row name 'Sigma B2 rel' | yes |
| 13 | audit row 37 is 'Sigma…' | Sigma | yes | row name 'Sigma B3 abs' | yes |
| 13 | audit row 38 is 'Sigma…' | Sigma | yes | row name 'Sigma B3 rel' | yes |
| 13 | audit row 39 is 'Sigma…' | Sigma | yes | row name 'Sigma B4 abs' | yes |
| 13 | audit row 40 is 'Sigma…' | Sigma | yes | row name 'Sigma B4 rel' | yes |
| 13 | audit row 41 is 'Sigma…' | Sigma | yes | row name 'Sigma B5 abs' | yes |
| 13 | audit row 42 is 'Sigma…' | Sigma | yes | row name 'Sigma B5 rel' | yes |

### 4. A4: references and prior-work judgements

Mechanical: 48 citation groups resolve; first citations of [1]–[53] are in order; one typed reference spans a wrong type ("Prop. 6.10–6.12" includes Counterexample 6.11); all figure references exist. Excluded as non-citations: `[0, ∞]`; `[1.01, 10]`; `[0, ∞]`; `[c + 2(1 − c)FΠ₀]` and 12 more bracketed formulas.

Prior-work judgements (evidence in `t17/results/e5_sources.md`):

| # | Where | Sentence (draft) | Cited | Verdict | Reason |
|---|---|---|---|---|---|
| S1 | §6.3, after Prop. 6.13 | "L/(2 − L) is the discrete-time variance factor α/(2 − α) of an exponentially weighted average [26]" | 26 | **undetermined** | The paper derives performance indices for α–β–γ trackers with acceleration measurements; the summaries do not show α/(2 − α) or an exponentially weighted average. The factor itself is textbook (the α-filter's noise-reduction ratio), but whether [26] states it could not be checked. |
| S2 | §6.1, Prop. 6.4 | "With measurement differencing [27, 28, 45], z = ẏ + y/τ, the optimal stationary error is …" | 27, 28, 45 | **supported** | [27] is the continuous-time optimal filter with coloured measurement noise; [28] the sampled-data counterpart; [45] revisits the Kalman filter with coloured measurement noise. Citing them for the differencing method is consistent with all three summaries. |
| S3 | §6.2 | "Filtering under coloured measurement noise is standard, by state augmentation or measurement differencing [27, 28, 45, 46], …" | 27, 28, 45, 46 | **supported** | As S2; [46]'s title is Kalman/UFIR estimation with coloured measurement noise (the paper itself was not returned; related Shmaliy work uses measurement differencing). |
| S4 | §6.2 | "… and the effect of mis-specified time-correlated errors on Kalman smoothing has been studied [47]." | 47 | **supported** | [47] studies misspecified temporal correlation of model error in (ensemble) Kalman smoothers. "Time-correlated errors" is general enough to cover model error. |
| S5 | §7.3 | "Coloured measurement noise is a standard setting for filter design [27, 28, 45, 46] and for analysing mis-specified time correlation [47]" | 27, 28, 45, 46, 47 | **claims more** | The first half is supported (as S3). The second half makes [47] an analysis of mis-specified time correlation **in coloured measurement noise**; [47]'s abstract is about time-correlated **model error** (process noise) in a smoother, not measurement noise. |
| S6 | §6.4 | "a trade-off in the sampling rate, with an optimum once delays are priced in, is known [48]" | 48 | **supported** | Title: "Analysis of the optimal sampling rate for state estimation in sensor networks with delays". The abstract was not returned; the sentence claims no more than the title. |
| S7 | §7.5 | "… an interior optimal sampling interval needs some other cost, such as the network delays of [48]." | 48 | **supported** | As S6. |
| S8 | §7.1 | "Monotonicity of optimal performance under garbling goes back to Blackwell's comparison of experiments [18, 19] and Le Cam's theory [49, 50]." | 18, 19, 49, 50 | **supported** | Blackwell's theorem equates garbling with universal preference (every decision maker does at least as well with the more informative experiment); Le Cam's deficiency and Torgersen's book generalise it. |
| S9 | §7.1 | "It extends to sequential experiments [20] and to observation channels and information structures in stochastic control and teams [21–23]." | 20, 21, 22, 23 | **supported** (as a group) | [20] is the sequential generalisation; [22] has chapters on comparing information structures; [23]'s title is the Blackwell ordering of information structures. [21]'s summary concerns optimisation and continuity of observation channels (concavity of the cost in the channel), not garbling explicitly; it supports "observation channels in stochastic control" but the monotonicity claim rests on [22, 23]. |
| S10 | §7.2 | "Theorem 7.6 extends the characterisation of linear normal experiments [24] (see also [50]) from static observations to stationary Gaussian processes ordered by their spectra; …" | 24, 50 | **supported** | [24]'s abstract: informativeness of linear normal experiments iff a Loewner (non-negative definite) ordering; [50] has a chapter on comparison of linear models. |
| S11 | §7.2 | "… a partial converse to Blackwell ordering for information structures is known in the game setting [51]." | 51 | **supported** | [51]'s title and abstract: comparison of information structures for zero-sum games, with a partial converse to Blackwell ordering (stated in standard Borel spaces). |
| S12 | §7.4 | "the prediction covariance of a delayed estimate is classical [29], …" | 29 | **undetermined** | [29] is a standard filtering-theory text; prediction error covariance is classical material, but the summaries do not show the book's treatment of delayed estimates. |
| S13 | §7.4 | "… and out-of-sequence and delayed measurements are handled in tracking [52, 53]." | 52, 53 | **supported** | [52]: exact update for out-of-sequence measurements caused by transmission delays; [53]: the decaying merit of a delayed (out-of-sequence) observation. |

### 5. Other disagreements in chapters 1–7 (listed, not resolved)

1. **"37 values of β"** (§7.6 verification of Theorem 7.8) and the repository's own label: Task 11 ran 129.
2. **"Prop. 6.10–6.12"** (§6.7 table) spans Counterexample 6.11.
3. **Theorem 2.2's parts** are numbered (1)–(4) in the draft and (a)–(d) in the repository. After this task's imports the thesis render carries the draft's 2.4 and 2.5, which cite "Theorem 2.2(1)–(2)" and "2.2(3)–(4)", next to the repository's Theorem 2.2 with parts (a)–(d).
4. **Proposition 2.7's proof:** the draft gives the value change as (4/3)|a|(bδ)^(3/2); the repository's proof writes (4/3)a(bδ)^(3/2) without the absolute value (A1 item 7 confirms the draft).
5. **[26]** (§6.3) is cited for the variance factor α/(2 − α) of an exponentially weighted average; the search summaries of [26] (α–β–γ trackers with acceleration measurements) do not show it.
6. **[21]** (§7.1) is cited for monotonicity under garbling in stochastic control; its abstract concerns optimisation and continuity of observation channels. [22, 23] carry the comparison of information structures.
7. **Bryson and Henrikson [28]** is dated 1968 in the bib (the journal version); the search found the 1967 Harvard report of the same work.
8. **Corollary 7.4's proof** (A1 item 6).
