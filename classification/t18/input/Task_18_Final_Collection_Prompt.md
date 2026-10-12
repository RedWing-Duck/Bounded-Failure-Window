# Task 18 — Final collection: verify chapters 8–9 and the Task 17 fixes, settle the last open items, and archive the thesis

You are working in the repository that holds `classification/` (Tasks 8–17), `verification/` (Tasks 1–7) and `reference/phase1/`. This is the last task of this cycle. Use the usual protocol:
- Write `classification/PREREG_t18.md` with every check in §5 and its pass criterion. Commit it **before** running anything that produces a result.
- Run the checks once, on one recorded commit.
- Report in `classification/RESULTS_t18.md`. A failed check stays a failure, with a diagnosis (criterion, input, code or document). Never change a criterion or an artifact after the recorded run.

**Do not change any mathematical content.** If you find a mathematical error anywhere, record it and do not fix it.

Keep the Task 16–17 precautions:
- every symbolic check gets a denesting step for √(x²) and an explicit sign argument;
- every identity SymPy cannot reduce gets a pre-registered numerical fallback (≥ 1,000 random sets, a stated seed);
- every high-precision test sets its working precision from the quantities involved, for example more than 2λΔt/ln 10 digits wherever e^(−2λΔt) appears.

## Attached

| File | What it is |
|---|---|
| `Thesis_Draft_full.md` | Export of the complete thesis draft: chapters 1–7, chapters 8–9 (marked "rough draft"), and Appendices A–E. Since Task 17 it adds chapters 8–9 and these Task 17 fixes: Corollary 7.4's proof completed; "129 values of β"; the §6.7 table label; the [47] sentences in §6.2 and §7.3; the [21] sentence in §7.1; the reason P⁻ < F in Proposition 6.13's proof; Task 17 in Appendix D; and chapter 8's counts updated to Tasks 1–17. Read it; do not edit it. |

---

## Part A — Verify what has not been verified

**A1. The Task 17 fixes.** Check each fix against the Task 17 finding it answers, and report each as resolved or not resolved:
- Corollary 7.4's proof: does it now cover σ⋆² → 0 and the last clause?
- the β count;
- the §6.7 label;
- the two [47] sentences;
- the [21] sentence;
- Proposition 6.13's P⁻ < F step: the identity f(F) = F²a² must reduce to 0.

**A2. Chapter 8.**
- Recount, from every task's own RESULTS or REPORT file:
  - the number of pre-registered checks with a verdict across Tasks 1–17 (the draft says 144);
  - the number that failed (the draft says 28);
  - the tasks with no pass criteria (the draft says Tasks 4 and 5).
- Check the §8.4 attribution table: every example cited in it is a real failure, its task label is right, and every failure in Appendix D falls under at least one listed attribution.
- Check §8.2's claim that the only persistent route disagreement was row 12 of the Task 13 audit, attributed to route (ii).
- Check §8.5's claim that the only independent referee pass is the one on Theorem 7.6 (Task 13). If the repository records any other, report it.

**A3. Chapter 9.** For every numerical or factual claim in §9.1–9.4, give the result or source it rests on and whether it matches, including:
- the factor-of-two window conditions (κ > 2, F′ > 2F, g > 2F, ρ > 2, λ′ < λ/2);
- 9.3F and 17.6F;
- 5 × 10⁻⁴;
- 10⁻⁸;
- 10^(−32,880,317);
- 0.125%;
- each open problem's description against the repository's open-problems section.

Report any claim with no source in the repository or the draft.

**A4. Whole-draft mechanical checks** (as in Task 17 E4):
- every [n] resolves, and [1]–[53] first appear in order;
- every typed result reference has the right type, ranges included;
- every Figure B.n exists;
- every "Task n" or "Tn.m" reference names a task and check that exist.

**A5. Two citations Task 17 could not settle.** Fetch the full text where you can. Both are open access or standard references: SpringerPlus is open access, and Jazwinski is a textbook.
- **[26]** (Saho & Masugi 2016): does it state, or use, the variance factor α/(2 − α) (or L/(2 − L)) for an exponentially weighted or α-type filter?
- **[29]** (Jazwinski 1970): does it give the prediction-error covariance for an estimate of a delayed state, or the prediction step in a form that covers it?

