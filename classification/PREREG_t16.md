# Pre-registration — Task 16: verify the thesis draft (chapters 1–5) against the repository; small repository fixes

Committed **before** any Task 16 script that produces a result is written or run. Not edited after its commit. The checks D1–D8
run **once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis attributed to the
**criterion**, the **input**, the **code** or the **document**. No criterion and no artifact is changed after the recorded run.

**No mathematical content changes.** Part A checks the draft and edits nothing. Parts B and C change wording, labels, checks and
one figure description, and nothing else. A mathematical error found in the draft or in the repository is recorded, not fixed.

**Inputs** (copied unchanged to `classification/t16/input/`):
- `Thesis_Draft_ch1-5.md`: the thesis draft, read-only. It is used to compare against the repository. The one exception is Part
  C.4, which the Task 16 prompt asks for explicitly: two thesis-only texts are refreshed from it (see Part C.4).
- `Task_16_Verify_Ch1-5_Prompt.md`: the Task 16 prompt.

Tools: Python 3, SymPy, mpmath (50 digits), NumPy, PyYAML. Seeds: 16001 (D1 random parameter sets), 16002 (D1 item 4
perturbations), 16003 (spare, used only if a numeric item needs a second independent draw; any use is reported).

## Disclosure: what is known before the run

The inputs and repository were read, with no Task 16 result produced, to write this file.

1. **The draft** (chapters 1–5) has been read in full. Its results 2.1–2.9, 3.1–3.7, 4.1–4.5 and 5.1–5.15 (36 results) match the
   36 register entries for chapters 2–5 in number and type as listed in `register/results.yaml`. The statements have not yet been
   compared with the repository.
2. **Figure B.4.** The script `t13/t13_figures_paper2.py` (block 2) uses λ = 1, Σ = 0.01 (F = 0.01), c = 1, κ = 1.5 and
   Π₀ = c/(κF) = 66.67. It locates Π_c as the first point of its plotting grid (`np.logspace(-3, 4, 1500)`, steps of about 1.1 %)
   where the Bayesian-weight gain falls below G⋆, and prints it with `.3g`: 56.7. Task 10 (`t10/t10_realize.py`) solves the same
   equation with `mp.findroot` at the same parameters and recorded Π_c = 56.2047 (`t10/results/t10_2.json`, `a13_supp`). The image
   carries no Π_c text (its captured text elements in `t15/results/cap_new_t13.pkl` are axis labels, ticks, legend entries,
   "(0, π_R): fails for every gain at R² = 0.6F" and "F"). The description's 56.7 therefore looks like the grid value, not the
   root. D5 recomputes the root independently.
3. **Sources of the A3 numbers** were located by searching the repository (file names listed under D3). Several of the stored
   values were seen while searching. The comparison itself is made in the run.
4. **Known edits named in the prompt.** The draft states "G⋆ = σ⋆²Π < FΠ for every Π > 0" in Proposition 3.5; the prompt says the
   repository has ≤. If the comparison confirms this, it is a difference of kind (c) (the draft is stronger) and **D2 fails by its
   criterion**, whatever D1 finds about the strict inequality (D1 item 2 tests it). The title of Corollary 5.4 differs; titles are
   compared as wording unless the statement's content differs.
5. **Crosswalk files.** `crosswalk.md` is written by `t14/build_register.py` from the `legacy` field of `results.yaml`, so the
   prefix is applied to that field and the crosswalk is regenerated from it. `crosswalk_v1.yaml` holds verbatim legacy strings
   rendered only in the paper render's change-log table. Its only A–E-form label is "§A.3" (in "§A.3 limits table (Stage 2
   completion)"); it is prefixed, which changes that one line of the paper render. Its other strings ("Prop. 1.1 (Stage 0–1)" and
   the like) are not A–E-form and cannot be read as figure labels; they are left unchanged.
6. **Bare figure labels in the renders.** T15 C10's 81 matches include figure labels outside the literal "Figure B.n": image file
   names (`B.4_realizability.png`), the Roadmap §7 Figures column ("B.3, B.4"), Appendix D/E text ("figure labels B.1–B.12",
   "figures B.1, B.3–B.12"). The rewritten check (D6) defines its exemption to cover these (below).
