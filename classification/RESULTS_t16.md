# Results — Task 16: the thesis draft (chapters 1–5) against the repository; small repository fixes

- Pre-registration: `classification/PREREG_t16.md`, commit **19c6ffe**.
- Artifacts checked: commit **bc0a72c**. D1–D8 ran once on it (35 s in all; `t16/results/t16_checks.log`, `.time`).
- Results: commit **cf29da7** (recorded outputs, the A2 classification, the item 4 review and the post-hoc diagnosis); this report follows it.

## Checks

| Check | Verdict | Details | Runtime (s) |
|---|---|---|---|
| D1 New proof steps (A1) | **FAIL** | 7 of 9 items hold in the recorded run; items 2 and 9 did not reduce in the pre-registered SymPy routes (code; both hold post hoc) | 33.07 |
| D2 Statements (A2) | **FAIL** | 17 differences in 36 results: 9 (a), 4 (b), 4 (c), 0 (d); kind (c) at 2.5, 2.7, 3.1, 3.5 | 0.07 |
| D3 Numbers (A3) | **PASS** | 84 of 84 values match their sources to the digits printed | 0.26 |
| D4 Cross-references (A4) | **PASS** | 30 citation groups, 0 unresolved; first-citation order 1–45 holds; 214 typed and 34 untyped result references, 0 broken; 6 figure references, 0 unknown | 0.09 |
| D5 Figure B.4 (Part B) | **PASS** | root Π_c = 56.2047; description, Appendix B and the B.4 caption print 56.20 | 0.01 |
| D6 Legacy labels (C.1) | **FAIL** | crosswalk: 0 unprefixed; renders: 2 flagged (2 figure labels outside the exemption window, Appendix E), 0 false hits on Figure B.n, 1 'Paper 1' (a quotation in Appendix D) | 0.46 |
| D7 Citation check (C.2) | **PASS** | 13 citations detected = baseline 13 (per file equal); intervals not flagged (2 listed as non-citations); no other hit | 0.38 |
| D8 Register wording (C.3) | **PASS** | 0 consolidated-v1 numbers in `verified_by` | 0.09 |

**Pre-registered checks that FAIL:** D1, D2, D6. Each stays a failure; diagnoses below.

## Diagnoses

- **D1 (attribution: code).** Item 2(b) asked SymPy's assumption system whether −λ + √(λ² + 2ΣΠ) is positive; it returns None (undecided), so the check recorded the claim as not shown. The radicand minus λ² is 2ΣΠ > 0, the other root is negative, and 1,000 random sets (seed 16003, the pre-registered spare) give no counterexample. Item 9's residual contains √(R⁴ + 4d(R² + d)) = R² + 2d (with Σ = λ(R² + d)), a square root of a square that none of the three pre-registered routes denests (the cause of the Task 10 and Task 13 route failures too); after substituting the denested root the residual is 0, and the recorded numeric residual was 1.4 × 10⁻⁴⁸. Both claims hold (`t16_diag.json`). Every other sub-check of items 2 and 9 passed in the recorded run.
- **D2 (attribution: document, and criterion).** Four differences are of kind (c). For 3.1 and 3.5 the draft's statement includes conclusions that the repository states in other results (Theorem 3.4, Lemma 3.6, Corollary 5.5): the draft is stronger than the repository's statement of *that* result, not than the repository; D1 items 1 and 2 verify the added conclusions. For 2.5 and 2.7 the draft has no statement, only a row of the §2.5 event table that leaves out the result's hypotheses; read as a statement it claims more than the repository. The criterion counts a correct, proved strengthening the same as an unproved one.
- **D6 (attribution: criterion, and document).** None of the three hits is a legacy label. Appendix E's chain comment added in this task ("… B.4 Pi_c") and its line "figures B.1, B.3–B.12 (text-only edits) and B.2" name figure labels more than 40 characters after a "figure" word, outside the pre-registered exemption window; Appendix D's T15 failure line quotes the phrase "0 'Paper 1'". Bare legacy labels in the thesis renders: 0; false hits on Figure B.n: 0.

## Disclosure

