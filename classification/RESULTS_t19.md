# Task 19: close the open items (results)

- Pre-registration: `classification/PREREG_t19.md`, commit **7b6bd60** (with the Part C route scripts `t19/t19_routes.py` and
  `t19/h13d_replay.py`).
- Artifacts as checked: commit **8cb8777** (Part A sync, `t19/t19_checks.py`). The single recorded run of G1–G7 and of every Part C
  re-check ran on this commit (notes: `t19/results/run_notes.md`).
- Results: this file and `t19/results/` (raw outputs, manual readings), committed with the Part D inventory and the Appendix D Task 19
  entry.
- Thesis archive: the Task 18 copy of `thesis/Thesis_Draft_full.md` had sha256
  `f1b8ecd345955975c9db6543bf5b69d2e060073422f24c68a222777d185323b6` (in git history); it is replaced by the attached draft, sha256
  `f8d0b94a632b3b91ac04579d925b1409abcb694772fdf63b95ce0cabc52111d1` (byte-identical to `t19/input/Thesis_Draft_full.md`).
- The prompt's E1 (a referee pass) was dropped by the author ("I got rid of E1 and replaced it with E2, calling it just Part E"); there
  is no `t19/referee_report.md`.

## Check table

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| G1 Citations (B1) | **FAIL** | identity reduces to 0 (fallback max residual 0); [29], [40] and both [21] sentences hold; [26] cannot be determined from Roberts's text (unreachable; secondary sources agree) | 0.17 + reading |
| G2 Theorem 2.2 (B2) | **PASS** | kind (a): identical after markup; 0 mismatches in 10,000 random sequences (classes with k up to 4) | 0.78 |
| G3 Chapter 8 (B3) | **FAIL** | recount 151 / 32, Tasks 4 and 5 without criteria; §8.5 matches; §8.2 route descriptions interchanged; §8.4 T13 example mislabelled; coverage parser missed 2 of 33 lines | 0.16 + reading |
| G4 Chapter 9 (B4) | **FAIL** | 22 claims; 21 match; the Hill equivalence sup q > 2 ⇔ c/(FΠ₀) > 4 holds for n = 2 only | 0.09 + reading |
| G5 Mechanical (B5) | **PASS** | 0 unresolved [n], order [1]–[53] holds; 455 typed references, 0 wrong; 0 unknown figures; 131 task and 50 check references, 0 bad; [46]–[53] first cited in chapters 6–7 | 0.15 |
| G6 Appendices (B6) | **PASS** | records A 82/82, C 53/53, D 51/51, 0 differences | 0.01 |
| G7 Sync (Part A) | **FAIL** | (i) 16 occurrences in 11 files (10 recorded files of Tasks 14, 15, 17; `t19/t19_register.py`'s docstring); 0 in live files; (ii) Theorem 2.2 proof equal; (iii) §11 has 6 items; (iv) Appendix A 0 differences | 0.08 |
| H-6.C5 | **PASS** | both routes, root-finding: 0.0917 at 0.683, 0.0823 at 0.655, 0.0433 at 0.538, 0.0136 at 0.33; T6 grid values round the same | 1.4 |
| H-9.2 | **PASS** | mp ARE (100 digits) at ε = 10⁻⁴⁰: max relative error 3.1 × 10⁻¹², 0 over 10⁻⁵ in 2,001 cases; √ε slope 0.5000 ± 3 × 10⁻¹³ in all 2,001 | 20.2 |
| H-9.5 | **PASS** | 400,000 samples at 50 digits: V strictly decreasing everywhere, V > P everywhere, 0 missed basins (21,633,897 local minima refined) | 7540.3 |
| H-10.1a | **PASS** | √((G + λ′)²) → G + λ′; residual 0; fallback holds | 0.3 |
| H-10.1b | **PASS** | R² = F/(1 + w): radicand (2w + 1)², Y > 0; residual 0; fallback max 1e-61 | 0.6 |
| H-10.5 | **PASS** | value slope in [1.45, 1.55], position slope in [0.45, 0.55], monotone, ratio constant; printed 1.50007 and 0.50002 reproduced | 6.6 |
| H-10.6 | **PASS** | 1,000 sets: P < 10⁻⁶ P_max at λτ = 10∓24, slopes ±0.5 within 10⁻³, asymptote within 10⁻³ | 1.2 |
| H-11.3 | **PASS** | 129 β, 387,000 classifications, 0 failures | 7002.7 |
| H-12.A5 | **PASS** | series route: limit and series minus the stated coefficient reduce to 0; sequence at Δt = 10¹⁰, 10²⁰, 10⁴⁰ within 10^(−D+6) on 1,000 sets | 1.6 |
| H-12.A7 | **PASS** | 907/907 D1 sets with G > 2FΠ: one prior minimum below F each, every dip positive, ℓ = u = 1 and not All; relative dips 10^(−32,880,317) to 10^(−0.024) | 75.2 |
| H-12.A8 | **PASS** | new code at 928 digits: post(0⁺) 0.09; one maximum 0.20457 at 2.4645; Δt_E = 100 to 20 digits; one minimum 0.0099875 at 200; dip 0.125 % | 10.6 |
| H-13.A-sym | **PASS** | both items reduce after `rewrite(exp)`; series positive; fallback max 6e-63; −sFr < 0 at every set | 0.9 |
| H-13.A2 | **PASS** | 10,000 sets: 0 link failures; cross-check within 8.3 × 10⁻¹²⁹ (up to 174 digits) | 4.8 |
| H-13.C2-12 | **FAIL** | 439 flagged, **45 persisting** (8 sets, tanh gain), all route (i) All vs route (ii) Empty at R² = L₋ | 41.7 |
| H-13.D | **PASS** | clean worktree of 7195070: RESULTS_t10 and RESULTS_t12 regenerated, verdicts identical, 0 issues after masking the provenance line | 23596.0 |
| H-14.C4 | **PASS** | at 45b0058: 0 numbering mismatches; 14 hunks: 6 split, 1 rows 25–26, 7 excess-identity type, 0 other | 0.4 |
| H-14.C10 | **PASS** | Task 15's resolver: 89 paths, 0 unresolved | 0.8 |
| H-16.D1 | **PASS** | 2(b): derivative identity, product −2ΣΠ < 0, G⋆ root and positive, 1,000 sets 0 failures; 9: (R² + 2d)², residual 0, fallback holds | 1.3 |
| H-16.D2 | **PASS** | Propositions 3.1 and 3.5: render and draft identical (no difference of any kind) | 0.0 + reading |
| H-17.E5 | **PASS** | both [47] sentences consistent with the title and abstract | reading |
| H-18.F2 | **PASS** | G3 recount: 151 and 32 | (G3) |
| H-18.F3 | **PASS** | G3 §8.5: matches the record | (G3) |
| H-18.F6 | **PASS** | G6 | (G6) |
| H-18.F1-21 | **PASS** | G1: the §1.6 [21] sentence is consistent with Yüksel & Linder | (G1) |

Totals: **31 checks with a verdict, 5 fail** (G1, G3, G4, G7, H-13.C2-12). Runtimes are wall times on 4 CPUs shared by the route
runner, the H-13.D replay and Part E (load about 10). H-13.D: Task 10 run script 13,959 s (its last step failed as diagnosed), the
omitted diagnosis script 0.2 s, `make_results_t10.py` 0.1 s, Task 12 run script 9,636 s.

**Pre-registered checks that FAIL:** G1, G3, G4, G7, H-13.C2-12. Each is diagnosed below.

## Diagnoses

1. **G1 (attribution: input).** Roberts (1959) could not be reached (tandfonline.com, scribd.com refused; WebFetch "host not
   resolved", curl CONNECT 403). The search returned the bibliographic record, a summary saying the limits are based on "the
   asymptotic standard deviation of the averages", and secondary sources crediting Roberts with limits L·σ·√(λ/(2 − λ)). The factor
   r/(2 − r) was not seen in Roberts's own text, so the criterion's "states the factor" cannot be confirmed. Every other G1 part holds
   (`t19/results/g1_citations.md`).
2. **G3 (attribution: code; document).** (a) Code: the coverage parser read an attribution only between ": " and " —"; two Appendix D
   lines use parentheses ("plan's construction (criterion as pre-registered)"; "document (4, …) and code (2, parser)"), both in the
   five kinds. Read as pre-registered, every failure is covered. (b) Document: §8.4's criterion row lists "SymPy routes with no
   handling of √(x²) (T10, T13)"; Task 13's route failures were an undecided sign (1 − e^(−2x)) and an unrewritten sinh, with no square
   root (RESULTS_t13; the draft follows RESULTS_t16's parenthetical, which RESULTS_t13 does not support). (c) Document: §8.2 describes
   route (i) as root-finding on monotone pieces and route (ii) as sampling; in `t10/classify.py` and PREREG_t10, route (i) applies the
   Theorem 2.2 rule to the turning-point values and route (ii) is the root-finding route with sign tests at sample points. The
   persistent-disagreement claim itself (row 12, route (ii)'s sample point) matches. (`t19/results/g3_examples.md`.)
3. **G4 (attribution: document).** §9.2: "The Hill gain differs: its window class needs sup q > 2, that is c/(FΠ₀) > 4". sup q =
   (c/(FΠ₀))·sup_t t^(n−1)/(1 + tⁿ); the sup is 1/2 only for n = 2. For n = 1.5, 3 and 4 the threshold on c/(FΠ₀) is 3.780, 3.780 and
   3.510, and the stated equivalence fails in 15, 11 and 24 of 1,000 random sets near the threshold. §5.4 defines the Hill gain for
   every real n > 1. Correction for the author: "for n = 2, c/(FΠ₀) > 4" (as in the §3 table and Proposition 5.13).
   (`t19/results/g4_claims.md`.)
4. **G7 (attribution: criterion; code).** Clause (i) counts every tracked file. Ten recorded files of past tasks keep the old key, as
   disclosed before the run (`t14/RESULTS_t14.md`, `t14/bib_check.md`, `t14/build_register.py`, `t14/make_bib.py`,
   `t14/make_bib_check.py`, `t14/results/t14_checks.json`, `t15/input/Task_15_Repo_Sync_Prompt.md`, `t15/t15_checks.py`,
   `t15/t15_register.py`, `t17/results/e5_sources.md`); the protocol forbids editing them (criterion). The eleventh is Task 19's own
   `t19/t19_register.py`, whose docstring names the key it replaces and was not in the pre-registered exclusion list (code). The live
   files (bibliography, register, sources, renders) have 0. Clauses (ii)–(iv) hold.
5. **H-13.C2-12 (attribution: criterion).** Post-hoc diagnosis (`t19/h1312_diag.py`, `t19/results/h/H-13.C2-12_diag.json`; not a pass
   criterion): the 45 persisting cases are in 8 sets, all tanh-gain curves, monotone increasing with no turning point, at the
   tolerance set "exactly" to L₋. That stored L₋ is the analysis's numerical limit; it differs from L₋ recomputed at higher precision
   by up to 3.2 × 10⁻²⁵ relative, and the gap f − R² at route (ii)'s single sample point is of the same size (10^(−25.7) to
   10^(−24.5) relative) and of either sign. With the pre-registered equality tolerance 10⁻³⁰⁰ the two routes therefore compare at a
   resolution finer than the stored critical value carries: route (i) reads R² = L₋ exactly (All), route (ii) resolves a sub-10⁻²⁴
   difference against a value accurate to about 10⁻²⁵. The corrected criterion set the tolerance below the approach scale but above
   nothing: it must lie between the precision of the stored limits (~10⁻²⁵) and the gap at the sample point, and here those coincide.
   The class at R² equal to the exact L₋ of an increasing curve is All (Theorem 2.2(2)), as route (i) says; no document change. The
   T13 diagnosis's "exactly L₋" was also loose: R² equals the stored limit, not the exact one.

**Development disclosures.** The dry run before the recorded run found one code fault, fixed in the artifacts commit: H-14.C4's
category (d) missed the excess identity's label line (fixed to identify a label line by the result heading above it, the
pre-registered definition). Dry outputs showed H-12.A8 reproducing the printed values at 80 digits; nothing else bearing on an outcome
was seen. The first launch of the Part C run was stopped after one minute (the session's 2-hour background limit); H-6.C5 had
completed and was kept, nothing else had written a result, and both jobs were relaunched detached on the same commit
(`run_notes.md`). Running the render chain rewrote the comment line of `register/tasks.yaml` (a past manual edit) and the PDF metadata of
the figures; both were restored, so the chain is not idempotent on those two points.

## Files changed (Part A, commit 8cb8777)

`references.bib` (entry 26: `roberts1959`); `register/references.yaml`, `register/results.yaml` (key, via the new chain step
`t19/t19_register.py`); `source/thesis_only/critical-tolerance.md` (draft lines 158–165, via `t19/make_thesis_only_t19.py`);
`source/Stages_0_4_Source.md` §11 items 5–6 (**documentation fix**, worded as the draft's §9.4 items 5–6); `register/render.py`
(Appendix C introduction); `t15/make_appendix_de.py` (Task 19 support, Appendix E row and chain); renders `Stages_0_4_Thesis.md`,
`Stages_0_4_Paper2.md`, `Appendix_C_References.md`, `Appendix_E_Reproduction.md`; `thesis/Thesis_Draft_full.md`. After the run:
`Appendix_D_Verification.md` (Tasks 1–19, the planned Task 19 entry), `OPEN_ITEMS.md`. No mathematical content changed.

## For the author

### 1. B1 — citations and scope

| Citation | Scope | Judgement |
|---|---|---|
| [26] Roberts (1959) | record, a summary of the paper, secondary EWMA sources | cannot be determined from Roberts's text; secondary sources credit him with λ/(2 − λ) |
| §6.3 identity | SymPy + 1,000-set fallback | holds for 0 < α < 2 (1 − (1 − α)² = α(2 − α) > 0) |
| [29] Jazwinski | contents, reviews | holds at contents scope (Ch. 7 linear filters and predictors, continuous–discrete filter) |
| [40] Anderson & Moore | contents, catalogue | holds at contents scope (Ch. 3 the discrete-time Kalman filter) |
| [21] in §1.6 and §7.1 | abstract (journal and arXiv versions) | both consistent (observation channels as optimisation variables in stochastic control) |

If you want [26] confirmed, the place to look is Roberts's §2 (variance of the geometric moving average) on JSTOR or Taylor & Francis.
Separately, Task 18 said Kalata's DOI was not confirmed; the bibliography already carried doi:10.1109/TAES.1984.310438.

### 2. B2–B4 — claims and verdicts

- **B2 Theorem 2.2:** the new closing sentences are the repository's referee sentences word for word (kind (a)); the rule as stated
  matched direct computation in 10,000 of 10,000 random sequences at tolerances equal to interior turning-point values.
- **B3 chapter 8:** recount 151 and 32 (with Task 2's informational pass), Tasks 4 and 5 without criteria — matches. §8.5 matches.
  Corrections needed: (a) §8.2's route descriptions are interchanged (route (ii) is the root-finding route; route (i) reads the
  turning-point values through Theorem 2.2), and "every classification … rests on route (i)" should be re-read accordingly;
  (b) §8.4's √(x²) example should name T10 (and T16 under Code) but not T13, whose route failures were a sign SymPy could not decide
  and a sinh it did not rewrite; (c) outside the pre-registered checks: the paragraph after the §8.4 table lists "the other document
  failures" but omits T16 D2, T16 D6 and T18 F6, which Appendix D attributes partly to the document.
- **B4 chapter 9:** 21 of 22 claims match (table in `t19/results/g4_claims.md`). Correction: §9.2's Hill sentence holds for n = 2 only
  ("for n = 2, c/(FΠ₀) > 4"); the general condition is c/(FΠ₀) > 2/h(n), h(n) = sup_t t^(n−1)/(1 + tⁿ) = (n − 1)^((n−1)/n)/n.
  "Propositions 5.8 and 5.9", the 9.3F/17.6F peaks, the Numerical result 8.2 grid sentence, open problem 2's evidence and open problem
  4's expectation all match.

### 3. B5–B6

No broken reference, no wrong type, no unknown figure, no bad task or check reference. The draft's Appendices A, C and D match the
renders record for record (Appendix D: Tasks 1–18; the Task 19 entry is new in the render). Introductions differ only in the
render's added source note for Appendix C.

### 4. Part C — re-checks

| ID | Original failure | Outcome |
|---|---|---|
| H-6.C5 | T6 C5 peak locations | resolved |
| H-9.2 | T9.2 ARE route | resolved |
| H-9.5 | T9.5 double-precision flags | resolved |
| H-10.1a | T10.1 misspecified inverse | resolved |
| H-10.1b | T10.1 forced ray | resolved |
| H-10.5 | T10.5 pair birth | resolved |
| H-10.6 | T10.6 zero-limit shape | resolved |
| H-11.3 | T11.3 classes at β ≥ 2 | resolved |
| H-12.A5 | T12 A5 sympy.limit | resolved |
| H-12.A7 | T12 A7 minimum below F | resolved |
| H-12.A8 | T12 A8 regression values | resolved |
| H-13.A-sym | T13 Part A 2 of 68 | resolved |
| H-13.A2 | T13 A2 numerical | resolved |
| H-13.C2-12 | T13 C2 row 12 | **not resolved** (criterion: the 10⁻³⁰⁰ tolerance is finer than the stored limit's precision) |
| H-13.D | T13 D reproduction | resolved |
| H-14.C4 | T14 C4 paper render vs v1 | resolved |
| H-14.C10 | T14 C10 dry-run resolver | resolved |
| H-16.D1 | T16 D1 items 2(b), 9 | resolved |
| H-16.D2 | T16 D2 3.1 and 3.5 | resolved |
| H-17.E5 | T17 E5 / T18 F1 [47] | resolved |
| H-18.F2 | T18 F2 counts | resolved |
| H-18.F3 | T18 F3 §8.5 referee sentence | resolved |
| H-18.F6 | T18 F6 appendices | resolved |
| H-18.F1-21 | T18 F1 [21] in §1.6 | resolved |

No re-check is a document finding: in each, the thesis's claim held at its printed precision. Two inventory notes: T14 C10 was
already resolved by Task 15's C13 (a pre-registered pass with the same resolver), which `OPEN_ITEMS.md` (Task 18) listed as only
diagnosed; and Task 18's pre-registration called the Task 13 referee report "twelve numbered points" (it has 14).

### 5. Part D — recount and the new OPEN_ITEMS.md

| Task | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Checks with a verdict | 12 | 3 | 8 | 0 | 0 | 6 | 15 | 5 | 7 | 10 | 11 | 13 | 15 | 11 | 13 | 8 | 7 | 7 | 31 | 182 |
| Failed | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 4 | 1 | 3 | 5 | 3 | 2 | 3 | 4 | 4 | 5 | 37 |

Tasks without pass criteria: 4 and 5. Failures of Tasks 1–19 by attribution, over the 38 failure lines of Appendix D (Task 13's C2 is
one failed check with two lines, rows 8 and 12), each kind a line names counted once ("route" and "plan's construction" as criterion):
**criterion 19, code 14, document 13, input 2, prediction 1.** Task 19's: G1 input; G3 code and document; G4 document; G7 criterion and
code; H-13.C2-12 criterion.

The new `OPEN_ITEMS.md` is reproduced in full in that file (attached); its sections are the conjecture and open problems, numerical
results, citations, external review, chapter 8–9 text, and failures not resolved by a later check. "Rough-draft chapters 8–9" stays
open: G3 and G4 failed.

### 6. E1

Dropped by the author before the run; no referee pass was made in this task.

### 7. Part E — Conjecture 6.22 (exploratory; `t19/part_e/`)

About two hours of work, D1 only. Achieved:

1. **Reduction.** With t = λΔt, g = G/λ and ν = 2ΠΣ/λ², post/F, prior/F and avg/F depend only on (t, g, ν) (checked symbolically): D1's
   conjecture is a statement about a two-parameter family.
2. **Structure.** Each metric's derivative is (positive denominator) × an exponential polynomial: post and prior have 6 terms
   (exponents 0, G, 2G, 2G + 2λ, 3G + 2λ, 4G + 2λ, polynomial coefficients of degree ≤ 2 in Δt), avg 11. The Pólya–Szegő bound gives at
   most 13 sign changes for post and prior and 25 for avg — far from 2, so the generic bound does not decide the conjecture.
3. **Prior without the exponential factor.** prior/F = 1 + e^(−2t)(p − 1), p = post/F, so d prior/dt has the sign of p′ − 2(p − 1); the
   e^(−2t) factor that defeated Task 12's zero tolerance drops out exactly.
4. **Parity from the endpoints (proved).** At t → 0: dp/dt → g(g − ν)/(ν(1 + g)); the prior bracket → −g(g − ν)/(ν(1 + g)); d(avg/F)/dt
   = −g²(g² + 4g − 4ν)t/(6ν(1 + g)) + O(t²). At t → ∞: dp/dt ~ −2/(νt²), the prior bracket → 2, d(avg/F)/dt ~ 1/(2t²). Hence, off the
   boundary curves, the number of turning points of post and of prior is **odd iff g > ν, i.e. G > 2FΠ**, and of avg **odd iff
   g² + 4g > 4ν**. (G > 2FΠ is the excess condition; the avg parity is a new condition.)
5. **Evidence.** A 41 × 41 log grid of (g, ν) ∈ [10⁻⁴, 10⁴]², t ∈ [10⁻⁸, 10⁸] (961 points, precision raised for small t), sign changes
   counted: post 0 or 1, avg 0 or 1, prior 0, 1 or 2 (2 at 55 points, all just below the diagonal, 10^(−1.4) ≤ g/ν < 1); never more
   than 2. The counts agree with the parity rule at every grid point off g = ν; the 41 disagreements are exactly the diagonal points,
   where the endpoint slope vanishes and the rule does not apply.

Remains: a proof of "at most two" for D1 (the parity result reduces it to excluding three or more, i.e. to an upper bound of 2 on a
6-term exponential polynomial with quadratic coefficients in a two-parameter family); a certified computation (interval arithmetic on a
compactified (g, ν, t) box with the endpoint expansions above as the boundary pieces) was not attempted in the time; D2 (three
parameters after scaling) and D3 were not studied. **No counterexample was found.** Conjecture 6.22's status is unchanged.

## Attachments

`RESULTS_t19.md`, `OPEN_ITEMS.md`, `Appendix_A_Register.md`, `Appendix_C_References.md`, `Appendix_D_Verification.md`,
`Appendix_E_Reproduction.md`.
