# Task 15 — Sync the repository with the thesis draft: references, figures, appendices, novelty rows, open Task 14 items

You are working in the repository that holds `classification/` (Tasks 8–14), `verification/` (Tasks 1–7) and `reference/phase1/`. Use the usual protocol:
- Write `classification/PREREG_t15.md` with every check in §10 and its pass criterion. Commit it **before** running anything that produces a result.
- Run the checks once, on one recorded commit.
- Report in `classification/RESULTS_t15.md`. A failed check stays a failure, with a diagnosis (criterion, input or code). Never change a criterion or an artifact after the recorded run.

**Do not change any mathematical content.** This task changes references, figures, file organisation, render templates and register metadata only. The exceptions are the checks in Part G, which test two results and change nothing unless a check fails. If you find a mathematical error, record it and do not fix it.

## Attached

| File | What it is |
|---|---|
| `references.bib` | The verified bibliography. 53 entries, 46 with DOI, no `VERIFY` notes. The author checked every DOI against the publisher. Two fixes on top of the author's file: `{K}alman` protected in two titles; `sahomasugi2016` has `pages = {309}` in place of the non-standard `articlenumber`. |
| `Thesis_Draft_ch1-4.md` | Export of the thesis draft (chapters 1–4 written, 5–9 outlined, appendices laid out). It is the source for the thesis-only statements (Part F), the reference numbering (Part B), the figure list (Part C) and the appendix structure (Part E). Read it; do not edit it. |

---

## 0. Decisions already taken (background, not checks)

1. **Excess identity is a Corollary** (thesis Corollary 3.3, key `excess-identity`). This is accepted for both renders. T14 C4 failed only because of this type change, and it stays recorded as a failure (attribution: criterion). The paper render prints Corollary from now on. Do not add a separate paper type.
2. **Citations are bracketed numbers [n].** Numbers are assigned by first citation in the thesis and frozen. A new reference takes the next free number and never displaces an earlier one. The full entries go in Appendix C.
3. **Figures carry no numbers inside the image.** No "Theorem 2", "Figure 3" or "Prop. 25" in titles, axis labels, legends or annotations. The text cites a figure as **Figure B.n**, and Appendix B lists them. Renumbering a result must never force a redraw.
4. **Appendices:** A Register of results · B Figures · C References · D Verification record, Tasks 1–14 · E Reproduction. Any earlier internal use of "Appendix B = verification record" or "Appendix C = reproduction" maps to D and E.
5. **Claims stay factual.** Novelty rows say what the searches found and nothing more.

---

## Part A — Bibliography

1. Replace `classification/references.bib` with the attached file. Keep the old one in git history only.
2. Attach the two unattached entries in the register's citation table:
   - `jazwinski1970` → key `latency`;
   - `simon2006` → keys `tau-relay-variance` and `stationary-variance`.

   If a key name differs, use the register key whose title matches (the delay/latency result; the τ-relay variance; the stationary variance). Report what you used.
3. Regenerate `classification/t14/bib_check.md`, or write `t15/bib_check.md`, with:
   - entry count;
   - DOI count;
   - `VERIFY` count;
   - dangling citations;
   - unused entries.

   The "VERIFY flags left in the bibliography" table in `RESULTS_t14.md` is superseded. Leave `RESULTS_t14.md` unchanged, and say in `RESULTS_t15.md` that its C9 failure is resolved by this input.

## Part B — Reference register and [n] rendering

1. Create `classification/register/references.yaml`, with one entry per reference: `number`, `key`, `first_cited` (a free-text location) and `status` (`cited` | `planned`). The numbering is frozen as below. Do not reorder it.