7. **T15 citation count.** T15 C4 recorded hits only, not the number of citation groups. D7's baseline is computed in the run by
   applying the T15 C4 pattern to the thesis renders at the T15 artifacts commit 41d5e43 (`git show`).

## Part A — the draft against the repository

Run script: `t16/t16_checks.py` (D1, D3, D4, D5, D6, D7, D8 and the A2 extraction). Output: `t16/results/t16_checks.json`, `.log`,
`a2_pairs.md`.

### D1 — new proof steps (A1)

Symbols are SymPy symbols declared positive (λ, Σ, Π, Π₀, c, G, λ′, Σ′, R², g, …). An **identity** holds if the difference of its
two sides reduces to 0 by any of: `simplify`; `factor(radsimp(·))`; `simplify` after `sqrtdenest`/`powsimp`. Every identity is also
evaluated at 1,000 random parameter sets (mpmath, 50 digits; log-uniform positives in [10⁻³, 10³], seed 16001) as a cross-check;
a nonzero symbolic residual is a failure even if the numeric residual is 0. An **inequality, sign or monotonicity claim** holds if
it holds at ≥ 1,000 random admissible sets with no counterexample (and a symbolic argument is recorded where SymPy gives one). A
**limit** holds if `sympy.limit` (or substitution into a continuous expression) gives the stated value.

| Item | What is checked |
|---|---|
| 1 Prop. 3.1 | (a) D/(2a) with a = λ + G, D = G²/Π + 2Σ equals (Σ + G²/(2Π))/(λ + G); the Lyapunov equation 0 = −2aP + D gives P = D/(2a). (b) With u = G²/Π, σ² = (Σ + u/2)/(λ + G) is continuous at (G, u) = (0, 0) with value F. (c) With G → G∞ > 0 and Π → ∞, σ² → Σ/(λ + G∞), and Σ/(λ + G∞) < F. |
| 2 Prop. 3.5, Lemma 3.6 | (a) The positive root p of 2Σ − 2λp − Πp² gives pΠ = −λ + √(λ² + 2ΣΠ) and p = 2Σ/(λ + √(λ² + 2ΣΠ)); σ²(G⋆, Π) = p. (b) ∂σ²/∂G = (G² + 2λG − 2ΣΠ)/(2Π(λ + G)²); its only positive zero is G⋆. (c) dσ⋆²/dΠ < 0; σ⋆² → F as Π → 0; G⋆ = σ⋆²Π and σ⋆² < F for Π > 0. (d) G⋆/(FΠ) = 2(√(1 + ν) − 1)/ν = 2/(1 + √(1 + ν)) with ν = 2ΣΠ/λ². |
| 3 Lemma 3.7 | dσ²/dΠ for G = G(Π) equals G·N/(2Π²(λ + G)²) with N = ε(G² + 2λG − 2ΣΠ) − G(λ + G), ε = ΠG′/G; and ∂σ²/∂Π = −G²/(2Π²(λ + G)). |
| 4 Prop. 2.9 remark | Logical review of "Direction in condition 2", step by step (recorded in the results), plus a numeric test: random C2 curves and perturbations satisfying conditions 1 and 2 (seed 16002, ≥ 1,000 (curve, Nᵢ) pairs), checking that σ̃² is monotone on each Nᵢ in the direction of σ². Holds if the argument has no gap and the test finds no counterexample. |
| 5 Thm 5.1 | The positive root in v of Πv² + 2λv − 2Σ = 0 equals σ⋆²(Π). |
| 6 Prop. 5.8 | (a) For G = cΠ/(Π + Π₀), ΠG′/G = 1 − G/c. (b) Substituting Π = Π₀G/(c − G) into N gives −(G/c)(G² + 2λG + 2ΣΠ₀ − λc). (c) The root −λ + √(λ² + λc − 2ΣΠ₀) is in (0, c) iff λc > 2ΣΠ₀, and λc > 2ΣΠ₀ iff κ = c/(FΠ₀) > 2. (d) The turning point is a maximum: N changes sign from + to − along increasing Π. |
| 7 Prop. 5.9 | With Π(G) = (G² + 2λ′G)/(2Σ′), ε = (G + 2λ′)/(2(G + λ′)) and N = G·p(G)/(2(G + λ′)), p = −(1 + r)G² − 4rλ′G + 2λ′(λ − 2rλ′), r = Σ/Σ′; p strictly decreasing on G > 0; p(0) > 0 iff F′ > 2F. |
| 8 Prop. 5.14 | (a) 2Π²(λ + G)²·dσ²/dΠ = ΠG′(2λG + G² − 2ΣΠ) − G²(λ + G). (b) σ² ≤ F iff 2ΣΠ ≥ λG. (c) Where σ² ≤ F and G′ ≥ 0: ΠG′(2λG + G² − 2ΣΠ) − G²(λ + G) ≤ G(λ + G)(ΠG′ − G). (d) For a Bayesian stage, ΠGᵢ′ − Gᵢ = −cᵢΠ²/(Π + Π₀,ᵢ)². |
| 9 Cor. 5.2 | σ⋆²(π_R) = R² for π_R = 2λ(F − R²)/R⁴, 0 < R² < F. |

