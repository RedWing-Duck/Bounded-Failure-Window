# Pre-registration — Task 17: verify chapters 6–7 and the new §2.5 statements; repository sync items

Committed **before** any Task 17 script that produces a result is written or run. Not edited after its commit. The checks E1–E7
run **once**, on one recorded commit (the artifacts commit). A failed check stays a failure, with a diagnosis attributed to the
**criterion**, the **input**, the **code** or the **document**. No criterion and no artifact is changed after the recorded run,
with one planned exception: the Task 17 entry of Appendix D, which can only be written from the recorded outcome (as for Task 15).

**No mathematical content changes.** Part A checks the draft and edits nothing. Part B changes renders, checks and thesis-only
texts. A mathematical error found in the draft or in the repository is recorded, not fixed.

**Inputs** (copied unchanged to `classification/t17/input/`): `Thesis_Draft_ch1-7.md` (the thesis draft, read-only, used to
compare against the repository; Part B.2 imports the passages the prompt names, and nothing else) and the Task 17 prompt.

Tools: Python 3, SymPy, mpmath (50 digits unless stated), NumPy, PyYAML; the session's web search tool for E5. Seeds: 17001 (E1
random parameter sets), 17002 (E1 numerical fallback for identities), 17003 (spare; any use reported).

## Disclosure: what is known before the run

1. **The draft** has been read: chapters 6–7 in full, the new §2.5 statements, Appendix D, and the changes to chapters 1–5 since
   Task 16 (the §1.5 sentence on Corollaries 5.2–5.3, the §2.5 table rows for 2.5 and 2.7, the definition of c_R in 4.5, and the
   "all 2,000 random sets with n = 2 (961 with the pair, 1,039 without)" wording). The statements have not yet been compared
   with the repository.
2. **A1 items were worked through by hand** while writing this file, to set up the symbolic checks. The hand derivations found no
   error. One reading question: in item 6 (Corollary 7.4), the statement's second sentence (the optimal classes along precision
   are lower ray and Empty, and every curve strictly above the envelope belongs to a miscalibrated gain) also uses Theorem 5.1,
   which the statement names, and σ⋆² → 0 as Π → ∞ (Theorem 3.4), which the proof does not name. Item 6 reports whether the
   proof as written covers it.
3. **The repository has no labelled statement of 6.13.** The source mentions it once, in Lemma 6.14 (the phase-1 discrete excess
   condition); the register title is "Discrete excess condition L/(2 − L) > FΠ_d for 0 ≤ L < 2". The manuscript's statement
   (`reference/phase1/`, quoted with its page in `RESULTS_t15.md`, item 4) is used as the repository's text for 6.13.
4. **Escaped citations.** At the Task 16 head (daae576) the thesis render prints 2 citation groups as `\[n\]`, both from
   thesis-only texts (`normal-form.md`, `tau-optimal-normal-form.md`). The draft passages imported in Part B.2 contain more.
5. **Prior-work sources (E5).** `references.bib` holds titles and DOIs but no abstracts. From this session doi.org and
   api.crossref.org are refused by the network policy (curl: CONNECT 403; the fetch tool: host not found). E5 therefore uses
   the bib title and the session's web search (one standard search per cited entry, by title, during the recorded run; the
   result summaries are stored in `t17/results/e5_sources.md`), plus the repository's own literature notes
   (`t13/literature_check.md`). Where these do not settle a sentence, the judgement is **undetermined** and is listed.
6. **Legacy-label hits.** Task 16's D6 flagged two figure labels in Appendix E, one in a code-block chain comment
   ("… result 5.6 wording, B.4 Pi_c"), and a quoted "Paper 1" in Appendix D. E7 is about labels only.
7. **Appendix D layout.** The draft's Appendix D writes each task as "**Task N.** prereg · results. k checks …" with
   "Failure — …" bullets; the repository's uses headings and field bullets. Part B.4 renders the repository's Appendix D in the
   draft's layout, so the new entries match the rest; the counts and attributions stay as recorded, and the Task 16 entry uses
   the draft's wording.
8. **A3 sources.** The stored values for chapters 6–7 are in the Task 9–13 results (`t9/`, `t10/`, `t11/`, `t12/`, `t13/`
   results and reports); they are located while writing the check script, after this commit. Values seen while locating them
   are disclosed in the results.

