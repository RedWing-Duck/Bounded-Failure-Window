# F3: chapter 8's claims against the repository record (manual, after the recorded run on f77ab8f)

## §8.2: "the one persistent disagreement, row 12 of the Task 13 audit (§4.1), the fault was in route (ii)"

Every results JSON was searched for persisting route disagreements (keys `persisting`, `n_persist`, `persistent` > 0). One entry:
`t13/results/t13_audit_classes.json`, row 12 ("Pi0 monotone"), 122 persisting. Other route comparisons record 0 persisting
(T10.7: 3 flagged, 0 persisting; T12 Part C: 1,109 flagged, 0 persisting; T13 audit: every other row 0; T15 C11: 0 route
disagreements). Task 13's diagnosis attributes row 12 to code: route (ii)'s sample point falls below its equality tolerance at an
exact limit (Appendix D, Task 13). **Matches.**

## §8.5: "Apart from the independent referee pass on Theorem 7.6 (Task 13), no result has yet had external review."

The record (`t13/RESULTS_t13.md` check C4, `t13/referee_report.md`, the source's change log rows "T13 C4 (referee 1–12)"):
- Task 13 C4 was an **independent referee pass on the whole consolidated document** of the time (`Stages_0_4_Consolidated.md` at
  5ac589c), by "a separate agent that had not seen the derivation history". RESULTS_t13: "C4 independent referee | record | 14 points,
  all valid, all fixed". The points concern many results (in today's numbering, among them Theorem 3.4, Propositions 6.16–6.18,
  Theorem 7.15, Proposition 6.17, Corollary 7.3, Corollary 5.4, Corollary 2.5, Theorem 2.2, Proposition 4.2 and Proposition 7.16).
- Theorem 7.6 (then Conjecture 4.11, Task 13 A8) is one result the referee read: "referee found no gap".
- No other referee or external review is recorded (other mentions are plans: `Stage_3_Plan.md`, the v2.1 roadmap).

**Does not match.** The only referee pass recorded covers the whole Stages 0–4 document, not only Theorem 7.6. It was also within
the project (a separate agent), so "external review" is accurate only in the sense that no review outside the project exists.
Suggested wording: "Apart from one independent referee pass over the whole consolidated document (Task 13, C4: 14 points, all
fixed), no result has had external review."
