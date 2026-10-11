# Failure-Set Topology in Stationary Linear Filters

Thesis draft v0.1 · John Holder · Oct 11, 2026 · @John Holder

**Status.** Chapters 1–4 drafted. Results are numbered by chapter: Theorem 3.2 is the second numbered result of chapter 3. Appendix A lists every result with its permanent repository key and its verification. References are cited as bracketed numbers \[n\], assigned in order of first citation and listed in Appendix C. Figures are cited as Figure B.n and collected in Appendix B; the images themselves carry no numbers. Remaining chapters are outlined with the results they will contain.

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

**Along precision, the model forbids only one thing.** A variance curve is reachable by some continuous gain iff it never dips below the optimal variance (Theorem 5.1). Every class is then available to some gain (Corollary 5.3), and smooth gains with the natural limits of Theorem 3.4 can have any number of window components (Corollary 5.4). The restrictions come from the gain family:

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

Every result has one type (Definition, Theorem, Proposition, Lemma, Corollary, Numerical result, Conjecture or Counterexample) and one number by chapter, so Theorem 5.12 is the twelfth numbered result of chapter 5. Each also has a permanent key in the project repository; Appendix A lists both, with the verification of each result. Analytic results were checked symbolically and numerically under pre-registered criteria committed before each run, from the starting study (Tasks 1–7) to the consolidation and renumbering (Tasks 13–14). Failed checks stay recorded as failures, with their diagnosis (chapter 8). Blind searches of 10⁶ and 4.4 × 10⁶ classifications found no class outside the predicted sets (Numerical result 8.1).

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

*Figure B.1 (Appendix B): the variance curve with its critical-tolerance diagram, each band labelled by its class.*

A second level sits above the diagram. A family parameter (κ, Π₀, ρ, β) changes the signature itself: it can add or remove turning points or reorder their values. The values of that parameter where the signature changes length are the **onset conditions** of later chapters, such as κ = 2 (Prop. 5.8) and the Hill pair birth (Theorem 5.12).

### 2.5 Where the class changes

For a fixed curve the class changes only at the events below; a sixth kind of point changes nothing. Each row is a consequence of Theorem 2.2 or its plateau extension.

| Event | Occurs when | Effect on the class | Label |
| --- | --- | --- | --- |
| Boundary | R² = L₋ or L₊ | a ray appears or disappears; at equality the approach direction decides | Thm 2.2(2) |
| Extremum | R² = σ²(tⱼ) | a component is born or dies (maximum), or two components merge or split (minimum) | Thm 2.2(3) |
| Equal height | two maxima share a value M₂ | k drops by 2 at the single tolerance M₂ | Cor. 2.5 |
| Plateau | R² equals a plateau value (C2′) | the plateau leaves the failure set and can split a component | Thm 2.4 |
| Pair birth | a family parameter creates a minimum–maximum pair | a new band of tolerances opens from zero width; values separate like δ^(3/2), positions like δ^(1/2) | Prop. 2.7 |
| Non-event | a stationary point that is not a turning point | none | Cor. 2.6 |

The first four are events in R² for one curve. Pair birth is an event in the family parameter: it changes the signature, and so the diagram itself.

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

**Reading.** The margin η is the operational meaning of "thin". When a class occupies a narrow band of tolerances, η is small and modelling errors larger than η can change the class. The Hill mixed band has median width 5 × 10⁻⁴ F (Prop. 5.13), and the sampled relay's prior dips reach 10^(−32,880,317) relative (Prop. 6.20). At a critical tolerance there is no margin at all: raising or lowering a maximum by any amount at R² equal to its value creates or removes a component.

**Relation to persistence stability.** Persistence diagrams are stable in sup norm: the bottleneck distance between the diagrams of two functions is at most the sup-norm distance between them \[31\]. The class at one fixed tolerance is not stable in that sense, because a small perturbation can push an extremum across R² or add a short component near a crossing. Proposition 2.9 is the fixed-level counterpart: it buys stability with a margin η and a monotonicity condition near the crossings. The contrast is between a summary over all levels at once, which is stable, and a single slice, which is not.

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

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters \[4–9, 36–38\].

### 3.2 Coordinates and the surface

Two dimensionless numbers carry all the dependence on λ, Σ, Π and G:

```latex
\nu = \frac{2F\Pi}{\lambda} = \frac{2\Sigma\Pi}{\lambda^2},
\qquad
q = \frac{G}{F\Pi}
```

ν is the signal-to-noise ratio accumulated over one relaxation time 1/λ; q is the gain measured against the floor precision FΠ. In them the variance takes one form.