## Part A — the draft against the repository

Run script: `t17/t17_checks.py` (E1, E3, E4, E6, E7, and the A2 extraction); `t17/t17_e5.md` procedure for E5. Outputs in
`t17/results/`.

### E1 — new proof steps (A1)

All symbols positive unless stated. An **identity** holds if the difference of its sides reduces to 0 by: `simplify`;
`factor(radsimp(·))`; or the **denesting step** — each `sqrt(X)` whose radicand X factors as Y² with Y > 0 under the stated
positivity (checked by `factor`, and Y's sign by an explicit argument) is replaced by Y, then `simplify`. A **sign or inequality**
is established by an explicit argument recorded in the output (a factorisation into factors of known sign), never by SymPy's
assumption system, and is also tested on ≥ 1,000 random parameter sets (log-uniform in [10⁻³, 10³], seed 17001). If an identity
does not reduce symbolically, the **numerical fallback** evaluates it at 1,000 random sets (seed 17002) at 50 digits and passes it
if every residual is below 10⁻³⁵ relative; both outcomes are reported.

| Item | What is checked |
|---|---|
| 1 Cor. 6.5 | Πb = 2λ(1 + νt); (Π√D)² = 4λ²((1 + νt)² + ν(1 − t)²) and Π√D > 0; P/F = 2/(1 + νt + √((1 + νt)² + ν(1 − t)²)) from P = 4Σ/(Π(b + √D)); value at t = 0 equals 2/(1 + √(1 + ν)). |
| 2 Lemma 6.1 normal form | σ²/F = 𝒱_τ(ν, q, t) with a = λ + G, G = qFΠ, t = λτ; σ² > F ⟺ q > 2(1 + aτ) (identity for σ² − F and a sign argument; numeric). |
| 3 Prop. 6.13 | P⁻ = (a²L²r + q)/(1 − a²(1 − L)²) from P⁻ = a²P⁺ + q and P⁺ = (1 − L)²P⁻ + L²r; numerator of P⁻ − F = a²L(Lr − F(2 − L)); denominator > 0 for 0 ≤ L < 2, 0 < a < 1; P⁻ > F ⟺ L/(2 − L) > φ; P⁺ − F = (P⁻ − F)/a²; for the steady-state Kalman filter (prior from the discrete Riccati equation), P⁻ < F and L⋆/(2 − L⋆) < φ/2 (sign argument and ≥ 1,000 random (λ, Σ, Π, Δt)). |
| 4 Lemma 6.14 | P̄ − F = (P⁺ − F)s/(2λΔt) from the definition of P̄; and the definition equals the time average over a period of P(t) = e^(−2λt)P⁺ + F(1 − e^(−2λt)). |
| 5 Lemma 6.23 | σ²/F = (1 + g²/u)/(1 + g) with g = G/λ, u = 2ΣΠ/λ²; for G = λ·γ(u), (Σ, Π) pairs with equal u give equal σ²/F (1,000 random sets, random smooth γ), so the relative failure set in u is the same along either sweep. |
| 6 Cor. 7.4 | Logical review (after the run, `t17/results/e1_item6_review.md`): does the statement follow from Corollary 7.3 and Proposition 7.7(a) as written? |
| 7 Prop. 2.7 | roots of a(x² − bδ) are ±√(bδ) for bδ > 0; |∫ between them| = (4/3)|a|(bδ)^(3/2). |
| 8 Thm 7.8 (3) | 2C/(B + √(B² + 4AC)) ≤ √(C/A) for A, B, C > 0 (sign argument and numeric); √(C/A) = √(2ΣK)τ^(β/2)/|1 − λτ| for v = (K/2)τ^(β−1), A = (1 − λτ)²/τ, C = 4Σv, λτ ≠ 1. |
| 9 Prop. 7.10 | A(1/(λ²τ)) = A(τ); v_(2−β, Kλ^(2−2β))(1/(λ²τ)) = v_(β,K)(τ); hence P_β,K(τ) = P_(2−β),Kλ^(2−2β)(1/(λ²τ)) identically (symbolic and numeric over random β ∈ (−3, 5)). |

Each item: holds, fails (counterexample or residual), or ambiguous (with the reading used).
**Pass:** all 9 items hold.

### E2 — statements (A2)

For 2.4–2.7, 6.1–6.28 and 7.1–7.16 (48 results) the run extracts the draft's statement and the repository's
(`source/Stages_0_4_Source.md` with [[key]] tokens resolved to thesis numbers; `source/thesis_only/tau-optimal-normal-form.md`
for 6.5; the manuscript statement for 6.13, disclosure 3) into `t17/results/a2_pairs.md`. Proofs, remarks and verification
lines are not compared, except that a proof the draft adds where the repository has none is noted (6.9 and 7.4 per the prompt).
After the run every difference is recorded in `t17/results/a2_classification.yaml` with both texts and a kind (a)–(d); for each
kind (c), where the added content is proved (in the draft, the repository or an A1 item), or "not proved". Manual reading.
**Pass:** no kind (d), and every kind (c) has its added content proved somewhere.

### E3 — numbers (A3)

Every value below is compared with its source **to the digits printed** (as in Task 16 D3). Formula values are recomputed with
mpmath; stored values are read from the Task 9–13 results.

| # | Draft value | Source |
|---|---|---|
| 1 | §6.1 worked example (λ = c = 1, Σ = 0.01, Π = Π₀ = 1, G = 0.5): V_w = 0.09, H_G = 0.0066667, τ_F = 16, σ²(1) = 0.04, σ²(10) = 0.011875, σ²(16) = 0.01 | Lemma 6.1, Props 6.2–6.3 |
| 2 | §6.1: σ⋆² = 0.0099505, P(1) = 0.0098039, V(1) = 0.0099010, P(10) = 0.0067813 | Prop. 6.4; V by minimising σ²(G, τ) over G ∈ [0, ∞] |
| 3 | §6.5 D1 example (G = 0.5, λ = 1, Σ = 0.01, Π = 1): post from 0.09 to a maximum 0.20457 at Δt = 2.4645 and to 0; Δt_E = 100 to 20 digits; avg 0.0099875 at Δt = 200, a dip of 0.125 % | M-P formulas of §6.3 |
| 4 | §6.3 D2 example (c = 3): P⁺ > F at every Δt (grid of 2,000 log-spaced Δt in [10⁻⁶, 10⁶]) and P⁺ → 4F | M-P formulas; Prop. 6.18 |
| 5 | §7.4 latency: P(0) = 0.0099505, P(1/e) = 0.0099763 | Prop. 7.11 |
| 6 | §6.5 G = 0.019 example: D1 avg has a maximum, then a minimum below its starting value | M-P formulas |
| 7 | census counts: 178 of 1,000 (Prop. 6.17 remark); 2,000 sets per family and 6,000 × 3 (Num. result 6.21); 1,000 of 1,000 D3 excess sets lower ray or Empty | Task 12 results |
| 8 | §2.5 verification: 1,000 tolerances (T10.5); exponents 1.50007 and 0.50002 | Task 10 results |
| 9 | §6.2 and §6.5 verification: 80,000 classifications (T9.4); 2 × 10⁻¹⁷ (T9.2); 285 and 13 flags (T9.5); 10,000 sets at 60 digits (T13 A7); 1.0 × 10⁻¹⁴ and 10⁻⁵⁰ (T10.6) | Task 9, 10, 13 results |
| 10 | §6.5 verification: 1,000 of 1,000 and Δt_E to 10⁻³⁰ (A2); 1,000 of 1,000 (A3, A4); 201,514 membership tests (A4); 10,000 sets at 100 digits (T13 A1, A2); 400,000 points (T12) | Task 12, 13 results |
| 11 | §6.6 verification: 2,000 sets each; position to 6 × 10⁻³¹ | Task 12 results |
| 12 | chapter 7 verification: 25,000 pairs; 37 values of β; 10,000 curves (T13 A4); 12,900 of 12,900 (T11); 8 × 10⁻⁵¹; |z| ≤ 1.91; 1,000 of 1,000 (T11.5); 9,000 pairs (T11.6); 11 of 11 and 10,000 sets at 100 digits (T13 A3); 400,000 points each (T11.6, T12 A9); 1,000 of 1,000 pairs (T12 A10) | Task 11, 12, 13 results |
| 13 | audit rows named in chapters 6–7 (13, 14, 15, 16, 17–19, 20, 24–32, 35–42) cover the sweeps the draft says | `t13/results/t13_audit_classes.json` row names |

A value whose stored source cannot be found is reported as **no source** and counts as a mismatch.
**Pass:** every value matches its source to the digits printed.

### E4 — cross-references, mechanical (A4)

As Task 16 D4, over chapters 1–7 (up to "## 8."): every [n] group of integers in 1–53 resolves in `register/references.yaml`;
numbers 1–53 first appear in ascending order; every typed result reference (with plurals, abbreviations and ranges) names a
register result of that type; every untyped table label exists; every "Figure B.n" exists in `register/figures.yaml`.
**Pass:** 0 unresolved; order holds for [1]–[53]; 0 wrong-type or nonexistent references; 0 unknown figure labels.

### E5 — prior-work sentences (A4, last item)

The sentences of chapters 6–7 citing [26], [27, 28, 45, 46] (and [27, 28, 45]), [47], [48], [18–23, 49, 50], [24, 50, 51],
[29, 52, 53] are listed with their cited entries in `t17/results/e5_judgements.md`. For each entry the evidence is the bib title,
the web-search summary (disclosure 5) and `t13/literature_check.md`. Each sentence gets: **supported**, **claims more** (with
what), or **undetermined** (the evidence does not settle it). Manual, after the run.
**Pass:** no sentence "claims more". Undetermined sentences are listed and do not count as failures.

## Part B — repository sync

1. **Escaped citations.** The render templates (`source/thesis_only/*.md`, including the new imports) write citations as `[n]`,
   not `\[n\]`. The citation check gains the escaped form.
2. **Thesis-only texts, thesis render only, `Stages_0_4_Source.md` unchanged.** `register/render.py` gains a list of overrides
   (`register/thesis_overrides.yaml`), applied in thesis mode only: **replace** a source result block (its label line through the
   end of its proof, or through its statement paragraph if it has no proof; following **Label:** lines and remarks are kept) by a
   thesis-only text, or **insert** a text before an anchor line. Imports (verbatim from the draft except `\[n\]` → `[n]`, each with
   a header naming its draft lines):
   - `stationary-variance.md` (3.1 statement and proof), inserted before the normal-form include;
   - `optimal-envelope.md` (3.5 statement, 3.6 statement and their joint proof), replacing the 3.6 block;
   - `plateaus.md`, `equal-height-maxima.md`, `degenerate-points.md`, `pair-birth.md` (2.4–2.7 with proofs), replacing the source
     blocks; all four differ from the source in wording at least;
   - `discrete-excess.md` (6.13 statement and proof), inserted before the 6.14 block.
3. **Legacy-label check** (E7): Task 16 D6's rule with the exemption window widened from 40 to 200 characters and with figure
   labels inside fenced code blocks of `Appendix_E_Reproduction.md` exempt.
4. **Appendix D** in the draft's layout (disclosure 7), with the Task 16 entry and, after the run, the Task 17 entry.

### E6 — escaped citations (B.1)

In every thesis render (Task 15's list): count `\[n\]` groups (escaped) and citation groups `[n]` (Task 15's pattern; all numbers
resolve). Baseline at daae576: unescaped + escaped citation groups. **Pass:** 0 escaped groups; unescaped count = baseline + the
citation groups contained in the new thesis-only texts (counted in those files).

### E7 — legacy labels (B.3)

Task 15's thesis renders, whitespace-normalised; every `\b[A-E]\.\d+\b` is **prefixed** ("legacy "), a **figure label** under the
widened exemption (B.1–B.12 and: file is Appendix B or in `figs_thesis/`; or "figure(s)"/"Figure(s)" within the 200 characters
before; or followed by "_"; or inside a fenced code block of Appendix E), or **flagged**. **Pass:** 0 flagged (that is, 0 bare
legacy labels and 0 false hits on figure labels, Appendix E included). "Paper 1" occurrences are reported, not judged.

## Report

`classification/RESULTS_t17.md`: commits, check table with outcomes and runtimes, diagnoses, files changed, and **For the author**
items 1–5. Attachments: `RESULTS_t17.md`, `Appendix_D_Verification.md`, the new `source/thesis_only/` files.
