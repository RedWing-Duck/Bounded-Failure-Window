# Pre-registration — Task 18: final collection (chapters 8–9, the Task 17 fixes, last open items, archive)

Committed **before** any Task 18 script that produces a result is written or run. Not edited after its commit. The checks F1–F7
run **once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis attributed to the
**criterion**, the **input**, the **code** or the **document**. No criterion and no artifact is changed after the recorded run,
with one planned exception: the Task 18 entry of Appendix D, written from the recorded outcome (as for Tasks 15 and 17).

**No mathematical content changes.** Part B makes two record corrections the prompt names (the β count in a label; the absolute
value in Proposition 2.7's proof, a documentation fix matching the thesis text), one thesis-only import (Theorem 2.2) and
re-renders. A mathematical error found anywhere is recorded, not fixed.

**Inputs** (copied unchanged to `classification/t18/input/`): `Thesis_Draft_full.md` (read-only; sha256
`f1b8ecd345955975c9db6543bf5b69d2e060073422f24c68a222777d185323b6`; archived unchanged as `thesis/Thesis_Draft_full.md` at the
repository root, Part B.4) and the Task 18 prompt.

Precautions (Tasks 16–17): every symbolic identity gets the denesting step (√(Y²) → Y with Y's sign argued) and explicit sign
arguments; every identity SymPy cannot reduce has a numerical fallback at ≥ 1,000 random sets, seed **18001**, relative residual
< 10⁻³⁵; any high-precision evaluation involving e^(−2λΔt) runs at more than 2λΔt/ln 10 + 60 digits. Spare seed **18002** (use
reported).

## Disclosure: what is known before the run

1. **The draft** has been read: the diff against the Task 17 input (the nine Task 17 fixes, §1 status line), chapters 8–9 in full,
   and the headers of Appendices A, C and D. Proposition 6.13's proof now ends "f(F) = F²a² > 0", which Task 17's diagnosis
   derived; Corollary 7.4's proof now cites Proposition 3.5 (σ⋆² → 0) and Theorem 5.1; §6.7 writes "Prop. 6.10, Cex. 6.11,
   Prop. 6.12" ("Cex." is new; F5 reads it as Counterexample).
2. **Chapter 8's totals.** The repository's Appendix D (rendered in Task 17 from each task's report) lists per-task counts whose
   sums are 144 and 28; that rendering parsed the same report tables F2 recounts. F2 re-derives the counts independently of
   Appendix D's code (its own parser) and checks the §8.4 examples against the failures recorded in the reports.
3. **§8.5 and the referee.** `classification/t13/referee_report.md` (Task 13, check C4) is an independent referee report on the
   whole consolidated document of the time: twelve numbered points on several results (in old numbering: Theorem 6, Propositions
   29–31, Theorem 35 and others), with dispositions, recorded in the source's change log as "T13 C4 (referee 1–12)". The draft's
   §8.5 says the only referee pass is on Theorem 7.6. F3 compares the claim with this record; on the reading in this disclosure
   it does not match.
4. **Theorem 2.2's parts in the thesis render.** The statement itself is labelled (a)–(d); the source refers to its parts five
   times (`[[critical-tolerance]](a)–(b)`, `(c)`, `(c),(d)`, `(d)` twice), four of them inside blocks already replaced by Task 17's
   thesis-only imports and one in the paper-only change log. After the import of the draft's Theorem 2.2 the expected count is 0.
5. **Appendix formats.** The draft escapes brackets (`&#91;1\]`, `\[n\]`, `\_`) and drops backticks; its Appendix C introduction
   says "[46]–[53] are first cited in chapters 6–7", the render's says otherwise. F6 compares records (table rows, reference
   entries, task entries and failure bullets) after removing formatting; the title and introduction paragraphs are compared and
   listed but are not records.
6. **A5 sources.** doi.org and Crossref are refused by the network policy (Task 17). Whether PubMed Central or the publisher
   pages for [26] can be fetched, and what is available for [29], is found out during the run.

## Part A — checks

Run script: `t18/t18_checks.py`. Manual readings after the run: `t18/results/` (F2's §8.4 mapping, F3, F4 table, A5).

### F1 — the Task 17 fixes (A1)

| Fix | Resolved if |
|---|---|
| Corollary 7.4's proof | the proof cites σ⋆² → 0 as Π → ∞ (Proposition 3.5) and Theorem 5.1 for the last clause; SymPy: lim_{Π→∞} 2Σ/(λ + √(λ² + 2ΣΠ)) = 0 |
| β count | the draft's count equals the number of distinct β in `t11/results/t11_3.json` |
| §6.7 label | every typed reference in the row names a result of that type (6.10 Proposition, 6.11 Counterexample, 6.12 Proposition) |
| [47] sentences (§6.2, §7.3) | both describe [47] as about time-correlated **model error** in Kalman smoothing, consistent with Task 17's evidence (`t17/results/e5_sources.md`) |
| [21] sentence (§7.1) | [21] is no longer cited for monotonicity under garbling, and its new role (observation channels as design variables) matches Task 17's evidence |
| Proposition 6.13's P⁻ < F | the proof states it; with f(M) = M² + s(r − F)M − sFr, s = 1 − a², f(F) − F²a² reduces to 0 (SymPy, denesting not needed); plus f(0) < 0 and leading coefficient 1 (sign argument), and a numerical test of M < F on 1,000 random (λ, Σ, Π, Δt), seed 18001, at the precision rule above |

**Pass:** all six resolved and f(F) = F²a² reduces to 0.

### F2 — chapter 8 counts (A2)

- For each task 1–17, the checks with a verdict are recounted from that task's own RESULTS or REPORT file (the first check table;
  for Tasks 1–3 and 6–7 the rows of `verification/REPORT.md` for that task), counting rows whose verdict cell says PASS or FAIL.
  Tasks with no pass/fail criteria are those whose report has no such rows.
- The §8.4 table: each example is matched to a failure recorded in the named task's report and its attribution there; the result
  is listed example by example (`t18/results/f2_examples.md`, manual after the run).
- Every failure in the Appendix D render (Tasks 1–17) is mapped to at least one of the five attributions (criterion, code,
  document, input, prediction); "route" and "plan's construction" count under criterion or code as their reports explain.
**Pass:** totals 144 and 28 and Tasks {4, 5}; every §8.4 example is a real failure of the named task; every Appendix D failure maps.

### F3 — chapter 8 claims (A2)

- §8.2: across every task's results (JSON and reports), the persistent route disagreements (route (i) vs route (ii) after
  diagnosis) are listed; the claim holds if the only one is row 12 of the Task 13 audit, attributed to route (ii).
- §8.5: every referee or external-review record in the repository (`referee`, `external review`, `independent` in reports,
  change logs and `t13/`) is listed; the claim holds if the only one is a referee pass on Theorem 7.6 (Task 13).
**Pass:** both claims match the record.

### F4 — chapter 9 claims (A3)

Every numerical or factual claim in §9.1–9.4 is listed with the result or stored value it rests on and a verdict
(`t18/results/f4_claims.md`). Mechanical parts in the run: the window conditions against Propositions 5.8, 5.9, 5.10, 6.25, 6.26
(register statements); 9.3F and 17.6F against the formulas (Task 16's values 9.2875, 17.575); 5 × 10⁻⁴ (`t10_4.json`); 10⁻⁸
(Numerical result 8.2, Task 10.5); 10^(−32,880,317) (`t12/RESULTS_t12.md`); 0.125 % (recomputed, Task 17's precision rule); each
of §9.4's six open problems against the repository's open-problems section (`source/Stages_0_4_Source.md`, §11) and register.
A claim with no source in the repository or the draft is a failure.
**Pass:** every claim has a source and matches it.

### F5 — mechanical (A4)

As Task 17 E4 over the whole draft text up to "## Appendices": [n] resolution and first-citation order for [1]–[53]; typed result
references with types, ranges and the abbreviations of Task 17 plus "Cex." (Counterexample); Figure B.n against `figures.yaml`.
Plus task references: every "Task n" names a task 1–17 with a pre-registration in the repository; every "Tn.m" and "Tn X" (for
example T10.7, T13 C2, T16 D1) names a check that appears in the first column of task n's check table (or, for Tasks 12–13, in its
A/B/C row labels). Appendix D's own task entries are excluded (they are F6's).
**Pass:** 0 unresolved [n]; order holds; 0 wrong-type or nonexistent result references; 0 unknown figures; 0 nonexistent task or
check references.

### F6 — appendices (B.5)

Appendices A, C and D of the draft against the renders at the artifacts commit (Appendix D render with Tasks 1–17). Normalisation
removes formatting only: HTML entities decoded, backslash escapes, backticks, `*` emphasis and Markdown table separators removed,
whitespace collapsed. Records are compared line for line: Appendix A table rows by result number; Appendix C entries by [n];
Appendix D task lines and failure bullets in order. Titles and introductions are compared and listed separately.
**Pass:** every record matches. Every difference, records and introductions, is listed.

### F7 — thesis render consistency (B.3)

In `Stages_0_4_Thesis.md`: count references to Theorem 2.2 with a letter part ("Theorem 2.2(a)" … "(d)", "Thm 2.2(…)", "2.2(c),(d)")
and lettered part labels in its statement ("(a) *Local constancy*" and the like). **Pass:** 0.

## Part A5 (reported, not pass/fail)

For [26] and [29]: fetch the full text where possible (PubMed Central / SpringerPlus for [26]; table of contents or preview for
[29]); report what each contains on the point at issue; if the answer is no or cannot be determined, give one or two standard
references that state the fact, with bibliographic details and DOIs. The bibliography and register are not changed.

## Part B — repository corrections

1. `source/Stages_0_4_Source.md`, Theorem 7.8's label: "37 values of $\beta$" → "129 values of $\beta$ ($\beta = k/20$,
   $k = -40, \dots, 80$, plus $\{0, 2\} \pm \{10^{-6}, 10^{-3}\}$)", the composition of `PREREG_t11.md`.