Each item is reported as **holds**, **fails** (with a counterexample or nonzero residual) or **ambiguous** (with the reading used).
**Pass:** all 9 items hold.

### D2 — statements carried over (A2)

For each of the 36 results 2.1–2.9, 3.1–3.7, 4.1–4.5, 5.1–5.15, the run extracts the draft's statement (from its bold label to
the start of its proof, or to the next heading or result if it has no proof; tables that belong to the statement included) and the
repository's statement (`Stages_0_4_Thesis.md` as rendered from `source/Stages_0_4_Source.md`, or `source/thesis_only/` for 2.3,
2.8, 2.9, 3.2) into `t16/results/a2_pairs.md`, side by side. Proofs, remarks and verification lines are not compared.

After the run each pair is read and every difference in hypotheses, conclusions, constants or class tables is recorded in
`t16/results/a2_classification.yaml` with both texts and one kind: (a) equivalent; (b) the draft is weaker; (c) the draft is
stronger; (d) the draft contradicts the repository. Wording, notation, ordering and titles do not count unless they change content.
This reading is manual; the yaml is committed with the results and D2's verdict is computed from it.
**Pass:** no difference of kind (c) or (d).

### D3 — numbers in chapters 1–5 (A3)

Every value below is compared with its source **to the digits printed** in the draft (the source is rounded to the printed
significant figures; counts must be equal). Formula values are recomputed in the run with mpmath (50 digits); repository values
are read from the files named.

