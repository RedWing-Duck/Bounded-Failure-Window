# Stages 0 and 1: Conventions, the Critical-Tolerance Theorem, and the Two Design Sweeps

**John Holder** · Working results for Paper 2 · 7 October 2026

Companion to *Roadmap v2*. Section and stage numbers refer to that roadmap. Every result carries a label (Roadmap Section 12). Notation follows Paper 1: $\lambda, \Sigma > 0$, floor $F = \Sigma/\lambda$, and for a gain $G \ge 0$ at precision $\Pi > 0$,

$$
\sigma^2(G, \Pi) = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}.
$$

All variances are actual stationary error variances.

---

## 1. Stage 0: Conventions

**C1 (domain).** A swept parameter $\theta$ ranges over an open interval $D = (\theta_-, \theta_+)$, with $-\infty \le \theta_- < \theta_+ \le \infty$. Endpoints never belong to $D$; behaviour there enters only through limits. For $\Pi$, $\Pi_0$ and $c$, $D = (0, \infty)$.

**C2 (regularity).** $\sigma^2$ is continuous on $D$ and **piecewise strictly monotone**: there are finitely many turning points $t_1 < \dots < t_n$ in $D$ with $\sigma^2$ strictly monotone on each piece $I_j = (t_{j-1}, t_j)$, where $t_0 = \theta_-$ and $t_{n+1} = \theta_+$. The endpoint limits $L_\pm = \lim_{\theta \to \theta_\pm} \sigma^2$ exist in $[0, \infty]$. (C2 must be verified for each sweep; it holds for all sweeps in this document.)

**C3 (failure set).** For a tolerance $R^2 > 0$, $\mathcal{F}(R^2) = \{\theta \in D : \sigma^2(\theta) > R^2\}$. The strict inequality makes $\mathcal{F}$ open.

**C4 (approach direction).** At an end, $\sigma^2$ approaches the finite limit $L_\pm$ **from above** if $\sigma^2 > L_\pm$ on the adjacent piece, and **from below** if $\sigma^2 < L_\pm$ there. Because the adjacent piece is strictly monotone (C2), exactly one of the two holds: from above at $\theta_-$ means the first piece is decreasing, and from above at $\theta_+$ means the last piece is increasing.

**C5 (class).** Write $\mathcal{F}(R^2)$ as a disjoint union of its connected components (open intervals). Its **class** is the triple $(\ell, u, k)$:
- $\ell = 1$ if some component contains $(\theta_-, \theta_- + \varepsilon)$ for some $\varepsilon > 0$ (a **lower ray**), else $0$;
- $u = 1$ if some component contains $(\theta_+ - \varepsilon, \theta_+)$ (an **upper ray**), else $0$;
- $k$ = the number of components bounded away from both ends (**windows**).

When $\ell = u = 1$ and the lower and upper rays are the same component, $\mathcal{F} = D$ and the class is written **All**. Named classes:

| Name | Class |
|---|---|
| Empty | $(0, 0, 0)$ |
| All | $\mathcal{F} = D$ |
| Lower ray (threshold) | $(1, 0, 0)$ |
| Upper ray | $(0, 1, 0)$ |
| Two rays | $(1, 1, 0)$, $\mathcal{F} \ne D$ |
| Window | $(0, 0, 1)$ |
| Multi-window | $(0, 0, k)$, $k \ge 2$ |
| Mixed | any class with $k \ge 1$ and $\ell + u \ge 1$ |

**C6 (critical tolerances).** $\mathcal{C} = \{L_-, L_+\} \cup \{\sigma^2(t_1), \dots, \sigma^2(t_n)\}$, keeping only finite values.

---

## 2. Stage 1: General results

**Proposition 1.1 (realizability; Topological classification A).** For every $\ell, u \in \{0,1\}$ and every finite $k \ge 0$, there is a continuous piecewise strictly monotone function on $(0,\infty)$ and a tolerance whose failure set has class $(\ell, u, k)$; All is realized as well. Classes with $k = \infty$ require infinitely many turning points and are excluded by C2.

*Proof.* Take a piecewise-linear zigzag with $k$ interior peaks of height 2 separated by troughs of height 0, preceded by a segment starting at height 2 (if $\ell = 1$) or 0 (if $\ell = 0$), and similarly at the upper end; set $R^2 = 1$. All: any function bounded below by 2, with $R^2 = 1$. $\square$

