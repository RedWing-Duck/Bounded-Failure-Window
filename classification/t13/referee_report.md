# Task 13 C4: independent referee report and dispositions

The referee was a separate agent that had not seen the derivation history. It received only
`Stages_0_4_Consolidated.md` (the draft as committed at `5ac589c`, after the C1 fix) and the instruction to report
(a) proof steps it cannot follow or believes wrong, (b) claims stronger than their proofs, (c) missing equality cases.
Its report is reproduced verbatim below, followed by my disposition of each point.

## Report (verbatim)

```
REFEREE REPORT

I read only Stages_0_4_Consolidated.md. I re-derived the algebra of each result named in the brief and spot-checked the worked examples with mpmath/sympy in scratch. These all reproduce: V(1), P(1), P(10), the misspecified-Kalman peak 17.575 and ratio 1.892, the D1 maximum 0.20457 at Δt = 2.4645, the avg dip 0.0099875 at Δt = 200, and Π0^pair for n = 1.5, 2, 3, 4. I found no error in the core proofs of Theorems 2, 25, 32(b),(c), 56 or 69, or in Propositions 9–12, 20, 41, 42 or 71. The real problems are two wrong class or condition claims (D2 and the D1-avg row), several unproved assumptions or limits, and a few equality cases.

1. [a/b] Proposition 29, plus Proposition 31's D2 row and synthesis rows 27–29. The results silently assume c < 2. For c > 2 the D2 gain L tends to c > 2, the excess test L/(2−L) > φ is no longer equivalent to P⁺ > F, and the formula for Δt_E has a negative denominator. Counterexample (λ = 1, Σ = 0.01, Π = Π0 = 1, c = 3, so κ = 300 > 2): P⁺/F = 233, 77, 12.7, 4.9 at Δt = 1, 10, 100, 1000, and post → (1−c)²F = 4F > F. The excess set is all of (0, ∞), not a lower ray. Prior and avg also tend to F from above, not from below as Proposition 31 states. From L(L(r+F) − 2F) > 0, for c > 2 the excess set is All when κ > 2, and the upper ray Δt > (2FΠ0 − c)/((c−2)FΠ) when κ < 2. Suggested fix: state 0 < c < 2 (with c ≤ 1 if under-relaxation is intended) in the D2 definition, or add the c ≥ 2 cases.

2. [a] Synthesis row 26 (D1 avg, "as row 25": 2R iff G > 2FΠ) is false in the "only if" direction. Counterexample: λ = 1, Σ = 0.01, Π = 1, G = 0.019 < 2FΠ = 0.02. avg/F is 0.999068 at Δt → 0, rises to 0.999165 near Δt = 10, falls to 0.998652 near Δt = 158, then returns to 1 from below. For R²/F in (0.998652, 0.999068) the failure set is two rays. Proposition 36 proves only the "if" direction. For row 25 (prior) the "only if" is not proved either; I found no counterexample in a quick scan. Suggested fix: say "2R if G > 2FΠ" and list the extra 2R cases as numerical (Numerical result 37).

3. [b] Theorem 6: "every R² ∈ (F, sup σ²) then gives a window". Read as class (0,0,1), this contradicts Corollary 48, which gives regular gains with k windows at R² = 1.25F. The proof only supports ℓ = u = 0 with k ≥ 1. Suggested fix: "gives a failure set of class (0,0,k), k ≥ 1 (a single window when σ² has one interior maximum, e.g. Proposition 7)".

4. [c] Section 6.2 "Optimal classes" (prior and avg), and by analogy the M-I rows 33–34. The text says "All (R² < σ*²), upper ray, …". At R² = σ*² the curve starts at σ*² and increases strictly, so it approaches from above and the class is All; the equality row is missing or implicitly wrong. Suggested fix: "All (R² ≤ σ*²), upper ray (σ*² < R² < F), Empty (R² ≥ F)", which matches the convention used in Propositions 15, 23 and 71.

5. [b] Theorem 35 and rows 33–34. The proof is not checkable from this document, which calls itself self-contained:
   - "Task 11's quadratic" (a2, a1, a0) is never written down, so the leading coefficient, the product of roots, the claim "the cleared quadratic equals its leading coefficient at p = 1" and the resultant cannot be verified.
   - The endpoint limits for M-I (σ*² as Δt → 0, F as Δt → ∞, and their approach directions) are proved nowhere; Proposition 31 covers M-P only. Rows 33–34 are nonetheless declared "complete".

   The resultant step itself is valid, and E² + 2xE − 1 = −2e^{−x}(sinh x − x) checks. Suggested fix: print the quadratic, prove the two limits, then keep the resultant argument.

6. [b/c] Proposition 30 (D3). No proof appears in the document. The excess-set formula agrees with a direct computation in 2,000 random cases, so it is probably right. Two specific problems:
   - "Census shape: lower ray or Empty" is a numerical observation placed inside a "Proposition (proved)".
   - The onset "iff ρ > 2 + u" is drawn from the small-Δt limit, but at ρ = 2 + u the first- and second-order terms cancel exactly. With x = λΔt, the expression s(1−φ)(ρ(1+φ)−2) − 4φ equals −u(3u² + 6u + 4)x³/6 + O(x⁴). So the equality case needs this cubic term; it does hold (no excess near 0), but the stated argument does not show it.

   Suggested fix: add the expansion; prove or relabel the shape claim.

7. [b] Proposition 36 ("two rays, or (1,1,k)") and Corollary 66. Both use C2 or C2′ (finitely many turning points or plateaus, continuity) without establishing it:
   - For the sampled relays, finiteness is exactly the open Conjecture 38.
   - For an arbitrary causally ordered sweep, P is only shown non-increasing. Without continuity a superlevel set can be (θ₋, x], which is not open (C3), and Theorem 3 needs finitely many plateaus.

   Suggested fix: state "assuming C2" in Proposition 36. In Corollary 66, say "an initial segment", or add continuity of P as a hypothesis.

8. [a, minor] Corollary 48: "each bump crosses 1.25F exactly twice" is not justified. v_B is strictly decreasing, so v_B plus a unimodal bump need not be unimodal; on the rising flank v can wiggle across 1.25F more than twice. Suggested fix: define v directly on each bump interval as strictly increasing then strictly decreasing, keeping it ≥ v_B and smooth at the support ends (for example by requiring b′ > |v_B′| on the rising flank).

9. [b] Corollary 59 (equal-height maxima). "Just below M2 both count in k" fails if either maximum's component reaches an end. Example: L₋ > M2 with no dip below R² between θ₋ and the first maximum; that maximum then lies in the lower ray. Suggested fix: add the hypothesis that both maxima lie in windows, which is the equality condition of Theorem 2(c).

10. [b, minor] Theorem 2(d) and the equality rows of Propositions 10 and 12. The proof of (d) points to the construction in (a), which assumes R² ∉ C. At interior critical tolerances the rule that is needed (a minimum with value R² is removed and splits a component; a maximum with value R² contributes nothing) is used, for example "the domain minus Π0*", but never stated. The extension is immediate, since {σ² > R²} on each piece is determined for every R², but it should be written. Also, the approach directions in (d) are redundant: they are determined by the ordered sequence under C2.

11. [b, wording] Proposition 9, first bullet: "L₋ = V_c and L₊ = F, approached from below" reads as if both limits are approached from below. This contradicts the second bullet (V_c from above when c ≤ G*). Suggested fix: "L₊ = F, approached from below; V_c's direction: see below."

12. [b, minor] Proposition 33. "By Theorem 65 an ordering would move all metrics the same way" needs one unstated step. Theorem 65 gives a pointwise-in-t inequality between two cyclostationary error curves with different periods. Post and prior are the minimum and supremum of each curve over its own period, and avg is the time mean. Then P_θ₂ ≤ P_θ₁ pointwise gives min ≤ min, sup ≤ sup and mean ≤ mean. Suggested fix: add this sentence.

13. [b, minor] Theorem 69 and its Reading. The Reading says causal ordering, pathwise (Blackwell) ordering and spectral dominance "coincide", but the theorem lists only (i)–(iii). The proof of (i) ⇒ (ii) uses only the two-sided smoothing inequality, which any non-causal garbling also gives, so pathwise ⇒ (ii) does follow. It should be stated as part (iv). The frequency-localization step should also say it normalises |ĝ|² by L and uses the approximate-identity lemma at Lebesgue points; the ±ω0 cross terms vanish because ω0 ≠ 0 and spectra are even. The argument is otherwise sound.

14. [c, minor] Proposition 54, case g = 2F. The parenthetical "lower ray for R² < F, Empty at R² ≥ F" omits All for R² ≤ H. The final class list is correct. Suggested fix: "All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F)".

Points checked and found correct:
- Theorem 2 (a)–(c) and Theorem 3.
- Propositions 7, 9–12, including every equality row (P1–P3, Π = Π_A, Π = Π_B, R² = σ*², R² = F), and Theorem 8.
- Lemma 13, Propositions 14–19, Proposition 20 (orthogonality, the a = 1/τ case, the G → ∞ endpoint, compactness), Proposition 21 and Theorem 24 (including the β = 0 and β = 2 limits).
- Theorem 25: the identity Φ_ττ = P²(β + (2−β)λ²τ²)/τ³ checks, and so does the "two strict maxima enclose a minimum" argument.
- Theorem 32 (a), (b), (c): every displayed identity checks.
- Propositions 41–43: formulas, w_M, derivative numerators, and the equality cases ρ = 2 and λ′ = λ/2.
- Propositions 53 and 57 (both tables, with R² = m and M = F handled correctly).
- Theorem 56: the R(T) coefficients, Descartes' rule, the n = 2 factorisation and φ*.
- Propositions 68 and 70, Proposition 71 (including All at R² ≤ σ*²) and Proposition 73.
- Every other row of the synthesis matrix agrees with its cited result.

Overall: The analytic core is sound. The critical-tolerance theorem, the design-sweep and τ-sweep classifications with their equality rows, the strict gap, β-unimodality, M-P monotonicity, the general-n Hill theorem and the spectral characterisation of causal garblings all survive a line-by-line check, and every worked number I recomputed is right. The errors sit in the Δt (sampled-filter) section and the synthesis matrix. D2 needs an unstated c < 2 (c = 3 is a counterexample), and row 26's "2R iff G > 2FΠ" is false for avg (G = 0.019 is a counterexample). Theorem 35 depends on a quadratic the document never prints and on M-I endpoint limits proved nowhere. Proposition 30 and the class claims for sampled relays mix proved and numerical statements. Theorem 6, Corollaries 48, 59 and 66, Proposition 36, and the optimal prior/avg equality row need small rewording or added hypotheses. None of this touches the main theorems, but items 1, 2 and 5 should be fixed before the paper relies on rows 25–34.
```

