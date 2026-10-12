# Failure-Set Topology in Stationary Linear Filters

Thesis draft v0.1 · John Holder · Oct 11, 2026 · @John Holder

**Status.** Chapters 1–7 drafted. Results are numbered by chapter: Theorem 3.2 is the second numbered result of chapter 3. Appendix A lists every result with its permanent repository key and its verification. References are cited as bracketed numbers \[n\], assigned in order of first citation and listed in Appendix C. Figures are cited as Figure B.n and collected in Appendix B; the images themselves carry no numbers. Remaining chapters are outlined with the results they will contain.

## 1. Introduction

A filter that must keep its error within a fixed specification can fail on a set of operating conditions with a definite shape: a threshold, a bounded window, two rays, or a mixture. This thesis classifies those shapes for scalar stationary linear filters, sweep by sweep, and shows which of them an optimal filter can never produce.

### 1.1 The question

A filter is usually judged at one operating point: how large is its error, and how far is it from the optimum? A specification asks something different. It fixes a tolerance R² and asks for which operating conditions the actual error variance σ² exceeds it. As a condition θ varies (observation precision, noise correlation time, sampling interval, process noise, or a design parameter), the answer is a set,

```latex
\mathcal F(R^2) = \{\theta : \sigma^2(\theta) > R^2\}
```

and its shape matters in practice. A threshold means "fails below some precision". A window means "fails only at intermediate precision, though both worse and better observations are acceptable". This thesis asks:

> Under what conditions does the failure set of a stationary linear filter change shape as an environment or design parameter varies, and which shapes are impossible for an optimal filter?

### 1.2 Starting point: a bounded failure window

This research began with a single relay: a constant-gain filter for an Ornstein–Uhlenbeck state whose gain follows the one-step Bayesian weight cΠ/(Π + Π₀) instead of the steady-state Kalman–Bucy gain \[1\]; this weight is a precision-weighting rule \[2, 3\]. That starting study, verified by Tasks 1–7 (Appendix D), produced three findings that set up the thesis:

- **The excess identity.** The relay is worse than no filtering exactly when its gain exceeds 2FΠ, where F is the uncorrected variance (Corollary 3.3). The optimal gain never exceeds FΠ (Proposition 3.5).
- **The window theorem.** For gains with natural limits, some tolerance fails on a bounded set of precisions away from zero iff sup G/Π > 2F (Theorem 3.4). For the Bayesian-weight gain this is κ > 2, where κ = c/(FΠ₀) (Proposition 5.8). In the worked example, at κ = 100 and R² = 0.05, the relay fails exactly for Π ∈ (1/9, 4).
- **The optimal filter never windows** along precision, because its error decreases strictly (Theorem 3.4).

That study answered the question for one gain family along one sweep. This thesis answers it for every sweep in the scalar model, for every natural gain family considered, and for the optimal filter.

### 1.3 The object of study

The failure set is an open subset of an interval, so it is a union of disjoint open intervals. Its **class** records three things: whether it contains a ray at the lower end (ℓ), a ray at the upper end (u), and how many components k it has away from both ends (C5). The named classes are Empty, All, lower ray, upper ray, two rays, window, multi-window and mixed (a ray plus window components).

Two kinds of sweep are studied:

- **Environment sweeps** change the observations or the signal: precision Π, correlation time τ, sampling interval Δt, process noise Σ. The optimal filter changes along them.
- **Design sweeps** change the filter only: prior precision Π₀, coupling c. They classify miscalibration.

A classification is **complete** when the class is determined at every parameter value and every tolerance, equality cases included, and every class claimed impossible has a proof.

### 1.4 Approach: two pillars and a bridge

The thesis rests on two organising results joined by one theorem.

- **The bridge: the critical-value signature (Theorem 2.2).** For any piecewise-monotone variance curve, the class at every tolerance is fixed by a finite list: the endpoint limits, the values at turning points, and two approach directions. Classifying a model reduces to computing that signature (chapter 2).
- **Pillar 1: the normal form (Theorem 3.2).** For the white-noise relay, every stationary variance is one surface evaluated along a path: σ²/F = 𝒱(ν, q), with ν = 2FΠ/λ and q = G/(FΠ). The floor crossing is the line q = 2, the optimal filter is the lower envelope, and each sweep or gain family is a path (chapter 3).
- **Pillar 2: causal information ordering (Theorem 7.2).** If one observation process can be manufactured from another as it arrives, plus independent noise, the optimal filtering error is monotone between them. Along such a sweep the optimal filter cannot window (chapter 7).

The resulting picture: a variance curve determines its signature, which determines the class; a gain family restricts which signatures are reachable; optimality and information ordering restrict them further.

### 1.5 Main results

**Every gain fails at tight tolerances.** For any continuous gain schedule and any R² < F, the failure set contains all precisions below π\_R = 2λ(F − R²)/R⁴ (Cor. 5.2). So a window class needs a tolerance at least as loose as the uncorrected error, for every gain, with no regularity assumptions.

**Along precision, the model forbids only one thing.** A variance curve is reachable by some continuous gain iff it never dips below the optimal variance (Theorem 5.1). Every class is then available to some gain, except that below the floor every failure set contains a lower ray (Corollaries 5.2–5.3), and smooth gains with the natural limits of Theorem 3.4 can have any number of window components (Corollary 5.4). The restrictions come from the gain family:

- natural single-stage gains have at most one window component (Propositions 5.8–5.11);
- the sigmoidal Hill gain, with zero initial slope, produces the mixed class lower ray plus window (Theorem 5.12, Proposition 5.13), and a mixed class of this kind needs G/Π to be non-monotone (Proposition 5.14);
- sums of two natural stages produce multi-window classes (Numerical result 5.15).

**Each sweep has its own repertoire.**

| Sweep | Relay classes (natural gains) | Optimal-filter classes | Labels |
| --- | --- | --- | --- |
| Precision Π | All, lower ray, window, Empty; mixed (1, 0, 1) for Hill | lower ray, Empty | 3.4, 5.8–5.14 |
| Prior Π₀, coupling c | All, lower ray, upper ray, two rays, Empty; never a window | — (design sweeps) | 4.1–4.5 |
| Correlation time τ, matched power | All, lower ray, Empty | lower ray, Empty | 6.3, 6.6–6.7 |
| Correlation time τ, matched variance | All, upper ray, Empty | window, Empty | 6.10–6.12 |
| Sampling interval Δt | adds two rays, (0, 1, 1) and (1, 0, 1) | post-update: lower ray, Empty; prior and time-averaged: All, upper ray, Empty | 6.13–6.21 |
| Process noise Σ | absolute tolerance: All, upper ray; relative tolerance: windows iff over-trust ρ > 2 | absolute: upper ray; relative: lower ray, Empty | 6.23–6.28 |

**Where the optimal filter can and cannot window.** Along any causally ordered sweep, the optimal filter's failure set is Empty, All or a single ray at the less informative end (Cor. 7.3). The condition is exactly sharp in a natural family of coloured noises, S(ω) = Kτ^β/(1 + τ²ω²): the sweep is ordered, the optimal error monotone, and optimal windows absent, all exactly when β ≤ 0 or β ≥ 2 (Theorem 7.8). Correlation time at matched variance is β = 1, and there the optimal filter does window (Prop. 6.10, Counterexample 6.11). Ordering must be causal: sensor delay gives experiments that are equivalent as whole paths, yet the optimal filter windows (Prop. 7.11). For additive stationary Gaussian noise the test is exact: causal ordering, pathwise ordering and pointwise dominance of noise spectra coincide (Theorem 7.6).

**A diagnostic.** Along a causally ordered sweep, any window, two rays or mixed class certifies that the filter is not optimal (Corollary 7.4). The bounded window of §1.2 is therefore a signature of miscalibration, not of the environment.

### 1.6 Contributions and relation to prior work

The novelty claims rest on targeted literature and patent searches made on 11 October 2026, not on an exhaustive review.

