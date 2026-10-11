# Task 14: thesis numbering, Phase 1 roll-in, matrix fix and bibliography (results)

- Pre-registration: `classification/PREREG_t14.md`, commit **e5edebf**.
- Artifacts as checked: commit **45b0058**. The single recorded run of C1–C10 ran on this commit.
- Results and diagnoses: commit **5a217a5**.
- Python 3, PyYAML, SymPy, mpmath.

## Check table

| Check | Verdict | Counts / details | Runtime (s) |
|---|---|---|---|
| C1 Register integrity | **PASS** | 82 entries; keys unique and well-formed; thesis numbers unique and contiguous in chapters 2–8; v1 numbers 1–73 all mapped; 91 legacy A–E labels, 0 unmapped | 0.06 |
| C2 Reference resolution | **PASS** | 775 tokens, 78 keys referenced; 0 unresolved, 0 unreferenced (thesis-only exempt). Tokens without a heading: paper render 0; thesis render 4 (discrete-excess, optimal-envelope, stationary-variance, structural-stability), all cited by thesis number only | 0.06 |
| C3 No hand-typed numbers | **PASS** | 0 matches in the sources (phase1 sources, reported only: 0) | 0.01 |
| C4 Paper render reproduces v1 | **FAIL** | numbering shift exact (0 mismatches); 14 differing hunks: 6 split, 1 rows 25–26, 7 other, all the pre-disclosed type change of the excess identity | 0.15 |
| C5 Thesis render | **PASS** | 14 files; 0 'Paper 1', 0 A–E labels | 0.0 |
| C6 Matrix identity | **PASS** | thesis and Roadmap tables byte-identical (45 lines); rows 25–26 exact | 0.0 |
| C7 Errata value | **PASS** | m = 0.0099851849 (8 s.f.) at Π = 0.334832641112; 5 s.f. 0.0099852 | 0.03 |
| C8 Phase 1 records | **PASS** | all six Task 1–7 hashes exist: 0944b81, 2f9da71, 70ebb55, 824ca06, a0d2be2, d21f193 | 0.02 |
| C9 Bibliography | **FAIL** | 53 entries; 0 dangling; unused ['jazwinski1970', 'simon2006']; 21 DOI entries, 0 resolved (doi.org blocked), all marked VERIFY | 5.39 |
| C10 Reproduction unaffected | **FAIL** | 90 paths checked; 9 flagged; diagnosis: 9/9 flagged paths resolve when built the way their scripts build them; attribution: code (the dry run's literal resolver), not a missing file. | 0.01 |
| Part G (3.2 and 6.5) | **PASS** | G1–G6 all reduce to 0; G6 at 20 rational points max abs. difference 1.5558e-61 |  |

**Pre-registered checks that FAIL:** C4 Paper render reproduces v1; C9 Bibliography; C10 Reproduction unaffected. Each is diagnosed below; no criterion was changed and no artifact was changed after the recorded run.

## Plain statements

- **Did any mathematical content change?** No. The paper render differs from the consolidated v1 only as follows:
  - numbers shift by one for v1 numbers 7 and above;
  - the window theorem's addendum is split out (same text; the lead-in becomes "In the setting of …", and "Proof of the addendum" becomes "Proof");
  - matrix rows 25–26 use the prescribed wording, which has the same content as v1;
  - the excess identity is printed as a Corollary instead of a Proposition, as the register types it.
  The thesis render differs from the paper render only in numbers, the `{{phase1}}` phrase, and the conditional passages listed in the source. No mathematical error was found.
- **What still needs a human decision?**
  1. The excess identity is typed Corollary in the register and was Proposition in v1. This is why C4 fails as worded. Accept the type change for the Paper 2 render, or give the register a separate paper type.
  2. `jazwinski1970` and `simon2006` are in the prompt's entry list but not in its attachment table, so C9 fails on them. Attach them to a result, or drop them.
  3. Roadmap §7, query rows for clusters 11–17: the second search set's query text and its clustering were not supplied. The rows give a topic and the bib keys grouped under it, marked "query text not supplied". Confirm or replace them.
  4. The images of fig01 (axis title) and fig06 (legend) carry v1 numbers (Theorem 2, Theorem 25). `figs_paper2/` was left untouched. The thesis captions in `figs_thesis/` link these images and say so. Regenerating the images needs a decision on how their labels are numbered.
  5. 34 bibliography entries carry `VERIFY` notes (listed below). No DOI could be resolved, because doi.org is blocked from this session.
  6. The starting-study manuscript was supplied mid-task as a PDF only, with no LaTeX source. It was added unchanged; since it was never in the repository, no history could be kept.
  7. The thesis-only results (2.3, 2.8, 2.9, 3.2, 6.5) have no text in the repository. Part G checked 3.2 and 6.5 in the reading ν = 2ΣΠ/λ², q = G/(FΠ), t = λτ, and both hold in that reading. Results 3.1, 3.5 and 6.13 have no heading in the consolidated document; the thesis render cites them by number, and their statements are in the manuscript.
  8. The prompt's CSV row for 3.2 had an unquoted comma in its title (`V(ν,q)`). The input copy (`t14/input/register_table.csv`) quotes it; nothing else was changed.

## Diagnoses

1. **C4 (attribution: criterion).** All 7 "other" hunks are the excess identity's type, printed from the register: its heading, its label line, the §12 row, the v1 number-map row, and three references ("Proposition 4" → "Corollary 4"). The pre-registration predicted this (disclosure item 4). The numbering check passed: every key's paper number is its v1 number, +1 for 7 and above, and the split result is 7. There is no other difference.
2. **C9 (attribution: input/criterion).** `jazwinski1970` and `simon2006` are not attached to any result in the prompt's citation table, and no source cites them. Every DOI entry is marked VERIFY because doi.org is unreachable (proxy CONNECT 403, every DOI).
3. **C10 (attribution: code).** The pre-registered dry run resolved string literals only against `classification/`, the script's directory and the repository root.
   - It flagged 9 literals. In `t14_c10_diag.py` each was resolved the way its script builds the path:
     - the two Task 13 audit scripts' `DOC`, evaluated by import, is the archived v1, which exists;
     - `README.md` in `t13_figures_paper2.py` is written by the script, not read;
     - the six `t*_symbolic*.py` names in `t13_regression_symbolic.py` are copied from `classification/t9`…`t12`, and all exist.
   - No file is missing. The only change Task 14 made for reproduction is the path fallback in `t13_audit_numbers.py` and `t13_audit_refs.py` (disclosure item 6).
4. **Development note (disclosure).** The converter (`make_source.py`) was developed by rendering in v1-number mode and diffing against v1, which is C4's method (ii). It was therefore known before the recorded run that the only remaining differences were the predicted ones.
5. **Deviation from the pre-registration's output list.** The pre-registration planned a `MANUSCRIPT_LOCATION.md` stub because the manuscript was absent. The author then supplied it, so it is now in `reference/phase1/` and the stub was not kept. The errata quotes were checked against its text, all verbatim (pp. 5, 5, 8, 12). The value m = 0.0099852 is not in the manuscript; C7 confirms it.

## C4 diff summary

Raw diff, actual paper render against v1: 691 changed lines. Almost all are numbers ≥ 7 shifted by one. In the v1-number render (method (ii)) there are 14 hunks:

| v1 lines | Category | v1 | render |
|---|---|---|---|
| 141-141 | other | **Proposition 4 (excess identity; Paper 1).** | **Corollary 4 (excess identity; Paper 1).** |
| 148-148 | other | **Label:** Proposition (proved in Paper 1; T8.1(c)). | **Label:** Corollary (proved in Paper 1; T8.1(c)). |
| 165-165 | other | $\sqrt{\lambda^2 + 2\Sigma\Pi} > \lambda$. The last statement is Proposition 4. As $G \to \infty$, $\sigma^2 \ | $\sqrt{\lambda^2 + 2\Sigma\Pi} > \lambda$. The last statement is Corollary 4. As $G \to \infty$, $\sigma^2 \si |
| 176-176 | b (split) | If moreover $G$ is increasing and $G(\Pi)/\Pi$ is strictly decreasing (e.g. any sum of Bayesian stages |  / **Label:** Theorem (proved in Paper 1 and its verification suite; optimal part re-checked T13 C2 row 1). /  |
| 180-180 | b (split) | *Proof of the addendum.* $2\Pi^2(\lambda + G)^2\,d\sigma^2/d\Pi = \Pi G'(2\lambda G + G^2 - 2\Sigma\Pi) - G^2( | *Proof.* $2\Pi^2(\lambda + G)^2\,d\sigma^2/d\Pi = \Pi G'(2\lambda G + G^2 - 2\Sigma\Pi) - G^2(\lambda + G)$, a |
| 184-185 | b (split) | **Label:** Theorem (proved in Paper 1 and its verification suite; optimal part re-checked T13 C2 row 1; addend | **Label:** Proposition (proved post hoc from the T13 C2 row-8 failure, SymPy steps in `t13_audit_classes_diag2 |
| 850-850 | other | **Label:** Lemma (proved; Proposition 4). | **Label:** Lemma (proved; Corollary 4). |
| 962-962 | b (split) | Bayesian sums the windows always lie above $F$ and never join a lower ray (Theorem 6, addendum). | Bayesian sums the windows always lie above $F$ and never join a lower ray (Proposition 6+). |
| 1149-1149 | b (split) | \| 8 \| $\Pi$ \| env. \| two-stage Bayesian \| $F$ → $\Sigma/(\lambda + c_1 + c_2)$ (above) \| up to 3 seen \| — \| A, | \| 8 \| $\Pi$ \| env. \| two-stage Bayesian \| $F$ → $\Sigma/(\lambda + c_1 + c_2)$ (above) \| up to 3 seen \| — \| A, |
| 1167-1168 | c (rows 25-26) | \| 25 \| $\Delta t$ (M-P) \| either \| D1, prior \| $\sigma^2(G, \Pi)$ → $F$ (below) \| none, min, max–min \| limits, | \| 25 \| $\Delta t$ (M-P) \| either \| D1, prior \| $\sigma^2(G, \Pi)$ → $F$ (below) \| none, min, max–min \| limits, |
| 1222-1222 | other | \| 4 \| Proposition \| excess identity \| Paper 1; T8.1 \| | \| 4 \| Corollary \| excess identity \| Paper 1; T8.1 \| |
| 1225-1224 | b (split) |  | \| 6+ \| Proposition \| no mixed class when $G/\Pi$ decreases \| T13 C2 (row-8 diagnosis) \| |
| 1268-1268 | other | \| 50 \| Lemma \| excess components \| T8.1 (Proposition 4) \| | \| 50 \| Lemma \| excess components \| T8.1 (Corollary 4) \| |
| 1376-1376 | other | \| Paper 1: excess identity, window theorem, Bayesian-weight \| Proposition 4, Theorem 6, Proposition 7 \| | \| Paper 1: excess identity, window theorem, Bayesian-weight \| Corollary 4, Theorem 6, Proposition 7 \| |

## Inventory (§1, state at the pre-registration commit)

Repository: 474 tracked files. Top level: `classification/` (Tasks 8–14), `verification/` (the starting study's suite: `PREREG.md`, `PREREG_t6.md`, `PREREG_t7.md`, `REPORT.md`, scripts `t1_symbolic.py`, `t2_em.py`, `t3_paired.py`, `t4a`–`t4e`, `t6_colored_symbolic.py`, `t7_*.py`, `run_all.sh`).

- **Starting-study manuscript:** no PDF, TeX or Word file in any commit or branch. It was supplied by the author during Task 14.
- **Task 1–7 commits:** d21f193 (pre-registration), 50f1b38…6457bad (T1–T4), 70ebb55 (results), 637d542 (report), 824ca06/0944b81 (T6), a0d2be2/2f9da71/183cb8f (T7).

Legacy-reference counts per file in `classification/`:
- legacy regex: Prop./Thm/… followed by a number;
- A–E labels;
- 'Paper 1'.

| File | Legacy regex | A–E | Paper 1 |
|---|---|---|---|
| classification/Bounded_Failure_Window_Classification_Roadmap_v2-1.md | 1 | 0 | 17 |
| classification/PREREG_t10.md | 1 | 0 | 1 |
| classification/PREREG_t11.md | 12 | 0 | 0 |
| classification/PREREG_t12.md | 1 | 0 | 0 |
| classification/PREREG_t13.md | 18 | 0 | 0 |
| classification/PREREG_t14.md | 17 | 0 | 5 |
| classification/PREREG_t8.md | 3 | 0 | 3 |
| classification/PREREG_t9.md | 14 | 0 | 1 |
| classification/REPORT.md | 4 | 0 | 5 |
| classification/Roadmap_v3.md | 108 | 0 | 3 |
| classification/Stage_0_1_Classification_Results.md | 21 | 0 | 6 |
| classification/Stage_2_Completion_Results.md | 50 | 8 | 6 |
| classification/Stage_2_Tau_Sweep_Results.md | 21 | 0 | 1 |
| classification/Stage_3_Falsification_Results.md | 55 | 0 | 12 |
| classification/Stage_3_Plan.md | 6 | 0 | 8 |
| classification/Stage_4_Optimality_Results.md | 51 | 0 | 4 |
| classification/Stages_0_4_Consolidated.md | 408 | 1 | 24 |
| classification/Task_10_Stage3_Prompt.md | 2 | 0 | 3 |
| classification/figs_paper2/README.md | 11 | 0 | 1 |
| classification/figs_paper2/fig01_stage1_schematic.txt | 1 | 0 | 0 |
| classification/figs_paper2/fig02_realizability.txt | 1 | 0 | 0 |
| classification/figs_paper2/fig03_hill_phase.txt | 2 | 0 | 0 |
| classification/figs_paper2/fig05_tau_normalizations.txt | 1 | 0 | 0 |
| classification/figs_paper2/fig07_delay.txt | 2 | 0 | 0 |
| classification/figs_paper2/fig08_optimal_sampling.txt | 2 | 0 | 0 |
| classification/figs_paper2/fig09_sampled_relay.txt | 1 | 0 | 0 |
| classification/figs_paper2/fig10_process_noise.txt | 1 | 0 | 1 |
| classification/results/t8.txt | 1 | 0 | 1 |
| classification/t10/RESULTS_t10.md | 0 | 0 | 2 |
| classification/t10/classify.py | 1 | 0 | 0 |
| classification/t10/make_results_t10.py | 0 | 0 | 2 |
| classification/t11/RESULTS_t11.md | 25 | 0 | 0 |
| classification/t11/make_results_t11.py | 25 | 0 | 0 |
| classification/t11/t11_delay.py | 1 | 0 | 0 |
| classification/t11/t11_garble.py | 1 | 0 | 0 |
| classification/t11/t11_notnec.py | 1 | 0 | 0 |
| classification/t11/t11_power_diag.py | 1 | 0 | 0 |
| classification/t11/t11_sampling.py | 2 | 0 | 0 |
| classification/t12/RESULTS_t12.md | 2 | 0 | 0 |
| classification/t12/make_results_t12.py | 2 | 0 | 0 |
| classification/t13/RESULTS_t13.md | 82 | 0 | 0 |
| classification/t13/literature_check.md | 3 | 0 | 0 |
| classification/t13/make_results_t13.py | 23 | 0 | 0 |
| classification/t13/referee_report.md | 59 | 0 | 0 |
| classification/t13/t13_A3_limits.py | 1 | 0 | 0 |
| classification/t13/t13_audit_numbers.py | 1 | 0 | 0 |
| classification/t13/t13_figures_paper2.py | 14 | 0 | 1 |
| classification/t13/t13_partA_symbolic.py | 8 | 0 | 0 |
| classification/t8_classify.py | 2 | 0 | 0 |
| classification/t8_common.py | 2 | 0 | 1 |
| classification/t8_no_window.py | 1 | 0 | 0 |
| classification/t8_realize.py | 1 | 0 | 0 |
| classification/t8_report.py | 4 | 0 | 5 |
| classification/t8_symbolic.py | 1 | 0 | 4 |
| classification/t9/RESULTS_t9.md | 8 | 0 | 0 |
| classification/t9/make_results_t9.py | 8 | 0 | 0 |
| classification/t9/t9_symbolic.py | 3 | 0 | 2 |
| **total** | 1098 | 9 | 119 |

## Files moved or created

- **Moved (`git mv`, unchanged):** `classification/Stages_0_4_Consolidated.md` → `classification/archive/Stages_0_4_Consolidated_v1.md`.
- **Added unchanged:** `reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf` (the author's upload).
- **Register:** `classification/register/` with `results.yaml`, `tasks.yaml`, `matrix.csv`, `crosswalk.md`, `crosswalk_v1.yaml` and `render.py`.
- **Sources:** `classification/source/` with `Stages_0_4_Source.md`, `Roadmap_v3_Source.md`, `figs/*.txt`, `figs/README.md`, `phase1/README.md` and `phase1/ERRATA.md`.
- **Renders (thesis):** `classification/Stages_0_4_Thesis.md`, `classification/Roadmap_v3.md` (overwritten; the earlier version is in git history), `classification/figs_thesis/` (10 captions and `README.md`), `classification/Appendix_A_Register.md`, `reference/phase1/README.md` and `reference/phase1/ERRATA.md`.
- **Render (paper):** `classification/Stages_0_4_Paper2.md`.
- **Bibliography:** `classification/references.bib` and `classification/t14/bib_check.md`.
- **Task 14 code:** `classification/t14/` with `t14_common.py`, `t14_inventory.py`, `build_register.py`, `make_source.py`, `make_roadmap_source.py`, `make_bib.py`, `make_bib_check.py`, `t14_checks.py`, `t14_c10_diag.py`, `t14_partG.py`, `make_results_t14.py`, `input/register_table.csv`, and `results/`.
- **Changed:** `classification/t13/t13_audit_numbers.py` and `t13_audit_refs.py`, which got a path fallback to the archived v1 (organisation only).

Regenerate everything with:
`python3 t14/build_register.py && python3 t14/make_source.py && python3 t14/make_roadmap_source.py && python3 register/render.py --numbering thesis && python3 register/render.py --numbering paper && python3 t14/make_bib.py`.

## VERIFY flags left in the bibliography

See `t14/bib_check.md` for the evidence behind each confirmed field.

| Key | Still to verify |
|---|---|
| heffes1966 | DOI not captured (10.1109/TAC.1966.1098392 appears only in a search summary) |
| friedland1967 | journal, volume, issue and pages (J. Basic Eng. 82(1), 35-45 per the prompt; seen only in search summaries); DOI not resolved at doi.org (unreachable from this session) |
| jazwinski1970 | publisher (Academic Press per catalog summaries; ISBN confirmed via the Elsevier listing) and edition |
| andersonmoore1979 | edition and publisher |
| simon2006 | edition |
| blackwell1951 | pages (search evidence points to 93-102, not 99-102, but only through summaries) |
| blackwell1953 | DOI not resolved at doi.org (unreachable from this session) |
| brysonjohansen1965 | title, venue, volume and pages (a search summary gives 'Linear filtering for time-varying systems using measurements containing colored noise', IEEE TAC 10(1), 4-10; not confirmed); DOI not resolved at doi.org (unreachable from this session) |
| brysonhenrikson1968 | title and venue (a search summary gives 'Estimation using sampled data containing sequentially correlated noise', J. Spacecraft and Rockets 5(6), 662-665; not confirmed); DOI not resolved at doi.org (unreachable from this session) |
| chang2014 | journal, volume and pages (Journal of Geodesy 88, 1163-1170 per one catalog summary); DOI not resolved at doi.org (unreachable from this session) |
| kalata1984 | number and pages (174-182 in one index, 174-181 in a reference list); DOI (10.1109/TAES.1984.310438 given in the prompt; not confirmed) |
| sahomasugi2016 | volume and article number (5, 309 per a search summary); DOI not resolved at doi.org (unreachable from this session) |
| ernstbanks2002 | title |
| barshalom2002 | pages (prompt 769-778; the IEEE record as quoted in a search summary gives 769-777); DOI (probably 10.1109/TAES.2002.1039398; not confirmed) |
| yoder2018 | full author list; DOI not resolved at doi.org (unreachable from this session); full author list |
| greenshtein1996 | DOI not resolved at doi.org (unreachable from this session) |
| yuksellinder2012 | issue (2, per a search summary); DOI not resolved at doi.org (unreachable from this session) |
| yukselbasar2013 | DOI not resolved at doi.org (unreachable from this session) |
| hogeboomburr2021 | title and DOI (not confirmed by search) |
| torgersen1991 | DOI not resolved at doi.org (unreachable from this session) |
| hansentorgersen1974 | DOI not resolved at doi.org (unreachable from this session) |
| hotzskelton1987 | DOI not resolved at doi.org (unreachable from this session) |
| hotzskelton1985 | DOI (10.1109/CDC.1985.268547 per a search summary; not confirmed) |
| collinsskelton1987 | DOI (not found) |
| xuskelton1992 | DOI not resolved at doi.org (unreachable from this session) |
| yasuda1993 | DOI |
| skeltonikeda1989 | title and DOI (nothing confirmed by search, including the author pairing and the volume/pages) |
| martinezrey2017 | DOI not resolved at doi.org (unreachable from this session) |
| shmaliy2020 | full author list, volume and pages (Shmaliy, Zhao and Ahn, 14(2), 64-71 per a search summary); DOI not resolved at doi.org (unreachable from this session); full author list |
| heeger1992 | DOI not resolved at doi.org (unreachable from this session) |
| carandiniheeger2012 | DOI not resolved at doi.org (unreachable from this session) |
| cohensteiner2007 | DOI not resolved at doi.org (unreachable from this session) |
| edelsbrunnerharer2010 | DOI not resolved at doi.org (unreachable from this session) |
| carr2003 | DOI not resolved at doi.org (unreachable from this session) |

## Provenance

- Pre-registration: e5edebf. Artifacts checked: 45b0058. Results: 5a217a5.
- Runtimes: C1–C10 total 5.7 s; Part G about 1 s; the inventory and every build script under 2 s each.
- Web: the bibliography search was run by a subagent of this session (37 searches) with an evidence rule. Only link titles and URLs count; generated summaries do not. doi.org and api.crossref.org were blocked.


## Addendum after Task 14: author-verified bibliography (supersedes the generated file)

After the recorded check run, the author supplied a DOI-verified `references.bib`. It was checked on 2026-10-11 against Crossref,
Project Euclid, arXiv and publisher/catalogue records. It replaces the file generated by `t14/make_bib.py`; that script and
`t14/bib_check.md` remain as the record of Task 14's own search.
- Same 53 keys. No citation key in `register/results.yaml` is dangling.
- 46 entries now carry DOIs, and none carries a VERIFY note, so item 5 of "What still needs a human decision?" is resolved.
- The author file agrees with the discrepancies recorded in `bib_check.md`: Bar-Shalom pp. 769–777; Blackwell (1951) pp. 93–102.
- The recorded C9 verdict (FAIL) is unchanged, because results are final. Its cause that remains is that `jazwinski1970` and
  `simon2006` are still not attached to any result (decision item 2).
