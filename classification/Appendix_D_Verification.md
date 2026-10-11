# Appendix D. Verification record, Tasks 1–14

One section per task: the pre-registration and results files, the number of pre-registered checks that passed and failed (read from each report's check table), and every failure with the attribution its report gives. Outcomes are copied from the reports, not re-judged. Every failure stays recorded as a failure.

## T1

- Pre-registration: `verification/PREREG.md`
- Results: `verification/REPORT.md`
- Checks: 12 with a verdict; 12 pass, 0 fail.
- Failures: none.

## T2

- Pre-registration: `verification/PREREG.md`
- Results: `verification/REPORT.md`
- Checks: 3 with a verdict; 3 pass, 0 fail.
- Failures: none.

## T3

- Pre-registration: `verification/PREREG.md`
- Results: `verification/REPORT.md`
- Checks: 8 with a verdict; 8 pass, 0 fail.
- Failures: none.

## T4

- Pre-registration: `verification/PREREG.md`
- Results: `verification/REPORT.md`
- Checks: Exploratory by pre-registration (outcomes reported either way; no pass/fail criteria).

## T5

- Pre-registration: `verification/PREREG.md`
- Results: `verification/REPORT.md`
- Checks: The report itself (`verification/REPORT.md`); no pass/fail criteria.

## T6

- Pre-registration: `verification/PREREG_t6.md`
- Results: `verification/REPORT.md`
- Checks: 6 with a verdict; 5 pass, 1 fail.
- Failure: C5 (peak locations to 3 s.f. against Task 4b): criterion — Task 4b located peaks on a grid of about 0.4 % steps; heights all match, three locations differ in the third figure.

## T7

- Pre-registration: `verification/PREREG_t7.md`
- Results: `verification/REPORT.md`
- Checks: 15 with a verdict; 15 pass, 0 fail.
- Failures: none.

## T8

- Pre-registration: `classification/PREREG_t8.md`
- Results: `classification/REPORT.md`
- Checks: 5 with a verdict; 5 pass, 0 fail.
- Failures: none.

## T9

- Pre-registration: `classification/PREREG_t9.md`
- Results: `classification/t9/RESULTS_t9.md`
- Checks: 7 with a verdict; 5 pass, 2 fail.
- Failure: T9.2 ARE route: criterion — the regularised ARE converges as √ε with a large prefactor; mp ARE and the closed-form Wiener filter match the document.
- Failure: T9.5 monotonicity and ordering: criterion — float64 resolution; 0 of 285 and 0 of 13 flags are real at higher precision.

## T10

- Pre-registration: `classification/PREREG_t10.md`
- Results: `classification/t10/RESULTS_t10.md`
- Checks: 10 with a verdict; 6 pass, 4 fail.
- Failure: T10.1 symbolic (2 items): criterion / route — no √(square) handling in the pre-registered SymPy route; identities hold.
- Failure: T10.2 A1.3 as specified: plan's construction (criterion as pre-registered); the supplementary construction passes.
- Failure: T10.5 pair birth: criterion.
- Failure: T10.6 matched-variance τ (zero-limit shape check): criterion.

## T11

- Pre-registration: `classification/PREREG_t11.md`
- Results: `classification/t11/RESULTS_t11.md`
- Checks: 11 with a verdict; 10 pass, 1 fail.
- Failure: T11.3 classes: criterion — the pre-registered limits/brackets at β ≥ 2.

## T12

- Pre-registration: `classification/PREREG_t12.md`
- Results: `classification/t12/RESULTS_t12.md`
- Checks: 13 with a verdict; 10 pass, 3 fail.
- Failure: Symbolic A5 (D2 post at Δt → ∞): code — the SymPy check route (`sympy.limit`); the series route confirms.
- Failure: A7 minimum below F and two rays: criterion — the zero tolerance is too coarse for the prior dip.
- Failure: A8 qualitative regression: prediction — the prompt's quick-check numbers.

## T13

- Pre-registration: `classification/PREREG_t13.md`
- Results: `classification/t13/RESULTS_t13.md`
- Checks: 15 with a verdict; 10 pass, 5 fail.
- Failure: Part A symbolic (2 of 68 items): criterion / route — identities verified by a post-hoc rewrite route.
- Failure: A2 numerical (auxiliary cross-check, 277 sets): code — precision loss; all agree at higher precision.
- Failure: C1 numbers, first run: document (4, a truncated worked value) and code (2, parser); passes after the fixes.
- Failure: C2 classes, row 8: document — the stated class (1,0,1) cannot occur (proved; class set corrected).
- Failure: C2 classes, row 12: code — route (ii) sample point below its equality tolerance at an exact limit.
- Failure: D reproduction, Task 10: code — `run_t10.sh` omits `t10_realize_diag.py`; Task 12: criterion — masking of the provenance runtime list.

## T14

- Pre-registration: `classification/PREREG_t14.md`
- Results: `classification/t14/RESULTS_t14.md`
- Checks: 11 with a verdict; 8 pass, 3 fail.
- Failure: C4 paper render reproduces v1: criterion — the register types the excess identity as a Corollary (accepted in Task 15).
- Failure: C9 bibliography: input / criterion — two entries unattached and DOIs unresolvable from the session; resolved by the Task 15 input (verified bib, attachments).
- Failure: C10 reproduction: code — the dry-run resolver; all 9 flagged paths resolve as their scripts build them.