| No. | Key | No. | Key | No. | Key |
|---|---|---|---|---|---|
| 1 | kalmanbucy1961 | 19 | blackwell1953 | 37 | kurt2025 |
| 2 | ernstbanks2002 | 20 | greenshtein1996 | 38 | simon2006 |
| 3 | friston2010 | 21 | yuksellinder2012 | 39 | kalman1960 |
| 4 | heffes1966 | 22 | yukselbasar2013 | 40 | andersonmoore1979 |
| 5 | friedland1967 | 23 | yukselbasar2024 | 41 | hotzskelton1985 |
| 6 | nishimura1967 | 24 | hansentorgersen1974 | 42 | collinsskelton1987 |
| 7 | griffin1968 | 25 | kalata1984 | 43 | yasuda1993 |
| 8 | sangsukiam1990 | 26 | sahomasugi2016 | 44 | skeltonikeda1989 |
| 9 | ge2016 | 27 | brysonjohansen1965 | 45 | chang2014 |
| 10 | teunissen2021 | 28 | brysonhenrikson1968 | 46 | shmaliy2020 (planned) |
| 11 | crouse2023 | 29 | jazwinski1970 | 47 | ren2021 (planned) |
| 12 | singh2009 | 30 | edelsbrunnerharer2010 | 48 | martinezrey2017 (planned) |
| 13 | boominathan2022 | 31 | cohensteiner2007 | 49 | lecam1964 (planned) |
| 14 | hotzskelton1987 | 32 | carr2003 | 50 | torgersen1991 (planned) |
| 15 | xuskelton1992 | 33 | milnor1963 | 51 | hogeboomburr2021 (planned) |
| 16 | heeger1992 | 34 | edelsbrunner2002 | 52 | barshalom2002 (planned) |
| 17 | carandiniheeger2012 | 35 | oudot2015 | 53 | yoder2018 (planned) |
| 18 | blackwell1951 | 36 | deyst1968 | | |

   The `first_cited` locations for 1–45 are in the thesis draft. Search for `[n]` there. 46–53 are planned for chapters 6–7.

2. **Thesis render:** every citation in `classification/source/` renders as `[n]`, or as `[n, m]` / `[n–m]` for runs of three or more consecutive numbers, sorted ascending.
   - Bib keys stay in the source.
   - Numbers are never typed by hand.
   - The paper render may keep its current style.

3. Render `classification/Appendix_C_References.md` from the register and the bib. Use one line per entry, in this format:

   `[n] Last, I. & Last, I. (year). Title. Journal vol(no), pages. doi:…`

   - Use "et al." for four or more authors, or where the bib has `and others`.
   - Convert LaTeX accents to Unicode (Yüksel, Başar, Martínez-Rey, Birkhäuser).
   - Book series volume numbers are not printed.
   - arXiv entries print as `arXiv:id`.

   Appendix C in the attached thesis draft is the reference output. Your render must match it line for line (check C3).

## Part C — Figures (Appendix B)

1. Create `classification/register/figures.yaml`, with one entry per figure: `label` (B.n), `key`, `source_file`, `script`, `caption_source`. The mapping is fixed:

| Label | Source |
|---|---|
| B.1 | fig01_stage1_schematic |
| B.2 | normal-form plane (new, item 3) |
| B.3 | fig_t8_sweeps (`classification/figures/`) |
| B.4 | fig02_realizability |
| B.5 | fig03_hill_phase |
| B.6 | fig04_peak_heights |
| B.7 | fig05_tau_normalizations |
| B.8 | fig08_optimal_sampling |
| B.9 | fig09_sampled_relay |
| B.10 | fig10_process_noise |
| B.11 | fig06_power_family |
| B.12 | fig07_delay |

2. Regenerate every image so it carries **no result or figure numbers**. Known cases from T14:
   - fig01: the axis title has "Theorem 2";
   - fig06: the legend has "Theorem 25".

   Scan every other image's text elements in the plotting scripts and list what you changed.
   - Write the outputs to `classification/figs_thesis/B.n_<key>.png` (and `.pdf` if the script supports it).
   - Leave `figs_paper2/` untouched.
   - Data, parameters and plotted curves stay identical. Only text elements change.

3. Generate **Figure B.2**, the (ν, q) plane, with ν on a log axis (about 10⁻² to 10³) and q from 0 to about 4:
   - the line q = 2 (the floor crossing; σ² > F iff q > 2);
   - the envelope q⋆(ν) = 2/(1 + √(1 + ν)), where 𝒱⋆ = q⋆;
   - the boundaries 𝒱(ν, q) = r for r = R²_rel ∈ {0.5, 1, 2}, with 𝒱(ν, q) = (1 + νq²/4)/(1 + νq/2). Solving gives q = r ± √(r² − 4(1 − r)/ν). For r < 1 this is real only for ν ≥ ν_R = 4(1 − r)/r².
   - Label curves with words or symbols only (e.g. "R²_rel = 0.5"), never with result numbers.
   - Include the script, `classification/t15/make_fig_B2.py`.

