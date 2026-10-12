# Pre-registration — Task 19: close the open items

Committed **before** any Task 19 script that produces a result is run. Not edited after its commit. The checks G1–G7 and the
Part C re-checks H-* run **once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis
attributed to the **criterion**, the **input**, the **code**, the **document** or a **prediction**. No criterion and no artifact is
changed after the recorded run, with two planned exceptions written from the recorded outcome: the Task 19 entry of Appendix D
(as in Tasks 15, 17 and 18) and `OPEN_ITEMS.md` (Part D).

**No mathematical content changes.** Part A swaps a bibliography key, imports the draft's Theorem 2.2 text as a thesis-only file,
adds two open problems to a list (a documentation fix), fixes a comparison normaliser and re-renders. A mathematical error found
anywhere is recorded, not fixed.

**Inputs** (copied unchanged to `classification/t19/input/`): `Thesis_Draft_full.md` (read-only; sha256
`f8d0b94a632b3b91ac04579d925b1409abcb694772fdf63b95ce0cabc52111d1`; archived unchanged as `thesis/Thesis_Draft_full.md`, Part A.6)
and the Task 19 prompt (`Task19_prompt.md`, sha256 `aba90b7e12ac3daf5679ef8b3daa0e13fe6c924ebf395dd43f3a67b1c6cae14d`).

**The prompt's E1 is dropped.** The author wrote after the prompt: "Sorry I got rid of E1 and replaced it with E2, calling it just
Part E." So there is no referee pass and no `t19/referee_report.md`; "E2" in the prompt's report list is Part E below.

## Precautions (Tasks 16–18)

- **Denesting and signs.** Every symbolic check states its square roots; where √(X) has X = c·Y², the root is replaced by Y only
  with an explicit sign argument that Y > 0 under the stated hypotheses (SymPy `is_positive` on a form where it is manifest, plus the
  argument written in the check). Where no square root occurs, that is recorded.
- **Numerical fallback.** Every identity SymPy cannot reduce, and every identity listed below as having one, has a fallback at
  ≥ 1,000 random sets with a stated seed and relative residual < 10⁻³⁵.
- **Working precision from the quantities.** Stated per check: more than 2λΔt/ln 10 + 60 digits wherever e^(−2λΔt) must be resolved
  against O(1) terms; where an exponentially small term is beyond all orders and is not resolved, the check says so and sets the
  precision from the cancellation that remains.
- **Seeds** (new): 19001 G1 fallback; 19002 G2; 19003 H-12.A5; 19004 H-10.1a; 19005 H-10.1b; 19006 H-13.A-sym; 19007 H-16.D1
  item 2(b); 19008 H-16.D1 item 9; 19009 G4 (Hill exponents). Spare 19099 (use reported). Re-checks that re-run a past task's
  pre-registered sample keep that task's seeds (named per check).

## Disclosure: what is known before the run

1. **The draft** has been read: the diff against the Task 18 archive (the changes listed in the prompt), chapters 8–9 in full,
   Theorem 2.2, §1.6, §6.3, §7.1, §7.4 and the appendix headers. The draft's new closing sentences of Theorem 2.2's proof and the
   repository's referee sentences (`source/Stages_0_4_Source.md`, the proof of `critical-tolerance`) were read side by side; apart
   from parentheses versus a colon and math markup they have the same words. G2's textual part is expected to give kind (a).
2. **§8.2's description of the routes.** The draft says route (i) "finds every crossing of R² by root-finding on the monotone pieces"
   and route (ii) "samples the curve and reads off its components, with an equality tolerance". In `t10/classify.py`, route (i) is the
   Theorem 2.2 rule on the turning-point sequence and route (ii) is root-finding on monotone pieces plus a sign test at sample points
   (with the equality tolerance). The route descriptions are part of the §8.2 claim and are read in G3 against the code.
3. **The Hill gain in §9.2.** The draft states "its window class needs sup q > 2, that is c/(FΠ₀) > 4" without naming n. For n = 2,
   sup q = c/(2FΠ₀) and the equivalence holds; §5.4 defines the Hill gain for every real n > 1, and for n ≠ 2 sup q is a different
   function of c/(FΠ₀). G4 judges the sentence as written: the equivalence must hold for the family the sentence names. It is
   expected to be judged "holds for n = 2 only".
4. **Chapter 8 counts.** Task 18's diagnosis recounted 144 checks and 28 failures for Tasks 1–17 when Task 2's "PASS (info)" row is
   counted; Task 18's own table has 7 checks and 4 failures. G3's parser is written for this task (rule below), not reused.
