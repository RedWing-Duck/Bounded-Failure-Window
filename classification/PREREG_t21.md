# Pre-registration — Task 21: figure labels in B.8, B.9 and B.10

Committed **before** any Task 21 change and before any Task 21 check is run. Not edited after its commit. The checks K1–K4 run
**once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis (criterion, input, code,
document or prediction).

**Base:** branch `task-20-thesis-sync` at `8ea738d` (Task 20 results commit). Nothing is pushed or merged.
**Input:** the author's request, copied verbatim to `classification/t21/input/Task21_prompt.md` (this commit).
**Scope:** text elements of three thesis figures only. No data, parameter, curve or caption changes; no recorded file of Tasks
1–20 changes; Task 20's results stay as recorded.

## How the repository works

`t15/make_figs_thesis.py` (render-chain step) copies `t13/t13_figures_paper2.py` (a Task 13 artifact, not edited), applies
`TEXT_EDITS` — (old text, new text) pairs, each asserted to occur exactly once — and runs the copy through `t15/fig_harness.py`,
which records every saved figure's plotted arrays and text elements in a capture pickle. Task 15 used the same mechanism to remove
result numbers from three figures. Task 21 adds six pairs to `TEXT_EDITS`; nothing else in the script changes.

## Changes (artifacts commit)

`t15/make_figs_thesis.py`, `TEXT_EDITS`, six new pairs (old → new, as Python source in `t13/t13_figures_paper2.py`):

| Figure | Element | Old | New |
|---|---|---|---|
| B.8 | legend | `"post (just after a sample)"` | `"posterior (just after a sample)"` |
| B.9 left | legend | `label="post"` | `label="posterior"` |
| B.9 left | title | `"D1, post: a window"` | `"D1, posterior: a window"` |
| B.9 right | legend | `label=r"avg$/F - 1$"` | `label=r"averaged$/F - 1$"` |
| B.9 right | y-axis | `set_ylabel(r"avg$/F - 1$")` | `set_ylabel(r"averaged$/F - 1$")` |
| B.10 both | x-axis | `r"$u = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)"` | `r"$\nu = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)"` |

Then run the render chain (Appendix E); commit `figs_thesis/B.8_*`, `B.9_*`, `B.10_*` images and `t15/gen/gen_figs_t13.py`.
As in Task 20, the chain's by-products are restored, not committed: capture pickles in `t15/results/`, `register/tasks.yaml`, and
PDFs whose only change is `/CreationDate`.

**Not changed (scope):** the repository's captions (`source/figs/fig08…`, `fig09…`, `fig10….txt`, rendered into
`figs_thesis/*.txt` and Appendix B) still say "post", "avg/F - 1" and "u". The request covers image labels only; the mismatch is
recorded in the results.

## Checks (recorded run: `python3 t21/t21_checks.py`)

Captures: `make_figs_thesis.py` run in a fresh scratch clone of `8ea738d` (pre) and of the artifacts commit (post); each capture
pickle is read from its clone, nothing is written to the repository except `t21/results/`.

- **K1 — data unchanged.** For every figure in both captures (t13 set and t8 set), the plotted arrays are identical
  (same count, shape and values, `numpy.array_equal`). **Pass** iff all are identical and both captures hold the same figures.
- **K2 — exactly the requested text changes.** The text elements differ between pre and post only in B.8, B.9 and B.10, and the
  differences are exactly: B.8 legend "post (just after a sample)" → "posterior (just after a sample)"; B.9 legend "post" →
  "posterior", title "D1, post: a window" → "D1, posterior: a window", legend and y-label "avg$/F - 1$" → "averaged$/F - 1$";
  B.10 both x-labels "$u = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)" → "$\nu = …$". **Pass** iff no other text element
  changes in any figure.
- **K3 — images.** `figs_thesis/B.8_optimal-sampling.png`, `B.9_sampled-relay.png` and `B.10_process-noise.png` differ from
  `8ea738d`; every other `figs_thesis/` file is byte-identical to `8ea738d`. **Pass** iff both hold.
- **K4 — chain.** In the post clone, every render-chain step exits 0 and `register/render.py` prints 0 errors, and afterwards every
  tracked file equals the artifacts commit except the by-products named above. **Pass** iff all hold.
