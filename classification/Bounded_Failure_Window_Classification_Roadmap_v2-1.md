# Roadmap v2: Classifying Failure-Set Topology in Stationary Linear Filters

**Author:** John Holder · **Status:** thesis-level research plan following Paper 1 · Revised 7 October 2026

This document is self-contained: it summarizes Paper 1, fixes notation and terminology, and sets out a formally specified classification program. Version 2 adds a precise definition of "complete classification," a general topology theorem, a falsification stage, a standard classification procedure, result labels, a verification protocol and a synthesis matrix.

---

## 1. Background: what Paper 1 established

**Paper 1:** J. Holder (2026), *A Bounded Failure Window in a Miscalibrated Precision-Weighted Relay*. Code and verification: `github.com/RedWing-Duck/Bounded-Failure-Window` (private until publication).

### 1.1 Model

A scalar Ornstein–Uhlenbeck coordinate is corrected toward a noisy signal with a gain that depends on the observation precision $\Pi$. The error $x$ obeys

$$
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\text{sim}},
$$

where:
- $\xi_s$ is white sensory noise of intensity $1/\Pi$;
- $\xi_{\text{sim}}$ is white process noise of intensity $2\Sigma$;
- $G(\Pi)$ is the gain schedule. At each precision the gain is constant in time, but it may vary across precisions.

This is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so all results concern **actual** error variance, never filter-reported variance.

### 1.2 Key results

**Stationary variance.**
$$
\sigma^2(\Pi) = \frac{\Sigma + \tfrac12 G^2/\Pi}{\lambda + G}.
$$
The floor (no correction) is $F = \Sigma/\lambda$. The high-precision limit is $H = \Sigma/(\lambda + G_\infty)$, where $G_\infty = \lim_{\Pi\to\infty} G$.

**Excess identity.**
$$
\sigma^2 - F = \frac{G\big(\lambda G/(2\Pi) - \Sigma\big)}{\lambda(\lambda + G)},
\qquad
\sigma^2 > F \iff G > 2F\Pi.
$$
Its reading: correction injects noise $G^2/(2\Pi)$ and removes variance $\Sigma G/\lambda$; the relay is worse than no correction exactly when injection exceeds removal.

**Optimal benchmark.** The steady-state Kalman–Bucy gain is $G^\star = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}$, with $\sigma_\star^2 = G^\star/\Pi$, which decreases strictly from $F$. Hence $G^\star \le F\Pi$: at least a factor of 2 below the excess threshold.

**Window theorem.** Assume $G$ is continuous, $G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$, and $G \to G_\infty \in (0,\infty)$. Then some tolerance $R^2$ fails on a bounded set of precisions away from zero (a **window**, not necessarily one interval) if and only if
$$
\sup_{\Pi>0} \frac{G(\Pi)}{\Pi} > 2F.
$$
- Every $R^2 \in (F, \sup\sigma^2)$ then produces a window.
- If $\sigma^2$ approaches $F$ from below as $\Pi \to 0$, $R^2 = F$ can produce one too.
- The optimal filter never produces a window.

**Bayesian-weight gain.** For $G = c\,\Pi/(\Pi + \Pi_0)$, define the over-weighting ratio $\kappa = (c/\Pi_0)/F$.
- A window exists if and only if $\kappa > 2$.
- The peak is then unique and analytically located.
- Four regimes against a tolerance: every precision ($R^2 \le H$), lower threshold ($H < R^2 \le F$), window ($F < R^2 < M$), none ($R^2 \ge M$), where $M$ is the peak variance.

**Effect size** (with $\lambda = c = 1$, $\Sigma = 0.01$):

| $\kappa$ | 2 | 3 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|---|
| Peak / $F$ | 1.000 | 1.036 | 1.175 | 1.584 | 2.432 | 5.000 | 9.288 |

**Windows need loose tolerances.** A window requires $R^2 \ge F$: the tolerance must be at least as loose as the error with no correction. Switching on correction then breaks a specification that was already being met.