4. Render `classification/Appendix_B_Figures.md`: one entry per figure, giving the label, a one-sentence factual description and the image link.
   - The descriptions are yours, written from what each script actually plots: axes, swept parameter, fixed parameters, what is marked.
   - The thesis draft's B.4–B.12 captions are placeholders. Your descriptions are the information I need to replace them.
5. Sweep `classification/source/` and the renders for figure references ("Figure 3.1", "fig02", "Fig. 4" and so on) and rewrite them as `Figure B.n` through the register.

## Part D — Roadmap §7 novelty rows

T14 reconstructed rows 11–17 of the §7 table from the bibliography. They mislabel the clusters and drop the two with no close prior found. In `classification/source/Roadmap_v3_Source.md`, replace those seven rows with the table below and re-render. Reference numbers render through Part B. Rows 6–10 stay.

| # | Cluster (thesis results) | Searched as | Verdict | Closest prior work | Use in thesis |
|---|---|---|---|---|---|
| 11 | Causal information ordering (Def. 7.1, Thm 7.2, Prop. 7.5, Thm 7.6) | comparison of sequential experiments · Blackwell filtration · causal garbling · comparison of information structures · dynamic Blackwell | Close prior: the general principle | greenshtein1996, yuksellinder2012, yukselbasar2013, yukselbasar2024, blackwell1951, blackwell1953, hansentorgersen1974, lecam1964, torgersen1991, hogeboomburr2021: garbling monotonicity for sequential experiments and control/team costs; no filtering-error version found | Claim only the causal-process definition and the filtering-error monotonicity; cite first |
| 12 | Delay counterexample (Cex. 7.12) | Blackwell equivalent time shift · filtering versus smoothing information · delayed observations comparison of experiments · latency value of information | No close prior found | Delayed-measurement filtering: jazwinski1970, barshalom2002, yoder2018; that delay hurts filtering is folklore | Claim as a counterexample about orders on experiments, not as "delay hurts" |
| 13 | Power-family sharpness (Thm 7.8; Prop. 6.10) | correlation time Kalman non-monotone · fixed variance vs fixed spectral density · colored noise bandwidth estimation error · noise normalization OU | No close prior found | Coloured-noise methods: brysonjohansen1965, brysonhenrikson1968, chang2014, shmaliy2020; no normalisation comparison or exponent threshold found | Claimable |
| 14 | Realizability (Thm 5.1) | covariance assignment · covariance control · achievable error variance · attainable covariance suboptimal gain · performance envelope Kalman | Known variant | Covariance assignment, matrix state feedback: hotzskelton1985, hotzskelton1987, collinsskelton1987, xuskelton1992, yasuda1993, skeltonikeda1989 | Claim the scalar filtering attainability and explicit inverse gain as the filtering analogue |
| 15 | Hill mixed class (Thm 5.12, Prop. 5.13) | sigmoidal gain precision · Hill function gain estimation · divisive normalization precision weighting · neural gain control noise non-monotone | No close prior found | Gain form from divisive normalisation: heeger1992, carandiniheeger2012; no estimation use with a multi-component failure set | Claimable; credit the gain form to carandiniheeger2012 |
| 16 | Sampling interval (Thm 6.19, Prop. 7.16) | sampling period steady-state Kalman error · sampled-data Kalman filter sampling rate · optimal sampling interval estimation · a priori a posteriori error sampling interval · intersample error | Known variant | Sampled-data filtering: andersonmoore1979; optimal sampling rate with delays: martinezrey2017 | Remark on which error functional is quoted; state the Δt noise scaling |
| 17 | The framework (Thm 2.2, Prop. 2.9) | persistent homology superlevel sets · merge tree · Morse theory one-dimensional · excursion set · level crossings · persistence diagram stability | Citation only | Persistence and merge trees: edelsbrunnerharer2010, cohensteiner2007, carr2003, milnor1963, edelsbrunner2002, oudot2015 | Cite; the fixed-level versus all-levels stability contrast stays a remark |