If either answer is no or cannot be determined, do not change the bibliography or the register. Report:
- what the source does contain;
- one or two candidate standard references that state the fact, with full bibliographic details and DOIs where they exist.

I will decide.

## Part B — Repository corrections

1. **The β count.** In `source/Stages_0_4_Source.md`, the label of Theorem 7.8 says "37 values of β". Correct it to 129, with the composition Task 11's pre-registration gives, and re-render. This is a factual correction of a record, not of mathematics.
2. **Proposition 2.7's proof.** The repository's proof writes the value change as (4/3)a(bδ)^(3/2), without the absolute value. The thesis-only text has (4/3)|a|(bδ)^(3/2). Make the repository's proof match, and record it as a documentation fix.
3. **Theorem 2.2's parts.** The thesis draft numbers them (1)–(4), and the repository (a)–(d). The thesis render now mixes them. Import the draft's statement of Theorem 2.2 as a thesis-only text, so the thesis render uses (1)–(4) throughout. Then check that no "(a)–(d)" reference to Theorem 2.2 remains in the thesis render.
4. **Archive the thesis text.** Commit the attached draft as `thesis/Thesis_Draft_full.md`, the thesis text of record for this cycle. It is not rendered and not edited. Record its sha256 in `RESULTS_t18.md`.
5. **Appendices.** Re-render:
   - Appendix A, from the register;
   - Appendix C, from the bib and the reference register;
   - Appendix D, with Tasks 1–18;
   - Appendix E, with the Task 18 row and chain step.

   Check that the draft's Appendices A, C and D match the renders line for line, apart from formatting, and list every difference.

## Part C — Closing inventory

Produce `classification/OPEN_ITEMS.md`, a single list of everything not settled at the end of this cycle, each with its status and where it is recorded:
- the conjecture and the open problems;
- the numerical results that are evidence rather than proof;
- the undetermined citations, if Part A5 leaves any;
- results with no external review;
- any rough-draft text (chapters 8–9);
- any check that still fails without a resolution.

Nothing in this list may be marked resolved unless a check in Tasks 1–18 resolved it.

## 5. Pre-registered checks (write these into PREREG_t18.md with these criteria)

| Check | Pass criterion |
|---|---|
| F1 Task 17 fixes (A1) | All six fixes resolve their finding; f(F) = F²a² reduces to 0 |
| F2 Chapter 8 counts (A2) | Recounted totals equal the draft's (144 checks with a verdict, 28 failed, Tasks 4 and 5 without criteria); every §8.4 example is a real failure with the right task; every Appendix D failure falls under a listed attribution |
| F3 Chapter 8 claims (A2) | §8.2's and §8.5's claims match the repository record |
| F4 Chapter 9 claims (A3) | Every numerical and factual claim has a source and matches it |
| F5 Mechanical (A4) | 0 unresolved [n]; first-citation order for [1]–[53]; 0 wrong-type references; 0 unknown figures; 0 nonexistent task or check references |
| F6 Appendices (B.5) | The draft's Appendices A, C and D match the renders apart from formatting |
| F7 Thesis render consistency (B.3) | 0 "(a)–(d)" references to Theorem 2.2 in the thesis render |

Part A5 and Part C are reported, not pass/fail.

## 6. Report (RESULTS_t18.md), and what to send back

In `RESULTS_t18.md`:
- the commits (pre-registration, artifacts checked, results);
- the check table with outcome and runtime;
- diagnoses of any failure;
- files changed;
- the sha256 of the archived thesis.

Then, under **For the author**, give:
1. **A1:** each fix with resolved or not resolved.
2. **A2:** the recounted totals per task, and any correction chapter 8 needs.
3. **A3:** every claim of chapter 9 with its source and verdict.
4. **A4:** any broken reference.
5. **A5:** what [26] and [29] contain, and candidate references if needed.
6. **Part B:** what changed in the repository.
7. **The closing inventory** (`OPEN_ITEMS.md`) in full.

Attach:
- `RESULTS_t18.md` and `OPEN_ITEMS.md`;
- the re-rendered Appendices A, C, D and E;
- the new thesis-only text for Theorem 2.2.
