# Pre-registration — Task 20: bring the repository in line with the thesis text

Committed **before** any Task 20 change to a source, the register, a generator or a rendered output, and before any Task 20
check is run. Not edited after its commit. The checks C1–C6 run **once**, on one recorded commit (the artifacts commit). A failed
check stays a failure, with a diagnosis attributed to the **criterion**, the **input**, the **code**, the **document** or a
**prediction**. No criterion and no artifact is changed after the recorded run.

**Base:** branch `task-20-thesis-sync`, created from `7855e45` (Task 19 results commit). Nothing is pushed or merged.
**Input:** the Task 20 prompt, copied verbatim to `classification/t20/input/Task20_prompt.md` (this commit).
**No mathematical content changes.** Task 20 changes register titles and numbers, adds one register entry with no verification,
adds seven bibliography entries, adds one non-failure line to Appendix D and swaps two figure labels. No result is re-proved and
no recorded file of Tasks 1–19 (`results/`, `input/`, `RESULTS*` / `REPORT*` files) is changed.

## How the repository works (read before this commit; determines the implementation)

1. **Thesis numbers are an explicit field.** `thesis_no` in `register/results.yaml` is the only source of thesis numbers
   (`register/render.py`, `numbering("thesis")`). Appendix A and `register/crosswalk.md` list entries **in file order**. Paper
   numbering comes from the order of headed results in `source/Stages_0_4_Source.md` and does not use `thesis_no`.
   So the 8.1/8.2 swap changes the two `thesis_no` values **and** swaps the two entries' order in `results.yaml` (so Appendix A
   stays in number order). Keys, sources and paper numbering do not change. In the source, narrow-windows already precedes
   blind-searches (lines 1017, 1022, 1264–1265), so after the swap the thesis render's numbers run in source order.
2. **`results.yaml` is rebuilt by chain step 1.** `t14/build_register.py` regenerates `results.yaml` from the Task 14 input table
   (`t14/input/register_table.csv`, a recorded input that must not change); `t15/t15_register.py`, `t16/t16_register.py` and
   `t19/t19_register.py` then patch it. A direct edit of `results.yaml` would be undone by the next chain run. Task 20 therefore
   follows the same pattern: a new chain step **`t20/t20_register.py`**, run after `t19/t19_register.py`, applies changes 1–3 to
   `results.yaml` and `references.yaml` and regenerates `register/crosswalk.md` (same layout as `t16_register.py`). It is
   idempotent. Appendix E's render chain gains this line, and its reproduction table a T20 row (`t15/make_appendix_de.py`).
3. **"7.6a" can be expressed without renumbering.** `thesis_no` is a free string; the renderer prints it verbatim and nothing in
   the chain parses it as a number (`chapter` is taken from the part before the dot). The entry is inserted in file order after
   7.6 and before 7.7. The register's header comment describes `thesis_no` as "chapter.counter"; "7.6a" is the one entry outside
   that form. The status is **`to-verify`**, the value `t14/build_register.py` already uses for results not yet independently
   verified. The prompt gives no title; the title used is **"Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6)"**, to be
   confirmed by the author. `cons_v1: null`, `legacy: []`, `citations: []`. The repository has no text for the lemma (the thesis
   draft holding it is not in the repository), so no source or thesis-only block is added; the key is not cited in any source.
4. **References.** `t15/t15_register.py` rewrites `references.yaml` from a frozen list of 53 keys (number 26 =
   `sahomasugi2016`); `t19/t19_register.py` then replaces **every** occurrence of `sahomasugi2016` with `roberts1959` in
   `references.yaml` and `results.yaml`. In a full chain run `t20_register.py` runs after that swap, so re-adding
   `sahomasugi2016` as [60] cannot be swapped. A stand-alone re-run of `t19_register.py` after `t20_register.py` **would** turn
   [60] into a second `roberts1959`; to prevent it, `t19_register.py` is narrowed (a generator change): in `references.yaml` it
   replaces the key only in the entry numbered 26, and in `results.yaml` only on a `citations` line that does not already contain
   `roberts1959`. On the chain's own input this does exactly what it did before.