Under the table, add one line: "Second-set priority combination searches: all four returned no prior work. 'No close prior found' describes these searches, not worldwide novelty."

Also delete "query text not supplied to Task 14" wherever it appears.

## Part E — Appendices A–E

1. `Appendix_A_Register.md` stays. Re-render it after the Part F status changes.
2. Create `Appendix_B_Figures.md` (Part C) and `Appendix_C_References.md` (Part B).
3. Create `Appendix_D_Verification.md`: one section per task, T1–T14 (T15 added after this run). Each section gives:
   - the PREREG file and the RESULTS file (paths);
   - the checks, with pass/fail counts;
   - every failure, with its attribution, in one line each.

   Copy outcomes from the RESULTS files. Never re-judge them.
4. Create `Appendix_E_Reproduction.md`: environment (Python and package versions from the lockfile or `pip freeze`), then the commands that regenerate every numerical result, figure and render, task by task, ending with the T14/T15 render chain.
5. Sweep the sources and renders for "Appendix B" or "Appendix C" used in the old sense (verification record, reproduction) and remap them to D and E.

## Part F — Thesis-only results and register status

1. Results 2.3, 2.8, 2.9, 3.2 and 6.5 have no text in the repository.
   - Import their statements **verbatim** from `Thesis_Draft_ch1-4.md` into `classification/source/thesis_only/<key>.md`. Locations: Definition 2.3 in §2.4; Corollary 2.8 in §2.7; Proposition 2.9 in §2.8 (with its displayed conditions); Theorem 3.2 in §3.2; Corollary 6.5 in §3.8, the τ-optimal formula.
   - Include 2.8's proof and 2.9's proof if the draft gives them.
   - These texts appear in the thesis render only.
2. Register status changes:
   - 3.2 and 6.5: verified by `T14 G`, status `proved`;
   - 2.8 and 2.9: per Part G.
3. Results 3.1, 3.5 and 6.13 have no heading in the consolidated document (T14 open item 7). Give me their statements as they appear in the manuscript, with page numbers, in the report. Do not add them to the sources.

## Part G — Verify Corollary 2.8 and Proposition 2.9

Use the existing classifier (T8–T13). Pre-register sample sizes and tolerances.

1. **Corollary 2.8 (reparameterisation).** Draw at least 1,000 C2 curves on an open interval (random trigonometric or polynomial sums, enough to produce several turning points). Pair each with random strictly monotone bijections φ, both increasing and decreasing, including non-smooth-but-continuous ones such as piecewise-linear.
   - At at least 50 tolerances per curve, including every critical value, check that:
     - k is preserved;
     - (ℓ, u) is preserved for increasing φ and exchanged for decreasing φ;
     - the signature is preserved, or reversed for decreasing φ.
   - Pass: zero mismatches.
2. **Proposition 2.9 (structural stability).** Implement the hypotheses exactly as stated in the draft: R² not in the critical set 𝒞; neighbourhoods Nᵢ inside monotone pieces; the margin η; and the monotonicity condition on Nᵢ.
   - For random curves and random perturbations that satisfy them, check that the class (ℓ, u, k) is unchanged. Pass: zero mismatches.
   - Separately, as an **illustration and not a pass criterion**, show one perturbation that violates only the monotonicity condition and changes the class. This records that the condition is doing work.
   - If the statement as written is ambiguous to implement, stop on that point. Report the ambiguity and the reading you would use. Do not choose a reading silently.

## Part H — Task 14 loose ends

1. **C5 detection miss.** In `Stages_0_4_Thesis.md`, around lines 829–830, "Paper 1's regularity" survives because the phrase is split across a line break.
   - Route it through the `{{phase1}}` phrase mechanism in the source.
   - Make the C5-style check whitespace-insensitive (normalise all whitespace, including newlines, before matching).
   - Re-run it as a T15 check over every render.
