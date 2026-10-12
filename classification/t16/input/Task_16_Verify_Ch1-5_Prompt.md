# Task 16 — Verify the thesis draft (chapters 1–5) against the repository; small repository fixes

You are working in the repository that holds `classification/` (Tasks 8–15), `verification/` (Tasks 1–7) and `reference/phase1/`. Use the usual protocol:
- Write `classification/PREREG_t16.md` with every check in §5 and its pass criterion. Commit it **before** running anything that produces a result.
- Run the checks once, on one recorded commit.
- Report in `classification/RESULTS_t16.md`. A failed check stays a failure, with a diagnosis (criterion, input, code or document). Never change a criterion or an artifact after the recorded run.

**Do not change any mathematical content in the repository.** Part A only checks the thesis draft; it edits nothing. Parts B and C change wording, labels, checks and one possible figure value, and nothing else. If you find a mathematical error, in the draft or in the repository, record it and do not fix it.

## Attached

| File | What it is |
|---|---|
| `Thesis_Draft_ch1-5.md` | Export of the thesis draft. Chapters 1–5 are written, 6–9 are outlined, and Appendices A–E are assembled. Since Task 15 it adds chapter 5 and Lemma 3.7, the full statements of Propositions 3.1 and 3.5 and Lemma 3.6 with a proof, a remark on Proposition 2.9, and verification-status lines. Read it; do not edit it. |

---

## Part A — Check the draft against the repository (the main task)

I wrote or rewrote several proofs by hand. I checked the key identities numerically, but SymPy was not available to me. Check each item below **symbolically with SymPy where it is an identity**, and numerically on at least 1,000 random parameter sets where it is an inequality or a sign claim. Report each item as holds, fails (with a counterexample) or ambiguous (with the reading you used).

**A1. New proof steps (not in the repository in this form).**

1. **Proposition 3.1 (§3.1):**
   - σ² = (Σ + G²/(2Π))/(λ + G) is the stationary variance of an Ornstein–Uhlenbeck process with rate λ + G and noise intensity G²/Π + 2Σ.
   - If G → 0 and G²/Π → 0 as Π → 0, then σ² → F.
   - If G → G∞ ∈ (0, ∞) as Π → ∞, then σ² → H = Σ/(λ + G∞) < F.
2. **Proposition 3.5 and Lemma 3.6 (§3.4):**
   - The Riccati root gives G⋆ = −λ + √(λ² + 2ΣΠ) and σ⋆² = 2Σ/(λ + √(λ² + 2ΣΠ)).
   - ∂σ²/∂G = (G² + 2λG − 2ΣΠ)/(2Π(λ + G)²).
   - σ⋆² is strictly decreasing in Π, tends to F as Π → 0, and satisfies G⋆ = σ⋆²Π < FΠ for Π > 0.
   - q⋆ = G⋆/(FΠ) = 2(√(1 + ν) − 1)/ν = 2/(1 + √(1 + ν)), with ν = 2ΣΠ/λ².
3. **Lemma 3.7 (§3.7):** dσ²/dΠ = G·N/(2Π²(λ + G)²) with N = ε(G² + 2λG − 2ΣΠ) − G(λ + G), where ε = ΠG′/G.
4. **Proposition 2.9, "Direction in condition 2" (§2.8):** under condition 1, σ̃² − R² has the same sign as σ² − R² at both ends of each Nᵢ, and those signs are opposite, so a strictly monotone σ̃² on Nᵢ is monotone in the same direction as σ². Check that the argument is complete as written.
5. **Theorem 5.1, proof:** the positive root in v of Πv² + 2λv − 2Σ = 0 is σ⋆²(Π).
6. **Proposition 5.8, proof:**
   - With G = cΠ/(Π + Π₀), ε = 1 − G/c.
   - Eliminating Π = Π₀G/(c − G) gives N = −(G/c)(G² + 2λG + 2ΣΠ₀ − λc).
   - The root G = −λ + √(λ² + λc − 2ΣΠ₀) lies in (0, c) iff λc > 2ΣΠ₀ (that is κ > 2), and the turning point is a maximum.
7. **Proposition 5.9, proof:** N = G·p(G)/(2(G + λ′)), with p as written; p is strictly decreasing on G > 0; and p(0) > 0 iff F′ > 2F.
8. **Proposition 5.14, proof:**
   - The derivative identity holds.
   - The bound: where σ² ≤ F, ΠG′(2λG + G² − 2ΣΠ) − G²(λ + G) ≤ G(λ + G)(ΠG′ − G) when G′ ≥ 0.
9. **Corollary 5.2:** σ⋆²(π_R) = R² for π_R = 2λ(F − R²)/R⁴.

**A2. Statements carried over from the repository.**
- For every numbered result in chapters 2–5 of the draft (2.1–2.9, 3.1–3.7, 4.1–4.5, 5.1–5.15), compare the draft's statement with `source/Stages_0_4_Source.md` (or `source/thesis_only/` for 2.3, 2.8, 2.9, 3.2). Report every difference in hypotheses, conclusions, constants or class tables. Wording and notation changes don't count; content changes do.
- Classify each difference as one of: (a) equivalent; (b) the draft is weaker; (c) the draft is stronger; (d) the draft contradicts the repository.
- Note the edits I know of: "G⋆ < FΠ for Π > 0" (strict) in 3.5, where the repository says ≤; and "Corollary 5.4 (unbounded windows for regular gains)", whose repository title is "unbounded complexity inside the model".

