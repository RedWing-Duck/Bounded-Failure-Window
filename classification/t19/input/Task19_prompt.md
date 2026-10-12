# Task 19: Close the open items

You are working in the repository that holds:
- `classification/` (Tasks 8–18, including `OPEN_ITEMS.md`);
- `verification/` (Tasks 1–7);
- `reference/phase1/`;
- `thesis/`.

This task works through `classification/OPEN_ITEMS.md`. It closes every item that a check or a repository change can close. Items that only new mathematics or an outside reader can close are left open, and stated plainly as open.

Use the usual protocol:
- Write `classification/PREREG_t19.md`, containing every check in §6 and every Part C re-check with its pass criterion. Commit it **before** running anything that produces a result.
- Run the checks once, on one recorded commit.
- Report in `classification/RESULTS_t19.md`. A failed check stays a failure, with a diagnosis (criterion, input, code, document or prediction). Never change a criterion or an artifact after the recorded run.

**Do not change any mathematical content.** If you find a mathematical error anywhere, record it and do not fix it.

Keep the Task 16–18 precautions:
- every symbolic check gets a denesting step for √(x²) and an explicit sign argument;
- every identity SymPy cannot reduce gets a pre-registered numerical fallback (≥ 1,000 random sets, a stated seed);
- every high-precision test sets its working precision from the quantities involved.

## Attached

| File | What it is |
|---|---|
| `Thesis_Draft_full.md` | Export of the complete thesis, chapters 1–9 and Appendices A–E. Read it; do not edit it. Since the Task 18 archive (sha256 f1b8ecd3…) it changes the items below. |

The changes since Task 18:
- §1.6: [21] is now cited for observation channels as design variables, and [22, 23] for the comparison of information structures.
- §6.3: a one-line derivation of α/(2 − α), and [26] is now Roberts (1959).
- §7.4: the delayed-estimate sentence now cites "the standard prediction step of the Kalman filter [29, 40]".
- Theorem 2.2's proof gains the Task 13 referee's closing sentences.
- Chapter 8:
  - its counts cover Tasks 1–18 (151 checks, 32 failed);
  - §8.4's table is re-sorted;
  - §8.5's referee sentence is rewritten.
- Chapter 9: the Hill-gain exception, "Propositions 5.8 and 5.9", and the evidence line in open problem 2.
- Chapters 8–9: a writing pass that removes the "rough draft" markers.
- Appendix C: the entry for [26].
- Appendix D: the Task 17 lines restored to the record's wording, and Task 18 added.

---

## Part A: Repository sync

1. **Bibliography.**
   - In `references.bib` and `register/references.yaml`, replace the key `sahomasugi2016` with `roberts1959`, keeping number 26. The entry is: Roberts, S. W. (1959), *Control chart tests based on geometric moving averages*, Technometrics 1(3), 239–250, doi:10.1080/00401706.1959.10489860.
   - Attach it to 6.13 in place of the old key.
2. **Theorem 2.2.** Replace `source/thesis_only/critical-tolerance.md` with the draft's statement and proof of Theorem 2.2, which now includes the closing sentences. Re-render the thesis.
3. **Open problems.** Add the draft's open problems 5 and 6 from §9.4 to `source/Stages_0_4_Source.md` §11 as items 5 and 6, worded as in the draft. This adds to a list of open questions; it is not a change of mathematical content. Record it as a documentation fix.
4. **Appendix A normaliser.** Make the comparison normaliser strip math delimiters (`$…$`). This addresses the T18 F6 code diagnosis.
5. **Appendices.** Re-render Appendices A, C, D and E:
   - Appendix C needs a current introduction, replacing the stale Task 15 wording.
   - Appendix D must cover Tasks 1–19. Its Task 18 entry should be the draft's.
   - Appendix E needs a Task 19 row and chain step.
6. **Archive.** Commit the attached draft as `thesis/Thesis_Draft_full.md`, replacing the Task 18 copy. The Task 18 copy stays in git history; record both sha256 values in `RESULTS_t19.md`.

## Part B: Verify the text changed since Task 18

**B1. Citations.** Judge each against the source's full text where you can reach it, otherwise its title, abstract and table of contents. Say which you used.
- **[26] Roberts 1959.** Does it give the variance of a geometric moving average as a factor r/(2 − r) (asymptotically) of the observation variance? Separately, check the draft's §6.3 identity α²v/(1 − (1 − α)²) = αv/(2 − α), symbolically, for 0 < α < 2.
- **[29, 40] in §7.4.** Does each source give the Kalman prediction step, P_(k+1|k) = A P_(k|k) Aᵀ + Q or its continuous-time form, so that the sentence as written is supported? Anderson & Moore (1979) is [40].
- **[21] in §1.6 and §7.1.** Is each sentence consistent with Yüksel & Linder (2012), *Optimization and convergence of observation channels in stochastic control*?

