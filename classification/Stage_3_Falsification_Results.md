# Stage 3: Falsification and Completeness

**John Holder** · Working results for Paper 2 · 8 October 2026 · verified (Task 10; four pre-registered checks failed on route or criterion, see Section 8)

Companion to Roadmap v2 (Section 7), `Stage_0_1_Classification_Results.md`, `Stage_2_Tau_Sweep_Results.md` and `Stage_3_Plan.md`. Notation as before:
- $\sigma^2(G,\Pi) = (\Sigma + G^2/(2\Pi))/(\lambda + G)$ and $F = \Sigma/\lambda$;
- $G^\star = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}$ and $\sigma_\star^2 = G^\star/\Pi$;
- classes $(\ell, u, k)$ as in C5.

Every result carries a Section 12 label.

**Summary.** No prediction of the Stage 3 plan was falsified. A blind search of $10^6$ classifications found no class outside the predicted sets. Six results organize the stage:
1. **Realizability (Theorem 3.1).** Along a precision sweep, the model constrains the variance curve only through the optimal envelope $\sigma_\star^2$. Every restriction beyond that comes from the shape of the gain family.
2. **Forced lower ray (Corollary 3.2).** At any tolerance tighter than the floor, *every* gain schedule fails on a ray $(0, \pi_R)$. So "windows need loose tolerances" holds for all gains, not just the Bayesian-weight gain.
3. **Unbounded windows (Corollary 3.4).** For every $k$ there is a smooth, Paper-1-regular gain with $k$ windows.
4. **Natural families have one or two turning points (Section 4).** The Hill gain ($n = 2$, proved) produces a **mixed class**, threshold plus window, in a natural family.
5. **Two-stage gains** produce multi-window curves (numerical result).
6. **The optimal filter produces a window** along correlation time at matched variance (Proposition 6.1). The Stage 4 restriction to information orderings is therefore necessary.

---

## 1. Realizability along the precision sweep

**Theorem 3.1 (gain realizability).** Fix $\lambda, \Sigma > 0$. A function $v : (0,\infty) \to (0,\infty)$ equals $\sigma^2(G(\Pi), \Pi)$ for some continuous gain schedule $G \ge 0$ if and only if $v$ is continuous and
$$
v(\Pi) \ge \sigma_\star^2(\Pi) \quad \text{for all } \Pi > 0.
$$
One such gain is the upper-branch inverse
$$
G_+(v, \Pi) = \Pi v + \sqrt{\Pi\,(\Pi v^2 + 2\lambda v - 2\Sigma)}.
$$

*Proof.*
- **Necessity** is Lemma 3.1 (Stage 0–1): $\sigma^2(\cdot, \Pi) \ge \sigma_\star^2(\Pi)$.
- **Sufficiency.** $\sigma^2(G, \Pi) = v$ is equivalent to $G^2 - 2\Pi v G + 2\Pi(\Sigma - \lambda v) = 0$. Its roots are $G_\pm = \Pi v \pm \sqrt{\Pi(\Pi v^2 + 2\lambda v - 2\Sigma)}$.
  - The radicand is $\ge 0$ iff $v$ is at least the positive root of $\Pi v^2 + 2\lambda v - 2\Sigma$, which is $(-\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})/\Pi = \sigma_\star^2$.
  - So $G_+(v(\Pi), \Pi)$ is a continuous function of $\Pi$ (a composition of continuous maps, with a non-negative radicand), and $G_+ \ge \Pi v > 0$. $\square$

**Label:** Theorem (proved; T10.1 symbolic, T10.2 101/101 constructions).

**Corollary 3.2 (forced lower ray; "windows need loose tolerances", general form).** For every continuous gain schedule and every $R^2 < F$, the failure set contains
$$
(0, \pi_R), \qquad \pi_R = \frac{2\lambda (F - R^2)}{R^4}.
$$
Hence $\ell = 1$. At a tolerance tighter than the floor, no gain schedule can give Empty, a pure window, an upper ray alone, or any class with $\ell = 0$.

*Proof.* $\sigma_\star^2$ decreases strictly from $F$ (Paper 1) and equals $R^2$ at $\pi_R$ (solve $\Pi R^4 + 2\lambda R^2 - 2\Sigma = 0$). For $\Pi < \pi_R$, $\sigma^2 \ge \sigma_\star^2 > R^2$. $\square$

**Label:** Corollary (proved). This removes every regularity assumption from Paper 1's "windows need loose tolerances".

**Corollary 3.3 (exact class set along $\Pi$).** For continuous, piecewise strictly monotone variance curves:
- for $R^2 < F$, the achievable classes are exactly those with $\ell = 1$ (any $u \in \{0,1\}$, any finite $k$, including All);
- for $R^2 \ge F$, every class $(\ell, u, k)$ with finite $k$ is achievable.