## Dispositions

All 14 points are **valid**. Points 1, 2 and 6 were reproduced independently before acting (`t12_common` at 40 digits: D2 with
c = 3 gives P⁺/F = 233.1, 77.36, 12.7, 4.886 at Δt = 1, 10, 100, 1000 and a prior that tends to F from above; D1 avg with
G = 0.019 has a maximum at Δt = 17.805 (avg/F = 0.999186) and a minimum at Δt = 149.47 (0.9986504) after starting at 0.9990677;
SymPy gives the ρ = 2 + u expansion −u(3u² + 6u + 4)x³/6). Every fix is logged in the document's change log (rows 31–44).

| # | Valid? | Fix |
|---|---|---|
| 1 | valid (document error) | D2 now requires $0 < c < 2$ in the model definition (all Task 12 and Task 13 draws had $c < 2$); the $c \ge 2$ cases are stated as a remark (All for $\kappa > 2$, upper ray otherwise). |
| 2 | valid (document error) | Rows 25–26: "2R if $G > 2F\Pi$ (Proposition 36); also found for $G \le 2F\Pi$ in avg (Numerical result 37)". The class lists were already correct. |
| 3 | valid | Theorem 6: "a failure set of class $(0,0,k)$, $k \ge 1$". |
| 4 | valid (missing equality row) | Optimal prior/avg classes and rows 22–23, 33–34: All ($R^2 \le \sigma_\star^2$). |
| 5 | valid | Theorem 35 rewritten with the quadratic printed. The referee's request led to a shorter proof: $a_0 = -a_1$ exactly, so $p = 2/(1 + \sqrt{1 + 2u/k(x)})$ with $k(x) = (1+u)x\coth(x/2) - 2u$, strictly increasing from 2 to $\infty$; this gives monotonicity and both limits. Verified in `t13_A3_closed.py` (11/11). The resultant argument is kept as a second route. |
| 6 | valid | Proposition 30 now has a proof (via Lemma 27 and the D3 quadratic) and the cubic term at $\rho = 2 + u$; the census shape moved to Numerical result 37. |
| 7 | valid | Proposition 36 states "assuming C2"; Corollary 66 adds continuity of $P$ (and C2′ for the class statement) and otherwise says "an initial segment". |
| 8 | valid | Corollary 48's construction now defines $v$ on each bump support as strictly increasing then strictly decreasing, $\ge v_B$, smooth at the support ends. |
| 9 | valid | Corollary 59 adds the hypothesis that both maxima lie in windows. |
| 10 | valid | Theorem 2(d) proof now states the rule at interior critical tolerances; notes that the approach directions follow from the sequence under C2. |
| 11 | valid (wording) | Proposition 9 first bullet reworded. |
| 12 | valid | Proposition 33 adds the min/sup/mean step. |
| 13 | valid | Theorem 69 adds (iv) pathwise (non-causal) Blackwell ordering, and the localization detail. |
| 14 | valid (missing equality row) | Proposition 54's $g = 2F$ case lists All for $R^2 \le H$. |