**Theorem 3.2(a) (normal form).**

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

*Figure B.2 (Appendix B; to draw): the (ν, q) plane with the line q = 2, the envelope q⋆(ν), and the boundaries for R²\_rel = 0.5, 1 and 2.*

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

The theorem covers every monotone design rule, not only the Bayesian weight: Task 8 ran 20,000 random parameter sets through five monotone gain sweeps each, 10⁶ classifications in all, with no window, no mixed class and no interior maximum, and the Task 13 audit repeated this for c·tanh(Π/Π₀), c(1 − e^(−Π/Π₀)) and cΠ²/(Π² + Π₀²) swept in Π₀.

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
| R² ≥ F | Upper ray (c\_R, ∞), equal to (c\_F, ∞) at R² = F |

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

**Verification.** Lemma 3.6 and Propositions 4.2 and 4.4 were checked symbolically, every identity reducing to zero (Task 8, checks T8.1–T8.2). Propositions 4.3 and 4.5 were checked at every row, including each critical tolerance exactly and at ±10⁻⁶ relative and the boundary cases Π = Π\_A and Π = Π\_B: 62 of 62 classes correct, computed by root-finding on monotone pieces (T8.3). Theorem 4.1 was checked on 10⁶ classifications (T8.4), and Task 13 re-audited all three rows on 1,000 fresh parameter sets each with no class outside the stated sets.

*Figure B.3 (Appendix B): σ² along the prior sweep at Π = 1 (case P3, U-shaped) and Π = 500 (case P1, monotone), and along the coupling sweep at Π = Π₀ = 1, with c⋆ and c\_F marked.*

## 5. The Precision Sweep: Expressivity of Gain Families

*To be drafted.* Realizability, forced lower ray, unbounded windows, natural families, the Hill mixed class, two-stage gains (results 5.1–5.15).

## 6. Beyond White Noise

*To be drafted.* Correlation time at matched power in normal form (results 6.1–6.12); sampling interval with time-averaged error as primary metric (results 6.13–6.22); process noise with absolute and relative tolerances (results 6.23–6.28).

## 7. Optimality and Information

*To be drafted.* Causal garbling, monotonicity, the power-normalised family, delay, the diagnostic corollary (results 7.1–7.16).

## 8. Verification

*To be drafted.* Pre-registration protocol; every recorded failure (Tasks 1–13); blind searches (Numerical results 8.1–8.2).

## 9. Discussion and Limits

*To be drafted.* Relevance (thin bands, invisible dips), open conjectures, applied relevance and multivariate extensions as future work.

## Appendices

**Appendix A — Register of results.** Every numbered result, with its thesis number, permanent repository key and verification. *To be assembled from the repository register (82 rows at freeze v1).*

**Appendix B — Figures.** The images carry no numbers; the text refers to each one as Figure B.n, so renumbering a result never forces a redraw. Captions are placeholders until the figures are regenerated.

B.1 — The variance curve of the starting relay with its critical-tolerance diagram, each band labelled by its class (source: fig01\_stage1\_schematic).

B.2 — The normal-form plane (ν, q): the line q = 2, the envelope q⋆(ν), and the class boundaries for R²\_rel = 0.5, 1 and 2 (to draw).

B.3 — σ² along the prior sweep at Π = 1 and Π = 500, and along the coupling sweep at Π = Π₀ = 1, with c⋆ and c\_F marked (source: fig\_t8\_sweeps).

B.4 — Realizability (source: fig02\_realizability).

B.5 — Hill-type phase diagram (source: fig03\_hill\_phase).

B.6 — Peak heights (source: fig04\_peak\_heights).

B.7 — Normalisations of the time constant τ (source: fig05\_tau\_normalizations).

B.8 — Optimal sampling (source: fig08\_optimal\_sampling).

B.9 — The sampled relay (source: fig09\_sampled\_relay).

B.10 — Process noise (source: fig10\_process\_noise).

B.11 — The power family (source: fig06\_power\_family).

B.12 — Measurement delay (source: fig07\_delay).

**Appendix C — References.** Numbered in order of first citation; a number, once assigned, does not change. References \[46\]–\[53\] are cited in chapters 5–9, still to be drafted.

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

**Appendix D — Verification record, Tasks 1–14.** Pre-registered criteria, outcomes and diagnoses of failures, task by task. *To be assembled.*

**Appendix E — Reproduction.** Environment, scripts and the commands that regenerate every numerical result and figure. *To be assembled.*
