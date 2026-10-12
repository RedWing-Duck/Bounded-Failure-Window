# Task 17 — Verify chapters 6–7 and the new §2.5 statements; repository sync items

You are working in the repository that holds `classification/` (Tasks 8–16), `verification/` (Tasks 1–7) and `reference/phase1/`. Use the usual protocol:
- Write `classification/PREREG_t17.md` with every check in §4 and its pass criterion. Commit it **before** running anything that produces a result.
- Run the checks once, on one recorded commit.
- Report in `classification/RESULTS_t17.md`. A failed check stays a failure, with a diagnosis (criterion, input, code or document). Never change a criterion or an artifact after the recorded run.

**Do not change any mathematical content in the repository.** Part A only checks the thesis draft. Part B changes renders, checks and thesis-only texts. If you find a mathematical error, in the draft or in the repository, record it and do not fix it.

**Lesson from Task 16:** before the recorded run, give every symbolic check a denesting step for square roots of squares (√(x²) → x under stated positivity) and an explicit sign argument, rather than SymPy's assumption system. Pre-register a numerical fallback (≥ 1,000 random sets, a stated seed) for any identity SymPy cannot reduce. Report both.

## Attached

| File | What it is |
|---|---|
| `Thesis_Draft_ch1-7.md` | Export of the thesis draft. Chapters 1–7 are written, 8–9 outlined, and Appendices A–E assembled. Since Task 16 it adds chapter 6, chapter 7, full statements of 2.4–2.7 in §2.5, and the Task 16 fixes. Read it; do not edit it. |

---

## Part A — Check the draft against the repository (the main task)

Same method as Task 16 Part A. Check identities symbolically and inequalities and signs numerically on ≥ 1,000 random parameter sets. Report each item as holds, fails (with a counterexample) or ambiguous (with the reading you used).

**A1. New proof steps (not in the repository in this form).**

1. **Corollary 6.5 (§6.1):** from Proposition 6.4, Πb = 2λ(1 + νt) and Π√D = 2λ√((1 + νt)² + ν(1 − t)²), so P/F = 2/(1 + νt + √((1 + νt)² + ν(1 − t)²)), with ν = 2ΣΠ/λ² and t = λτ. At t = 0 it equals 2/(1 + √(1 + ν)).
2. **Lemma 6.1 in normal form (§6.1):** σ²/F = 𝒱_τ(ν, q, t) of §3.8, and σ² > F iff q > 2(1 + aτ), with a = λ + G and q = G/(FΠ).
3. **Proposition 6.13 (§6.3):**
   - With q = F(1 − a²), r = 1/(ΠΔt) and φ = FΠΔt: P⁻ = (a²L²r + q)/(1 − a²(1 − L)²), and the numerator of P⁻ − F equals a²L(Lr − F(2 − L)).
   - The denominator is positive for 0 ≤ L < 2.
   - P⁻ > F iff L/(2 − L) > φ.
   - P⁺ − F = (P⁻ − F)/a².
   - For the steady-state Kalman gain, L⋆ = P⁻/(P⁻ + r) with P⁻ < F, and L⋆/(2 − L⋆) < φ/2 for every Δt > 0.
4. **Lemma 6.14:** the identity P̄ − F = (P⁺ − F)·s/(2λΔt) follows from the definition of P̄ in §6.3.
5. **Lemma 6.23's proof:** under a relative tolerance, the Σ sweep and the precision sweep give the same failure set in u for a gain depending on (Σ, Π) only through u.
6. **Corollary 7.4's proof:** it follows from Corollary 7.3 and Proposition 7.7(a), as written.
7. **Proposition 2.7 (§2.5, as now stated):** for dσ²/dθ ≈ a(x² − bδ), the roots are ±√(bδ), and the change in value between them is (4/3)|a|(bδ)^(3/2).
8. **The bound in Theorem 7.8, part 3:** P ≤ √(C/A) = √(2ΣK)·τ^(β/2)/|1 − λτ| for the power family, with v(τ) = (K/2)τ^(β−1).
9. **Proposition 7.10 (duality):** P_β,K(τ) = P_(2−β), Kλ^(2−2β)(1/(λ²τ)), identically.

