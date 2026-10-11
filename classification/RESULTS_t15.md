# Task 15: sync the repository with the thesis draft (results)

- Pre-registration: `classification/PREREG_t15.md`, commit **aa0b914**.
- Artifacts checked: commit **41d5e43**. Checks C1–C10 and C13 and Part G (C11, C12) ran once on it.
- Results and diagnoses: commit **48c3088**.
- The planned post-run register change (status of 2.8 and 2.9) and the re-render of Appendices A and D are in the commit after the results.

## Check table

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| C1 Bibliography | **PASS** | 53 entries, 46 DOI, 0 VERIFY; dangling [], unused []; jazwinski1970 → ['latency'], simon2006 → ['stationary-variance', 'tau-relay-variance'] | 0.1 |
| C2 Reference register | **PASS** | numbers 1–53 unique and contiguous; bijection with the bib; equal to the frozen table; 46–53 planned | 0.02 |
| C3 Appendix C render | **PASS** | 53 lines against the draft's 53; 0 differences | 0.0 |
| C4 [n] rendering | **FAIL** | 19 thesis renders; hits: classification/Appendix_B_Figures.md: [['unresolved number', '[0, 10]']] | 0.26 |
| C5 Figures carry no numbers | **PASS** | 12 figures, 398 text elements inspected; 0 with a match | 0.02 |
| C6 Figure B.2 | **PASS** | touch at (ν_R, r) = (8.0, 0.5) exact; r = 1 boundary {0} ∪ {2}: True; ordering violations 0 at 10⁴ ν; negative q drawn 0 | 0.02 |
| C7 Figure data unchanged | **PASS** | all plotted arrays of B.1 and B.3–B.12 equal the original scripts' (11 figures) | 21.97 |
| C8 Roadmap §7 | **PASS** | rows 11–17 equal the Part D table; the line follows it; no 'query text not supplied'; rows 6–10 unchanged | 0.01 |
| C9 Appendix letters | **PASS** | 0 old-sense uses; 5/5 appendix files | 0.01 |
| C10 Thesis phrase check | **FAIL** | 0 'Paper 1' in 20 renders; A–E pattern matches: 81, all the new figure labels B.1–B.12 | 0.01 |
| C11 Corollary 2.8 | **PASS** | 1000 curves ({'smooth-inc': 250, 'pl-inc': 250, 'smooth-dec': 250, 'pl-dec': 250}), 50000 tolerances, 200000 classifications; class mismatches 0, signature mismatches 0, route disagreements 0; turning points per curve {'1': 481, '2': 390, '3': 114, '4': 14, '5': 1} | 467.3 |
| C12 Proposition 2.9 | **PASS** | 1000 cases on 500 curves ({'a': 500, 'b': 500}); mismatches 0; skipped 0; crossings {'1': 618, '2': 322, '3': 54, '4': 5, '5': 1} | 412.6 |
| C13 Reproduction unaffected | **PASS** | 89 paths; 0 unresolved | 0.04 |

**Pre-registered checks that FAIL:** C4 [n] rendering; C10 Thesis phrase check. Each is diagnosed below.

## Diagnoses

- **C4 (attribution: criterion/code).** 1 flagged item(s); 1 are interval notation in figure descriptions (e.g. 'theta in [0, 10]'), not citations. Attribution: criterion/code — the pre-registered bracket pattern cannot tell an interval from a citation. Item: `iecewise strictly monotone curve sigma^2(theta) on theta in [0, 10] (a sum of three Gau`.
- **C10 (attribution: criterion).** 81 A–E matches, 81 of them Task 15's figure labels B.1–B.12 (decision 3), 0 other; 0 'Paper 1'. The labels B.1–B.12 coincide in form, and for B.1–B.12 also in text, with the legacy labels B.1–B.12 of the crosswalk, so the pre-registered legacy-label pattern cannot pass once figures are labelled B.n. Attribution: criterion. No other A–E label and no 'Paper 1' remains anywhere, newlines included, so the Part H.1 miss is fixed.
- **Task 14 C9** (unused entries, unresolvable DOIs) is resolved by this task's input: the verified bib and the Part A attachments (C1 passes). `RESULTS_t14.md` is unchanged.
- **Development disclosure.** Before the recorded run, the Appendix C formatter was compared with the draft's list during development, as with T14's converter. The Part G code was smoke-tested on 8 curves (C11) and 6 curves (C12); those results are kept in `t15/results/t15_partG_smoke*.json`. The smoke test showed that the pre-registered monomial polynomials give mostly 1–2 turning points. The design was not changed. A separate, exploratory run on Chebyshev series is reported below and is not a pass criterion.