**B2. Theorem 2.2.**
- Are the draft's new closing sentences equivalent to the closing sentences the Task 13 referee added to the repository's proof (point 10)? Use Task 16's kinds (a)–(d).
- Do they hold on ≥ 10,000 random piecewise-monotone sequences with tolerances set equal to interior turning-point values, with classification by the rule as stated against direct computation?

**B3. Chapter 8.**
- Every example in §8.4's table is a real failure with the right task label.
- Every Task 1–18 failure in Appendix D falls under at least one attribution row.
- §8.2's claim of one persistent route disagreement (T13 C2 row 12, route (ii)) matches the record.
- §8.5's referee sentence matches `t13/referee_report.md`: one pass, the whole consolidated document, 14 points, all fixed.
- The 151 checks and 32 failures for Tasks 1–18 match a recount under the rule stated in the text (Task 2's informational pass counted, as its pre-registration does).

**B4. Chapter 9.** Re-run Task 18's A3 claim table against the current wording. In particular check these:
- §9.1 attributes the spectral test to Theorem 7.6, and "sharp within the power-normalised family" to Theorem 7.8.
- The Hill-gain exception: sup q > 2 ⇔ c/(FΠ₀) > 4, and a window component possible below it (Proposition 5.13).
- "Propositions 5.8 and 5.9" for 9.3F and 17.6F.
- "The grid of Numerical result 8.2 missed every window of width 10⁻⁸".
- Open problem 2: "at most 3 … Bayesian … at most 4 … Hill … in 2,000 random sets per family".
- Open problem 4: "is expected to split into scalar copies". Is it stated as expectation, not as a result?

Report every claim with its source and verdict.

**B5. Mechanical, whole draft** (as T18 F5):
- every [n] resolves, and [1]–[53] first appear in order;
- every typed result reference has the right type;
- every Figure B.n exists;
- every "Task n" or "Tn.m" reference exists.

**B6. Appendices.** The draft's Appendices A, C and D match the Part A.5 renders, apart from formatting and the Task 19 entry, which the draft does not yet have. List every difference.

## Part C: Re-check every failure that was diagnosed but not re-checked

Section 6 of `OPEN_ITEMS.md` lists the failures marked **diagnosed** or **open**. For each one, pre-register a corrected check, and run it with the rest. Rules:
- The corrected criterion follows the diagnosis in that task's own report. Quote the original criterion, the diagnosis and the corrected criterion side by side in `PREREG_t19.md`.
- The corrected check must test the claim **as the thesis states it**, at the precision the thesis prints. It may not be weaker than the thesis's claim. If the diagnosis implies the thesis claim itself should be weakened, record that as a document finding instead of a passing check.
- Use the original task's artifacts and inputs unchanged. New code is allowed only as a new checking route, and must be committed with the pre-registration.
- Each re-check gets its own ID: H-6.C5, H-9.2, H-9.5, and so on.

The list, with hints from the reports. Use the reports as the authority.

| ID | Original failure | Hint for the corrected check |
|---|---|---|
| H-6.C5 | T6 C5: peak locations to 3 s.f. from a 0.4% grid | locate each peak by root-finding on dσ²/dθ, then compare to the printed figures |
| H-9.2 | T9.2: ARE route | the route named in the T9 diagnosis |
| H-9.5 | T9.5: monotonicity flags in double precision | extended precision at the flagged points |
| H-10.1a, H-10.1b | T10.1: two symbolic items | with √(x²) denesting and a sign argument, plus the numerical fallback |
| H-10.5 | T10.5: pair birth | the criterion named in the T10 diagnosis |
| H-10.6 | T10.6: zero-limit shape | the criterion named in the T10 diagnosis |
| H-11.3 | T11.3: classes, with limits at β ≥ 2 | the corrected limits from the T11 diagnosis; all 129 β values |
| H-12.A5 | T12 A5: `sympy.limit` on the D2 coefficient | series expansion or a high-precision limit sequence |
| H-12.A7 | T12 A7: minimum below F | a zero tolerance scaled to the dip, at precision set by e^(−2λΔt) |
| H-12.A8 | T12 A8: regression against prompt values | independently recomputed reference values, not the prompt's |
| H-13.A-sym | T13 Part A: 2 of 68 symbolic items | denesting and sign argument, plus the numerical fallback |
| H-13.A2 | T13 A2: numerical | extended precision at the cancellation |
| H-13.C2-12 | T13 C2 row 12: route (ii) tolerance | route (ii) with an equality tolerance below the exact limit's scale; the routes must agree |
| H-13.D | T13 D: reproduction | per the T13 diagnosis |
| H-14.C4 | T14 C4: paper render reproduces v1 | the criterion Task 15 accepted, now pre-registered and run |
| H-14.C10 | T14 C10: dry-run path resolver | a resolver that handles the failing paths; the dry run completes |
| H-16.D1 | T16 D1: items 2(b) and 9 | denesting and sign argument, plus the numerical fallback |
| H-16.D2 | T16 D2: 3.1 and 3.5 | compare the thesis-only imports with the draft's statements (kinds a–d) |
| H-17.E5 | T17 E5 / T18 F1: [47] scope | judge the current §6.2 and §7.3 sentences against [47]'s title and abstract, with the scope stated in advance |
| H-18.F2 | T18 F2: counts | covered by B3; the rule for "PASS (info)" stated in advance |
| H-18.F3 | T18 F3: §8.5 referee sentence | covered by B3 |
| H-18.F6 | T18 F6: appendices | covered by B6 |
| H-18.F1-21 | T18 F1: [21] in §1.6 | covered by B1 |

Report each re-check as resolved (pass), not resolved (fail, with a diagnosis), or document finding.

## Part D: Re-issue the inventory

Rewrite `classification/OPEN_ITEMS.md` for the end of Task 19, in the same format.
- An item may be marked **resolved** only if a pre-registered check in Tasks 1–19 resolved it.
- Items no check can resolve stay open, worded factually:
  - Conjecture 6.22;
  - Proposition 6.20's dependence on it;
  - the open problems;
  - the numerical results, which are evidence by nature;
  - external review.
- Close the "rough-draft chapters 8–9" entry only if B3 and B4 pass.

Also give the recount for chapter 8 and Appendix D, by task, through Task 19:
- the checks with a verdict;
- the failures;
- the tasks without pass criteria;
- the failures of Tasks 1–19 sorted by attribution (criterion, code, document, input, prediction).

**Part E. Conjecture 6.22, exploratory (time-box it; stop when the time is used).** Try to make progress on at most two turning points along Δt for D1–D3. For example:
- a sign-change bound for the derivative's exponential-polynomial form;
- or a computer-assisted argument: certified interval arithmetic on a compact normalised parameter region, plus endpoint asymptotics.

Report what was achieved, what remains, and any counterexample. Do not change the conjecture's status; a proof found here would need its own verification task.

## 6. Pre-registered checks (write these into PREREG_t19.md with these criteria)

| Check | Pass criterion |
|---|---|
| G1 Citations (B1) | [26] states the r/(2 − r) factor, or a form equivalent to it; the §6.3 identity reduces to 0; each of [29] and [40] supports the §7.4 sentence; both [21] sentences are consistent with [21]. Judge each against the stated scope (full text or abstract) and list every judgement. |
| G2 Theorem 2.2 (B2) | Kind (a) or (b) against the repository's referee sentences; 0 mismatches in ≥ 10,000 cases |
| G3 Chapter 8 (B3) | Every §8.4 example is real and correctly labelled; every Appendix D failure is covered; the §8.2 and §8.5 claims match the record; the recount equals 151 and 32 for Tasks 1–18 |
| G4 Chapter 9 (B4) | Every claim has a source and matches it |
| G5 Mechanical (B5) | 0 unresolved [n]; first-citation order holds; 0 wrong-type references; 0 unknown figures; 0 nonexistent task or check references |
| G6 Appendices (B6) | The draft's A, C and D match the renders, apart from formatting and the Task 19 entry |
| G7 Sync (Part A) | 0 occurrences of `sahomasugi2016` in the repository outside git history; the thesis render's Theorem 2.2 proof equals the draft's; source §11 has 6 items; the Appendix A comparison shows 0 differences after delimiter stripping |
| H-* Re-checks (Part C) | One criterion per re-check, as pre-registered under the Part C rules |

Parts D and E are reported, not pass/fail.

## 7. Report (RESULTS_t19.md), and what to send back

In `RESULTS_t19.md`, give:
- the commits (pre-registration, artifacts checked, results);
- the check table with outcome and runtime, including every H-* re-check;
- the diagnoses of any failure;
- the files changed;
- both thesis sha256 values.

Then, under **For the author**, give:
1. **B1:** each citation judgement, and the scope used.
2. **B2–B4:** every claim with its source and verdict, and any correction the text needs.
3. **B5–B6:** any broken reference or appendix difference.
4. **Part C:** a table of every re-check with resolved / not resolved / document finding.
5. **Part D:** the recount by task through Task 19, and the new `OPEN_ITEMS.md` in full.
6. **E1:** the referee's points, with your assessment of each.
7. **E2:** what was achieved on Conjecture 6.22.

Attach:
- `RESULTS_t19.md`;
- `OPEN_ITEMS.md`;
- `t19/referee_report.md`;
- the re-rendered Appendices A, C, D and E.