- Before the recorded run each check was run once with its output discarded (standard output to /dev/null, JSON to the scratchpad), only to see that it ran. One code error was fixed: D3's maximiser of φₙ (a Newton start that strayed into complex values), replaced by golden-section search with a Newton polish; because the polish limits precision, the tolerance for t\*² = 2√3 − 3 was set to 10⁻³⁰ at the same time, before any value was seen. The D2 extraction was checked for completeness; it reported 2.4–2.7 missing from the draft, which reading the draft had already shown (they appear only in the §2.5 table).
- D2's classification and D1 item 4's logical review are manual readings made after the recorded run (`t16/results/a2_classification.yaml`, `d1_item4_review.md`).

## Files changed

- `register/results.yaml` (legacy labels prefixed; 5.6 `verified_by` "T8.1 (Corollary 3.3, excess identity)"); `register/crosswalk.md` (regenerated); `register/crosswalk_v1.yaml` ("legacy §A.3"); `register/figures.yaml` (B.4 Π_c = 56.20).
- `source/figs/fig02_realizability.txt`, `source/figs/README.md` (Π_c = 56.20); `source/thesis_only/structural-stability.md` (the "Direction in condition 2" remark), `source/thesis_only/normal-form.md` (heading "Theorem 3.2 (normal form)").
- Renders: `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (one change-log line: "legacy §A.3"), `Appendix_A_Register.md`, `Appendix_B_Figures.md`, `Appendix_E_Reproduction.md`, `figs_thesis/B.4_realizability.txt`, `figs_thesis/README.md`.
- `t15/make_appendix_de.py` (Appendix E: the T16 row and the `t16/t16_register.py` step).
- New: `t16/t16_register.py`, `t16/t16_checks.py`, `t16/t16_diag.py`, `t16/make_results_t16.py`, `t16/input/`, `t16/results/`.

## For the author

### 1. A1: the new proof steps

| Item | Verdict | Evidence |
|---|---|---|
| 1 Prop 3.1 | holds | D/(2a) = (Σ + G²/(2Π))/(λ + G) reduces to 0; the Lyapunov equation gives P = D/(2a); both limits by substitution into a continuous expression; F − H = ΣG∞/(λ(λ + G∞)) > 0. |
| 2 Prop 3.5 / Lemma 3.6 | holds post hoc; recorded as not shown (code) | Riccati root, G⋆ = pΠ, σ⋆² = p = σ²(G⋆), ∂σ²/∂G, both forms of q⋆: residual 0. dσ⋆²/dΠ < 0, σ⋆² → F, σ⋆² < F: 0 counterexamples in 1,000. The recorded run did not establish "G⋆ is the only positive zero" (SymPy could not decide the sign); it holds (diagnosis D1). |
| 3 Lemma 3.7 | holds | total derivative minus G·N/(2Π²(λ + G)²): residual 0; ∂σ²/∂Π = −G²/(2Π²(λ + G)): residual 0. |
| 4 Prop 2.9 remark (numeric part) | holds | logical review: complete as written (`d1_item4_review.md`); numeric: 1,000 (curve, Nᵢ) pairs, 0 counterexamples. |
| 5 Thm 5.1 | holds | positive root of Πv² + 2λv − 2Σ minus σ⋆²: residual 0. |
| 6 Prop 5.8 | holds | ε = 1 − G/c and the eliminated N: residual 0; root in (0, c) iff λc > 2ΣΠ₀ iff κ > 2: symbolic, and 0 counterexamples in 1,000; turning point a maximum: N changes sign + → − in 1,000 of 1,000 sets with κ > 2. |
| 7 Prop 5.9 | holds | inverse Π(G), ε and N = G·p(G)/(2(G + λ′)): residual 0; p′ < 0 and p(0) > 0 iff F′ > 2F: 0 counterexamples. |
| 8 Prop 5.14 | holds | derivative identity, σ² − F factorisation, gap identity (RHS − LHS = ΠG′(2ΣΠ − λG)) and the Bayesian-stage identity: residual 0; the bound: 0 counterexamples in 1,000. |
| 9 Cor 5.2 | holds post hoc; recorded as not shown (code) | the recorded run left the residual R²(R² + 2d − √(R⁴ + 4d(R² + d)))/(R² + √(…)) (numeric 1.4 × 10⁻⁴⁸); the radicand is (R² + 2d)², so it is 0 and the identity holds (diagnosis D1). |

No item fails mathematically and none is ambiguous. One sub-claim outside the nine items was also checked post hoc: §3.3's 𝒱 − 1 = νq(q − 2)/(4 + 2νq) (residual 0).

### 2. A2: statements

No difference beyond wording in: 2.1, 2.8, 2.9, 3.2, 3.7, 4.1, 4.3, 5.1, 5.2, 5.3, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.12, 5.14, 5.15.

**2.2, kind (a).** Part (1) adds "It can change only when R² crosses or equals a critical tolerance"; part (4) adds "The positions tⱼ are needed only to locate the components"; part (3)'s equality condition is worded "lies in its own component touching neither end".

- Draft: Hence k is at most the number of interior maxima above R², with equality iff each such maximum lies in its own component touching neither end.
- Repository: so k ≤ #{interior local maxima with value > R²}, with equality iff each such maximum lies in a component that touches neither end and contains no other such maximum.
- Note: The added sentences restate (a) and (d); "its own component" means "contains no other such maximum".

**2.3, kind (a).** The draft follows the definition with an example table (the Bayesian-weight bands). The definition itself is identical to the repository's thesis-only text.

- Draft: Table: R² ≤ H All; H < R² ≤ F Lower ray; F < R² < M Window; R² ≥ M Empty (κ > 2).
- Repository: (no table in the definition; the same classes are Proposition 5.8's)

**2.4, kind (b).** The draft has no statement of Theorem 2.4; it appears only as a row of the §2.5 table. The row omits that plateau values join the critical tolerances, that a plateau can remove a component, and the ray rule at an end adjacent to a plateau.

- Draft: Plateau | R² equals a plateau value (C2′) | the plateau leaves the failure set and can split a component | Thm 2.4
- Repository: Under C2′ instead of C2, Theorem 2.2 holds with three changes: plateau values join the critical tolerances; at R² equal to a plateau value the plateau is excluded from 𝓕, which can split or remove components; an end adjacent to a plateau at value L carries a ray iff R² < L.

**2.5, kind (c).** The draft has no statement of Corollary 2.5; its §2.5 table row states the effect without the corollary's hypotheses (the two maxima separated by a lower minimum, each just below M₂ in a component touching neither end). Read as a statement, the row claims k drops by 2 whenever two maxima share a value, which the repository does not claim (it fails, for example, when one of the maxima lies in a ray component).

- Draft: Equal height | two maxima share a value M₂ | k drops by 2 at the single tolerance M₂ | Cor. 2.5
- Repository: If two interior maxima share the value M₂, are separated by a lower minimum, and just below M₂ each lies in a component touching neither end (the equality condition of Theorem 2.2(c)), then just below M₂ both count in k, and at and above M₂ both windows are gone: k drops by 2 at one tolerance. The class is otherwise unaffected.
- Note: A table summary, not a statement; on the strict reading the draft is stronger.

**2.6, kind (b).** Table row only; it omits "a flat-topped maximum acts as a maximum".

- Draft: Non-event | a stationary point that is not a turning point | none | Cor. 2.6
- Repository: A stationary point that is not a turning point never changes the class, and a flat-topped maximum acts as a maximum.

**2.7, kind (c).** Table row only; it states the scaling without the hypothesis "through a nondegenerate fold of N".

- Draft: Pair birth | a family parameter creates a minimum–maximum pair | a new band of tolerances opens from zero width; values separate like δ^(3/2), positions like δ^(1/2) | Prop. 2.7
- Repository: If a minimum–maximum pair is born at θ₀ through a nondegenerate fold of N, then at distance δ from θ₀ the turning-point positions separate like δ^{1/2} and the values like M − m ~ δ^{3/2}; the band of tolerances that sees the pair opens continuously from zero width.
- Note: A table summary, not a statement; on the strict reading the draft is stronger (a degenerate fold can give other exponents).

**3.1, kind (c).** The draft's Proposition 3.1 adds two limits to the variance formula (σ² → F when G → 0 and G²/Π → 0 as Π → 0; σ² → H = Σ/(λ + G∞) < F when G → G∞ ∈ (0, ∞)) and the noise convention. The repository's 3.1 is the model and the formula only; it states the same limits elsewhere (Theorem 3.4's hypotheses and Corollary 5.5, "L₋ = F and L₊ = H").

- Draft: If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F.
- Repository: The stationary variance (Proposition 3.1) is σ²(G, Π) = (Σ + G²/(2Π))/(λ + G).
- Note: D1 item 1 verifies the added limits. No content is new to the repository; it is moved into 3.1. The repository's Corollary 5.5 proof cites the limits; the draft's Corollary 5.5 proof cites Proposition 3.1 for them.

**3.3, kind (a).** The draft states the excess identity in normal-form coordinates (𝒱 − 1 = νq(q − 2)/(4 + 2νq), so σ² > F iff q > 2; dimensionally G > 2FΠ); the repository states it dimensionally (σ² − F = G(λG/(2Π) − Σ)/(λ(λ + G))).

- Draft: 𝒱(ν, q) − 1 = νq(q − 2)/(4 + 2νq), so σ² > F if and only if q > 2 … in dimensional form it reads G > 2FΠ.
- Repository: σ² − F = G(λG/(2Π) − Σ)/(λ(λ + G)),  σ² > F ⟺ G > 2FΠ.
- Note: Equivalent under G = qFΠ, ν = 2ΣΠ/λ² (the normal-form identity checks to 0 post hoc, t16_diag.json).

**3.4, kind (b).** The repository's statement also gives the optimal filter's classes along Π (lower ray for R² < F, Empty for R² ≥ F) and notes k = 1 for one interior maximum and k > 1 possible; the draft's statement says only that the optimal filter never windows (the classes appear in §3.4's consequences). The window condition sup q > 2 equals the repository's sup G/Π > 2F. The draft adds the table of each family's sup q.

- Draft: Some tolerance yields a window class iff sup q > 2 along the path; every R² between F and sup σ² then gives class (0, 0, k) with k ≥ 1. The optimal filter never windows along precision, because its error decreases strictly (Proposition 3.5).
- Repository: … iff sup_{Π > 0} G(Π)/Π > 2F; every R² ∈ (F, sup σ²) then gives a failure set of class (0,0,k) with k ≥ 1 (a single window when σ² has one interior maximum, as in Proposition 5.8; k > 1 is possible, Corollary 5.4). The optimal variance σ⋆²(Π) decreases strictly from F to 0, so the optimal filter never windows along Π: its classes are lower ray (R² < F) and Empty (R² ≥ F).

**3.5, kind (c).** The repository's Proposition 3.5 is the formula pair (G⋆ and σ⋆² = G⋆/Π = 2Σ/(λ + √(λ² + 2ΣΠ))). The draft's statement adds the Riccati equation, minimality over constant gains, strict decrease of σ⋆² from F, G⋆ = σ⋆²Π < FΠ for Π > 0 (strict), and q⋆ = σ⋆²/F. Each addition is in the repository elsewhere, Lemma 3.6 ("minimum value σ⋆²(Π) = G⋆/Π < F", strict) and Theorem 3.4 ("σ⋆² decreases strictly from F to 0").

- Draft: G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.
- Repository: Optimal (Kalman–Bucy) gain G⋆(Π) = −λ + √(λ² + 2ΣΠ) and optimal variance σ⋆²(Π) = G⋆/Π = 2Σ/(λ + √(λ² + 2ΣΠ)) (Proposition 3.5).
- Note: The non-strict "G⋆ = σ⋆²Π ≤ FΠ" named in the prompt is the manuscript's (Paper 1, Proposition 3, p. 4; quoted in RESULTS_t15.md), not the repository's; the repository's Lemma 3.6 is already strict. D1 item 2 verifies the strict bound.

**3.6, kind (b).** The draft states only the monotonicity on (0, G⋆) and (G⋆, ∞). The repository's statement also gives ∂σ²/∂G (in the draft's proof), the closed intervals [0, G⋆] and [G⋆, ∞), the minimum value σ⋆² = G⋆/Π < F, σ²(0, Π) = F, σ² → ∞, and σ² ≤ F iff 0 ≤ G ≤ 2FΠ.

- Draft: At fixed Π, σ² is strictly decreasing in G on (0, G⋆) and strictly increasing on (G⋆, ∞).
- Repository: … σ²(·, Π) is strictly decreasing on [0, G⋆] and strictly increasing on [G⋆, ∞), with minimum value σ⋆²(Π) = G⋆/Π < F. Moreover σ²(0, Π) = F, σ² → ∞ as G → ∞, and σ²(G, Π) ≤ F ⟺ 0 ≤ G ≤ 2FΠ, with equality exactly at G = 0 and G = 2FΠ.
- Note: The minimum value moved to the draft's Proposition 3.5; σ² ≤ F iff G ≤ 2FΠ is the draft's Corollary 3.3.

**4.2, kind (a).** The draft adds "There is no interior extremum" in case Π ≥ Π_A (implied by strict increase) and drops the middle step "c > 2FΠ".

- Draft: V_c > F iff Π < Π_B, and V_c = F iff Π = Π_B.
- Repository: V_c > F ⟺ c > 2FΠ ⟺ Π < Π_B, and V_c = F ⟺ Π = Π_B.

**4.4, kind (a).** The draft writes c⋆ and c_F explicitly ((Π + Π₀)(√(λ² + 2ΣΠ) − λ)/Π and 2FΠ/K = 2F(Π + Π₀)); with K = Π/(Π + Π₀) these equal the repository's G⋆/K and 2F(Π + Π₀).

- Draft: c⋆ = G⋆(Π)/K = (Π + Π₀)(√(λ² + 2ΣΠ) − λ)/Π … c_F = 2FΠ/K = 2F(Π + Π₀)
- Repository: c⋆ = G⋆(Π)/K … c_F = 2F(Π + Π₀)

**4.5, kind (a).** Same classes. The draft's last row names the upper ray (c_R, ∞), a symbol it does not define (the repository writes no symbol).

- Draft: R² ≥ F | Upper ray (c_R, ∞), equal to (c_F, ∞) at R² = F
- Repository: upper ray (R² ≥ F, equal to (c_F, ∞) at R² = F)

**5.4, kind (a).** Title only ("unbounded windows for regular gains" vs "unbounded complexity inside the model"); "the regularity of Theorem 3.4" vs "the starting study's regularity", with the same conditions written out in both.

- Draft: Corollary 5.4 (unbounded windows for regular gains). For every k ≥ 1 there is a C^∞ gain schedule with the regularity of Theorem 3.4 (…) whose failure set at R² = 1.25F has exactly k windows.
- Repository: Corollary 5.4 (unbounded complexity inside the model). For every k ≥ 1 there is a C^∞ gain schedule satisfying the starting study's regularity (…) whose failure set at R² = 1.25F has exactly k windows.

**5.11, kind (a).** The draft writes H = Σ/(λ + G₀) explicitly (the repository's H with G∞ = G₀) and adds a remark after the statement.

- Draft: σ² decreases strictly from ∞ to H = Σ/(λ + G₀).
- Repository: σ² decreases strictly from ∞ to H.

**5.13, kind (a).** The draft writes "All (R² ≤ H)" in the no-pair case where the repository writes "All"; the onset is called "the window condition of Theorem 3.4" instead of "the starting study's window onset".

- Draft: Without the pair: All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F).
- Repository: Without the pair: All, lower ray (H < R² < F), Empty (R² ≥ F).

**The two edits named in the prompt.** "G⋆ < FΠ for Π > 0" (3.5): the non-strict ≤ is the manuscript's (Paper 1, Proposition 3, p. 4), not the repository's, whose Lemma 3.6 already states σ⋆² = G⋆/Π < F; the strict form holds (D1 item 2). Corollary 5.4's title differs; the statement does not.

**Should the thesis render carry the draft's wording of 3.1, 3.5, 3.6 and 3.7?** 3.7 is already identical. 3.1 and 3.5 have no labelled statement in the repository (only §1's model paragraph and a bullet), and the draft's statements are verified (D1 items 1–2), so importing them as thesis-only texts would give both a statement. 3.6 should move with 3.5: the draft moves the minimum value into 3.5 and "σ² ≤ F iff G ≤ 2FΠ" into 3.3, so taking the draft's 3.6 alone would drop content the repository states. Not changed (Part C.4).

### 3. A3: numbers

| # | Value | Printed | Computed or stored | Source | Match |
|---|---|---|---|---|---|
| 1 | kappa = 100, R2 = 0.05: lower end of the failure set | 1/9 | yes | formula (exact roots) | yes |
| 1 | kappa = 100, R2 = 0.05: upper end of the failure set | 4 | yes | formula (exact roots) | yes |
| 1 | failure set is between the roots (sigma2 > R2 at the midpoint) | (1/9, 4) | yes | formula | yes |
| 1 | factor 36 = 4/(1/9) | 36 | 36.0 | formula | yes |
| 2 | Pi0^pair, n = 1.5 (formula) | 30.243 | 30.2430947474 | formula c phi_n(t*)/(2 n Sigma) | yes |
| 2 | Pi0^pair, n = 1.5 (Task 13 regression) | 30.243 | 30.2430947474 | t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression | yes |
| 2 | Pi0^pair, n = 2 (formula) | 31.475 | 31.4750497595 | formula c phi_n(t*)/(2 n Sigma) | yes |
| 2 | Pi0^pair, n = 2 (Task 13 regression) | 31.475 | 31.4750497595 | t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression | yes |
| 2 | Pi0^pair, n = 3 (formula) | 37.820 | 37.8200022316 | formula c phi_n(t*)/(2 n Sigma) | yes |
| 2 | Pi0^pair, n = 3 (Task 13 regression) | 37.820 | 37.8200022316 | t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression | yes |
| 2 | Pi0^pair, n = 4 (formula) | 44.180 | 44.1796834278 | formula c phi_n(t*)/(2 n Sigma) | yes |
| 2 | Pi0^pair, n = 4 (Task 13 regression) | 44.180 | 44.1796834278 | t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression | yes |
| 2 | Pi0^pair, n = 8 (formula) | 62.711 | 62.7113145769 | formula c phi_n(t*)/(2 n Sigma) | yes |
| 2 | Pi0^pair, n = 8 (Task 13 regression) | 62.711 | 62.7113145769 | t13/results/t13_partA_numeric_A4_A5_A7.json A5.regression | yes |
| 3 | M/F misspecified Kalman (formula) | 17.575 | 17.5750544106 | formula G_M, Pi_M (Prop. 5.9) | yes |
| 3 | M/F Bayesian weight (formula) | 9.2875 | 9.2875272053 | formula (Prop. 5.8 turning point) | yes |
| 3 | ratio (formula) | 1.892 | 1.89232871378 | formula | yes |
| 3 | 17.575 (Task 13 audit) | 17.575 | 17.5750544106 | t13/results/t13_audit_numbers.json | yes |
| 3 | 9.2875 (Task 13 audit) | 9.2875 | 9.2875272053 | t13/results/t13_audit_numbers.json | yes |
| 3 | 1.892 (Task 13 audit) | 1.892 | 1.89232871378 | t13/results/t13_audit_numbers.json | yes |
| 4 | pi_R at R2 = 0.6F | 222.2 | 222.222222222 | formula | yes |
| 5 | c lambda/(4 Sigma) | 25 | 25.0 | formula | yes |
| 5 | sup q <= 2 for the Hill gain at Pi0 = 25.0 | <= 2 | yes | grid maximum 2.0 | yes |
| 5 | sup q <= 2 for the Hill gain at Pi0 = 31.475 | <= 2 | yes | grid maximum 1.588562351 | yes |
| 6 | t*^2 = 2 sqrt 3 - 3 (n = 2) | 2√3 − 3 | yes | formula | yes |
| 7 | Pi_B | 50 | 50.0 | formula | yes |
| 7 | Pi_A | 150 | 150.0 | formula | yes |
| 7 | case at Pi = 1.0 | P3 | yes | formula | yes |
| 7 | Pi0* at Pi = 1.0 | 99.498 | 99.4975246918 | formula | yes |
| 7 | sigma*^2 at Pi = 1.0 | 0.0099505 | 0.00995049383621 | formula | yes |
| 7 | V_c at Pi = 1.0 | 0.255 | 0.255 | formula | yes |
| 7 | case at Pi = 60.0 | P2 | yes | formula | yes |
| 7 | Pi0* at Pi = 60.0 | 64.162 | 64.161984871 | formula | yes |
| 7 | sigma*^2 at Pi = 60.0 | 0.0080540 | 0.00805399495699 | formula | yes |
| 7 | V_c at Pi = 60.0 | 0.0091667 | 0.00916666666667 | formula | yes |
| 7 | case at Pi = 500.0 | P1 | yes | formula | yes |
| 7 | V_c at Pi = 500.0 | 0.0055 | 0.0055 | formula | yes |
| 7 | sigma*^2 below F at Pi = 1 | 0.5% | 0.00495061637922 | formula | yes |
| 7 | two-ray band width at Pi = 60, relative to F | 11% | 0.111267170968 | formula | yes |
| 8 | c* | 0.019901 | 0.0199009876724 | formula | yes |
| 8 | sigma*^2 | 0.0099505 | 0.00995049383621 | formula | yes |
| 8 | c_F | 0.04 | 0.04 | formula | yes |
| 9 | mixed band median | 5 × 10^-4 | 0.000498227933786 | t10/results/t10_4.json band_rel_median | yes |
| 9 | mixed band minimum | 4 × 10^-22 | 4.42721151149e-22 | t10_4.json band_rel_min | yes |
| 9 | mixed band maximum | 0.96 | 0.961781026043 | t10_4.json band_rel_max | yes |
| 9 | mixed band with no window above F | 16% | 0.161668036154 | t10_4.json frac_M_lt_F | yes |
| 10 | target constructions passed | 101 | 101.0 | t10_2.json every[].pass | yes |
| 10 | target constructions | 101 | 101.0 | t10_2.json every | yes |
| 10 | forbidden targets blocked | 24 | 24.0 | t10_2.json forbidden[].blocked | yes |
| 10 | forbidden targets | 24 | 24.0 | t10_2.json forbidden | yes |
| 10 | supplementary construction k = 1 to 5, all pass | k = 1 to 5 | yes | t10_2.json a13_supp | yes |
| 10 | G(1e12)/G(1e11) - 1 | 6 × 10^-10 | 5.9999999996e-10 | t10_2.json a13_supp.ratio_minus_1 | yes |
| 11 | misspecified Kalman sets | 2000 | 2000.0 | t10_3.json families.misspec.n | yes |
| 11 | misspecified Kalman sets passing | 2000 | 2000.0 | t10_3.json families.misspec n - n_fail | yes |
| 11 | Hill n = 2 sets with the pair (root-count check) | 961 | 961.0 | t10_3.json families.hill.tp_hist_n2['2'] | yes |
| 11 | root-count disagreements | 0 | 0.0 | t10_3.json exact_count_disagreements | yes |
| 11 | Task 10 census sets | 10000 | 10000.0 | t10_3.json families.hill.n | yes |
| 11 | turning-point position error (Bayes) | 6 × 10^-31 | 6.04167987717e-31 | t10_3.json families.bayes.max_pos_rel_err | yes |
| 11 | two-channel Bayes (max, min, max) | 7 | 7.0 | t10_3.json exploratory.bayes2 | yes |
| 11 | two-channel Bayes sets | 2000 | 2000.0 | t10_3.json exploratory.bayes2.n | yes |
| 11 | two-channel Hill (min, max, min, max) | 63 | 63.0 | t10_3.json exploratory.hill2 | yes |
| 11 | two-channel Hill sets | 2000 | 2000.0 | t10_3.json exploratory.hill2.n | yes |
| 12 | Hill sets with two turning points | 4868 | 4868.0 | t10_4.json n_sets | yes |
| 12 | tolerances tested | 77888 | 77888.0 | t10_4.json n_tests | yes |
| 13 | A5 random sets | 5000 | 5000.0 | t13 A5.n | yes |
| 13 | n range lower end 1.01 | 1.01 | yes | t13/t13_partA_numeric.py (10**uniform(log10 1.01, 1)) | yes |
| 14 | T8.3 classes correct | 62 | 62.0 | results/t8_3.json n_match | yes |
| 14 | T8.3 classes tested | 62 | 62.0 | results/t8_3.json n_tests | yes |
| 14 | ±10^-6 relative tests | 10^-6 | yes | REPORT.md | yes |
| 14 | T8.4 sets | 20000 | 20000.0 | results/t8_4.json N | yes |
| 14 | T8.4 classifications | 10^6 | yes | results/t8_4.json total_classifications | yes |
| 14 | five sweeps | 5 | 5.0 | t8_no_window.py SWEEPS | yes |
| 15 | persisting route disagreements, row 12 | 122 | 122.0 | t13_audit_classes.json rows[12] | yes |
| 15 | 1,000 fresh sets per design-sweep row (10, 11, 12) | 1000 | yes | t13_audit_classes.json rows 10-12 curves | yes |
| 16 | T10.7 classifications | 10^6 | yes | t10/results/t10_7.json total | yes |
| 16 | T12 Part C classifications | 4.4 × 10^6 | 4400000.0 | t12/results/t12_blind.json total | yes |
| 17 | relative prior dip 10^(-32,880,317) | 10^-32880317 | yes | t12/RESULTS_t12.md | yes |
| 18 | C11 curves | 1000 | 1000.0 | t15_partG.json C11.curves | yes |
| 18 | C11 tolerances per curve >= 50 | 50 | 50.0 | C11.min_tolerances_per_curve | yes |
| 18 | C11 classifications | 200000 | 200000.0 | C11.classifications | yes |
| 18 | C12 perturbations | 1000 | 1000.0 | C12.cases_run | yes |
| 18 | C12 curves | 500 | 500.0 | C12.curves | yes |
| 18 | illustration amplitude/eta | 0.9 | 0.9 | ILL.amplitude_over_eta | yes |
| 18 | illustration upper ray -> (0, 1, 4) | upper ray -> (0, 1, 4) | yes | ILL.class_before/after | yes |

### 4. A4: references

No broken reference. 30 citation groups resolve; numbers 1–45 first appear in order; 214 typed references (Theorem, Prop., Cor., …, ranges expanded) name a result of that type; 34 table labels exist; Figure B.1–B.6 references (6) exist. Excluded as intervals: `[0, ∞]`; `[1.01, 10]`.

### 5. Part B: Π_c

The B.4 script (`t13/t13_figures_paper2.py`) uses λ = 1, Σ = 0.01, c = 1, κ = 1.5, Π₀ = c/(κF) = 66.67, the parameters the description states. It takes Π_c as the first point of its 1,500-point log grid where cΠ/(Π + Π₀) < G⋆, and prints it to three figures: 56.7. The root of cΠ/(Π + Π₀) = −λ + √(λ² + 2ΣΠ) is 56.204689, the value Task 10 also recorded; the description's 56.7 is the grid value, not a computation error in the formula. The description now gives Π_c = 56.20 (figures.yaml, Appendix B, the B.4 caption and the figs_thesis README). The image shows no Π_c and is unchanged, as is the curve (the bumps are still placed relative to the grid value). The Task 13 paper outputs (`figs_paper2/fig02_realizability.txt`, `figs_paper2/README.md`) keep 56.7, and re-running the T13 script prints 56.7 again.

### 6. Other disagreements in chapters 1–5 (listed, not resolved)

1. **"961 random sets" (§5.6, Theorem 5.12(b)).** Task 10's exact root-count check ran on all 2,000 sets with n = 2 (`t10/t10_census.py`), of which 961 had the pair and 1,039 none; 0 disagreements. The repository's own label also says "961 random sets". The count of sets checked is 2,000.
2. **§1.5 "Every class is then available to some gain (Corollary 5.3)".** Corollary 5.3 restricts R² < F to classes with ℓ = 1; the sentence is right for R² ≥ F, or for "some tolerance".
3. **Proposition 4.5 uses c_R** ("Upper ray (c_R, ∞)") without defining it.
4. **§2.5 table rows for 2.4–2.7** are the draft's only statements of those results; rows for 2.5 and 2.7 leave out hypotheses (see A2).
5. **Citations written \[n\] in the renders** are not seen by Task 15's bracket pattern, which D7 keeps: 2 such groups in the thesis renders (classification/Stages_0_4_Thesis.md). Neither check tests them.
6. **Appendix D's T15 entry** quotes the phrase "Paper 1", and Appendix E names figure labels without "Figure"; both trip D6's pre-registered pattern (above).
