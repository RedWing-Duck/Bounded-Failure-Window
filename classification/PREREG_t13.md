# Pre-registration — Task 13: finalize Stages 0–4 (close open items, consolidate, audit, reproduce)

Committed **before** any Task 13 script is written to disk or run. Not edited after its commit. Failures stay recorded,
are diagnosed post hoc in `t13/*_diag.py` and attributed to the **document**, the **code** or the **criterion**. Only
genuine code bugs are fixed, each documented in `t13/RESULTS_t13.md`. Nothing in `verification/` is modified.

**Inputs** (all in `classification/`): `Bounded_Failure_Window_Classification_Roadmap_v2-1.md`,
`Stage_0_1_Classification_Results.md` (verified by Task 8; its report is `REPORT.md`, which plays the role of
`RESULTS_t8`), `Stage_2_Tau_Sweep_Results.md` (Task 9), `Stage_3_Falsification_Results.md` (Task 10; Task 10 tested
`Stage_3_Plan.md`, from which this document was written), `Stage_4_Optimality_Results.md` (Task 11),
`Stage_2_Completion_Results.md` (Task 12), `PREREG_t8`…`PREREG_t12`, `t9/`…`t12/RESULTS_t*.md` and all code.
The Roadmap and the Stage 3 results document were added to the repository with this commit (they were supplied for
Task 13). `Stage_2_Completion_Results.md` was committed at `645fc13`.

**Disclosure (protocol: anything known before the run that bears on an outcome).** While reading the inputs I
sketched proof routes for several Part A items (no code was run). The routes are pre-registered below as exact
identities so that their checks are fixed in advance. Expected outcomes from the sketches: A1 proved (verification),
A2 proved (new route, below), A4 proved (new route), A5 proved (new route), A7 proved (new route), A8 proved (new
route, subject to the referee pass). A3 and A6 have no route; they are expected to stay unresolved. These are
expectations, not results; each outcome is decided only by the pre-registered checks.

Tools: Python 3, NumPy, SciPy, SymPy, Matplotlib, mpmath only. Seeds: Part A 13001–13009; Part C 13100–13199;
Part D uses the seeds already in the Task 8–12 code.

## Common method (Tasks 9–12, mandatory)
- mpmath at ≥ 50 digits for turning points (dps 50; 60 for flagged re-runs; 100 for the Part A chains). Turning points
  are sign changes of an analytic (SymPy-derived or closed-form) derivative with the T10 method (12 points/decade,
  adaptive golden-section step at local minima of |derivative|, bisection to width 1e-30 in log10 θ, zero tolerance
  1e-40·|f|/θ). Never from differences of the curve; `mp.diff` is used only where Tasks 11–12 already used it (M-I).
- Components by root-finding with the two-route classifier of Tasks 10–12 (`t10/classify.py`, unchanged).
- Limits and brackets: the proved asymptotics in the table of Part C below, with each outer bracket set from the
  approach rate. Zero limits are absolute (|f(x_end)| ≤ 1e-30), infinite limits ≥ 1e30, finite limits within 1e-20
  relative (`t11_common.analyse_with_limits`).
- Fold exponents (if used): positions 1/2, values 3/2.
- SymPy route for identities: `simplify`; else `simplify(together(expand))`; else factor radicands then simplify;
  exact 0 only. Sign claims via identities with manifestly signed right sides. Every `sympy.limit` result is also
  checked by a series route (substitution x = 1/t, exponentially small terms set to 0 beyond all orders, `series`).
- Exponential underflow: where a factor such as e^{−2λΔt} would fall below working precision, the range is
  restricted (λΔt ≤ 50 at 100 digits, so e^{−100} ≈ 4e-44 ≫ 1e-100) or the precision is raised; such points are never
  counted as violations.

---

## Part A — close the open items

