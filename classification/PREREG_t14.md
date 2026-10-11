# Pre-registration — Task 14: thesis numbering, Phase 1 roll-in, matrix fix and bibliography

Committed **before** any Task 14 script is written to disk or run and before any check below is evaluated. Not edited after
its commit. Failures stay recorded, are diagnosed post hoc (in `t14/RESULTS_t14.md`, with `t14/*_diag.py` where code is
needed) and attributed to the **document**, the **code** or the **criterion**. Nothing in `verification/` is modified.

**No mathematical content changes.** Task 14 changes numbering, references, file organisation and citations only. A
mathematical error found on the way is recorded in the report and not fixed.

Tools: Python 3, NumPy, SciPy, SymPy, Matplotlib, mpmath, PyYAML (only for reading and writing the register). No random
numbers are used.

## Disclosure: what is known before the run

The repository was read, with no script run, to write this file. These findings bear on the outcomes:

1. **The starting-study manuscript is not in this repository.** No PDF, LaTeX or Word file of "A Bounded Failure Window in
   a Miscalibrated Precision-Weighted Relay" exists in any commit or branch. The full history was fetched first, since the
   clone was shallow. `Precision-Gated-Relay-Reproduce/paper/manuscript.pdf` is a different note ("Non-Monotonic Variance and
   Reafference-Dependent Timing in Offline Neural Simulation"). It has no §3.4, §3.8 or §5.2 matching the errata. So §4.1
   (`git mv` of the manuscript into `reference/phase1/`) cannot be carried out. `reference/phase1/` is created with
   `README.md` and `ERRATA.md`, and a `MANUSCRIPT_LOCATION.md` stub records that the file must be supplied. The errata quote
   the manuscript's text as given in the Task 14 prompt; those quotes cannot be checked against the manuscript here.
2. **All Task 1–7 hashes exist** (`git cat-file -e` succeeded for d21f193, 70ebb55, 824ca06, a0d2be2 and 2f9da71 after the
   unshallow fetch). Check C8 re-runs this inside a script.
3. **doi.org and api.crossref.org are blocked** by the session's network policy (proxy CONNECT rejected; WebFetch cannot
   resolve them). Only web search is available. So DOIs cannot be "resolved at doi.org". Under C9 every DOI is therefore
   expected to be marked `VERIFY: DOI not resolved (doi.org unreachable from this session)`. Web search is used to
   corroborate VERIFY-flagged fields; a search result counts as corroboration only through a publisher or indexing URL that
   carries the identifier, never through a generated summary alone.
4. **Type change in the register.** The register (given in the prompt) types `excess-identity` as a Corollary; v1 has it
   as Proposition 4. The paper render takes its types from the register, so it will print "Corollary 4" wherever v1 prints
   "Proposition 4": the heading, the label line, the §12 row and each reference. This is not one of C4's allowed differences
   (a)–(c). **C4 is therefore expected to FAIL on these lines.** The criterion is kept as given, and the diff summary lists
   them.
5. **Rows 25–26 in v1 already have the right content**, but the cell wording given in §5 renders as "(Proposition 36)",
   "(Numerical result 37)" instead of v1's abbreviations "(Prop. 36)", "(Num. 37)". This falls under C4's allowance (c).
6. **Task 13 scripts read `classification/Stages_0_4_Consolidated.md`** (`t13_audit_numbers.py`, `t13_audit_refs.py`). After
   the `git mv` that path is gone, and a Task 13 replay would fail. Planned fix (organisation only): give both scripts a path
   fallback to `archive/Stages_0_4_Consolidated_v1.md`, whose content is byte-identical. C10 tests the result.
7. **Thesis-only definitions for Part G.** The register names thesis results 3.2 and 6.5 whose text is not in the
   repository. Part G uses the reading stated in its section below, which matches v1's Lemma 39, Proposition 16 and
   Theorem 45. If the thesis defines ν or q differently, Part G checks this reading, not the thesis text.
8. **Figure images carry v1 numbers.** `fig01` (axis title "Theorem 2") and `fig06` (legend "Theorem 25") have result
   numbers drawn into the PNG/PDF. `figs_paper2/` stays untouched and the images are not regenerated. `figs_thesis/` holds
   the thesis-numbered captions and links the existing images. This is listed under "needs a human decision".

## Definitions used by the checks