1. **The classification of failure-set topology** for stationary linear filters, including the forced lower ray and each sweep's complete class table. No prior work was found that treats the tolerance-exceedance set itself as the object of study. The neighbouring literature computes actual error under mismatch at given operating points \[4–9\] or designs filters to meet a specification. Related work studies filtering under misspecified models \[10, 11\] and when feedback helps at all \[12, 13\].
2. **Expressivity of gain families.** Realizability is the scalar filtering analogue of covariance assignment \[14, 15\], which treats state covariance under feedback in multivariable control. The Hill mixed class appears to be new; the gain form itself comes from divisive normalisation \[16, 17\].
3. **Optimality.** The power-family threshold (Theorem 7.8), the matched-variance optimal window (Counterexample 6.11) and the delay counterexample (Counterexample 7.12) appear to be new. Theorem 7.2 is presented as a filtering instance of known results: monotonicity of optimal performance under garbling orders goes back to Blackwell \[18, 19\] and extends to sequential experiments \[20\] and stochastic control and teams \[21–23\]. What is specific here is the causal garbling of observation processes and its conclusion for filtering error. Theorem 7.6 extends the static characterisation for linear normal experiments \[24\] to stationary Gaussian processes ordered by their spectra; no process version was found.
4. **Smaller contributions.** The normal form (dimensionless indices are precedented by Kalata's tracking index \[25\]); the excess threshold G = 2FΠ as an explicit statement; and the observation that, under matched-precision sampling, the post-update error falls with Δt while the prior and time-averaged errors rise.

The constant-gain variance, the Kalman–Bucy steady state \[1\], the discrete variance factor α/(2 − α) \[26\], the coloured-noise methods \[27, 28\] and the delay prediction covariance \[29\] are background. The framework of chapter 2 is the fixed-level reading of zero-dimensional persistence \[30, 31\].

### 1.7 Scope and conventions

- **Model.** Scalar, linear, stationary, Gaussian. The gain is constant in time at each parameter value but may vary across values.
- **Error.** Always the actual stationary error variance, never the variance a filter reports from its own model.
- **Noise convention.** Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, so the floor is F = Σ/λ.
- **Sampling.** Each sample has noise variance 1/(ΠΔt). The time-averaged error is the primary metric; post-update and prior errors are reported alongside, because they move in opposite directions.
- **Moving floor.** For the Σ sweep, both absolute (R² fixed) and relative (R²/F fixed) tolerances are reported, because they give opposite rays.
- **Excluded.** Multivariate states, nonlinear dynamics, time-varying gains, and applied relevance studies, which chapter 9 lists as future work.

### 1.8 How results were established

Every result has one type (Definition, Theorem, Proposition, Lemma, Corollary, Numerical result, Conjecture or Counterexample) and one number by chapter, so Theorem 5.12 is the twelfth numbered result of chapter 5. Each also has a permanent key in the project repository; Appendix A lists both, with the verification of each result. Analytic results were checked symbolically and numerically under pre-registered criteria committed before each run, from the starting study (Tasks 1–7) to the consolidation, renumbering and repository sync (Tasks 13–15). Failed checks stay recorded as failures, with their diagnosis (chapter 8). Blind searches of 10⁶ and 4.4 × 10⁶ classifications found no class outside the predicted sets (Numerical result 8.1).

### 1.9 Outline

- **Chapter 2** sets out the framework: conventions, the critical-tolerance theorem, the signature, the events at which classes change, reparameterisation and stability.
- **Chapter 3** derives the normal form of the white-noise relay.
- **Chapter 4** treats the design sweeps as horizontal paths on that surface.
- **Chapter 5** studies the precision sweep and the expressivity of gain families.
- **Chapter 6** leaves white noise: correlation time, sampling interval and process noise.
- **Chapter 7** proves the optimality results and their limits.
- **Chapter 8** reports verification, including every recorded failure.
- **Chapter 9** discusses relevance, open conjectures and future work.

## 2. Framework: The Critical-Value Signature

The topology of a failure set is fixed by a finite list of numbers: the endpoint limits and turning-point values of the variance curve, together with two approach directions (Theorem 2.2). This chapter states that theorem and organises its consequences for the rest of the thesis. Only Corollary 2.8 and Proposition 2.9 are new statements; everything else rearranges Theorem 2.2.

### 2.1 Setting and conventions

A sweep varies one parameter θ over an open interval and records the actual stationary error variance σ²(θ) of a filter. Variances are always actual, never the variance a filter reports from its own model.

- **C1 (domain).** θ ranges over D = (θ₋, θ₊), with −∞ ≤ θ₋ < θ₊ ≤ ∞. Endpoints never belong to D; behaviour there enters only through limits.
- **C2 (regularity).** σ² is continuous on D, with finitely many turning points t₁ < … < tₙ and strictly monotone pieces between them. The endpoint limits L± = lim σ² as θ → θ± exist in \[0, ∞\].
- **C2′ (plateaus).** As C2, but finitely many pieces may be constant. Used only in §2.5.
- **C3 (failure set).** For a tolerance R² > 0, the failure set is open:

```latex
\mathcal F(R^2) = \{\theta \in D : \sigma^2(\theta) > R^2\}
```

- **C4 (approach direction).** σ² approaches a finite L₋ from above if σ² > L₋ on the first piece (the first piece increases away from it), and from below otherwise. At θ₊ it approaches from above if the last piece decreases towards L₊.
- **C5 (class).** 𝓕(R²) is a disjoint union of open intervals. Its class is (ℓ, u, k): ℓ = 1 if a component contains a neighbourhood of θ₋ (a lower ray), u = 1 likewise at θ₊ (an upper ray), and k counts the components bounded away from both ends (window components).
- **C6 (critical tolerances).** 𝒞 is the set of finite values among L₋, σ²(t₁), …, σ²(tₙ), L₊.

| Named class | (ℓ, u, k) |
| --- | --- |
| Empty | (0, 0, 0) |
| All | 𝓕 = D |
| Lower ray | (1, 0, 0) |
| Upper ray | (0, 1, 0) |
| Two rays | (1, 1, 0), 𝓕 ≠ D |
| Window | (0, 0, 1) |
| Multi-window | (0, 0, k), k ≥ 2 |
| Mixed | k ≥ 1 and ℓ + u ≥ 1 |

A whole failure set bounded away from both ends is often called a window. This thesis keeps that meaning for the **window class** (0, 0, k) and calls each bounded component a **window component**. The distinction matters: a mixed class contains window components but is not a window.

### 2.2 Topology alone excludes nothing

**Proposition 2.1 (realizability).** For every ℓ, u ∈ {0, 1} and every finite k ≥ 0 there is a continuous, piecewise strictly monotone function on (0, ∞) and a tolerance whose failure set has class (ℓ, u, k); All is realised too. Classes with k = ∞ need infinitely many turning points and are excluded by C2.

*Proof.* Take a piecewise-linear zigzag with k interior peaks of height 2 separated by troughs of height 0, starting at height 2 if ℓ = 1 and 0 otherwise, and ending likewise for u; set R² = 1. For All, take any function bounded below by 2. ∎

Every restriction in this thesis therefore comes from the filtering model, never from topology.

### 2.3 The critical-tolerance theorem

**Theorem 2.2.** Assume C1–C6.

1. **Local constancy.** The class of 𝓕(R²) is constant on each connected component of (0, ∞) \\ 𝒞. It can change only when R² crosses or equals a critical tolerance.
2. **Rays.** ℓ = 1 if R² < L₋ and ℓ = 0 if R² > L₋. If R² = L₋, then ℓ = 1 iff σ² approaches L₋ from above. The same holds for u with L₊.
3. **Window components.** Each window component contains an interior local maximum tⱼ with σ²(tⱼ) > R², and distinct components contain distinct maxima. Hence k is at most the number of interior maxima above R², with equality iff each such maximum lies in its own component touching neither end.
4. **Determining data.** The class of 𝓕(R²), for every R², is determined by the ordered sequence (L₋, σ²(t₁), …, σ²(tₙ), L₊) and the two approach directions. The positions tⱼ are needed only to locate the components.

*Proof.* (1) On each piece, σ² is a strictly monotone bijection onto the open interval between its end values, all of which lie in 𝒞 or are infinite. For R² ∉ 𝒞, the piece's contribution to 𝓕 is empty, the whole piece, or a one-sided subinterval at its larger end, decided by where R² sits relative to the end values. Adjacent contributions join exactly when the shared turning-point value exceeds R². All of this is constant between critical tolerances. (2) Near θ₋, σ² is close to L₋; at equality the first piece is strictly monotone, so it lies entirely above or entirely below L₋. (3) A window component (a, b) has a, b ∈ D with σ²(a) = σ²(b) = R² and σ² > R² between, so σ² attains an interior maximum there, which is a turning point. Disjoint components contain distinct maxima. (4) The construction in (1) uses only the end values of each piece, and (2) adds the approach directions. ∎

Applied to the Bayesian-weight gain with κ > 2 (Proposition 5.8), the sequence (F, M, H) with both ends approached from above returns its four regimes, equality cases included.

Theorem 2.2 is the one-dimensional case of a known picture: the superlevel sets of a function on an interval, followed as the threshold moves, form a zero-dimensional persistence module (equivalently a merge tree), whose changes occur only at endpoint values and critical values. See \[32\] for join trees of superlevel sets, \[33\] for the Morse-theoretic backbone, and \[30, 34, 35\] for persistence and merge trees. What this thesis adds is the reading at a *fixed* tolerance, with equality cases and approach directions, which is the reading a specification needs.

### 2.4 The critical-value signature

**Definition 2.3.** The *critical-value signature* of a curve satisfying C2 is

```latex
S(\sigma^2) = \big(L_-,\ \sigma^2(t_1),\ \dots,\ \sigma^2(t_n),\ L_+;\ d_-,\ d_+\big)
```

where d± ∈ {above, below} are the approach directions. Its **critical-tolerance diagram** is the (θ, R²) half-plane cut by horizontal lines at the values in 𝒞: each band between consecutive lines carries one class, and each line carries its own equality class.

By Theorem 2.2(4) the class is a function of S and R² alone, so classifying a model means computing its signature. The precision sweep of the Bayesian-weight relay (Proposition 5.8) shows the reading:

| Band of R² | Class (κ > 2) |
| --- | --- |
| R² ≤ H | All |
| H < R² ≤ F | Lower ray |
| F < R² < M | Window |
| R² ≥ M | Empty |

*Figure B.1 (Appendix B): a schematic curve (not a filter's variance) with its critical tolerances, and the class in each band between them.*

A second level sits above the diagram. A family parameter (κ, Π₀, ρ, β) changes the signature itself: it can add or remove turning points or reorder their values. The values of that parameter where the signature changes length are the **onset conditions** of later chapters, such as κ = 2 (Prop. 5.8) and the Hill pair birth (Theorem 5.12).

### 2.5 Where the class changes

For a fixed curve the class changes only at the events below; a sixth kind of point changes nothing. Each row is a consequence of Theorem 2.2 or its plateau extension.

| Event | Occurs when | Effect on the class | Label |
| --- | --- | --- | --- |
| Boundary | R² = L₋ or L₊ | a ray appears or disappears; at equality the approach direction decides | Thm 2.2(2) |
| Extremum | R² = σ²(tⱼ) | a component is born or dies (maximum), or two components merge or split (minimum) | Thm 2.2(3) |
| Equal height | two maxima separated by a lower minimum share a value M₂, each in a window just below it | k drops by 2 at the single tolerance M₂ | Cor. 2.5 |
| Plateau | R² equals a plateau value (C2′) | the plateau leaves the failure set and can split a component | Thm 2.4 |
| Pair birth | a family parameter creates a minimum–maximum pair through a nondegenerate fold | a new band of tolerances opens from zero width; values separate like δ^(3/2), positions like δ^(1/2) | Prop. 2.7 |
| Non-event | a stationary point that is not a turning point | none | Cor. 2.6 |

The first four are events in R² for one curve. Pair birth is an event in the family parameter: it changes the signature, and so the diagram itself.

The four results behind the table rows are these.

**Theorem 2.4 (plateaus).** Under C2′ instead of C2, Theorem 2.2 holds with three changes: plateau values join the critical tolerances; at R² equal to a plateau value the plateau is excluded from 𝓕, which can split or remove components; and an end adjacent to a plateau at value L carries a ray iff R² < L.

*Proof.* As for Theorem 2.2(1)–(2). A constant piece of value p contributes the whole piece to 𝓕 if R² < p and nothing otherwise, which is constant on each interval of tolerances that avoids p. ∎

**Corollary 2.5 (equal-height maxima).** Suppose two interior maxima share the value M₂, are separated by a lower minimum, and just below M₂ each lies in a component touching neither end (the equality condition of Theorem 2.2(3)). Then just below M₂ both count in k, and at and above M₂ both windows are gone: k drops by 2 at one tolerance. The class is otherwise unaffected.

*Proof.* Theorem 2.2(3)–(4). ∎

Families with at most one maximum cannot produce this event.

**Corollary 2.6 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a flat-topped maximum acts as a maximum.

*Proof.* By Theorem 2.2(4) the class depends only on the ordered turning-point values, the endpoint limits and the approach directions. ∎

**Proposition 2.7 (pair birth).** Suppose a minimum–maximum pair is born as a family parameter passes δ = 0 through a nondegenerate fold: near the birth point, in a local coordinate x, dσ²/dθ ≈ a(x² − bδ) with a, b ≠ 0. Then for bδ > 0 the turning-point positions separate like δ^(1/2) and the values like M − m \~ δ^(3/2), so the band of tolerances that sees the pair opens continuously from zero width.

*Proof.* The roots of a(x² − bδ) are ±√(bδ), and the change in value between them is (4/3)|a|(bδ)^(3/2). ∎

*Verification status: Theorem 2.4 and Corollaries 2.5 and 2.6 were checked in Task 10 (T10.5): the plateau case; k = 2 just below an equal-height pair and Empty at and above it, by both classification routes; and 1,000 tolerances with identical classes with and without an inflection point. For Proposition 2.7, T10.5 fitted the exponents 1.50007 (values) and 0.50002 (positions) for the Hill gain with n = 2. The pre-registered pair-birth check failed on its criterion (Appendix D, Task 10); the result rests on the proof.*

### 2.6 From shape to topology

Non-monotonicity, extrema and window components are three different properties, and only the last is topological. The chain runs in one direction:

1. **Monotone curve.** The class is Empty, All or a single ray (lower if decreasing, upper if increasing). No other class is possible.
2. **Non-monotone curve.** It has at least one turning point. A curve whose only turning point is a minimum gives at most two rays, never a window component (this is the mechanism of Theorem 4.1).
3. **Interior maximum above R².** It lies in some component of 𝓕(R²).
4. **Window component.** That component is a window component only if, on each side of the maximum, the curve falls to R² or below before reaching the end: through a minimum at or below R², or an endpoint limit below R² (or equal to it and approached from below).

So a non-monotone curve can fail to window at a given tolerance, and one curve can show a window at one tolerance and a ray at another. The Hill gain shows all four levels in one family (Prop. 5.13).

### 2.7 Reparameterisation

**Corollary 2.8.** Let φ : D′ → D be a continuous strictly monotone bijection between open intervals, and set σ̃² = σ² ∘ φ. For every R², the failure set 𝓕̃(R²) = φ⁻¹(𝓕(R²)) has the same k. If φ is increasing it has the same (ℓ, u); if φ is decreasing, ℓ and u are exchanged. The signature is preserved, reversed when φ is decreasing.

*Proof.* φ is a homeomorphism, so it maps components to components and preserves being bounded away from both ends. An increasing φ maps neighbourhoods of θ′₋ onto neighbourhoods of θ₋; a decreasing one maps them onto neighbourhoods of θ₊. ∎

Classes are therefore properties of the failure set, not of the scale on which a sweep is plotted: Π, log Π and Π³ give the same classes. Orientation still matters: sweeping 1/Π instead of Π, or the sampling rate 1/Δt instead of Δt, turns every lower ray into an upper ray. Window widths and positions are not invariant; the starting study's window (1/9, 4) spans a factor of 36 in Π but a different length in any other coordinate.

### 2.8 Structural stability

Away from critical tolerances the class survives small errors in the variance curve, provided the error does not add wiggles where the curve crosses the tolerance.

**Proposition 2.9.** Let σ² satisfy C2 and let R² ∉ 𝒞. Then the crossing set {θ : σ²(θ) = R²} is finite, say {x₁, …, x\_m}. Choose disjoint compact intervals Nᵢ ⊂ D, each inside one monotone piece, with xᵢ in the interior of Nᵢ, and set

```latex
\eta = \inf\big\{\,|\sigma^2(\theta) - R^2| : \theta \in D \setminus \textstyle\bigcup_i \operatorname{int} N_i\big\}
```

Then η > 0, and every continuous σ̃² on D with

1. sup over D of |σ̃² − σ²| < η, and
2. σ̃² strictly monotone on each Nᵢ

has failure set 𝓕̃(R²) of the same class as 𝓕(R²).

*Proof.*

- **Finitely many crossings.** Since R² is not a turning-point value, crossings lie inside pieces, at most one per strictly monotone piece.
- **η > 0.** The function |σ² − R²| is continuous and positive on the closed set K = D \\ ∪ int Nᵢ, which contains no crossing. Near θ± it tends to |L± − R²|, which is positive because L± ∈ 𝒞 when finite (or to ∞). So it is bounded below on the tails, and on the compact remainder.
- **Signs off the crossings.** On K, condition 1 gives σ̃² − R² the same sign as σ² − R².
- **One crossing per Nᵢ.** The ends of Nᵢ lie in K, where σ² − R² takes opposite signs; so does σ̃² − R². By condition 2, σ̃² crosses R² exactly once in Nᵢ, in the same direction.
- **Conclusion.** σ̃² − R² and σ² − R² have the same ordered pattern of positive and negative intervals along D, ends included. Components correspond one to one, and so do the components touching each end. ∎

**Sufficient condition.** If σ² is C¹ with non-zero slope on each Nᵢ, condition 2 holds for any C¹ perturbation whose slope differs from σ²′ by less than min |σ²′| on each Nᵢ.

**Why condition 2 is needed.** Closeness in sup norm alone does not suffice: a wiggle of height below η placed at a crossing can cross R² several times and create extra, arbitrarily short components.

**Direction in condition 2.** Condition 2 names no direction, and none is needed: by condition 1, σ̃² − R² has the same sign as σ² − R² at both ends of Nᵢ, and those signs are opposite, so a strictly monotone σ̃² on Nᵢ is monotone in the same direction as σ².

**Reading.** The margin η is the operational meaning of "thin". When a class occupies a narrow band of tolerances, η is small and modelling errors larger than η can change the class. The Hill mixed band has median width 5 × 10⁻⁴ F (Prop. 5.13), and the sampled relay's prior dips reach 10^(−32,880,317) relative (Prop. 6.20). At a critical tolerance there is no margin at all: raising or lowering a maximum by any amount at R² equal to its value creates or removes a component.

**Relation to persistence stability.** Persistence diagrams are stable in sup norm: the bottleneck distance between the diagrams of two functions is at most the sup-norm distance between them \[31\]. The class at one fixed tolerance is not stable in that sense, because a small perturbation can push an extremum across R² or add a short component near a crossing. Proposition 2.9 is the fixed-level counterpart: it buys stability with a margin η and a monotonicity condition near the crossings. The contrast is between a summary over all levels at once, which is stable, and a single slice, which is not.

*Verification status: Corollary 2.8 and Proposition 2.9 were checked numerically in Task 15 under pre-registered criteria. For 2.8: 1,000 curves, each with increasing and decreasing, smooth and piecewise-linear reparameterisations, at 50 or more tolerances per curve including every critical value; 200,000 classifications, no class or signature mismatch. For 2.9: 1,000 perturbations on 500 curves satisfying both conditions; no class change. A perturbation that breaks only condition 2 (a wiggle of height 0.9η inside one Nᵢ) changed the class from an upper ray to (0, 1, 4), as the remark above predicts.*

### 2.9 What the framework supplies

Theorem 2.2 reduces every classification in this thesis to two tasks: compute the signature of a curve, or constrain which signatures a family can reach. The remaining chapters divide that work:

- **Chapter 3** gives the tool for computing signatures of the white-noise relay: a normal form in which every curve is a path across one fixed surface.
- **Chapters 4–6** compute signatures sweep by sweep.
- **Chapter 5** also measures *expressivity*: which signatures a gain family can reach, from every allowed class (arbitrary continuous gains) down to at most one window component (natural single-stage gains).
- **Chapter 7** constrains the optimal filter: along a causal information ordering its curve is monotone, so its signature has no turning points.

The spine is therefore: curve → signature → class; gain family → reachable signatures; optimality and information ordering → further restriction.

## 3. The Normal Form of the White-Noise Relay

For the scalar continuous-time relay with white sensory noise, every stationary variance is one fixed surface evaluated along a path: σ²(θ) = F·𝒱(ν(θ), q(θ)) (Theorem 3.2). The surface carries the floor crossing, the optimal filter and every tolerance boundary; a sweep or a gain family only chooses the path. This is the first of the thesis's two pillars. It does not reach coloured or sampled noise, or optimal filters beyond white noise; those are organised by causal information ordering in chapter 7.

*Verification status: Theorem 3.2 was checked by hand and then verified symbolically in Task 14 (Part G), in the reading ν = 2ΣΠ/λ², q = G/(FΠ).*

### 3.1 The model

A scalar error x is corrected toward a noisy signal with a gain G that depends on the observation precision Π:

```latex
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\mathrm{sim}},
\qquad
\sigma^2 = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}
```

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters \[4–9, 36–38\].

*Proof.* The state x is an Ornstein–Uhlenbeck process with rate a = λ + G and noise intensity D = G²/Π + 2Σ, so its stationary variance is D/(2a), which is the formula above. The two limits follow by substitution. ∎

### 3.2 Coordinates and the surface

Two dimensionless numbers carry all the dependence on λ, Σ, Π and G:

```latex
\nu = \frac{2F\Pi}{\lambda} = \frac{2\Sigma\Pi}{\lambda^2},
\qquad
q = \frac{G}{F\Pi}
```

ν is the signal-to-noise ratio accumulated over one relaxation time 1/λ; q is the gain measured against the floor precision FΠ. In them the variance takes one form.

**Theorem 3.2 (normal form).**

```latex
\frac{\sigma^2}{F} = \mathcal V(\nu, q) = \frac{1 + \nu q^2/4}{1 + \nu q/2}
```

*Proof.* Divide σ² by F = Σ/λ: σ²/F = (1 + G²/(2ΠΣ))/(1 + G/λ). With G = qFΠ, G/λ = νq/2 and G²/(2ΠΣ) = q²FΠ/(2λ) = νq²/4. ∎

This is Lemma 6.23 in better coordinates: with g = G/λ = νq/2 it reads (1 + g²/ν)/(1 + g). The coordinate q is preferred because the floor crossing and the optimal filter become simple in it (§3.3–3.4). Reducing filter performance to dimensionless indices is not new: Kalata's tracking index \[25\] does it with one parameter for α–β trackers. The contribution here is this two-parameter form for the continuous-time relay, and its use as a map of failure regions. Two partial derivatives are used throughout:

```latex
\frac{\partial \mathcal V}{\partial q} = \frac{\nu\,(\nu q^2 + 4q - 4)}{2(\nu q + 2)^2},
\qquad
\frac{\partial \mathcal V}{\partial \nu} = \frac{q\,(q - 2)}{(\nu q + 2)^2}
```

### 3.3 The floor crossing is the line q = 2

Subtracting the floor gives

```latex
\mathcal V(\nu, q) - 1 = \frac{\nu\, q\,(q - 2)}{4 + 2\nu q}
```

so σ² > F if and only if q > 2, whatever λ, Σ and Π are. This is **Corollary 3.3 (excess identity)**; in dimensional form it reads G > 2FΠ. The numerator of 𝒱 adds the noise the correction injects, νq²/4 in units of F; the denominator divides by the variance it removes, 1 + νq/2. Injection beats removal exactly when q > 2.

**Theorem 3.4 (window theorem).** Let G be continuous along the precision sweep, with G → 0 and G²/Π → 0 as Π → 0, and G → G∞ ∈ (0, ∞). Some tolerance yields a window class iff sup q > 2 along the path; every R² between F and sup σ² then gives class (0, 0, k) with k ≥ 1. The optimal filter never windows along precision, because its error decreases strictly (Proposition 3.5). Each family's condition is that supremum:

| Gain family | q along Π | sup q | Window condition | Label |
| --- | --- | --- | --- | --- |
| Bayesian weight cΠ/(Π + Π₀) | c/(F(Π + Π₀)), decreasing | κ = c/(FΠ₀), at Π → 0 | κ > 2 | Prop. 5.8 |
| Capped min(gΠ, c) | g/F, then c/(FΠ) | g/F | g > 2F | Prop. 5.10 |
| Hill n = 2 | cΠ/(F(Π² + Π₀²)), peaked at Π₀ | c/(2FΠ₀) | Π₀ < cλ/(4Σ) | Theorem 5.12 |
| Misspecified Kalman | decreasing from F′/F | F′/F | F′ > 2F | Prop. 5.9 |
| Precision-blind G₀ | G₀/(FΠ), unbounded at Π → 0 | ∞ | none: G → 0 fails, curve starts at ∞ | Prop. 5.11 |

The over-weighting ratio κ is therefore not a special Bayesian quantity: it is the value of q at the low-precision end, and it equals sup q only for gains whose G/Π decreases. For the Hill gain q starts at 0 and peaks inside the domain, so its condition is c/(FΠ₀) > 4, not > 2.

The condition sup q > 2 governs the **window class**, not window components. In the worked example (λ = c = 1, Σ = 0.01), the Hill gain with 25 ≤ Π₀ < 31.475 has sup q ≤ 2 yet produces a window component inside the mixed class (1, 0, 1) (Prop. 5.13).

### 3.4 The optimal filter is the lower envelope

At fixed ν, ∂𝒱/∂q vanishes where νq² + 4q − 4 = 0, which has one positive root:

```latex
q^\star(\nu) = \frac{2}{1 + \sqrt{1 + \nu}},
\qquad
\mathcal V_\star(\nu) = \mathcal V(\nu, q^\star) = q^\star(\nu)
```

The identity 𝒱⋆ = q⋆ holds because νq⋆²/4 = 1 − q⋆ at the root, so 𝒱⋆ = (2 − q⋆)/(1 + νq⋆/2) = q⋆. In dimensional form it is G⋆ = σ⋆²Π, the steady-state Kalman–Bucy gain \[1, 39, 40\] (Proposition 3.5, Lemma 3.6).

**Proposition 3.5 (optimal gain).** For this plant the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives

```latex
G^\star(\Pi) = p\,\Pi = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
\qquad
\sigma_\star^2(\Pi) = p = \frac{2\Sigma}{\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}}
```

G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.

**Lemma 3.6 (single minimum in the gain).** At fixed Π, σ² is strictly decreasing in G on (0, G⋆) and strictly increasing on (G⋆, ∞).

*Proof of Proposition 3.5 and Lemma 3.6.* The Riccati equation and its positive root give the steady-state Kalman–Bucy filter \[1, 39, 40\]. Differentiating the formula of Proposition 3.1 in G gives ∂σ²/∂G = (G² + 2λG − 2ΣΠ)/(2Π(λ + G)²), whose only positive zero is G⋆; this is Lemma 3.6, and it gives the minimality in Proposition 3.5. σ⋆² decreases strictly in Π because √(λ² + 2ΣΠ) increases, and it tends to 2Σ/(2λ) = F as Π → 0. Dividing G⋆ by FΠ with ν = 2ΣΠ/λ² gives q⋆ = 2(√(1 + ν) − 1)/ν = 2/(1 + √(1 + ν)). ∎

*Verification status: Proposition 3.5 in Tasks 1 and 7; Lemma 3.6 symbolically in Task 8 (T8.1).*

Three consequences follow at once:

- 𝒱 is strictly decreasing in q below q⋆ and strictly increasing above it, at every ν (Lemma 3.6).
- q⋆ < 1, so the optimal filter sits at least a factor of 2 below the floor-crossing line q = 2.
- 𝒱⋆ decreases strictly from 1 (ν → 0) to 0 (ν → ∞). Along the precision sweep the optimal filter's classes are therefore lower ray or Empty, as chapter 7 obtains from information ordering (Prop. 7.7(a)).

From ∂𝒱/∂ν, a path at constant q rises with precision when q > 2 and falls when q < 2: an over-gained relay gets worse as observations improve.

### 3.5 Tolerance boundaries

Write R²\_rel = R²/F. The boundary 𝒱 = R²\_rel is the quadratic q² − 2R²\_rel·q + 4(1 − R²\_rel)/ν = 0, with roots

```latex
q_\pm(\nu;\, R^2_{\mathrm{rel}}) = R^2_{\mathrm{rel}} \pm \sqrt{R^4_{\mathrm{rel}} + \frac{4\,(R^2_{\mathrm{rel}} - 1)}{\nu}}
```

Since 𝒱 − R²\_rel has the sign of (q − q₋)(q − q₊), the failure region at fixed ν is q > q₊ **or** q < q₋. Three regimes follow:

| Tolerance | Failure region in the (ν, q) plane | Consequence |
| --- | --- | --- |
| R²\_rel > 1 (looser than the floor) | q > q₊ only (q₋ < 0); q₊ falls from ∞ at ν → 0 to 2R²\_rel at ν → ∞ | failure needs over-gain; windows live here |
| R²\_rel = 1 (the floor) | q > 2 | the excess identity |
| R²\_rel < 1 (tighter than the floor) | everything for ν < ν\_R = 4(1 − R²\_rel)/R⁴\_rel; q < q₋ or q > q₊ beyond | every gain fails at low precision |

In dimensional form ν < ν\_R is Π < π\_R = 2λ(F − R²)/R⁴: below that precision the whole surface lies above the tolerance, which is the forced lower ray of Corollary 5.2. The two branches meet on the envelope, at q = R²\_rel and ν = ν\_R. Above the floor only the upper side matters; below it, under-gain fails too.

*Figure B.2 (Appendix B): the (ν, q) plane with the line q = 2, the envelope q⋆(ν), and the boundaries for R²\_rel = 0.5, 1 and 2.*

### 3.6 The inverse map: realizability

Solving 𝒱 = v/F for q inverts the surface:

```latex
q_\pm = \mathcal V \pm \sqrt{\mathcal V^2 + \frac{4(\mathcal V - 1)}{\nu}},
\qquad
G_+ = F\Pi\, q_+ = \Pi v + \sqrt{\Pi\,(\Pi v^2 + 2\lambda v - 2\Sigma)}
```

G₊ is exactly the realizing gain of Theorem 5.1. The root is real iff ν𝒱² + 4𝒱 − 4 ≥ 0, that is 𝒱 ≥ 𝒱⋆: the same quadratic as the envelope. So the surface is two-sheeted over its envelope. This is the scalar filtering analogue of covariance assignment \[14, 15, 41–44\], which characterises the state covariances a feedback gain can assign in multivariable control; in the scalar filter the attainable set is the whole half-line above the optimum, with an explicit gain. The upper sheet q₊ ≥ q⋆ holds the over-gained relays and the lower sheet q₋ ≤ q⋆ the under-gained ones.

Two results of chapter 5 read directly off this picture:

- **Realizability (Theorem 5.1).** Any continuous curve on or above the envelope is reached by a continuous gain on the upper sheet; nothing below the envelope is reachable.
- **The branch switch (Corollary 5.4).** On the upper sheet G₊ ≥ Πv, so G₊/Π → 2H whenever v → H > 0, and the gain diverges. A gain with a finite limit must cross from the upper sheet to the lower one, and can do so only where its path touches the envelope.

### 3.7 Sweeps as paths

A sweep is a path θ ↦ γ(θ) = (ν(θ), q(θ)), and σ²(θ) = F(θ)·𝒱(γ(θ)). Along a path parameterised by ν,

```latex
\frac{d\mathcal V}{d\nu} = \frac{q\,(q - 2) + \tfrac{\nu}{2}\,(\nu q^2 + 4q - 4)\, q'(\nu)}{(\nu q + 2)^2}
```

which is the elasticity lemma (Lemma 3.7) in normal form. Its turning points are the turning points of the variance curve, so a gain family's signature is read from its path.

**Lemma 3.7 (elasticity form).** For any differentiable gain G(Π) > 0 with elasticity ε = ΠG′/G,

```latex
\frac{d\sigma^2}{d\Pi} = \frac{G\,N}{2\Pi^2(\lambda + G)^2},
\qquad
N = \varepsilon\,(G^2 + 2\lambda G - 2\Sigma\Pi) - G(\lambda + G)
```

The turning points of σ²(Π) are the sign changes of N. When G is strictly monotone, N is a function of G alone.

*Proof.* dσ²/dΠ = ∂σ²/∂G · G′ + ∂σ²/∂Π = (G² + 2λG − 2ΣΠ)G′/(2Π(λ + G)²) − G²/(2Π²(λ + G)); then use ΠG′ = εG. ∎

*Verification status: symbolically in Task 10 (T10.1(a)).*

The failure set is the preimage of the failure region. With a fixed floor, 𝓕(R²) = {θ : 𝒱(γ(θ)) > R²/F}. With a moving floor, the threshold moves too: 𝓕(R²) = {θ : 𝒱(γ(θ)) > R²/F(θ)}.

| Sweep | ν | q | Floor | Path on the surface | Chapter |
| --- | --- | --- | --- | --- | --- |
| Prior precision Π₀, coupling c | fixed | moves with G | fixed | horizontal | 4 |
| Precision Π | ∝ Π | G(Π)/(FΠ) | fixed | a curve set by the gain family | 5 |
| Process noise Σ | ∝ Σ | G/(FΠ) | moves (F ∝ Σ) | relative tolerance: fixed boundary; absolute: boundary R²/F moves along the path | 6 |

A horizontal path crosses the unimodal section 𝒱(ν, ·) at most once through its minimum, so a monotone gain sweep at fixed precision has at most one turning point, a minimum, and never a window component (Theorem 4.1). Under a relative tolerance the threshold is constant again, which is why the Σ sweep then classifies like the precision sweep (Lemma 6.23).

### 3.8 Scope

The normal form covers the scalar, stationary, continuous-time relay with white sensory noise and a gain that is constant in time at each parameter value. Within that scope the white-noise results of chapters 3–5 read as objects on one surface:

| Result | On the surface |
| --- | --- |
| Excess identity (Cor. 3.3) | the line q = 2 |
| Optimal gain (Prop. 3.5, Lemma 3.6) | the envelope q = q⋆(ν) |
| Window theorem (Theorem 3.4) | sup q > 2 along the path |
| Monotone gain sweeps (Theorem 4.1) | horizontal paths through a unimodal section |
| Forced lower ray (Cor. 5.2) | for ν < ν\_R the surface lies above the tolerance |
| Realizability (Theorem 5.1) | the inverse map, upper sheet |
| Branch switch (Cor. 5.4) | crossing sheets at an envelope touch |
| Elasticity (Lemma 3.7) | the path derivative |
| Σ sweep, relative tolerance (Lemma 6.23) | a path against a fixed boundary |

One extension is immediate. Under matched-power coloured noise, handled by measurement differencing \[27, 28, 45\], Lemma 6.1 becomes a three-coordinate surface with t = λτ:

```latex
\mathcal V_\tau(\nu, q, t) = \frac{1 + \dfrac{\nu q^2}{4\,\big(1 + t\,(1 + \nu q/2)\big)}}{1 + \nu q/2},
\qquad
\frac{P}{F} = \frac{2}{1 + \nu t + \sqrt{(1 + \nu t)^2 + \nu (1 - t)^2}}
```

The second formula is the optimal filter along τ (Corollary 6.5); at t = 0 both reduce to the white-noise surface and its envelope. Chapter 6 uses them.

The normal form does not cover sampled observations (6.13–6.22), correlation time at matched variance or in the power family (Prop. 6.10, Theorem 7.8), or sensor delay (Prop. 7.11). There the optimal filter's behaviour is decided by the information structure of the observations, not by the shape of 𝒱, and chapter 7 takes over. Theorem 2.2 applies on both sides.

## 4. Design Sweeps as Horizontal Paths

A design sweep changes the filter but not what it observes, so its path on the surface 𝒱(ν, q) runs horizontally at fixed ν. Each horizontal section has a single minimum, so every design sweep has at most one turning point, a minimum, and can never produce a window component or a mixed class (Theorem 4.1). The two design parameters of the Bayesian-weight relay, prior precision and coupling, are classified completely here (Propositions 4.2–4.5); both reach their best value exactly at the optimal filter.

### 4.1 Why design sweeps are horizontal

A design sweep varies a parameter θ of the gain only. Precision Π, relaxation rate λ and process noise Σ stay fixed, so ν = 2FΠ/λ and the floor F are fixed, and only q(θ) = G(θ)/(FΠ) moves. By Lemma 3.6 the section q ↦ 𝒱(ν, q):

- equals 1 at q = 0 (no correction gives the floor);
- decreases strictly to its minimum 𝒱⋆(ν) = q⋆(ν) at q = q⋆;
- increases strictly after it, passing 1 again at q = 2 and growing without bound.

**Theorem 4.1 (monotone gain sweeps cannot window).** Fix Π. Let θ ↦ G(θ) be continuous and strictly monotone on D. Then σ²(G(θ), Π) is strictly monotone or strictly decreasing-then-increasing on D. Every failure set is therefore Empty, All, a lower ray, an upper ray or two rays; no window component and no mixed class can occur.

*Proof.* Composing the section of Lemma 3.6, which decreases and then increases, with a strictly monotone map gives a function with at most one interior turning point, a minimum. Such a function is strictly quasiconvex, so its sublevel sets {σ² ≤ R²} are intervals (possibly a point or empty). The complement of an interval in an open interval is at most two rays. ∎

The theorem covers every monotone design rule, not only the Bayesian weight: Task 8 ran 20,000 random parameter sets through five monotone gain sweeps each, 10⁶ classifications in all, with no window, no mixed class and no interior maximum, and the Task 13 audit repeated this for c·tanh(Π/Π₀), c(1 − e^(−Π/Π₀)) and cΠ²/(Π² + Π₀²) swept in Π₀. That audit row found no class outside the stated sets, but it failed its pre-registered rule on agreement between the two classification routes: 122 disagreements persisted, which Task 13 attributed to code, a sample point of the second route falling below its equality tolerance at an exact limit (Appendix D).

Two consequences shape the rest of the chapter:

- **The optimal filter is fixed along a design sweep**, because the observations do not change. Design sweeps therefore classify miscalibration only; there is no optimal-filter column.
- **A sweep whose gain passes through G⋆ has minimum value exactly σ⋆²(Π).** The best setting of any design parameter reproduces the steady-state Kalman–Bucy filter, and both directions of misweighting are worse.

### 4.2 Prior precision

Fix Π > 0 and c > 0. The Bayesian-weight gain G(Π₀) = cΠ/(Π + Π₀) decreases strictly from c (as Π₀ → 0) to 0 (as Π₀ → ∞), so q moves left along the section, from q\_c = c/(FΠ) to 0. Write

```latex
V_c = \sigma^2(c, \Pi) = \frac{\Sigma + c^2/(2\Pi)}{\lambda + c},
\qquad
\Pi_A = \frac{c(c + 2\lambda)}{2\Sigma},
\qquad
\Pi_B = \frac{c}{2F} = \frac{c\lambda}{2\Sigma}
```

so that Π\_B < Π\_A. In normal form the three cases below are simply where the starting point q\_c sits on the section: Π ≥ Π\_A means q\_c ≤ q⋆; Π\_B ≤ Π < Π\_A means q⋆ < q\_c ≤ 2; Π < Π\_B means q\_c > 2.

**Proposition 4.2 (prior precision: endpoints and extrema).**

- L₊ = F, approached from below; L₋ = V\_c, with the approach direction below.
- If Π ≥ Π\_A (c ≤ G⋆), σ² increases strictly from V\_c, approached from above, to F. There is no interior extremum.
- If Π < Π\_A (c > G⋆), there is exactly one interior extremum, a global minimum at Π₀⋆ = Π(c/G⋆ − 1) with value σ⋆²(Π); V\_c is then approached from below.
- V\_c > F iff Π < Π\_B, and V\_c = F iff Π = Π\_B.

*Proof.* Compose Lemma 3.6 with the strictly decreasing map Π₀ ↦ G. The gain passes through G⋆ iff c > G⋆, which is c² + 2λc > 2ΣΠ, i.e. Π < Π\_A; solving cΠ/(Π + Π₀) = G⋆ gives Π₀⋆. Near Π₀ = ∞, G → 0⁺ where σ² decreases in G, so σ² increases in Π₀ and F is approached from below. Near Π₀ = 0, G → c⁻: if c > G⋆, σ² increases in G there, so it decreases in Π₀ and V\_c is approached from below; if c ≤ G⋆ the reverse. V\_c against F is Corollary 3.3 at G = c. ∎

**Proposition 4.3 (prior precision: classification at every tolerance).**

*Case P1, Π ≥ Π\_A* (sequence V\_c, F):

| Tolerance | Class |
| --- | --- |
| R² ≤ V\_c | All |
| V\_c < R² < F | Upper ray |
| R² ≥ F | Empty |

*Case P2, Π\_B ≤ Π < Π\_A* (sequence V\_c, σ⋆², F, with σ⋆² < V\_c ≤ F):

| Tolerance | Class |
| --- | --- |
| R² < σ⋆² | All |
| R² = σ⋆² | Two rays (D minus the single point Π₀⋆) |
| σ⋆² < R² < V\_c | Two rays |
| V\_c ≤ R² < F | Upper ray (empty band when Π = Π\_B) |
| R² ≥ F | Empty |

*Case P3, Π < Π\_B* (sequence V\_c, σ⋆², F, with σ⋆² < F < V\_c):

| Tolerance | Class |
| --- | --- |
| R² < σ⋆² | All |
| σ⋆² ≤ R² < F | Two rays (at equality, D minus Π₀⋆) |
| F ≤ R² < V\_c | Lower ray |
| R² ≥ V\_c | Empty |

*Proof.* Theorem 2.2 applied to Proposition 4.2. F is approached from below, so R² = F never gives an upper ray. V\_c is approached from above in P1, so R² = V\_c gives All there, and from below in P2–P3, so R² = V\_c gives no lower ray. The minimum value σ⋆² is attained only at Π₀⋆, which is the single point removed at R² = σ⋆². ∎

**Worked example** (λ = c = 1, Σ = 0.01, so F = 0.01, Π\_B = 50, Π\_A = 150):

| Π | Case | Π₀⋆ | σ⋆² | V\_c |
| --- | --- | --- | --- | --- |
| 1 | P3 | 99.498 | 0.0099505 | 0.255 |
| 60 | P2 | 64.162 | 0.0080540 | 0.0091667 |
| 500 | P1 | none | — | 0.0055 |

**Reading.** The best fixed prior at a given precision is the one that makes the Bayesian weight equal the Kalman–Bucy gain; both a prior that is too weak and one that is too strong are worse. At low precision the two-ray band is extremely thin (at Π = 1, σ⋆² is only 0.5% below F); at intermediate precision it is wide (at Π = 60 it spans 0.0080540 to 0.0091667, about 11% of F). The prior sweep never windows, whatever the precision.

### 4.3 Coupling

Fix Π and Π₀, and write K = Π/(Π + Π₀) ∈ (0, 1). The gain G = cK increases strictly from 0 to ∞ as c does, so q moves right along the whole section, from 0 to ∞. It therefore always passes q⋆, and always crosses the floor line q = 2.

**Proposition 4.4 (coupling: endpoints and extrema).** L₋ = F, approached from below, and L₊ = ∞. There is exactly one interior extremum, a global minimum at

```latex
c^\star = \frac{G^\star(\Pi)}{K} = \frac{(\Pi + \Pi_0)\big(\sqrt{\lambda^2 + 2\Sigma\Pi} - \lambda\big)}{\Pi}
```

with value σ⋆²(Π). The variance returns to F at c\_F = 2FΠ/K = 2F(Π + Π₀), and σ² > F iff c > c\_F.

*Proof.* Lemma 3.6 composed with the strictly increasing map c ↦ cK, which passes through G⋆ and through 2FΠ. ∎

**Proposition 4.5 (coupling: classification at every tolerance).** There is no case split.

| Tolerance | Class |
| --- | --- |
| R² < σ⋆² | All |
| R² = σ⋆² | Two rays (D minus the single point c⋆) |
| σ⋆² < R² < F | Two rays |
| R² ≥ F | Upper ray (c\_R, ∞), where c\_R > c⋆ solves σ² = R² (so c\_R = c\_F at R² = F) |

The class is never Empty, because σ² → ∞ as c → ∞, and never a window.

*Proof.* Theorem 2.2 with the sequence (F, σ⋆², ∞) and F approached from below. ∎

**Worked example** (λ = 1, Σ = 0.01, Π = Π₀ = 1): c⋆ = 0.019901, σ⋆² = 0.0099505, c\_F = 0.04.

**Reading.** Coupling behaves like a volume control on the correction. Too little coupling wastes the observations; too much admits more measurement noise than the damping is worth, and beyond c\_F the relay is worse than no filtering at all, at every tolerance at or above the floor.

### 4.4 Summary

| Sweep | Path on the surface | Classes | Never |
| --- | --- | --- | --- |
| Any monotone gain at fixed Π | horizontal, monotone in q | Empty, All, lower ray, upper ray, two rays | window, mixed (Theorem 4.1) |
| Prior precision Π₀ | horizontal, from q\_c down to 0 | P1: All, upper ray, Empty; P2: adds two rays; P3: All, two rays, lower ray, Empty | window (Proposition 4.3) |
| Coupling c | horizontal, from 0 up to ∞ | All, two rays, upper ray | Empty, window (Proposition 4.5) |

**Verification.** Lemma 3.6 and Propositions 4.2 and 4.4 were checked symbolically, every identity reducing to zero (Task 8, checks T8.1–T8.2). Propositions 4.3 and 4.5 were checked at every row, including each critical tolerance exactly and at ±10⁻⁶ relative and the boundary cases Π = Π\_A and Π = Π\_B: 62 of 62 classes correct, computed by root-finding on monotone pieces (T8.3). Theorem 4.1 was checked on 10⁶ classifications (T8.4), and Task 13 re-audited all three rows on 1,000 fresh parameter sets each with no class outside the stated sets. The audit row for the Π₀ sweep of the tanh, exponential and Hill-type gains (§4.1) failed its pre-registered route-agreement rule; it is recorded as a failure, attributed to code (Appendix D, Task 13).

*Figure B.3 (Appendix B): σ² along the prior sweep at Π = 1 (case P3, U-shaped) and Π = 500 (case P1, monotone), and along the coupling sweep at Π = Π₀ = 1, with c⋆ and c\_F marked.*

## 5. The Precision Sweep: Expressivity of Gain Families

Along precision the gain family chooses the path through the (ν, q) plane: ν grows in proportion to Π, and q = G(Π)/(FΠ) is whatever the design rule makes it. This chapter asks two questions. What does the model itself allow along precision, whatever the gain? And what do the gain families used in practice actually produce? The first has a short answer: the model rules out exactly one thing, a variance below the optimum (§5.1). Every further restriction belongs to a gain family (§5.2–5.5).

### 5.1 What the model allows

**Theorem 5.1 (gain realizability).** Fix λ, Σ > 0. A function v : (0, ∞) → (0, ∞) is the variance curve σ²(G(Π), Π) of some continuous gain schedule G ≥ 0 if and only if v is continuous and v ≥ σ⋆² everywhere. One such gain is the upper-branch inverse

```latex
G_+(v, \Pi) = \Pi v + \sqrt{\Pi\,(\Pi v^2 + 2\lambda v - 2\Sigma)}
```

*Proof.* Necessity is Proposition 3.5. For sufficiency, σ²(G, Π) = v is the quadratic G² − 2ΠvG + 2Π(Σ − λv) = 0, with roots G± = Πv ± √(Π(Πv² + 2λv − 2Σ)). The radicand is non-negative iff Πv² + 2λv − 2Σ ≥ 0, and the positive root of that quadratic in v is G⋆/Π = σ⋆² (Proposition 3.5), so the condition is v ≥ σ⋆². Then G₊(v(Π), Π) is continuous, and G₊ ≥ Πv > 0. ∎

In the coordinates of chapter 3 this is the inverse map of §3.6: a curve on or above the envelope is reached on the upper sheet, and nothing below the envelope is reached at all. It is the scalar filtering analogue of covariance assignment \[14, 15, 41–44\]; in the scalar filter the attainable set is the whole half-line above the optimum, and the gain is explicit.

**Corollary 5.2 (forced lower ray).** For every continuous gain schedule and every R² < F, the failure set contains (0, π\_R), with π\_R = 2λ(F − R²)/R⁴. Hence ℓ = 1: at a tolerance tighter than the floor, no gain gives Empty, a pure window, an upper ray alone, or any other class with ℓ = 0.

*Proof.* σ⋆² decreases strictly from F (Proposition 3.5) and equals R² where ΠR⁴ + 2λR² − 2Σ = 0, that is at Π = π\_R. For Π < π\_R, σ² ≥ σ⋆² > R². ∎

So "windows need loose tolerances" holds for every gain schedule, with no regularity assumption. In the (ν, q) plane, π\_R is the precision ν\_R of §3.5, below which the whole surface lies above the tolerance.

**Corollary 5.3 (exact class set along precision).** For continuous, piecewise strictly monotone variance curves: for R² < F the achievable classes are exactly those with ℓ = 1 (any u, any finite k, including All); for R² ≥ F every class with finite k is achievable.

*Proof.* Impossibility is Corollary 5.2. For achievability, by Theorem 5.1 it is enough to build a continuous, piecewise strictly monotone v ≥ σ⋆² with the target class. For R² < F, follow σ⋆² on (0, π\_R\] and then a zigzag in log Π with troughs at R² and peaks above it. For R² ≥ F, use troughs at F and peaks above R², starting above R² (for ℓ = 1) or on σ⋆² (for ℓ = 0). For All, take v = σ⋆² + R². ∎

The constructions above may use gains that diverge or oscillate at the ends of the sweep. Under the regularity of Theorem 3.4 the endpoint limits are pinned, but the number of windows is not.

**Corollary 5.4 (unbounded windows for regular gains).** For every k ≥ 1 there is a C^∞ gain schedule with the regularity of Theorem 3.4 (G → 0 and G²/Π → 0 as Π → 0; G → G∞ ∈ (0, ∞)) whose failure set at R² = 1.25F has exactly k windows.

*Proof.* Take the Bayesian-weight gain G\_B with 1 < κ < 2 (Proposition 5.8). Its variance v\_B = σ²(G\_B, ·) stays below F and is smooth and strictly decreasing. Near Π = 0, G\_B > G⋆ (its initial slope is κF > F); for large Π, G\_B < G⋆. So G\_B first meets G⋆ at some Π\_c, where v\_B touches σ⋆², and G\_B = G₊(v\_B, ·) on (0, Π\_c). Choose k disjoint closed intervals inside (0, Π\_c). On each, set v = v\_B + b with b ≥ 0 smooth and equal to 0 near the interval's ends, such that v rises strictly to a peak value 1.5F and then falls strictly: on the rising flank take b′ > |v\_B′|, on the falling flank b′ ≤ 0. Set v = v\_B elsewhere, G = G₊(v, ·) on (0, Π\_c) and G = G\_B beyond. Outside the bump intervals G = G\_B, so G is smooth and keeps the regularity of G\_B at both ends. Each bump rises strictly and then falls strictly, so it crosses 1.25F exactly twice, and v\_B < F elsewhere. ∎

The construction has to leave the upper sheet before the end of the sweep. On that sheet G₊ ≥ Πv, so G₊/Π → 2H whenever v → H > 0, and the gain diverges; a gain with a finite limit can cross to the lower sheet only where its path touches the envelope (§3.6). In the proof that crossing is the point Π\_c.

*Figure B.4 (Appendix B): a realized curve with three windows at R² = 1.25F on a Bayesian-weight base curve, and the forced lower ray at R² = 0.6F.*

**Corollary 5.5 (what regularity pins).** Under the regularity of Theorem 3.4, L₋ = F and L₊ = H = Σ/(λ + G∞). So ℓ is fixed by R² against F (with the approach direction when R² = F), u by R² against H, and k is unbounded (Corollary 5.4). Since H < F, there is never an upper ray when R² ≥ F.

*Proof.* The limits are those of Proposition 3.1; the rest is Theorem 2.2. ∎

Along precision, then, the model rules out exactly one thing: being better than the optimal filter. Every further restriction is a property of the gain family.

**Verification.** Theorem 5.1 was checked symbolically (Task 10, T10.1) and by 101 of 101 target constructions (T10.2). Corollaries 5.2 and 5.3 were checked by the same 101 constructions and by 24 of 24 forbidden targets, each blocked (T10.2). Two symbolic items failed in the pre-registered SymPy route, which could not simplify square roots of squares; the identities hold by the factor-radicand route (Appendix D, Task 10). For Corollary 5.4, the construction first pre-registered failed its check (Appendix D, Task 10). The construction given in the proof passed for k = 1 to 5, with the gain converging (G(10¹²)/G(10¹¹) − 1 = 6 × 10⁻¹⁰).

### 5.2 Tools for gain families

Three lemmas do most of the work for particular families. Lemma 3.7 locates turning points through the elasticity ε = ΠG′/G. The next two fix the excess set and the high-precision end.

**Lemma 5.6 (excess components).** {σ² > F} = {G/Π > 2F} pointwise. Hence at R² = F the failure set is the excess set; for R² ≥ F every failure component lies in an excess component; and if G/Π is unimodal or decreasing, there is at most one window at R² = F.

*Proof.* Corollary 3.3, applied at each Π: σ² > F iff q = G/(FΠ) > 2. For R² ≥ F, {σ² > R²} ⊂ {σ² > F}. If G/Π is unimodal or decreasing, {G/Π > 2F} is an interval. ∎

**Lemma 5.7 (bounded gains approach H from above).** If G < G∞ everywhere, then σ² ≥ Σ/(λ + G) > H, so H is approached from above and never attained.

*Proof.* σ² ≥ Σ/(λ + G) because G²/(2Π) ≥ 0, and Σ/(λ + G) > Σ/(λ + G∞) = H. ∎

### 5.3 Monotone and saturating families

The starting study's gain is the one-step Bayesian weight, a precision-weighting rule \[2, 3\].

**Proposition 5.8 (Bayesian-weight gain along precision).** Let G = cΠ/(Π + Π₀), with over-weighting ratio κ = (c/Π₀)/F. Then σ² has one turning point, a maximum M, iff κ > 2, and is strictly decreasing otherwise. The endpoint limits are F (approached from above iff κ > 2) and H = Σ/(λ + c) (approached from above). The classes are:

- κ > 2: All (R² ≤ H), lower ray (H < R² ≤ F), window (F < R² < M), Empty (R² ≥ M);
- κ ≤ 2: All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F).

*Proof.* Here ε = Π₀/(Π + Π₀) = 1 − G/c, and eliminating Π = Π₀G/(c − G) in Lemma 3.7 gives N = −(G/c)(G² + 2λG + 2ΣΠ₀ − λc). As Π runs over (0, ∞), G runs once over (0, c). The quadratic has the positive root G = −λ + √(λ² + λc − 2ΣΠ₀), which lies below c, iff λc > 2ΣΠ₀, that is κ > 2. Near Π = 0 the quadratic is close to 2ΣΠ₀ − λc, so N > 0 there when κ > 2 and the turning point is a maximum. G/Π → κF, so F is approached from above iff κ > 2 (Lemma 5.6). H is approached from above by Lemma 5.7. The classes follow from Theorem 2.2. ∎

The over-weighting ratio decides the window, and the peak is unique.

**Proposition 5.9 (misspecified Kalman gain).** Let G = −λ′ + √(λ′² + 2Σ′Π), the steady-state gain designed for wrong parameters λ′ and Σ′, with F′ = Σ′/λ′ and r = Σ/Σ′. If F′ > 2F, σ² has exactly one turning point, a maximum, at the gain

```latex
G_M = \frac{-2r\lambda' + \sqrt{4r^2\lambda'^2 + 2(1 + r)\lambda'(\lambda - 2r\lambda')}}{1 + r},
\qquad
\Pi_M = \frac{G_M^2 + 2\lambda' G_M}{2\Sigma'}
```

If F′ ≤ 2F, σ² is strictly decreasing. L₋ = F (approached from above iff F′ > 2F) and L₊ = 0. The classes are lower ray (0 < R² ≤ F), window (F < R² < M) and Empty (R² ≥ M) when F′ > 2F, and lower ray (R² < F) and Empty (R² ≥ F) otherwise. All never occurs.

*Proof.* Π(G) = (G² + 2λ′G)/(2Σ′) and ε = (G + 2λ′)/(2(G + λ′)), so Lemma 3.7 gives N = G·p(G)/(2(G + λ′)) with p(G) = −(1 + r)G² − 4rλ′G + 2λ′(λ − 2rλ′). The function p is strictly decreasing on G > 0, and p(0) > 0 iff F′ > 2F; so there is at most one sign change, from + to −. As Π → ∞, G²/(2Π) → Σ′ while G → ∞, so σ² → 0. The direction at Π → 0 follows from Lemma 5.6, since G/Π → F′. ∎

The onset matches the Bayesian-weight onset with κ replaced by F′/F, but the peak is higher. At over-weighting ratio 100 (κ = F′/F = 100, with λ = λ′ = c = 1, Σ = 0.01), the peak is M/F = 17.575 for the misspecified Kalman gain against 9.2875 for the Bayesian weight, a ratio of 1.892.

*Figure B.6 (Appendix B): peak variance M/F against the initial over-weighting for the two gains.*

**Proposition 5.10 (capped gain).** Let G = min(gΠ, c). On the linear branch dσ²/dΠ = g(gλ/2 − Σ)/(λ + gΠ)², of constant sign g − 2F; on the capped branch σ² is strictly decreasing. So:

- g > 2F: one maximum, at the kink Π = c/g;
- g < 2F: σ² is strictly decreasing;
- g = 2F: a plateau σ² ≡ F on (0, c/g\], then strictly decreasing. By Theorem 2.4 the classes are All (R² ≤ H), lower ray (H < R² < F) and Empty (R² ≥ F).

The classes that occur are All, lower ray, window and Empty.

**Proposition 5.11 (precision-blind gain).** For a constant gain G = G₀, σ² decreases strictly from ∞ to H = Σ/(λ + G₀). The classes are All (R² ≤ H) and lower ray (R² > H).

A precision-blind gain over-gains at low precision without bound (q = G₀/(FΠ) → ∞), so its curve starts at ∞ and never returns to F; it fails the regularity of Theorem 3.4 at the low-precision end, and it never windows.

### 5.4 The Hill gain and the mixed class

The Hill gain G = cΠⁿ/(Πⁿ + Π₀ⁿ) is the divisive-normalisation form of neural gain control \[16, 17\], used here as an estimator gain. Unlike the families of §5.3, its ratio G/Π rises and then falls, so q starts at 0, peaks inside the sweep and decays.

**Theorem 5.12 (Hill gain, every real n > 1).** Let G = cΠⁿ/(Πⁿ + Π₀ⁿ) with n > 1, t = Π/Π₀ and T = tⁿ, and set

```latex
P_n(T) = -(\lambda + c)\,T^2 + (n - 1)(c + 2\lambda)\,T + (2n - 1)\lambda,
\qquad
\varphi_n(t) = \frac{t^{\,n-1} P_n(t^n)}{(1 + t^n)^2}
```

(a) σ² has either no turning point or exactly two, a minimum followed by a maximum. The pair exists iff Π₀ < Π₀^pair(n) = c·φₙ(t\*)/(2nΣ), where t\* is the unique maximiser of φₙ. At equality there is a single degenerate stationary point.

(b) For n = 2, t\*² = 2√3 − 3 and

```latex
\Pi_0^{\mathrm{pair}} = \frac{c\,\varphi_*}{4\Sigma},
\qquad
\varphi_* = \frac{t^*\big(\lambda(16\sqrt3 - 24) + c(14\sqrt3 - 24)\big)}{16 - 8\sqrt3}
```

*Proof.* With ε = n/(1 + T), Lemma 3.7 gives N(1 + T)³ = c·T·Pₙ(T) − 2nΣΠ₀·t·(1 + T)², so sign N = sign(c·φₙ(t)/(2n) − ΣΠ₀). As a function of T, φₙ = T^a Pₙ(T)/(1 + T)² with a = (n − 1)/n ∈ (0, 1), and dφₙ/dT = T^(a−1) R(T)/(1 + T)³ with R(T) = a·Pₙ·(1 + T) + T(1 + T)Pₙ′ − 2T·Pₙ. Write Pₙ = p₂T² + p₁T + p₀, with p₂ = −(λ + c) < 0, p₁ = (n − 1)(c + 2λ) > 0 and p₀ = (2n − 1)λ > 0. The cubic R has coefficients a·p₀ > 0, a(p₀ + p₁) + p₁ − 2p₀, (a − 1)p₁ + (a + 2)p₂ < 0 and a·p₂ < 0. Whatever the sign of the linear coefficient, there is exactly one sign change, so by Descartes' rule R has exactly one positive root. Hence φₙ rises from φₙ(0⁺) = 0 to its maximum at t\* and then decreases to −∞. Near t = 0, N(1 + T)³/t = c·t^(n−1)Pₙ − 2nΣΠ₀(1 + T)² → −2nΣΠ₀ < 0. So N is negative throughout, or changes sign −, +, −: a minimum, then a maximum. For n = 2, R(t²) = −½(t⁴ + 6t² − 3)((λ + c)t² + λ), whose positive root is t\*² = 2√3 − 3. ∎

At λ = c = 1, Σ = 0.01, the pair threshold is Π₀^pair = 30.243, 31.475, 37.820, 44.180 and 62.711 for n = 1.5, 2, 3, 4 and 8.

**Proposition 5.13 (Hill gain: classification and the mixed class).** Let H = Σ/(λ + c). σ² tends to F from below as Π → 0 (since G/Π → 0 < 2F) and to H from above as Π → ∞ (Lemma 5.7), and H < m < F when the pair exists, so two rays never occur. With the pair and M > F (for n = 2, Π₀ < cλ/(4Σ), the window condition of Theorem 3.4):

| Tolerance | Class |
| --- | --- |
| R² ≤ H | All |
| H < R² < m | Lower ray |
| m ≤ R² < F | Lower ray + window (1, 0, 1) |
| F ≤ R² < M | Window |
| R² ≥ M | Empty |

With the pair and M ≤ F: All (R² ≤ H), lower ray (H < R² < m), (1, 0, 1) (m ≤ R² < M), lower ray (M ≤ R² < F), Empty (R² ≥ F). Without the pair: All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F).

