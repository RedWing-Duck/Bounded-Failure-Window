# Bounded-Failure-Window

Verification record and source for the thesis

> Holder, J. (2026). *Shape Classification of Failure-Sets in Stationary Linear Filters: Critical values, gain families and
> information ordering.* Zenodo. https://doi.org/10.5281/zenodo.23439075

The published PDF is in [`thesis/Holder_2026_Shape_Classification_of_Failure-Sets.pdf`](thesis/Holder_2026_Shape_Classification_of_Failure-Sets.pdf)
(sha256 `3484684841e0bc089f4396b47c98cd5f46826cffbe0a3f17a0576c42e58cfcec`). The DOI version is the version of record.

The thesis classifies the shapes of failure sets (threshold, bounded window, two rays, mixtures) for scalar stationary
linear filters of an Ornstein–Uhlenbeck signal, as one parameter varies. Every numbered result in it has a permanent key in
this repository, and every check behind it is recorded here, failures included.

## Snapshot

The tag **`v1.0-thesis`** marks the state that corresponds to the published thesis:

- the register, sources, appendices and figures match the published text through **Task 21**. The published figures carry
  Task 21's labels: B.8 to B.10 use "posterior", "averaged" and ν;
- the thesis's Appendix E lists the reproduction commands through Task 20. Task 21 changed only figure text, via
  `t15/make_figs_thesis.py`, and adds no new command;
- later commits, if any, are not part of the published record.

## How results were established

Each verification task was **pre-registered** before it ran: `PREREG_*.md`, committed before any result, stating changes,
checks and numeric pass criteria. Each task then made **one recorded run**, and its results file lists every verdict.

- A failed check **stays a failure**, with a diagnosis attributed to the criterion, the input, the code, the document or a
  prediction.
- No criterion is changed after a run.
- Every recorded output is committed, with the commit hashes it ran on.

Across Tasks 1–19: **182 checks with a verdict, 37 failed**. Of the **24 re-checks** under corrected criteria in Task 19,
**23 passed**. The full record is in [`classification/Appendix_D_Verification.md`](classification/Appendix_D_Verification.md).
Tasks 20 and 21 synchronised the repository with the thesis text: [`classification/RESULTS_t20.md`](classification/RESULTS_t20.md)
and [`classification/RESULTS_t21.md`](classification/RESULTS_t21.md).

**Open (not proved):**
- Numerical results 5.15 (two-stage gains), 6.21 (sampled-relay census), 8.1 and 8.2.
- Conjecture 6.22.
- Lemma 7.6a, which is recorded with status `to-verify` because no task has examined it.

## Layout

| Path | Contents |
|---|---|
| `thesis/` | The published PDF, and `Thesis_Draft_full.md` (the last draft archived by Task 19) |
| `verification/` | Tasks 1–7 (the starting study): `PREREG*.md`, scripts `t1_…`–`t7_…`, `results/`, `REPORT.md` |
| `classification/` | Tasks 8–21: `PREREG_tN.md`, `tN/` (scripts, `results/`, `input/`), `RESULTS_tN.md` (or `tN/RESULTS_tN.md`) |
| `classification/register/` | Register of results (`results.yaml`: thesis number, key, type, title, verifying checks, status), references, figures, crosswalk, renderer |
| `classification/source/` | Key-token sources from which the renders are built |
| `classification/Appendix_A_…E_….md` | Appendices A–E as rendered for the thesis |
| `classification/figs_thesis/` | Figures B.1–B.12 as used in the thesis |
| `reference/phase1/` | The starting-study manuscript and its errata |

**Numbering.** Thesis numbers (for example Theorem 5.12) come only from `thesis_no` in `classification/register/results.yaml`.
Each result also has a permanent key, such as `hill-turning-points`. Appendix A lists both, and `register/crosswalk.md` maps
them to earlier labels.

**Earlier file names.** Before the thesis took its final form, the material was organised as "Stages 0–4" and as two papers.
File names such as `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md`, `figs_paper2/` and `Roadmap_v3.md` keep those names.
`Stages_0_4_Thesis.md` is the thesis-numbered render.

## Reproduction

See [`classification/Appendix_E_Reproduction.md`](classification/Appendix_E_Reproduction.md) (thesis Appendix E).

- **Environment of the recorded runs:** Python 3.13.16; numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0,
  matplotlib 3.11.2, PyYAML 6.0.1. There is no lockfile; each task records its environment in its `results/env.json`.
- **Commands:** `cd verification && bash run_all.sh` runs Tasks 1–7. `bash classification/reproduce_all.sh WORKDIR 8 9 10 11 12 13`
  runs Tasks 8–13 in a clean checkout. The Task 14–20 render chain, run from `classification/`, rebuilds the register,
  renders and appendices.
- **Long runs:** several runs take hours (Task 10 about 4 h, Task 12 about 2.7 h, Task 13 C2 about 4 h on 4 CPUs).

## Use of AI systems

The thesis's Declaration describes how AI systems were used. Simulations and checks in this repository were run with Claude
Code. Commits authored by that agent carry the name "Claude" and a session trailer.

## Licence

- **Code** (`*.py`, `*.sh`): MIT, see [`LICENSE`](LICENSE).
- **Text, data and figures:** CC BY 4.0, see [`LICENSE-docs`](LICENSE-docs).
- **Citation:** use [`CITATION.cff`](CITATION.cff), which cites the thesis DOI.