*Proof.* Impossibility for $R^2 < F$ is Corollary 3.2. For achievability, by Theorem 3.1 it suffices to build a continuous piecewise-monotone $v \ge \sigma_\star^2$ with the target class.
- **$R^2 < F$.** Set $v = \sigma_\star^2$ on $(0, \pi_R]$, which exceeds $R^2$ there. On $[\pi_R, \infty)$, where $\sigma_\star^2 \le R^2$, use a piecewise-linear zigzag (in $\log\Pi$) with troughs at value $R^2$ and peaks above $R^2$, arranged to give the required $u$ and $k$. To merge the lower ray with the first peak, start that peak at $\pi_R$. For All, take $v = \sigma_\star^2 + R^2$.
- **$R^2 \ge F$.** Here $\sigma_\star^2 < F \le R^2$ everywhere, so any zigzag with troughs in $[\max(\sigma_\star^2), R^2]$, e.g. at value $F$, and peaks above $R^2$ works. Near $\Pi = 0$, either start above $R^2$ (for $\ell = 1$) or follow $\sigma_\star^2$ (for $\ell = 0$). $\square$

**Label:** Corollary (proved; T10.2 realized every target, 101/101, and blocked every forbidden target, 24/24).

**Corollary 3.4 (unbounded complexity inside the model).** For every $k \ge 1$ there is a $C^\infty$ gain schedule satisfying Paper 1's regularity ($G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$; $G \to G_\infty \in (0,\infty)$) whose failure set at $R^2 = 1.25F$ has exactly $k$ windows.

*Proof (corrected construction).*
- **Base gain.** Take the Bayesian-weight gain $G_B$ with $1 < \kappa < 2$. Then:
  - $v_B = \sigma^2(G_B, \cdot) < F$ everywhere, since there is no excess when $\kappa \le 2$ (Paper 1);
  - $G_B > G^\star$ near $0$, since its initial slope $c/\Pi_0 = \kappa F$ exceeds $G^{\star\prime}(0) = F$;
  - $G_B < G^\star$ for large $\Pi$, since $G^\star \to \infty$;
  - so $G_B$ meets $G^\star$ first at some $\Pi_c$, where $v_B$ touches $\sigma_\star^2$, and on $(0, \Pi_c)$ $G_B$ lies on the upper branch: $G_B = G_+(v_B, \cdot)$.
- **Bumps.** Add to $v_B$ $k$ disjoint, compactly supported $C^\infty$ bumps inside $(0, \Pi_c)$, each unimodal with peak $1.5F$.
- **New gain.** Set $G = G_+(v, \cdot)$ on $(0, \Pi_c)$ and $G = G_B$ beyond.
  - Outside the bump supports $G = G_B$, so $G$ is continuous and smooth, and Paper 1's regularity is inherited at both ends.
  - Each bump crosses $1.25F$ exactly twice, and $v_B < F$ elsewhere, so there are exactly $k$ windows. $\square$

**Label:** Corollary (proved; T10.2 supplementary check passed for $k = 1..5$, with $G(10^{12})/G(10^{11}) - 1 = 6\times10^{-10}$).

**Correction to the plan.** The plan used $G_+$ everywhere. That fails Paper 1's regularity: when $v \to H > 0$, $G_+ \ge \Pi v$ gives $G_+/\Pi \to 2H$, so $G_+ \to \infty$ (T10.2 as specified: FAIL). The upper branch realizes any curve, but a gain that converges must switch to the lower branch at a point where $v$ touches $\sigma_\star^2$, and the bumps must avoid that point (Gaussian tails do not). Theorem 3.1 is unaffected.

**Corollary 3.5 (what regularity pins).** Under Paper 1's regularity, $L_- = F$ and $L_+ = H = \Sigma/(\lambda + G_\infty)$. So:
- $\ell$ is fixed by $R^2$ versus $F$, plus the approach direction at $R^2 = F$;
- $u$ is fixed by $R^2$ versus $H$;
- $k$ is unbounded (Corollary 3.4);
- since $H < F$, there is never an upper ray at $R^2 \ge F$.

**Label:** Corollary (proved).

**Reading.** Along the precision sweep, the filtering model rules out exactly one thing: being better than optimal. Every further restriction (one peak, no mixed class, no upper ray) is a property of the **gain family**. Section 4 therefore carries the substance.

---

## 2. Excess components

**Lemma 3.6.** $\{\sigma^2 > F\} = \{G/\Pi > 2F\}$ pointwise (the excess identity). Hence:
- at $R^2 = F$ the failure set *is* the excess set;
- for $R^2 \ge F$, every failure component lies in an excess component;
- if $G/\Pi$ is unimodal or decreasing, there is at most one excess component, and so at most one window at $R^2 = F$.