**Extensions already proved.**
- *Coloured sensory noise* (Ornstein–Uhlenbeck, correlation time $\tau$, matched zero-frequency power): the excess condition becomes $G/\Pi > 2F(1 + a\tau)$ with $a = \lambda + G$. For the Bayesian-weight gain, a window exists iff $c/\Pi_0 > 2F(1 + \lambda\tau)$.
- *Discrete time* (gain $L$, per-sample precision $\Pi_d$): prior and posterior error exceed the floor iff $L/(2 - L) > F\Pi_d$, i.e. injection $L^2 r$ exceeds removal $F\,L(2 - L)$. The optimal discrete gain satisfies $L^\star/(2 - L^\star) < \tfrac12 F\Pi_d$.

**Other gain shapes.**
- Precision-blind gain $G = G_0$: no window; variance diverges as $\Pi \to 0$.
- Hill gain $G = c\Pi^2/(\Pi^2 + \Pi_0^2)$: zero initial slope, yet a window opens iff $\Pi_0 < c\lambda/(4\Sigma)$. So initial over-weighting is sufficient, not necessary.
- Capped schedule $G = \min(g\Pi, c)$: window iff $g > 2F$.

**Exploratory findings (simulation).**
- Signal drift adds a separate failure mode at high precision.
- Kalman gains of a misspecified model share the Bayesian-weight onset condition, but peak about twice as high at $\kappa = 100$ (0.1758 vs 0.0929 in the continuous limit). Peak height depends on gain shape.

---

## 2. Terminology

### 2.1 Terms coined in Paper 1
- **Excess identity**: $\sigma^2 - F$ has the sign of $G - 2F\Pi$.
- **Window / bounded failure window**: a failure set that is nonempty, bounded, and away from zero.
- **Failure set / tolerance-failure set**: $\{\theta : \sigma^2(\theta) > R^2\}$.
- **Bayesian-weight gain**: $c\Pi/(\Pi + \Pi_0)$, the one-step Kalman weight used as a steady gain.
- **Over-weighting ratio** $\kappa$: the gain's initial slope divided by the optimal initial slope.
- **Precision-blind gain**: a gain independent of precision.
- **Capped precision schedule**: $\min(g\Pi, c)$.
- **Three reference points**: the optimal filter, no filtering ($F$), and the task tolerance ($R^2$).
- **Four regimes**: every precision, threshold, window, none.
- **"Windows need loose tolerances."**

Ordinary words given a specific meaning:
- **Relay**: the constant-gain filter. The name comes from the neural-modelling origin of the question.
- **Floor** ($F$), also called the zero-precision value; **high-precision limit** ($H$).
- **Statistical confinement** and **operational failure**: two of the three "stability" notions.
- **Gain family**, **gain schedule**, **slope ratio**.

### 2.2 Naming collisions to handle
- **"Excess"**: in adaptive filtering, "excess mean-square error" is error above the *optimal* (Wiener) solution. Ours is excess above the *no-correction floor*. Say so at first use.
- **"Relay"**: in control theory this means relay (on–off) feedback and relay autotuning. Define at first use.
- **"Floor"**: differs from "noise floor" in signal processing.
- **Consistency:** Paper 1 mixes "mean-squared" and "mean-square"; pick one. It uses "filter-calculated" only for Ge et al.'s term and "filter-reported" for its own.

---

## 3. Central research question

> Under what conditions does the tolerance-failure set of a stationary linear filter change topology as an environment or design parameter varies, and which topologies are impossible for an optimal filter?

Sub-questions, each answered by a stage below:
1. What failure-set topologies are possible in principle? (Stages 0–1)
2. What quantities determine the topology? (Stage 1)
3. Which sweeps and gain families produce each topology? (Stage 2)
4. Is the list for this model complete, and how complex can failure sets get? (Stage 3)
5. Which topologies are impossible for optimal filters? (Stage 4)
6. Are the possible topologies robust and practically relevant? (Stage 5)
7. Do the results extend to discrete-time, coloured-noise and multivariate filters? (Stage 6)

**Minimal thesis.** Stages 0–4 for a meaningful set of scalar sweeps and gain families form a coherent thesis on their own. Stages 5–6 strengthen it but are not required to make it valid.

---

## 4. Stage 0: Define the classification problem

