# Bounded-Failure-Window

Verification code and results for the bounded-window results in "Shape Classification of Failure-Sets in Stationary Linear Filters" (John Holder, independent researcher, 2026).

Paper (open access): https://doi.org/10.5281/zenodo.23439075

## What this is

When a precision-weighted relay is miscalibrated, the error variance can rise above both its low-precision and high-precision limits, forming a bounded window of bad performance in between. This repo holds the pre-registered numerical verification of that phenomenon: the frozen pass/fail criteria, the simulation and symbolic-check code, the raw results, and the figures.

The criteria in `PREREG.md` were written and committed before any simulation ran. Where a criterion turned out badly posed, that is reported in `REPORT.md`; the criterion itself was not changed.

## Layout

- `verification/PREREG.md`, `PREREG_t6.md`, `PREREG_t7.md` — the frozen criteria for each round of checks
- `verification/t1_symbolic.py`, `t2_em.py`, `t3_paired.py`, `t4a_discrete.py`, `t4b_colored.py`, `t4c_drift.py`, `t4d_gains.py`, `t4e_fixed_gain.py`, `t6_colored_symbolic.py`, `t7_*.py` — the check scripts (symbolic identities, Euler-Maruyama simulations with common random numbers and batch-means standard errors, robustness checks that break one assumption at a time)
- `verification/common.py`, `make_report.py`, `t6_report.py`, `t7_report.py` — shared code and report generation
- `verification/run_all.sh` — runs every check from scratch and regenerates the report
- `verification/results/` — raw outputs: per-task JSON, logs, runtime table, environment record
- `verification/figures/` — figures produced by the checks
- `verification/REPORT.md` — the full verification report, generated from the results

## Reproducing

Requires Python 3 with numpy, scipy, sympy, and matplotlib:

    bash verification/run_all.sh

This deletes `results/` and `figures/`, re-runs every check, and regenerates `REPORT.md`.

## Results

All pre-registered tasks passed. Task 1: symbolic identities verified with SymPy. Task 2: simulation matches the closed form at all 43 precision points. Task 3: peak location and window crossings confirmed. Task 4: the window prediction holds when breaking one assumption at a time (discrete-time filter, coloured sensory noise, drifting signal, gain families). Tasks 6 and 7: coloured-noise symbolic check and revision checks. Full tables in `REPORT.md`.