5. **The old bibliography key** occurs, before Part A, in 13 files tracked by git (inventory by `git grep`): the live
   `references.bib`, `register/references.yaml`, `register/results.yaml`, and ten recorded files of Tasks 14, 15 and 17
   (`t14/RESULTS_t14.md`, `t14/bib_check.md`, `t14/build_register.py`, `t14/make_bib.py`, `t14/make_bib_check.py`,
   `t14/results/t14_checks.json`, `t15/input/Task_15_Repo_Sync_Prompt.md`, `t15/t15_checks.py`, `t15/t15_register.py`,
   `t17/results/e5_sources.md`). The protocol forbids changing past tasks' recorded artifacts, so those ten keep it, and G7's first
   clause, as the prompt words it, **is expected to fail** on them (attribution: criterion). G7 reports the live-file count alongside.
   Task 19's own pre-registration, check script and copy of the prompt must name the key to search for it; they are excluded.
6. **Appendix C's introduction.** The draft's reads "Numbered in order of first citation; a number, once assigned, does not change.
   References [46]–[53] are first cited in chapters 6–7." The render's still says "cited in chapters 5–9, still to be drafted". Part
   A.5 replaces it with the draft's wording; G5 computes where [46]–[53] are first cited, which tests that sentence.
7. **Network.** doi.org, Crossref, PubMed Central, SpringerOpen and pageplace were refused in Tasks 17–18; web search works. B1's
   scope per source is whatever is reachable, stated per judgement.
8. **Development.** The Part C route scripts below were written before this commit and not run. After this commit they are
   smoke-tested with `--dry` (a few sets each, outputs under `t19/results/dry/`, not results) for crashes only; any crash fix goes in
   the artifacts commit and is listed in the results. Nothing seen in a dry run that bears on an outcome changes a criterion; it is
   disclosed in the results.
9. **Runtime.** H-13.D replays Tasks 10 and 12 (about 7 hours on 4 CPUs in Task 13); H-11.3, H-9.5 and H-13.A2 take about an hour
   each. The route runner and the replay may run concurrently on the 4 CPUs; reported runtimes are wall times under that load.

## Part A — repository sync (artifacts, before the recorded run)

1. `references.bib`: the entry `sahomasugi2016` replaced by `roberts1959` (Roberts, S. W. (1959). Control chart tests based on
   geometric moving averages. Technometrics 1(3), 239–250. doi:10.1080/00401706.1959.10489860). `register/references.yaml`: the key
   replaced, number 26 kept. `register/results.yaml`: 6.13's citation key replaced. A new chain step `python3 t19/t19_register.py`
   (after `t16/t16_register.py`) applies the key swap to the register files, so a re-run of the chain cannot bring the old key back.
2. `source/thesis_only/critical-tolerance.md`: the draft's Theorem 2.2 statement and proof (draft lines 158–165, `\[n\]` → `[n]`),
   by `t19/make_thesis_only_t19.py` (chain step replacing `t18/make_thesis_only_t18.py`'s output); thesis re-rendered.
3. `source/Stages_0_4_Source.md` §11: items 5 and 6 added, worded as the draft's §9.4 items 5 and 6. Documentation fix.
4. The appendix comparison normaliser (G6, G7) strips math delimiters `$…$` in addition to Task 18's formatting removal.
5. Re-render Appendices A, C, D and E: Appendix C's introduction as in disclosure 6; Appendix D for Tasks 1–18 at the artifacts
   commit, with the Task 18 entry as the draft's (the repository's `FAILURES_T18` already matches it), and Tasks 1–19 after the run
   (the planned Task 19 entry); Appendix E with a Task 19 row and chain step.
6. `thesis/Thesis_Draft_full.md` replaced by the attached draft, byte-identical; both sha256 values recorded.

## The checks of §6 (G1–G7)

Run script: `t19/t19_checks.py` (artifacts commit). Manual readings after the run, in `t19/results/`: `g1_citations.md`,
`g3_examples.md` and `g3_claims.md`, `g4_claims.md`, `h16d2_classification.yaml`, `h17e5_sources.md`.

### G1 — citations (B1)

- **[26] Roberts (1959).** Judged against the full text if reachable, otherwise abstract and any reproduced formula. Holds if the
  source states that the geometric moving average z_t = r·x_t + (1 − r)·z_(t−1) of observations with variance σ² has variance
  σ²·r/(2 − r) (asymptotically, or as the limit of σ²·r/(2 − r)·[1 − (1 − r)^(2t)]) or an algebraically equivalent form.
- **§6.3 identity** (draft line 1026): α²v/(1 − (1 − α)²) − αv/(2 − α) reduces to 0 in SymPy; sign argument: 1 − (1 − α)² =
  α(2 − α) > 0 for 0 < α < 2, so both sides are defined and positive; no square root occurs. Fallback seed 19001: 1,000 sets,
  α uniform on (0, 2), v log-uniform on [10⁻³, 10³], 60 digits.
- **[29] Jazwinski (1970) and [40] Anderson & Moore (1979)** against the §7.4 sentence "the error of a delayed estimate follows from
  the standard prediction step of the Kalman filter [29, 40]": each holds if the source gives the prediction (time-update) step of the
  covariance, P(k+1|k) = A P(k|k) Aᵀ + Q, or its continuous-time or continuous–discrete form (propagation of the error covariance
  between observations), so that the sentence as written is supported. Judged on contents and any reachable text.
