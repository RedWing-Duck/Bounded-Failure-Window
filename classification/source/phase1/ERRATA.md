# Errata to the starting-study manuscript

Manuscript: `Holder_2026_Bounded_Failure_Window_Final.pdf` in this folder (17 pages). Each quote below was checked against the
text extracted from it (`pdftotext`) in Task 14; page numbers refer to that PDF. Each entry names the thesis result that states the
correct version.

**E1 (§3.4, "Windows need loose tolerances", last sentence; p. 5).**
- *Old:* "Any tolerance below F produces at most a threshold, whatever the gain."
- *Correct:* [[forced-lower-ray]]. For any gain and $R^2 < F$, the failure set contains $(0, \pi_R)$ with
  $\pi_R = 2\lambda(F - R^2)/R^4$. For the Bayesian-weight gain this is a single threshold; other gains can add bounded
  components ([[hill-classification]]).

**E2 (§3.4, after the theorem; p. 5).**
- *Old:* "…and no tested gain produced more than one interval."
- *Correct:* below the floor the Hill gain gives a threshold plus a separate bounded interval ([[hill-classification]]).

**E3 (§3.8, "A gain with no initial over-weighting"; p. 8).**
- *Missing:* $\sigma^2$ first dips below $F$ to a minimum $m$, so tolerances between $m$ and $\min(M, F)$ give a threshold plus a
  bounded interval.
- *Correct:* [[hill-turning-points]] and [[hill-classification]]. The value $m = 0.0099852$ ($n = 2$, $\Pi_0 = 5$,
  $\lambda = c = 1$, $\Sigma = 0.01$) comes from the Task 14 prompt; it does not appear in the manuscript. Task 14 check C7 tests
  it (`classification/t14/RESULTS_t14.md`).

**E4 (§5.2, "Every failure set was a single interval"; p. 12).**
- *Correct:* this is true at the tolerances examined, all at or above $F$. Below $F$ the Hill gain can give two components
  ([[hill-classification]]).
- *Tolerances examined*, read from the Task 4 scripts (`verification/t4a_discrete.py` … `t4d_gains.py`) and
  `verification/PREREG.md`:
  - The interval counts are for the excess set $\{\sigma^2 > F\}$ ($R^2 = F = 0.01$) and the window $\{\sigma^2 > 0.05\}$
    ($R^2 = 0.05$), in Tasks 4a–4d.
  - Task 4c also tracks where the $R^2 = 0.008$ threshold moves, but counts no intervals there.
  - No interval count was made at a tolerance below $F$. In Task 4d the Hill $n = 2$ gain showed at most one interval of each
    set.
