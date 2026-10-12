# Results — Task 18: final collection (chapters 8–9, the Task 17 fixes, last open items, archive)

- Pre-registration: `classification/PREREG_t18.md`, commit **97e1889**.
- Artifacts checked: commit **f77ab8f**. F1–F7 ran once on it (8 s; `t18/results/t18_checks.log`, `.time`).
- Results: raw outputs **1beb7d6**; manual readings, diagnosis and `OPEN_ITEMS.md` **4ef7286**; this report follows.
- Archived thesis: `thesis/Thesis_Draft_full.md`, sha256 **f1b8ecd345955975c9db6543bf5b69d2e060073422f24c68a222777d185323b6** (byte-identical to the input).

## Checks

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| F1 Task 17 fixes (A1) | **FAIL** | 4 of 6 resolved in the recorded run: Corollary 7.4's proof resolved, β count resolved, §6.7 label resolved, [47] sentences **not resolved**, [21] sentence **not resolved**, Proposition 6.13's P⁻ < F resolved; f(F) − F²a² reduces to 0 | 6.62 |
| F2 Chapter 8 counts (A2) | **FAIL** | recorded recount 143 checks, 28 failed, no criteria [4, 5]; 144 when Task 2's 'PASS (info)' row is read as the rule says (code); every §8.4 example a real failure of the named task; every Appendix D failure maps | 0.0 |
| F3 Chapter 8 claims (A2) | **FAIL** | §8.2 matches (one persistent disagreement: Task 13 audit row 12, route (ii)); §8.5 does not (Task 13 C4's referee read the whole document) | 0.16 |
| F4 Chapter 9 claims (A3) | **PASS** | 25 claims, each sourced and matching; notes on the Hill gain and on open problems 5–6 (not in the repository's §11) | 0.0 |
| F5 Mechanical (A4) | **PASS** | 49 citation groups, 0 unresolved, order [1]–[53] holds; 451 typed references, 0 wrong; 12 figure references; 128 task and 50 check references, 0 nonexistent | 0.2 |
| F6 Appendices (B.5) | **FAIL** | records A 82/82 (1 difference), C 53/53 (0), D 46/46 (3) | 0.01 |
| F7 Thesis render consistency (B.3) | **PASS** | 0 lettered references to Theorem 2.2 | 0.0 |

**Pre-registered checks that FAIL:** F1, F2, F3, F6. Each stays a failure; diagnoses below.

## Diagnoses

- **F1 (attribution: code and document).** [47]: the recorded search for sentences citing [47] ran over the whole draft and picked up Appendix D's quotation of the Task 17 finding; restricted to chapters 1–9, both sentences (§6.2, §7.3) say "time-correlated model error" (`t18_diag.json`; code). [21]: §7.1 now cites [21] for observation channels as design variables, but §1.6 (line 85) still says monotonicity under garbling "extends to sequential experiments [20] and stochastic control and teams [21–23]" (document; not resolved). The other four fixes are resolved, and f(F) = F²a² reduces to 0 by `simplify`, with 0 of 1,000 counterexamples to M < F at up to 39,399 digits (seed 18001).
- **F2 (attribution: code).** The recount parser required a verdict cell equal to "PASS" and skipped Task 2's T2.1c ("PASS (info)"), giving 143. The pre-registered rule counts cells that say PASS or FAIL; so read, the total is 144, with 28 failed and Tasks 4 and 5 without criteria, as the draft says. The §8.4 mapping holds (`f2_examples.md`).
- **F3 (attribution: document).** §8.5 says the only referee pass was on Theorem 7.6 (Task 13). The record is an independent referee pass (a separate agent, inside the project) over the whole consolidated Stages 0–4 document, 14 points, all valid and fixed (`t13/referee_report.md`, RESULTS_t13 C4); Theorem 7.6 was among the results read. This was known from the inventory and disclosed in the pre-registration (disclosure 3).
- **F6 (attribution: code and document).** Appendix A: one row differs only by math delimiters ("$n = 2$" vs "n = 2"), formatting the normaliser did not strip (code). Appendix D: the draft rewrote three Task 17 failure lines after the fixes ("omits" → "omitted … (the corollary holds; the proof was completed)", "M < F" → "P⁻ < F", "spans" → "spanned", "makes" → "made"); the repository's lines are the record as written at Task 17 (document). Appendix C: all 53 entries match.

## Disclosure

- Before the recorded run each check was run once with its output discarded, to see that it ran, and F6's parsers and F4's extractions were checked to find records on both sides. No code was changed after that.
- The Task 13 referee record (F3) was read while taking stock, before the pre-registration (disclosure 3).
- While building Part B.3, `register/render.py`'s block rule was widened so that a multi-paragraph statement (Theorem 2.2's) is replaced through its proof; the Task 17 overrides render unchanged.
- F2's §8.4 mapping, F3, F4 and A5 are manual readings after the recorded run (`t18/results/`).

## Files changed

- `source/Stages_0_4_Source.md`: Theorem 7.8's label, "37 values of β" → "129 values of β (β = k/20, k = −40, …, 80, plus {0, 2} ± {10⁻⁶, 10⁻³})" (record correction); Proposition 2.7's proof, (4/3)a(bδ)^(3/2) → (4/3)|a|(bδ)^(3/2) (documentation fix).
- New `source/thesis_only/critical-tolerance.md` (the draft's Theorem 2.2, parts (1)–(4)); `register/thesis_overrides.yaml` (replace critical-tolerance); `register/render.py` (block rule through the proof).
- New `thesis/Thesis_Draft_full.md` (archive, not rendered).
- Renders: `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (the β label and |a|), `Appendix_A_Register.md`, `Appendix_C_References.md` (unchanged by this task), `Appendix_D_Verification.md` (Tasks 1–18), `Appendix_E_Reproduction.md` (T18 row, chain step).
- `t15/make_appendix_de.py` (T18 entry, chain); new `t18/` scripts, inputs and results; `OPEN_ITEMS.md`.

## For the author

### 1. A1: the Task 17 fixes

| Fix | Verdict | Evidence |
|---|---|---|
| Corollary 7.4's proof | resolved | cites σ⋆² = 2Σ/(λ + √(λ² + 2ΣΠ)) → 0 (Proposition 3.5) to exclude All, and Theorem 5.1 for the last clause; SymPy limit 0 |
| β count | resolved | the draft says 129; `t11_3.json` has 129 distinct β. The repository's label is corrected in Part B.1 |
| §6.7 label | resolved | "Prop. 6.10, Cex. 6.11, Prop. 6.12": types match the register |
| [47] sentences | resolved (post hoc) | §6.2 and §7.3 both say "mis-specified time-correlated model error"; the recorded sub-check failed on scope (code) |
| [21] sentence | **not resolved** | §7.1 is fixed ("where observation channels are also treated as design variables [21]"); §1.6 still cites [21–23] for monotonicity under garbling |
| Proposition 6.13's P⁻ < F | resolved | the proof now states f(F) = F²a² > 0; f(F) − F²a² reduces to 0; f is monic with f(0) = −sFr < 0; numerical: 0 of 1,000 |

### 2. A2: chapter 8 counts

| Task | Checks with a verdict | Failed |
|---|---|---|
| 1 | 12 | 0 |
| 2 | 3 | 0 |
| 3 | 8 | 0 |
| 4 | 0 | 0 |
| 5 | 0 | 0 |
| 6 | 6 | 1 |
| 7 | 15 | 0 |
| 8 | 5 | 0 |
| 9 | 7 | 2 |
| 10 | 10 | 4 |
| 11 | 11 | 1 |
| 12 | 13 | 3 |
| 13 | 15 | 5 |
| 14 | 11 | 3 |
| 15 | 13 | 2 |
| 16 | 8 | 3 |
| 17 | 7 | 4 |
| **Total** | **144** (143 if T2.1c's "PASS (info)" is excluded) | **28** |

Tasks 4 and 5 have no pass criteria. Corrections chapter 8 may need:
- §8.4, "Code" row: T10's and T13's SymPy failures and T9.5's double-precision flags are attributed to the criterion ("criterion / route", "criterion") in their reports, not to code.
- §8.4, "four truncated worked values (T13)": Task 13 records four occurrences of one truncated value (0.0099504 for 0.0099505).
- §8.5: the Task 13 referee pass covered the whole consolidated document (14 points), not only Theorem 7.6.
- §8.2 is correct.

### 3. A3: chapter 9

| # | § | Claim | Source | Verdict |
|---|---|---|---|---|
| 1 | 9.1 | The shape of a failure set is fixed by the endpoint limits, turning-point values and two approach directions | Theorem 2.2(4) | matches |
| 2 | 9.1 | Every white-noise relay variance is σ²/F = 𝒱(ν, q) along a path; floor crossing q = 2; optimal filter = lower envelope | Theorem 3.2, Corollary 3.3, Proposition 3.5 | matches |
| 3 | 9.1 | Along precision the model forbids only a variance below the optimum; further restrictions belong to the gain family | Theorem 5.1, Corollaries 5.2–5.3, §5.2–5.5 | matches |
| 4 | 9.1 | Causal ordering ⇒ optimal filter cannot do worse; no optimal windows along ordered sweeps | Theorem 7.2, Corollary 7.3 | matches |
| 5 | 9.1 | Spectral test for additive Gaussian noise; sharp in the power family; sufficient not necessary; must be causal | Theorem 7.6, Theorem 7.8, Proposition 7.13, Counterexample 7.12 | matches |
| 6 | 9.1 | Diagnostic: window, two rays or mixed class along an ordered sweep certifies a miscalibrated filter | Corollary 7.4 | matches |
| 7 | 9.2 | Window conditions κ > 2 (Bayesian weight), F′ > 2F (misspecified Kalman), g > 2F (capped), ρ > 2 or λ′ < λ/2 (moving floor, relative tolerance) | Propositions 5.8, 5.9, 5.10, 6.25, 6.26 (source statements in t18_checks.json) | matches |
| 8 | 9.2 | "Below that threshold the relay never windows" | the same propositions: strictly decreasing (5.8, 5.9, 5.10) or no window (6.25, 6.26) below the threshold | matches for the families listed. The Hill gain is not listed: its window condition is c/(FΠ₀) > 4, i.e. sup q > 2 (Theorem 3.4), and it has a window component in the mixed class below that (Proposition 5.13); "all have the same form" holds for the listed families only |
| 9 | 9.2 | Peak 9.3F (Bayesian weight) and 17.6F (misspecified Kalman) at over-weighting ratio 100 | recomputed: 9.2875272, 17.575054 (both round as printed); §5.3 text after Proposition 5.9 | matches; the parenthesis cites Proposition 5.9 only, but the Bayesian value comes from Proposition 5.8's formula (same paragraph of §5.3) |
| 10 | 9.2 | Hill mixed band median relative width 5 × 10⁻⁴ | `t10_4.json` band_rel_median 4.98 × 10⁻⁴; Proposition 5.13's paragraph | matches |
| 11 | 9.2 | Windows of relative width 10⁻⁸ occur | Numerical result 8.2 (source: 20/20 curves, 55 windows; T10.5) | matches |
| 12 | 9.2 | A grid-based check would miss them | Numerical result 8.2: a 10⁴-point log grid found none | matches |
| 13 | 9.2 | Prior dips as small as 10^(−32,880,317) | `t12/RESULTS_t12.md` ("between 10^-32880317 and 10^-17") | matches |
| 14 | 9.2 | Time-averaged dip 0.125 % in the worked example | recomputed: avg(200) = 0.0099875, dip 0.125 % (Task 17 E3 also) | matches |
| 15 | 9.3 | Scalar, stationary, linear scope | §1.7 | matches |
| 16 | 9.3 | Ornstein–Uhlenbeck signal throughout; chapter 2 applies to any curve | §3.1, §7.1 setting; Theorem 2.2's hypotheses C1–C6 | matches |
| 17 | 9.3 | Theorem 7.6 needs additive stationary Gaussian noise; Theorem 7.2 does not | statements of 7.5–7.6 and 7.2 | matches |
| 18 | 9.3 | Conventions: Σ half the diffusion intensity; samples carry 1/(ΠΔt); absolute or relative tolerance; time average primary; Theorem 6.19 depends on the noise scaling | Proposition 3.1 and §1.7; §6.3; §6.6; §6.3; §6.4 ("The statement depends on the scaling r = 1/(ΠΔt)") | matches |
| 19 | 9.3 | One parameter at a time; Theorem 2.2 does not describe multi-parameter regions | C1 (domain an interval) | matches |
| 20 | 9.4 (1) | Conjecture 6.22; census found no exception; mixed exponential rates defeat polynomial methods | repository §11 item 1 | matches |
| 21 | 9.4 (2) | Bound on turning points of two-stage sums; Corollary 5.4; natural sums open | repository §11 item 2 | matches (the draft omits the evidence line "at most 3 and 4 turning points in 2,000 sets") |
| 22 | 9.4 (3) | Necessary condition for monotone optimal error | repository §11 item 3 | matches |
| 23 | 9.4 (4) | Two-state α–β filter; decoupled multivariate splits; mixing case open | repository §11 item 4 | matches |
| 24 | 9.4 (5) | A gain that tracks correlation time: every gain along τ is set by precision alone | §6.1 ("The relay's gain is set by precision alone") | sourced in the draft; **not in the repository's open-problems section** |
| 25 | 9.4 (6) | Applications: none worked out | §1.7 ("applied relevance studies, which chapter 9 lists as future work") | sourced in the draft; **not in the repository's open-problems section** |

**Verdict.** Every claim has a source in the repository or the draft and matches it. Two notes: the "same form" claim (8) holds for
the families listed, not for the Hill gain; open problems 5 and 6 are new relative to the repository's §11 (which has items 1–4).

### 4. A4: references

No broken reference: 49 citation groups resolve and [1]–[53] first appear in order; 451 typed references (with "Cex.") have the right type; 12 figure references exist; 128 "Task n" and 50 "Tn.m"/"Tn X" references name existing tasks and checks.

### 5. A5: [26] and [29]

**Access.** Full texts could not be fetched from this session: `pmc.ncbi.nlm.nih.gov`, `springerplus.springeropen.com` and
`api.pageplace.de` are refused (curl: CONNECT 403; the fetch tool: host not resolved), as are doi.org and Crossref (Task 17). The
session's web search (extended mode, 2026-10-12) was used instead; its summaries are paraphrased below.

## [26] Saho, K. & Masugi, M. (2016). α–β–γ tracking filters using acceleration measurements. SpringerPlus 5, 309. doi:10.1186/s40064-016-1960-8

- **What the source contains (from the search summaries):** a short report proposing two α–β–γ filters that use acceleration
  measurements (position–acceleration-measured, PAM; position–velocity–acceleration-measured, PVAM), with performance indices
  (steady-state tracking errors) derived from the authors' earlier work on position–velocity-measured filters, and numerical
  comparisons with the position-only-measured α–β–γ filter; derivations in its Additional file 1.
- **Does it state or use α/(2 − α) (or L/(2 − L)) for an exponentially weighted or α-type filter?** **Cannot be determined.** The
  summaries show no α-filter noise-reduction ratio and no exponentially weighted average; the extracted formulas were garbled.
  Its subject (three-state trackers with acceleration measurements) makes the scalar α-filter factor at most incidental.
- **Candidate standard references for "the variance factor α/(2 − α) of an exponentially weighted average":**
  1. Roberts, S. W. (1959). Control chart tests based on geometric moving averages. *Technometrics* 1(3), 239–250.
     doi:10.1080/00401706.1959.10489860 (DOI confirmed by the search from a published reference list). The EWMA control chart; the
     asymptotic EWMA variance factor λ/(2 − λ) is the standard result attributed to it (the search confirmed the factor from a
     secondary source, not from Roberts's text).
  2. Kalata, P. R. (1984). The tracking index: a generalized parameter for α–β and α–β–γ target trackers. *IEEE Transactions on
     Aerospace and Electronic Systems* AES-20(2), 174–182. DOI not confirmed from this session. The standard reference for steady-state
     α–β(–γ) tracker indices; whether it prints the α-filter ratio α/(2 − α) was not confirmed.

## [29] Jazwinski, A. H. (1970). Stochastic Processes and Filtering Theory. Mathematics in Science and Engineering 64. Academic Press.

- **What the source contains (from the search summaries):** nine chapters; Chapter 7 "Linear Filtering Theory" (pp. 194–265), with
  sections Introduction, Continuous–Discrete Filter, Discrete Filter, Continuous Filter, Observability and Information; the book
  introduces filtering, prediction and smoothing as problems, and a review says the linear chapters discuss "filtering and
  prediction". No section titled "prediction" was returned, and no statement about delayed estimates.
- **Does it give the prediction-error covariance for an estimate of a delayed state, or the prediction step in a form that covers
  it?** **Cannot be determined from the available text.** The continuous–discrete filter's between-observation covariance
  propagation is the prediction step that covers the delayed-state case (P(t | t − d) = e^(−2λd)P + F(1 − e^(−2λd)) for the scalar
  OU state), but the table of contents and review do not show it explicitly.
- **Candidate standard references for the prediction covariance:**
  1. Anderson, B. D. O. & Moore, J. B. (1979). *Optimal Filtering*. Prentice-Hall, Englewood Cliffs (ISBN 0-13-638122-7); Dover
     reprint 2005 (ISBN 0-486-43938-0). No DOI. Covers the discrete Kalman filter, prediction and smoothing (the search confirmed
     the bibliographic details and the topics, not the specific equation).
  2. Gelb, A. (ed.) (1974). *Applied Optimal Estimation*. MIT Press (ISBN 0-262-57048-3). No DOI. Standard treatment of
     covariance propagation between measurements. Not checked by search in this session.

The bibliography and the register are unchanged; the decision is the author's.

### 6. Part B: what changed in the repository

- Theorem 7.8's label now says 129 values of β, with the composition of `PREREG_t11.md`.
- Proposition 2.7's proof (repository source, paper render) now has (4/3)|a|(bδ)^(3/2), matching the thesis text.
- The thesis render's Theorem 2.2 is the draft's, with parts (1)–(4); no lettered reference to it remains (F7). Note: the draft's proof of Theorem 2.2 does not include the closing sentences the Task 13 referee (point 10) added to the repository's proof (the rule at a tolerance equal to an interior turning-point value; approach directions determined by the sequence). The thesis render now shows the draft's proof; the paper render keeps the repository's.
- `thesis/Thesis_Draft_full.md` archived (sha256 f1b8ecd345955975c9db6543bf5b69d2e060073422f24c68a222777d185323b6).
- Appendices A, C, D (Tasks 1–18) and E (Task 18 row and chain step) re-rendered. Their introductions differ from the draft's, which is not a record difference; one is stale: the render's Appendix C introduction still says references [46]–[53] "are cited in chapters 5–9, still to be drafted" (Task 15 wording), while the draft says "first cited in chapters 6–7".

### 7. The closing inventory (`OPEN_ITEMS.md`)

Everything not settled when Task 18 closed, with its status and where it is recorded. An item is marked **resolved** only when a
pre-registered check in Tasks 1–18 resolved it; a post-hoc diagnosis, however convincing, leaves it **diagnosed, not re-checked**.

## 1. The conjecture and the open problems

| Item | Status | Recorded in |
|---|---|---|
| Conjecture 6.22: sampled relays D1–D3 have at most two turning points along Δt in every metric | **open** (no proof; no counterexample in Task 12's census, 6,000 sets × 3 metrics, or Task 13's audit) | register 6.22 (status conjecture); `source/Stages_0_4_Source.md` §11 item 1; draft §9.4(1) |
| Proposition 6.20 assumes C2 for D1's prior and avg curves (finitely many turning points), which Conjecture 6.22 would give | **conditional** on an unproved hypothesis | Proposition 6.20's statement; Task 13 C4 referee point 7 |
| Open problem: a bound on turning points of two-stage sums | **open** (at most 3 and 4 observed in 2,000 sets each) | source §11 item 2; draft §9.4(2); Numerical result 5.15 |
| Open problem: a necessary condition for monotone optimal error beyond the power family | **open** | source §11 item 3; draft §9.4(3) |
| Open problem: the fixed α–β filter and multivariate models (mixing case) | **open** | source §11 item 4; draft §9.4(4) |
| Open problem: a gain that tracks correlation time | **open**; in the draft only, not in the repository's §11 | draft §9.4(5); RESULTS_t18 F4 |
| Open problem: applications | **open**; in the draft only, not in the repository's §11 | draft §9.4(6), §1.7; RESULTS_t18 F4 |

## 2. Numerical results: evidence, not proof

| Item | Status | Recorded in |
|---|---|---|
| Numerical result 5.15 (two-stage gains: (max, min, max) in 7 of 2,000; (min, max, min, max) in 63 of 2,000) | numerical | register 5.15; T10.3, T13 C2 rows 8–9 |
| Numerical result 6.21 (census of sampled relays; class lists per family and metric) | numerical | register 6.21; T12 A8, Part C; T13 C2 rows 24–32 |
| Class lists of the sampled relays (synthesis-matrix rows 24–32): excess sets and limits proved, full class sets not | numerical | draft §8.5; `register/matrix.csv` |
| Numerical result 8.1 (blind searches: 10⁶ and 4.4 × 10⁶ classifications; Task 13 audit) | numerical | register 8.1; T10.7, T12 Part C, T13 C2 |
| Numerical result 8.2 (windows of relative width 10⁻⁸ need root-finding) | numerical | register 8.2; T10.5 |

## 3. Citations not settled

| Item | Status | Recorded in |
|---|---|---|
| [26] Saho & Masugi 2016, cited (§6.3) for the variance factor α/(2 − α) of an exponentially weighted average | **undetermined**: full text unreachable; summaries show α–β–γ trackers with acceleration measurements, no α/(2 − α). Candidate replacements: Roberts 1959 (doi:10.1080/00401706.1959.10489860), Kalata 1984. Author's decision | T17 E5 (S1); `t18/results/a5_sources.md` |
| [29] Jazwinski 1970, cited (§7.4) for the prediction covariance of a delayed estimate | **undetermined**: contents show Chapter 7 "Linear Filtering Theory" with a continuous–discrete filter section; the delayed-state statement not confirmed. Candidates: Anderson & Moore 1979; Gelb 1974. Author's decision | T17 E5 (S12); `t18/results/a5_sources.md` |
| [21] still cited, as "[21–23]", for monotonicity under garbling in §1.6 (fixed in §7.1, not in §1.6) | **open** (document) | RESULTS_t18 F1 |
| [28] dated 1968 in the bib (journal version); the search found the 1967 Harvard report of the same work | noted, not an error | RESULTS_t17, For the author 5.7 |

## 4. External review

| Item | Status | Recorded in |
|---|---|---|
| No result has had review outside the project | **open** | draft §8.5 |
| One independent referee pass inside the project (a separate agent) over the whole Stages 0–4 consolidated document, 14 points, all fixed; Theorem 7.6 among the results read | done (Task 13 C4); the draft's §8.5 describes it as a pass on Theorem 7.6 only | `t13/referee_report.md`; RESULTS_t13 C4; RESULTS_t18 F3 |

## 5. Rough-draft text

| Item | Status | Recorded in |
|---|---|---|
| Chapter 8 (Verification) | **rough draft**; checked in Task 18 F2–F3: counts match post hoc (144, 28, Tasks 4 and 5); §8.4's "Code" row holds three failures the reports attribute to the criterion; §8.4's "four truncated worked values" are four occurrences of one value; §8.5's referee sentence does not match the record | draft §8; RESULTS_t18 |
| Chapter 9 (Discussion and Limits) | **rough draft**; checked in Task 18 F4: every claim sourced and matching; the "same form" window claim holds for the listed families (not the Hill gain); open problems 5–6 are new relative to the repository | draft §9; RESULTS_t18 |
| Draft's Theorem 2.2 proof (now in the thesis render) omits the closing sentences the Task 13 referee added to the repository's proof (the rule at an interior critical tolerance; approach directions determined by the sequence) | **open** (document; the paper render keeps the repository's proof) | RESULTS_t18, For the author 6 |

## 6. Checks that failed and were not resolved by a later check

Each failure below is recorded with its diagnosis in its task's report and in Appendix D. "Diagnosed" means the report attributes
it and, where relevant, shows the claim holds; no later pre-registered check re-ran it.

| Task | Failure | Attribution | Status |
|---|---|---|---|
| 6 | C5 peak locations to 3 s.f. | criterion | diagnosed |
| 9 | T9.2 ARE route; T9.5 monotonicity flags | criterion | diagnosed |
| 10 | T10.1 symbolic (2 items); T10.5 pair birth; T10.6 zero-limit shape | criterion / route; criterion; criterion | diagnosed |
| 10 | T10.2 A1.3 as specified | criterion (plan's construction) | **resolved** by T10.2 A1.3 supplementary (PASS) |
| 11 | T11.3 classes | criterion | diagnosed (limits corrected in the diagnosis) |
| 12 | Symbolic A5 (sympy.limit); A7 minimum below F; A8 regression | code; criterion; prediction | diagnosed |
| 13 | Part A symbolic (2 of 68); A2 numerical; C2 row 8; C2 row 12; D reproduction | criterion / route; code; document; code; code / criterion | diagnosed (row 8 led to Proposition 5.14, proved in Task 13) |
| 13 | C1 numbers, first run | document, code | **resolved** by C1 after the fixes (PASS) |
| 14 | C4 paper render reproduces v1 | criterion | diagnosed (accepted in Task 15) |
| 14 | C9 bibliography | input / criterion | **resolved** by T15 C1 (PASS) |
| 14 | C10 reproduction dry-run resolver | code | diagnosed |
| 15 | C4 [n] rendering | criterion / code | **resolved** by T16 D7 (PASS) |
| 15 | C10 phrase check | criterion | **resolved** by T17 E7 (PASS), after T16 D6 failed |
| 16 | D1 items 2(b), 9 | code | diagnosed (both hold post hoc) |
| 16 | D2 statements | document / criterion | 2.5 and 2.7: **resolved** by T17 E2 (PASS); 3.1 and 3.5: diagnosed (thesis-only imports in Task 17, not re-compared) |
| 16 | D6 legacy labels | criterion / document | **resolved** by T17 E7 (PASS) |
| 17 | E1 item 3 (P⁻ < F at 50 digits) | code | **resolved** by T18 F1 (identity and adaptive-precision test) |
| 17 | E1 item 6 (Corollary 7.4's proof) | document | **resolved** by T18 F1 |
| 17 | E3 β count | document | **resolved** by T18 F1 (draft); repository label corrected in Task 18 Part B |
| 17 | E4 range label | document | **resolved** by T18 F1 |
| 17 | E5 [47] in §7.3 | document | diagnosed: the corrected sentences say "model error" (T18 F1 post hoc); the recorded F1 sub-check failed on scope |
| 18 | F1 (the [47] scope; [21] in §1.6) | code; document | [47]: diagnosed; [21]: **open** |
| 18 | F2 counts | code | diagnosed (144 with T2.1c's "PASS (info)") |
| 18 | F3 §8.5 referee sentence | document | **open** |
| 18 | F6 appendices | code (Appendix A, math delimiters); document (Appendix D's Task 17 entry reworded in the draft) | Appendix A: diagnosed; Appendix D wording: **open** |
