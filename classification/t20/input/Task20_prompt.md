I'm finishing a thesis, "Failure-Set Topology in Stationary Linear Filters". It is built from this repository: RedWing-Duck/Bounded-Failure-Window, branch claude/task-8-classification-suite-0b1ey4, head 7855e45 (the Task 19 results commit). The thesis text has moved ahead of the repository. Your job is to bring the repository in line, as one new verification task, Task 20, following the repository's own protocol:
- pre-register first;
- make one recorded run;
- failures stay failures, with a diagnosis.

Ground rules
- Create a new branch from 7855e45, task-20-thesis-sync. Commit there. Do not push, merge, or rewrite history.
- Commit classification/PREREG_t20.md first: the changes below and the checks with their pass criteria, before you change anything else. Then make the changes, run the checks once, and commit classification/RESULTS_t20.md with every verdict, including failures.
- Do not change any recorded file of Tasks 1–19 (their results/, input/ and RESULTS files). Change only live sources, the register, generators and rendered outputs.
- If a requested change doesn't fit how the repository works, stop and report the options. Don't improvise. Example: the register may have no way to number a result "7.6a".
- Paths: the register is classification/register/; the render chain is listed in classification/Appendix_E_Reproduction.md.

Changes

1. Register titles (classification/register/results.yaml).
   - 2.1 topological-realizability: "Topological realisability"
   - 2.8 reparameterisation: "Reparameterisation (orientation swaps ℓ and h)"
   - 5.1 realizability: "Gain realisability"
   - 6.17 d3-excess: "D3 excess set; onset ρ > 2 + ν" (ν = 2ΣΠ/λ², the register's former u)
   - 6.19 dt-optimal-mp: "Optimal M-P along Δt: posterior ↓; prior ↑; averaged ↑"
   - Swap the thesis numbers of 8.1 and 8.2, so that 8.1 = narrow-windows ("Narrow windows need root-finding") and 8.2 = blind-searches ("Blind searches find no unpredicted class"). Keys stay the same. Find out how thesis numbers are assigned (order in results.yaml, order in the source, or an explicit field) and change only what is needed. Report the mechanism.
   - Change keys only if the title change requires it. If a key changes, report every file that cites it.

2. Lemma 7.6a.
   The thesis states Lemma 7.6a (thesis §7.2): the lemma that supplies the whole-path step (iv) ⇒ (ii) in the proof of Theorem 7.6 (key gaussian-orderings-coincide). It covers both causal and whole-path garblings. Add a register entry if the register can hold it:
   - type Lemma
   - number 7.6a, placed between 7.6 and 7.7
   - a new key, e.g. whole-path-garbling
   - verified_by empty
   - a status that shows it has not been independently checked
   If the numbering scheme can't express "7.6a" without renumbering 7.7–7.16, stop and report the options. Don't renumber.

3. References [54]–[60] (classification/register/references.yaml and classification/references.bib).
   Keep frozen numbering ("a new reference takes the next free number"). Add these seven, numbered as given, with first_cited "draft §1.6 Contributions and relation to prior work" and status cited:
   [54] sinopoli2004 — Sinopoli, B., Schenato, L., Franceschetti, M., Poolla, K., Jordan, M. I. & Sastry, S. S. (2004). Kalman filtering with intermittent observations. IEEE Transactions on Automatic Control 49(9), 1453–1464. doi:10.1109/TAC.2004.834121
   [55] wu2018 — Wu, J., Shi, G., Anderson, B. D. O. & Johansson, K. H. (2018). Kalman filtering over Gilbert–Elliott channels: stability conditions and critical curve. IEEE Transactions on Automatic Control 63(4), 1003–1017. doi:10.1109/TAC.2017.2732821
   [56] jiang2026 — Jiang, S., Shi, J. & Moura, S. (2026). Mitigating overconfidence in nonlinear Kalman filters via covariance recalibration. Automatica, accepted for publication; volume, pages and DOI not yet assigned. arXiv:2407.05717
   [57] bosov2026 — Bosov, A., Bosov, S. & Uryupin, I. (2026). Beyond divergence: failure modes of the classical extended Kalman filter in a unified nonlinear tracking model. Mathematics 14(17), 3071. doi:10.3390/math14173071
   [58] gotovos2013 — Gotovos, A., Casati, N., Hitz, G. & Krause, A. (2013). Active learning for level set estimation. Proceedings of the 23rd International Joint Conference on Artificial Intelligence (IJCAI 2013), 1344–1350. AAAI Press. https://dl.acm.org/doi/10.5555/2540128.2540322 (no DOI)
   [59] tenne2002 — Tenne, D. & Singh, T. (2002). Characterizing performance of α-β-γ filters. IEEE Transactions on Aerospace and Electronic Systems 38(3), 1072–1087. doi:10.1109/TAES.2002.1039425
   [60] sahomasugi2016 — Saho, K. & Masugi, M. (2016). α–β–γ tracking filters using acceleration measurements. SpringerPlus 5, 309. doi:10.1186/s40064-016-1960-8
   Notes:
   - Reuse the old sahomasugi2016 BibTeX from git history (41d5e43:classification/references.bib) if it matches.
   - Attach [60] to result 6.13 (discrete-excess) alongside roberts1959, since the thesis cites it there for the factor α/(2 − α).
   - The other six are cited only in chapter 1. Task 14's C9 failed on references attached to no result, so check how the register and render handle unattached references, and report what you did.
   - Task 19's t19_register.py swaps sahomasugi2016 for roberts1959 at number 26. Make sure re-adding the key as 60 doesn't collide with that swap.

4. Appendix D "Recorded" line (classification/t15/make_appendix_de.py).
   Add a mechanism for non-failure lines (e.g. NOTES = {"T13": [...]}), emitted after a task's failure bullets as "- Recorded — …". Add exactly this line for Task 13:
   "A3 (Theorem 7.15): the pre-registered resultant route, completed post hoc in exact arithmetic (`t13/t13_A3_proof.py`, 22 of 22 checks; the pre-registered attempt `t13_A3_attempt.py` reported 'unresolved'): the resultant of the cleared quadratic and its x-derivative is 4u²x²(u + 1)²(E − 1)⁴(E² + 2xE − 1)², and E² + 2xE − 1 = −2e^(−x)(sinh x − x) < 0 on E = e^(−x), so dp/dx never vanishes."
   Counts and failure lines must not change.

5. Figures B.5 and B.6.
   The thesis has B.5 = peak-heights and B.6 = hill-phase.
   - In t15/t15_register.py, make B.5 = ("B.5", "peak-heights", "fig04_peak_heights", …) and B.6 = ("B.6", "hill-phase", "fig03_hill_phase", …), in that order, and swap the two description keys.
   - Swap the two sections in source/figs/README.md and the two figure tokens in source/Roadmap_v3_Source.md.
   - Run the chain, then delete the stale figs_thesis/B.5_hill-phase.* and figs_thesis/B.6_peak-heights.* files.

Checks to pre-register (each needs a pass criterion)
- C1 Register: the rendered Appendix A shows the new titles, 8.1 = narrow-windows, 8.2 = blind-searches, and Lemma 7.6a, or the documented reason it couldn't be added. No other row changes.
- C2 References: Appendix C renders [1]–[53] unchanged, byte for byte against the committed file, plus [54]–[60] as above. bibfmt formats all seven without error. Every DOI string matches the list above.
- C3 Appendix D: the regenerated file differs from the committed one only by the Task 13 Recorded line. Totals stay 182 / 37 / 38.
- C4 Figures: Appendix B, figs_thesis/README.md and the Roadmap list B.5 = peak-heights and B.6 = hill-phase. No stale B.5/B.6 files remain. The PNGs are byte-identical to their pre-swap counterparts under the new names.
- C5 Chain: every step of the render chain runs with exit 0, and the T15–T19 check scripts still run with exit 0. Record the expected verdict changes (for example T18 F6, T19 G6/G7(iv) on the Appendix A titles, and G6 on the Appendix D line) as expected differences with their causes.
- C6 Sync with the thesis: confirm the repository now agrees with these thesis statements:
  - §7.5 "…passing 22 of 22 checks (Appendix D, Task 13)"
  - §8.1 "182 checks with a verdict … 37 of them failed"
  - the reference entries [54]–[60] as written above

Report
Give me one Markdown report containing:
- the branch and the commit hashes (pre-registration and results)
- a before/after table of every title, number and reference change
- the new Appendix D Task 13 entry, verbatim
- the C1–C6 verdicts, with diagnoses for any failure
- anything you couldn't do, with the options for it
- a final list headed "Thesis text to update", naming anything in the repository that now disagrees with the thesis wording quoted above