Outcome rule (each item): **proved** iff every pre-registered identity reduces to 0, every sign claim is shown by a
manifestly signed form, and the numerical check (if any) has 0 failures; **disproved** iff a counterexample is found
and confirmed at ≥ 60 digits; otherwise **unresolved**, reported with the best partial result and the numerical
evidence. For each item the numerical sets are drawn log-uniformly over four decades (λ, Σ, Π, K, c, Π0, ρ ∈ [1e-2,
1e2]) unless stated.

### A1 — Prop. 2.6(b) (optimal M-P prior increasing in Δt). Seed 13001.
x = λΔt, s = 1 − e^{−2x}, s′ = 2e^{−2x}, r = λ/(Πx), q = sF; M = P⁻ is the positive root of
f(M) = M² + s(r − F)M − sFr.
Symbolic checks (each must reduce to 0 or be manifestly signed):
1. DARE: M² + M(rs − q) − qr ≡ f(M) with q = sF.
2. f′(M) = 2M + s(r − F) > 0 at the root (product of roots −sFr < 0).
3. Implicit derivative: −f_x/f_M has numerator FMs′ − (F − M) r (s/x − s′) (with r′ = −r/x).
4. Identity on the root: sr(F − M) − M(M − sF) ≡ −f(M).
5. Rewritten bracket: FMs′ − (F − M)r(s/x − s′) ≡ M[Fs′ − (M − sF)(s/x − s′)/s] on f = 0.
6. f(F) = F²(1 − s) > 0 and f(sF) = −sFr(1 − s) < 0, hence sF < M < F.
7. s/x − s′ > 0 for x > 0 (s concave, s(0) = 0; identity: (s − xs′)/x with s − xs′ = 1 − e^{−2x}(1 + 2x) > 0 by
   e^{y} > 1 + y).
8. Sufficient inequality s s′ ≥ (1 − s)(s/x − s′) ⇔ s′ ≥ (1 − s)s/x ⇔ 2x ≥ 1 − e^{−2x} (identities with s, s′).
Numerical: 10,000 sets (λ, Σ, Π), x log-uniform on [1e-8, 50], mpmath 100 digits: dM/dx > 0 (analytic implicit
derivative) and every link (sF < M < F; s/x > s′; 0 < M − sF < F(1 − s); bracket > 0; 2x ≥ 1 − e^{−2x}).
**Pass:** all symbolic items and 0 numerical failures.

### A2 — Num. 2.6c (optimal M-P time-average P̄ increasing). Seed 13002.
Route: P⁺ = F/(1 + μ), μ = m/s with m² + s(1 − φ)m − sφ = 0 (D3 quadratic at ρ = 1), φ = FΠΔt = w x, w = FΠ/λ, so
μ² + (1 − φ)μ − φ/s = 0 and P̄ = F − (F/2)Q, Q = μ s/((1 + μ) x). P̄ increasing ⇔ Q decreasing.
Symbolic checks:
1. P̄ − [F − (F − M)(e^{2x} − 1)/(2x)] ≡ 0 and P̄ − [F − (F/2)Q] ≡ 0 with M = a²P⁺ + q.
2. μ equation and P⁺ = F/(1 + μ) satisfy the Kalman recursion (P⁺ = Mr/(M + r), M = a²P⁺ + q).
3. μ > 0 and μ + 1 − φ = (φ/s)/μ > 0, so 2 + 2μ − φ > φ > 0.
4. Implicit: (2μ + 1 − φ)μ′ ≡ φμ/x + μ(μ + 1 − φ)E with E = 1/x − s′/s > 0.
5. d ln Q/dx ≡ μ′/(μ(1 + μ)) − E, and the identity
   (1 + μ)(2μ + 1 − φ)E − [φ/x + (μ + 1 − φ)E] ≡ Eμ(2 + 2μ − φ) − w, together with μ(2 + 2μ − φ) ≡ φ(2/s + μ).