*Proof.* Theorem 2.2 applied to the signature of Theorem 5.12, with the endpoint limits and directions above. ∎

The mixed class is narrow in practice. Across the census of Task 10, the band width (min(M, F) − m)/F has median 5 × 10⁻⁴, with range 4 × 10⁻²² to 0.96, and in 16% of parameter sets the mixed band exists with no window above F. In the worked example (λ = c = 1, Σ = 0.01, n = 2), the Hill gain with 25 ≤ Π₀ < 31.475 has sup q ≤ 2, yet it produces a window component inside the mixed class.

*Figure B.5 (Appendix B): for the Hill gain with n = 2, the turning-point values over Π₀, the mixed band and the window band, with the pair birth and the window onset marked.*

The families of §5.3 cannot produce this class. The next proposition gives the reason: a gain that increases while G/Π strictly decreases never has a minimum at or below the floor.

**Proposition 5.14 (no mixed class when G/Π decreases).** In the setting of Theorem 3.4, suppose moreover that G is increasing and G(Π)/Π is strictly decreasing, as for any sum of Bayesian stages cᵢΠ/(Π + Π₀,ᵢ). Then σ² is strictly decreasing wherever σ² ≤ F. So every interior minimum lies above F, and no failure set combines a lower ray with a window: the classes (1, 0, k), k ≥ 1, do not occur.