## Part G detail

- **C11** used 1000 pre-registered curves with 50 or more tolerances each, every critical value included.
- **Exploratory C11X** (not pre-registered): Chebyshev series of degree 9–12 with seeds 15301/15302 gave None curves with turning points None. Class mismatches None, signature mismatches None, route disagreements None.
- **C12:** 1000 cases. Two kinds of perturbation: (a) constant on each Nᵢ; (b) a smooth sum accepted only if strictly monotone on every Nᵢ. The class was unchanged in all cases with sup |δ| < η.
- **Illustration (not a criterion):** a wiggle of amplitude 0.9η inside N₁, violating only condition 2, changes the class from upper ray to (0, 1, 4) (route ii agrees: (0, 1, 4)); R² = 4.20894298926, η = 0.444631.
- **Ambiguity in Proposition 2.9, not blocking.** Condition 2 asks for σ̃² strictly monotone on each Nᵢ without naming the direction. Under condition 1 the ends of Nᵢ have opposite signs of σ̃² − R², which forces the direction of σ². Reading used: any strictly monotone σ̃² on Nᵢ. Generator (b) accepts either direction; only the forced one can occur.

## Files moved or created

- **Register:** `register/references.yaml`, `register/figures.yaml`, `register/bibfmt.py`; `register/render.py` extended (citation, figure and include tokens; paper numbering on paper-visible text); `register/results.yaml` (citations; status of 3.2 and 6.5; after the run, 2.8 and 2.9); `register/tasks.yaml` (wording only).
- **Sources:** `source/thesis_only/{signature, reparameterisation, structural-stability, normal-form, tau-optimal-normal-form}.md` (verbatim imports); edits to `source/Stages_0_4_Source.md`, `source/Roadmap_v3_Source.md`, `source/figs/*`, `source/phase1/ERRATA.md` (17 pages).
- **Renders:** `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (one line break moved), `Roadmap_v3.md`, `Appendix_A_Register.md`, new `Appendix_B_Figures.md`, `Appendix_C_References.md`, `Appendix_D_Verification.md`, `Appendix_E_Reproduction.md`, and `reference/phase1/`.
- **Figures:** `figs_thesis/B.n_<key>.png` (B.1–B.12) and `.pdf` (all except B.3, whose script writes PNG only); the captions `figs_thesis/B.n_<key>.txt` replace `figs_thesis/fig*.txt`. `figs_paper2/` is untouched.
- **Code:** `t15/` with `t15_register.py`, `make_sources_t15.py`, `fig_harness.py`, `make_figs_thesis.py` (writes `gen/gen_figs_t13.py` and `gen/gen_figs_t8.py`), `make_fig_B2.py`, `make_appendix_de.py`, `t15_checks.py`, `t15_partG.py`, `t15_diag.py`, `make_results_t15.py`, `bib_check.md`, `input/` (the draft and the prompt) and `results/`.

## Regenerate everything

From `classification/`:

```
python3 t15/t15_register.py
python3 t15/make_figs_thesis.py
python3 register/render.py --numbering thesis && python3 register/render.py --numbering paper
python3 t15/make_appendix_de.py --with-t15
python3 t15/t15_checks.py && python3 t15/t15_partG.py C11 C12 ILL
```

Appendix E gives the full chain, Tasks 1–15.

## For the author

### 1. Part H.2: the manuscript PDF

`reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf`: `pdfinfo` reports **17 pages**, producer pdfTeX-1.40.25, 462,929 bytes, sha256 `9f60625a98c1cdd23c96360e64eb511acba0ee45321dde95980ab6795070eedf`. This is the **same file** as yours.

- ERRATA's "18 pages" was my error: splitting `pdftotext` output on form feeds gives an empty 18th element. It is corrected to 17.
- Each cited page holds its quote (`pdftotext -f n -l n`): E1 p. 5 yes, E2 p. 5 yes, E3 p. 8 yes, E4 p. 12 yes.

### 2. Part C.4: what each figure plots

- **Figure B.1** (`stage1-schematic`; script `t13/t13_figures_paper2.py`). Left: a schematic piecewise strictly monotone curve sigma^2(theta) on theta in [0, 10] (a sum of three Gaussian bumps and a logistic step; no filtering parameters), its endpoint limits and turning-point values as dotted horizontal lines (the critical tolerances), turning points marked, and the failure set at the dashed tolerance R^2 = 1.25 shaded. Right: the class read off in each band between consecutive critical tolerances.
- **Figure B.2** (`normal-form-plane`; script `t15/make_fig_B2.py`). The (nu, q) plane, nu = 2 Sigma Pi/lambda^2 on a log axis from 1e-2 to 1e3 and q = G/(F Pi) from 0 to 5: the floor crossing q = 2, the optimal envelope q*(nu) = 2/(1 + sqrt(1 + nu)) (where the optimal variance ratio equals q*), and the tolerance boundaries V(nu, q) = R^2_rel for R^2_rel = 0.5, 1 and 2, with the point (nu_R, 0.5) where the R^2_rel = 0.5 boundary touches the envelope marked; only q >= 0 is drawn.
- **Figure B.3** (`design-sweeps`; script `t8_figures.py`). sigma^2 (log scale) at lambda = c = 1, Sigma = 0.01 along three design sweeps: (a) the prior sweep over Pi_0 from 1e-2 to 1e5 at Pi = 1 (case P3, U-shaped, with F, V_c, the minimum sigma*^2 and Pi_0* marked and a zoom inset near the minimum); (b) the prior sweep at Pi = 500 (case P1, monotone, with F and V_c marked); (c) the coupling sweep over c from 1e-4 to 10 at Pi = Pi_0 = 1, with F, sigma*^2, c* and c_F marked and a zoom inset.
- **Figure B.4** (`realizability`; script `t13/t13_figures_paper2.py`). sigma^2 against precision Pi (log axis) at lambda = 1, Sigma = 0.01 (F = 0.01): the optimal envelope sigma*^2(Pi) with the region below it shaded as unreachable, a Bayesian-weight base curve (kappa = 1.5) with three compactly supported bumps of peak 1.5F placed before the envelope touch point Pi_c = 56.7, the tolerance R^2 = 1.25F (three windows) and the tolerance R^2 = 0.6F with the forced lower ray (0, pi_R), pi_R = 222.2, marked.
- **Figure B.5** (`hill-phase`; script `t13/t13_figures_paper2.py`). Hill gain with n = 2 at lambda = c = 1, Sigma = 0.01: over the half-saturation Pi_0 (log axis), the turning-point values m/F (dashed) and M/F (solid) as tolerances R^2/F, the band m <= R^2 < min(M, F) shaded as the mixed class lower ray + window and the band F <= R^2 < M shaded as window, with vertical lines at the pair birth Pi_0^pair = 31.475 and the window onset c lambda/(4 Sigma) = 25.
- **Figure B.6** (`peak-heights`; script `t13/t13_figures_paper2.py`). Peak variance M/F against the initial over-weighting x for the Bayesian-weight gain (x = kappa) and the misspecified Kalman gain (x = F'/F) at lambda = lambda' = c = 1, Sigma = 0.01; both rise from 1 at x = 2, and the end values at x = 100 (9.2875 and 17.575) are annotated.
- **Figure B.7** (`tau-normalizations`; script `t13/t13_figures_paper2.py`). Stationary error against correlation time tau (log axes) at lambda = 1, Sigma = 0.01, Pi = 1 for the relay with G = 0.5 and the optimal filter. Left, matched zero-frequency power: both decrease, with F marked. Right, matched variance v = 0.05: the relay increases and the optimal error is unimodal with maximum P_max = 0.008333 at tau = 1/lambda; the optimal-filter failure set at R^2 = 0.8 P_max is shaded.
- **Figure B.8** (`optimal-sampling`; script `t13/t13_figures_paper2.py`). Optimal error against the sampling interval Delta t (log axis) in the point-sampled model at lambda = 1, Sigma = 0.01, Pi = 1 (per-sample noise variance 1/(Pi Delta t)): the error at sample times (post) falls from sigma*^2 towards 0, while the prior error and the time average rise from sigma*^2 to F; sigma*^2 and F are marked.
- **Figure B.9** (`sampled-relay`; script `t13/t13_figures_paper2.py`). Sampled relay D1 (gain 1 - exp(-G Delta t), G = 0.5, lambda = 1, Sigma = 0.01, Pi = 1) along Delta t (log axis). Left: the error at sample times with the window band R^2 in (0.09, 0.20457) shaded and the excess crossing Delta t_E = 100 marked. Right: the time average as avg/F - 1 on a symmetric-log axis, with the two-ray band between its minimum and F shaded and Delta t_E marked.
- **Figure B.10** (`process-noise`; script `t13/t13_figures_paper2.py`). The process-noise sweep at lambda = Pi = 1, against u = 2 Sigma Pi/lambda^2 (log axes), for the Sigma-independent gain (G = 1), the Sigma-tracking gain over-trusting precision by rho = 10, and the optimal filter. Left: absolute error. Right: relative error sigma^2/F, where the over-trusting gain rises above 1 to a peak of about 2.17 before falling.
- **Figure B.11** (`power-family`; script `t13/t13_figures_paper2.py`). Colour map of the optimal error relative to its supremum over tau, P/sup P, for the power-normalised family S = K tau^beta/(1 + tau^2 omega^2) at lambda = 1, Sigma = 0.01, K = 1, over the exponent beta (horizontal) and log10(lambda tau) (vertical); the position of the single maximum for 0 < beta < 2 is drawn, and the three regimes (ordered with information increasing in tau; spectra cross; ordered with information decreasing in tau) are labelled in words.
- **Figure B.12** (`delay`; script `t13/t13_figures_paper2.py`). Optimal filtering error P(d(theta)) for observations delayed by d(theta) = theta exp(-theta), at lambda = 1, Sigma = 0.01, Pi = 1, against theta (log axis): it rises from sigma*^2 = 0.0099505 to P(1/e) = 0.0099763 at theta = 1 and falls back; the optimal-filter failure set at R^2 = 0.0099634 is shaded, and theta = 1, where the causal order reverses, is marked.

### 3. Part C.2: text elements changed

- **B.1:** `class in each band (Theorem 2)` → `class in each band`
- **B.2:** new figure; its labels use words and symbols only.
- **B.3:** no text element changed (none carried a number).
- **B.4:** `realized curve with three windows (Corollary 48)` → `realized curve with three windows`
- **B.5:** no text element changed (none carried a number).
- **B.6:** no text element changed (none carried a number).
- **B.7:** no text element changed (none carried a number).
- **B.8:** no text element changed (none carried a number).
- **B.9:** no text element changed (none carried a number).
- **B.10:** no text element changed (none carried a number).
- **B.11:** `the single maximum (Theorem 25)` → `the single maximum`
- **B.12:** no text element changed (none carried a number).

### 4. Part F.3: statements of 3.1, 3.5 and 6.13 in the manuscript

**3.1 = Proposition 1 (p. 3).** "The stationary variance of (1) is σ²(Π) = (Σ + ½G²/Π)/(λ + G). (2) If G → 0 and G²/Π → 0 as Π → 0, then σ² tends to the floor F = Σ/λ. If G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F." Proof: x is an Ornstein–Uhlenbeck process with rate a = λ + G and noise intensity D = G²/Π + 2Σ, so its stationary variance is D/(2a).

**3.5 = Proposition 3 (p. 4), "steady-state Kalman–Bucy filter [9]".** "For this plant, the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives G⋆(Π) = pΠ = −λ + √(λ² + 2ΣΠ), σ⋆²(Π) = p = 2Σ/(λ + √(λ² + 2ΣΠ)). (4) G⋆ also minimizes (2) over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain." It continues: "This is standard. The remark used below is that σ⋆² decreases strictly from F, so G⋆ = σ⋆²Π ≤ FΠ."

**6.13 = Proposition 6 (p. 7).** "M_L = (ϕ²L²r + q)/(1 − ϕ²(1 − L)²), S_L = (1 − L)²M_L + L²r, S_L − F = (M_L − F)/ϕ², and M_L > F ⟺ S_L > F ⟺ L/(2 − L) > FΠ_d. (10) The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < ½FΠ_d for every Π_d > 0." Proof: see the manuscript's Appendix A (p. 14).

### 5. Part G outcomes

- **C11 (Corollary 2.8):** **PASS**, with class mismatches 0 and signature mismatches 0. The exploratory run with more turning points gave None and None.
- **C12 (Proposition 2.9):** **PASS**, 0 mismatches.
- **Illustration:** violating only condition 2 changes the class (upper ray → (0, 1, 4)).
- **Ambiguity:** see Part G detail above. It is not blocking.

### 6. Where references 46–53 belong

From the register's citation table: the result, the line of its heading in `classification/source/Stages_0_4_Source.md`, and the reference number.

| Ref. | Key | Result (thesis no., key) | Source line |
|---|---|---|---|
| [46] | shmaliy2020 | 6.10 `matched-variance-optimal` | 433 |
| [46] | shmaliy2020 | 7.8 `power-family-sharpness` | 480 |
| [47] | ren2021 | 6.10 `matched-variance-optimal` | 433 |
| [47] | ren2021 | 7.8 `power-family-sharpness` | 480 |
| [48] | martinezrey2017 | 6.19 `dt-optimal-mp` | 605 |
| [48] | martinezrey2017 | 7.16 `mp-not-ordered` | 643 |
| [49] | lecam1964 | 7.1 `causal-garbling` | 1036 |
| [49] | lecam1964 | 7.2 `causal-monotonicity` | 1042 |
| [50] | torgersen1991 | 7.1 `causal-garbling` | 1036 |
| [50] | torgersen1991 | 7.2 `causal-monotonicity` | 1042 |
| [50] | torgersen1991 | 7.5 `spectral-dominance` | 1070 |
| [50] | torgersen1991 | 7.6 `gaussian-orderings-coincide` | 1082 |
| [51] | hogeboomburr2021 | 7.5 `spectral-dominance` | 1070 |
| [51] | hogeboomburr2021 | 7.6 `gaussian-orderings-coincide` | 1082 |
| [52] | barshalom2002 | 7.11 `latency` | 1122 |
| [52] | barshalom2002 | 7.12 `pathwise-not-enough` | 1138 |
| [53] | yoder2018 | 7.11 `latency` | 1122 |
| [53] | yoder2018 | 7.12 `pathwise-not-enough` | 1138 |

### 7. Disagreements with the attached draft (listed, not resolved)

1. **Figure B.1 caption.** The draft calls it "the variance curve of the starting relay with its critical-tolerance diagram", and §2.4 says "the variance curve". The image (fig01) is a schematic curve, a sum of three Gaussian bumps and a logistic step with no filtering parameters, not the relay's variance.
2. **Task 13 audit of the design sweeps (§4.1, §4.4 Verification).** The draft says the Task 13 audit repeated the design-sweep check "with no class outside the stated sets". That is true, but row 12 of the Task 13 class audit (the Π₀ sweep of tanh, exp and Hill gains) **failed** its pre-registered rule: 122 persisting route disagreements, attributed to code (`t13/RESULTS_t13.md`, diagnosis 7). §4.4 should say so if it cites the audit.
3. **Planned references.** The draft's Appendix C says [46]–[53] are cited in chapters 5–9; the Task 15 prompt says chapters 6–7. The register's attachments put them on results 6.10, 6.19, 7.1, 7.2, 7.5, 7.6, 7.8, 7.11, 7.12 and 7.16 (table above), so chapters 6–7.
4. **Figure B.2 axis.** The draft and prompt ask for q from 0 to about 4. The R²_rel = 2 boundary approaches q = 4 from above (q₊ → 2R²_rel), so the figure uses 0–5 to show it.
5. **Label collision.** The figure labels B.1–B.12 have the same form as, and for B.1–B.12 the same text as, the legacy labels B.1–B.12 kept in `register/crosswalk.md` (B.1 = 2.1 topological realizability, …). Thesis-facing text uses only figure labels, but a reader of the crosswalk could confuse the two. This is why C10 fails.
6. **Theorem 3.2 labelling.** The draft states "Theorem 3.2(a) (normal form)" with the partial derivatives as unlabelled text; the register has 3.2 as one theorem. The thesis-only import keeps the draft's text verbatim.

## Provenance

- Pre-registration aa0b914; artifacts 41d5e43; results 48c3088.
- Runtimes: checks 23 s (C7 reruns the original figure scripts); Part G C11 467.3 s, C12 412.6 s, exploratory C11X None s.
- Seeds: 15001/15002 (C11), 15101/15102 (C12), 15201 (illustration), 15301/15302 (exploratory).