5. **Unattached references.** The renderer prints every `references.yaml` entry in Appendix C whether or not any result cites it.
   Attachment is `citations` in `results.yaml`; the only checks that look at it are Task 14 C9 and Task 15 C1 (a bib key that is
   neither attached, nor cited by a `[@key]` token in a source, nor `planned`, is "unused"). The six chapter-1 references
   ([54]–[59]) are cited only in the thesis's chapter 1, which has no source in the repository. They are added **unattached**
   (no result cites them; attaching them to results would misstate where the thesis cites them). Their `first_cited` field
   records where they are cited. [60] `sahomasugi2016` is attached to 6.13 `discrete-excess` after `roberts1959`.
6. **Bibliography format.** Appendix C lines are produced by `register/bibfmt.py` (unchanged): four or more authors print as
   "First et al."; an `@article` prints "Journal vol(no), pages" and ignores `note`, `eprint` and `url`; an `@inproceedings`
   prints "booktitle, pages" (no publisher, no URL). The seven `references.bib` entries hold every element of the prompt's
   entries as BibTeX fields; where `bibfmt` does not print a field, the rendered line differs from the prompt's text (C6).
   - `sahomasugi2016`: the entry in `41d5e43:classification/references.bib` has title `$\alpha$-$\beta$-$\gamma$ tracking
     filters…` (hyphens, rendering "α-β-γ"); the prompt has "α–β–γ" (en dashes). It does not match, so the prompt's version is
     used (`$\alpha$--$\beta$--$\gamma$`); all other fields are the old entry's.
   - `jiang2026`: `@article`, `journal = {Automatica}`, `note = {accepted for publication; volume, pages and DOI not yet assigned}`,
     `eprint = {2407.05717}`, `archiveprefix = {arXiv}`, no `doi`.
   - `gotovos2013`: `@inproceedings`, `booktitle`, `pages`, `publisher = {AAAI Press}`, `url`, no `doi`.
   - New entries are taken from the prompt; they were not checked against Crossref (unreachable from the session in Tasks 17–19).
     A comment in `references.bib` says so.
7. **Figures.** `t15/t15_register.py` writes `register/figures.yaml` from its `FIGS` list and `DESC` dict; `t15/make_figs_thesis.py`
   names images `{label}_{key}` from that yaml; the renderer writes Appendix B in yaml order and cites figures by key
   (`{{fig:key}}`). The swap edits `FIGS` (order and labels) and `DESC` (keys), `source/figs/README.md` (section order) and
   `source/Roadmap_v3_Source.md` line 108 (token order).
