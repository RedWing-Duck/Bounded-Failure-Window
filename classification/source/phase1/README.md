# The starting study (Tasks 1–7): reference record

**What it was.** The starting study analysed a precision-weighted relay: a constant-gain correction of a scalar
Ornstein–Uhlenbeck signal toward a noisy observation, with a Bayesian-weight gain $G = c\Pi/(\Pi + \Pi_0)$. It derived the
relay's actual stationary error variance in closed form, showed that a miscalibrated relay can be worse than no correction
inside a bounded window of sensory precisions (the window theorem), and located the peak. It extended the analysis to
coloured sensory noise and to discrete time, and checked the results with simulations: Euler–Maruyama runs, paired
comparisons of miscalibrated, calibrated and optimal relays, and breaking one assumption at a time.

**It is part of the thesis.** Its results carry thesis numbers like any other result and are listed in Appendix A
(`classification/Appendix_A_Register.md`). Thesis-facing documents cite these results by number and the verification as
Tasks 1–7. They do not cite the manuscript as a separate publication.

**Thesis results it established** (in whole, or in part where marked):
- [[stationary-variance]]: stationary variance; equivalence with the constant-gain filter.
- [[excess-identity]]: the excess identity.
- [[window-theorem]]: the window theorem.
- [[optimal-envelope]]: the optimal gain and envelope.
- [[bayesian-weight]]: the Bayesian-weight gain along precision (onset κ > 2; four regimes).
- [[capped-gain]], [[precision-blind]] and [[hill-turning-points]]: in part (its non-Kalman gain checks).
- [[tau-relay-variance]]: relay variance with coloured noise.
- [[discrete-excess]]: the discrete excess condition.

**Where its verification lives.**

| Task | Pre-registration | Results commit | Report |
|---|---|---|---|
| T1–T5 | `verification/PREREG.md` (`d21f193`) | `70ebb55` | `verification/REPORT.md` |
| T6 | `verification/PREREG_t6.md` (`824ca06`) | `0944b81` | `verification/REPORT.md`, Task 6 section |
| T7 | `verification/PREREG_t7.md` (`a0d2be2`) | `2f9da71` | `verification/REPORT.md`, Task 7 section |

Scripts: `verification/t1_*.py` … `verification/t7_*.py`, run by `verification/run_all.sh`. The same records are in
`classification/register/tasks.yaml`.

**Status of this folder.** This is a reference record of that work, not a cited publication.
- `Holder_2026_Bounded_Failure_Window_Final.pdf`: the manuscript, unchanged. It is the PDF only (no LaTeX source was supplied)
  and was added in Task 14 from the copy the author uploaded; it was not in the repository before.
- `ERRATA.md`: corrections to its text. Each correction names the thesis result that states the correct version.
