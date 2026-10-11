# Pre-registration — Task 15: sync the repository with the thesis draft

Committed **before** any Task 15 script that produces a result is written to disk or run. Not edited after its commit. The checks
below run **once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis attributed to
the **criterion**, the **input** or the **code**. No criterion and no artifact is changed after the recorded run, with one planned
exception: the register status of results 2.8 and 2.9, which Part F.2 makes depend on the outcome of C11 and C12 (see "Planned
post-run change").

**No mathematical content changes.** Task 15 changes references, figures, file organisation, render templates and register
metadata only. Part G tests results 2.8 and 2.9 and changes nothing. A mathematical error found on the way is recorded, not fixed.

**Inputs:**
- `references.bib` (attached; byte-identical to the committed `classification/references.bib`, so Part A.1 is a no-op);
- `Thesis_Draft_ch1-4.md` (attached, read-only; copied unchanged to `classification/t15/input/Thesis_Draft_ch1-4.md` so the
  checks can read it);
- the Task 15 prompt (copied to `classification/t15/input/Task_15_Repo_Sync_Prompt.md`).

Tools: Python 3, NumPy, SciPy, SymPy, Matplotlib, mpmath, PyYAML. Seeds: 15001 (C11 curves), 15002 (C11 maps), 15101 (C12
curves), 15102 (C12 perturbations), 15201 (C12 illustration).

## Disclosure: what is known before the run

The inputs and repository were read, with no result produced, to write this file.

1. **Manuscript PDF** (`reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf`):
   - `pdfinfo` reports `Pages: 17`, 462,929 bytes, sha256 `9f60625a98c1cdd23c96360e64eb511acba0ee45321dde95980ab6795070eedf`. This
     is the author's file.
   - `ERRATA.md`'s "18 pages" was my error in Task 14: splitting `pdftotext` output on form feeds leaves an empty 18th element.
     The page numbers cited in E1–E4 came from the same split and are expected to be right.
   - Part H.2 corrects the count and checks each page with `pdftotext -f n -l n`.
2. **Figure text elements carrying result numbers** (read from the scripts): fig01 axis title "class in each band (Theorem 2)";
   fig02 legend "realized curve with three windows (Corollary 48)"; fig06 legend "the single maximum (Theorem 25)". `t8_figures.py`
   (B.3) shows none. These three are edited; every other text element is kept. C5 inspects the figure objects.
3. **The split "Paper 1"** is at `source/Stages_0_4_Source.md` lines 830–831 ("inherits Paper\n1's regularity"). A
   whitespace-insensitive count of the current thesis render finds 1 occurrence.
4. **Author–year text in the thesis renders:**
   - Roadmap §7 rows 6–10 quote search results "as returned" (e.g. "Kalman–Bucy (1961)", "Wang, Ho and Liu, IEEE TAC 2003"). C8
     requires them unchanged, so C4 excludes those five rows; the exclusion is reported.
   - Appendix C is the reference list and has author–year form by design, so C4 excludes it too.
   - The §12 literature sentence of the consolidated document ("Hansen and Torgersen, *Ann. Statist.* 2 (1974) …") is converted to
     `[@…]` citations in the thesis render. The paper render keeps its wording.
5. **Appendix C format** is inferred from the draft's Appendix C:
   - two authors joined by "&"; three as "A, B & C"; four or more as "First et al.";
   - hyphenated initials printed spaced ("Xu, J.-H." → "Xu, J. H.", as in the draft);
   - books print the publisher only (no series, address, ISBN or note);
   - in-proceedings and in-collection entries print "booktitle[ volume], pages" (no publisher);
   - `arXiv:id` is printed only when the entry has no journal or booktitle (Kurt and Orguner yes; Boominathan and Pitkow, and
     Hogeboom-Burr and Yüksel, no, as in the draft).
6. **Thesis-only texts** imported verbatim from the draft (Part F) contain hand-typed result numbers and `\[n\]` citations,
   because they are copied verbatim. No Task 15 check forbids that. They are marked as imported in the render.
7. **Rows 11–17 of Roadmap §7** have six columns; rows 6–10 have four. The new rows therefore go in a second table, directly after
   row 10, with the prompt's header. Rows 6–10 stay byte-identical.
8. **The draft's Proposition 2.9** was read for implementability (Part G.2). The proof forces the direction in condition 2
   (strictly monotone on Nᵢ) to be that of σ² on Nᵢ, because the ends of Nᵢ have opposite signs. The statement does not say this.
   It is not a blocking ambiguity, but the report records it. Reading used: any strictly monotone σ̃² on Nᵢ (both directions are
   allowed by the generator; only the forced one can occur under condition 1).

## Definitions

- **Citation token** (sources): `[@k1; @k2; …]`. The thesis render prints `[n]` or `[n, m, …]`, sorted ascending, with runs of
  three or more consecutive numbers as `n–m`. The paper render prints the same. Bib keys stay in the source.
- **Figure token** (sources): `{{fig:key}}` renders "Figure B.n"; `{{fig:key|n}}` renders "B.n". Both come from
  `register/figures.yaml`.
- **Include token** (sources): `{{include:path}}` inserts `source/<path>` verbatim. It is used, inside thesis-only blocks, for
  `source/thesis_only/<key>.md`.
- **Paper numbering** counts headed results in the paper-visible text only, after thesis-only content is removed, so
  thesis-only imports never shift paper numbers.
- **Thesis renders:**
  - `Stages_0_4_Thesis.md`, `Roadmap_v3.md`;
  - `Appendix_A_Register.md`, `Appendix_B_Figures.md`, `Appendix_C_References.md`, `Appendix_D_Verification.md`,
    `Appendix_E_Reproduction.md`;
  - `figs_thesis/*.txt`, `figs_thesis/README.md`;
  - `reference/phase1/README.md`, `reference/phase1/ERRATA.md`.
- **Sources:** everything under `classification/source/` (including `thesis_only/`) and `register/matrix.csv`.

## Checks and pass criteria

**C1 Bibliography.** `references.bib` has 53 entries, 46 carry a `doi` field, 0 contain `VERIFY`; 0 dangling citation keys
(`results.yaml` citations and source `[@…]` keys all in the bib). After Part A (jazwinski1970 → `latency`; simon2006 →
`tau-relay-variance` and `stationary-variance`), 0 unused entries. An entry counts as used if it is attached to a register result,
cited in a source, or listed as planned in `references.yaml`. Pass: all hold.

**C2 Reference register.** `register/references.yaml` has numbers 1–53, unique and contiguous, in a bijection with the bib keys,
and equal to the prompt's frozen table exactly (number ↔ key; `status` planned for 46–53, cited for 1–45). Pass: all hold.

**C3 Appendix C render.** `Appendix_C_References.md` equals the draft's Appendix C line for line, after normalising: whitespace
collapsed, Markdown escapes removed (`&#91;` → `[`, backslash before a punctuation character dropped), blank lines ignored.
Compared: the 53 entry lines. Pass: identical.

**C4 [n] rendering.** In every thesis render except Appendix C and Roadmap §7 rows 6–10 (disclosure item 4):
- (a) no raw bib key (any bib key as a whole word);
- (b) no author–year citation, matched by `\b[A-Z][\w–'-]+ \((19|20)\d\d[a-z]?\)` or
  `\b[A-Z][a-z]+ (and|&) [A-Z][a-z]+\b[^.\n]{0,60}?\b(19|20)\d\d\b` or `et al\.`;
- (c) no unrendered `[@` token;
- (d) every bracketed citation number (`[n]`, `[n, m]`, `[n–m]` in rendered citation positions) lies in 1–53 and resolves in
  `references.yaml`.

Pass: 0 for (a)–(c), and all resolve for (d).

**C5 Figures carry no numbers.** For every B.n image (B.1–B.12), the figure objects created by its script are inspected (not the
image): titles, axis labels, tick labels, legend texts, `Text` and `Annotation` artists, colorbar labels and suptitles. No text
matches `(Theorem|Proposition|Prop\.|Lemma|Corollary|Cor\.|Figure|Fig\.)\s*\d`. Pass: 0 matches.

**C6 Figure B.2.** Using the functions `make_fig_B2.py` plots from:
- the envelope touches each r < 1 boundary at exactly (ν_R, r), ν_R = 4(1 − r)/r², to 1e-9 (q₊ = q₋ = q⋆ = r there);
- at r = 1 the drawn boundary is {q = 0} ∪ {q = 2};
- wherever an r-boundary exists, q₋ ≤ q⋆ ≤ q₊, at 10⁴ log-spaced ν in [10⁻², 10³];
- only q ≥ 0 is drawn (checked on the plotted arrays).

Pass: all hold.

**C7 Figure data unchanged.** For each regenerated B.n (B.1, B.3–B.12), every plotted array (line x/y data, collection offsets,
paths and arrays, fill polygons, images) of the new script equals the original script's (`t13/t13_figures_paper2.py`,
`t8_figures.py`, run unchanged into a scratch directory) to 1e-12 (absolute, or relative where |value| > 1). Pass: equal for
all.