- **Register:** `classification/register/results.yaml` (82 entries, from the prompt's table), `tasks.yaml` and
  `matrix.csv`. **Crosswalk:** `register/crosswalk.md` (No., Key, Cons. v1, Legacy) and `register/crosswalk_v1.yaml`. The
  latter holds the verbatim legacy strings of v1's change log (§13) and the two "It was …" remarks, for the paper render.
- **Sources:** `classification/source/Stages_0_4_Source.md`, `source/Roadmap_v3_Source.md`, `source/figs/*.txt`,
  `source/figs/README.md`, and `register/matrix.csv`.
- **Token grammar** (rendered by `register/render.py`):
  - `[[key]]` renders type and number. `[[key|n]]` renders the number only. `[[key|t]]` renders the type only.
  - `[[key|a]]` renders the abbreviated type and number (Thm, Prop., Cor., Num., Lemma, Def., Conj., Counterex.). This
    extends the prompt's three forms and is needed for the matrix's abbreviated label column.
  - `{{phase1}}` renders "the starting study (Tasks 1–7)" in thesis mode and "Paper 1" in paper mode; `{{phase1}}'s`
    renders "the starting study's" in thesis mode.
  - `{{thesis:…}}` and `{{paper:…}}` keep their content in one mode only. They also have block forms, `<!--thesis-->…<!--/thesis-->`
    and `<!--paper-->…<!--/paper-->`.
  - `{{legacy:id}}` is allowed only inside paper-only content and renders the crosswalk string `id`.
  - `{{matrix}}` renders `register/matrix.csv`.
- **Headed result:** a result whose statement in the source begins with a bold `**[[key]] (…).**` heading. Paper numbering
  is 1, 2, 3, … over headed results in order of appearance in `Stages_0_4_Source.md`. Thesis numbering is the register's
  `thesis_no`.
- **Legacy regex** (§1 of the prompt): `\b(Prop\.|Proposition|Thm|Theorem|Lemma|Cor\.|Corollary|Conj\.|Conjecture|Num\.|Numerical result|Counterexample|Def\.|Definition)\s*\d+(\.\d+)?[a-z′']?\b`,
  together with `\b[A-E]\.\d+\b` and the string `Paper 1`.

## Checks and pass criteria

**C1 Register integrity.** `results.yaml` has 82 entries; keys are unique and match `^[a-z0-9-]+$`; `thesis_no` is unique;
the numbers within each chapter run contiguously from 1; every consolidated v1 number 1–73 is mapped at least once (an entry's
`cons_v1` maps number n if it is the string "n", or begins with "n " as in "6 (main part)"); every legacy A–E label in the
prompt's table appears in some entry's `legacy` list. Pass: all hold.

**C2 Reference resolution.** Every `[[…]]` token in every source resolves to a register key. Every register key is referenced
at least once in the sources; the thesis-only keys of 2.3, 2.8, 2.9, 3.2 and 6.5 are exempt. Also reported: every token in a
render whose key has no heading in that render's numbering. For the paper render this means any token outside thesis-only
content whose key is not headed. Pass: 0 unresolved, 0 unreferenced. The headless-token count is reported and does not decide
the verdict.

**C3 No hand-typed numbers.** In the sources, the legacy regex (both parts) and the string `Paper 1` match 0 times outside
fenced code blocks and the crosswalk files. Pass: 0.

**C4 The paper render reproduces v1.** `Stages_0_4_Paper2.md` equals `archive/Stages_0_4_Consolidated_v1.md` except for:
- (a) numbers shifted by the split of 5.14, where every number ≥ 7 shifts by one;
- (b) the split itself;
- (c) the text of matrix rows 25–26.

Method: (i) check that the paper number of every key with v1 number n is n for n < 7 and n + 1 for n ≥ 7, and that
`no-mixed-decreasing-ratio` is 7. (ii) Render the source in paper mode, substituting each key's v1 number (with "6+" for the
new key), and line-diff the result against v1. (iii) Assign each differing hunk to (b), (c) or "other". (b) covers the lines
of Theorem 6's statement, label and proof, the new result, and every reference that now points to the new key; (c) covers
matrix rows 25–26.

A diff summary is reported, including the raw diff of the actual paper render against v1. Pass: no "other" hunk. Expected
FAIL is disclosed above (item 4).

**C5 Thesis render.** `Stages_0_4_Thesis.md`, the rendered `Roadmap_v3.md`, `Appendix_A_Register.md` and every file in
`figs_thesis/` contain 0 occurrences of "Paper 1" and 0 legacy A–E labels (`\b[A-E]\.\d+\b`). Pass: 0.

**C6 Matrix identity.** The matrix tables rendered into `Stages_0_4_Thesis.md` and into the rendered `Roadmap_v3.md` are
byte-identical, and rows 25–26 read exactly as §5 of the prompt. "Exactly" compares the Conditions cell after normalising
LaTeX to the prompt's plain form: `$` signs removed, `\Pi` → Π, `\le` → ≤, `[[key]]` → its rendered thesis reference. The
expected strings are:
- prior: `2R if G > 2FΠ (Proposition 6.20)`
- avg: `2R if G > 2FΠ (Proposition 6.20); also seen for G ≤ 2FΠ (Numerical result 6.21)`