*Proof.* 2Π²(λ + G)²·dσ²/dΠ = ΠG′(2λG + G² − 2ΣΠ) − G²(λ + G), and σ² ≤ F iff 2ΣΠ ≥ λG. There the bracket is at most G(λ + G), so, since G′ ≥ 0, the right side is at most G(λ + G)(ΠG′ − G), which is negative because G/Π is strictly decreasing. For a Bayesian stage, ΠGᵢ′ − Gᵢ = −cᵢΠ²/(Π + Π₀,ᵢ)² < 0. ∎

### 5.5 Two-stage gains

Sums of natural stages behave differently once the stages are widely separated in Π₀.

**Numerical result 5.15 (two-stage gains).** Sums of two widely separated natural stages produce more than one maximum. Two-channel Bayesian gains show (max, min, max) in 7 of 2,000 parameter sets, giving multi-window failure sets. Two-channel Hill gains show (min, max, min, max) in 63 of 2,000 sets, giving mixed multi-window failure sets. For the Bayesian sums the windows always lie above F and never join a lower ray, as Proposition 5.14 requires. No bound on the number of turning points of such sums is known (chapter 9).

### 5.6 Summary

| Gain family | Turning points | Classes along Π | Window condition | Result |
| --- | --- | --- | --- | --- |
| Any continuous gain | any | for R² < F, every class with ℓ = 1; for R² ≥ F, every class | — | Theorem 5.1, Cor. 5.2–5.3 |
| Regular gains (Theorem 3.4) | any | ℓ fixed by F, u by H; k unbounded | sup q > 2 | Cor. 5.4–5.5 |
| Bayesian weight | at most 1 (maximum) | All, lower ray, window, Empty | κ > 2 | Prop. 5.8 |
| Misspecified Kalman | at most 1 (maximum) | lower ray, window, Empty; never All | F′ > 2F | Prop. 5.9 |
| Capped | at most 1 (maximum at the kink), or a plateau | All, lower ray, window, Empty | g > 2F | Prop. 5.10 |
| Precision-blind | none | All, lower ray | never | Prop. 5.11 |
| Hill, n > 1 | none, or a minimum then a maximum | All, lower ray, (1, 0, 1), window, Empty | M > F (n = 2: Π₀ < cλ/(4Σ)) | Theorem 5.12, Prop. 5.13 |
| Increasing G with G/Π decreasing | any | no (1, 0, k) | — | Prop. 5.14 |
| Two-stage sums | up to 4 observed | multiple windows; mixed multi-window (Hill sums) | — | Num. result 5.15 |

**Verification.**

- Proposition 5.8 was proved in the starting study and checked there (Tasks 1, 3 and 7). Its reduction was re-checked in Task 10 (T10.3, turning-point position error 6 × 10⁻³¹), and its classes in T10.7 and in the Task 13 class audit (row 2).
- Proposition 5.9: symbolic by the factor-radicand route (T10.1), 2,000 of 2,000 parameter sets (T10.3), Task 13 audit row 3.
- Propositions 5.10 and 5.11: T10.3 (and T10.5 for the plateau), Task 13 audit rows 4 and 5.
- Theorem 5.12(b) was checked symbolically (T10.1(e)) and on all 2,000 random sets with n = 2 (961 with the pair, 1,039 without), with no disagreement in the number of roots. Part (a) was checked in Task 13 (A5): symbolic identities, a regression of Π₀^pair(n) against Task 10's values for n = 1.5, 2, 3, 4 and 8, and 5,000 random sets with real n in \[1.01, 10\]. Task 10's census covered 10,000 sets (T10.3).
- Proposition 5.13: 4,868 sets with two turning points, 77,888 tolerances, no mismatch (T10.4); Task 13 audit rows 6 and 7.
- Proposition 5.14 was proved after a failure: row 8 of the Task 13 class audit stated a class (1, 0, 1) for sums of Bayesian stages that cannot occur. The class set was corrected and the proof's steps checked in SymPy (Appendix D, Task 13).
- Numerical result 5.15 comes from an exploratory census (T10.3) and Task 13 audit rows 8 and 9.

## 6. Beyond White Noise

Chapters 3–5 kept the sensory noise white and varied the gain or the precision. This chapter keeps the gain rule fixed and changes the noise or the clock instead: the noise's correlation time τ (§6.1–6.2), the sampling interval Δt (§6.3–6.5) and the process noise Σ, which moves the floor itself (§6.6). Each sweep is classified by Theorem 2.2. Two results matter most for chapter 7: along matched-variance τ the optimal filter windows (Counterexample 6.11), and along Δt its error metrics move in opposite directions (Theorem 6.19).

### 6.1 Correlation time at matched zero-frequency power

Let the sensory noise η be Ornstein–Uhlenbeck with correlation time τ > 0, normalised so that its zero-frequency power stays 1/Π:

```latex
C_\eta(u) = \frac{e^{-|u|/\tau}}{2\Pi\tau},
\qquad
S_\eta(\omega) = \frac{1/\Pi}{1 + \tau^2\omega^2}
```

As τ → 0 this tends to white noise of intensity 1/Π, the model of chapter 3. The relay's gain is set by precision alone, so along τ it is a constant G > 0 (G = 0 gives σ² ≡ F). Write a = λ + G.

**Lemma 6.1 (relay variance).**

```latex
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2}{2\Pi(1 + a\tau)}\right),
\qquad
\sigma^2 > F \iff \frac{G}{\Pi} > 2F(1 + a\tau)
```

*Proof.* The process-noise part contributes Σ/a. A first-order filter 1/(s + a) driven by Ornstein–Uhlenbeck input of variance v and rate 1/τ has output variance v/(a(a + 1/τ)); with v = G²/(2Πτ) this is G²/(2Πa(1 + aτ)). The excess form follows by subtracting F. ∎

In the coordinates of chapter 3, with t = λτ, this is the three-coordinate surface 𝒱\_τ(ν, q, t) of §3.8. Colouring divides the injected noise νq²/4 by 1 + t(1 + νq/2), so the excess threshold rises from q > 2 to q > 2(1 + aτ).

**Proposition 6.2 (relay: endpoints and monotonicity).** σ² is strictly decreasing in τ, from V\_w = (Σ + G²/(2Π))/(λ + G) (approached from below) to H\_G = Σ/(λ + G) (approached from above). Always H\_G < F, and V\_w > F iff G > 2FΠ.

*Proof.* The only τ-dependence is the factor 1/(1 + aτ). The approach directions follow for a decreasing function; V\_w against F is Corollary 3.3. ∎

**Proposition 6.3 (relay: classification).** The classes are All (R² ≤ H\_G), lower ray (0, τ\_R) (H\_G < R² < V\_w) and Empty (R² ≥ V\_w), with

```latex
\tau_R = \frac{1}{a}\left(\frac{G^2}{2\Pi(aR^2 - \Sigma)} - 1\right)
```

At R² = F the class is the lower ray (0, τ\_F), τ\_F = (G/(2FΠ) − 1)/a, if G > 2FΠ, and Empty otherwise.

*Proof.* Theorem 2.2 with the signature (V\_w, H\_G); solve Lemma 6.1 for τ. ∎

In the worked example (λ = c = 1, Σ = 0.01, Π = Π₀ = 1, so G = 0.5): V\_w = 0.09, H\_G = 0.0066667 and τ\_F = 16; σ²(1) = 0.04, σ²(10) = 0.011875 and σ²(16) = 0.01. At matched zero-frequency power, colouring the noise always helps a fixed relay, and failure concentrates near the white limit.

**Proposition 6.4 (optimal stationary error).** With measurement differencing \[27, 28, 45\], z = ẏ + y/τ, the optimal stationary error is the positive root of

```latex
(1 - \lambda\tau)^2 P^2 + \Big(4\Sigma\tau + \frac{2\lambda}{\Pi}\Big)P - \frac{2\Sigma}{\Pi} = 0,
\qquad
P(\tau) = \frac{4\Sigma}{\Pi\,(b + \sqrt{D})}
```

with b = 4Στ + 2λ/Π and D = b² + 8Σ(1 − λτ)²/Π. The rationalised form has no singularity at λτ = 1.

*Proof.* z = hs + v with h = 1/τ − λ and v = w\_s + w\_η, where the measurement intensity is R\_v = 2Σ + 1/(Πτ²) and the cross-intensity is 2Σ. The steady-state Riccati equation with correlated noise is 0 = −2λP + 2Σ − (hP + 2Σ)²/R\_v; multiplying by −τ²R\_v gives the quadratic. Its constant term is negative and its leading coefficient non-negative, so it has exactly one positive root. ∎

**Corollary 6.5 (normalised optimal error).** With ν = 2ΣΠ/λ² and t = λτ,

```latex
\frac{P}{F} = \frac{2}{1 + \nu t + \sqrt{(1 + \nu t)^2 + \nu\,(1 - t)^2}}
```

*Proof.* Multiply Proposition 6.4 through by Π: Πb = 2λ(1 + νt) and Π√D = 2λ√((1 + νt)² + ν(1 − t)²). Then P/F = (λ/Σ)·4Σ/(Π(b + √D)) gives the formula. ∎

At t = 0 the formula reduces to the envelope q⋆(ν) of Proposition 3.5.

**Theorem 6.6 (optimal error decreases in τ).** P is strictly decreasing on (0, ∞), with P(0⁺) = σ⋆²(Π) and P(τ) \~ 1/(Πτ(1 + √(1 + λ²/(2ΣΠ)))) → 0.

*Proof.* b increases in τ, and dD/dτ = 32Σ²τ + 16Σλ²τ/Π > 0, so b + √D increases. At τ = 0, P = 2Σ/(λ + √(λ² + 2ΣΠ)) = σ⋆². For large τ, b \~ 4Στ and √D \~ 4Στ√(1 + λ²/(2ΣΠ)). ∎

Theorem 6.6 also follows from information ordering: at matched zero-frequency power the observation processes are ordered by causal garbling along τ (Proposition 7.7(b)), and Theorem 7.2 applies.

**Proposition 6.7 (optimal: classification).** The failure set is the lower ray (0, τ⋆\_R) for 0 < R² < σ⋆², and Empty for R² ≥ σ⋆², with

```latex
\tau^\star_R = \frac{2\lambda R^2 - 4\Sigma + \sqrt{\Delta}}{2\lambda^2 R^2},
\qquad
\Delta = 16\Sigma^2 - 16\lambda\Sigma R^2 + \frac{8\lambda^2(\Sigma - \lambda R^2)}{\Pi}
```

The optimal filter never produces All, a window, an upper ray or two rays along τ.

*Proof.* Theorem 2.2 with Theorem 6.6. Setting P = R² in Proposition 6.4 gives a quadratic in τ with leading coefficient λ²R⁴ > 0 and constant term R⁴ + 2λR²/Π − 2Σ/Π, which is negative iff R² < σ⋆². ∎

**Proposition 6.8 (best constant-gain relay).** Let V(τ) = inf over G ≥ 0 of σ²(G, τ). Then P ≤ V, V is strictly decreasing, V(0⁺) = σ⋆² and V(∞) = 0.

*Proof.* A constant-gain relay is a causal linear estimator, so P ≤ V. G = 0 is never the infimiser, since ∂σ²/∂G = −Σ/λ² < 0 there. Take τ₁ < τ₂. If the infimum at τ₁ is attained at G₁ > 0, then V(τ₂) ≤ σ²(G₁, τ₂) < V(τ₁). If it is approached as G → ∞, its value is 1/(2Πτ₁) > 1/(2Πτ₂) ≥ V(τ₂). As τ → ∞, σ²(G, τ) → Σ/(λ + G), whose infimum is 0. ∎

**Proposition 6.9 (strict gap).** P(τ) < V(τ) for every τ > 0: no constant-gain relay is optimal under coloured noise.

*Proof.*

1. If a relay with gain G attained P, its estimate would be the conditional mean (by uniqueness of the L² projection), so its error e = s − ŝ would be orthogonal to every past observation.
2. For the relay, ė = −ae − Gη + w\_s, and for u ≥ 0 (w\_s after t − u is independent of y(t − u)),

   ```latex
   c(u) = \mathbb{E}[e(t)\,y(t-u)] = e^{-au}c(0) - \frac{G}{2\Pi\tau}\,\frac{e^{-u/\tau} - e^{-au}}{a - 1/\tau} \quad (a \ne 1/\tau)
   ```

   with −(G/(2Πτ))·u·e^(−au) in place of the last term when a = 1/τ. For G > 0 the e^(−u/τ) term (or the ue^(−au) term) is non-zero, so c ≢ 0. For G = 0, c(u) = Fe^(−λu) ≢ 0. So no relay with finite gain is optimal.