**C8 Roadmap §7.** In `source/Roadmap_v3_Source.md`:
- rows 11–17, with each citation token replaced by its comma-joined keys in original order, equal the Part D table text exactly;
- the line "Second-set priority combination searches: all four returned no prior work. 'No close prior found' describes these
  searches, not worldwide novelty." follows the table;
- no "query text not supplied" remains in any source or render;
- rows 6–10 are byte-identical to the Task 14 version (commit 77a939c).

Pass: all hold.

**C9 Appendix letters.** No "Appendix B" or "Appendix C" in the old sense (verification record, reproduction) in any source or
render. Matches are listed and judged by context, with references to the manuscript's own appendices exempt. `Appendix_A_Register.md`
… `Appendix_E_Reproduction.md` exist. Pass: 0 old-sense uses and 5 files present.

**C10 Thesis render phrase check.** After collapsing all whitespace (newlines included) to single spaces, every thesis render
contains 0 "Paper 1" and 0 matches of `\b[A-E]\.\d+\b`. Pass: 0.

**C11 Corollary 2.8 (Part G.1).** Using the existing classifier (`t11_common.analyse_with_limits` with the T10 turning-point method,
and `t10/classify.py` routes (i) and (ii)):
- **Curves:** 1,000 C2 curves σ²(θ) = P(tanh(log₁₀ θ)) on D = (0, ∞), where P is a random polynomial of degree 6–9. Coefficients
  are standard normal plus a constant shift making P > 0 on [−1, 1]; curves with a stationary point that is not a turning point
  are redrawn.
