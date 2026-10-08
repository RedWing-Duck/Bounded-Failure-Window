# Stage 4: The Optimality Theorem

**John Holder** · Working results for Paper 2 · 8 October 2026 · *unverified (Task 11 pending)*

Companion to Roadmap v2 (Section 8) and the Stage 0–1, 2 and 3 results. Notation as before:
- $F = \Sigma/\lambda$;
- $\sigma_\star^2(\Pi) = G^\star/\Pi = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})$.

Every result carries a Section 12 label.

**Stage 3 status.** Stage 3 is complete for every sweep Stage 2 has covered. Two items are carried forward under their labels:
- Conjecture 3.10 (Hill gain, $n \ne 2$);
- the turning-point bounds for two-stage gains (numerical result).

The $\Delta t$ and $\Sigma$ sweeps will need their own Stage 3 pass once Stage 2 covers them.

**Summary of Stage 4.**
1. **Theorem 4.2.** If a sweep orders observations by *causal* garbling, the optimal filter's error is monotone along it. Its failure set is then only Empty, All or a single ray at the less-informative end. It is never a window.
2. **Proposition 4.4.** For additive Gaussian noise, causal ordering by linear garbling is equivalent to pointwise dominance of noise spectra. This gives a one-line test.
3. **Precision and matched zero-frequency $\tau$ are information orderings.** This settles Stage 2's open question (Proposition 4.5).
4. **Theorem 4.6 (sharpness).** In the family of OU noises with zero-frequency power scaling as $\tau^\beta$, three things coincide: ordering, monotone optimal error, and the absence of optimal-filter windows. All three hold exactly when $\beta \le 0$ or $\beta \ge 2$.
5. **Causality is essential (Proposition 4.7).** A sweep of pathwise-equivalent experiments (sensor latency) gives the optimal filter a window.
6. **Ordering is sufficient, not necessary, in general (Proposition 4.8).**
7. **Diagnostic corollary.** Along a causally ordered sweep, a window certifies miscalibration. Paper 1's windows are therefore signatures of the filter, not of the environment.

---

## 1. Setting

**Scope: observation sweeps.** The signal $s$ is the stationary OU process ($\dot s = -\lambda s + w_s$, intensity $2\Sigma$) and is the same for every $\theta$. Only the observation process $Y_\theta$ changes, jointly stationary with $s$. The optimal filtering error is
$$
P(\theta) = \mathbb{E}\big[(s(t) - \mathbb{E}[s(t) \mid Y_\theta(u),\ u \le t])^2\big],
$$
which is independent of $t$ by stationarity.

Sweeps that change the signal itself ($\Sigma$, $\lambda$) change the estimand and are outside the information-ordering framework. They are treated in the remark at the end of Section 4.

**Definition 4.1 (causal garbling).** Write $\theta_1 \preceq_c \theta_2$ ("$\theta_2$ is causally at least as informative") if there is:
- a random element $U$ independent of $(s, Y_{\theta_2})$, and
- a process $Y'$ such that, for every $t$, $Y'(u \le t)$ is measurable with respect to $\mathcal{G}_t = \sigma(Y_{\theta_2}(u \le t)) \vee \sigma(U)$,

