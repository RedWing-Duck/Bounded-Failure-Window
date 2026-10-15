# Appendix D. Verification record, Tasks 1–19

For each task: the pre-registration and results files, the pre-registered checks that passed and failed, and every failure with the attribution its report gives (criterion, input, code, document or prediction). Outcomes are copied from the reports, not re-judged, and every failure stays recorded.

**Task 1.** verification/PREREG.md · verification/REPORT.md. 12 checks with a verdict; 12 pass, 0 fail.

**Task 2.** verification/PREREG.md · verification/REPORT.md. 3 checks with a verdict; 3 pass, 0 fail.

**Task 3.** verification/PREREG.md · verification/REPORT.md. 8 checks with a verdict; 8 pass, 0 fail.

**Task 4.** verification/PREREG.md · verification/REPORT.md. Exploratory by pre-registration (outcomes reported either way; no pass/fail criteria).

**Task 5.** verification/PREREG.md · verification/REPORT.md. The report itself (`verification/REPORT.md`); no pass/fail criteria.

**Task 6.** verification/PREREG_t6.md · verification/REPORT.md. 6 checks with a verdict; 5 pass, 1 fail.

- Failure — C5 (peak locations to 3 s.f. against Task 4b): criterion — Task 4b located peaks on a grid of about 0.4 % steps; heights all match, three locations differ in the third figure.

**Task 7.** verification/PREREG_t7.md · verification/REPORT.md. 15 checks with a verdict; 15 pass, 0 fail.

**Task 8.** classification/PREREG_t8.md · classification/REPORT.md. 5 checks with a verdict; 5 pass, 0 fail.

**Task 9.** classification/PREREG_t9.md · classification/t9/RESULTS_t9.md. 7 checks with a verdict; 5 pass, 2 fail.

- Failure — T9.2 ARE route: criterion — the regularised ARE converges as √ε with a large prefactor; mp ARE and the closed-form Wiener filter match the document.
- Failure — T9.5 monotonicity and ordering: criterion — float64 resolution; 0 of 285 and 0 of 13 flags are real at higher precision.

**Task 10.** classification/PREREG_t10.md · classification/t10/RESULTS_t10.md. 10 checks with a verdict; 6 pass, 4 fail.

- Failure — T10.1 symbolic (2 items): criterion / route — no √(square) handling in the pre-registered SymPy route; identities hold.
- Failure — T10.2 A1.3 as specified: plan's construction (criterion as pre-registered); the supplementary construction passes.
- Failure — T10.5 pair birth: criterion.
- Failure — T10.6 matched-variance τ (zero-limit shape check): criterion.

**Task 11.** classification/PREREG_t11.md · classification/t11/RESULTS_t11.md. 11 checks with a verdict; 10 pass, 1 fail.

- Failure — T11.3 classes: criterion — the pre-registered limits/brackets at β ≥ 2.

**Task 12.** classification/PREREG_t12.md · classification/t12/RESULTS_t12.md. 13 checks with a verdict; 10 pass, 3 fail.

- Failure — Symbolic A5 (D2 post at Δt → ∞): code — the SymPy check route (`sympy.limit`); the series route confirms.
- Failure — A7 minimum below F and two rays: criterion — the zero tolerance is too coarse for the prior dip.
- Failure — A8 qualitative regression: prediction — the prompt's quick-check numbers.

**Task 13.** classification/PREREG_t13.md · classification/t13/RESULTS_t13.md. 15 checks with a verdict; 10 pass, 5 fail.

- Failure — Part A symbolic (2 of 68 items): criterion / route — identities verified by a post-hoc rewrite route.
- Failure — A2 numerical (auxiliary cross-check, 277 sets): code — precision loss; all agree at higher precision.
- Failure — C1 numbers, first run: document (4, a truncated worked value) and code (2, parser); passes after the fixes.
- Failure — C2 classes, row 8: document — the stated class (1,0,1) cannot occur (proved; class set corrected).
- Failure — C2 classes, row 12: code — route (ii) sample point below its equality tolerance at an exact limit.
- Failure — D reproduction, Task 10: code — `run_t10.sh` omits `t10_realize_diag.py`; Task 12: criterion — masking of the provenance runtime list.
- Recorded — A3 (Theorem 7.15): the pre-registered resultant route, completed post hoc in exact arithmetic (`t13/t13_A3_proof.py`, 22 of 22 checks; the pre-registered attempt `t13_A3_attempt.py` reported 'unresolved'): the resultant of the cleared quadratic and its x-derivative is 4u²x²(u + 1)²(E − 1)⁴(E² + 2xE − 1)², and E² + 2xE − 1 = −2e^(−x)(sinh x − x) < 0 on E = e^(−x), so dp/dx never vanishes.

**Task 14.** classification/PREREG_t14.md · classification/t14/RESULTS_t14.md. 11 checks with a verdict; 8 pass, 3 fail.