- **[21] Yüksel & Linder (2012)** against §1.6 (draft line 85: "in stochastic control, where observation channels are themselves
  design variables [21]") and §7.1 (line 1208: "where observation channels are also treated as design variables [21]"): each holds if
  consistent with the title and abstract (observation channels optimised as design variables in stochastic control).
**Pass:** [26] holds; the identity reduces to 0 (and the fallback holds); [29] and [40] each hold; both [21] sentences hold. Each
judgement lists its scope (full text / abstract / contents / secondary source). "Cannot be determined" is not a pass.

### G2 — Theorem 2.2 (B2)

- **Text.** The draft's closing sentences ("At a tolerance equal to an interior turning-point value … iff L₊ > L₋.") against the
  repository's referee sentences in the source proof of `critical-tolerance`, after removing math markup, parentheses and
  punctuation differences; classified with Task 16's kinds (a) equivalent, (b) the draft weaker, (c) stronger, (d) contradicts.
- **Random test.** 10,000 random piecewise-monotone sequences (seed 19002): n turning points uniform in 1–8, alternating max/min with
  random first kind, values and limits L₋, L₊ integers in 0–6 consistent with strict monotonicity of every piece (so ties between
  non-adjacent values are frequent); R² = the value of a uniformly chosen interior turning point. **Rule as stated:** directions from
  the sequence (the first piece rises iff σ²(t₁) > L₋); each piece contributes nothing if R² ≥ its larger end value, the whole open
  piece if R² ≤ its smaller end value, else a one-sided part at its larger end; adjacent contributions join iff the shared turning
  value exceeds R² (so a minimum with value R² splits and a maximum with value R² contributes nothing); ℓ, u from the end pieces; All
  iff one component touching both ends. **Direct computation:** the piecewise-linear function through (0, L₋), (j, σ²(t_j)),
  (n + 1, L₊) on (0, n + 1), its set {f > R²} computed exactly in rational arithmetic as a union of open intervals, and the class
  read from the components.
**Pass:** kind (a) or (b), and 0 mismatches between rule and direct computation in 10,000 cases.

### G3 — chapter 8 (B3)

- **§8.4 examples.** Every example in the table is matched to a failure recorded in the named task's report and its attribution there
  (manual, `g3_examples.md`). Real and correctly labelled = the named task has that failure with that attribution.
- **Coverage.** Every failure line of the Appendix D render (Tasks 1–18) carries an attribution containing one of criterion, code,
  document, input, prediction; "route" and "plan's construction" count as criterion (their reports explain them so).
- **§8.2** (one persistent route disagreement, T13 C2 row 12, fault in route (ii): a sample point below its equality tolerance at an
  exact limit; and the descriptions of route (i) and route (ii)) against every task's results JSON (persisting disagreements, as T18
  F3) and `t10/classify.py`. **§8.5** (one referee pass, the whole consolidated Stages 0–4 document, 14 points, all fixed, Task 13)
  against `t13/referee_report.md` and RESULTS_t13 C4, plus every referee or external-review mention in the repository.