Pass: identical and both rows exact.

**C7 Errata value.** For the Hill gain G = cΠ²/(Π² + Π₀²) with Π₀ = 5, λ = c = 1, Σ = 0.01, compute the interior minimum m of
σ² = (Σ + G²/(2Π))/(λ + G), which is the first turning point along Π, in mpmath at 60 digits. Method: bisect on the sign of the
analytic derivative to a width of 1e-40 in log10 Π. Report m to 8 significant figures. Pass: m rounded to 5 significant figures
equals 0.0099852. Otherwise the correct value is recorded and `ERRATA.md` E3 is updated.

**C8 Phase 1 records.** Every Task 1–7 hash in `tasks.yaml` exists (`git cat-file -e`). These are d21f193, 70ebb55, 824ca06,
a0d2be2 and 2f9da71, plus the Task 6 results commit 0944b81 read from the log. Pass: all exist; any missing are recorded.

**C9 Bibliography.** Every citation key used in `results.yaml` exists in `references.bib`, and every bib entry is used at least
once in `results.yaml` or by a `[cite]` in a source. Every entry carrying a DOI either resolves at `https://doi.org/<doi>`, tried
once per DOI from a script and recorded in `t14/bib_check.md`, or carries a `VERIFY` note. Pass: 0 dangling keys, 0 unused
entries, and every DOI entry resolved or marked VERIFY.

**C10 Reproduction unaffected.** `reproduce_all.sh` still finds every script and input after the file moves. Dry run, listing
paths only; Tasks 8–13 are not re-run. Paths checked:
- (a) every run script in `reproduce_all.sh`'s RUN table;
- (b) every script those run scripts invoke;
- (c) every repository file named by a string literal ending in `.md`, `.py` or `.sh` in those scripts that is read rather than
  written, resolved against `classification/`. Files a task writes itself are excluded: `REPORT.md`, `RESULTS_t*.md` and
  anything under `results/`, `figs*/` or `figures/`.

Pass: 0 missing paths.

## Part G (optional; run only after C1–C10 are recorded)

Reading used: ν = 2ΣΠ/λ² (v1's u), q = G/(FΠ), t = λτ.

**G1.** V(ν, q) := σ²/F = (1 + νq²/4)/(1 + νq/2) equals (Σ + G²/(2Π))/(λ + G) / F for G = qFΠ. The check is SymPy `simplify` of
the difference to 0.

**G2.** ∂V/∂q = ν(νq²/4 + q − 1)/(2(1 + νq/2)²) and ∂V/∂ν = q(q − 2)/(4(1 + νq/2)²), each checked by `simplify` of the
difference.

**G3.** Level-set roots. V = v ⇔ q = q±(v) = v ± √(v² − 4(1 − v)/ν), checked by substitution. These are real iff v ≥ q⋆.

**G4.** Envelope identity. The minimiser q⋆ solves νq²/4 + q − 1 = 0 (q⋆ = 2(√(1 + ν) − 1)/ν), and V(ν, q⋆) = q⋆ = σ⋆²/F, checked
by `simplify`.

**G5.** The inverse map reproduces 5.1. G = q₊(v/F)·FΠ equals G₊(v, Π) = Πv + √(Π(Πv² + 2λv − 2Σ)), checked by `simplify` of
the difference, or of the difference of squares with a sign argument.

**G6.** 6.5. With P from v1's Proposition 16, P/F = 2/(1 + νt + √((1 + νt)² + ν(1 − t)²)), checked by `simplify` and at 20 random
rational points evaluated at 60 digits. The points use the fixed seed 14001.

Pass: each item reduces to 0 (or holds at every point). A failure is recorded and attributed; a failure in G is not taken as
evidence of a mathematical error in the thesis without the thesis text.

## Outputs

The following outputs are produced:
- `register/results.yaml`, `register/tasks.yaml`, `register/matrix.csv`, `register/crosswalk.md`,
  `register/crosswalk_v1.yaml`, `register/render.py`;
- `archive/Stages_0_4_Consolidated_v1.md`, moved with `git mv` and unchanged;
- `source/…`, `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md`, the rendered `Roadmap_v3.md`, `figs_thesis/` and
  `Appendix_A_Register.md`;
- `reference/phase1/README.md`, `ERRATA.md` and `MANUSCRIPT_LOCATION.md`;
- `references.bib` and `t14/bib_check.md`;
- `t14/` scripts (`t14_inventory.py`, `t14_checks.py`, `t14_partG.py`), `t14/results/*.json` and `t14/RESULTS_t14.md`.

The prompt's §1 inventory is produced by `t14_inventory.py` from the state **before** any file is changed. It reports counts
per file of both legacy regexes and of `Paper 1`, read from this pre-registration commit with `git show`.