2. `source/Stages_0_4_Source.md`, Proposition 2.7's proof: `\tfrac43a(b\delta)^{3/2}` → `\tfrac43|a|(b\delta)^{3/2}`.
3. `source/thesis_only/critical-tolerance.md`: the draft's Theorem 2.2 statement and proof (draft lines 158–165), placed by
   `register/thesis_overrides.yaml` (replace `critical-tolerance`).
4. `thesis/Thesis_Draft_full.md` at the repository root, byte-identical to the input; sha256 recorded in the results.
5. Re-render Appendices A, C, D (Tasks 1–17 at the recorded run; the Task 18 entry after it) and E (Task 18 row and chain step
   `python3 t18/make_thesis_only_t18.py`).

## Part C — closing inventory

`classification/OPEN_ITEMS.md`, written after the run: the conjecture and open problems; numerical results that are evidence
rather than proof; undetermined citations; results with no external review; rough-draft text; checks that still fail without a
resolution. Nothing is marked resolved unless a check in Tasks 1–18 resolved it, and each item names where it is recorded.

## Report

`classification/RESULTS_t18.md`: commits, check table with outcomes and runtimes, diagnoses, files changed, the archived thesis's
sha256, and **For the author** items 1–7. Attachments: `RESULTS_t18.md`, `OPEN_ITEMS.md`, Appendices A, C, D and E,
`source/thesis_only/critical-tolerance.md`.