**A3. Numbers in chapters 1–5.**
- Re-derive every numerical value in chapters 1–5 that comes from a formula, from the repository's scripts or from the formula at the stated parameters. This includes:
  - Π₀^pair = 30.243, 31.475, 37.820, 44.180 and 62.711 for n = 1.5, 2, 3, 4 and 8 (at λ = c = 1, Σ = 0.01);
  - M/F = 17.575 and 9.2875, and their ratio 1.892;
  - π_R = 222.2;
  - the Hill window onset 25 = cλ/(4Σ);
  - the mixed-band statistics (median 5 × 10⁻⁴, range 4 × 10⁻²² to 0.96, 16%);
  - every count quoted in the verification paragraphs (101/101, 24/24, 2,000/2,000, 961, 5,000, 10,000, 4,868, 77,888, 7/2,000, 63/2,000, 6 × 10⁻³¹, 6 × 10⁻¹⁰).
- Report value, source and match for each.

**A4. Citations and cross-references in the draft.**
- Every [n] in chapters 1–5 resolves in `register/references.yaml`. Numbers [1]–[45] first appear in ascending order of first citation.
- Every "Theorem/Proposition/Lemma/Corollary/Numerical result x.y" in the draft names a register result of that type and number.
- Every "Figure B.n" exists in `register/figures.yaml`.
- Report any reference to a result that does not exist or has a different type.

## Part B — Figure B.4 value

The B.4 description gives the envelope touch point of the Bayesian-weight base curve as **Π_c = 56.7** (κ = 1.5, λ = c = 1, Σ = 0.01). Solving cΠ/(Π + Π₀) = −λ + √(λ² + 2ΣΠ) with Π₀ = c/(κF) and F = Σ/λ gives **Π_c = 56.20**.

- Report the value the script uses and how it computes it, and which parameters the figure actually uses.
- If the script's parameters differ from the description, correct the description.
- If the description's value is a rounding or computation error, correct the description (and the image annotation, if the image shows it).
- Do not change the curve.

## Part C — Small repository fixes (carried from Task 15)

1. **Legacy-label collision.**
   - In `register/crosswalk.md` and `crosswalk_v1.yaml`, prefix every legacy label with `legacy ` (for example `legacy B.1`), so legacy labels can no longer be read as figure labels.
   - Rewrite the legacy-label check so that `Figure B.n` and the Appendix B entries are exempt and only bare legacy labels count.
2. **Citation check.** Count a bracket group as a citation only if it is a comma- or dash-separated list of integers that resolve in `register/references.yaml`. Intervals such as `[0, 10]` must not be flagged.
3. **Register wording.** `results.yaml`, result 5.6, `verified_by: T8.1 (Proposition 4)` carries a consolidated-v1 number. Rewrite it with thesis numbering (the check is of the excess identity, Corollary 3.3), and re-render Appendix A.
4. **Thesis-only texts.**
   - Refresh `source/thesis_only/` from the attached draft: `structural-stability.md` (add the "Direction in condition 2" remark) and `normal-form.md` (the heading is now "Theorem 3.2 (normal form)", with no "(a)").
   - Report whether the thesis render should also carry the draft's new wording of 3.1, 3.5, 3.6 and 3.7. Do not change those sources.
5. **Re-run the Task 15 checks C4 and C10** with the fixed patterns, as T16 checks. The T15 results stay as recorded.

## 5. Pre-registered checks (write these into PREREG_t16.md with these criteria)

| Check | Pass criterion |
|---|---|
| D1 New proof steps (A1) | All 9 items hold (identities reduce to 0 in SymPy; inequalities and signs hold on ≥ 1,000 random sets with no counterexample) |
| D2 Statements (A2) | No difference of kind (c) or (d) |
| D3 Numbers (A3) | Every value matches its source to the digits printed |
| D4 Cross-references (A4) | 0 unresolved [n]; first-citation order holds for [1]–[45]; 0 references to a nonexistent result or wrong type; 0 unknown figure labels |
| D5 Figure B.4 (Part B) | The description's Π_c equals the value computed from the figure's parameters, to the digits printed |
| D6 Legacy labels (C.1) | Every legacy label in the crosswalk has the prefix; the rewritten check reports 0 bare legacy labels in thesis renders and 0 false hits on Figure B.n |
| D7 Citation check (C.2) | 0 false hits on intervals; every real citation in the renders still detected (count equal to Task 15's) |
| D8 Register wording (C.3) | No consolidated-v1 result number in any `verified_by` field |

## 6. Report (RESULTS_t16.md), and what to send back

In `RESULTS_t16.md`:
- the commits (pre-registration, artifacts checked, results);
- the check table with outcome and runtime;
- diagnoses of any failure;
- files changed.

Then, under **For the author**, give:
1. **A1:** each item with holds, fails or ambiguous, and the SymPy residual or counterexample.
2. **A2:** every difference, with its kind and both texts side by side.
3. **A3:** a table of each value, its source and whether it matches.
4. **A4:** any broken reference.
5. **Part B:** the Π_c answer.
6. Anything else in chapters 1–5 that disagrees with the repository. List it; do not resolve it.

Attach `RESULTS_t16.md`, the re-rendered `Appendix_A_Register.md`, `register/crosswalk.md` and `register/results.yaml`.
