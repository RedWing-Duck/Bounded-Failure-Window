# Task 20: bring the repository in line with the thesis text (results)

- **Branch:** `task-20-thesis-sync`, from `7855e45` (Task 19 results commit). Not pushed or merged.
- **Pre-registration:** `classification/PREREG_t20.md`, commit **e7881bf** (with the prompt in `t20/input/Task20_prompt.md`).
- **Artifacts as checked:** commit **b254b32**. This is `adca3b7` (the changes and renders) plus `b254b32` (a crash fix in
  `t20/t20_checks.py`, see Notes).
- **Recorded run:** `python3 t20/t20_checks.py --work <scratch>`, run once on b254b32. Raw output is in `t20/results/t20_checks.json`,
  logs are in `t20/results/logs/`, and the C5 diffs are in `t20/results/c5_diffs.md`. The C5 attribution was read after the run and is
  in `t20/results/c5_attribution.yaml`. The C5 verdict was then set by `t20_checks.py --verdict`, which re-runs nothing.
- **Environment:** Python 3.13.16, numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0, matplotlib 3.11.2, PyYAML 6.0.1.

## Check table

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| C1 Register (Appendix A) | **PASS** | The rendered Appendix A equals the expected one: 7855e45 with the five new titles, 8.1 = `narrow-windows`, 8.2 = `blind-searches`, and the 7.6a row after 7.6. There are no other differences. `results.yaml` has 83 entries, with unique keys and unique numbers | 0.1 |
| C2 References | **PASS** | (a) Lines up to [53] are byte-identical. (b) [54]–[60] are in order and equal `bibfmt` output; `references.yaml` runs 1–60, with 26 = roberts1959 and 60 = sahomasugi2016. (c) No `bibfmt` errors. (d) All DOIs match, and 56 and 58 have none. (e) 6.13 cites [roberts1959, sahomasugi2016]; no result cites 54–59. (f) The register steps run twice give identical files; `t19_register.py` run alone afterwards prints "0 replaced" twice and changes nothing | 1.6 |
| C3 Appendix D | **PASS** | The only difference from 7855e45 is the inserted Task 13 "Recorded" line. Totals are 182 checks, 145 pass, 37 fail, 38 failure lines, 1 Recorded line. The regenerated file equals the committed one | 0.0 |
| C4 Figures | **PASS** | `figures.yaml` has B.5 = peak-heights and B.6 = hill-phase. Appendix B, `figs_thesis/README.md` and the Roadmap ("Figures B.5, B.6") are in the new order. No stale files remain. The PNGs are byte-identical to the old B.6 and B.5 PNGs, and the captions exist | 0.0 |
| C5 Chain and T15–T19 check scripts | **PASS** | (a) The 12-step chain exits 0 at the artifacts commit; render prints 0 errors. The tracked files that change are the by-products only: PDF `/CreationDate`, `tasks.yaml` and `cap_new_t13.pkl`. The 11-step chain at 7855e45 also exits 0. (b) All 12 script runs (6 scripts × 2 commits) exit 0. (c) One verdict changed, T15 C1 (PASS → FAIL), attributed to cause (iii). Nothing is unattributed | 1,834.9 |
| C6 Sync with the thesis | **FAIL** | (a) "22 of 22 checks": holds, and `t13_A3_proof.json` has 22 items, all passing. (b) 182 checks / 37 failed: holds. (c) The bib fields hold every element of all seven entries, but the rendered Appendix C lines equal the prompt's text only for [57], [59] and [60]; [54], [55], [56] and [58] differ | 0.0 |

**Totals: 6 checks, 5 pass, 1 fail (C6).** C6 failed as pre-registered ("Prediction (disclosed …)").

## Diagnoses

### 1. C6(c) (attribution: criterion / document)

The prompt's reference entries are written in a different format from the one the repository's Appendix C uses (`register/bibfmt.py`,
unchanged). Rendered lines against the prompt:

- **[54] and [55]:** "Sinopoli, B. et al." and "Wu, J. et al." are printed, because four or more authors print as "First et al.".
  The full author lists are in `references.bib`.