6. Hence d ln Q/dx < 0 ⇔ w < wxE(2/s + μ) ⇐ (1 − xs′/s)(2/s) ≥ 1 ⇔ 1 − e^{−4x} ≥ 4x e^{−2x} ⇔ sinh(2x) ≥ 2x
   (identity checks for each ⇔ step; the last by the series of sinh y − y with positive coefficients).
Numerical: the A1 sets: dP̄/dx > 0 (analytic) and every link (μ > 0, μ > φ − 1, E > 0, (1 − xs′/s)(2/s) ≥ 1).
**Pass:** all symbolic items and 0 numerical failures.

### A3 — Num. 2.8 / 4.10a (M-I optimal monotone in Δt). Seed 13003.
Attempt: scalar reduction (Task 11's closed form `samp_p` is the positive root of a2 p² + a1 p + a0 = 0); implicit
derivative dp/dx = −(a2′p² + a1′p + a0′)/(2a2p + a1); SymPy attempt to show the numerator negative at the root
(substitution E = e^{−x}, resultant with the quadratic, factor, manifestly signed form), 1,800 s timeout per metric.
Garbling route recorded as an argument only (nested chains are Cor. 4.9; non-nested pairs are the gap).
Numerical: 10,000 sets (λ, Σ, Π), x log-uniform on [1e-8, 50], 100 digits: dP_a/dx > 0 and dP_b/dx > 0 from the
SymPy-differentiated closed form (analytic). **Outcome:** proved only if the symbolic sign is established;
disproved if a numerical violation is confirmed at 120 digits; otherwise unresolved with these numbers.

### A4 — Num. 4.6a (power family unimodal for 0 < β < 2). Seed 13004.
Route: P is the positive root of Φ(τ, P) = A P² + B P − C, A = (1 − λτ)²/τ, B = 4(Σ + λv), C = 4Σv,
v = (K/2)τ^{β−1}. Φ_P = 2AP + B > 0. At a critical point (P′ = 0): Φ_τ = A′P² − 4v′(Σ − λP) = 0 and
P″ = −Φ_ττ/Φ_P with Φ_ττ = A″P² − 4v″(Σ − λP).
Symbolic checks:
1. A′ = (λ²τ² − 1)/τ², A″ = 2/τ³, v′/v = (β − 1)/τ, v″/v′ = (β − 2)/τ (β ≠ 1).
2. On Φ_τ = 0 (β ≠ 1): Φ_ττ ≡ P²(A″ − A′v″/v′) ≡ P²[β + (2 − β)λ²τ²]/τ³ (> 0 for 0 < β < 2).
3. β = 1: Φ_τ = A′P², so the only critical point is τ = 1/λ (Prop. 6.1 recovered).
4. Every critical point is a strict local maximum ⇒ at most one critical point (between two strict maxima the
   minimum on the closed interval is an interior critical point that is not a strict maximum); existence from
   Theorem 4.6 (P → 0 at both ends, P > 0). Hence exactly one turning point, k = 1.
Numerical: 10,000 curves, β uniform on (0, 2), (λ, Σ, K) four decades, T10 method with limits_pow brackets:
exactly 1 turning point (a maximum) in every curve, and the identity in 2 evaluated at that point is positive.
**Pass:** all symbolic items and 0 numerical failures.

### A5 — Conj. 3.10 (Hill, every real n > 1). Seed 13005.
Route: t = Π/Π0, T = t^n, G = cT/(1 + T), ε = n/(1 + T). From Lemma 3.7,
N(1 + T)³ ≡ c T P_n(T) − 2nΣΠ0 t(1 + T)², P_n(T) = −(λ + c)T² + (n − 1)(c + 2λ)T + (2n − 1)λ.
So sign N = sign(cφ_n(t)/(2n) − ΣΠ0), φ_n(t) = t^{n−1}P_n(t^n)/(1 + t^n)².
Symbolic checks:
1. The N(1 + T)³ identity (with ε = n(1 − G/c)); n = 2 gives Stage 3's P_4 and the factor 4 = 2n.
2. dφ_n/dT has the sign of R(T) = aP(1 + T) + T(1 + T)P′ − 2TP, a = (n − 1)/n (identity).
3. Coefficients of R: a p0 (> 0), a(p0 + p1) + p1 − 2p0, (a − 1)p1 + (a + 2)p2 (< 0 for n > 1: a − 1 = −1/n,
   p1 = (n − 1)(c + 2λ) > 0, p2 = −(λ + c) < 0, a + 2 > 0), a p2 (< 0). Descartes: exactly one sign change, so exactly
   one positive root T*; φ_n increases then decreases, φ_n(0⁺) = 0, φ_n → −∞.
4. Near t = 0, N < 0 (c(2n − 1)λ t^n ≪ 2nΣΠ0 t for n > 1): first turning point is a minimum.
5. n = 2: R(t²) ∝ −(t⁴ + 6t² − 3)((λ + c)t² + λ) (Stage 3's factorization recovered).
Consequences: 0 turning points, or a minimum then a maximum; single pair-birth value
Π0^pair(n) = c φ_n(t*)/(2nΣ). Numerical: (i) regression of Π0^pair(n) (λ = c = 1, Σ = 0.01) against Task 10's
table, n = 1.5, 2, 3, 4, 8: 30.2430947474, 31.4750497595, 37.8200022316, 44.1796834278, 62.7113145769, to 1e-9
relative; (ii) 5,000 random sets with n log-uniform on [1.01, 10] and Π0 log-uniform on [0.5, 2]·Π0^pair (so both
sides of the onset are sampled): T10-method turning points equal the prediction (0 if Π0 > Π0^pair, (min, max)
otherwise) in every set. **Pass:** all symbolic items, regression and 0 mismatches.

### A6 — Conj. 2.11 (sampled relays D1–D3, at most two turning points, every metric). Seed 13006.
Attempt per (family, metric) with the explicit fixed-gain P⁺ and Lemma 2.1. No route is known; the expected outcome is
unresolved. Partial results to report: endpoint asymptotics (proved in Task 12), single excess component (Props.
2.2–2.4). Numerical evidence: Task 12's census (6,000 sets × 3 metrics) and the Part C class audit (its D-family rows
record turning-point histograms on 1,000 new sets each). **Outcome:** proved for a (family, metric) only by a complete
symbolic argument; disproved if any curve with ≥ 3 turning points is found and confirmed at 60 digits.

### A7 — Num. 3.5 (strict gap P < V along matched-zero-frequency τ). Seed 13007.
Route: (i) MMSE uniqueness: if a relay with gain G attained P its error would be orthogonal to every past
observation. (ii) For the relay (a = λ + G), the lagged covariance c(u) = E[x(t) y(t − u)], u ≥ 0, satisfies
c(u) = e^{−au}c(0) − (G/(2Πτ))(e^{−u/τ} − e^{−au})/(a − 1/τ) (a ≠ 1/τ), and −(G/(2Πτ)) u e^{−au} + e^{−au}c(0)
(a = 1/τ). For G > 0 the e^{−u/τ} (resp. u e^{−au}) term is nonzero, so c ≢ 0; for G = 0, c(u) = F e^{−λu} ≢ 0.
(iii) G → ∞: σ² → Var η = 1/(2Πτ), and the estimator ŝ = y has E[(s − y)y] = −Var η ≠ 0, so P < 1/(2Πτ).
(iv) σ²(G, τ) is continuous on [0, ∞] (compactified), so V = min > P.
Symbolic checks: the c(u) formula from the stationary covariance of (s, η, x) (Lyapunov equation) and the
integral; the G → ∞ limit; the coefficient of e^{−u/τ}. Numerical: 10,000 sets (λ, Σ, Π, τ), 60 digits:
V − P > 0 with V from all positive real roots of the analytic stationarity polynomial of σ²(G, τ) in G
(`mp.polyroots`) and the G → ∞ limit. **Pass:** all symbolic items and 0 failures.

### A8 — Conj. 4.11 (non-linear causal garblings add nothing for additive stationary Gaussian noise). Seed none.
(1) Literature check first (web, if available): Blackwell comparison of Gaussian / linear normal experiments
(Hansen & Torgersen 1974 and later), comparison of experiments for Gaussian processes. Queries recorded.
(2) Proof route: if θ1 ⪯_c θ2 by any (non-linear) causal garbling, then for every square-integrable target Z
measurable w.r.t. s, MSE(Z | Y1(≤ t)) ≥ MSE(Z | Y2(≤ t)) (proof of Thm 4.2 with Z in place of s(t)). By stationarity
and Lévy's upward theorem (fixed-lag limit), the same holds for the two-sided σ-fields. For linear Z = ∫g(u)s(u)du
(g smooth, compact support) the Gaussian two-sided MMSE is ∫|ĝ|² S_sS_η/(S_s + S_η) dω/2π, so
h = S_sS_1/(S_s + S_1) − S_sS_2/(S_s + S_2) ≥ 0 a.e. (|ĝ|² concentrates at any frequency); x ↦ S_s x/(S_s + x) is
strictly increasing where S_s > 0, so S_1 ≥ S_2 a.e., i.e. linear causal garbling (Prop. 4.4(1)).
Symbolic check: d/dx [S x/(S + x)] = S²/(S + x)² > 0. **Outcome:** proved iff the written proof is complete and the
independent referee (Part C4) raises no unresolved valid objection to it; otherwise unresolved with the partial result.

### A-reg — regression of every verified Theorem/Proposition (Tasks 8–12)
One combined script runs the five symbolic scripts (`t8_symbolic.py`, `t9/t9_symbolic.py`, `t10/t10_symbolic.py`,
`t11/t11_symbolic.py`, `t12/t12_symbolic.py`) and the documented fallback routes for the three items that needed them
(Task 10: the two √(square) items via `t10_symbolic_diag.py`; Task 12: the D2 O(1/Δt) coefficient via the series route
of `t12_symbolic_diag.py`). **Pass:** 100% of items reduce to 0 (or are manifestly signed) by the fixed route or the
documented fallback; every item is counted once.

---

## Part B — consolidated document (not a pass/fail check)
`Stages_0_4_Consolidated.md` per the Task 13 prompt: one global numbering sequence (Theorem 1, Lemma 2, …), a change log
mapping every old number to its new number, every correction from Tasks 8–12 applied and logged, exactly one Section 12
label per result (header kind = label), each label citing the verifying task(s). Results with two labels in the stage
documents ("Proposition + Counterexample", "Numerical result + Conjecture") are split into two numbered results.
Mathematical content changes only where Part A or a recorded correction requires it.

---

## Part C — consistency audit (scripted)

### C1 — numbers
Scope: every decimal literal (regex `\d+\.\d+`, and `a\times10^{b}` forms) in Sections 1–11 of the consolidated
document (the verification appendix and change log are records, not claims, and are excluded). A registry
(`t13/numbers_registry.py`) maps each literal (string + anchor phrase) to a formula evaluated at ≥ 50 digits.
**Pass:** every literal in scope is matched by exactly one registry entry and every entry's computed value matches the
literal to its stated precision (half a unit in the last stated digit; "≈" literals: 1% relative). Unmatched literals
and mismatches are failures.

### C2 — classes (one row of the synthesis matrix at a time)
Per row: 1,000 random parameter sets (seed 13100 + row index), 100 tolerances per set: 50 log-uniform on
[½·min, 2·max] of the finite positive critical tolerances, 50 near-critical (10 exactly a critical tolerance, 40
within ±1e-6 relative of one; critical value chosen uniformly). Curves with no finite positive critical value
(monotone 0 → ∞) get 100 values of the curve at log-uniform sweep points over 40 decades (Task 12 rule).
Route (i) in mp (dps 50 turning points); route (ii) in float64 where a float curve exists (else mp), with every
flagged case (disagreement or out-of-set) re-run in mp at dps 60.
**Pass per row:** 0 persisting classes outside the row's stated set, 0 persisting route disagreements, and every
class in the stated set observed at least once. An unobserved stated class is a document error unless it is reachable
only on a measure-zero set of parameters, justified in the diagnosis.

Rows, stated sets, sampled parameters, limits and brackets (derivations: the cited pre-registrations, plus the new
rows derived here). Brackets are log10 of the sweep variable; "shift" is the T-family shift (−log10 λ for τ, Δt).

| # | Row | Stated classes | Limits L₋ → L₊ (approach rate) | Bracket |
|---|---|---|---|---|
| 1 | Π, optimal σ*² | lower ray, Empty | F (dev O(Π)) → 0 (~√(2Σ/Π)) | ±80 |
| 2 | Π, Bayesian | All, lower ray, window, Empty | F (O(Π)) → H = Σ/(λ+c) (O(1/Π)) | ±80 |
| 3 | Π, misspecified Kalman | lower ray, window, Empty | F (O(Π)) → 0 (~Π^{−1/2}) | ±80 |
| 4 | Π, capped | All, lower ray, window, Empty | F (exact on linear branch near 0; O(Π)) → Σ/(λ+c) (O(1/Π)) | ±80 |
| 5 | Π, precision-blind | All, lower ray | ∞ (~1/Π) → Σ/(λ+G0) (O(1/Π)) | ±80 |
| 6 | Π, Hill n = 2 | All, lower ray, (1,0,1), window, Empty | F (O(Π²)) → Σ/(λ+c) (O(Π^{−2})) | ±80 |
| 7 | Π, Hill n > 1 (n log-uniform [1.01, 10]) | All, lower ray, (1,0,1), window, Empty | F (O(Π^n)) → Σ/(λ+c) (O(Π^{−n})) | ±80 |
| 8 | Π, two-stage Bayesian (T10 draw) | All, lower ray, window, (1,0,1), (0,0,2), Empty | F → Σ/(λ+c₁+c₂) (O(Π), O(1/Π)) | ±80 |
| 9 | Π, two-stage Hill (T10 draw) | All, lower ray, (1,0,1), (1,0,2), window, (0,0,2), Empty | F (O(Π²)) → Σ/(λ+c₁+c₂) (O(Π^{−2})) | ±80 |
| 10 | Π0, Bayesian | All, two rays, lower ray, upper ray, Empty | V_c (O(Π0)) → F (O(1/Π0)) | ±80 |
| 11 | c, Bayesian | All, two rays, upper ray | F (O(c)) → ∞ (~c) | ±80 |
| 12 | Π0, monotone gain at fixed Π (c·tanh(Π/Π0), c(1−e^{−Π/Π0}), cΠ²/(Π²+Π0²), one per set at random) | All, two rays, lower ray, upper ray, Empty | V_c (exp. or O(Π0²)) → F (O(1/Π0) or O(Π0^{−2})) | ±80 |
| 13 | τ (zero-freq. power), relay | All, lower ray, Empty | V_w (O(τ)) → H_G (O(1/τ)) | ±80, shift |
| 14 | τ (zero-freq. power), optimal | lower ray, Empty | σ*² (O(τ)) → 0 (~1/τ) | ±80, shift |
| 15 | τ (matched variance), relay | All, upper ray, Empty | H_G (O(τ)) → top (O(1/τ)) | ±80, shift |
| 16 | τ (matched variance), optimal | window, Empty | 0 (~√τ) → 0 (~τ^{−1/2}) | ±80, shift |
| 17 | τ, power family β ≤ 0 (900 β uniform on [−2, 0), 100 at β = 0) | lower ray, Empty | β < 0: F (~τ^{|β|}) → 0; β = 0: σ*²(1/K) → 0 | β < 0: lower max(80, 50/|β|); upper max(80, 100/(2−β)) |
| 18 | τ, power family 0 < β < 2 | window, Empty | 0 → 0 (~τ^{β/2}, τ^{(β−2)/2}) | max(80, 100/β), max(80, 100/(2−β)) |
| 19 | τ, power family β ≥ 2 (900 β uniform on (2, 4], 100 at β = 2) | upper ray, Empty | 0 → β = 2: σ*²(λ²/K); β > 2: F (~τ^{2−β}) | lower max(80, 100/β); upper β > 2: max(80, 50/(β − 2)); β = 2: 80 |
| 20 | delay d = θe^{−θ}, optimal | All, window, Empty | σ*² (O(θ)) → σ*² (O(θe^{−θ})) | ±80 |
| 21–23 | Δt (M-P), optimal post / prior / avg | lower ray, Empty / All, upper ray, Empty / All, upper ray, Empty | Task 12 `dt_limits` | ∓80 − log10 λ |
| 24–26 | Δt, D1 post / prior / avg | Empty, lower ray, window / All, Empty, lower ray, upper ray, two rays, (0,1,1) / same as prior | Task 12 | Task 12 |
| 27–29 | Δt, D2 post / prior / avg | All, Empty, lower ray, upper ray, two rays, window, (1,0,1) / All, Empty, lower ray, upper ray, two rays / same as prior | Task 12 | Task 12 |
| 30–32 | Δt, D3 post / prior / avg | Empty, lower ray, window / All, Empty, lower ray, upper ray, two rays, (0,1,1) / All, Empty, lower ray, upper ray, two rays | Task 12 | Task 12 |
| 33–34 | Δt (M-I), optimal (a) / (b) | All, upper ray, Empty | σ*² → F (Task 12) | Task 12 |
| 35–36 | Σ, Σ-independent gain, abs / rel | All, upper ray / All, lower ray | Task 12 `sig_limits` | ∓80 |
| 37–38 | Σ, Σ-tracking ρ, abs / rel | upper ray / lower ray, window, Empty | Task 12 | ∓80 |
| 39–40 | Σ, Σ-tracking λ′, abs / rel | upper ray / lower ray, window, Empty | Task 12 | ∓80 |
| 41–42 | Σ, optimal, abs / rel | upper ray / lower ray, Empty | Task 12 | ∓80 |

Derivations for the new rows. Row 1: σ*² = 2Σ/(λ + √(λ² + 2ΣΠ)) = F(1 − ΣΠ/(2λ²) + O(Π²)) at 0, and ~√(2Σ/Π) at ∞;
at 1e∓80 the deviation is ≤ 1e-74 relative (parameters within 1e±2, so ΣΠ/λ² ≤ 1e6) and the zero limit is reached
(≤ 2e-38 ≤ 1e-30). Rows 2–9: σ² − F ~ G(λG/(2Π) − Σ)/(λ(λ+G)) with G = O(Π) (O(Π^n) for Hill) near 0; near ∞ the
gains converge to G∞ at rate 1/Π (Bayesian, capped beyond the kink, blind) or Π^{−n} (Hill), and σ² − H = O(1/Π);
misspecified: G ~ √(2Σ′Π), σ² ~ (Σ + Σ′)/G → 0 like Π^{−1/2}, ≤ 1e-36 at Π = 1e80. Rows 10–12: G → c (Π0 → 0) at
rate O(Π0) (Bayesian), exponentially (tanh, exponential) or O(Π0²) (Hill-form), and G → 0 at O(1/Π0) or O(Π0^{−2})
(Π0 → ∞); σ² is smooth in G, so deviations are ≤ 1e-72 at the brackets. Row 11: σ² ~ cK/(2Π) → ∞ linearly. Rows
13–16: Tasks 9–10 (deviation O(τ) or O(1/τ); optimal ~1/τ; matched variance P ≤ √(C/A) ~ √τ and τ^{−1/2}).
Rows 17–19: Task 11 `limits_pow` with the diagnosed correction (Task 11 diagnosis: β = 2 limit σ*²(λ²/K); β > 2
bracket max(80, 50/(β − 2)) because P − F ~ τ^{2−β}; by the duality Prop. 4.6b the β < 0 lower end mirrors it,
bracket max(80, 50/|β|)). Row 20: Task 11 (P(d) − σ*² = (F − σ*²)(1 − e^{−2λd}), d ~ θ at 0 and θe^{−θ} at ∞).
Rows 21–42: PREREG_t12 (limits and brackets derived there; Δt brackets ∓80 − log10 λ; Σ brackets ∓80), with the
tolerance rule for monotone 0 → ∞ curves stated above.

Parameter draws: λ, Σ, Π, Π0, c, G, G0, K, ρ, λ′ log-uniform on [1e-2, 1e2]; Task 12's c ∈ [2e-4, 2) for D2; two-stage
draws as Task 10 (c₁, c₂, Π01 four decades, Π02 = Π01·10^{U(1,6)}); misspecified Kalman (λ′, Σ′) four decades; capped
(g, c) four decades. Turning-point histograms are recorded for every row (they serve A6 for rows 24–32).

### C3 — references and labels
**Pass (0 errors):** (a) every reference of the form "Theorem/Proposition/Lemma/Corollary/Numerical result/
Conjecture/Counterexample/Definition N" (and the abbreviations Thm, Prop., Cor., Num., Conj., Def.) in the
consolidated document resolves to a result defined in it with that number and that kind; (b) every defined result
appears exactly once in the verification appendix with the same kind; (c) no result header carries two kinds and no
label line contradicts its header; (d) every section reference "Section N" resolves.

### C4 — independent referee
A separate agent that has not seen the derivation history receives only `Stages_0_4_Consolidated.md` and reports
(a) proof steps it cannot follow or believes wrong, (b) claims stronger than their proofs, (c) missing equality
cases. Its report is recorded verbatim; each point is classified valid (fixed, logged) or invalid (explained).
Not pass/fail; the number of valid points is reported.

---

## Part D — full reproducibility
`classification/reproduce_all.sh` runs, in a clean checkout (`git worktree` of the Task 13 code commit in a scratch
directory), Task 8 (`run_all.sh`), Task 9 (`t9/run_t9.sh`), Task 10 (`t10/run_t10.sh`), Task 11 (`t11/run_t11.sh`),
Task 12 (`t12/run_t12.sh`) and Task 13 (`t13/run_t13.sh`), in that order, with the seeds in the code, and writes
`manifest.json` (commit hashes, package versions, per-task runtimes, SHA-256 of every output file). It may be invoked
for a subset of tasks; the run is done as one invocation for Tasks 8–12 (started first) and one for Task 13, both from
the same worktree, and the two manifests are merged. A comparison script (`t13/compare_repro.py`) then checks:
**Pass:** for each of `REPORT.md` and `RESULTS_t9`…`RESULTS_t12`, after masking runtimes, timing totals, commit
hashes, dates and the code-commit argument, (i) every verdict cell (PASS/FAIL/record/DONE) is identical, and (ii) every
other number is identical or, if not, agrees to relative 1e-6 (floating-point tolerance; MC and seeds are fixed).
Every mismatch is listed and diagnosed. The total runtime is recorded; the reviewer estimate for 4 CPUs is the
measured wall time scaled by (CPUs used here)/4.

---

## Parts E and F (not pass/fail)
Figures `figs_paper2/` (10 figures, colourblind-safe palette, PNG + PDF, one caption file each, all from the
consolidated formulas) and `Roadmap_v3.md` with the novelty check (queries, sources, relevance; targeted, not
exhaustive), as specified in the prompt.

## Report
`t13/RESULTS_t13.md` from `t13/make_results_t13.py`: one row per check (verdict, counts, worst errors, runtime,
hashes); Part A outcome table; the referee report with dispositions; reproducibility results; plain statements
(did any Stage 0–4 result change; any class outside the stated sets; what remains open).
