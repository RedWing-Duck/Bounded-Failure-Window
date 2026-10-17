# Task 21: figure labels in B.8, B.9 and B.10 (results)

- **Branch:** `task-20-thesis-sync`. Not pushed or merged.
- **Pre-registration:** `classification/PREREG_t21.md`, commit **38de807**, with the request in `t21/input/Task21_prompt.md`.
- **Artifacts as checked:** commit **28486b5**. The change is six `TEXT_EDITS` pairs in `t15/make_figs_thesis.py`; the
  regenerated `figs_thesis/B.8_*`, `B.9_*` and `B.10_*` images and `t15/gen/gen_figs_t13.py` are committed with it.
- **Recorded run:** `python3 t21/t21_checks.py`, run once (44 s), output in `t21/results/t21_checks.json` and `logs/`.
- **Environment:** Python 3.13.16 and the package versions of Appendix E. The platform string is now `…fc-v139…`.

## Check table

| Check | Verdict | Details |
|---|---|---|
| K1 Data unchanged | **FAIL** | 11 figures in both captures. Only `B.6_hill-phase` is reported, and only arrays 0 and 1 (lines of shape (70, 2)) |
| K2 Exactly the requested text changes | **PASS** | B.8: 1 change; B.9: 4 changes; B.10: 2 x-labels. All are as pre-registered, and no other text element changed in any figure |
| K3 Images | **FAIL** | The three PNGs changed (as required), but so did `B.8_optimal-sampling.pdf`, `B.9_sampled-relay.pdf` and `B.10_process-noise.pdf`. Every other `figs_thesis/` file is byte-identical |
| K4 Chain | **FAIL** | All 12 steps exit 0 and render reports 0 errors. One tracked file differs outside the by-products: `Appendix_E_Reproduction.md` |

**Totals: 4 checks, 1 pass, 3 fail.** None of the failures is a defect in the figures; each comes from the check code or the
criterion wording (see Diagnoses).

## Diagnoses

1. **K1 (attribution: code).** The two hill-phase lines contain NaN gaps, and `numpy.array_equal` treats NaN as unequal to
   NaN. In a post-hoc reading (no re-run of the check), `array_equal(..., equal_nan=True)` is True for both arrays, and
   `B.6_hill-phase.png` is byte-identical in the pre and post clones. B.6 received no edit. The plotted data are unchanged.
2. **K3 (attribution: criterion).** The criterion allowed only the three PNGs to change, but the edited figures' PDFs carry
   the same text and necessarily change with them. The pre-registered change list ("`figs_thesis/B.8_*`, `B.9_*`, `B.10_*`
   images") includes the PDFs; the criterion omitted them.
3. **K4 (attribution: criterion / environment).** Appendix E records the platform string. The container's kernel string
   changed since Task 20 (`fc-v114` → `fc-v139`), so a regenerated Appendix E differs in that one line. The by-product list in
   the criterion did not name it. The committed Appendix E was left as Task 20 recorded it.

## Not changed (scope; recorded)

- The repository's captions for these figures (`source/figs/fig08_optimal_sampling.txt`, `fig09_sampled_relay.txt`,
  `fig10_process_noise.txt`, rendered into `figs_thesis/*.txt` and Appendix B) still say "(post)", "avg/F - 1" and "u".
- Text inside the images that the request did not name:
  - B.8's legend entry "time average";
  - B.9's right-panel title "D1, time average: two rays (dip of 0.125%)".