**Domain.** Each swept parameter $\theta$ has a stated domain, normally an open interval $(\theta_-, \theta_+)$ with $\theta_\pm$ possibly $0$ or $\infty$. Every statement distinguishes a finite endpoint that belongs to the domain from an asymptotic limit. Paper 1's convention is kept: precision lives on $\Pi > 0$, and behaviour at $0$ and $\infty$ enters only through limits.

**Failure set.** $\mathcal{F}(R^2) = \{\theta : \sigma^2(\theta) > R^2\}$, with $\sigma^2$ the actual stationary error variance, assumed continuous on the domain. Strict inequality is the convention throughout, so the failure set is open.

**Complete topological description.** An open subset of an interval is a countable union of disjoint open intervals. It is therefore described exactly by three items:
- whether it contains a neighbourhood of the lower end (a **lower ray**);
- whether it contains a neighbourhood of the upper end (an **upper ray**);
- the number $k$ of components bounded away from both ends (**windows**), which may be $0, 1, 2, \ldots$ or infinite.

The **class** of a failure set is the triple (lower ray?, upper ray?, $k$). The named classes of v1 are special cases:

| Named class | (lower, upper, $k$) |
|---|---|
| Empty | (no, no, 0) |
| Everything | the whole domain (a single component touching both ends) |
| Lower ray / threshold | (yes, no, 0) |
| Upper ray | (no, yes, 0) |
| Two rays | (yes, yes, 0) with a gap |
| Window | (no, no, 1) |
| Multi-window | (no, no, $k \ge 2$) |
| Mixed | e.g. (yes, no, 1): a threshold plus a window |

**"Complete classification" means two different things, kept separate:**
- **A. Topological classification:** which classes a continuous $\sigma^2$ can produce at all. The answer is all of them, so this part is a short lemma.
- **B. Model classification:** which classes actually occur for a given model, sweep and gain family, for every tolerance, with conditions. This is the substance of the thesis.

A model classification is **complete** when, for every parameter value and every tolerance (including the critical tolerances of Stage 1), the class is determined, and every class claimed impossible has a proof.

---

## 5. Stage 1: General classification theorem

**Critical tolerances.** For continuous $\sigma^2$ with finitely many local extrema, define the critical tolerances as the endpoint limits $\sigma^2(\theta_-^+)$, $\sigma^2(\theta_+^-)$ and the values of $\sigma^2$ at its local extrema.

**Theorem to prove (Stage 1 core).**
1. The class of $\mathcal{F}(R^2)$ is constant on each open interval of $R^2$ between consecutive critical tolerances. It can change only when $R^2$ crosses a critical tolerance.
2. A lower (upper) ray is present iff $R^2$ is below the lower (upper) endpoint limit; when $R^2$ equals the limit, the approach direction decides.
3. The number of windows satisfies $k \le$ the number of interior local maxima with value above $R^2$, with equality under a stated separation condition.
4. Hence the whole classification of a model reduces to computing endpoint limits and the ordered list of extremum values and positions.

Parts 1–3 are near-topological. The thesis content is part 4: computing these quantities in closed form for filtering models.

**Equality cases are mandatory.** Every classification table must state the class at each critical tolerance ($R^2 = F$, $R^2 = H$, $R^2 = M$, and any other extremum value) and at each parameter value where the number of extrema changes (onset conditions such as $\kappa = 2$, degenerate stationary points, equal-height extrema). Paper 1 already has one such case: a gain whose variance approaches $F$ from below produces a window at exactly $R^2 = F$.

**Filtering-specific link.** The excess set $\{E > 0\}$, with $E = \sigma^2 - F$, decides whether windows exist for tolerances just above the floor; by the excess identity this is $\{G > 2F\Pi\}$ for precision sweeps.

---

## 6. Stage 2: Model classification

### 6.1 Two kinds of sweep
- **Environment sweeps** change the world the filter sees: precision $\Pi$, correlation time $\tau$, process-noise scale $\Sigma$. The optimal filter changes along them, so optimal-filter questions are meaningful.
- **Design sweeps** change the filter itself: prior precision $\Pi_0$, coupling $c$. The optimal filter does not depend on them; they classify miscalibration.
- The sampling interval $\Delta t$ can be either, depending on whether it is imposed or chosen.