3. As G → ∞, σ² → Var η = 1/(2Πτ), the error of the estimator ŝ = y. That estimator is not optimal either, since E\[(s − y)y\] = −Var η ≠ 0.
4. σ²(G, τ) is continuous on the compactified range \[0, ∞\], so its minimum V(τ) is attained there and exceeds P(τ). ∎

In the worked example (λ = 1, Σ = 0.01, Π = 1): σ⋆² = 0.0099505; P(1) = 0.0098039 (the case λτ = 1) against V(1) = 0.0099010; P(10) = 0.0067813. The fixed relay with G = 0.5 gives 0.04 and 0.011875, and tends to H\_G = 0.0066667 as τ → ∞, while P → 0.

### 6.2 Correlation time at matched variance

The same physical change, narrowing the noise bandwidth, can be normalised differently. Fix the noise variance v instead of its zero-frequency power:

```latex
C_\eta(u) = v\,e^{-|u|/\tau},
\qquad
S_\eta(\omega) = \frac{2v\tau}{1 + \tau^2\omega^2}
```

**Proposition 6.10 (optimal filter at matched variance).** The optimal stationary error is the positive root of

```latex
A(\tau)P^2 + BP - C = 0,
\qquad
A = \frac{(1 - \lambda\tau)^2}{\tau},\quad B = 4(\Sigma + \lambda v),\quad C = 4\Sigma v
```

that is P = 2C/(B + √(B² + 4AC)). Consequently:

1. P is strictly decreasing in A, so it is unimodal in τ, with its maximum at τ = 1/λ and P\_max = Σv/(Σ + λv).
2. A(τ) = A(1/(λ²τ)), so P is symmetric in log τ about τ = 1/λ.
3. P \~ 2√(Σvτ) as τ → 0, and P \~ (2/λ)√(Σv/τ) as τ → ∞.
4. For 0 < R² < P\_max the failure set is the window (τ₋, τ₊), and for R² ≥ P\_max it is Empty, where

```latex
\tau_\pm = \frac{(2\lambda + A_R) \pm \sqrt{A_R\,(4\lambda + A_R)}}{2\lambda^2},
\qquad
A_R = \frac{C - BR^2}{R^4},
\qquad
\tau_-\tau_+ = \frac{1}{\lambda^2}
```

*Proof.* The correlated-noise Riccati equation of Proposition 6.4 holds with w\_η of intensity 2v/τ, so R\_v = 2Σ + 2v/τ; multiplying by −τR\_v gives the quadratic. Its constant term is negative and B > 0, so there is one positive root, and it decreases in A ≥ 0. Items 1–3 follow from the shape of A. For item 4, set P = R², solve for A, then solve λ²τ² − (2λ + A\_R)τ + 1 = 0. ∎

Filtering under coloured measurement noise is standard, by state augmentation or measurement differencing \[27, 28, 45, 46\], and the effect of mis-specified time-correlated errors on Kalman smoothing has been studied \[47\]. The searches of §1.6 found no comparison of the two normalisations of the same noise.

**Counterexample 6.11 (the optimal filter can window).** The statement "the optimal filter never produces a window" holds along precision (Theorem 3.4) and along matched-zero-frequency τ (Theorem 6.6), but fails along matched-variance τ: by Proposition 6.10 the optimal failure set is a window for every 0 < R² < P\_max.

**Proposition 6.12 (relay at matched variance).** For fixed G > 0,

```latex
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2 v\,\tau}{1 + a\tau}\right)
```

which is strictly increasing, from H\_G to (Σ + G²v/a)/a, and at least P throughout. The classes are All (R² ≤ H\_G), upper ray (H\_G < R² below the top value) and Empty (R² at or above the top value).

The same change of bandwidth gives a monotone optimal filter at matched zero-frequency power and a windowed one at matched variance. The normalisation is a modelling choice, and it changes the topology. Chapter 7 explains the difference: at matched zero-frequency power the observations are ordered by causal garbling along τ (Proposition 7.7), and at matched variance they cannot be, since an ordering would rule out the optimal window (Corollary 7.3).

*Figure B.7 (Appendix B): stationary error against τ for the relay and the optimal filter, at matched zero-frequency power (left) and matched variance (right).*

**Verification.**

- Lemma 6.1 was checked by an augmented-state Lyapunov route (Task 9, T9.1(a), (b)).
- Propositions 6.2 and 6.3: T9.1, T9.4 (80,000 classifications); Task 13 audit row 13.
- Proposition 6.4 was checked against the closed-form Wiener filter to 2 × 10⁻¹⁷ (T9.2). The pre-registered route through a regularised algebraic Riccati equation failed its tolerance, because the regularisation converges as √ε with a large prefactor; an extended-precision Riccati solution agrees (Appendix D, Task 9).
- Corollary 6.5 was verified symbolically in Task 14 (Part G).
- Theorem 6.6 and Propositions 6.7 and 6.8: T9.1, T9.4, T9.5; Task 13 audit row 14. T9.5's monotonicity check failed at double precision: 285 and 13 flags, none real at higher precision (Appendix D, Task 9).
- Proposition 6.9 was proved in Task 13 (A7): a symbolic covariance identity and 10,000 parameter sets at 60 digits, with no failure. Task 9 had recorded strictness only as a numerical result.
- Proposition 6.10: three routes agree to 1.0 × 10⁻¹⁴, and the shape is exact to 10⁻⁵⁰ (T10.6); Task 13 audit row 16. The pre-registered check of its shape near τ = 0 failed as specified (attribution: criterion; Appendix D, Task 10).
- Counterexample 6.11 and Proposition 6.12: T10.6; Task 13 audit row 15.

### 6.3 Sampling: models and excess sets

Sampling replaces the continuous observation by samples every Δt. In the point-sampled model with matched floor (M-P), the state and observations are

```latex
x_{k+1} = a\,x_k + w_k,\quad a = e^{-\lambda\Delta t},\quad \operatorname{Var} w = q = F(1 - a^2);
\qquad
z_k = x_k + v_k,\quad \operatorname{Var} v = r = \frac{1}{\Pi\Delta t}
```

The per-sample noise variance r = 1/(ΠΔt) is the variance of white noise of intensity 1/Π averaged over the interval, so every sample becomes more precise as the interval grows. Write s = 1 − a² and φ = FΠΔt.

The error is periodic in time, so one number per Δt needs a choice of metric. Three are used:

- the posterior error at sample times, P⁺ (**post**);
- the prior error just before a sample, P⁻ = a²P⁺ + q (**prior**);
- the time average over the period, P̄ = F − (F − P⁺)·s/(2λΔt) (**avg**).

Post and prior are the minimum and the supremum of the periodic error curve, and avg is its mean. The time average is the primary metric of this thesis, because it is the error a user experiences across the period; post and prior are reported alongside it.

Four filters are compared:

- the optimal filter (steady-state Kalman);
- **D1**, the sampled relay, with L = 1 − e^(−GΔt);
- **D2**, the discrete Bayesian weight, with L = cΠΔt/(ΠΔt + Π₀) and 0 < c < 2;
- **D3**, the discrete Kalman filter over-trusting precision by a factor ρ.

For a fixed gain L,

```latex
P^+ = \frac{(1 - L)^2 q + L^2 r}{1 - (1 - L)^2 a^2}
```

The integrate-and-dump model (M-I), in which each sample is the average of the observation over its interval, is treated in chapter 7, where it is ordered by causal garbling (Corollary 7.14, Theorem 7.15).

**Proposition 6.13 (discrete excess condition).** For a fixed gain 0 ≤ L < 2, the prior error is

```latex
P^- = \frac{a^2 L^2 r + q}{1 - a^2(1 - L)^2},
\qquad
P^+ - F = \frac{P^- - F}{a^2}
```

and P⁻ > F iff P⁺ > F iff L/(2 − L) > φ. The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < φ/2 for every Δt > 0.

*Proof.* With q = F(1 − a²), the numerator of P⁻ − F is a²L²r + F(1 − a²) − F + Fa²(1 − L)² = a²L(Lr − F(2 − L)), and the denominator is positive for 0 ≤ L < 2; so P⁻ > F iff Lr > F(2 − L), that is L/(2 − L) > F/r = φ. P⁻ = a²P⁺ + q gives P⁺ − F = (P⁻ − F)/a². For the optimal filter, L⋆ = P⁻/(P⁻ + r) with P⁻ < F, so L⋆/(2 − L⋆) = P⁻/(P⁻ + 2r). This is below F/(2r) iff P⁻(2r − F) < 2rF, which holds because P⁻ < F. ∎

This is the discrete form of the excess identity: L/(2 − L) is the discrete-time variance factor α/(2 − α) of an exponentially weighted average \[26\], and φ = FΠΔt plays the role of FΠ. As in continuous time, the optimal gain sits at most halfway to the excess threshold.

**Lemma 6.14 (shared excess set).** For any filter on M-P, P⁻ − F = a²(P⁺ − F) and P̄ − F = (P⁺ − F)·s/(2λΔt). Hence all three metrics exceed F on the same set, {L/(2 − L) > φ}.

*Proof.* The first identity is Proposition 6.13; the second is the definition of P̄. ∎

**Proposition 6.15 (D1: the tanh lemma).** L/(2 − L) = tanh(GΔt/2), so the excess set is {G·h(GΔt) > FΠ} with h(x) = tanh(x/2)/x strictly decreasing from 1/2. The excess set is the lower ray (0, Δt\_E) iff G > 2FΠ, the continuous-time condition, and is empty otherwise; Δt\_E solves tanh(GΔt/2) = FΠΔt.

*Proof.* h′(x) = (x − sinh x)/(2x² cosh²(x/2)) < 0 since sinh x > x, and h → 1/2 as x → 0. ∎

Sampling never creates excess that continuous time lacks, and longer intervals remove it.

**Proposition 6.16 (D2).** The excess set is the lower ray Δt < Δt\_E = (c − 2FΠ₀)/((2 − c)FΠ) iff κ = c/(FΠ₀) > 2, and empty otherwise.

The model requires 0 < c < 2, so that 0 < L < 2. For c > 2 the gain tends to c, L/(2 − L) > φ no longer characterises excess, and the excess set can be all of (0, ∞): with λ = 1, Σ = 0.01, Π = Π₀ = 1 and c = 3, P⁺ > F at every Δt and P⁺ → 4F.

**Proposition 6.17 (D3).** The excess set is {φ < 1 and s(1 − φ)(ρ(1 + φ) − 2) > 4φ}. Its small-Δt behaviour gives the onset: with u = 2ΣΠ/λ², there is excess near Δt = 0 iff ρ > 2 + u. This is the continuous-time excess condition for G = −λ + √(λ² + 2ρΣΠ), since √(1 + ρu) > 1 + u iff ρ > 2 + u.

*Proof.* D3's gain is L = m/(1 + m), with m the positive root of Q(m) = m² + s(1 − ρφ)m − sρφ. By Lemma 6.14, excess holds iff L/(2 − L) > φ, iff m(1 − φ) > 2φ. If φ ≥ 1 this fails. If φ < 1 it says m > T = 2φ/(1 − φ), that is Q(T) < 0 (Q has one positive root and is increasing there), and Q(T)(1 − φ)²/φ = 4φ − s(1 − φ)(ρ(1 + φ) − 2). Near Δt = 0, with x = λΔt and φ = ux/2, the difference s(1 − φ)(ρ(1 + φ) − 2) − 4φ is 2x(ρ − 2 − u) + O(x²). At ρ = 2 + u the first two orders cancel and it equals −u(3u² + 6u + 4)x³/6 + O(x⁴) < 0, so there is no excess near 0 in that case either. ∎

The onset ρ > 2 is the condition for excess at some precision (Proposition 6.25); at fixed precision it is not enough. In 178 of 1,000 census sets, 2 < ρ ≤ 2 + u and there is no excess near Δt = 0.

**Proposition 6.18 (endpoint limits).** With G\_ρ = −λ + √(λ² + 2ρΣΠ):

| Filter | Δt → 0 (all metrics) | Δt → ∞ |
| --- | --- | --- |
| Optimal | σ⋆² | post → 0; prior and avg → F from below |
| D1 | σ²(G, Π) | post → 0; prior → F from below (gap ∝ e^(−2λΔt)); avg → F from below, like −F/(2λΔt) |
| D2 | σ²(cΠ/Π₀, Π) | post → (1 − c)²F, with Δt·(P⁺ − (1 − c)²F) → c\[c + 2(1 − c)FΠ₀\]/Π; prior and avg → F from below |
| D3 | σ²(G\_ρ, Π) | post → 0; prior and avg → F from below |

### 6.4 The optimal filter along the sampling interval

**Theorem 6.19 (optimal M-P error along Δt).**

(a) P⁺ is strictly decreasing, from σ⋆² to 0.

(b) P⁻ is strictly increasing, from σ⋆² to F.

(c) P̄ is strictly increasing, from σ⋆² to F.

*Proof.* Write x = λΔt, s = 1 − e^(−2x), s′ = 2e^(−2x) and r = λ/(Πx).

(a) P⁺ = F/(1 + μ), where μ > 0 solves μ² + (1 − φ)μ − φ/s = 0. The root μ is strictly increasing in φ and in w := φ/s, and both increase in x (since e^y > 1 + y).

(b) M = P⁻ is the positive root of f(M) = M² + s(r − F)M − sFr, and f′(M) = 2M + s(r − F) > 0 there, because the product of the roots, −sFr, is negative. Implicit differentiation with r′ = −r/x gives sign(dM/dx) = sign B, with B = FMs′ − (F − M)r(s/x − s′). On f = 0, sr(F − M) = M(M − sF), so B = M\[Fs′ − (M − sF)(s/x − s′)/s\]. Now f(F) = F²(1 − s) > 0 and f(sF) = −sFr(1 − s) < 0 give sF < M < F, hence 0 < M − sF < F(1 − s); and s/x > s′, since s − xs′ = e^(−2x)(e^(2x) − 1 − 2x) > 0. So B > (MF/s)\[ss′ − (1 − s)(s/x − s′)\] = (MF/s)(e^(−2x)/x)(2x − 1 + e^(−2x)) > 0. The last factor is positive because y ↦ e^(−y) − 1 + y vanishes at 0 and has derivative 1 − e^(−y) > 0.

(c) By Lemma 6.14 and (a), P̄ = F − (F/2)Q with Q = μs/((1 + μ)x), so it suffices that Q decreases. With φ = wx (now w = FΠ/λ) and E = 1/x − s′/s > 0, implicit differentiation of the μ equation and φ/s = μ(μ + 1 − φ) give (2μ + 1 − φ)μ′ = φμ/x + μ(μ + 1 − φ)E, where 2μ + 1 − φ > 0 and μ + 1 − φ > 0. Then d ln Q/dx = μ′/(μ(1 + μ)) − E, and (1 + μ)(2μ + 1 − φ)E − \[w + (μ + 1 − φ)E\] = Eμ(2 + 2μ − φ) − w, with μ(2 + 2μ − φ) = φ(2/s + μ). Hence d ln Q/dx < 0 iff 1 < xE(2/s + μ) = (1 − xs′/s)(2/s + μ). This holds since μ > 0 and

```latex
\Big(1 - \frac{x s'}{s}\Big)\frac{2}{s} = 1 + \frac{2e^{-2x}\,(\sinh 2x - 2x)}{s^2} \ge 1
```

The limits are Proposition 6.18. ∎

So the optimal filter's classes along Δt depend on the metric. Post: lower ray (R² < σ⋆²) or Empty (R² ≥ σ⋆²). Prior and avg: All (R² ≤ σ⋆², since σ⋆² is approached from above), upper ray (σ⋆² < R² < F) and Empty (R² ≥ F).

Each sample carries the signal with noise variance 1/(ΠΔt), so longer intervals make every sample more precise; but the samples are sparser, so the error grows more between them. Post sees only the first effect; prior and avg see both, and the second wins. The ingredients are standard sampled-data filtering \[40\], and a trade-off in the sampling rate, with an optimum once delays are priced in, is known \[48\]. Theorem 6.19 adds the direction of each metric under this matched-precision scaling. The statement depends on the scaling r = 1/(ΠΔt); a fixed per-sample variance is a different question and is not treated here. Because post falls while prior and avg rise, the M-P family is not ordered by causal garbling in either direction (Proposition 7.16).

*Figure B.8 (Appendix B): optimal error against Δt, with post falling toward 0 and prior and avg rising to F.*

### 6.5 Sampled relays

**Proposition 6.20 (two rays from an over-weighted sampled relay).** Let D1 have G > 2FΠ, and assume C2 for these curves (finitely many turning points; Conjecture 6.22 would give it). Then prior and avg start at σ²(G, Π) > F and end at F, approached from below, so each has an interior minimum below F. For R² between the lowest minimum and F, the failure set contains a lower and an upper ray: two rays, or (1, 1, k) if there are several minima.

*Proof.* Continuity and Proposition 6.18. ∎

The dips differ greatly in depth. For avg, P̄ − F \~ −F/(2λΔt), a modest dip. For prior, the gap is multiplied by e^(−2λΔt), and Task 12 measured relative dips from 10⁻¹⁷ down to 10^(−32,880,317). The prior's two rays exist mathematically but have no practical weight; the avg's two rays are real but narrow.

In the worked example (D1, G = 0.5, λ = 1, Σ = 0.01, Π = 1), post rises from 0.09 to a single maximum 0.20457 at Δt = 2.4645 and falls to 0, a window for 0.09 < R² < 0.20457. Avg crosses F at Δt\_E = 100 (to 20 digits), dips to 0.0099875 at Δt = 200 (a dip of 0.125%) and returns to F from below.

*Figure B.9 (Appendix B): the sampled relay D1 along Δt, error at sample times (left) and time average (right).*

**Numerical result 6.21 (census of sampled relays).** On 2,000 parameter sets per family, every class agreed between the two classification routes:

| Family | Metric | Turning-point shapes | Classes found |
| --- | --- | --- | --- |
| D1 | post | none, max | Empty, lower ray, window |
| D1 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, (0, 1, 1) |
| D1 | avg | none, min, max–min | All, Empty, lower ray, upper ray, two rays, (0, 1, 1) |
| D2 | post | none, max, min, min–max | All, Empty, lower ray, upper ray, two rays, window, (1, 0, 1) |
| D2 | prior, avg | none, min | All, Empty, lower ray, upper ray, two rays |
| D3 | post | none, max | Empty, lower ray, window |
| D3 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, (0, 1, 1) |
| D3 | avg | none, min | All, Empty, lower ray, upper ray, two rays |

The D3 excess set at R² = F (post) was a lower ray or Empty in 1,000 of 1,000 sets. Two rays in D1 avg also occur with G ≤ 2FΠ (for example G = 0.019, λ = 1, Σ = 0.01, Π = 1: a maximum, then a minimum below the starting value), so G > 2FΠ is sufficient for two rays (Proposition 6.20) but not necessary.

Natural gains along Δt give two mixed classes: upper ray + window (0, 1, 1), from a max–min shape (a hump before the slow return to F), and lower ray + window (1, 0, 1), from the min–max shape of D2 post.

**Conjecture 6.22 (at most two turning points).** Along Δt, D1–D3 have at most two turning points in every metric.

No case with more than two was found in the census or in the Task 13 audit, and no proof is known (chapter 9).

**Verification.**

- Lemma 6.14: symbolic (Task 12, A1).
- Proposition 6.15: symbolic, 1,000 of 1,000 sets, Δt\_E to 10⁻³⁰ (A2).
- Proposition 6.16: symbolic, 1,000 of 1,000 sets (A3).
- Proposition 6.17: symbolic, 1,000 of 1,000 sets, no disagreement in 201,514 membership tests (A4); the equality case ρ = 2 + u was checked by series in Task 13.
- Proposition 6.13 was proved in the starting study and checked there (Tasks 4 and 7); the proof above is the direct computation.
- Proposition 6.18: symbolic (A5). The pre-registered route for the D2 coefficient, SymPy's limit, failed; the series route confirms it (attribution: code; Appendix D, Task 12).
- Theorem 6.19:
  - (a) symbolic in Task 12 (A6);
  - (b) and (c) in Task 13 (A1, A2): every step symbolic, and 10,000 parameter sets at 100 digits with no failure in any link;
  - two identities passed only by a post-hoc rewrite route, recorded as failures of the pre-registered route (Appendix D, Task 13);
  - (c) had been a numerical result in Task 12 (400,000 points).
- Proposition 6.20 rests on Proposition 6.18. Task 12's pre-registered check of a minimum below F failed, because its zero tolerance was too coarse for the prior's dip (attribution: criterion; Appendix D, Task 12).
- Numerical result 6.21: Task 12 (A8, Part C), 6,000 sets × 3 metrics; Task 13 audit rows 24–32. A qualitative regression against quick-check numbers in the Task 12 prompt failed; the error was in those predicted numbers (attribution: prediction; Appendix D, Task 12).

### 6.6 Process noise: a moving floor

Fix λ and Π and sweep Σ. Now the floor F = Σ/λ moves with the parameter, so the tolerance convention matters. Two are used: **absolute**, with a fixed R², and **relative**, where failure means σ² > rF for a fixed r. In the coordinates of chapter 3, u = 2ΣΠ/λ² is the coordinate ν of §3.2, and g = G/λ = νq/2.