*Consequence:* topological classification alone excludes nothing. All restrictions in this program come from the filtering model (Classification B).

**Theorem 1.2 (critical-tolerance theorem).** Assume C1–C6.

(a) *Local constancy.* The class of $\mathcal{F}(R^2)$ is constant on each connected component of $(0, \infty) \setminus \mathcal{C}$. It can change only when $R^2$ crosses or equals a critical tolerance.

(b) *Rays.* $\ell = 1$ if $R^2 < L_-$ and $\ell = 0$ if $R^2 > L_-$. If $R^2 = L_-$, then $\ell = 1$ iff $\sigma^2$ approaches $L_-$ from above. The same holds for $u$ with $L_+$.

(c) *Windows.* Each window contains an interior local maximum $t_j$ with $\sigma^2(t_j) > R^2$, and distinct windows contain distinct maxima. Hence
$$
k \le \#\{\text{interior local maxima } t_j : \sigma^2(t_j) > R^2\},
$$
with equality iff each such maximum lies in a component that touches neither end and contains no other such maximum.

(d) *Determining data.* The class of $\mathcal{F}(R^2)$, for every $R^2$, is determined by the ordered sequence
$$
(L_-,\ \sigma^2(t_1),\ \dots,\ \sigma^2(t_n),\ L_+)
$$
together with the approach directions at the two ends. The locations $t_j$ are not needed for the class; they are needed only to locate the components.

*Proof.*
(a) On each piece $I_j$, $\sigma^2$ is a strictly monotone continuous bijection onto the open interval between its end values $a_j$ and $b_j$ (turning-point values or endpoint limits, all in $\mathcal{C}$ or infinite). For $R^2 \notin \mathcal{C}$, the set $\{\sigma^2 > R^2\} \cap I_j$ is empty, all of $I_j$, or a one-sided subinterval adjacent to the larger end, and which of the three is decided by the position of $R^2$ relative to $a_j$ and $b_j$. That pattern is the same for all $R^2$ in one component of $(0,\infty) \setminus \mathcal{C}$. Two adjacent pieces' contributions join into one component exactly when $\sigma^2(t_j) > R^2$, which is also constant there. So the components, their number, and which ones touch the ends are all constant.
(b) Near $\theta_-$, $\sigma^2$ is close to $L_-$. If $R^2 < L_-$ it exceeds $R^2$ on some $(\theta_-, \theta_- + \varepsilon)$; if $R^2 > L_-$ it does not. If $R^2 = L_-$, the first piece is strictly monotone, so $\sigma^2 > L_-$ throughout it iff it approaches from above, and $\sigma^2 < L_-$ throughout it otherwise.
(c) A window is $(a, b)$ with $a, b \in D$. By continuity and maximality, $\sigma^2(a) = \sigma^2(b) = R^2$ and $\sigma^2 > R^2$ on $(a,b)$, so $\sigma^2$ attains a maximum on $[a,b]$ at an interior point, which is a turning point with value $> R^2$. Distinct windows are disjoint, so they contain distinct maxima. The equality condition restates when the map from windows to such maxima is onto.
(d) Follows from (a)–(c): the construction in (a) uses only the end values of each piece, i.e. the ordered sequence, and (b) adds the approach directions. $\square$

**Label:** Proposition 1.1, Theorem 1.2 — analytically proved.

**Check against Paper 1.** For the precision sweep with the Bayesian-weight gain and $\kappa > 2$: sequence $(F, M, H)$, approach from above at $\Pi \to 0$ and from above at $\Pi \to \infty$. Theorem 1.2 gives: All for $R^2 \le H$; lower ray for $H < R^2 \le F$; window for $F < R^2 < M$; Empty for $R^2 \ge M$. This is Paper 1's four-regime corollary, including its equality cases.

---

## 3. The gain lemma