- Failure — C4 paper render reproduces v1: criterion — the register types the excess identity as a Corollary (accepted in Task 15).
- Failure — C9 bibliography: input / criterion — two entries unattached and DOIs unresolvable from the session; resolved by the Task 15 input (verified bib, attachments).
- Failure — C10 reproduction: code — the dry-run resolver; all 9 flagged paths resolve as their scripts build them.

**Task 15.** classification/PREREG_t15.md · classification/RESULTS_t15.md. 13 checks with a verdict; 11 pass, 2 fail.

- Failure — C4 [n] rendering: criterion / code — the pre-registered bracket pattern flags the interval '[0, 10]' in the Appendix B description of Figure B.1; it is not a citation, and no unresolved citation remains.
- Failure — C10 thesis phrase check: criterion — all 81 A–E matches are Task 15's figure labels B.1–B.12, which coincide in form with the legacy labels the pattern targets; 0 'Paper 1', no legacy label remains.

**Task 16.** classification/PREREG_t16.md · classification/RESULTS_t16.md. 8 checks with a verdict; 5 pass, 3 fail.

- Failure — D1 new proof steps of the thesis draft (2 of 9 items): code — SymPy could not decide a sign and could not denest a square root of a square; both items hold (post-hoc diagnosis).
- Failure — D2 statements against the repository: document / criterion — four statements differ in content: 3.1 and 3.5 gather conclusions the repository states in other results (verified in D1), and the §2.5 table rows for 2.5 and 2.7 left out hypotheses (full statements were then added to the thesis).
- Failure — D6 legacy labels: criterion / document — three hits, none a legacy label: two figure labels in Appendix E outside the exemption window, and a quotation in Appendix D.

**Task 17.** classification/PREREG_t17.md · classification/RESULTS_t17.md. 7 checks with a verdict; 3 pass, 4 fail.

- Failure — E1 new proof steps of the thesis draft (2 of 9 items): code / document — the 50-digit test of the optimal prior M < F (Proposition 6.13) cannot resolve it when e^(−2λΔt) < 10⁻⁵⁰ (it holds exactly, f(F) = F²a² > 0); Corollary 7.4's proof as written omits σ⋆² → 0 and Theorem 5.1 (the corollary holds).
- Failure — E3 numbers (1 of 88): document — "37 values of β" for Theorem 7.8, in the repository's label and the draft; Task 11 ran 129.
- Failure — E4 cross-references: document — "Prop. 6.10–6.12" spans Counterexample 6.11.
- Failure — E5 prior-work sentences: document — §7.3 makes [47] an analysis of coloured measurement noise; it studies time-correlated model error (2 sentences undetermined: no abstracts reachable from the session).

**Task 18.** classification/PREREG_t18.md · classification/RESULTS_t18.md. 7 checks with a verdict; 3 pass, 4 fail.

- Failure — F1 Task 17 fixes (2 of 6): code / document — the [47] search included Appendix D's quotation of the old finding (both chapter sentences now say model error); §1.6 still cites [21–23] for monotonicity under garbling (fixed in §7.1 only).
- Failure — F2 chapter 8 counts: code — the recount parser skipped Task 2's 'PASS (info)' row (143); read as pre-registered the total is 144, with 28 failed and Tasks 4 and 5 without criteria.
- Failure — F3 chapter 8 claims: document — §8.5 names a referee pass on Theorem 7.6 only; Task 13 C4's independent referee read the whole consolidated document (14 points, all fixed).
- Failure — F6 appendices: code / document — Appendix A differs only in math delimiters; the draft's Appendix D rewords three Task 17 failure lines (tense, P⁻ for M, 'the proof was completed').

**Task 19.** classification/PREREG_t19.md · classification/RESULTS_t19.md. 31 checks with a verdict; 26 pass, 5 fail.

- Failure — G1 citations: input — Roberts (1959) unreachable from the session; that it states r/(2 − r) cannot be determined from its text (secondary sources agree); the §6.3 identity, [29], [40] and both [21] sentences hold.
- Failure — G3 chapter 8: code / document — the coverage parser missed two Appendix D lines (both covered); §8.2 interchanges the route descriptions; §8.4 lists Task 13 under √(x²) handling, which Task 13's report does not support. Recount 151 / 32 and §8.5 match.
- Failure — G4 chapter 9: document — §9.2's c/(FΠ₀) > 4 for the Hill gain holds for n = 2 only.
- Failure — G7 sync: criterion / code — the old key remains in ten recorded files of Tasks 14, 15 and 17 (not editable) and in Task 19's register script's docstring; 0 in live files; the other three clauses hold.
- Failure — H-13.C2-12 C2 row 12 re-check: criterion — 45 persisting cases; the 10⁻³⁰⁰ tolerance is finer than the stored limit's precision (about 10⁻²⁵), so the routes compare below what the critical value carries.