- **[56]:** printed "… covariance recalibration. Automatica." For an `@article`, `bibfmt` does not print `note` ("accepted for
  publication; volume, pages and DOI not yet assigned") or `eprint` ("arXiv:2407.05717"); both are in the bib entry.
- **[58]:** printed "Gotovos, A. et al. … (IJCAI 2013), 1344–1350." The "et al." rule applies, an `@inproceedings` prints no
  publisher ("AAAI Press") and no URL, and "(no DOI)" is not printed. Publisher and URL are in the bib entry.
- **[57], [59] and [60]:** identical to the prompt.

Changing `bibfmt.py` would also change lines [1]–[53] (for example [9] and [53] use "et al."), which C2 forbids. The options are
listed in the report, not taken.

### 2. C5 prediction (attribution: prediction)

PREREG_t20 predicted verdict changes in T18 F6, T19 G6 and G7(iv) on the Appendix A titles, T19 G6 on the Recorded line, T19 G7(i)
on `sahomasugi2016`, and possibly T15 C5/C7 and T19 G5. None of these changed verdict. T18 F6, T19 G6 and T19 G7 already failed at
7855e45, and their outputs changed for causes (i) and (iii):
- F6/G6: seven Appendix A differences and Appendix C differences;
- G7: `sahomasugi2016` live in `references.bib` (the entry and the Task 20 comment), `references.yaml` and `results.yaml`.

T15 C5/C7 and T19 G5 stayed PASS. The prediction was not a criterion. The only verdict change was T15 C1, which the prediction
listed under the references.

Checks whose output changed with the same verdict, and the cause of each:
- T15 C2, C3: references; still FAIL.
- T15 C5, C7: figure names; still PASS.
- T15 C9: mentions; still PASS.
- T15 C10, T16 D6, T17 E7: figure-label exemption counts; verdicts unchanged.
- T17 E2: result count 49.
- T18 F3, T19 G3: their mention lists now include `PREREG_t20.md`.
- T19 G4: register titles.

## Notes

1. **Crash fix before the recorded run (code).** A crash-only smoke test of `t20_checks.py` found that `chain_steps` split
   Appendix E at the first mention of "render chain", which is a table row, and raised `IndexError`. It now splits at the section
   heading (commit b254b32).
   The smoke test called C1, C4, C6, C2, the C5 chain pieces and C3 with their results not printed. Their logs were deleted.
   One thing seen bears on an outcome, and is disclosed here: while the bib entries were being written (after the
   pre-registration), `bibfmt.fmt` was run on the seven new entries once. Its output matched the pre-registered C6 prediction.
2. **Titles that the body text still contradicts (document).** Task 20 changed titles only, as asked:
   - 6.17's title now says ν, but the source body (`source/Stages_0_4_Source.md` lines 33 and 573–588, rendered in
     `Stages_0_4_Thesis.md`) still writes u = 2ΣΠ/λ².
   - 6.19's title says posterior/averaged, but the body says "post"/"avg".
   - The 2.8 thesis-only text (`source/thesis_only/reparameterisation.md`) still says "ℓ and u".
3. **Lemma 7.6a.** The register holds it as `thesis_no: '7.6a'` (a free string; no renumbering), with status `to-verify` and title
   "Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6)". The prompt gave no title, so this one is for the author to confirm. The
   repository has no text for the lemma, and no source cites the key. The register header still describes `thesis_no` as
   "chapter.counter", and 7.6a is the one exception. The T18/T19 Appendix A record parsers count 82 records, not 83, because their
   pattern does not read "7.6a".
4. **Appendix C intro.** It still says "Numbered in order of first citation … References [46]–[53] are first cited in chapters 6–7".
   [54]–[60] are first cited in §1.6 but carry the next free numbers, as the frozen-numbering rule requires.
5. **Keys.** No key changed. `topological-realizability` and `realizability` keep their -ize spelling: keys are permanent and the
   title change does not require a new key.