**Lemma 3.1 (single minimum in $G$).** Fix $\Pi > 0$. On $G \in [0, \infty)$,
$$
\frac{\partial \sigma^2}{\partial G} = \frac{G^2 + 2\lambda G - 2\Sigma\Pi}{2\Pi(\lambda + G)^2}.
$$
The numerator has exactly one positive root,
$$
G^\star(\Pi) = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
$$
so $\sigma^2(\cdot, \Pi)$ is strictly decreasing on $[0, G^\star]$ and strictly increasing on $[G^\star, \infty)$. Its minimum value is $\sigma_\star^2(\Pi) = G^\star/\Pi < F$. Moreover $\sigma^2(0,\Pi) = F$, $\sigma^2(G,\Pi) \to \infty$ as $G \to \infty$, and
$$
\sigma^2(G, \Pi) \le F \iff 0 \le G \le 2F\Pi,
$$
with equality to $F$ exactly at $G = 0$ and $G = 2F\Pi$.

*Proof.* Quotient rule: the numerator of $\partial_G\sigma^2$ is $\tfrac{G}{\Pi}(\lambda + G) - \Sigma - \tfrac{G^2}{2\Pi} = \tfrac{1}{2\Pi}(G^2 + 2\lambda G - 2\Sigma\Pi)$. The quadratic has roots $-\lambda \pm \sqrt{\lambda^2 + 2\Sigma\Pi}$, one negative and one positive; it is negative between them and positive beyond. At the root, $G^2 + 2\lambda G = 2\Sigma\Pi$ gives $\sigma^2 = G^\star/\Pi$, and $G^\star/\Pi < F$ because $\sqrt{\lambda^2 + 2\Sigma\Pi} > \lambda$ implies $2\Sigma/(\lambda + \sqrt{\cdot}) < \Sigma/\lambda$. The last statement is the excess identity of Paper 1. As $G \to \infty$, $\sigma^2 \sim G/(2\Pi)$. $\square$

**Label:** Proposition (proved). This is the steady-state Kalman–Bucy gain of Paper 1, now shown to be the unique minimizer with strict monotonicity on each side.

**Theorem 3.2 (monotone gain sweeps cannot window).** Fix $\Pi$. Let $\theta \mapsto G(\theta)$ be continuous and strictly monotone on $D$. Then $\sigma^2(G(\theta), \Pi)$ is strictly monotone or strictly decreasing-then-increasing on $D$. Its sublevel sets $\{\sigma^2 \le R^2\}$ are intervals, so every failure set is Empty, All, a lower ray, an upper ray, or two rays. **No window and no mixed class can occur.**

*Proof.* Composition of Lemma 3.1's strictly decreasing-then-increasing function with a strictly monotone map is strictly monotone or strictly decreasing-then-increasing (a single interior minimum at most). Such a function is strictly quasiconvex, so its sublevel sets are intervals (possibly a point or empty). The complement of an interval in an open interval is at most two rays. $\square$

**Label:** Theorem (proved). Both design sweeps below are instances. Windows in Paper 1 arise precisely because sweeping $\Pi$ moves both $G$ and the curve $\sigma^2(\cdot, \Pi)$ itself.

---

## 4. Prior-precision sweep ($\theta = \Pi_0$, design sweep)

**Setting.** Fixed $\Pi > 0$, $c > 0$; $G(\Pi_0) = c\Pi/(\Pi + \Pi_0)$, strictly decreasing from $c$ (as $\Pi_0 \to 0$) to $0$ (as $\Pi_0 \to \infty$). Write $G^\star = G^\star(\Pi)$, $\sigma_\star^2 = G^\star/\Pi$, and
$$
V_c = \sigma^2(c, \Pi) = \frac{\Sigma + c^2/(2\Pi)}{\lambda + c}.
$$

**Proposition 4.1 (endpoints and extrema).**
- $L_- = V_c$ (as $\Pi_0 \to 0$) and $L_+ = F$ (as $\Pi_0 \to \infty$). The approach to $F$ is always **from below**.
- If $c \le G^\star$: $\sigma^2$ is strictly increasing in $\Pi_0$, from $V_c$ (approached from above) to $F$. No interior extremum.
- If $c > G^\star$: $\sigma^2$ has exactly one interior extremum, a global minimum, at
$$
\Pi_0^\star = \Pi\left(\frac{c}{G^\star} - 1\right),
$$
with value $\sigma_\star^2(\Pi)$, the optimal variance at that precision. The approach to $V_c$ is then from below.
- $V_c > F \iff c > 2F\Pi$, and $V_c = F \iff c = 2F\Pi$.
- In terms of $\Pi$: $c > G^\star \iff \Pi < \Pi_A := \dfrac{c(c + 2\lambda)}{2\Sigma}$, and $c > 2F\Pi \iff \Pi < \Pi_B := \dfrac{c}{2F} = \dfrac{c\lambda}{2\Sigma}$, with $\Pi_B < \Pi_A$.