### 6.2 Scalar sweeps

| Swept variable | Kind | Floor fixed? | Status |
|---|---|---|---|
| Precision $\Pi$ | environment | yes | done (Paper 1) |
| Correlation time $\tau$ | environment | yes | excess condition proved; sweep in $\tau$ not done |
| Sampling interval $\Delta t$ | either | yes, with matched discretization | condition proved at fixed $\Delta t$; sweep not done |
| Process-noise scale $\Sigma$ | environment | **no** | not started; needs moving-floor treatment |
| Prior precision $\Pi_0$ | design | yes | **done**: Stage 0–1 results, Props 4.1–4.2 |
| Coupling $c$ | design | yes | **done**: Stage 0–1 results, Props 5.1–5.2 |

For each: endpoint limits, extrema (number, positions, values), critical tolerances, the class for every tolerance including equality cases, and the optimal filter's behaviour where meaningful.

**Moving floors.** When $\Sigma$ (or $\lambda$) is swept, $F = \Sigma/\lambda$ moves with $\theta$. The tolerance stays fixed, so the Stage 1 theorem still applies, but the excess identity no longer decides the class by itself.

### 6.3 Gain families
Bayesian-weight; Kalman gain of a misspecified model; Hill/sigmoid; capped linear; fixed $\alpha$–$\beta$; precision-blind. For each, map onset conditions *and* peak heights. Paper 1 showed peak height can differ by about a factor of 2 at the same initial over-weighting.

---

## 7. Stage 3: Falsification and completeness

This is a formal stage, not a contingency. Its aim is to break the classification before a referee does.

**Component bounds (Stage 2.5 in effect).** For every gain family and sweep, establish one of:
1. an exact maximum number of local extrema of $\sigma^2$, and hence of failure-set components; or
2. a construction showing that arbitrarily many components are possible.

The second outcome would be a strong result: for instance, a continuous gain schedule whose $G/\Pi$ crosses $2F$ many times produces many windows near $R^2 = F$ (Paper 1, Section 3.4).

**Adversarial questions to settle explicitly.**
- Can a continuous gain schedule produce three or more separated windows? (Expected: yes, by construction.)
- Can a mixed class (a ray plus windows) occur for a natural gain family, not only a constructed one?
- Can two extrema have equal height, and does that change the class?
- Can a degenerate stationary point change the class without changing the number of extrema?
- Can a numerical search over parameters find a class not predicted by the analysis?
- Can an optimal filter be non-monotone along a sweep that is not an information ordering? (Links to Stage 4.)

**Search method.** Random and adversarial parameter sampling, deliberately concentrated near every critical tolerance and onset condition, with root-finding rather than grids to locate components. Grids miss narrow windows.

---

## 8. Stage 4: The optimality theorem

- **Known:** along precision sweeps the optimal error is strictly decreasing, so the optimal filter produces only empty, everything or lower-ray failure sets. No windows, no upper rays, no two rays.
- **Conjecture:** the same holds along any environment sweep that orders observations by informativeness in Blackwell's sense.
- **Open side:** sweeps that are not information orderings (correlation time at matched zero-frequency power; sampling interval). Determine whether the optimal filter can produce a window or other non-monotone class along them.
- **Scope:** environment sweeps only.
- **Either outcome is publishable.** If the conjecture holds, it is the organizing theorem: windows are impossible for optimal filters exactly along information orderings. If it fails, the counterexample is a result in its own right.

---

## 9. Stage 5: Robustness and practical relevance

**Structural stability.** By the Stage 1 theorem, the class is locally constant in $R^2$ away from critical tolerances. Extend this to parameters:
- How far is a given system from the nearest classification boundary (in $R^2$ and in model parameters)?
- Does a small perturbation of $G(\theta)$ destroy a window? (Expected: not if $R^2$ is a regular value and extrema are non-degenerate.)
- How much numerical error misidentifies a class?

**Practical relevance.** Paper 1 showed windows need loose tolerances ($R^2 \ge F$) and large miscalibration for large peaks. Quantify this per family: the smallest miscalibration that produces a window clearing a given tolerance margin above $F$.