with $(s, Y') \overset{d}{=} (s, Y_{\theta_1})$.

In words: the less informative observations can be manufactured from the more informative ones *as they arrive*, plus independent randomness. This is Blackwell's garbling with a causality constraint added.

---

## 2. The monotonicity theorem

**Theorem 4.2.** If $\theta_1 \preceq_c \theta_2$, then $P(\theta_2) \le P(\theta_1)$.

*Proof.* Equality of joint laws gives $P(\theta_1) = \mathbb{E}[(s(t) - \mathbb{E}[s(t) \mid Y'(\le t)])^2]$. Since $\sigma(Y'(\le t)) \subseteq \mathcal{G}_t$, conditioning on the larger $\sigma$-field cannot increase mean-square error:
$$
P(\theta_1) \ge \mathbb{E}\big[(s(t) - \mathbb{E}[s(t) \mid \mathcal{G}_t])^2\big].
$$
Because $U$ is independent of $(s, Y_{\theta_2})$, $\mathbb{E}[s(t) \mid \mathcal{G}_t] = \mathbb{E}[s(t) \mid Y_{\theta_2}(\le t)]$. The right side is therefore $P(\theta_2)$. $\square$

**Label:** Theorem (proved). The argument is pointwise in $t$, so it also holds for cyclostationary observations (used in Corollary 4.9).

**Corollary 4.3 (no optimal-filter windows along causal orderings).** Suppose $\theta_1 < \theta_2 \Rightarrow \theta_1 \preceq_c \theta_2$ on the whole domain. Then $P$ is non-increasing, and for every $R^2$ the optimal filter's failure set $\{P > R^2\}$ is an initial segment of the domain: **Empty, All or a lower ray.** For the reverse ordering it is Empty, All or an upper ray.

Windows, two rays and mixed classes are impossible.

*Proof.* A superlevel set of a non-increasing function is an initial segment. Plateaus are allowed; Theorem 3.13 covers them. $\square$

**Label:** Corollary (proved). Strict monotonicity is **not** needed.

**Corollary 4.10 (diagnostic).** Along a causally ordered sweep, if any filter's failure set has a window, two rays or a mixed class, that filter is not optimal.

Paper 1's windows along precision, and Stage 3's Hill mixed class, are therefore signatures of miscalibration. Combined with Theorem 3.1 (Stage 3), the precision-sweep picture is complete:
- the optimal filter sits on the envelope $\sigma_\star^2$, whose classes are lower ray and Empty;
- every curve strictly above the envelope belongs to some miscalibrated gain, and every class is available to such gains.

**Label:** Corollary (proved).

---

## 3. A checkable test for additive Gaussian noise

**Proposition 4.4 (spectral dominance).** Let $y_\theta = s + \eta_\theta$, where the $\eta_\theta$ are stationary Gaussian, independent of $s$, with spectral densities $S_\theta(\omega)$. White components are handled in integrated-observation form, as constant densities.

1. **Sufficiency.** If $S_{\theta_1}(\omega) \ge S_{\theta_2}(\omega)$ for almost every $\omega$, then $\theta_1 \preceq_c \theta_2$.
2. **Necessity within linear garblings.** Suppose $S_s > 0$ everywhere. If $Y' = h * y_{\theta_2} + n$, with $h$ a causal LTI filter and $n$ independent, realizes $\theta_1$, then $h = \delta$ and $S_n = S_{\theta_1} - S_{\theta_2} \ge 0$.

So, within causal linear garblings, ordering is equivalent to pointwise spectral dominance.

*Proof.*
1. Let $\xi$ be stationary Gaussian with density $S_{\theta_1} - S_{\theta_2}$, independent of everything, and set $Y' = y_{\theta_2} + \xi$. Then $Y'(\le t)$ is a function of $y_{\theta_2}(\le t)$ and $U = \xi$, and $\eta_{\theta_2} + \xi$ is Gaussian with density $S_{\theta_1}$ and independent of $s$.
2. The cross-spectrum of $s$ with $Y'$ is $H S_s$, which must equal $S_s$, so $H \equiv 1$. Matching the spectra of $Y'$ then gives $S_n = S_{\theta_1} - S_{\theta_2}$. $\square$

**Label:** Proposition (proved). Whether non-linear causal garblings can order two Gaussian experiments that are not linearly ordered is left as Conjecture 4.11 (expected: no, by analogy with the static Gaussian case).

**Proposition 4.5 (the sweeps done so far).**
- **(a) Precision.** $S_\Pi = 1/\Pi$ decreases in $\Pi$, so the sweep is ordered. This recovers Paper 1's result that the optimal filter is monotone along precision.
- **(b) Correlation time at matched zero-frequency power.** $S_\tau(\omega) = (1/\Pi)/(1 + \tau^2\omega^2)$ decreases in $\tau$ at every $\omega$, so the sweep **is a causal information ordering**. Stage 2's Theorem 3.2′ (monotone $P$) follows as a corollary; its strictness still comes from the Stage 2 closed form. The garbling noise has
$$
S_\xi(\omega) = \frac{(\tau_2^2 - \tau_1^2)\,\omega^2}{\Pi\,(1+\tau_1^2\omega^2)(1+\tau_2^2\omega^2)} = |H_\xi(i\omega)|^2,
\qquad
H_\xi(s) = \sqrt{\frac{\tau_2^2 - \tau_1^2}{\Pi}}\;\frac{s}{(1+\tau_1 s)(1+\tau_2 s)},
$$
a second-order process.
- **(c) Correlation time at matched variance.** $S_\tau = 2v\tau/(1+\tau^2\omega^2)$. For $\tau_1 < \tau_2$ it is larger at $\omega = 0$ for $\tau_2$ and larger as $\omega \to \infty$ for $\tau_1$. Every pair crosses, so no two values are linearly ordered. Since $P$ is non-monotone there (Stage 3, Proposition 6.1), Theorem 4.2 shows the family is not causally ordered by *any* garbling.

**Label:** Proposition (proved). Part (b) answers the roadmap's Stage 4 "open side": matched zero-frequency $\tau$ is an information ordering, not a counterexample candidate.

---

## 4. Sharpness: the power-normalized OU family

**Family.** OU sensory noise with spectrum
$$
S_{\beta,\tau}(\omega) = \frac{K\tau^\beta}{1 + \tau^2\omega^2},
\qquad
\operatorname{Var}\eta = v(\tau) = \tfrac{K}{2}\,\tau^{\beta - 1},
\qquad
\tau \in (0,\infty),\ K > 0,\ \beta \in \mathbb{R}.
$$
Two members are already known:
- $\beta = 0$ is matched zero-frequency power ($K = 1/\Pi$, Stage 2);
- $\beta = 1$ is matched variance ($K = 2v$, Stage 3).

The optimal error is Stage 3's quadratic with $v = v(\tau)$:
$$
P = \frac{2C}{B + \sqrt{B^2 + 4AC}},
\qquad
A = \frac{(1-\lambda\tau)^2}{\tau},\ B = 4(\Sigma + \lambda v),\ C = 4\Sigma v.
$$

**Theorem 4.6.**
1. **$\beta \le 0$.** $S_{\beta,\tau}$ decreases in $\tau$ at every $\omega$. The sweep is causally ordered (information increasing in $\tau$), so $P$ is non-increasing. Optimal classes: lower ray or Empty.
2. **$\beta \ge 2$.** $S_{\beta,\tau}$ increases in $\tau$ at every $\omega$. The sweep is causally ordered (information decreasing in $\tau$), so $P$ is non-decreasing. Optimal classes: upper ray or Empty.
3. **$0 < \beta < 2$.** Every pair $\tau_1 \ne \tau_2$ has crossing spectra, so no two are linearly ordered. Moreover $P \to 0$ at both ends while $P > 0$, so for every $0 < R^2 < \max P$ the optimal filter's failure set is bounded away from both ends: **class $(0,0,k)$ with $k \ge 1$**, i.e. a window.

Hence, in this family:
$$
\text{causally ordered} \iff P \text{ monotone} \iff \text{no optimal-filter window} \iff \beta \notin (0, 2).
$$

*Proof.*
- **Ordering.** $\partial_\tau \log S = \beta/\tau - 2\tau\omega^2/(1+\tau^2\omega^2)$. The second term lies in $[0, 2/\tau)$.
  - If $\beta \le 0$, the derivative is $\le 0$ for every $\omega$.
  - If $\beta \ge 2$, it is $> 0$ for every $\omega$.
  - If $0 < \beta < 2$, it is positive at $\omega = 0$, and tends to $(\beta - 2)/\tau < 0$ as $\omega \to \infty$.
  
  Parts 1–2 then follow from Proposition 4.4 and Corollary 4.3. For the crossing claim in part 3: at $\omega = 0$, $S \propto \tau^\beta$ is increasing; as $\omega \to \infty$, $S \sim K\tau^{\beta-2}/\omega^2$ is decreasing.
- **Limits.** For all $\tau$,
$$
P \le \frac{2C}{\sqrt{4AC}} = \sqrt{C/A} = \frac{\sqrt{2\Sigma K}\,\tau^{\beta/2}}{|1 - \lambda\tau|}.
$$
  This tends to $0$ as $\tau \to 0$ iff $\beta > 0$, and as $\tau \to \infty$ iff $\beta < 2$.
- **Window.** For $0 < \beta < 2$, $P$ is continuous and positive with zero limits at both ends. For any $R^2 < \max P$, $\{P > R^2\}$ is non-empty and contained in a compact subinterval. $\square$

**Label:** Theorem (proved).

**Numerical result 4.6a (unimodality).** For $0 < \beta < 2$, $P$ has exactly one turning point, so $k = 1$, in every case checked so far ($\beta \in \{0.05, 0.5, 1, 1.5, 1.95\}$, quick float64 check). Proved for $\beta = 1$ (Stage 3). Task 11 tests it on a fine grid; it is a conjecture otherwise.

**Proposition 4.6b (duality).**
$$
P_{\beta, K}(\tau) = P_{2-\beta,\ K\lambda^{2-2\beta}}\!\left(\frac{1}{\lambda^2\tau}\right).
$$

*Proof.* $A$ is invariant under $\tau \mapsto 1/(\lambda^2\tau)$. The variance $(K'/2)\,x^{1-\beta}$ at $x = 1/(\lambda^2\tau)$ equals $(K/2)\tau^{\beta-1}$ when $K' = K\lambda^{2-2\beta}$. $\square$

**Label:** Proposition (proved). Part 2 of Theorem 4.6 is the mirror image of part 1.

**Reading.** In the natural one-parameter family of coloured noises, the information-ordering condition is exactly sharp: it holds iff the optimal filter cannot window. The two normalizations studied so far sit on opposite sides of the boundary: $\beta = 0$ is ordered and $\beta = 1$ is not.

**Remark (signal sweeps).** For sweeps of $\Sigma$ or $\lambda$, $\sigma_\star^2$ is monotone anyway:
- increasing in $\Sigma$;
- decreasing in $\lambda$ at fixed $\Sigma$;
- increasing in $\lambda$ at fixed $F$, since $\sigma_\star^2 = 2F/(1 + \sqrt{1 + 2F\Pi/\lambda})$.

So the optimal filter has no window there either, but for an elementary reason, not an information-ordering one. **Label:** Proposition (proved; one-line derivatives).

---

## 5. Limits of the theorem

**Proposition 4.7 (causality is essential: pathwise ordering is not enough).**

Setup. Observations are delayed: $y_d(t) = s(t - d) + $ white noise of intensity $1/\Pi$, with $d \ge 0$.
- For every $d$, the whole observation path is a time shift of the $d = 0$ path. So all values of $d$ are equivalent as Blackwell experiments about the path of $s$.
- The optimal *filtering* error is
$$
P(d) = F - e^{-2\lambda d}\,\big(F - \sigma_\star^2(\Pi)\big),
$$
which is strictly increasing in $d$. (By the OU property, $s(t) = e^{-\lambda d}s(t-d) + $ an independent innovation of variance $F(1 - e^{-2\lambda d})$, and $s(t-d)$ is filtered with error $\sigma_\star^2$.)

Sweep. Take latency $d(\theta) = \theta e^{-\theta}$, which rises then falls. The optimal filter then has a **window** in $\theta$ for every $R^2 \in \big(\sigma_\star^2,\ P(1/e)\big)$, even though every member of the sweep is pathwise Blackwell-equivalent to every other.

The causal order runs $d_1 < d_2 \Rightarrow d_2 \preceq_c d_1$, since extra delay is a causal garbling. This order reverses at $\theta = 1$, which is exactly where the window sits.

**Label:** Proposition (proved) + Counterexample (analytic) to "Blackwell ordering (pathwise) implies monotone filtering error". It explains why Definition 4.1 must be causal. Example values ($\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$): $P(0) = 0.0099505$, $P(1/e) = 0.0099763$.

**Proposition 4.8 (ordering is sufficient, not necessary, for monotonicity).** Take matched variance ($\beta = 1$) restricted to $\tau \in (1/\lambda, \infty)$.
- $P$ is strictly decreasing there (Stage 3, Proposition 6.1).
- Yet every pair of noise spectra crosses (Proposition 4.5(c)), so no two values are linearly causally ordered.

So monotone optimal error does not require an information ordering.

**Label:** Proposition (proved, for linear garblings). Extending to all garblings needs Conjecture 4.11.

**Corollary 4.9 (sampling interval, nested grids).** Consider integrate-and-dump sampling at interval $\Delta t$, with $z_k$ the average of $dy$ over the $k$-th interval.
- If $\Delta t_2 = m\,\Delta t_1$ for an integer $m$ and the grids are aligned, each coarse sample is the average of $m$ fine samples, all completed by the time the coarse one is. That is a causal garbling.
- Hence the optimal error, pointwise in $t$ and so also time-averaged, satisfies $P(\Delta t_2) \ge P(\Delta t_1)$. This holds along every chain $\Delta t_0, m\Delta t_0, m^2\Delta t_0, \ldots$

**Label:** Corollary (proved). Monotonicity on the full continuum of $\Delta t$ (non-nested pairs such as $2$ and $3$) is **open**. Task 11 tests it numerically; the Stage 2 $\Delta t$ sweep must settle it.

---

## 6. Answer to the Stage 4 question (Roadmap Section 8)

| Roadmap item | Answer | Result |
|---|---|---|
| Known: precision sweep, optimal monotone | Recovered as an instance of a general theorem | Prop. 4.5(a) |
| Conjecture: monotone along every information ordering | **True**, once the ordering is causal; pathwise ordering is not enough | Thm 4.2, Cor. 4.3; Prop. 4.7 |
| Open side: $\tau$ at matched zero-frequency power | It *is* an information ordering, so monotone | Prop. 4.5(b) |
| Open side: $\tau$ at matched variance | Not ordered; the optimal filter windows | Prop. 4.5(c); Stage 3 Prop. 6.1 |
| Open side: sampling interval | Monotone along nested grids; continuum open | Cor. 4.9 |
| Is ordering exactly the right condition? | Exactly sharp in the power-normalized OU family; sufficient but not necessary in general | Thm 4.6; Prop. 4.8 |

**Thesis-level statement.** Along any causally ordered environment sweep, an optimal filter's failure set is Empty, All or a single ray at the less-informative end. Every other class, including Paper 1's window, certifies a miscalibrated filter.

**Synthesis-matrix additions.**

| Sweep | Kind | Filter | Ordered? | Optimal classes | Label |
|---|---|---|---|---|---|
| $\tau$, $\beta \le 0$ | env. | optimal | yes, info ↑ in $\tau$ | lower ray, Empty | Thm 4.6 |
| $\tau$, $0 < \beta < 2$ | env. | optimal | no (spectra cross) | window ($k \ge 1$; $k = 1$ numerically), Empty | Thm 4.6; Num. 4.6a |
| $\tau$, $\beta \ge 2$ | env. | optimal | yes, info ↓ in $\tau$ | upper ray, Empty | Thm 4.6 |
| delay $d(\theta)$ | env. | optimal | pathwise-equivalent, causally reversing | window when $d$ is non-monotone | Prop. 4.7 |
| $\Delta t$, nested | env. | optimal | yes | ray, Empty | Cor. 4.9 |

**Open, carried forward.**
- Conjecture 4.11 (non-linear garblings add nothing for Gaussian experiments).
- Numerical result 4.6a (unimodality for $0 < \beta < 2$).
- The $\Delta t$ continuum.
- Whether a tidy *necessary* condition for monotone optimal error exists beyond the power family.