*Proof.* Compose Lemma 3.1 with the strictly decreasing map $\Pi_0 \mapsto G$. The gain passes through $G^\star$ iff $c > G^\star$, at $c\Pi/(\Pi + \Pi_0) = G^\star$, which solves to $\Pi_0^\star$. Near $\Pi_0 = \infty$, $G \to 0^+$ and $\sigma^2$ is decreasing in $G$, so increasing in $\Pi_0$: approach to $F$ from below. Near $\Pi_0 = 0$, $G \to c^-$; if $c > G^\star$, $\sigma^2$ is increasing in $G$ there, so decreasing in $\Pi_0$ (approach to $V_c$ from below); if $c \le G^\star$, the opposite. $V_c$ versus $F$ is Lemma 3.1 at $G = c$. $c > G^\star \iff c^2 + 2\lambda c > 2\Sigma\Pi$. $\Pi_B < \Pi_A$ since $c\lambda < c(c + 2\lambda)$. $\square$

**Interpretation.** The minimum over the prior is exactly the optimal filter's variance: the best fixed prior at this precision reproduces the Kalman–Bucy gain. Both misweighting directions (prior too weak, prior too strong) are worse.

**Proposition 4.2 (complete classification, every tolerance).** Three cases, by $\Pi$.

*Case P1: $\Pi \ge \Pi_A$ (equivalently $c \le G^\star$).* Sequence $(V_c, F)$; $\sigma^2$ increases strictly from $V_c$ to $F$, attaining neither.

| Tolerance | Class |
|---|---|
| $R^2 \le V_c$ | All |
| $V_c < R^2 < F$ | Upper ray |
| $R^2 \ge F$ | Empty |

*Case P2: $\Pi_B \le \Pi < \Pi_A$ (equivalently $G^\star < c \le 2F\Pi$).* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < V_c \le F$.

| Tolerance | Class |
|---|---|
| $R^2 < \sigma_\star^2$ | All |
| $R^2 = \sigma_\star^2$ | Two rays (domain minus the single point $\Pi_0^\star$) |
| $\sigma_\star^2 < R^2 < V_c$ | Two rays |
| $V_c \le R^2 < F$ | Upper ray |
| $R^2 \ge F$ | Empty |

(At $\Pi = \Pi_B$, $V_c = F$ and the upper-ray row is empty.)

*Case P3: $\Pi < \Pi_B$ (equivalently $c > 2F\Pi$).* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < F < V_c$.

| Tolerance | Class |
|---|---|
| $R^2 < \sigma_\star^2$ | All |
| $R^2 = \sigma_\star^2$ | Two rays (domain minus $\Pi_0^\star$) |
| $\sigma_\star^2 < R^2 < F$ | Two rays |
| $F \le R^2 < V_c$ | Lower ray |
| $R^2 \ge V_c$ | Empty |

*Proof.* Theorem 1.2 applied to Proposition 4.1. Equality rows use the approach directions: $F$ is approached from below, so $R^2 = F$ never gives an upper ray; $V_c$ is approached from above in P1 (so $R^2 = V_c$ gives All) and from below in P2–P3 (so $R^2 = V_c$ gives no lower ray). At $R^2 = \sigma_\star^2$ the minimum value is attained only at $\Pi_0^\star$. $\square$

**Label:** Propositions 4.1–4.2 — proved. The roadmap's numerical lead (U-shape, two rays) is now a proposition, and it holds only for $\Pi < \Pi_A$; for $\Pi \ge \Pi_A$ the sweep is monotone.

**Worked example** ($\lambda = c = 1$, $\Sigma = 0.01$): $\Pi_B = 50$, $\Pi_A = 150$.
- $\Pi = 1$ (P3): $G^\star = 0.0099504$, $\Pi_0^\star = 99.498$, $\sigma_\star^2 = 0.0099504$, $V_c = 0.255$.
- $\Pi = 60$ (P2): $\Pi_0^\star = 64.162$, $\sigma_\star^2 = 0.0080540$, $V_c = 0.0091667$.
- $\Pi = 500$ (P1): monotone from $V_c = 0.0055$ to $F$.