**Lemma 6.23 (Σ scaling).** σ²/F = (1 + g²/u)/(1 + g). For a gain that depends on (Σ, Π) only through u, the relative-tolerance Σ sweep and the precision sweep classify identically in u.

*Proof.* Divide σ² by F = Σ/λ, as in Theorem 3.2. Under a relative tolerance the threshold r is fixed, so the failure set is {u : 𝒱 > r} along the same path in either sweep. ∎

**Proposition 6.24 (Σ-independent gain).** Absolute: σ² is affine and increasing in Σ, from G²/(2Π(λ + G)) (approached from above) to ∞; the classes are All and upper ray. Relative: σ²/F decreases from ∞ to 1/(1 + g); the classes are All and lower ray. The excess set (r = 1) is Σ < λG/(2Π).

**Proposition 6.25 (Σ-tracking Kalman gain, over-trust ρ).** Let G = −λ + √(λ² + 2ρΣΠ) and w = √(1 + ρu). Absolute: σ² is strictly increasing from 0, class upper ray. Relative:

```latex
\frac{\sigma^2}{F} = \frac{(1 + \rho)\,w + (1 - \rho)}{w\,(w + 1)}
```

which starts at 1 and tends to 0, with a single maximum at w\_M = \[(ρ − 1) + √(2ρ(ρ − 1))\]/(1 + ρ) iff ρ > 2, and is strictly decreasing otherwise. The classes are:

- ρ > 2: lower ray (r ≤ 1, since the start at 1 is approached from above), window (1 < r below the peak), Empty (at or above the peak);
- ρ ≤ 2: lower ray (r < 1), Empty (r ≥ 1).

*Proof.* Absolute: σ²Π/λ = \[(w² − 1)/ρ + (w − 1)²\]/(2w), whose w-derivative is \[(w² − 1)(1 + 1/ρ) + 2/ρ\]/(2w²) > 0. Relative: the numerator of the derivative, −(1 + ρ)w² + 2(ρ − 1)w + (ρ − 1), is a downward parabola with value 2(ρ − 2) at w = 1 and vertex at (ρ − 1)/(1 + ρ) < 1. The classes follow from Theorem 2.2. ∎

**Proposition 6.26 (Σ-tracking Kalman gain, misspecified λ′).** Let G = −λ′ + √(λ′² + 2ΣΠ). Absolute: σ² is strictly increasing from 0, class upper ray. Relative: σ²/F starts at 1 and tends to 0, with a single maximum iff λ′ < λ/2, and is strictly decreasing otherwise. The classes are lower ray (r ≤ 1), window (1 < r below the peak) and Empty when λ′ < λ/2, and lower ray (r < 1) and Empty (r ≥ 1) otherwise.

*Proof.* With Σ = (G² + 2λ′G)/(2Π): absolute σ² = G(G + λ′)/(Π(λ + G)), with derivative numerator G² + 2λG + λλ′ > 0. Relative σ²/F = 2λ(G + λ′)/((G + 2λ′)(G + λ)), with derivative numerator 2λ\[−G² − 2λ′G + λ′(λ − 2λ′)\]. That bracket is a downward parabola with vertex at G = −λ′ < 0 and value λ′(λ − 2λ′) at G = 0. ∎

**Proposition 6.27 (optimal filter along Σ).** Absolute: σ⋆² is increasing from 0, class upper ray. Relative: σ⋆²/F = 2/(1 + √(1 + u)) is decreasing, classes lower ray and Empty.

**Proposition 6.28 (signal sweeps).** σ⋆² is increasing in Σ, decreasing in λ at fixed Σ, and increasing in λ at fixed F, since σ⋆² = 2F/(1 + √(1 + 2FΠ/λ)). So the optimal filter never windows along these sweeps either, for an elementary reason rather than an information-ordering one.

On a moving floor the tolerance convention decides the topology. With absolute tolerances every family is monotone. With relative tolerances, windows return under the same factor-of-two over-confidence condition as in chapters 3 and 5: ρ > 2, or λ′ < λ/2 (that is F′/F > 2). Under either convention, the optimal filter never windows along Σ.

*Figure B.10 (Appendix B): the process-noise sweep for the Σ-independent gain, the over-trusting Σ-tracking gain (ρ = 10) and the optimal filter, absolute error (left) and relative error (right).*

**Verification.** Lemma 6.23 and Propositions 6.24–6.27 were checked symbolically in Task 12 (B1–B5). Propositions 6.25 and 6.26 were also checked on 2,000 parameter sets each, with the maximum's position for 6.25 to 6 × 10⁻³¹. Propositions 6.24–6.27 were covered by Task 13 audit rows 35–42. Proposition 6.28 is a set of one-line derivatives (T11.1).

### 6.7 Summary

| Sweep | Optimal filter | Relay or natural gains | Result |
| --- | --- | --- | --- |
| τ, matched zero-frequency power | decreasing: lower ray, Empty | fixed relay decreasing: All, lower ray, Empty; no relay is optimal | Lemma 6.1–Prop. 6.9 |
| τ, matched variance | unimodal: window, Empty | fixed relay increasing: All, upper ray, Empty | Prop. 6.10–6.12 |
| Δt, post | decreasing: lower ray, Empty | D1, D3: window; D2: also (1, 0, 1) | Theorem 6.19, Num. result 6.21 |
| Δt, prior and avg | increasing: All, upper ray, Empty | two rays; (0, 1, 1) | Theorem 6.19, Prop. 6.20, Num. result 6.21 |
| Σ, absolute tolerance | increasing: upper ray | every family monotone | Prop. 6.24–6.27 |
| Σ, relative tolerance | decreasing: lower ray, Empty | window iff ρ > 2 or λ′ < λ/2 | Lemma 6.23, Prop. 6.25–6.26 |

The optimal filter is monotone along every sweep in this chapter except matched-variance τ, where it windows. Along Δt each metric is monotone, but post moves opposite to prior and avg. Chapter 7 connects both facts to information ordering: an ordering by causal garbling forbids optimal windows (Corollary 7.3) and makes every metric move the same way (Proposition 7.16), so neither of these families is ordered.

## 7. Optimality and Information

Chapters 3–6 found the optimal filter's error monotone along most sweeps, and two exceptions: along matched-variance τ it windows (Counterexample 6.11), and along the sampling interval its metrics move in opposite directions (Theorem 6.19). The normal form of chapter 3 cannot explain either; both lie outside its scope. This chapter supplies the second pillar of the thesis. When one observation process can be built from another causally, by adding independent randomness as the data arrive, the optimal filter on the richer process can never do worse. Along a sweep ordered this way the optimal filter cannot window. The chapter states that ordering (§7.1), gives an exact spectral test for it (§7.2), and then tests its reach: it is exactly sharp in a natural family of coloured noises (§7.3), it must be causal (§7.4), and it explains the sampling results of chapter 6 (§7.5).

### 7.1 Causal garbling and monotonicity

**Setting: observation sweeps.** The signal s is the same stationary Ornstein–Uhlenbeck process for every θ; only the observation process Y\_θ, jointly stationary with s, changes. The optimal filtering error is

```latex
P(\theta) = \mathbb{E}\Big[\big(s(t) - \mathbb{E}[\,s(t) \mid Y_\theta(u),\ u \le t\,]\big)^2\Big]
```

**Definition 7.1 (causal garbling).** Write θ₁ ⪯\_c θ₂ ("θ₂ is causally at least as informative as θ₁") if there are a random element U, independent of (s, Y\_θ₂), and a process Y′ such that, for every t, Y′(u ≤ t) is measurable with respect to 𝒢\_t = σ(Y\_θ₂(u ≤ t)) ∨ σ(U), and (s, Y′) has the same joint law as (s, Y\_θ₁).

In words: the worse observations can be manufactured from the better ones as they arrive, using only the past and present of the better process plus independent randomness.

**Theorem 7.2 (monotonicity under causal garbling).** If θ₁ ⪯\_c θ₂, then P(θ₂) ≤ P(θ₁).

*Proof.* Equality of joint laws gives P(θ₁) = E\[(s(t) − E\[s(t) | Y′(≤ t)\])²\]. Since σ(Y′(≤ t)) ⊆ 𝒢\_t, conditioning on the larger σ-field cannot increase the mean-square error. Because U is independent of (s, Y\_θ₂), E\[s(t) | 𝒢\_t\] = E\[s(t) | Y\_θ₂(≤ t)\]. ∎

The argument is pointwise in t, so it holds for cyclostationary observations too. It also holds with any square-integrable target measurable with respect to s in place of s(t), which Theorem 7.6 uses.

Theorem 7.2 is the filtering instance of a known principle. Monotonicity of optimal performance under garbling goes back to Blackwell's comparison of experiments \[18, 19\] and Le Cam's theory \[49, 50\]. It extends to sequential experiments \[20\] and to observation channels and information structures in stochastic control and teams \[21–23\]. What is specific here is the causal form of the order on observation processes, and its consequence for the topology of filtering failure sets.

**Corollary 7.3 (no optimal windows along causal orderings).** Suppose θ₁ < θ₂ implies θ₁ ⪯\_c θ₂ on the whole domain. Then P is non-increasing, so every optimal failure set is an initial segment of the domain. If moreover P is continuous (and satisfies C2′), the optimal failure set is Empty, All or a lower ray at every R². For the reverse ordering it is Empty, All or an upper ray. Windows, two rays and mixed classes are impossible.

*Proof.* A superlevel set of a non-increasing function is an initial segment. For continuous P it is open, hence Empty, the whole domain or (θ₋, x); plateaus are allowed by Theorem 2.4. ∎

Strict monotonicity is not needed.

**Corollary 7.4 (diagnostic).** Along a causally ordered sweep, a failure set with a window, two rays or a mixed class certifies that the filter is not optimal. With Theorem 5.1, the precision-sweep picture is complete: the optimal filter sits on the envelope σ⋆² (classes lower ray and Empty), and every curve strictly above it belongs to some miscalibrated gain.

*Proof.* Corollary 7.3, and Proposition 7.7(a) below for the precision sweep. ∎

So the bounded window of the starting study (§1.2) and the Hill mixed class (Proposition 5.13) are signatures of the filter, not of the environment.

### 7.2 A spectral test

For additive noise the ordering can be read off the spectra.

**Proposition 7.5 (spectral dominance).** Let y\_θ = s + η\_θ, with η\_θ stationary Gaussian, independent of s, with spectral density S\_θ (white components written as constant densities).

1. If S\_θ₁ ≥ S\_θ₂ almost everywhere, then θ₁ ⪯\_c θ₂.
2. Suppose S\_s > 0. If Y′ = h ∗ y\_θ₂ + n, with h causal and linear time-invariant and n independent, realises θ₁, then h = δ and S\_n = S\_θ₁ − S\_θ₂ ≥ 0.

*Proof.* (1) Let ξ be stationary Gaussian with density S\_θ₁ − S\_θ₂, independent of everything, and set Y′ = y\_θ₂ + ξ. (2) The cross-spectrum of s with Y′ is H·S\_s, which must equal S\_s, so H ≡ 1; matching the spectra of Y′ then gives S\_n. ∎

The next theorem shows that for additive Gaussian noise the spectral test is exact: non-linear causal garblings, and even non-causal garblings of whole paths, add nothing.

**Theorem 7.6 (the orderings coincide for Gaussian noise).** In the setting of Proposition 7.5, with S\_s > 0 almost everywhere, the following are equivalent:

- (i) θ₁ ⪯\_c θ₂ by some causal garbling, possibly non-linear;
- (ii) S\_θ₁ ≥ S\_θ₂ almost everywhere;
- (iii) θ₁ ⪯\_c θ₂ by adding independent stationary Gaussian noise;
- (iv) Y\_θ₁ is a garbling of Y\_θ₂ as whole paths, not necessarily causal (pathwise Blackwell ordering).

*Proof.* (ii) ⇒ (iii) is Proposition 7.5(1), and (iii) ⇒ (i) and (i) ⇒ (iv) are immediate. For (iv) ⇒ (ii) the two-sided inequality below holds directly, since a garbling of the whole path cannot lower any smoothing error. For (i) ⇒ (ii): by the proof of Theorem 7.2 with a square-integrable target Z measurable with respect to s in place of s(t),

```latex
\mathbb{E}\big[(Z - \mathbb{E}[Z \mid Y_{\theta_1}(\le t)])^2\big] \;\ge\; \mathbb{E}\big[(Z - \mathbb{E}[Z \mid Y_{\theta_2}(\le t)])^2\big]
\quad \text{for every } t
```

As t → ∞ the σ-fields σ(Y\_θ(≤ t)) increase to σ(Y\_θ(ℝ)), so by Lévy's upward theorem both sides converge to the two-sided (smoothing) errors, and the inequality survives. Take Z = ∫ g(u)s(u) du with g smooth and compactly supported. Because (s, Y\_θ) is jointly Gaussian, the two-sided conditional mean is linear and its error is ∫ |ĝ(ω)|² h\_θ(ω) dω/2π, with h\_θ = S\_s S\_θ/(S\_s + S\_θ). So ∫ |ĝ|²(h\_θ₁ − h\_θ₂) ≥ 0 for every such g. Taking g(u) = ψ(u/L) cos(ω₀u) with L → ∞ concentrates |ĝ|²/L at ±ω₀ as an approximate identity (the cross terms vanish for ω₀ ≠ 0, and the spectra are even), so h\_θ₁ ≥ h\_θ₂ at every Lebesgue point. Since x ↦ S\_s x/(S\_s + x) is strictly increasing where S\_s > 0 (its derivative is S\_s²/(S\_s + x)²), S\_θ₁ ≥ S\_θ₂ almost everywhere. ∎

Theorem 7.6 extends the characterisation of linear normal experiments \[24\] (see also \[50\]) from static observations to stationary Gaussian processes ordered by their spectra; a partial converse to Blackwell ordering for information structures is known in the game setting \[51\]. The searches of §1.6 found no version for processes.

**Proposition 7.7 (which studied sweeps are ordered).**

- (a) Precision: S\_Π = 1/Π decreases in Π, so the sweep is ordered, and the monotone optimal filter of the starting study is recovered.
- (b) Matched-zero-frequency τ: S\_τ(ω) = (1/Π)/(1 + τ²ω²) decreases in τ at every ω, so τ₁ ⪯\_c τ₂ for τ₂ > τ₁; information increases with τ. The garbling noise is the second-order process

```latex
S_\xi(\omega) = \frac{(\tau_2^2 - \tau_1^2)\,\omega^2}{\Pi\,(1 + \tau_1^2\omega^2)(1 + \tau_2^2\omega^2)} = |H_\xi(i\omega)|^2,
\qquad
H_\xi(s) = \sqrt{\frac{\tau_2^2 - \tau_1^2}{\Pi}}\;\frac{s}{(1 + \tau_1 s)(1 + \tau_2 s)}
```

Theorem 6.6's monotonicity follows; its strictness comes from the closed form.

- (c) Matched-variance τ: S\_τ = 2vτ/(1 + τ²ω²). Every pair crosses: the larger τ has more power at ω = 0, the smaller as ω → ∞. So by Theorem 7.6 no two values are ordered by any garbling, linear or not.

*Proof.* Proposition 7.5(1) for (a) and (b); the factorisation of S\_ξ is direct. Theorem 7.6 for (c). ∎

### 7.3 The power family: the condition is sharp

A one-parameter family of coloured noises contains both normalisations of chapter 6. Let η be Ornstein–Uhlenbeck with

```latex
S_{\beta,\tau}(\omega) = \frac{K\tau^\beta}{1 + \tau^2\omega^2},
\qquad
\operatorname{Var}\eta = v(\tau) = \tfrac{K}{2}\,\tau^{\beta - 1},
\qquad
\tau \in (0, \infty),\ K > 0,\ \beta \in \mathbb{R}
```

β = 0 is matched zero-frequency power (K = 1/Π), and β = 1 is matched variance (K = 2v). The optimal error is the root of Proposition 6.10 with v = v(τ). Coloured measurement noise is a standard setting for filter design \[27, 28, 45, 46\] and for analysing mis-specified time correlation \[47\]; the searches of §1.6 found no comparison across normalisations and no exponent threshold.

**Theorem 7.8 (sharpness in the power family).**

1. β ≤ 0: S\_β,τ decreases in τ at every ω. The sweep is causally ordered, with information increasing in τ, so P is non-increasing. Optimal classes: lower ray and Empty.
2. β ≥ 2: S\_β,τ increases in τ at every ω. The sweep is ordered with information decreasing in τ, so P is non-decreasing. Optimal classes: upper ray and Empty.
3. 0 < β < 2: every pair τ₁ ≠ τ₂ has crossing spectra, and P → 0 at both ends while P > 0. So for every 0 < R² < max P the optimal failure set is bounded away from both ends: a window, and exactly one by Theorem 7.9.

Hence, in this family: causally ordered ⇔ P monotone ⇔ no optimal-filter window ⇔ β ∉ (0, 2).

*Proof.* ∂ log S/∂τ = β/τ − 2τω²/(1 + τ²ω²), and the second term lies in \[0, 2/τ). So the derivative is ≤ 0 for every ω if β ≤ 0, > 0 for every ω if β ≥ 2, and changes sign with ω if 0 < β < 2. Parts 1 and 2 follow from Proposition 7.5 and Corollary 7.3. For part 3, P ≤ 2C/√(4AC) = √(C/A) = √(2ΣK)·τ^(β/2)/|1 − λτ|, which tends to 0 as τ → 0 iff β > 0, and as τ → ∞ iff β < 2. ∎

Where that bound does not vanish, the limits of P are: for β < 0 and τ → 0, P → F; for β = 0 and τ → 0, P → σ⋆²(1/K); for β = 2 and τ → ∞, P → σ⋆²(λ²/K), not F; and for β > 2 and τ → ∞, P → F, approached like τ^(2−β).

**Theorem 7.9 (unimodality for 0 < β < 2).** For 0 < β < 2, P has exactly one turning point, a maximum, so the optimal failure set has k = 1.

*Proof.* Let Φ(τ, P) = AP² + BP − C, so Φ\_P = 2AP + B > 0. With A′ = (λ²τ² − 1)/τ², A″ = 2/τ³, v′/v = (β − 1)/τ and v″/v′ = (β − 2)/τ:

```latex
\Phi_\tau = A'P^2 - 4v'(\Sigma - \lambda P),
\qquad
\Phi_{\tau\tau} = A''P^2 - 4v''(\Sigma - \lambda P)
```

At a critical point P′ = 0, so Φ\_τ = 0 and P″ = −Φ\_ττ/Φ\_P. For β ≠ 1, substituting Σ − λP = A′P²/(4v′),

```latex
\Phi_{\tau\tau} = P^2\Big(A'' - A'\,\frac{v''}{v'}\Big) = \frac{P^2\,\big(\beta + (2 - \beta)\lambda^2\tau^2\big)}{\tau^3} > 0
```

so P″ < 0. For β = 1, Φ\_τ = A′P² vanishes only at τ = 1/λ, where A″ > 0 gives the same sign. Every critical point is therefore a strict local maximum. Two strict maxima would enclose an interior minimum, a critical point that is not a strict maximum; so there is at most one critical point. There is at least one, because P > 0 and P → 0 at both ends (Theorem 7.8). ∎

**Proposition 7.10 (duality).** P\_β,K(τ) = P\_(2−β), Kλ^(2−2β)(1/(λ²τ)).

*Proof.* A is invariant under τ ↦ 1/(λ²τ), and (K′/2)x^(1−β) at x = 1/(λ²τ) equals (K/2)τ^(β−1) when K′ = Kλ^(2−2β). ∎

In this natural family of coloured noises the information-ordering condition is exactly sharp, and the two normalisations of chapter 6 sit on opposite sides of the boundary: β = 0 is ordered, β = 1 is in the windowed band. Duality maps the band onto itself about β = 1.

*Figure B.11 (Appendix B): the optimal error relative to its supremum over τ, across β and log₁₀(λτ), with the three regimes labelled.*

### 7.4 Delay: why the ordering must be causal

**Proposition 7.11 (latency).** Let y\_d(t) = s(t − d) + white noise of intensity 1/Π, with d ≥ 0. All values of d are pathwise Blackwell-equivalent, yet the optimal filtering error is

```latex
P(d) = F - e^{-2\lambda d}\big(F - \sigma_\star^2(\Pi)\big)
```

which is strictly increasing in d. Along the latency sweep d(θ) = θe^(−θ), which rises and then falls, the optimal filter has a window in θ for every R² ∈ (σ⋆², P(1/e)). The causal order (d₁ < d₂ ⇒ d₂ ⪯\_c d₁) reverses at θ = 1, where the window sits. The classes along θ are All (R² ≤ σ⋆²), window (σ⋆² < R² < P(1/e)) and Empty (R² ≥ P(1/e)).

*Proof.* By the Ornstein–Uhlenbeck property, s(t) = e^(−λd)s(t − d) plus an independent innovation of variance F(1 − e^(−2λd)), and s(t − d) is filtered with error σ⋆². So P(d(θ)) > σ⋆² for every θ > 0, with limit σ⋆² at both ends and a single maximum at θ = 1. ∎