| # | Draft value | Source |
|---|---|---|
| 1 | κ = 100, R² = 0.05: failure set (1/9, 4); factor 36 (§1.2, §2.7) | formula: σ² of cΠ/(Π + Π₀), λ = c = 1, Σ = 0.01, Π₀ = c/(κF) |
| 2 | Π₀^pair = 30.243, 31.475, 37.820, 44.180, 62.711 for n = 1.5, 2, 3, 4, 8 (§5.4; 31.475 also §3.3) | formula: c·φₙ(t\*)/(2nΣ), λ = c = 1, Σ = 0.01; and the Task 13 regression values (`t13/results/t13_regression_symbolic.json` or `t13_partA_numeric_A4_A5_A7.json`) |
| 3 | M/F = 17.575 and 9.2875; ratio 1.892 (§5.3) | formula (κ = F′/F = 100, λ = λ′ = c = 1, Σ = 0.01); Task 13 audit (`t13/results/t13_audit_numbers.json`) |
| 4 | π_R = 222.2 (R² = 0.6F, Figure B.4) | formula 2λ(F − R²)/R⁴ |
| 5 | Hill window onset 25 = cλ/(4Σ); 25 ≤ Π₀ < 31.475 gives sup q ≤ 2 (§3.3, §5.4) | formula: sup q = c/(2FΠ₀) for n = 2 |
| 6 | t\*² = 2√3 − 3 for n = 2 (Theorem 5.12(b)) | formula: numerical maximiser of φ₂ |
| 7 | Chapter 4 worked examples: Π_B = 50, Π_A = 150; Π = 1: Π₀⋆ = 99.498, σ⋆² = 0.0099505, V_c = 0.255; Π = 60: 64.162, 0.0080540, 0.0091667; Π = 500: V_c = 0.0055; cases P3/P2/P1; "0.5 % below F"; "about 11 % of F" | formulas of Propositions 4.2–4.3 |
| 8 | Coupling: c⋆ = 0.019901, σ⋆² = 0.0099505, c_F = 0.04 (Π = Π₀ = 1) | formulas of Proposition 4.4 |
| 9 | Mixed band: median 5 × 10⁻⁴, range 4 × 10⁻²² to 0.96, 16 % (§2.8, §5.4) | `t10/results/t10_4.json`, `t10/RESULTS_t10.md` |
| 10 | 101/101, 24/24, k = 1 to 5, 6 × 10⁻¹⁰ (§5.1) | `t10/results/t10_2.json`, `t10/RESULTS_t10.md` |
| 11 | 2,000/2,000; 961; 10,000; 6 × 10⁻³¹; 7/2,000; 63/2,000 (§5.6, §5.5) | `t10/results/t10_3.json` (or `t10_1.json`), `t10/RESULTS_t10.md` |
| 12 | 4,868 and 77,888 (§5.6) | `t10/results/t10_4.json` |
| 13 | 5,000 sets, n ∈ [1.01, 10] (§5.6) | Task 13 A5 results (`t13/results/`) |
| 14 | 62 of 62; ±10⁻⁶ relative; 20,000 sets × 5 sweeps = 10⁶ classifications (§4.1, §4.4) | `classification/REPORT.md` and Task 8 results |
| 15 | 122 persisting disagreements; 1,000 fresh sets per audit row (§4.1, §4.4) | `t13/results/t13_audit_classes.json`, `t13/RESULTS_t13.md` |
| 16 | 10⁶ and 4.4 × 10⁶ blind-search classifications (§1.8) | Task 8 (T8.4) and `t12/RESULTS_t12.md` |
| 17 | 10^(−32,880,317) relative prior dip (§2.8) | `t12/RESULTS_t12.md` |
| 18 | Task 15 numbers in §2.8: 1,000 curves, ≥ 50 tolerances, 200,000 classifications, 1,000 perturbations on 500 curves, 0.9η, upper ray → (0, 1, 4) | `t15/results/t15_partG.json`, `t15/t15_partG.py` |

Any further number in chapters 1–5 that comes from a formula or a script, found while extracting, is added to the table in the
results and reported, but does not enter the pass rule unless it is listed above.
**Pass:** every listed value matches its source to the digits printed.

### D4 — citations and cross-references (A4)

Parsed from draft chapters 1–5 (lines up to the "## 6." heading), with Markdown escapes removed:
- **[n]:** every bracket group of integers, commas and en-dash ranges (`[4–9, 36–38]`) whose numbers all lie in 1–53 is a
  citation; each number must resolve in `register/references.yaml`; numbers 1–45 must first appear in ascending order (first
  appearance of n before first appearance of n + 1). Bracketed intervals such as `[0, ∞]` and `[1.01, 10]` are excluded by
  context (preceded by "in", or containing a symbol or a decimal point); every exclusion is listed.
- **Typed references:** "Theorem, Proposition, Lemma, Corollary, Definition, Numerical result, Conjecture, Counterexample" (and
  plurals, and the abbreviations Thm, Prop., Props., Cor., Num. result) followed by x.y, or a range x.y–x.z, or a list. Each
  number must exist in `results.yaml` with that type; for a range, every member must exist and have the type.
  Suffixes like "2.2(4)" or "7.7(a)" refer to the result 2.2 or 7.7.
- **Untyped references** (bare x.y or x.y–x.z in the "Label(s)" and "Result" table columns and in "results x.y–x.z"): existence
  only.
- **Figures:** every "Figure B.n" must exist in `register/figures.yaml`.

**Pass:** 0 unresolved [n]; first-citation order holds for [1]–[45]; 0 references to a nonexistent result or a wrong type; 0
unknown figure labels.

## Part B — Figure B.4 value

The figure's parameters are read from the script (disclosure 2). If the description's Π_c is not the root at those parameters,
the description is corrected to the root, rounded to four significant figures, in: the `figures.yaml` description (set by
`t16/t16_register.py`, which runs after `t15/t15_register.py`), the caption source `source/figs/fig02_realizability.txt` and
`source/figs/README.md`, and the renders made from them (`Appendix_B_Figures.md`, `figs_thesis/B.4_realizability.txt`,
`figs_thesis/README.md`). The curve, the script and the image are not changed; the Task 13 paper outputs (`figs_paper2/`) are not
regenerated and keep 56.7 (reported).