---

## 5. Coupling sweep ($\theta = c$, design sweep)

**Setting.** Fixed $\Pi, \Pi_0 > 0$; $K = \Pi/(\Pi + \Pi_0) \in (0,1)$ and $G = cK$, strictly increasing from $0$ to $\infty$.

**Proposition 5.1 (endpoints and extrema).**
- $L_- = F$, approached **from below**; $L_+ = \infty$.
- Exactly one interior extremum, a global minimum, at
$$
c^\star = \frac{G^\star(\Pi)}{K} = \frac{(\Pi + \Pi_0)\left(\sqrt{\lambda^2 + 2\Sigma\Pi} - \lambda\right)}{\Pi},
$$
with value $\sigma_\star^2(\Pi)$.
- $\sigma^2 = F$ again at $c_F = 2F\Pi/K = 2F(\Pi + \Pi_0)$; $\sigma^2 > F$ iff $c > c_F$.

*Proof.* Lemma 3.1 composed with the strictly increasing map $c \mapsto cK$, which always passes through $G^\star$ and $2F\Pi$. $\square$

**Proposition 5.2 (complete classification, every tolerance).** No case split.

| Tolerance | Class |
|---|---|
| $R^2 < \sigma_\star^2$ | All |
| $R^2 = \sigma_\star^2$ | Two rays (domain minus $c^\star$) |
| $\sigma_\star^2 < R^2 < F$ | Two rays |
| $R^2 \ge F$ | Upper ray, $(c_R, \infty)$ with $c_R \ge c_F$ |

The class is never Empty, since $\sigma^2 \to \infty$ as $c \to \infty$. At $R^2 = F$ the upper ray is exactly $(c_F, \infty)$.

*Proof.* Theorem 1.2 with sequence $(F, \sigma_\star^2, \infty)$ and approach to $F$ from below. $\square$

**Label:** Propositions 5.1–5.2 — proved.

**Worked example** ($\lambda = 1$, $\Sigma = 0.01$, $\Pi = \Pi_0 = 1$): $c^\star = 0.019901$, $\sigma_\star^2 = 0.0099504$, $c_F = 0.04$.

---

## 6. Synthesis-matrix entries

| Sweep | Kind | Gain family | Endpoint limits (approach) | Extrema | Critical tolerances | Possible classes | Label |
|---|---|---|---|---|---|---|---|
| $\Pi_0$, $\Pi \ge \Pi_A$ | design | Bayesian-weight | $V_c$ (above) → $F$ (below) | none | $V_c, F$ | All, upper ray, Empty | Proposition |
| $\Pi_0$, $\Pi_B \le \Pi < \Pi_A$ | design | Bayesian-weight | $V_c$ (below) → $F$ (below) | one min, $\sigma_\star^2$ | $\sigma_\star^2, V_c, F$ | All, two rays, upper ray, Empty | Proposition |
| $\Pi_0$, $\Pi < \Pi_B$ | design | Bayesian-weight | $V_c$ (below) → $F$ (below) | one min, $\sigma_\star^2$ | $\sigma_\star^2, F, V_c$ | All, two rays, lower ray, Empty | Proposition |
| $c$ | design | Bayesian-weight | $F$ (below) → $\infty$ | one min, $\sigma_\star^2$ | $\sigma_\star^2, F$ | All, two rays, upper ray | Proposition |
| any monotone gain sweep at fixed $\Pi$ | design | any | — | ≤ 1 min | — | no window, no mixed class | Theorem 3.2 |

**What Stages 0–1 established.**
1. Topology alone permits every class (Prop. 1.1); all restrictions come from the model.
2. The class at every tolerance is fixed by the ordered extremum values and endpoint limits with approach directions (Thm. 1.2).
3. A sweep that moves the gain monotonically at fixed precision can never produce a window (Thm. 3.2). Windows require sweeps that move the variance curve itself, as precision does.
4. The best value of either design parameter recovers exactly the Kalman–Bucy variance at that precision.

**Open items passed to later stages.**
- Stage 2: environment sweeps ($\tau$, $\Delta t$, $\Sigma$), where Theorem 3.2 does not apply.
- Stage 3: a natural (non-constructed) gain family producing a mixed class or multi-window along a precision sweep.
- Stage 4: whether the optimal filter is monotone along every environment sweep that is an information ordering.