In the worked example (λ = 1, Σ = 0.01, Π = 1), P(0) = 0.0099505 and P(1/e) = 0.0099763.

That delay degrades filtering is not new: the prediction covariance of a delayed estimate is classical \[29\], and out-of-sequence and delayed measurements are handled in tracking \[52, 53\]. What the proposition adds is a statement about orders on experiments.

**Counterexample 7.12 (pathwise ordering is not enough).** Proposition 7.11 is a sweep of pathwise Blackwell-equivalent experiments along which the optimal filtering error is not monotone. So "Blackwell ordering of whole paths implies monotone filtering error" is false, and Definition 7.1 must be causal.

The causal order also cannot be reversed into a characterisation of monotonicity.

**Proposition 7.13 (ordering is sufficient, not necessary).** Along matched-variance τ restricted to (1/λ, ∞), P is strictly decreasing (Proposition 6.10), yet no two values are causally ordered by any garbling (Proposition 7.7(c)). So a monotone optimal error does not require an information ordering.

*Figure B.12 (Appendix B): the optimal filtering error along the latency sweep d(θ) = θe^(−θ), with its window and the reversal at θ = 1.*

### 7.5 Sampling

Chapter 6 left two facts about the sampling interval unexplained: the post-update and the averaged errors of the point-sampled model move in opposite directions (Theorem 6.19), and its relays produce mixed classes. Integrate-and-dump sampling (M-I), in which each sample z\_k is the average of the observation over the k-th interval, behaves differently, and the ordering explains why.

**Corollary 7.14 (integrate-and-dump, nested grids).** If Δt₂ = mΔt₁ for an integer m and the grids are aligned, each coarse M-I sample is the average of the m fine samples completed by the time it is taken: a causal garbling. Hence the optimal error, pointwise in t and time-averaged, satisfies P(Δt₂) ≥ P(Δt₁) along every chain Δt₀, mΔt₀, m²Δt₀, …

*Proof.* Theorem 7.2, pointwise in t (the observations are cyclostationary), then averaged. ∎

On the continuum the ordering argument does not reach non-nested pairs, but the closed form does.

**Theorem 7.15 (integrate-and-dump on the continuum).** Both M-I optimal metrics, (a) the error at sample times and (b) the time average, are strictly increasing in Δt on the whole continuum, including non-nested pairs.

*Proof.* By scaling, P\_a = F·p(x, u) with x = λΔt and u = 2ΣΠ/λ². In reduced units (λ = Σ = 1, Π = u/2, E = e^(−x)) the integrate-and-dump model has process covariances q₁₁ = 1 − E², q₁₂ = 2\[(1 − E) − (1 − E²)/2\] and q₂₂ = 2\[x − 2(1 − E) + (1 − E²)/2\] for the state and its interval average. With h = (1 − E)/x, r\_e = q₂₂/x² + 1/(Πx) and g = q₁₂/x, the posterior p is the positive root of

```latex
a_2p^2 + a_1p + a_0 = 0,
\qquad
a_2 = h^2,\quad a_1 = r_e(1 - E^2) - q_{11}h^2 + 2Ehg,\quad a_0 = -(q_{11}r_e - g^2)
```

These coefficients satisfy a₀ = −a₁ identically, and a₂/a₁ = u(1 − E)/(2K) with K = u\[x(1 + E) − 2(1 − E)\] + x(1 + E). Hence

```latex
p = \frac{2}{1 + \sqrt{1 + 2u/k(x)}},
\qquad
k(x) = \frac{K}{1 - E} = (1 + u)\,x\coth(x/2) - 2u
```

Since d/dx\[x coth(x/2)\] = (sinh x − x)/(2 sinh²(x/2)) > 0, k increases strictly from k(0⁺) = 2 to ∞, so p increases strictly from 2/(1 + √(1 + u)) = σ⋆²/F to 1. So (a) is strictly increasing, from σ⋆² (approached from above) to F (approached from below). For (b), P\_b = P\_a·φ + F(1 − φ) with φ = (1 − E²)/(2x) and φ′ = −E²(e^(2x) − 1 − 2x)/(2x²) < 0, so dP\_b/dx = P\_a′φ + (P\_a − F)φ′ > 0. ∎

A second, independent route through the resultant of the cleared quadratic and its x-derivative confirms (a); it is recorded with the Task 13 checks (Appendix D).

**Proposition 7.16 (M-P is not a causal-garbling family).** Along Δt, the point-sampled model is ordered in neither direction.

*Proof.* By Theorem 7.2 an ordering would give a pointwise-in-t inequality between the two cyclostationary optimal error curves. Post, prior and avg are the minimum, the supremum and the time mean of each curve over its period, so all three would move the same way. But post falls while prior and avg rise (Theorem 6.19). ∎

So the two sampling models sit on opposite sides of the ordering: integrate-and-dump discards information as the interval grows and is ordered, while point sampling with matched precision trades per-sample precision against sample density and is not. Under integrate-and-dump every optimal metric worsens with Δt, so the optimal filter never windows there either, and an interior optimal sampling interval needs some other cost, such as the network delays of \[48\].

### 7.6 Summary: the answer to the optimality question

Along any causally ordered sweep, an optimal filter's failure set is Empty, All or a single ray at the less-informative end, and every other class certifies a miscalibrated filter (Corollaries 7.3–7.4). For additive Gaussian noise the ordering is decided by the spectra alone (Theorem 7.6). The condition is exactly sharp in the power-normalised family (Theorem 7.8), sufficient but not necessary in general (Proposition 7.13), and must be causal (Counterexample 7.12).

| Sweep | Ordered? | Optimal filter | Result |
| --- | --- | --- | --- |
| Precision Π | yes, information increasing | lower ray, Empty | Prop. 7.7(a), Theorem 3.4 |
| τ at matched zero-frequency power (β = 0) | yes, information increasing | lower ray, Empty | Prop. 7.7(b), Theorem 6.6 |
| Power family, β ≤ 0 or β ≥ 2 | yes | single ray, Empty | Theorem 7.8 |
| τ at matched variance (β = 1), power family 0 < β < 2 | no: spectra cross | exactly one window | Prop. 7.7(c), Theorems 7.8–7.9 |
| Latency d(θ) = θe^(−θ) | causal order reverses at θ = 1 | All, window, Empty | Prop. 7.11, Counterexample 7.12 |
| Δt, integrate-and-dump | yes on nested grids; monotone on the continuum | All, upper ray, Empty | Cor. 7.14, Theorem 7.15 |
| Δt, point sampling | no | post decreasing; prior and avg increasing | Prop. 7.16, Theorem 6.19 |
| Σ and λ (signal sweeps) | not an observation sweep | monotone, for an elementary reason | Prop. 6.28 |

**Verification.**

- Theorem 7.2: Task 11 (T11.1), with a Monte Carlo realisation of a garbling (T11.2). Corollaries 7.3 and 7.4: Task 11.
- Proposition 7.5: spectral checks on 25,000 pairs (T11.1, T11.3).
- Theorem 7.6: written proof, a symbolic check of the monotone map, and an independent referee pass (Task 13, A8).
- Proposition 7.7: T11.1, T11.3.
- Theorem 7.8: T11.3 over 37 values of β; Task 13 audit rows 17–19. The class check pre-registered in T11.3 failed because its limits and brackets at β ≥ 2 were wrong (P → σ⋆²(λ²/K) at β = 2, not F); they were corrected in the diagnosis (attribution: criterion; Appendix D, Task 11).
- Theorem 7.9: symbolic identities and 10,000 curves (Task 13, A4). Task 11 had recorded it as a numerical result (12,900 of 12,900 curves).
- Proposition 7.10: T11.1, T11.3, to 8 × 10⁻⁵¹.
- Proposition 7.11 and Counterexample 7.12: T11.4, with a Monte Carlo check (|z| ≤ 1.91); Task 13 audit row 20.
- Proposition 7.13: T11.5, 1,000 of 1,000 sets.
- Corollary 7.14: no violation in 9,000 pairs (T11.6).
- Theorem 7.15: closed form and limits (11 of 11), the exact resultant route, and 10,000 parameter sets at 100 digits with no violation (Task 13, A3); T11.6 and T12 (A9), 400,000 points each.
- Proposition 7.16: 1,000 of 1,000 pairs (Δt, 2Δt) (T12, A10).

## 8. Verification

*To be drafted.* Pre-registration protocol; every recorded failure (Tasks 1–13); blind searches (Numerical results 8.1–8.2).

## 9. Discussion and Limits

*To be drafted.* Relevance (thin bands, invisible dips), open conjectures, applied relevance and multivariate extensions as future work.

## Appendices

**Appendix A — Register of results.** Every numbered result with its thesis number, permanent repository key and the tasks that verified it (task identifiers as in Appendix D). Rendered from the repository register, freeze v1; 82 results.

| No. | Type | Result | Key | Verified by | Status |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Proposition | Topological realizability | topological-realizability | T8.5 | proved |
| 2.2 | Theorem | Critical-tolerance theorem | critical-tolerance | T8.1, T8.3, T9–T13 classifiers | proved |
| 2.3 | Definition | Critical-value signature and stratification | signature | — | definition |
| 2.4 | Theorem | Plateaus (C2′) | plateaus | T10.5 | proved |
| 2.5 | Corollary | Equal-height maxima | equal-height-maxima | T10.5 | proved |
| 2.6 | Corollary | Degenerate stationary points | degenerate-points | T10.5 | proved |
| 2.7 | Proposition | Pair birth | pair-birth | T10.5 (with diagnosis) | proved |
| 2.8 | Corollary | Reparameterisation (orientation swaps ℓ and u) | reparameterisation | T15 C11 | proved |
| 2.9 | Proposition | Structural stability at a fixed tolerance | structural-stability | T15 C12 | proved |
| 3.1 | Proposition | Stationary variance; constant-gain filter equivalence | stationary-variance | T1, T2 | proved |
| 3.2 | Theorem | Normal form σ²/F = V(ν,q) | normal-form | T14 G | proved |
| 3.3 | Corollary | Excess identity σ² > F ⇔ q > 2 | excess-identity | T1, T8.1 | proved |
| 3.4 | Theorem | Window theorem (sup q > 2); optimal monotone along Π | window-theorem | T1, T3, T4, T13 C2 | proved |
| 3.5 | Proposition | Optimal gain and envelope V⋆ = q⋆ | optimal-envelope | T1, T7 | proved |
| 3.6 | Lemma | Single minimum in the gain | single-minimum-gain | T8.1 | proved |
| 3.7 | Lemma | Elasticity form (path derivative) | elasticity | T10.1 | proved |
| 4.1 | Theorem | Monotone gain sweeps cannot window | monotone-gain-sweeps | T8.4, T13 C2 | proved |
| 4.2 | Proposition | Prior precision: endpoints and extrema | prior-endpoints | T8.1, T8.2 | proved |
| 4.3 | Proposition | Prior precision: classification | prior-classification | T8.3, T13 C2 | proved |
| 4.4 | Proposition | Coupling: endpoints and extrema | coupling-endpoints | T8.1, T8.2 | proved |
| 4.5 | Proposition | Coupling: classification | coupling-classification | T8.3, T13 C2 | proved |
| 5.1 | Theorem | Gain realizability | realizability | T10.1, T10.2 | proved |
| 5.2 | Corollary | Forced lower ray | forced-lower-ray | T10.1 (factor-radicand route), T10.2 | proved |
| 5.3 | Corollary | Exact class set along precision | exact-class-set | T10.2 | proved |
| 5.4 | Corollary | Unbounded windows for regular gains | unbounded-windows | T10.2 (supplementary) | proved |
| 5.5 | Corollary | What regularity pins | regularity-pins | T10 (derivation) | proved |
| 5.6 | Lemma | Excess components | excess-components | T8.1 (Corollary 3.3, excess identity) | proved |
| 5.7 | Lemma | Bounded gains approach H from above | bounded-gain-limit | T10.3, T10.7 | proved |
| 5.8 | Proposition | Bayesian-weight gain along precision (onset κ > 2; four regimes) | bayesian-weight | T1, T3, T7, T10.3, T10.7, T13 C2 | proved |
| 5.9 | Proposition | Misspecified Kalman gain | misspecified-kalman | T10.1, T10.3, T13 C2 | proved |
| 5.10 | Proposition | Capped gain | capped-gain | T10.3, T10.5, T13 C2 | proved |
| 5.11 | Proposition | Precision-blind gain | precision-blind | T4, T10.3, T13 C2 | proved |
| 5.12 | Theorem | Hill gain for every real n > 1 | hill-turning-points | T4, T7, T10.1, T10.3 (n = 2), T13 A5 | proved |
| 5.13 | Proposition | Hill classification and the mixed class | hill-classification | T10.4, T13 C2 | proved |
| 5.14 | Proposition | No mixed class when G/Π decreases | no-mixed-decreasing-ratio | T13 C2 (row-8 diagnosis, t13\_audit\_classes\_diag2.py) | proved |
| 5.15 | Numerical result | Two-stage gains | two-stage-gains | T10.3, T13 C2 | numerical |
| 6.1 | Lemma | Relay variance at matched power (with coloured excess condition) | tau-relay-variance | T4, T6, T9.1 | proved |
| 6.2 | Proposition | Relay monotone in τ | tau-relay-monotone | T9.1, T9.4 | proved |
| 6.3 | Proposition | Relay classification along τ | tau-relay-classes | T9.4, T13 C2 | proved |
| 6.4 | Proposition | Optimal error along τ (closed form) | tau-optimal-error | T9.1, T9.2 (Wiener route; ARE route via diagnosis) | proved |
| 6.5 | Corollary | Normalised optimal error P/F | tau-optimal-normal-form | T14 G | proved |
| 6.6 | Theorem | Optimal error decreases in τ | tau-optimal-monotone | T9.1, T9.5 | proved |
| 6.7 | Proposition | Optimal classification along τ | tau-optimal-classes | T9.4, T13 C2 | proved |
| 6.8 | Proposition | Best constant-gain relay | tau-best-constant-gain | T9.5 (with mp diagnosis) | proved |
| 6.9 | Proposition | Strict gap P < V | tau-strict-gap | T13 A7 | proved |
| 6.10 | Proposition | Optimal filter at matched variance | matched-variance-optimal | T10.6, T13 C2 | proved |
| 6.11 | Counterexample | The optimal filter can window | optimal-can-window | T10.6 | proved |
| 6.12 | Proposition | Relay at matched variance | matched-variance-relay | T10.6, T13 C2 | proved |
| 6.13 | Proposition | Discrete excess condition L/(2 − L) > FΠ\_d for 0 ≤ L < 2 | discrete-excess | T4, T7 | proved |
| 6.14 | Lemma | Shared excess set (M-P) | shared-excess-set | T12 | proved |
| 6.15 | Proposition | D1 tanh lemma | d1-excess | T12 | proved |
| 6.16 | Proposition | D2 excess set (0 < c < 2) | d2-excess | T12 | proved |
| 6.17 | Proposition | D3 excess set; onset ρ > 2 + u | d3-excess | T12 | proved |
| 6.18 | Proposition | Endpoint limits along Δt | dt-endpoint-limits | T12 (with series-route diagnosis) | proved |
| 6.19 | Theorem | Optimal M-P along Δt: post ↓; prior ↑; avg ↑ | dt-optimal-mp | T12 (a), T13 A1, A2 (b), (c) | proved |
| 6.20 | Proposition | Two rays from an over-weighted sampled relay | dt-two-rays | T12 (with diagnosis) | proved |
| 6.21 | Numerical result | Census of sampled relays | dt-relay-census | T12, T13 C2 | numerical |
| 6.22 | Conjecture | At most two turning points (sampled relays) | dt-two-turning-points | T12, T13 A6, C2 | conjecture |
| 6.23 | Lemma | Σ scaling | sigma-scaling | T12 | proved |
| 6.24 | Proposition | Σ-independent gain | sigma-independent-gain | T12, T13 C2 | proved |
| 6.25 | Proposition | Σ-tracking gain with over-trust ρ | sigma-overtrust | T12, T13 C2 | proved |
| 6.26 | Proposition | Σ-tracking gain with misspecified λ′ | sigma-misspecified-lambda | T12, T13 C2 | proved |
| 6.27 | Proposition | Optimal filter along Σ | sigma-optimal | T12, T13 C2 | proved |
| 6.28 | Proposition | Signal sweeps (Σ and λ): optimal monotone | signal-sweeps | T11.1 | proved |
| 7.1 | Definition | Causal garbling | causal-garbling | — | definition |
| 7.2 | Theorem | Monotonicity under causal garbling | causal-monotonicity | T11.1, T11.2 | proved |
| 7.3 | Corollary | No optimal windows along causal orderings | no-optimal-windows | T11 | proved |
| 7.4 | Corollary | Diagnostic | diagnostic | T11 | proved |
| 7.5 | Proposition | Spectral dominance | spectral-dominance | T11.1, T11.3 | proved |
| 7.6 | Theorem | Causal; pathwise and spectral orderings coincide (Gaussian) | gaussian-orderings-coincide | T13 A8 | proved |
| 7.7 | Proposition | Which studied sweeps are ordered | sweeps-ordered | T11.1, T11.3 | proved |
| 7.8 | Theorem | Sharpness in the power family | power-family-sharpness | T11.3 (with diagnosis), T13 C2 | proved |
| 7.9 | Theorem | Unimodality for 0 < β < 2 | power-family-unimodal | T13 A4, T11.3 (numerical) | proved |
| 7.10 | Proposition | Duality | power-family-duality | T11.1, T11.3 | proved |
| 7.11 | Proposition | Latency | latency | T11.4, T13 C2 | proved |
| 7.12 | Counterexample | Pathwise ordering is not enough | pathwise-not-enough | T11.4 | proved |
| 7.13 | Proposition | Ordering sufficient; not necessary | ordering-not-necessary | T11.5 | proved |
| 7.14 | Corollary | Integrate-and-dump; nested grids | mi-nested | T11.6 | proved |
| 7.15 | Theorem | Integrate-and-dump on the continuum | mi-continuum | T13 A3, T11.6, T12 | proved |
| 7.16 | Proposition | M-P is not a causal-garbling family | mp-not-ordered | T12 | proved |
| 8.1 | Numerical result | Blind searches find no unpredicted class | blind-searches | T10.7, T12 Part C, T13 C2 | numerical |
| 8.2 | Numerical result | Narrow windows need root-finding | narrow-windows | T10.5 | numerical |

**Appendix B — Figures.** The images carry no numbers; the text refers to each one as Figure B.n, so renumbering a result never forces a redraw. The captions below describe what each regenerated image plots (Task 15).

B.1 — A schematic curve σ²(θ) for 0 ≤ θ ≤ 10 (three Gaussian bumps and a logistic step; not the variance of any filter), with its endpoint limits and turning-point values dotted as critical tolerances, its turning points marked and the failure set at R² = 1.25 shaded. Right: the class in each band between consecutive critical tolerances.

B.2 — The (ν, q) plane, ν = 2ΣΠ/λ² from 10⁻² to 10³ (log axis) and q = G/(FΠ) from 0 to 5: the floor crossing q = 2, the optimal envelope q⋆(ν) = 2/(1 + √(1 + ν)), and the boundaries 𝒱(ν, q) = R²\_rel for R²\_rel = 0.5, 1 and 2. The R²\_rel = 1 boundary is the pair of lines q = 0 and q = 2; the R²\_rel = 0.5 boundary touches the envelope at ν\_R = 8 (marked).

B.3 — σ² (log scale) at λ = c = 1, Σ = 0.01 along three design sweeps: (a) Π₀ from 10⁻² to 10⁵ at Π = 1 (case P3, U-shaped; F, V\_c, σ⋆² and Π₀⋆ marked); (b) the same sweep at Π = 500 (case P1, monotone; F and V\_c marked); (c) c from 10⁻⁴ to 10 at Π = Π₀ = 1 (F, σ⋆², c⋆ and c\_F marked). Insets zoom on the minima in (a) and (c).

B.4 — σ² against Π (log axis) at λ = 1, Σ = 0.01 (F = 0.01): the optimal envelope σ⋆²(Π), with the unreachable region below it shaded; a Bayesian-weight base curve (κ = 1.5) carrying three compactly supported bumps of peak 1.5F, placed before the envelope touch point Π\_c = 56.20; the tolerance 1.25F, which gives three windows; and the tolerance 0.6F, with its forced lower ray (0, π\_R), π\_R = 222.2.

B.5 — Hill gain, n = 2, at λ = c = 1, Σ = 0.01, over the half-saturation Π₀ (log axis): the turning-point values m/F (dashed) and M/F (solid). The band m ≤ R² < min(M, F) is the mixed class, lower ray plus window; the band F ≤ R² < M is a window. Vertical lines mark the pair birth Π₀ = 31.475 and the window onset cλ/(4Σ) = 25.

B.6 — Peak variance M/F against the initial over-weighting x, for the Bayesian-weight gain (x = κ) and the misspecified Kalman gain (x = F′/F), at λ = λ′ = c = 1, Σ = 0.01. Both rise from 1 at x = 2; at x = 100 they reach 9.2875 and 17.575.