**Label:** Lemma (proved). It covers the Bayesian-weight, misspecified-Kalman, capped and Hill families.

---

## 3. The counting method

**Lemma 3.7 (elasticity form).** For any differentiable gain schedule $G(\Pi) > 0$, with elasticity $\varepsilon = \Pi G'/G$,
$$
\frac{d\sigma^2}{d\Pi} = \frac{G\,N}{2\Pi^2(\lambda+G)^2},
\qquad
N = \varepsilon\,\big(G^2 + 2\lambda G - 2\Sigma\Pi\big) - G(\lambda + G).
$$
Turning points of $\sigma^2(\Pi)$ are exactly the sign changes of $N$. When $G$ is strictly monotone, $N$ becomes a function of $G$ alone.

*Proof.* Chain rule:
$$
\frac{d\sigma^2}{d\Pi}
= \partial_G\sigma^2\,G' + \partial_\Pi\sigma^2
= \frac{(G^2 + 2\lambda G - 2\Sigma\Pi)G'}{2\Pi(\lambda+G)^2} - \frac{G^2}{2\Pi^2(\lambda+G)}.
$$
Put this over the common denominator and write $\Pi G' = \varepsilon G$. $\square$

**Label:** Lemma (proved; T10.1). Monotonicity of $G$ is needed only for the reduction to one variable.

---

## 4. Turning-point bounds for natural gain families (precision sweep)

**General fact used below.** If $G < G_\infty$ everywhere, then $\sigma^2 \ge \Sigma/(\lambda+G) > \Sigma/(\lambda + G_\infty) = H$. So $H$ is approached from above and never attained. This holds for the Bayesian-weight, Hill and capped gains.

### 4.1 Bayesian-weight, $G = c\Pi/(\Pi + \Pi_0)$

With $\varepsilon = 1 - G/c$, the equation $N = 0$ reduces to $G^2 + 2\lambda G + 2\Sigma\Pi_0 - \lambda c = 0$. This has one positive root iff $\lambda c > 2\Sigma\Pi_0$, i.e. $\kappa > 2$. Near $\Pi = 0$, $N \approx \Pi(\lambda c/\Pi_0 - 2\Sigma)$, so the turning point is a maximum.

**Label:** Proposition (proved; recovers Paper 1's onset in three lines; T10.3 position error $6\times10^{-31}$).

### 4.2 Misspecified Kalman gain, $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma'\Pi}$

**Proposition 3.8.** Let $F' = \Sigma'/\lambda'$ and $r = \Sigma/\Sigma'$.
- If $F' > 2F$: $\sigma^2$ has exactly one turning point, a maximum, at the gain
$$
G_M = \frac{-2r\lambda' + \sqrt{4r^2\lambda'^2 + 2(1+r)\lambda'(\lambda - 2r\lambda')}}{1+r},
\qquad
\Pi_M = \frac{G_M^2 + 2\lambda' G_M}{2\Sigma'}.
$$
- If $F' \le 2F$: $\sigma^2$ is strictly decreasing.
- Endpoints: $L_- = F$, approached from above iff $F' > 2F$; $L_+ = 0$.