**A2. Statements carried over from the repository.**
- For every numbered result in §2.5 (2.4–2.7), chapter 6 (6.1–6.28) and chapter 7 (7.1–7.16), compare the draft with `source/Stages_0_4_Source.md` (or `source/thesis_only/` for 6.5). Use Task 16's kinds: (a) equivalent; (b) the draft is weaker; (c) the draft is stronger; (d) the draft contradicts the repository. Give both texts for every difference.
- For each kind (c), say whether the added content is proved somewhere: in the draft, in the repository or in an A1 item.
- Edits I know of:
  - 6.13 is restated in the M-P notation of §6.3 (the manuscript writes ϕ, M_L, S_L, Π_d);
  - 6.9 and 7.4 carry short proofs in the draft;
  - 7.6's title is "the orderings coincide for Gaussian noise".

**A3. Numbers in chapters 6–7.** Re-derive every numerical value from its formula or from the repository's stored results, and report value, source and match for each. This includes:
- the worked examples: V_w = 0.09, H_G = 0.0066667, τ_F = 16, σ²(1) = 0.04, σ²(10) = 0.011875, σ⋆² = 0.0099505, P(1) = 0.0098039, V(1) = 0.0099010, P(10) = 0.0067813;
- the D1 example: 0.20457 at Δt = 2.4645, Δt_E = 100, 0.0099875 at Δt = 200, dip 0.125%;
- the latency example: P(0) = 0.0099505, P(1/e) = 0.0099763;
- the D2 example (c = 3: P⁺ → 4F);
- the census counts (178 of 1,000; 2,000 per family; 6,000 × 3);
- every count and tolerance quoted in the verification paragraphs of chapters 6–7.

**A4. Citations and cross-references.**
- Every [n] in chapters 1–7 resolves in `register/references.yaml`, and [1]–[53] first appear in ascending order.
- Every typed result reference ("Proposition 6.10", "Corollary 7.3" and so on) names a register result of that type and number.
- Every Figure B.n exists.
- For each sentence in chapters 6–7 that cites prior work, check that the cited entry's title and abstract (from the bib, or the DOI landing page if reachable) support the sentence as written. Report any sentence that claims more than its source. These are the sentences with [26], [27, 28, 45, 46], [47], [48], [18–23, 49, 50], [24, 50, 51], [29, 52, 53].

## Part B — Repository sync items

1. **Escaped citations.** Some renders print citations as `\[n\]`. Unescape them in the render templates, and widen the citation check to detect that form; it should find 0 afterwards.
2. **Thesis-only texts.**
   - Import the draft's statements and proofs of 3.1, 3.5 and 3.6 together as `source/thesis_only/` texts, rendered in the thesis render only. Task 16 advised that 3.6 must move with 3.5.
   - Import the draft's §2.5 statements of 2.4–2.7 and 6.13 where they differ from the source.
   - Leave `Stages_0_4_Source.md` unchanged.
3. **Legacy-label check.** Widen the exemption window so figure labels in Appendix E's chain comments are exempt. Re-run that check as a T17 check; the T16 result stays as recorded.
4. **Appendix D.** Add the Task 16 and Task 17 entries, with the same format and attributions as the draft's Appendix D.

## 4. Pre-registered checks (write these into PREREG_t17.md with these criteria)

| Check | Pass criterion |
|---|---|
| E1 New proof steps (A1) | All 9 items hold (identities reduce to 0 with the denesting step, or by the pre-registered numerical fallback; inequalities and signs hold on ≥ 1,000 random sets) |
| E2 Statements (A2) | No difference of kind (d); every kind (c) has its added content proved somewhere |
| E3 Numbers (A3) | Every value matches its source to the digits printed |
| E4 Cross-references (A4, mechanical part) | 0 unresolved [n]; first-citation order holds for [1]–[53]; 0 wrong-type or nonexistent result references; 0 unknown figure labels |
| E5 Prior-work sentences (A4, last item) | No sentence claims more than its source supports (judged against title and abstract; list every judgement) |
| E6 Escaped citations (B.1) | 0 `\[n\]` in any render; citation count otherwise unchanged |
| E7 Legacy labels (B.3) | 0 bare legacy labels; 0 false hits on figure labels anywhere, Appendix E included |

## 5. Report (RESULTS_t17.md), and what to send back

In `RESULTS_t17.md`:
- the commits (pre-registration, artifacts checked, results);
- the check table with outcome and runtime;
- diagnoses of any failure;
- files changed.

Then, under **For the author**, give:
1. **A1:** each item with holds, fails or ambiguous, and its residual or counterexample.
2. **A2:** every difference, with its kind and both texts side by side.
3. **A3:** a table of each value, its source and whether it matches.
4. **A4:** any broken reference, and every prior-work judgement.
5. Anything else in chapters 1–7 that disagrees with the repository. List it; do not resolve it.

Attach `RESULTS_t17.md`, the re-rendered `Appendix_D_Verification.md` and the new `source/thesis_only/` files.