- **Reparameterisations:** each curve is paired with one φ: D → D, φ(θ′) = 10^ψ(log₁₀ θ′). The kinds are 250 each:
  - ψ(x) = a x + b sin x with |b| < a (smooth increasing);
  - piecewise-linear increasing with 3–6 random kinks and slopes in [0.5, 2];
  - the negatives of both (decreasing).
- **Tolerances:** at least 50 per curve. These are every critical value, each critical value × (1 ± 1e-6), and log-uniform draws on
  [½ min, 2 max] of the critical values, up to 50 in total.
- **Mismatch:** for route r ∈ {i, ii}, route r's class of σ² ∘ φ differs from the transform of route r's class of σ², where the
  transform is the identity for increasing φ and (ℓ, u) exchanged for decreasing φ. A signature mismatch is turning-point values not
  equal (relative 1e-25), in the same order or reversed for decreasing φ, or approach directions not preserved (exchanged for
  decreasing φ).

Pass: 0 class mismatches and 0 signature mismatches. Route disagreements within one curve are reported.

**C12 Proposition 2.9 (Part G.2).** With the same classifier:
- **Curves and tolerances:** 500 curves as in C11 (seed 15101). Two tolerances per curve, drawn log-uniform on the curve's range
  and redrawn if within 1e-6 relative of a value in 𝒞: 1,000 cases.