*Proof.* Here $\Pi(G) = (G^2 + 2\lambda' G)/(2\Sigma')$ and $\varepsilon = (G + 2\lambda')/(2(G+\lambda'))$. Substituting into Lemma 3.7,
$$
N = \frac{G}{2(G+\lambda')}\,q(G),
\qquad
q(G) = -(1+r)G^2 - 4r\lambda' G + 2\lambda'(\lambda - 2r\lambda').
$$
- $q$ is strictly decreasing on $G > 0$.
- $q(0) > 0$ iff $\lambda > 2r\lambda'$, i.e. iff $F' > 2F$.

So $N$ changes sign once, from $+$ to $-$, iff $F' > 2F$, and is negative throughout otherwise. As $\Pi \to \infty$, $G^2/(2\Pi) \to \Sigma'$ while $G \to \infty$, so $\sigma^2 \to 0$. The approach direction at $0$ follows from Lemma 3.6, since $G/\Pi \to F'$. $\square$

**Classification.**
- If $F' > 2F$:
  - $0 < R^2 \le F$: lower ray;
  - $F < R^2 < M$: window;
  - $R^2 \ge M$: Empty.
- Otherwise:
  - $R^2 < F$: lower ray;
  - $R^2 \ge F$: Empty.

All never occurs, because $L_+ = 0$.

**Label:** Proposition (proved; T10.3 2000/2000 sets, regression values pass). This upgrades Paper 1's exploratory finding to a closed form. Its onset matches the Bayesian-weight onset with $\kappa \to F'/F$. At over-weighting ratio 100, the peak is $M/F = 17.575$ versus $9.2875$ for the Bayesian-weight gain, a ratio of **1.892** (Paper 1: "about twice"; figure F4).

### 4.3 Capped, $G = \min(g\Pi, c)$

On the linear branch, $d\sigma^2/d\Pi = g(g\lambda/2 - \Sigma)/(\lambda + g\Pi)^2$, which has the constant sign of $g - 2F$. On the capped branch, $\sigma^2 = (\Sigma + c^2/(2\Pi))/(\lambda + c)$ is strictly decreasing. So:
- $g > 2F$: one maximum, at the kink $\Pi = c/g$;
- $g < 2F$: strictly decreasing;
- $g = 2F$: **plateau** $\sigma^2 \equiv F$ on $(0, c/g]$, then strictly decreasing.

**Label:** Proposition (proved; T10.3, T10.5).

### 4.4 Precision-blind, $G = G_0$

$\sigma^2$ is strictly decreasing from $L_- = \infty$ to $H$. Classes: All for $R^2 \le H$, lower ray for $R^2 > H$.

**Label:** Proposition (proved).

### 4.5 Hill, $G = c\Pi^n/(\Pi^n + \Pi_0^n)$

**Proposition 3.9 (Hill, $n = 2$).** Let $t = \Pi/\Pi_0$, $t_*^2 = 2\sqrt3 - 3$, and
$$
\varphi_* = \frac{t_*\big(\lambda(16\sqrt3 - 24) + c(14\sqrt3 - 24)\big)}{16 - 8\sqrt3},
\qquad
\Pi_0^{\text{pair}} = \frac{c\,\varphi_*}{4\Sigma}.
$$
- If $\Pi_0 < \Pi_0^{\text{pair}}$: $\sigma^2$ has exactly two turning points, a minimum $m$ followed by a maximum $M$.
- If $\Pi_0 > \Pi_0^{\text{pair}}$: $\sigma^2$ is strictly decreasing.
- If $\Pi_0 = \Pi_0^{\text{pair}}$: a single degenerate stationary point, not a turning point.

*Proof.* By Lemma 3.7, $\operatorname{sign} N = \operatorname{sign} Q(t)$, where $t\,Q(t) = N(1+t^2)^3$ up to a positive factor and
$$
Q(t) = c\,t\,P_4(t) - 4\Sigma\Pi_0 (1+t^2)^2,
\qquad
P_4(t) = -(\lambda+c)t^4 + (c+2\lambda)t^2 + 3\lambda.
$$
So $Q > 0$ iff $c\,\varphi(t)/4 > \Sigma\Pi_0$, where $\varphi(t) = t P_4(t)/(1+t^2)^2$. A direct computation gives
$$
\varphi'(t) = \frac{-(t^4 + 6t^2 - 3)\,\big((\lambda + c)t^2 + \lambda\big)}{(1+t^2)^3}.
$$
The second factor is positive, and $t^4 + 6t^2 - 3$ has the single positive root $t_*$. So:
- $\varphi$ increases on $(0, t_*)$ and decreases after it;
- $\varphi(0) = 0$ and $\varphi \to -\infty$.

Hence $\{Q > 0\}$ is an open interval when $\Sigma\Pi_0 < c\varphi(t_*)/4$, and empty otherwise. Since $Q(0) = -4\Sigma\Pi_0 < 0$, $N$ goes $-, +, -$: a minimum, then a maximum. Evaluating $\varphi(t_*)$ with $t_*^2 = 2\sqrt3 - 3$ gives $\varphi_*$. $\square$

**Label:** Proposition (proved). Task 10:
- the $\varphi'$ factorization is SymPy output, re-checked numerically on 2,000 random $(\lambda, c)$ with no sign mismatches;
- at $\lambda = c = 1$, $\Sigma = 0.01$: closed form $\Pi_0^{\text{pair}} = 31.4750497595392$, against the numerical value $31.4750497595392$ (relative difference $6\times10^{-17}$);
- 961 random $n = 2$ sets: exact root-count disagreements 0.

**Classification (Hill, pair present).** Let $H = \Sigma/(\lambda+c)$. Then:
- $\sigma^2 \to F$ from below at $0$, since $G/\Pi \to 0 < 2F$;
- $\sigma^2 \to H$ from above at $\infty$ (general fact above);
- the ordering is $H < m < F$, so the class "two rays" is impossible (it needs $m < H$).

**Case $M > F$** ($\Pi_0 < c\lambda/(4\Sigma)$, Paper 1's window onset):

| Tolerance | Class |
|---|---|
| $R^2 \le H$ | All |
| $H < R^2 < m$ | Lower ray |
| $m \le R^2 < F$ | **Lower ray + window** $(1,0,1)$; at $R^2 = m$ the minimum point splits them |
| $F \le R^2 < M$ | Window |
| $R^2 \ge M$ | Empty |

**Case $M \le F$** ($c\lambda/(4\Sigma) \le \Pi_0 < \Pi_0^{\text{pair}}$):

| Tolerance | Class |
|---|---|
| $R^2 \le H$ | All |
| $H < R^2 < m$ | Lower ray |
| $m \le R^2 < M$ | **Lower ray + window** $(1,0,1)$ |
| $M \le R^2 < F$ | Lower ray |
| $R^2 \ge F$ | Empty |

**Without the pair** ($\Pi_0 \ge \Pi_0^{\text{pair}}$):
- $R^2 \le H$: All;
- $H < R^2 < F$: lower ray;
- $R^2 \ge F$: Empty.

**Label:** Proposition (proved, from Theorem 1.2 and Proposition 3.9). Task 10: 4,868 two-turning-point sets, 77,888 tolerances, zero mismatches.

**Answer to adversarial question 2.** A mixed class occurs in a natural gain family. It is practically narrow:
- band width $(\min(M,F) - m)/F$ has median $5\times10^{-4}$, ranging from $4\times10^{-22}$ to $0.96$;
- in 16% of sets the mixed band exists without any window above $F$.

**Conjecture 3.10 (Hill, every $n > 1$).** $\sigma^2$ has either no turning point or exactly a minimum followed by a maximum, and there is a single pair-birth value $\Pi_0^{\text{pair}}(n)$.

**Label:** Numerical result + Conjecture.
- Task 10 tested $n \in \{1.5, 2, 3, 4, 8\}$, 10,000 sets, with zero sets having 1, 3 or ≥ 4 turning points.
- There was exactly one transition per $n$: $\Pi_0^{\text{pair}} = 30.243, 31.475, 37.820, 44.180, 62.711$ at $\lambda = c = 1$, $\Sigma = 0.01$.
- The $n = 2$ proof route ($Q = c\,t\,P - 4\Sigma\Pi_0(\ldots)$, then unimodality of the ratio) is the natural attack for general $n$.

### 4.6 Two-stage gains (exploratory)

Sums of two widely separated natural stages produce more than one maximum:
- two-channel Bayesian: 7 of 2,000 sets, sequence (max, min, max), i.e. **multi-window**;
- two-channel Hill: 63 of 2,000 sets, sequence (min, max, min, max), i.e. **mixed multi-window**.

**Label:** Numerical result. Multi-window failure sets need no constructed gain: two natural stages suffice.

### 4.7 Fixed α–β filter

The α–β filter is a two-state filter, so it does not fit the scalar model. It moves to Stage 6.

---

## 5. Degeneracies (adversarial questions 3 and 4)

**Corollary 3.11 (equal-height maxima).** Suppose two interior maxima share the value $M_2$ and are separated by a lower minimum. Then:
- just below $M_2$, $k$ counts both;
- at and above $M_2$, both windows are gone, so $k$ drops by 2 at a single tolerance.

The class is otherwise unaffected.

*Proof.* Theorem 1.2(c),(d). $\square$

**Label:** Corollary (proved; T10.5: $k = 2$ just below, Empty at and above, both routes). Families with at most one maximum (Sections 4.1–4.5) cannot produce this.

**Corollary 3.12 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a flat-topped maximum acts as a maximum.

*Proof.* By Theorem 1.2(d), the class depends only on the ordered turning-point values, the endpoint limits and the approach directions. $\square$

**Answer to question 4:** no.

**Label:** Corollary (proved; T10.5: 1,000 tolerances, identical classes with and without the inflection).

**Theorem 3.13 (plateaus; extension of Theorem 1.2).** Replace C2 by C2′: $\sigma^2$ is continuous, and $D$ splits into finitely many pieces, each strictly monotone or constant. Then Theorem 1.2 holds with these changes:
- plateau values join the critical tolerances;
- at $R^2$ equal to a plateau value, that plateau is excluded from the failure set, which can split or remove components;
- an end adjacent to a plateau at value $L$ carries a ray iff $R^2 < L$.

*Proof.* As for Theorem 1.2(a)–(b). On a constant piece of value $p$, the piece's contribution is all of the piece if $R^2 < p$ and empty otherwise, and this is constant on each interval avoiding $p$. $\square$

**Label:** Theorem (proved).

**Natural instance.** Capped gain at $g = 2F$:
- lower ray for $R^2 < F$, extending past the kink $c/g$;
- Empty at $R^2 = F$ and above.

By the excess identity, a plateau at $F$ occurs exactly where $G = 2F\Pi$ on an interval.

**Proposition 3.14 (pair birth).** Suppose a minimum–maximum pair is born at a parameter value $\theta_0$ through a nondegenerate fold of $N$. Then at distance $\delta$ from $\theta_0$:
- the turning-point positions separate like $\delta^{1/2}$;
- the values separate like $M - m \sim \delta^{3/2}$.

So the band of tolerances that sees the pair opens continuously from zero width.

*Proof.* Near the fold, $d\sigma^2/d\Pi \approx a(x^2 - b\delta)$ in a local coordinate $x$. Its roots are $\pm\sqrt{b\delta}$, and the value change between them is $\tfrac43 a (b\delta)^{3/2}$. $\square$

**Label:** Proposition (proved under nondegeneracy). Task 10, Hill $n = 2$: fitted exponents $1.50007$ for values and $0.50002$ for positions. The pre-registered exponent window $[0.4, 0.6]$ applied to the wrong quantity (Section 8).

**Narrow windows.**
- Windows of relative width $10^{-8}$ were found by the root-finding classifier in 20/20 curves (55 windows).
- A $10^4$-point log grid found none of them.

This justifies the roadmap's "root-finding, not grids" rule.

---

## 6. The optimal filter can produce a window (adversarial question 6)

**Setting.** Sensory noise is Ornstein–Uhlenbeck with **fixed variance** $v$ and correlation time $\tau \in (0, \infty)$, i.e. $C_\eta(u) = v e^{-|u|/\tau}$: a sensor of fixed noise level and varying bandwidth. Stage 2 used matched zero-frequency power instead.

**Proposition 6.1.** Measurement differencing ($z = \dot y + y/\tau$, as in Stage 2) gives the optimal stationary error as the positive root of
$$
A(\tau)\,P^2 + B\,P - C = 0,
\qquad
A = \frac{(1-\lambda\tau)^2}{\tau},\quad B = 4(\Sigma + \lambda v),\quad C = 4\Sigma v,
$$
that is, $P = 2C/(B + \sqrt{B^2 + 4AC})$. Consequently:
1. $P$ is strictly decreasing in $A$. Since $A$ decreases on $(0, 1/\lambda)$ and increases after, $P$ is **unimodal** with its maximum at $\tau = 1/\lambda$:
$$
P_{\max} = \frac{\Sigma v}{\Sigma + \lambda v}.
$$
2. $A(\tau) = A(1/(\lambda^2\tau))$, so $P$ is symmetric in $\log\tau$ about $1/\lambda$.
3. $P \sim 2\sqrt{\Sigma v\tau}$ as $\tau \to 0$ and $P \sim (2/\lambda)\sqrt{\Sigma v/\tau}$ as $\tau \to \infty$. Both limits are $0$, approached from above.
4. **Classification.**
   - For $0 < R^2 < P_{\max}$, the failure set is a **window** $(\tau_-, \tau_+)$ with
$$
\tau_\pm = \frac{(2\lambda + A_R) \pm \sqrt{A_R(4\lambda + A_R)}}{2\lambda^2},
\qquad
A_R = \frac{C - BR^2}{R^4},
\qquad
\tau_-\tau_+ = \frac{1}{\lambda^2}.
$$
   - For $R^2 \ge P_{\max}$ the failure set is Empty.

*Proof.* The correlated-noise Riccati equation of Stage 2 holds with $w_\eta$ of intensity $2v/\tau$, so $R_v = 2\Sigma + 2v/\tau$. Multiplying by $-\tau R_v$ gives the quadratic. Its constant term is negative and $B > 0$, so there is one positive root, decreasing in $A \ge 0$. Items 1–3 follow from the shape of $A$. For item 4, set $P = R^2$ and solve for $A$, then solve $\lambda^2\tau^2 - (2\lambda + A_R)\tau + 1 = 0$. $\square$

**Label:** Proposition (proved). Task 10 evidence:
- three independent routes (quadratic, mpmath regularized ARE with per-set scaled $\varepsilon$, closed-form causal Wiener filter) agree to $1.0\times10^{-14}$ on 4,000 evaluations;
- shape, symmetry and window endpoints are exact to $10^{-50}$;
- Monte Carlo $|z| \le 1.39$.

**Relay along the same sweep** (fixed $G$, $a = \lambda + G$):
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2 v\tau}{1 + a\tau}\right),
$$
strictly increasing from $H_G$ to $(\Sigma + G^2 v/a)/a$, and $\ge P$ throughout.
- $R^2 \le H_G$: All;
- $H_G < R^2 <$ top: upper ray;
- $R^2 \ge$ top: Empty.

**Label:** Proposition (proved; T10.6).

**Counterexample (analytic) to the unrestricted claim "the optimal filter never produces a window".** Paper 1's statement holds along precision sweeps, and Stage 2 showed it along $\tau$ at matched zero-frequency power. Proposition 6.1 shows it fails along $\tau$ at matched variance.

**Consequence for Stage 4.** If observations are Blackwell-ordered along a sweep, the optimal mean-square error is monotone along it. A non-monotone $P$ therefore means this family is **not** an information ordering, so the Stage 4 conjecture stands. But the result shows its hypothesis is **necessary**: without information ordering, optimal filters do produce windows. Stage 4's question becomes whether information ordering is *exactly* the right condition.

Note on the two colour normalizations: the same physical change (narrowing noise bandwidth) gives a monotone optimal filter at matched zero-frequency power and a windowed one at matched variance. The choice of normalization is a modelling decision with topological consequences, and Paper 2 should say so.

---

## 7. Answers to the six adversarial questions (Roadmap Section 7)

| # | Question | Answer | Result | Label |
|---|---|---|---|---|
| 1 | Three or more separated windows from a continuous gain? | Yes, any $k$, even smooth and Paper-1-regular; also from two natural stages | Cor. 3.4; §4.6 | Corollary; Numerical result |
| 2 | Mixed class in a natural family? | Yes: Hill gain, lower ray + window, in a narrow band | Prop. 3.9 | Proposition |
| 3 | Equal-height extrema change the class? | Only at that tolerance, where $k$ drops by 2 | Cor. 3.11 | Corollary |
| 4 | Degenerate stationary point changes the class without changing extrema? | No | Cor. 3.12 | Corollary |
| 5 | Numerical search finds an unpredicted class? | No: $10^6$ classifications, 3 float64 flags, 0 persisting at 60 digits | T10.7 | Numerical result |
| 6 | Optimal filter non-monotone along a non-information sweep? | Yes: matched-variance $\tau$, window for the optimal filter | Prop. 6.1 | Proposition + Counterexample |

**Completeness status of the model classification (Roadmap Section 4, definition B).**
- Complete, with every class at every tolerance determined and impossibilities proved, for:
  - Bayesian-weight along $\Pi$, $\Pi_0$ and $c$;
  - misspecified Kalman, capped and precision-blind along $\Pi$;
  - Hill $n = 2$ along $\Pi$;
  - relay and optimal filter along both $\tau$ normalizations;
  - arbitrary continuous gains along $\Pi$ (Corollary 3.3).
- Conditional on Conjecture 3.10: Hill $n \ne 2$.
- Exploratory: two-stage gains.

---

## 8. Verification (Task 10)

Pre-registration `classification/PREREG_t10.md`, commit `da3d826`; results at commit `cbe96fe`; 5,861 s on 4 CPUs. **Six checks pass. Four fail: two on a pre-registered criterion I mis-set, one on SymPy's route, and one on the plan's own construction.** All four stay recorded as failures.

| Check | Verdict | Result |
|---|---|---|
| T10.1 Symbolic | **FAIL** | 24/26 reduce by the fixed route. The other two (misspecified-Kalman inverse; forced ray) need $\sqrt{x^2} = x$ under sign conditions positive-symbol assumptions cannot express; both reduce to 0 once factored. Route limitation; identities correct. |
| T10.2 Realizability, every class | PASS | 101/101 targets realized; 24/24 forbidden targets blocked |
| T10.2 A1.3 as specified | **FAIL** | $k$ windows in all five cases, but $G_+$ diverges as $\Pi \to \infty$. **Plan error**, corrected in Corollary 3.4 |
| T10.2 A1.3 supplementary (branch switch) | PASS | all five; $G(10^{12})/G(10^{11}) - 1 = 6\times10^{-10}$ |
| T10.3 Census | PASS | 18,000 sets; Bayesian, misspecified Kalman, capped, precision-blind and Hill histograms exactly as predicted; positions to $6\times10^{-31}$ |
| T10.4 Hill mixed class | PASS | 4,868 sets, 77,888 tolerances, 0 mismatches |
| T10.5 Degeneracies | **FAIL** | Four sub-checks pass. Pair-birth exponent 1.500 vs pre-registered $[0.4, 0.6]$: **criterion error**, since that window applies to positions (measured 0.500), not to $M - m$ |
| T10.6 Matched-variance $\tau$ | **FAIL** | Routes, classes, relay, Monte Carlo and regression all pass. The shape check's zero-limit threshold ($10^{-6}P_{\max}$ at $\lambda\tau = 10^{\mp12}$) was mis-set; the asymptote gives $4\times10^{-6}$. **Criterion error.** The supplementary check at $10^{\mp24}$ passes 1000/1000 |
| T10.7 Blind search | PASS | $10^6$ classifications; 0 classes outside the predicted sets; 0 route disagreements |

**Corrections from Task 10:**
1. Corollary 3.4's construction switches to the lower branch (plan error).
2. "Hill sextic" in the plan: $Q$ is a quintic, and $tQ$ is the sextic.
3. Lemma 3.7 holds for any differentiable $G > 0$; monotonicity is needed only to reduce to one variable.
4. "Two rays" is removed from the Hill predicted set: it is impossible because $\sigma^2 > H$ everywhere (§4, general fact). This explains why T10.7 never saw it.
5. Two Task 10 prompt criteria were mis-set by me (pair-birth exponent, zero-limit threshold).

No class changed.

**Code bugs** (documented in `RESULTS_t10.md`): an onset-side rounding at $\kappa = 2$, fixed before the full run; a float/decimal mismatch in $F$ for the plateau check, fixed and re-run. Neither changed a verdict on the plan.

**Protocol lessons for Task 11.**
- For a fold, pre-register exponents for positions ($1/2$) and values ($3/2$) separately.
- Derive zero-limit thresholds from the proved asymptote, not by guess.
- Allow SymPy a factor-then-simplify route for radicals of squares, stated in the pre-registration.

**Figures** (`classification/t10/figs/`):
- F1 realizability envelope with a 3-window curve and the forced ray;
- F2 Hill family;
- F3 Hill phase diagram;
- F4 peak heights, Bayesian vs misspecified Kalman;
- F5 matched-variance $\tau$, optimal window and relay.

---

## 9. Synthesis-matrix entries (Stage 3)

| Sweep | Kind | Gain family | Endpoint limits (approach) | Extrema | Critical tolerances | Possible classes | Optimal can produce | Conditions | Label |
|---|---|---|---|---|---|---|---|---|---|
| $\Pi$ | env. | any continuous | free above $\sigma_\star^2$ | any finite number | — | $R^2 < F$: exactly the classes with $\ell = 1$; $R^2 \ge F$: all | lower ray, Empty | — | Thm 3.1, Cor. 3.2–3.4 |
| $\Pi$ | env. | misspecified Kalman | $F$ → $0$ (above) | ≤ 1 max | $F, M$ | lower ray, window, Empty | lower ray, Empty | max iff $F' > 2F$ | Prop. 3.8 |
| $\Pi$ | env. | capped $\min(g\Pi, c)$ | $F$ → $H$ (above) | ≤ 1 max (kink); plateau at $g = 2F$ | $H, F, M$ | All, lower ray, window, Empty | lower ray, Empty | max iff $g > 2F$ | Prop. §4.3, Thm 3.13 |
| $\Pi$ | env. | precision-blind | $\infty$ → $H$ (above) | none | $H$ | All, lower ray | lower ray, Empty | — | Prop. §4.4 |
| $\Pi$ | env. | Hill $n = 2$ | $F$ (below) → $H$ (above) | 0, or min then max | $H, m, M, F$ | All, lower ray, **mixed (1,0,1)**, window, Empty; never two rays | lower ray, Empty | pair iff $\Pi_0 < \Pi_0^{\text{pair}}$; window iff $\Pi_0 < c\lambda/(4\Sigma)$ | Prop. 3.9 |
| $\Pi$ | env. | Hill $n \ne 2$ | as $n = 2$ | conj. 0 or 2 | — | as $n = 2$ | lower ray, Empty | — | Conjecture 3.10 |
| $\Pi$ | env. | two-stage Bayesian / Hill | — | up to 3 / 4 seen | — | multi-window; mixed multi-window | lower ray, Empty | — | Numerical result |
| $\tau$ (matched variance) | env. | any fixed $G > 0$ | $H_G$ (above) → top (below) | none | $H_G$, top | All, upper ray, Empty | — | — | Prop. §6 |
| $\tau$ (matched variance) | env. | optimal | $0$ → $0$ | one max at $1/\lambda$ | $P_{\max}$ | **window**, Empty | window, Empty | — | Prop. 6.1 |

---

## 10. Roadmap updates

1. **Stage 4.**
   - Reframe the question from "is the Blackwell conjecture true?" to "is information ordering exactly the condition for optimal-filter monotonicity?". Proposition 6.1 shows the hypothesis is necessary.
   - Move matched-variance $\tau$ from "open" to "settled: windows".
2. **Section 2 terminology.** "Windows need loose tolerances" is now a theorem for every gain schedule (Corollary 3.2).
3. **Section 6.3.** α–β moves to Stage 6.
4. **Stage 5.** The Hill mixed band (median relative width $5\times10^{-4}$) and the misspecified-Kalman peak ratio (1.89) are ready-made relevance inputs.
5. **Open, carried forward:**
   - Conjecture 3.10 (Hill, general $n$);
   - turning-point bounds for two-stage gains;
   - the $\Delta t$ and $\Sigma$ sweeps (Stage 2).