- **Recount.** For each task 1–18, the rows of its check table (Tasks 1–7: `verification/REPORT.md` rows of that task, as T18 F2;
  Tasks 8–18: the first table with a Verdict or Result column in the task's report); a row counts if its verdict cell, after removing
  `*`, **begins with** PASS or FAIL (so "PASS (info)" counts as a pass, as Task 2's pre-registration intends). Tasks with no counted
  row are tasks without pass criteria.
**Pass:** every §8.4 example real and correctly labelled; every Appendix D failure covered; §8.2 and §8.5 match the record; recount
151 checks and 32 failures for Tasks 1–18, and Tasks 4 and 5 without criteria.

### G4 — chapter 9 (B4)

The Task 18 A3 claim table re-run on the current §9.1–9.4: every numerical or factual claim with its source and a verdict
(`g4_claims.md`). Computed in the run: 9.3F and 17.6F from the formulas (Task 16's values 9.2875 and 17.575) and that Propositions
5.8 and 5.9 are the Bayesian-weight and misspecified-Kalman results; sup q for the Hill gain (symbolic for n = 2; numeric for
n ∈ {1.5, 3, 4} at 1,000 random (c, F, Π₀), seed 19009, to show whether "sup q > 2 ⇔ c/(FΠ₀) > 4" depends on n); the worked example
25 ≤ Π₀ < 31.475 against sup q ≤ 2; 5 × 10⁻⁴ (`t10_4.json`); Numerical result 8.2 and "the grid … missed every window"
(`t10_5.json`, narrow sub-check); 10^(−32,880,317) (`t12/RESULTS_t12.md`); 0.125 % (recomputed); open problem 2's "at most 3 …
at most 4 … 2,000 random sets per family" (`t10/RESULTS_t10.md` two-stage census); open problem 4's "is expected to split" worded as
an expectation; §9.1's attributions (Theorem 7.6 the spectral test; Theorem 7.8 sharp within the power-normalised family) against the
register statements; open problems 1–6 against the source's §11 after Part A.3. A claim with no source, or not matching it as written,
is a failure.
**Pass:** every claim has a source and matches it.

### G5 — mechanical (B5)

As T18 F5 over the whole draft up to "## Appendices": [n] resolution and first-citation order for [1]–[53] (and the chapter of first
citation of each of [46]–[53]); typed result references (Task 17's abbreviations plus "Cex."); Figure B.n against `figures.yaml`;
every "Task n" names a task 1–18 with a report; every "Tn.m" and "Tn X" names a check in task n's check table.
**Pass:** 0 unresolved [n]; order holds; 0 wrong-type references; 0 unknown figures; 0 nonexistent task or check references.

### G6 — appendices (B6)

The draft's Appendices A, C and D against the renders at the artifacts commit (Appendix D: Tasks 1–18), records compared as T18 F6
(Appendix A rows by number, C entries by [n], D task lines and failure bullets in order) after the normaliser of Part A.4 (formatting
and `$…$` removed). Titles and introductions compared and listed.
**Pass:** every record matches, apart from formatting and the Task 19 entry (absent from both at the artifacts commit). Every
difference is listed.

### G7 — sync (Part A)

(i) Occurrences of `sahomasugi2016` in every file tracked by git at the artifacts commit, excluding Task 19's own pre-registration,
check script and `t19/input/` (they name the key to search for it); the live files (bibliography, register, sources, renders) are
reported separately. (ii) The thesis render's Theorem 2.2 proof equals the draft's after normalisation. (iii) The source's §11 has 6
numbered items. (iv) Appendix A comparison: 0 differences after delimiter stripping.
**Pass:** (i) 0 occurrences (expected to fail on the ten recorded files, disclosure 5); (ii)–(iv) hold.

## Part C — re-checks of failures diagnosed but never re-checked

Run script: `t19/t19_routes.py` (and `t19/h13d_replay.py` for H-13.D), committed with this file. Every route uses the original
task's artifacts and inputs unchanged (imported or read). For each: the original criterion, the diagnosis (verbatim from the task's
report, shortened with "…") and the corrected criterion. Each is reported as **resolved** (pass), **not resolved** (fail, with a
diagnosis) or **document finding** (the diagnosis implies the thesis's claim itself should be weakened).

### H-6.C5 (Task 6, C5)
- **Original** (`verification/PREREG_t6.md`): "Peak height and location must match the t4b semi-analytic peaks reported in REPORT.md
  (… 0.09169 at 0.684, 0.08234 at 0.654, 0.04326 at 0.539, 0.01356 at 0.33) to 3 significant figures."
- **Diagnosis** (`verification/REPORT.md`): "t4b located its peaks on a grid with steps of about 0.4 % in Π, which is coarser than 3
  significant figures … the third significant figure of the t4b peak locations is a grid artefact. The correct values to 3 s.f. are
  0.683 (τ = 0.01), 0.655 (τ = 0.1), 0.538 (τ = 1), 0.33 (τ = 10)."
- **Corrected.** At λ = c = 1, Σ = 0.01, P = 1 and each τ: the peak of the Task 6 symbolic C_xx (gain cΠ/(Π + P)) located by
  root-finding on dC_xx/dΠ = 0 (mpmath, 50 digits), and the peak of the Task 4b semi-analytic var_tau located the same way. **Pass:**
  heights and locations of the two routes agree to 3 s.f. at every τ, and Task 6's recorded fine-grid peaks round to the same 3 s.f.
  The thesis prints no peak values (only §8.4's "peak positions to 3 figures from a 0.4% grid"); the claim tested is the derivation's
  agreement with Task 4b at 3 s.f.

### H-9.2 (Task 9, T9.2 ARE route)
- **Original** (`PREREG_t9.md`): "`scipy.linalg.solve_continuous_are` … ε ∈ {1e-4, 1e-6, 1e-8, 1e-10} … cubic polynomial in √ε … PASS
  (ARE) iff relative error ≤ 1e-5 in every one of the 2,001 cases."
- **Diagnosis** (`t9/RESULTS_t9.md`): "the regularised error P_ε converging to Proposition 3.1 as √ε in every failing case … the √ε
  prefactor is large … mp ARE at ε = 1e-40 matches Proposition 3.1 to 3.1e-12 (0 over 1e-5)."
- **Corrected.** The same ARE (Hamiltonian stable subspace, the diagnosis's `are_mp` definition executed unchanged) at 100 digits,
  ε = 10⁻³⁰ and 10⁻⁴⁰, on the 2,001 pre-registered cases (seed 9002). **Pass:** relative error to Proposition 3.1 ≤ 1e-5 at
  ε = 10⁻⁴⁰ in every case, and the log-slope of the gap between ε = 10⁻³⁰ and 10⁻⁴⁰ in [0.45, 0.55] wherever the gap at 10⁻³⁰
  exceeds 10⁻⁶⁰ (the thesis: "the regularisation converges as √ε … an extended-precision Riccati solution agrees").

### H-9.5 (Task 9, T9.5 monotonicity flags)
- **Original** (`PREREG_t9.md`): "V(τ): float64; bracket on a 401-point grid … `minimize_scalar` … Must be strictly decreasing along
  the grid and ≥ P … at every grid τ."
- **Diagnosis** (`t9/RESULTS_t9.md`): "The error is in the criterion (float64 resolution), not the document … 0 of 285 are real … 0 of
  13 are real."
- **Corrected.** All 400,000 pre-registered samples (2,000 sets, seed 9004, 200 τ each), V in mpmath at 50 digits (the differences
  at issue are 10⁻¹⁹–10⁻¹⁶ relative): the least of 1/(2Πτ), F and the stationary values refined by `findroot` from every local minimum
  of the 401-point grid. **Pass** (Propositions 6.8–6.9 as stated: V strictly decreasing, P < V): V strictly decreasing along every
  grid, V > P at every sample, and V never above the grid minimum by more than 10⁻¹² relative.

### H-10.1a and H-10.1b (Task 10, T10.1 two symbolic items)
- **Original** (`PREREG_t10.md`): "every item exactly 0, no numeric fallback. Route per item: `simplify`; else
  `simplify(together(expand))`; else single-√ remainder." Items (c) G(Π(G)) − G and (g) σ*²(π_R) − R².
- **Diagnosis** (`t10/RESULTS_t10.md`): "Factoring the radicand gives (G + lambda1)**2 and the expression reduces to 0 … its square
  root equals (2Σ − λR²)/R² only when R² < 2F … With R² = F/(1 + w), w > 0 … it reduces to 0. Attribution: criterion / route."
- **Corrected.** (a) G(Π(G)) − G with √((G + λ′)²) → G + λ′ (sign: sum of positives); residual 0; fallback seed 19004.
  (b) σ*²(π_R) − R² with Σ = λF and R² = F/(1 + w), w > 0 (exactly 0 < R² < F), each radicand written as Y² with Y > 0 manifest,
  and the dimensional sign argument 2F − R² > 0 because R² < F; residual 0; fallback seed 19005 (R² uniform in (0, F)), 60 digits.
  **Pass:** each item's residual reduces to 0 with its sign argument, and its fallback holds.

### H-10.5 (Task 10, pair birth)
- **Original** (`PREREG_t10.md`): "PASS iff M − m → 0 monotonically in δ and the least-squares slope of log(M − m) vs log δ lies in
  [0.4, 0.6]. *A priori note:* … the slope for M − m is expected near 1.5."
- **Diagnosis** (`t10/RESULTS_t10.md`): "Slope … = 1.5000; slope of the turning-point separation = 0.5000 … The pre-registered
  [0.4, 0.6] applies to positions, not to M − m."
- **Corrected.** Hill n = 2, λ = c = 1, Σ = 0.01, Task 10's code unchanged (`pair_birth`, `hill_count`). **Pass** (Proposition 2.7
  and its verification line): on δ = 10⁻⁶…10⁻¹², M − m → 0 monotonically, the value slope in [1.45, 1.55] and the position slope in
  [0.45, 0.55]; (M − m)/sep³ constant to 10⁻³ (the fold constant |a|/6); and on δ = 10⁻⁴…10⁻¹⁴ the fitted exponents match the printed
  1.50007 and 0.50002 at their printed digits.

### H-10.6 (Task 10, zero-limit shape)
- **Original** (`PREREG_t10.md`): "zero limits: P < 1e-6·P_max at λτ = 1e∓12 … expected to **fail** in every set."
- **Diagnosis** (`t10/RESULTS_t10.md`): "P/P_max at λτ = 1e∓12 is at least 3.99999e-06 … equals the asymptote … The supplementary check
  (P < 1e-6 P_max at λτ = 1e∓24, log-slopes ±0.5 within 1e-3) passes … P → 0 at both ends."
- **Corrected.** On the T10.6 sets (seed 10006, 1,000 sets), `t10_tau.P_rat` unchanged, 60 digits. **Pass:** P < 10⁻⁶ P_max at
  λτ = 10∓24; log-slope between λτ = 10^(∓10) and 10^(∓12) within 10⁻³ of ±0.5; and P/P_max at λτ = 10∓12 equal to
  2·10⁻⁶(Σ + λv)/√(λΣv) within 10⁻³. (The core shape parts passed in the recorded T10 run and are not re-run.)

### H-11.3 (Task 11, classes at β ≥ 2)
- **Original** (`PREREG_t11.md`): "β ≥ 2 → upper ray or Empty … route (i) = route (ii) everywhere", with the limit table giving F at
  β = 2 and the bracket ±80.
- **Diagnosis** (`t11/RESULTS_t11.md`): "β = 2: … P → 2F/(1 + √(1 + 2Σ/K)) = σ*²(λ²/K) … The pre-registered table gave F. β slightly
  above 2: … approached like τ^{2−β}; the pre-registered outer bracket x = 80 leaves P far from F."
- **Corrected.** All 129 β × 300 sets × 10 tolerances (the pre-registered draws, rng 11003), Task 11's code unchanged except the two
  corrected inputs: L₊ = σ*²(λ²/K) at β = 2 and outer bracket max(80, 50/(β − 2)) − log₁₀ λ for β > 2. **Pass** (Theorem 7.8): the
  pre-registered class rule in every classification, routes (i) and (ii) agreeing.

### H-12.A5 (Task 12, D2 coefficient)
- **Original** (`PREREG_t12.md`): "limits of the table via `sympy.limit`/series … exact 0, no numeric fallback."
- **Diagnosis** (`t12/RESULTS_t12.md`): "`sympy.limit` returns 0 … Exact route: replace e^{−2λΔt} by 0 (beyond all orders), set
  Δt = 1/t and take t → 0 … difference … 0 … O(1/Δt)." Attribution: code.
- **Corrected.** Series route on Task 12's symbolic expression (limit and `series` at t → 0⁺ after e^(−2λΔt) → 0): difference from
  c[c + 2(1 − c)FΠ₀]/Π reduces to 0. Limit sequence: 1,000 sets (seed 19003) at Δt = 10¹⁰, 10²⁰, 10⁴⁰ with 60 + 2D digits (the
  remaining cancellation is 10⁻ᴰ relative; e^(−2λΔt) is beyond all orders and not resolved). **Pass:** both reduce to 0, and the
  relative error is below 10^(−D+6) at every set and Δt.

### H-12.A7 (Task 12, minimum below F)
- **Original** (`PREREG_t12.md`): "existence of a minimum < F and the class at R² = (min + F)/2 ∈ {two rays} (or (1,1,k) recorded)",
  turning points by the T10 method with "zero tolerance 1e-40·|metric|/θ".
- **Diagnosis** (`t12/RESULTS_t12.md`): "the pre-registered zero tolerance 1e-40·|prior|/θ treats the derivative as zero once
  e^{−2λΔt} is below about 1e-40 … Scanning the sign of g instead … finds a minimum in 590 of the 590 sets … dips … between
  10^-32880317 and 10^-17."
- **Corrected.** Every D1 set of the A8 census with G > 2FΠ: the prior minimum as a − to + sign change of g = 2λ(F − P⁺) + dP⁺/dΔt
  (801-point scan of log₁₀ λΔt ∈ [−8, 8] at dps_for(λΔt) + 20 digits, 120 bisections); the dip in the factored form
  e^(−2λΔt)(F − P⁺)/F, so the zero tolerance scales with the dip (a direct evaluation would need more than 2λΔt/ln 10 digits, up to
  3.3 × 10⁷); the class at R² = (lowest minimum + F)/2 from the endpoint limits and that minimum. Symbolic prerequisite: Task 12's
  prior equals F + e^(−2λΔt)(P⁺ − F). **Pass** (Proposition 6.20, prior half; the avg half passed in the recorded T12 run, 907/907):
  a minimum below F in every set, every dip positive, ℓ = u = 1 and not All in every set.

### H-12.A8 (Task 12, regression values)
- **Original** (`PREREG_t12.md`): "post has a single maximum with value within 2% of 0.166 at Δt within a factor 2 of 1; avg crosses F
  at Δt within a factor 1.5 of 50 … *Expected to fail.*"
- **Diagnosis** (`t12/RESULTS_t12.md`): "attribution: prediction — the prompt's quick-check numbers … maximum 0.204573 at Δt = 2.4645
  … avg crosses F at Δt = 100 … minimum 0.0099875."
- **Corrected.** Reference values recomputed by new code written from the thesis's §6.3 formulas only (no Task 12 code; derivatives by
  numerical differentiation), at int(2λΔt_max/ln 10) + 60 digits. **Pass:** the §6.5 worked example as printed: post(0⁺) = 0.09;
  one turning point, a maximum 0.20457 at Δt = 2.4645; post → 0; avg crosses F once, at Δt_E = 100 to 20 significant digits; one
  turning point after Δt_E, a minimum 0.0099875 at Δt = 200; dip 0.125 %; avg < F after Δt_E and → F.

### H-13.A-sym (Task 13, Part A, 2 of 68 symbolic items)
- **Original** (`PREREG_t13.md`): "`simplify`; else `simplify(together(expand))`; else factor radicands then simplify; exact 0 only.
  Sign claims via identities with manifestly signed right sides."
- **Diagnosis** (`t13/RESULTS_t13.md`): "The sign of −sFr (A1 item 2) is not decided by SymPy's assumptions because 1 − e^{−2x} is not
  known positive; the A2 identity with sinh is not reduced … Both reduce to 0 after `rewrite(exp)` / an explicit positive series."
- **Corrected.** Item 2: −sFr = −(Fk/x)e^(−2x)(e^(2x) − 1) reduces to 0, and e^y − 1 has positive series coefficients from y¹ (sign
  argument). Item 6: the identity after `.rewrite(exp)` reduces to 0. No square roots (recorded). Fallback seed 19006: 1,000 sets,
  x ∈ [10⁻⁸, 50], at 60 + ⌈−2 log₁₀ x⌉ + ⌈4x/ln 10⌉ digits. **Pass:** both reduce, the series is positive, the fallback holds and
  −sFr < 0 at every set.

### H-13.A2 (Task 13, A2 numerical)
- **Original** (`PREREG_t13.md`): "10,000 sets … mpmath 100 digits … **Pass:** all symbolic items and 0 numerical failures."
- **Diagnosis** (`t13/RESULTS_t13.md`): "The auxiliary cross-check P̄(μ) = P̄(M) to 1e-80 … failed in 277 sets, all at λΔt ≥ 26.6,
  because F − M cancels about 2x/ln 10 digits. With 100 + 2x/ln 10 + 30 digits all agree." Attribution: code.
- **Corrected.** All 10,000 sets (seeds 13001·100000 + i), the pre-registered links by `a12_job` unchanged at 100 digits, the
  cross-check at 100 + ⌈2x/ln 10⌉ + 30 digits. **Pass:** 0 link failures and the cross-check within 10⁻⁸⁰ in every set.

### H-13.C2-12 (Task 13, C2 row 12)
- **Original** (`PREREG_t13.md`): "route (ii) in float64 … every flagged case … re-run in mp at dps 60. **Pass per row:** 0 persisting
  classes outside the row's stated set, 0 persisting route disagreements, and every class in the stated set observed at least once."
- **Diagnosis** (`t13/RESULTS_t13.md`): "122 persisting disagreements … all at R² exactly L₋ on increasing curves whose approach to L₋
  is exponentially flat … route (ii) tests one point … where f − R² is below its 1e-40 relative equality tolerance." Attribution: code.
- **Corrected.** The row's 1,000 sets and 100 tolerances as pre-registered (seed 13112), Task 13's code for draws, analysis and first
  pass; every flagged case re-run at 400 digits with an equality tolerance of 10⁻³⁰⁰ relative in both routes (route (ii) re-implemented
  line for line with the tolerance as a parameter). **Pass:** the C2 per-row rule.

### H-13.D (Task 13, reproduction)
- **Original** (`PREREG_t13.md`): "`reproduce_all.sh` runs, in a clean checkout … **Pass:** for each of `REPORT.md` and `RESULTS_t9`…
  `RESULTS_t12`, after masking runtimes, timing totals, commit hashes, dates … every verdict cell … identical, and … every other number
  is identical or … agrees to relative 1e-6."
- **Diagnosis** (`t13/RESULTS_t13.md`): Task 10 "(attribution: code, Task 10's run script). t10/run_t10.sh omits t10_realize_diag.py";
  Task 12 "all on the provenance runtime line … (attribution: criterion; the masking covers runtime numbers but not the list of script
  names …)". Tasks 8, 9 and 11 passed and are not re-run.
- **Corrected** (`t19/h13d_replay.py`). A clean worktree of 7195070 (the Task 13 replay's commit): Task 10's run script, then the
  omitted `t10_realize_diag.py`, then `make_results_t10.py cbe96fe`; Task 12's run script. `compare_repro.compare` unchanged, with the
  provenance line "Runtime per script (s): …" masked in both texts. **Pass:** both reports with identical verdicts and 0 issues.
  (Appendix E already notes that `run_t10.sh` omits the diagnosis script; the one-command claim of `reproduce_all.sh` is not changed.)

### H-14.C4 (Task 14, paper render reproduces v1)
- **Original** (`PREREG_t14.md`): "`Stages_0_4_Paper2.md` equals `archive/Stages_0_4_Consolidated_v1.md` except for: (a) numbers
  shifted by the split of 5.14 … (b) the split itself; (c) the text of matrix rows 25–26 … Pass: no "other" hunk."
- **Diagnosis** (`t14/RESULTS_t14.md`): "All 7 "other" hunks are the excess identity's type, printed from the register." Task 15's
  prompt: "Excess identity is a Corollary … accepted for both renders."
- **Corrected.** At the Task 14 artifacts commit 45b0058 (clean worktree), `t14_checks.c4` run unchanged, its hunks re-categorised
  with (d) the excess identity's type (a hunk whose lines become equal after "Corollary" → "Proposition", on lines naming the excess
  identity or "Corollary 4"). **Pass:** 0 numbering mismatches and no hunk outside (a)–(d).

### H-14.C10 (Task 14, dry-run resolver)
- **Original** (`PREREG_t14.md`): "every repository file named by a string literal … resolved against `classification/` … Pass: 0
  missing paths."
- **Diagnosis** (`t14/RESULTS_t14.md`): "9/9 flagged paths resolve when built the way their scripts build them; attribution: code (the
  dry run's literal resolver)."
- **Corrected.** Task 15's resolver (`t15_checks.c13`, unchanged), which builds each path the way its script does, on the current
  repository. **Pass:** 0 unresolved. (Task 15's C13 passed with it, on 89 paths; Task 18's inventory still listed T14 C10 as
  diagnosed, which this check addresses.)

### H-16.D1 (Task 16, D1 items 2(b) and 9)
- **Original** (`PREREG_t16.md`): "An identity holds if the difference … reduces to 0 by any of: `simplify`; `factor(radsimp(·))`;
  `simplify` after `sqrtdenest`/`powsimp` … **Pass:** all 9 items hold."
- **Diagnosis** (`RESULTS_t16.md`): "Item 2(b) asked SymPy's assumption system whether −λ + √(λ² + 2ΣΠ) is positive; it returns None …
  Item 9's residual contains √(R⁴ + 4d(R² + d)) = R² + 2d … a square root of a square that none of the three pre-registered routes
  denests." Attribution: code.
- **Corrected.** 2(b): the derivative identity; product of the numerator's roots −2ΣΠ < 0 (exactly one positive root); G⋆ is that root
  (identity); G⋆ > 0 because (λ² + 2ΣΠ) − λ² = 2ΣΠ > 0 and √(λ²) = λ; numerically, 1,000 sets (seed 19007), exactly one positive real
  root equal to G⋆ to 10⁻⁴⁰. 9: with Σ = λ(R² + d), d > 0, the radicand is (R² + 2d)² up to a positive factor, R² + 2d > 0, residual
  0; fallback seed 19008. **Pass:** both items hold.

### H-16.D2 (Task 16, D2 statements 3.1 and 3.5)
- **Original** (`PREREG_t16.md`): "each pair is read and every difference … recorded … with … one kind: (a) equivalent; (b) the draft is
  weaker; (c) the draft is stronger; (d) the draft contradicts the repository … **Pass:** no difference of kind (c) or (d)."
- **Diagnosis** (`RESULTS_t16.md`): "For 3.1 and 3.5 the draft's statement includes conclusions that the repository states in other
  results … The criterion counts a correct, proved strengthening the same as an unproved one." The thesis render now carries the
  draft's statements as thesis-only imports (Task 17), never re-compared.
- **Corrected.** The thesis render's statements of Propositions 3.1 and 3.5 against the current draft's (extraction in the run;
  reading after it, `h16d2_classification.yaml`). **Pass:** no difference of kind (c) or (d).

### H-17.E5 (Task 17 E5 / Task 18 F1, [47])
- **Original** (`PREREG_t18.md` F1): "both describe [47] as about time-correlated **model error** in Kalman smoothing, consistent with
  Task 17's evidence"; the recorded sub-check searched a scope that included Appendix D.
- **Diagnosis** (`RESULTS_t18.md`): "[47]: diagnosed" (the search scope included Appendix D; attribution: code).
- **Corrected.** Scope stated in advance: the two body sentences only (§6.2, draft line 952; §7.3, line 1282), judged against [47]'s
  title and abstract (Ren, Amezcua & van Leeuwen 2021, QJRMS 147, 573–588) as found by web search. **Pass:** both sentences
  consistent with the title and abstract.

### Covered by the G checks
- **H-18.F2** (counts): verdict of G3's recount sub-criterion (151 and 32, rule above).
- **H-18.F3** (§8.5 referee sentence): verdict of G3's §8.5 sub-criterion.
- **H-18.F6** (appendices): verdict of G6.
- **H-18.F1-21** ([21] in §1.6): verdict of G1's §1.6 [21] judgement.

## Part D — inventory and recount (reported, not pass/fail)

`classification/OPEN_ITEMS.md` rewritten after the run, same format. An item is **resolved** only if a pre-registered check in
Tasks 1–19 resolved it. Conjecture 6.22, Proposition 6.20's dependence on it, the open problems, the numerical results and external
review stay open. "Rough-draft chapters 8–9" is closed only if G3 and G4 pass. Recount through Task 19 by task: checks with a verdict
(the G3 rule; for Task 19, every row of its check table with PASS or FAIL, G1–G7 and each H-* row, the four covered H-18 rows
included), failures, tasks without criteria, and the failures of Tasks 1–19 by attribution.

## Part E — Conjecture 6.22, exploratory (reported, not pass/fail)

Time-boxed to about two hours of work, run while the long checks run. Approaches, in order: (1) the derivative of each D1 metric along
Δt written as an exponential polynomial in Δt over a positive denominator, and a bound on its sign changes (a Descartes / Pólya-type
rule for exponential sums, or a Wronskian chain); (2) if that does not close, a computer-assisted argument on a compact normalised
parameter region with endpoint asymptotics, as far as the time allows. Reported: what was achieved, what remains, any counterexample.
The conjecture's status is not changed.

## Report

`classification/RESULTS_t19.md`: commits (pre-registration, artifacts, results); the check table with outcomes and runtimes, every
H-* included; diagnoses; files changed; both thesis sha256 values; **For the author** 1–7 (item 6, E1, records that E1 was dropped).
Attachments: `RESULTS_t19.md`, `OPEN_ITEMS.md`, Appendices A, C, D and E.