- **Neighbourhoods:** for each crossing xᵢ, Nᵢ = [xᵢ − hᵢ, xᵢ + hᵢ] in x = log₁₀ θ. Here hᵢ is a uniform fraction in [0.1, 0.9]
  of the distance to the nearest turning point, end of the grid range, or neighbouring crossing's half-distance.
- **Margin:** η is computed exactly as the minimum of |σ² − R²| over the turning-point values, the ends of every Nᵢ and |L± − R²|.
  This equals the infimum, because σ² is monotone on each segment of D minus the interiors of the Nᵢ.
- **Perturbation,** with amplitude A uniform in [0.05, 0.95]·η and support inside x ∈ [−20, 20]. Two kinds, alternating:
  - (a) δ = A·w(c(x))·sin(ω c(x) + φ), with c(x) the "clock" that is constant on each Nᵢ, so σ̃² = σ² + const there;
  - (b) δ = A·w(x)·Σⱼ aⱼ sin(ωⱼ x + φⱼ), normalised so sup |δ| ≤ A. It is accepted only if σ̃² is strictly monotone on every Nᵢ,
    checked by the sign of the analytic derivative of σ̃² at 2,000 points per Nᵢ, plus its value at the ends; otherwise redrawn.
  - Here w is a C∞ bump with compact support, so σ̃² satisfies C2 and keeps the limits L±.
- **Mismatch:** the class of σ̃² (route i or ii) ≠ class of σ² (same route).

Pass: 0 mismatches. **Illustration (not a pass criterion):** one perturbation that violates only condition 2 (a wiggle inside one
Nᵢ of amplitude < η), shown to change the class.

**C13 Reproduction unaffected.** Every run script in `reproduce_all.sh` exists, every script it invokes exists, and every
repository file named by a string literal ending in `.md`, `.py` or `.sh` in those scripts resolves the way the script builds
its path. Candidates, tried in order:
- the script's directory;
- `classification/`;
- the repository root;
- `classification/<tN>/` for literals named `tN_*`;
- the module-level `DOC` of a script, evaluated by import (Task 13 audit scripts).

Literals the script writes (opened with mode `"w"`) and outputs (`REPORT.md`, `RESULTS_t*.md`, files under `results/`, `figs*/`,
`figures/`) are excluded. Pass: 0 unresolved.

## Planned post-run change

Part F.2 sets the register status of 2.8 and 2.9 from Part G:
- If C11 passes, 2.8 gets `verified_by: [T15 C11]` and `status: proved`. Likewise 2.9 with C12.
- On a failure the status stays `to-verify` and the failure is recorded.

This one register edit, and the re-render of `Appendix_A_Register.md` and `Appendix_D_Verification.md` (adding T15), are made
after the run in a separate, labelled commit. They are the only post-run changes. 3.2 and 6.5 are set before the run (`T14 G`,
`proved`).

## Outputs

- **Register:** `register/references.yaml`, `register/figures.yaml`; `results.yaml` (citations and status, per Parts A and F).
- **Sources:** `source/thesis_only/*.md`; edits to the existing sources (citation, figure and include tokens; Part D rows;
  Part H.1).
- **Rendering:** `register/render.py` (new tokens; paper numbering on paper-visible text).
- **Appendices:** `Appendix_B_Figures.md`, `Appendix_C_References.md`, `Appendix_D_Verification.md` and
  `Appendix_E_Reproduction.md`; re-rendered `Appendix_A_Register.md`, `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md`,
  `Roadmap_v3.md`, `figs_thesis/` and `reference/phase1/`.
- **Figures:** `figs_thesis/B.n_<key>.png` and `.pdf`.
- **Task 15 code:**
  - `t15/make_fig_B2.py`, `t15/make_figs_thesis.py` (with the generated scripts it runs), `t15/fig_harness.py`;
  - `t15/t15_checks.py`, `t15/t15_partG.py`;
  - `t15/bib_check.md`, `t15/results/`.
- **Report:** `classification/RESULTS_t15.md`.