### D5 — Figure B.4

Π_c is computed with `mp.findroot` from cΠ/(Π + Π₀) = −λ + √(λ² + 2ΣΠ) at the script's parameters. Every "Pi_c = x" in the
B.4 description, in Appendix B and in `figs_thesis/B.4_realizability.txt` is compared with it to the digits printed.
**Pass:** all equal.

## Part C — repository fixes

1. **Legacy labels.** Every A–E-form label (`[A-E].n`, with suffixes and "+"-joined lists) in the `legacy` field of
   `results.yaml` is prefixed `legacy `, and `crosswalk.md` is regenerated from it; "§A.3" in `crosswalk_v1.yaml` becomes
   "legacy §A.3". Applied by `t16/t16_register.py`.
2. **Citation check** rewritten as D7.
3. **Register wording.** Result 5.6's `verified_by` "T8.1 (Proposition 4)" becomes "T8.1 (Corollary 3.3, excess identity)";
   Appendix A is re-rendered. Applied by `t16/t16_register.py`.
4. **Thesis-only texts.** `source/thesis_only/structural-stability.md` gains the draft's "Direction in condition 2" paragraph
   (verbatim, after the proof); `source/thesis_only/normal-form.md` changes its heading to "**Theorem 3.2 (normal form).**". Both
   header notes name the new source lines. Whether the thesis render should carry the draft's wording of 3.1, 3.5, 3.6 and 3.7 is
   reported, not done.
5. The render chain in Appendix E gains the `t16/t16_register.py` step. All renders are regenerated.

### D6 — legacy labels (re-run of T15 C10 with the fixed pattern)

- (i) Every A–E-form label in the crosswalk (`crosswalk.md` Legacy column, the `legacy` field of `results.yaml`,
  `crosswalk_v1.yaml`) is preceded by "legacy ".
- (ii) In the thesis renders (T15's list, whitespace-normalised), every match of `\b[A-E]\.\d+\b` is classified: **prefixed**
  (preceded by "legacy "); **figure label** (one of B.1–B.12 in `figures.yaml` and either the file is `Appendix_B_Figures.md` or in
  `figs_thesis/`, or the word "Figure"/"Figures"/"figure"/"figures" occurs in the 40 characters before it, or it is followed by
  "_" as in a file name); otherwise **bare legacy label**. "Paper 1" occurrences are counted as in T15 C10.
- (iii) False hits on Figure B.n: matches immediately preceded by "Figure " that are classified bare.

**Pass:** (i) holds; 0 bare legacy labels; 0 false hits on Figure B.n; 0 "Paper 1".

### D7 — citation check (re-run of T15 C4 with the fixed pattern)

Same files and exclusions as T15 C4 (Appendix C and Roadmap §7 rows 6–10 excluded); same raw-key, author–year and `[@` token
tests. A bracket group matched by T15's pattern is a **citation** only if it is a comma- or dash-separated list of integers that
all resolve in `references.yaml`; any other group is listed as a non-citation and not flagged. Baseline: the number of groups T15's
pattern matches in the thesis renders at 41d5e43, minus those T15's diagnosis (`t15/results/t15_diag.json`) classed as not
citations.
**Pass:** 0 false hits on intervals (no flagged group that is an interval); no raw-key, author–year or token hit; the number of
citations detected equals the baseline, in total and per file.

### D8 — register wording

Every `verified_by` entry in `results.yaml` is searched for a result type (Theorem, Proposition, Prop., Lemma, Corollary, Cor.,
Definition, Numerical result, Conjecture, Counterexample, Thm) followed by an integer that is not of the form x.y (a
consolidated-v1 number).
**Pass:** 0 matches.

## Report

`classification/RESULTS_t16.md`: the commits (pre-registration, artifacts, results); the check table with outcome and runtime;
diagnoses of failures; files changed; and **For the author** items 1–6 as the prompt lists them. Attachments: `RESULTS_t16.md`,
`Appendix_A_Register.md`, `register/crosswalk.md`, `register/results.yaml`.