B.7 — Stationary error against the correlation time τ (log axes) at λ = 1, Σ = 0.01, Π = 1, for the relay with G = 0.5 and for the optimal filter. Left, matched zero-frequency power: both decrease. Right, matched variance v = 0.05: the relay increases, and the optimal error is unimodal with maximum P\_max = 0.008333 at τ = 1/λ; the optimal filter's failure set at R² = 0.8 P\_max is shaded.

B.8 — Optimal error against the sampling interval Δt (log axis) in the point-sampled model at λ = 1, Σ = 0.01, Π = 1, with per-sample noise variance 1/(ΠΔt): the error at sample times falls from σ⋆² toward 0, while the prior error and the time average rise from σ⋆² to F.

B.9 — The sampled relay D1 (gain 1 − e^(−GΔt), G = 0.5, λ = 1, Σ = 0.01, Π = 1) along Δt (log axis). Left: the error at sample times, with the window band 0.09 < R² < 0.20457 shaded and the excess crossing Δt\_E = 100 marked. Right: the time average, plotted as avg/F − 1 on a symmetric-log axis, with the two-ray band between its minimum and F shaded.

B.10 — The process-noise sweep at λ = Π = 1 against u = 2ΣΠ/λ² (log axes), for the Σ-independent gain (G = 1), the Σ-tracking gain that over-trusts precision by ρ = 10, and the optimal filter. Left: absolute error. Right: σ²/F, where the over-trusting gain rises above 1 to a peak of about 2.17 and then falls.

B.11 — The optimal error relative to its supremum over τ, P/sup P, for the power-normalised family S = Kτ^β/(1 + τ²ω²) at λ = 1, Σ = 0.01, K = 1, over the exponent β (horizontal) and log₁₀(λτ) (vertical). The single maximum for 0 < β < 2 is drawn, and the three regimes (ordered with information increasing in τ; spectra cross; ordered with information decreasing in τ) are labelled.

B.12 — Optimal filtering error P(d(θ)) for observations delayed by d(θ) = θe^(−θ), at λ = 1, Σ = 0.01, Π = 1, against θ (log axis): it rises from σ⋆² = 0.0099505 to P(1/e) = 0.0099763 at θ = 1 and falls back. The failure set at R² = 0.0099634 is shaded, and θ = 1, where the causal order reverses, is marked.

**Appendix C — References.** Numbered in order of first citation; a number, once assigned, does not change. References \[46\]–\[53\] are first cited in chapters 6–7.

&#91;1\] Kalman, R. E. & Bucy, R. S. (1961). New results in linear filtering and prediction theory. Journal of Basic Engineering 83(1), 95–108. doi:10.1115/1.3658902

&#91;2\] Ernst, M. O. & Banks, M. S. (2002). Humans integrate visual and haptic information in a statistically optimal fashion. Nature 415, 429–433. doi:10.1038/415429a

&#91;3\] Friston, K. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience 11(2), 127–138. doi:10.1038/nrn2787

&#91;4\] Heffes, H. (1966). The effect of erroneous models on the Kalman filter response. IEEE Transactions on Automatic Control 11(3), 541–543. doi:10.1109/TAC.1966.1098392

&#91;5\] Friedland, B. (1967). On the effect of incorrect gain in Kalman filter. IEEE Transactions on Automatic Control 12(5), 610. doi:10.1109/TAC.1967.1098688

&#91;6\] Nishimura, T. (1967). Error bounds of continuous Kalman filters and the application to orbit determination problems. IEEE Transactions on Automatic Control 12(3), 268–275. doi:10.1109/TAC.1967.1098597

&#91;7\] Griffin, R. E. & Sage, A. P. (1968). Large and small scale sensitivity analysis of optimum estimation algorithms. IEEE Transactions on Automatic Control 13(4), 320–329. doi:10.1109/TAC.1968.1098936

&#91;8\] Sangsuk-Iam, S. & Bullock, T. E. (1990). Analysis of discrete-time Kalman filtering under incorrect noise covariances. IEEE Transactions on Automatic Control 35(12), 1304–1309. doi:10.1109/9.61006

&#91;9\] Ge, Q. et al. (2016). Performance analysis of the Kalman filter with mismatched noise covariances. IEEE Transactions on Automatic Control 61(12), 4014–4019. doi:10.1109/TAC.2016.2535158

&#91;10\] Teunissen, P. J. G., Khodabandeh, A. & Psychas, D. (2021). A generalized Kalman filter with its precision in recursive form when the stochastic model is misspecified. Journal of Geodesy 95(9), 108. doi:10.1007/s00190-021-01562-0

&#91;11\] Crouse, D. F. (2023). Mismatched filter design applied to 1D and 2D sinusoidal models. Proceedings of the 26th International Conference on Information Fusion (FUSION 2023), 1–8. doi:10.23919/FUSION52260.2023.10224097

&#91;12\] Singh, A. & Hespanha, J. P. (2009). Optimal feedback strength for noise suppression in autoregulatory gene networks. Biophysical Journal 96(10), 4013–4023. doi:10.1016/j.bpj.2009.02.064

&#91;13\] Boominathan, L. & Pitkow, X. (2022). Phase transitions in when feedback is useful. Advances in Neural Information Processing Systems 35, 10849–10861.

&#91;14\] Hotz, A. & Skelton, R. E. (1987). Covariance control theory. International Journal of Control 46(1), 13–32. doi:10.1080/00207178708933880

&#91;15\] Xu, J. H. & Skelton, R. E. (1992). An improved covariance assignment theory for discrete systems. IEEE Transactions on Automatic Control 37(10), 1588–1591. doi:10.1109/9.256389

&#91;16\] Heeger, D. J. (1992). Normalization of cell responses in cat striate cortex. Visual Neuroscience 9(2), 181–197. doi:10.1017/S0952523800009640

&#91;17\] Carandini, M. & Heeger, D. J. (2012). Normalization as a canonical neural computation. Nature Reviews Neuroscience 13(1), 51–62. doi:10.1038/nrn3136

&#91;18\] Blackwell, D. (1951). Comparison of experiments. Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, 93–102. doi:10.1525/9780520411586-009

&#91;19\] Blackwell, D. (1953). Equivalent comparisons of experiments. Annals of Mathematical Statistics 24(2), 265–272. doi:10.1214/aoms/1177729032

&#91;20\] Greenshtein, E. (1996). Comparison of sequential experiments. Annals of Statistics 24(1), 436–448. doi:10.1214/aos/1033066220

&#91;21\] Yüksel, S. & Linder, T. (2012). Optimization and convergence of observation channels in stochastic control. SIAM Journal on Control and Optimization 50(2), 864–887. doi:10.1137/100808976

&#91;22\] Yüksel, S. & Başar, T. (2013). Stochastic Networked Control Systems: Stabilization and Optimization under Information Constraints. Birkhäuser. doi:10.1007/978-1-4614-7085-4

&#91;23\] Yüksel, S. & Başar, T. (2024). Comparison of information structures and their Blackwell ordering. Stochastic Teams, Games, and Control under Information Constraints, 261–283. doi:10.1007/978-3-031-54071-4\_7

&#91;24\] Hansen, O. H. & Torgersen, E. N. (1974). Comparison of linear normal experiments. Annals of Statistics 2(2), 367–373. doi:10.1214/aos/1176342672

&#91;25\] Kalata, P. R. (1984). The tracking index: a generalized parameter for α-β and α-β-γ target trackers. IEEE Transactions on Aerospace and Electronic Systems 20(2), 174–182. doi:10.1109/TAES.1984.310438

&#91;26\] Saho, K. & Masugi, M. (2016). α-β-γ tracking filters using acceleration measurements. SpringerPlus 5, 309. doi:10.1186/s40064-016-1960-8

&#91;27\] Bryson, A. E. & Johansen, D. E. (1965). Linear filtering for time-varying systems using measurements containing colored noise. IEEE Transactions on Automatic Control 10(1), 4–10. doi:10.1109/TAC.1965.1098063

&#91;28\] Bryson, A. E. & Henrikson, L. J. (1968). Estimation using sampled data containing sequentially correlated noise. Journal of Spacecraft and Rockets 5(6), 662–665. doi:10.2514/3.29327

&#91;29\] Jazwinski, A. H. (1970). Stochastic Processes and Filtering Theory. Academic Press.

&#91;30\] Edelsbrunner, H. & Harer, J. (2010). Computational Topology: An Introduction. American Mathematical Society.

&#91;31\] Cohen-Steiner, D., Edelsbrunner, H. & Harer, J. (2007). Stability of persistence diagrams. Discrete and Computational Geometry 37(1), 103–120. doi:10.1007/s00454-006-1276-5

&#91;32\] Carr, H., Snoeyink, J. & Axen, U. (2003). Computing contour trees in all dimensions. Computational Geometry 24(2), 75–94. doi:10.1016/S0925-7721(02)00093-7

&#91;33\] Milnor, J. (1963). Morse Theory. Princeton University Press.

&#91;34\] Edelsbrunner, H., Letscher, D. & Zomorodian, A. (2002). Topological persistence and simplification. Discrete and Computational Geometry 28(4), 511–533. doi:10.1007/s00454-002-2885-2

&#91;35\] Oudot, S. Y. (2015). Persistence Theory: From Quiver Representations to Data Analysis. American Mathematical Society.

&#91;36\] Deyst, J. J., Jr. & Price, C. F. (1968). Conditions for asymptotic stability of the discrete minimum-variance linear estimator. IEEE Transactions on Automatic Control 13(6), 702–705. doi:10.1109/TAC.1968.1099024

&#91;37\] Kurt, B. & Orguner, U. (2025). Performance of the Kalman filter and smoother for benchmark studies. arXiv:2511.22034.

&#91;38\] Simon, D. (2006). Optimal State Estimation: Kalman, H Infinity, and Nonlinear Approaches. Wiley-Interscience. doi:10.1002/0470045345

&#91;39\] Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. Journal of Basic Engineering 82(1), 35–45. doi:10.1115/1.3662552

&#91;40\] Anderson, B. D. O. & Moore, J. B. (1979). Optimal Filtering. Prentice-Hall.

&#91;41\] Hotz, A. & Skelton, R. E. (1985). A covariance control theory. Proceedings of the IEEE Conference on Decision and Control, 552–557. doi:10.1109/CDC.1985.268547

&#91;42\] Collins, E. G. & Skelton, R. E. (1987). A theory of state covariance assignment for discrete systems. IEEE Transactions on Automatic Control 32(1), 35–41. doi:10.1109/TAC.1987.1104443

&#91;43\] Yasuda, K., Skelton, R. E. & Grigoriadis, K. M. (1993). Covariance controllers: a new parametrization of the class of all stabilizing controllers. Automatica 29(3), 785–788. doi:10.1016/0005-1098(93)90075-5

&#91;44\] Skelton, R. E. & Ikeda, M. (1989). Covariance controllers for linear continuous-time systems. International Journal of Control 49(5), 1773–1785. doi:10.1080/00207178908559737

&#91;45\] Chang, G. (2014). On Kalman filter for linear system with colored measurement noise. Journal of Geodesy 88(12), 1163–1170. doi:10.1007/s00190-014-0751-7

&#91;46\] Shmaliy, Y. S., Zhao, S. & Ahn, C. K. (2020). Kalman and UFIR state estimation with coloured measurement noise using backward Euler method. IET Signal Processing 14(2), 64–71. doi:10.1049/iet-spr.2019.0166

&#91;47\] Ren, H., Amezcua, J. & van Leeuwen, P. J. (2021). Effects of mis-specified time-correlated model error in the (ensemble) Kalman smoother. Quarterly Journal of the Royal Meteorological Society 147(734), 573–588. doi:10.1002/qj.3934

&#91;48\] Martínez-Rey, M., Espinosa, F. & Gardel, A. (2017). Analysis of the optimal sampling rate for state estimation in sensor networks with delays. ISA Transactions 68, 293–301. doi:10.1016/j.isatra.2017.03.007

&#91;49\] Le Cam, L. (1964). Sufficiency and approximate sufficiency. Annals of Mathematical Statistics 35(4), 1419–1455. doi:10.1214/aoms/1177700372

&#91;50\] Torgersen, E. N. (1991). Comparison of Statistical Experiments. Cambridge University Press. doi:10.1017/CBO9780511666353

&#91;51\] Hogeboom-Burr, I. & Yüksel, S. (2021). Comparison of information structures for zero-sum games and a partial converse to Blackwell ordering in standard Borel spaces. SIAM Journal on Control and Optimization 59(3), 1781–1803. doi:10.1137/20M1343701

&#91;52\] Bar-Shalom, Y. (2002). Update with out-of-sequence measurements in tracking: exact solution. IEEE Transactions on Aerospace and Electronic Systems 38(3), 769–777. doi:10.1109/TAES.2002.1039398

&#91;53\] Yoder, J. et al. (2018). Exploring the exponentially decaying merit of an out-of-sequence observation. Sensors 18(6), 1947. doi:10.3390/s18061947

**Appendix D — Verification record, Tasks 1–16.** For each task: the pre-registration and results files, the pre-registered checks that passed and failed, and every failure with the attribution its report gives (criterion, input, code, document or prediction). Outcomes are copied from the reports, not re-judged, and every failure stays recorded.

**Task 1.** verification/PREREG.md · verification/REPORT.md. 12 checks with a verdict; 12 pass, 0 fail.

**Task 2.** verification/PREREG.md · verification/REPORT.md. 3 checks with a verdict; 3 pass, 0 fail.

**Task 3.** verification/PREREG.md · verification/REPORT.md. 8 checks with a verdict; 8 pass, 0 fail.

**Task 4.** verification/PREREG.md · verification/REPORT.md. Exploratory by pre-registration (outcomes reported either way; no pass/fail criteria).

**Task 5.** verification/PREREG.md · verification/REPORT.md. The report itself (verification/REPORT.md); no pass/fail criteria.

**Task 6.** verification/PREREG\_t6.md · verification/REPORT.md. 6 checks with a verdict; 5 pass, 1 fail.

- Failure — C5 (peak locations to 3 s.f. against Task 4b): criterion — Task 4b located peaks on a grid of about 0.4 % steps; heights all match, three locations differ in the third figure.

**Task 7.** verification/PREREG\_t7.md · verification/REPORT.md. 15 checks with a verdict; 15 pass, 0 fail.

**Task 8.** classification/PREREG\_t8.md · classification/REPORT.md. 5 checks with a verdict; 5 pass, 0 fail.

**Task 9.** classification/PREREG\_t9.md · classification/t9/RESULTS\_t9.md. 7 checks with a verdict; 5 pass, 2 fail.

- Failure — T9.2 ARE route: criterion — the regularised ARE converges as √ε with a large prefactor; mp ARE and the closed-form Wiener filter match the document.
- Failure — T9.5 monotonicity and ordering: criterion — float64 resolution; 0 of 285 and 0 of 13 flags are real at higher precision.

**Task 10.** classification/PREREG\_t10.md · classification/t10/RESULTS\_t10.md. 10 checks with a verdict; 6 pass, 4 fail.

- Failure — T10.1 symbolic (2 items): criterion / route — no √(square) handling in the pre-registered SymPy route; identities hold.
- Failure — T10.2 A1.3 as specified: plan's construction (criterion as pre-registered); the supplementary construction passes.
- Failure — T10.5 pair birth: criterion.
- Failure — T10.6 matched-variance τ (zero-limit shape check): criterion.

**Task 11.** classification/PREREG\_t11.md · classification/t11/RESULTS\_t11.md. 11 checks with a verdict; 10 pass, 1 fail.

- Failure — T11.3 classes: criterion — the pre-registered limits/brackets at β ≥ 2.

**Task 12.** classification/PREREG\_t12.md · classification/t12/RESULTS\_t12.md. 13 checks with a verdict; 10 pass, 3 fail.

- Failure — Symbolic A5 (D2 post at Δt → ∞): code — the SymPy check route (sympy.limit); the series route confirms.
- Failure — A7 minimum below F and two rays: criterion — the zero tolerance is too coarse for the prior dip.
- Failure — A8 qualitative regression: prediction — the prompt's quick-check numbers.

**Task 13.** classification/PREREG\_t13.md · classification/t13/RESULTS\_t13.md. 15 checks with a verdict; 10 pass, 5 fail.

- Failure — Part A symbolic (2 of 68 items): criterion / route — identities verified by a post-hoc rewrite route.
- Failure — A2 numerical (auxiliary cross-check, 277 sets): code — precision loss; all agree at higher precision.
- Failure — C1 numbers, first run: document (4, a truncated worked value) and code (2, parser); passes after the fixes.
- Failure — C2 classes, row 8: document — the stated class (1,0,1) cannot occur (proved; class set corrected).
- Failure — C2 classes, row 12: code — route (ii) sample point below its equality tolerance at an exact limit.
- Failure — D reproduction, Task 10: code — run\_t10.sh omits t10\_realize\_diag.py; Task 12: criterion — masking of the provenance runtime list.

**Task 14.** classification/PREREG\_t14.md · classification/t14/RESULTS\_t14.md. 11 checks with a verdict; 8 pass, 3 fail.

- Failure — C4 paper render reproduces v1: criterion — the register types the excess identity as a Corollary (accepted in Task 15).
- Failure — C9 bibliography: input / criterion — two entries unattached and DOIs unresolvable from the session; resolved by the Task 15 input (verified bib, attachments).
- Failure — C10 reproduction: code — the dry-run resolver; all 9 flagged paths resolve as their scripts build them.

**Task 15.** classification/PREREG\_t15.md · classification/RESULTS\_t15.md. 13 checks with a verdict; 11 pass, 2 fail.

- Failure — C4 \[n\] rendering: criterion / code — the pre-registered bracket pattern flags the interval '\[0, 10\]' in the Appendix B description of Figure B.1; it is not a citation, and no unresolved citation remains.
- Failure — C10 thesis phrase check: criterion — all 81 A–E matches are Task 15's figure labels B.1–B.12, which coincide in form with the legacy labels the pattern targets; 0 'Paper 1', no legacy label remains.

**Task 16.** classification/PREREG\_t16.md · classification/RESULTS\_t16.md. 8 checks with a verdict; 5 pass, 3 fail.

- Failure — D1 new proof steps of the thesis draft (2 of 9 items): code — SymPy could not decide a sign and could not denest a square root of a square; both items hold (post-hoc diagnosis).
- Failure — D2 statements against the repository: document / criterion — four statements differ in content: 3.1 and 3.5 gather conclusions the repository states in other results (verified in D1), and the §2.5 table rows for 2.5 and 2.7 left out hypotheses (full statements were then added to the thesis).
- Failure — D6 legacy labels: criterion / document — three hits, none a legacy label: two figure labels in Appendix E outside the exemption window, and a quotation in Appendix D.

**Appendix E — Reproduction.** Environment and the commands that regenerate every numerical result, figure and render.

- Python 3.13.16 on Linux-6.18.44-fc-v114-x86\_64-with-glibc2.39
- Packages (from the installed environment, importlib.metadata; the repository has no lockfile): numpy 2.5.3, scipy 1.18.1, sympy 1.14.0, mpmath 1.3.0, matplotlib 3.11.2, PyYAML 6.0.1.
- Tasks 1–7 record their own environment in verification/results/env.json; Tasks 8–13 in each task's results/env.json.

All commands run from the repository root unless stated.

| Task | What it regenerates | Command |
| --- | --- | --- |
| T1–T7 | starting-study checks, simulations, figures, verification/REPORT.md | cd verification && bash run\_all.sh |
| T8 | Stage 0–1 checks, figure, classification/REPORT.md | cd classification && bash run\_all.sh |
| T9 | Stage 2 τ sweep, t9/RESULTS\_t9.md | cd classification && bash t9/run\_t9.sh |
| T10 | Stage 3 checks, figures, t10/RESULTS\_t10.md | cd classification && bash t10/run\_t10.sh (then python3 t10/t10\_realize\_diag.py, which the run script omits; see Task 13) |
| T11 | Stage 4 checks, figures, t11/RESULTS\_t11.md | cd classification && bash t11/run\_t11.sh |
| T12 | Δt and Σ sweeps, figures, t12/RESULTS\_t12.md | cd classification && bash t12/run\_t12.sh |
| T13 | open items, audits, Paper 2 figures, t13/RESULTS\_t13.md | cd classification && bash t13/run\_t13.sh |
| T8–T13 at once | clean checkout, manifest | bash classification/reproduce\_all.sh WORKDIR 8 9 10 11 12 13 |
| T14 | register, sources, renders, bibliography check | see the render chain below |
| T15 | figures B.n, appendices, renders, checks | see the render chain below |

The Task 14–15 render chain, from classification/:

```bash
python3 t14/build_register.py          # register from the T14 table (T14; overwrites T15 metadata, re-apply next line)
python3 t15/t15_register.py            # T15 citations/status, references.yaml, figures.yaml
python3 t15/make_figs_thesis.py        # figures B.1, B.3-B.12 (text-only edits) and B.2
python3 register/render.py --numbering thesis   # Stages_0_4_Thesis.md, Roadmap_v3.md, figs_thesis/*.txt, Appendices A-C, reference/phase1/
python3 register/render.py --numbering paper    # Stages_0_4_Paper2.md
python3 t15/make_appendix_de.py        # Appendices D and E
python3 t15/t15_checks.py && python3 t15/t15_partG.py   # Task 15 checks
```

The sources were derived once from their Task 14 versions and are now edited directly; this chain does not regenerate them.