2. **Errata page count.** `reference/phase1/ERRATA.md` says the manuscript PDF has **18 pages**. The copy the author holds has **17 pages**:
   - `pdfinfo` reports `Pages: 17`;
   - producer pdfTeX-1.40.25;
   - 462,929 bytes;
   - sha256 `9f60625a98c1cdd23c96360e64eb511acba0ee45321dde95980ab6795070eedf`.

   For `reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf`, report the `pdfinfo` page count, the byte size and the sha256.
   - **Same file:** correct the page count in `ERRATA.md` and check that every page number cited in E1–E4 points to the quoted text, using `pdftotext -f n -l n`.
   - **Different file:** change nothing. Report the difference, including a `pdftotext` diff summary, and which file the errata page numbers fit.
3. **Figure-label decision (T14 item 4):** resolved by Part C.
4. **VERIFY table (T14 item 5):** resolved by Part A.

## 10. Pre-registered checks (write these into PREREG_t15.md with these criteria)

| Check | Pass criterion |
|---|---|
| C1 Bibliography | 53 entries; 46 DOI; 0 `VERIFY`; 0 dangling; 0 unused after Part A attachments (planned 46–53 count as used if attached to a register result or listed as planned) |
| C2 Reference register | `references.yaml` has numbers 1–53, unique and contiguous, in a bijection with the bib keys, and matches the frozen table exactly |
| C3 Appendix C render | Line-for-line identical to Appendix C of the attached draft, after normalising whitespace and Markdown escapes |
| C4 [n] rendering | No raw bib key and no author–year citation in any thesis render; every rendered number resolves in the register |
| C5 Figures carry no numbers | No match of `(Theorem\|Proposition\|Prop\.\|Lemma\|Corollary\|Cor\.\|Figure\|Fig\.)\s*\d` in any text element of any B.n image's script output (inspect the figure objects, not OCR) |
| C6 Figure B.2 | Envelope touches each r < 1 boundary at exactly (ν_R, r) to 1e-9; at r = 1 the boundary is {q = 0} ∪ {q = 2}; wherever an r-boundary exists, q₋ ≤ q⋆ ≤ q₊ (the optimum lies between its branches), sampled at 10⁴ ν values; only q ≥ 0 is drawn |
| C7 Figure data unchanged | For each regenerated B.n, the plotted arrays equal those of the previous image's script to 1e-12 |
| C8 Roadmap §7 | Rows 11–17 equal the Part D table; no "query text not supplied" remains; rows 6–10 unchanged |
| C9 Appendix letters | No "Appendix B"/"Appendix C" in the old sense in any source or render; A–E files exist |
| C10 Thesis render phrase check | Whitespace-insensitive: 0 "Paper 1", 0 A–E legacy labels, across all thesis renders |
| C11 Corollary 2.8 | 0 mismatches (Part G.1) |
| C12 Proposition 2.9 | 0 mismatches (Part G.2) |
| C13 Reproduction unaffected | Every script path resolves the way its script builds it (fixes T14 C10's resolver) |

## 11. Report (RESULTS_t15.md), and what to send back

In `RESULTS_t15.md`:
- the commit checked;
- the check table with outcome and runtime;
- diagnoses of any failure;
- files moved or created;
- the regenerate-everything command chain.

Then, under the heading **For the author**, give these items. I need them to finish the thesis:
1. Part H.2: the PDF facts and the answer on the errata page count.
2. Part C.4: the factual description of each figure B.1–B.12.
3. Part C.2: the text elements changed in each image.
4. Part F.3: the statements of 3.1, 3.5 and 6.13 with page numbers.
5. Part G: the outcomes, and any ambiguity found in 2.9's statement.
6. Every place in `classification/source/` where a reference in 46–53 belongs: result key, file and line, and reference number. I will cite them in chapters 6–7.
7. Anything that disagrees with the attached draft: a number, a statement, a figure. List it; do not resolve it.

Attach to the reply:
- `RESULTS_t15.md`;
- `Appendix_A_Register.md` through `Appendix_E_Reproduction.md`;
- `register/results.yaml`, `register/references.yaml`, `register/figures.yaml` and `register/crosswalk.md`;
- a zip of `figs_thesis/` (the B.n images and the B.2 script).