8. **By-products the chain writes into recorded directories.** `t15/make_figs_thesis.py` and `t15/make_fig_B2.py` write capture
   pickles to `t15/results/` (`cap_new_t13.pkl`, `cap_new_t8.pkl`, `cap_B2.pkl`), keyed by output name, so the swap changes
   `cap_new_t13.pkl`. These are Task 15 recorded results: they are restored to `7855e45` after the chain and not committed. Two
   other known drifts are not committed either (found in the read-only review before this task): every thesis PDF is rewritten
   with a new `/CreationDate` (only the two renamed figures' PDFs are committed; the others are restored), and the chain rewrites
   two hand-edited lines of `register/tasks.yaml` (restored).
9. **Titles that also appear in body text.** Register titles are rendered only in Appendix A. The source still writes
   "$\rho > 2 + u$" with $u = 2\Sigma\Pi/\lambda^2$ (source lines 33, 573–588) and "post"/"avg" (§6); Task 20 changes titles only,
   as the prompt asks, and records the resulting mismatches in the results.

## Changes (artifacts commit, after this commit and before the recorded run)

| # | Change | Where |
|---|---|---|
| 1 | Titles: 2.1 "Topological realisability"; 2.8 "Reparameterisation (orientation swaps ℓ and h)"; 5.1 "Gain realisability"; 6.17 "D3 excess set; onset ρ > 2 + ν"; 6.19 "Optimal M-P along Δt: posterior ↓; prior ↑; averaged ↑". 8.1 = `narrow-windows`, 8.2 = `blind-searches` (thesis_no and order). No key changes. | `t20/t20_register.py` → `register/results.yaml`, `register/crosswalk.md` |
| 2 | Lemma 7.6a `whole-path-garbling` after 7.6 (see 3 above). | same |
| 3 | References [54]–[60] (status `cited`, first_cited "draft §1.6 Contributions and relation to prior work"); [60] attached to 6.13. | `t20/t20_register.py` → `register/references.yaml`, `register/results.yaml`; `references.bib`; `t19/t19_register.py` narrowed |
| 4 | `NOTES` dict and "- Recorded — …" lines after a task's failure bullets; the Task 13 line verbatim from the prompt. Appendix E: chain line `python3 t20/t20_register.py` after `t19/t19_register.py`, and a T20 row. | `t15/make_appendix_de.py` |
| 5 | Figures: B.5 = `peak-heights`, B.6 = `hill-phase`. | `t15/t15_register.py`, `source/figs/README.md`, `source/Roadmap_v3_Source.md` |
| 6 | Run the render chain (Appendix E order, with the new step); delete `figs_thesis/B.5_hill-phase.*` and `figs_thesis/B.6_peak-heights.*`; commit rendered outputs (except item 8's by-products). | renders |

The check script `t20/t20_checks.py` is written in the artifacts commit. It implements the criteria below and nothing else.

## Checks (recorded run, on the artifacts commit)

Baseline for every "committed" comparison: the file at `7855e45`.

### C1 — Register (Appendix A)
`Appendix_A_Register.md` is compared row by row with `7855e45`. **Pass** iff the difference is exactly:
(a) the rows 2.1, 2.8, 5.1, 6.17, 6.19 with the new titles and every other column unchanged;
(b) row 8.1 = `narrow-windows` and row 8.2 = `blind-searches`, each with its old type, title, verified-by and status, in that order;
(c) one new row `| 7.6a | Lemma | Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6) | \`whole-path-garbling\` | — | to-verify |`
immediately after the 7.6 row;
and no other row, header or intro line changes. Also: `results.yaml` has 83 entries with unique keys and unique `thesis_no`.

### C2 — References (Appendix C, references.yaml, references.bib)
**Pass** iff all hold:
(a) every line of `Appendix_C_References.md` up to and including the [53] line and its following blank line is byte-identical
to `7855e45`;
(b) seven further entries follow, numbered [54]–[60] in that order, for keys sinopoli2004, wu2018, jiang2026, bosov2026,
gotovos2013, tenne2002, sahomasugi2016; `references.yaml` numbers are 1–60 with unique keys, 26 = roberts1959,
60 = sahomasugi2016, and [54]–[60] have status `cited` and the prompt's first_cited;
(c) `bibfmt.fmt` returns a line for each of the seven without raising;
(d) the `doi` field equals the prompt's DOI string for 54, 55, 57, 59, 60, and is absent for 56 and 58;
(e) `results.yaml`: 6.13 citations = [roberts1959, sahomasugi2016]; no result cites any of 54–59; each key in `references.yaml`
is in `references.bib` and vice versa;
(f) collision test: the register steps of the chain run twice in a scratch clone give byte-identical `results.yaml` and
`references.yaml`, and `t19/t19_register.py` run alone afterwards changes neither file.

### C3 — Appendix D
`t15/make_appendix_de.py --with-t19` output compared with `7855e45`'s `Appendix_D_Verification.md`. **Pass** iff the only
difference is the insertion, directly after Task 13's last failure bullet, of the line
`- Recorded — ` + the prompt's Task 13 text (exactly), followed by the existing blank line; and the totals recomputed from the
regenerated file are 182 checks with a verdict, 37 fail, 38 failure lines (the "- Recorded" line is not counted as either).

### C4 — Figures
**Pass** iff all hold:
(a) `register/figures.yaml`: B.5 key `peak-heights`, B.6 key `hill-phase`, listed B.5 before B.6;
(b) `Appendix_B_Figures.md` shows "**Figure B.5.** Peak variance M/F…" with image `figs_thesis/B.5_peak-heights.png`, then
"**Figure B.6.** Hill gain…" with `figs_thesis/B.6_hill-phase.png`;
(c) `figs_thesis/README.md` has a `## Figure B.5` section showing `B.5_peak-heights.png` followed by `## Figure B.6` showing
`B.6_hill-phase.png`; `Roadmap_v3.md` row 5 says "Figures B.5, B.6" and the source tokens are peak-heights then hill-phase;
(d) no file `figs_thesis/B.5_hill-phase.*` or `figs_thesis/B.6_peak-heights.*` exists;
(e) `figs_thesis/B.5_peak-heights.png` is byte-identical to `7855e45:…/B.6_peak-heights.png`, and `figs_thesis/B.6_hill-phase.png`
to `7855e45:…/B.5_hill-phase.png`; the caption files `B.5_peak-heights.txt` and `B.6_hill-phase.txt` exist.

### C5 — Chain and later check scripts
In a fresh local clone of the artifacts commit (scratch directory outside the repository; nothing written to the repository):
(a) every render-chain step of the new Appendix E, in order, exits 0, `register/render.py` prints 0 errors, and afterwards every
tracked file is identical to the artifacts commit except the by-products of item 8 (capture pickles, PDF `/CreationDate`,
`register/tasks.yaml`);
(b) `t15/t15_checks.py`, `t15/t15_partG.py`, `t16/t16_checks.py`, `t17/t17_checks.py`, `t18/t18_checks.py`, `t19/t19_checks.py`
each exit 0, in that clone and in a fresh clone of `7855e45` (baseline), with the same Python environment;
(c) every check whose verdict differs between baseline and artifacts commit is attributed, by the difference in that check's own
recorded output, to one of the causes below. **Pass** iff (a) and (b) hold and no verdict change is unattributed.
Causes: **(i)** Appendix A records (new titles, 8.1/8.2, the 7.6a row, 83 entries); **(ii)** the Appendix D "Recorded" line;
**(iii)** references [54]–[60] (60 entries, 51 DOIs, `sahomasugi2016` live again, unattached keys);
**(iv)** the figure swap (labels, names, capture keys); **(v)** the `to-verify` status.
Expected differences (prediction, from reading the check code; not a criterion): T18 F6 and T19 G6 (A records) and G7(iv) on the
Appendix A titles; T19 G6 (D records) on the Recorded line; T15 C1 (entry and DOI counts) and T19 G7(i) (`sahomasugi2016` in live
files) on the references; T15 C5/C7 and T19 G5 possibly on the figure names. Checks already failing at baseline may stay failing.
`t19/t19_routes.py` and `t19/h13d_replay.py` (hours, no input touched by Task 20) and the Task 1–13 run scripts are not run.

### C6 — Sync with the thesis
**Pass** iff all hold:
(a) Appendix D's Task 13 entry contains "22 of 22 checks", and `t13/results/t13_A3_proof.json` has 22 items, all passing
(supports §7.5 "…passing 22 of 22 checks (Appendix D, Task 13)");
(b) the regenerated Appendix D totals are 182 checks with a verdict and 37 failed (§8.1);
(c) for each of [54]–[60], the `Appendix_C_References.md` line equals "[n] " followed by the prompt's text for that entry,
exactly (after Unicode NFC normalisation); and every element of the prompt's entry (authors in full, title, venue, volume,
number, pages, year, DOI / arXiv id / URL / status note) is present in the `references.bib` fields.

**Prediction (disclosed, from reading `bibfmt.py`; not run):** C6(c) fails on the rendered lines for [54], [55] and [58]
(four or more authors print as "et al."), [56] (`note` and arXiv id not printed for an `@article`) and [58] (publisher, URL and
"(no DOI)" not printed); [57], [59] and [60] are expected to match. The bib-field part is expected to hold. If so, C6 fails with
attribution **criterion/document** (the thesis's reference format differs from the repository's Appendix C format), and the
options are reported rather than `bibfmt.py` being changed (changing its rules would change lines [1]–[53], against C2).

## Disclosure: what is known before the run

The read-only review that preceded this task (same session, before the branch existed) re-ran the render chain and the T15–T19
check scripts at `7855e45` in a scratch copy: all exited 0; the chain reproduced the committed files except the PDF
`/CreationDate` and two lines of `register/tasks.yaml`; among the checks reporting a verdict, T15 C2, C3, C4, C10, T16 D6, D7, T17 E3, E4, E6, T18 F1, F6, T19 G6, G7 were
failing at `7855e45` (several because later tasks changed their inputs on purpose). No Task 20 change has been run.