**Applied case.** One concrete setting with published gains and specifications (GNSS/INS fix weighting is the leading candidate). The decisive question: do real systems ever combine a specification looser than the uncorrected error with miscalibration large enough to clear it? Either answer is a result.

## 10. Stage 6: Extensions
- **Discrete time and coloured noise:** restate Paper 1's Propositions 5 and 6 as corollaries of the Stage 1 framework rather than separate results.
- **Multivariate:**
  1. Decoupled case: if dynamics, process-noise covariance, measurement-noise covariance and gain are simultaneously diagonalizable, the problem splits into scalar copies. Prove this first. Sharing eigenvectors with the floor covariance alone is not enough.
  2. Mixing case: search 2×2 systems for windows no single direction predicts.
  3. Choose and justify the vector failure criterion (trace, largest eigenvalue, or a fixed direction); the classification may differ between them.

---

## 11. Standard classification procedure

Given a model, a swept parameter $\theta$ and a gain schedule $G(\theta)$:
1. State the domain and its endpoint conventions.
2. Compute the endpoint limits of $\sigma^2$.
3. Find all stationary points of $\sigma^2$ and classify them (maximum, minimum, degenerate).
4. Order them by position and compute their values.
5. Form the list of critical tolerances.
6. For each interval between critical tolerances, and at each critical tolerance, read off (lower ray?, upper ray?, $k$).
7. Record onset conditions: parameter values where the number of extrema changes.
8. Apply the optimal-filter restriction where the sweep is an environment sweep.
9. Label every conclusion as analytic, numerical or conditional (Section 12).

---

## 12. Result labels

Every result in the thesis carries exactly one label:
- **Theorem / Proposition:** proved analytically.
- **Corollary:** follows directly from a proved result.
- **Numerical result:** supported computationally, not proved.
- **Conjecture:** plausible, unproved.
- **Counterexample:** a demonstrated instance, analytic or numerical, stated as which.

The synthesis matrix (Section 14) shows the label of each entry.

---

## 13. Verification protocol

Paper 1's approach (checks specified in advance, pass/fail criteria committed before running, failures left recorded) carries over, extended for classification:

**Analytic:** symbolic derivation; an independent second simplification; limiting cases (including Paper 1's results as special cases); dimensional consistency.

**Numerical:** random parameter sets; values on, just inside and just outside every predicted boundary; component counting by root-finding, not grids.

**Adversarial:** extreme parameter ratios; nearly degenerate and nearly equal extrema; very narrow and very broad windows; tolerances within $10^{-6}$ relative of a critical tolerance; parameters approaching domain ends.

---

## 14. Final output: synthesis matrix

The classification result of the thesis is one table, filled in by Stages 2–4:

| Sweep | Kind | Gain family | Endpoint limits | Extrema | Critical tolerances | Possible classes | Optimal can produce | Conditions | Label |
|---|---|---|---|---|---|---|---|---|---|
| $\Pi$ | env. | Bayesian-weight | $F \to H$ | one max iff $\kappa > 2$ | $H, F, M$ | everything, lower ray, window, empty | lower ray, everything, empty | $\kappa > 2$ for window | Theorem (Paper 1) |
| $\Pi_0$ | design | Bayesian-weight | $V_c \to F$ (below) | one min iff $\Pi < \Pi_A$, value $\sigma_\star^2$ | $\sigma_\star^2, V_c, F$ | All, two rays, lower ray, upper ray, Empty; never a window | n/a | cases P1–P3 by $\Pi_A, \Pi_B$ | Proposition (Stage 0–1 results, verified T8) |
| $c$ | design | Bayesian-weight | $F$ (below) $\to \infty$ | one min, $\sigma_\star^2$ at $c^\star$ | $\sigma_\star^2, F$ | All, two rays, upper ray; never Empty or a window | n/a | none | Proposition (verified T8) |
| any monotone gain sweep at fixed $\Pi$ | design | any | — | at most one min | — | no window, no mixed class | n/a | — | Theorem 3.2 (verified T8) |
| $\tau$ | env. | Bayesian-weight | — | — | — | — | open (Stage 4) | — | — |
| $\Delta t$ | either | — | — | — | — | — | open | — | — |
| $\Sigma$ | env. | — | moving floor | — | — | — | — | — | — |

---

## 15. Novelty step for the classification

Repeat Paper 1's literature check for the new, more specific question: *has anyone classified the tolerance-exceedance sets of stationary filtering error as a parameter varies?* This is narrower than "is non-monotone filtering error known?", which it is. Search the estimation, control, data-assimilation and robust-filtering literature; record queries and sources; state the result as targeted, not exhaustive, unless it is exhaustive.

---

## 16. Preliminary results (numerical leads, not proofs)

> **Superseded.** Both leads below are now proved, with a correction: the prior sweep is U-shaped only for $\Pi < c(c+2\lambda)/(2\Sigma)$ and monotone above it. See `Stage_0_1_Classification_Results.md`.

These were computed numerically from the closed form in Section 1.2 with $\lambda = c = 1$ and $\Sigma = 0.01$ (so $F = 0.01$). They are leads, not proofs.

**Sweeping the prior precision $\Pi_0$ at fixed $\Pi$ gives a U-shaped curve.**
- As $\Pi_0 \to 0$ the gain tends to $c$ and the variance is large (2.50 at $\Pi = 0.1$; 0.255 at $\Pi = 1$).
- As $\Pi_0 \to \infty$ the gain tends to 0 and the variance returns to exactly $F$.
- In between there is a single minimum slightly below $F$ (0.00995 at $\Pi = 1$, near $\Pi_0 \approx 99.5$), where the gain matches the optimal gain.
- Consequence: for tolerances between that minimum and $F$, the failure set is **two rays**, $(0, a) \cup (b, \infty)$. For $R^2 \ge F$ it is a lower ray. The two-ray band is very narrow, because the minimum is only slightly below $F$.
- Reason: at fixed $\Pi$, the variance as a function of the gain has a single minimum at $G^\star$, so any sweep that moves the gain monotonically through $G^\star$ is U-shaped.

**Sweeping the coupling $c$ at $\Pi = \Pi_0 = 1$ is also U-shaped.**
- The variance equals $F$ at $c \to 0$, dips to a minimum of 0.00995 near $c \approx 0.02$, then grows without bound (about 250 at $c = 1000$).
- Consequence: two rays for tolerances between the minimum and $F$, and an **upper ray** for $R^2 \ge F$.

**Implication for the classification.** Two new classes (two rays; upper ray from a parameter sweep) appear immediately once the swept variable is not precision. This is a strong sign that the classification is not trivial, and that the window is specific to sweeps along which the gain rises and then falls relative to $2F\Pi$.

**To verify first in the new project:** prove the single-minimum property of $\sigma^2$ in $G$ (the stationarity condition $G^2 + 2\lambda G - 2\Sigma\Pi = 0$ has one positive root, so this should be short), then derive both sweeps' extrema in closed form.

---

---

## 17. Order of work and outputs

1. Stage 0 and Stage 1 first: short, and they fix the language for everything else.
2. Stage 2 for the design sweeps ($\Pi_0$, $c$), which have concrete leads, then $\tau$ and $\Delta t$, then $\Sigma$.
3. Stage 3 alongside Stage 2, family by family.
4. Stage 4 once Stage 2 has at least two environment sweeps done.
5. Paper 2: Stages 0–4 for scalar models (this is also the minimal thesis).
6. Paper 3: multivariate (Stage 6). Applied note: Stage 5.

**Stop conditions.**
- If Stage 2 yields no closed-form content beyond the Stage 1 theorem, the classification is a lemma; fold it into the applied work.
- If the Blackwell conjecture fails, write up the counterexample.

---

## 18. How to use this document in a new chat

Attach this file and name the stage. Suggested first request:

> Using the roadmap, do Stages 0 and 1: state the domain conventions, prove the critical-tolerance theorem, then apply the Section 11 procedure to the prior-precision and coupling sweeps. Prove that $\sigma^2$ has a single minimum in $G$ at fixed $\Pi$, derive both sweeps' extrema in closed form, classify every tolerance including equality cases, and label each result. Then write a Claude Code verification prompt following Section 13.

Treat Section 1.2 as established. Verify Section 16 before relying on it.
