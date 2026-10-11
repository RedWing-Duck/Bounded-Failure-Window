# Failure-Set Topology in Stationary Linear Filters: Stages 0–4, Consolidated

**John Holder** · Source document for Paper 2 · consolidated by Task 13 · October 2026

This document replaces the six stage documents (`Stage_0_1_Classification_Results.md`, `Stage_2_Tau_Sweep_Results.md`,
`Stage_3_Falsification_Results.md`, `Stage_4_Optimality_Results.md`, `Stage_2_Completion_Results.md`, and the Stage 3
plan) as the single source for Paper 2. It follows Roadmap v2 (Stages 0–4) and is self-contained. Every result carries
one number from a single sequence and exactly one Roadmap Section 12 label; the label line cites the verifying task(s).
Section 12 lists every result with its label and verification; the change log in Section 13 maps every old number to its
new one and records every correction.

---

## 1. Notation and conventions

**Model.** A scalar Ornstein–Uhlenbeck signal $s$ ($\dot s = -\lambda s + w_s$, $w_s$ white of intensity $2\Sigma$) is
corrected toward a noisy observation with a gain $G \ge 0$ that is constant in time. The error $x$ of the constant-gain
filter (the **relay**) obeys
$$
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\text{sim}},
$$
with $\xi_s$ white sensory noise of intensity $1/\Pi$ (precision $\Pi > 0$) and $\xi_{\text{sim}}$ of intensity $2\Sigma$.
All variances are **actual** stationary error variances, never filter-reported ones. The stationary variance is
$$
\sigma^2(G, \Pi) = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}.
$$

**Reference quantities.**
- Floor (no correction): $F = \Sigma/\lambda$.
- Optimal (Kalman–Bucy) gain $G^\star(\Pi) = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}$ and optimal variance
  $\sigma_\star^2(\Pi) = G^\star/\Pi = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})$.
- High-precision limit $H = \Sigma/(\lambda + G_\infty)$ for a gain with $G \to G_\infty$ as $\Pi \to \infty$.
- $u = 2\Sigma\Pi/\lambda^2$ and $g = G/\lambda$ (Sections 6–7). The class letter $u$ and the variable $u$ are
  distinguished by context.

"Excess" means error above the no-correction floor $F$, not above the optimal (Wiener) error as in adaptive filtering.
"Relay" means the constant-gain filter, not relay (on–off) feedback.

**C1 (domain).** A swept parameter $\theta$ ranges over an open interval $D = (\theta_-, \theta_+)$,
$-\infty \le \theta_- < \theta_+ \le \infty$. Endpoints never belong to $D$; behaviour there enters only through limits.

**C2 (regularity).** $\sigma^2$ is continuous on $D$ and **piecewise strictly monotone**: there are finitely many turning
points $t_1 < \dots < t_n$ in $D$, with $\sigma^2$ strictly monotone on each piece $I_j = (t_{j-1}, t_j)$ ($t_0 = \theta_-$,
$t_{n+1} = \theta_+$). The endpoint limits $L_\pm = \lim_{\theta \to \theta_\pm}\sigma^2$ exist in $[0, \infty]$.

**C2′ (plateaus).** As C2, but each piece may be strictly monotone or constant.

**C3 (failure set).** For a tolerance $R^2 > 0$, $\mathcal F(R^2) = \{\theta \in D : \sigma^2(\theta) > R^2\}$. The strict
inequality makes $\mathcal F$ open.

**C4 (approach direction).** At an end, $\sigma^2$ approaches the finite limit $L_\pm$ **from above** if $\sigma^2 > L_\pm$
on the adjacent piece and **from below** if $\sigma^2 < L_\pm$ there. Under C2 exactly one holds: from above at $\theta_-$
means the first piece is **increasing**, and from above at $\theta_+$ means the last piece is **decreasing**.

**C5 (class).** Write $\mathcal F(R^2)$ as a disjoint union of open intervals. Its class is the triple $(\ell, u, k)$:
$\ell = 1$ if some component contains $(\theta_-, \theta_- + \varepsilon)$ (a **lower ray**); $u = 1$ if some component
contains $(\theta_+ - \varepsilon, \theta_+)$ (an **upper ray**); $k$ is the number of components bounded away from both
ends (**windows**). If one component is all of $D$ the class is **All**.

| Name | Class |
|---|---|
| Empty | $(0,0,0)$ |
| All | $\mathcal F = D$ |
| Lower ray (threshold) | $(1,0,0)$ |
| Upper ray | $(0,1,0)$ |
| Two rays | $(1,1,0)$, $\mathcal F \ne D$ |
| Window | $(0,0,1)$ |
| Multi-window | $(0,0,k)$, $k \ge 2$ |
| Mixed | $k \ge 1$ and $\ell + u \ge 1$ |

**C6 (critical tolerances).** $\mathcal C = \{L_-, L_+\} \cup \{\sigma^2(t_1), \dots, \sigma^2(t_n)\}$, finite values only
(under C2′, plateau values as well).

**Two kinds of sweep.** Environment sweeps change the world the filter sees ($\Pi$, correlation time $\tau$, $\Sigma$);
design sweeps change the filter ($\Pi_0$, $c$). The sampling interval $\Delta t$ is either.

---

## 2. The critical-tolerance theorem

**Proposition 1 (topological realizability).** For every $\ell, u \in \{0,1\}$ and every finite $k \ge 0$ there is a
continuous piecewise strictly monotone function on $(0,\infty)$ and a tolerance whose failure set has class
$(\ell, u, k)$; All is realized too. Classes with $k = \infty$ need infinitely many turning points and are excluded by C2.

*Proof.* A piecewise-linear zigzag with $k$ interior peaks of height 2 separated by troughs of height 0, preceded by a
segment starting at height 2 (if $\ell = 1$) or 0 (if $\ell = 0$), and likewise at the upper end; $R^2 = 1$. For All, any
function bounded below by 2. $\square$

**Label:** Proposition (proved; T8.5, 21/21 classes).

Reading: topology alone excludes nothing; every restriction below comes from the filtering model.

**Theorem 2 (critical-tolerance theorem).** Assume C1–C6.

(a) *Local constancy.* The class of $\mathcal F(R^2)$ is constant on each connected component of $(0,\infty)\setminus\mathcal C$.

(b) *Rays.* $\ell = 1$ if $R^2 < L_-$ and $\ell = 0$ if $R^2 > L_-$. If $R^2 = L_-$, then $\ell = 1$ iff $\sigma^2$
approaches $L_-$ from above. The same holds for $u$ with $L_+$.

(c) *Windows.* Each window contains an interior local maximum $t_j$ with $\sigma^2(t_j) > R^2$, and distinct windows
contain distinct maxima, so $k \le \#\{\text{interior local maxima with value} > R^2\}$, with equality iff each such
maximum lies in a component that touches neither end and contains no other such maximum.

(d) *Determining data.* The class at every $R^2$ is determined by the ordered sequence
$(L_-, \sigma^2(t_1), \dots, \sigma^2(t_n), L_+)$ and the two approach directions.

*Proof.* (a) On each piece $I_j$, $\sigma^2$ is a strictly monotone continuous bijection onto the open interval between its
end values $a_j, b_j$ (turning-point values or endpoint limits). For $R^2 \notin \mathcal C$, $\{\sigma^2 > R^2\} \cap I_j$
is empty, all of $I_j$, or a one-sided subinterval adjacent to the larger end, decided by the position of $R^2$ relative to
$a_j, b_j$; adjacent contributions join exactly when $\sigma^2(t_j) > R^2$. All of this is constant on a component of
$(0,\infty)\setminus\mathcal C$. (b) Near $\theta_-$, $\sigma^2$ is close to $L_-$; if $R^2 = L_-$ the first piece is strictly
monotone, so $\sigma^2 > L_-$ throughout it iff the approach is from above. (c) A window $(a, b)$ has
$\sigma^2(a) = \sigma^2(b) = R^2$ and $\sigma^2 > R^2$ inside, so $\sigma^2$ has an interior maximum on $[a,b]$, a turning
point with value $> R^2$; disjoint windows contain distinct maxima. (d) The construction in (a) uses only the ordered end
values, and (b) adds the approach directions. At a tolerance equal to an interior turning-point value the same holds: a
minimum with value $R^2$ is excluded from $\mathcal F$ and splits the component around it, and a maximum with value $R^2$
contributes nothing. Under C2 the approach directions are themselves determined by the sequence (the first piece rises iff
$\sigma^2(t_1) > L_-$, or, with no turning point, iff $L_+ > L_-$). $\square$

**Label:** Theorem (proved; T8.1(h), T8.3 62/62 classes; used by every classifier in T9–T13).

Reading: the classification of any sweep reduces to its endpoint limits, approach directions and ordered extremum values.

**Theorem 3 (plateaus).** Under C2′ instead of C2, Theorem 2 holds with three changes: plateau values join the critical
tolerances; at $R^2$ equal to a plateau value the plateau is excluded from $\mathcal F$, which can split or remove
components; an end adjacent to a plateau at value $L$ carries a ray iff $R^2 < L$.

*Proof.* As Theorem 2(a)–(b). A constant piece of value $p$ contributes all of the piece if $R^2 < p$ and nothing otherwise,
which is constant on each interval avoiding $p$. $\square$

**Label:** Theorem (proved; T10.5 plateau check).

**Check against Paper 1.** For the Bayesian-weight gain along $\Pi$ with $\kappa > 2$ (Proposition 8) the sequence is
$(F, M, H)$, approached from above at both ends; Theorem 2 gives All ($R^2 \le H$), lower ray ($H < R^2 \le F$), window
($F < R^2 < M$), Empty ($R^2 \ge M$): Paper 1's four regimes, including the equality cases.

---

## 3. The model along precision

**Corollary 4 (excess identity; Paper 1).**
$$
\sigma^2 - F = \frac{G\big(\lambda G/(2\Pi) - \Sigma\big)}{\lambda(\lambda + G)},
\qquad
\sigma^2 > F \iff G > 2F\Pi.
$$

**Label:** Corollary (proved in Paper 1; T8.1(c)).

Reading: correction injects noise $G^2/(2\Pi)$ and removes variance $\Sigma G/\lambda$; the relay is worse than no
correction exactly when injection exceeds removal.

**Lemma 5 (single minimum in the gain).** Fix $\Pi > 0$. On $G \in [0,\infty)$,
$$
\frac{\partial\sigma^2}{\partial G} = \frac{G^2 + 2\lambda G - 2\Sigma\Pi}{2\Pi(\lambda + G)^2}.
$$
The numerator has exactly one positive root, $G^\star(\Pi)$, so $\sigma^2(\cdot, \Pi)$ is strictly decreasing on
$[0, G^\star]$ and strictly increasing on $[G^\star, \infty)$, with minimum value $\sigma_\star^2(\Pi) = G^\star/\Pi < F$.
Moreover $\sigma^2(0, \Pi) = F$, $\sigma^2 \to \infty$ as $G \to \infty$, and $\sigma^2(G, \Pi) \le F \iff 0 \le G \le 2F\Pi$,
with equality exactly at $G = 0$ and $G = 2F\Pi$.

*Proof.* The numerator of $\partial_G\sigma^2$ is $\tfrac{G}{\Pi}(\lambda + G) - \Sigma - \tfrac{G^2}{2\Pi} =
\tfrac{1}{2\Pi}(G^2 + 2\lambda G - 2\Sigma\Pi)$, with roots $-\lambda \pm \sqrt{\lambda^2 + 2\Sigma\Pi}$, one of each sign.
At the root, $G^2 + 2\lambda G = 2\Sigma\Pi$ gives $\sigma^2 = G^\star/\Pi$, and $G^\star/\Pi < F$ because
$\sqrt{\lambda^2 + 2\Sigma\Pi} > \lambda$. The last statement is Corollary 4. As $G \to \infty$, $\sigma^2 \sim G/(2\Pi)$.
$\square$

**Label:** Lemma (proved; T8.1(a)–(c)).

**Theorem 6 (window theorem; Paper 1).** Assume $G$ is continuous, $G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$, and
$G \to G_\infty \in (0,\infty)$. Then some tolerance fails on a bounded set of precisions away from zero (a window) iff
$\sup_{\Pi > 0} G(\Pi)/\Pi > 2F$; every $R^2 \in (F, \sup\sigma^2)$ then gives a failure set of class $(0,0,k)$ with $k \ge 1$ (a single window when
$\sigma^2$ has one interior maximum, as in Proposition 8; $k > 1$ is possible, Corollary 49). The optimal variance
$\sigma_\star^2(\Pi)$ decreases strictly from $F$ to $0$, so the optimal filter never windows along $\Pi$: its classes are
lower ray ($R^2 < F$) and Empty ($R^2 \ge F$).

**Label:** Theorem (proved in Paper 1 and its verification suite; optimal part re-checked T13 C2 row 1).

**Proposition 7 (no mixed class when $G/\Pi$ decreases).** In the setting of Theorem 6, if moreover $G$ is increasing and $G(\Pi)/\Pi$ is strictly decreasing (e.g. any sum of Bayesian stages
$c_i\Pi/(\Pi + \Pi_{0,i})$), then $\sigma^2$ is strictly decreasing wherever $\sigma^2 \le F$, so every interior minimum exceeds
$F$ and no failure set combines a lower ray with a window: the classes $(1,0,k)$, $k \ge 1$, do not occur.

*Proof.* $2\Pi^2(\lambda + G)^2\,d\sigma^2/d\Pi = \Pi G'(2\lambda G + G^2 - 2\Sigma\Pi) - G^2(\lambda + G)$, and
$\sigma^2 \le F \iff 2\Sigma\Pi \ge \lambda G$. There the bracket is at most $G(\lambda + G)$, so the derivative has the sign of at
most $G(\lambda + G)(\Pi G' - G) < 0$. For a Bayesian stage, $\Pi G_i' - G_i = -c_i\Pi^2/(\Pi + \Pi_{0,i})^2 < 0$. $\square$

**Label:** Proposition (proved post hoc from the T13 C2 row-8 failure, SymPy steps in `t13_audit_classes_diag2.py`).

**Proposition 8 (Bayesian-weight gain along precision).** For $G = c\Pi/(\Pi + \Pi_0)$, with over-weighting ratio
$\kappa = (c/\Pi_0)/F$: $\sigma^2$ has one turning point, a maximum $M$, iff $\kappa > 2$, and is strictly decreasing
otherwise. Endpoint limits $F$ (from above iff $\kappa > 2$) and $H = \Sigma/(\lambda + c)$ (from above). Classes: if
$\kappa > 2$, All ($R^2 \le H$), lower ray ($H < R^2 \le F$), window ($F < R^2 < M$), Empty ($R^2 \ge M$); if $\kappa \le 2$,
All ($R^2 \le H$), lower ray ($H < R^2 < F$), Empty ($R^2 \ge F$).

*Proof.* By Lemma 52 with $\varepsilon = 1 - G/c$, $N = 0$ reduces to $G^2 + 2\lambda G + 2\Sigma\Pi_0 - \lambda c = 0$,
which has one positive root iff $\lambda c > 2\Sigma\Pi_0$, i.e. $\kappa > 2$. Near $\Pi = 0$,
$N \approx \Pi(\lambda c/\Pi_0 - 2\Sigma)$, so the turning point is a maximum. $H$ is approached from above by Lemma 53.
The classes follow from Theorem 2. $\square$

**Label:** Proposition (proved in Paper 1; reduction T10.3, position error $6\times10^{-31}$; T10.7 and T13 C2 row 2).

Reading: the over-weighting ratio decides the window, and the peak is unique.

---

## 4. Design sweeps

**Theorem 9 (monotone gain sweeps cannot window).** Fix $\Pi$. Let $\theta \mapsto G(\theta)$ be continuous and strictly
monotone on $D$. Then $\sigma^2(G(\theta), \Pi)$ is strictly monotone or strictly decreasing-then-increasing, so every
failure set is Empty, All, a lower ray, an upper ray or two rays. No window and no mixed class occur.

*Proof.* Lemma 5's strictly decreasing-then-increasing function composed with a strictly monotone map has at most one
interior minimum, so it is strictly quasiconvex; its sublevel sets are intervals and their complements in $D$ are at most
two rays. $\square$

**Label:** Theorem (proved; T8.4, 1,000,000 classifications, 0 windows or mixed classes; T13 C2 rows 10–12).

Reading: windows need a sweep that moves the variance curve itself, as precision does.

### 4.1 Prior precision $\Pi_0$

Fixed $\Pi, c > 0$; $G(\Pi_0) = c\Pi/(\Pi + \Pi_0)$ decreases from $c$ to $0$. Write $V_c = \sigma^2(c, \Pi)$,
$\Pi_A = c(c + 2\lambda)/(2\Sigma)$ and $\Pi_B = c/(2F) = c\lambda/(2\Sigma)$, so $\Pi_B < \Pi_A$.

**Proposition 10 (prior precision: endpoints and extrema).**
- $L_+ = F$, approached from below; $L_- = V_c$, with the approach direction given below.
- If $c \le G^\star$ (i.e. $\Pi \ge \Pi_A$): $\sigma^2$ increases strictly from $V_c$ (approached from above) to $F$.
- If $c > G^\star$ ($\Pi < \Pi_A$): one interior extremum, a global minimum at $\Pi_0^\star = \Pi(c/G^\star - 1)$ with value
  $\sigma_\star^2(\Pi)$; $V_c$ is then approached from below.
- $V_c > F \iff c > 2F\Pi \iff \Pi < \Pi_B$, and $V_c = F \iff \Pi = \Pi_B$.

*Proof.* Lemma 5 composed with the strictly decreasing map $\Pi_0 \mapsto G$, which passes through $G^\star$ iff
$c > G^\star$, at $\Pi_0^\star$. Near $\Pi_0 = \infty$, $G \to 0^+$ where $\sigma^2$ decreases in $G$, so $F$ is approached
from below. $c > G^\star \iff c^2 + 2\lambda c > 2\Sigma\Pi$. $\square$

**Label:** Proposition (proved; T8.1(d),(f),(g), T8.2).

**Proposition 11 (prior precision: classification at every tolerance).**

*Case P1, $\Pi \ge \Pi_A$.* Sequence $(V_c, F)$: All ($R^2 \le V_c$), upper ray ($V_c < R^2 < F$), Empty ($R^2 \ge F$).

*Case P2, $\Pi_B \le \Pi < \Pi_A$.* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < V_c \le F$: All
($R^2 < \sigma_\star^2$); two rays ($R^2 = \sigma_\star^2$, the domain minus $\Pi_0^\star$; and $\sigma_\star^2 < R^2 < V_c$);
upper ray ($V_c \le R^2 < F$); Empty ($R^2 \ge F$). At $\Pi = \Pi_B$ the upper-ray row is empty.

*Case P3, $\Pi < \Pi_B$.* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < F < V_c$: All ($R^2 < \sigma_\star^2$);
two rays ($\sigma_\star^2 \le R^2 < F$); lower ray ($F \le R^2 < V_c$); Empty ($R^2 \ge V_c$).

*Proof.* Theorem 2 with Proposition 10; $F$ is approached from below, $V_c$ from above in P1 and from below in P2–P3, and the
minimum value is attained only at $\Pi_0^\star$. $\square$

**Label:** Proposition (proved; T8.3, 62/62 classes including all equality rows; T13 C2 row 10).

**Worked example** ($\lambda = c = 1$, $\Sigma = 0.01$): $\Pi_B = 50$, $\Pi_A = 150$.
- $\Pi = 1$ (P3): $G^\star = 0.0099505$, $\Pi_0^\star = 99.498$, $\sigma_\star^2 = 0.0099505$, $V_c = 0.255$.
- $\Pi = 60$ (P2): $\Pi_0^\star = 64.162$, $\sigma_\star^2 = 0.0080540$, $V_c = 0.0091667$.
- $\Pi = 500$ (P1): monotone from $V_c = 0.0055$ to $F$.

Reading: the best fixed prior at a given precision reproduces the Kalman–Bucy gain; both misweighting directions are worse.

### 4.2 Coupling $c$

Fixed $\Pi, \Pi_0$; $K = \Pi/(\Pi + \Pi_0)$ and $G = cK$ increases from $0$ to $\infty$.

**Proposition 12 (coupling: endpoints and extrema).** $L_- = F$ (from below), $L_+ = \infty$. One interior extremum, a
global minimum at $c^\star = G^\star(\Pi)/K$ with value $\sigma_\star^2(\Pi)$. $\sigma^2 = F$ again at
$c_F = 2F(\Pi + \Pi_0)$, and $\sigma^2 > F$ iff $c > c_F$.

*Proof.* Lemma 5 composed with $c \mapsto cK$, which passes through $G^\star$ and $2F\Pi$. $\square$

**Label:** Proposition (proved; T8.1(e)–(g), T8.2).

**Proposition 13 (coupling: classification).** All ($R^2 < \sigma_\star^2$); two rays ($\sigma_\star^2 \le R^2 < F$; at
$R^2 = \sigma_\star^2$ the domain minus $c^\star$); upper ray ($R^2 \ge F$, equal to $(c_F, \infty)$ at $R^2 = F$). Never
Empty and never a window.

*Proof.* Theorem 2 with sequence $(F, \sigma_\star^2, \infty)$ and approach to $F$ from below. $\square$

**Label:** Proposition (proved; T8.3; T13 C2 row 11).

**Worked example** ($\lambda = 1$, $\Sigma = 0.01$, $\Pi = \Pi_0 = 1$): $c^\star = 0.019901$, $\sigma_\star^2 = 0.0099505$,
$c_F = 0.04$.

---

## 5. Correlation-time sweeps

Sensory noise $\eta$ is Ornstein–Uhlenbeck with correlation time $\tau > 0$. Two normalizations are studied, and a
family that contains both.

### 5.1 Matched zero-frequency power

$C_\eta(u) = e^{-|u|/\tau}/(2\Pi\tau)$ and $S_\eta(\omega) = (1/\Pi)/(1 + \tau^2\omega^2)$, so $S_\eta(0) = 1/\Pi$ for every
$\tau$. The relay's gain is set by precision alone, so along $\tau$ it is a constant $G > 0$ (with $G = 0$,
$\sigma^2 \equiv F$); write $a = \lambda + G$.

**Lemma 14 (relay variance).**
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2}{2\Pi(1 + a\tau)}\right),
\qquad
\sigma^2 > F \iff G/\Pi > 2F(1 + a\tau).
$$

*Proof.* The process-noise part contributes $\Sigma/a$. A first-order filter $1/(s + a)$ driven by OU input of variance
$v$ and rate $1/\tau$ has output variance $v/(a(a + 1/\tau))$; with $v = G^2/(2\Pi\tau)$ this is $G^2/(2\Pi a(1 + a\tau))$.
The excess form follows by subtracting $F$. $\square$

**Label:** Lemma (proved; T9.1(a),(b) by an augmented-state Lyapunov route).

**Proposition 15 (relay: endpoints and monotonicity).** $\sigma^2$ is strictly decreasing in $\tau$, from
$V_w = (\Sigma + G^2/(2\Pi))/(\lambda + G)$ (approached from below) to $H_G = \Sigma/(\lambda + G)$ (approached from above).
Always $H_G < F$; $V_w > F \iff G > 2F\Pi$.

*Proof.* The only $\tau$-dependence is $1/(1 + a\tau)$. Approach directions follow from C4 for a decreasing function;
$V_w$ versus $F$ is Lemma 5. $\square$

**Label:** Proposition (proved; T9.1, T9.4).

**Proposition 16 (relay: classification).** All ($R^2 \le H_G$); lower ray $(0, \tau_R)$ ($H_G < R^2 < V_w$); Empty
($R^2 \ge V_w$), with
$$
\tau_R = \frac{1}{a}\left(\frac{G^2}{2\Pi(aR^2 - \Sigma)} - 1\right).
$$
At $R^2 = F$: lower ray $(0, \tau_F)$, $\tau_F = (G/(2F\Pi) - 1)/a$, if $G > 2F\Pi$; Empty otherwise.

*Proof.* Theorem 2 with sequence $(V_w, H_G)$; solve Lemma 14 for $\tau$. $\square$

**Label:** Proposition (proved; T9.1(c), T9.4, 80,000 classifications; T13 C2 row 13).

**Worked example** ($\lambda = c = 1$, $\Sigma = 0.01$, $\Pi = \Pi_0 = 1$, so $G = 0.5$): $V_w = 0.09$,
$H_G = 0.0066667$, $\tau_F = 16$; $\sigma^2(1) = 0.04$, $\sigma^2(10) = 0.011875$, $\sigma^2(16) = 0.01$.

Reading: at matched zero-frequency power, colouring the noise always helps a fixed relay; failure concentrates near the
white limit.

**Proposition 17 (optimal stationary error).** With measurement differencing ($z = \dot y + y/\tau$), the optimal
stationary error is the positive root of
$$
(1 - \lambda\tau)^2P^2 + \Big(4\Sigma\tau + \frac{2\lambda}{\Pi}\Big)P - \frac{2\Sigma}{\Pi} = 0,
\qquad
P(\tau) = \frac{4\Sigma}{\Pi(b + \sqrt D)},\quad b = 4\Sigma\tau + \frac{2\lambda}{\Pi},\quad D = b^2 + \frac{8\Sigma(1-\lambda\tau)^2}{\Pi}.
$$
The rationalized form has no singularity at $\lambda\tau = 1$.

*Proof.* $z = hs + v$ with $h = 1/\tau - \lambda$, $v = w_s + w_\eta$, measurement intensity $R_v = 2\Sigma + 1/(\Pi\tau^2)$
and cross-intensity $2\Sigma$. The steady-state correlated-noise Riccati equation is
$0 = -2\lambda P + 2\Sigma - (hP + 2\Sigma)^2/R_v$; multiplying by $-\tau^2R_v$ gives the quadratic. Its constant term is
negative and its leading coefficient non-negative, so it has one positive root. $\square$

**Label:** Proposition (proved; T9.1(d),(e); T9.2 Wiener route to $2\times10^{-17}$; mp ARE route in the T9 diagnosis).

**Theorem 18 (optimal error decreases in $\tau$).** $P$ is strictly decreasing on $(0,\infty)$, with
$P(0^+) = \sigma_\star^2(\Pi)$ and $P(\tau) \sim 1/\big(\Pi\tau(1 + \sqrt{1 + \lambda^2/(2\Sigma\Pi)})\big) \to 0$.

*Proof.* $b$ increases in $\tau$, and $dD/d\tau = 32\Sigma^2\tau + 16\Sigma\lambda^2\tau/\Pi > 0$, so $b + \sqrt D$
increases. At $\tau = 0$, $P = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})$. For large $\tau$, $b \sim 4\Sigma\tau$ and
$\sqrt D \sim 4\Sigma\tau\sqrt{1 + \lambda^2/(2\Sigma\Pi)}$. $\square$

**Label:** Theorem (proved; T9.1(f),(g), T9.5). Also a corollary of Theorem 66 via Proposition 71(b).

**Proposition 19 (optimal: classification).** Lower ray $(0, \tau_R^\star)$ for $0 < R^2 < \sigma_\star^2$; Empty for
$R^2 \ge \sigma_\star^2$, with
$$
\tau_R^\star = \frac{2\lambda R^2 - 4\Sigma + \sqrt\Delta}{2\lambda^2R^2},
\qquad
\Delta = 16\Sigma^2 - 16\lambda\Sigma R^2 + \frac{8\lambda^2(\Sigma - \lambda R^2)}{\Pi}.
$$
The optimal filter never produces All, a window, an upper ray or two rays along $\tau$.

*Proof.* Theorem 2 with Theorem 18. $P = R^2$ in Proposition 17 is a quadratic in $\tau$ with leading coefficient
$\lambda^2R^4 > 0$ and constant term $R^4 + 2\lambda R^2/\Pi - 2\Sigma/\Pi$, negative iff $R^2 < \sigma_\star^2$. $\square$

**Label:** Proposition (proved; T9.1(h), T9.4; T13 C2 row 14).

**Proposition 20 (best constant-gain relay).** Let $V(\tau) = \inf_{G \ge 0}\sigma^2(G, \tau)$. Then $P \le V$, $V$ is
strictly decreasing, $V(0^+) = \sigma_\star^2$ and $V(\infty) = 0$.

*Proof.* A constant-gain relay is a causal linear estimator, so $P \le V$. $G = 0$ is never the infimizer
($\partial_G\sigma^2 = -\Sigma/\lambda^2 < 0$ there). For $\tau_1 < \tau_2$: if the infimum at $\tau_1$ is attained at
$G_1 > 0$, then $V(\tau_2) \le \sigma^2(G_1, \tau_2) < V(\tau_1)$; if it is approached as $G \to \infty$, its value is
$1/(2\Pi\tau_1) > 1/(2\Pi\tau_2) \ge V(\tau_2)$. As $\tau \to \infty$, $\sigma^2(G, \tau) \to \Sigma/(\lambda + G)$, whose
infimum is $0$. $\square$

**Label:** Proposition (proved; T9.5 with the mp diagnosis).

**Proposition 21 (strict gap).** $P(\tau) < V(\tau)$ for every $\tau > 0$.

*Proof.* (i) If a relay with gain $G$ attained $P$, its estimate would equal the conditional mean (uniqueness of the
$L^2$ projection), so its error $e = s - \hat s$ would be orthogonal to every past observation. (ii) For the relay,
$\dot e = -ae - G\eta + w_s$, and for $u \ge 0$
$$
c(u) = \mathbb E[e(t)\,y(t-u)] = e^{-au}c(0) - \frac{G}{2\Pi\tau}\,\frac{e^{-u/\tau} - e^{-au}}{a - 1/\tau}
\quad (a \ne 1/\tau),
$$
with $-\tfrac{G}{2\Pi\tau}\,u\,e^{-au}$ in place of the last term when $a = 1/\tau$ ($w_s$ after $t - u$ is independent of
$y(t-u)$). For $G > 0$ the $e^{-u/\tau}$ term (or the $ue^{-au}$ term) is nonzero, so $c \not\equiv 0$; for $G = 0$,
$c(u) = Fe^{-\lambda u} \not\equiv 0$. So no relay is optimal. (iii) As $G \to \infty$, $\sigma^2 \to \operatorname{Var}\eta =
1/(2\Pi\tau)$, the error of the estimator $\hat s = y$, which is not optimal either since
$\mathbb E[(s - y)y] = -\operatorname{Var}\eta \ne 0$. (iv) $\sigma^2(G, \tau)$ is continuous on the compactified range
$[0, \infty]$, so its minimum $V(\tau)$ is attained there and exceeds $P(\tau)$. $\square$

**Label:** Proposition (proved; T13 A7: symbolic covariance identity and 10,000 sets at 60 digits, 0 failures; T9.5 had
recorded strictness as a numerical result).

**Worked example** ($\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$): $\sigma_\star^2 = 0.0099505$; $P(1) = 0.0098039$ (the
linear case $\lambda\tau = 1$) against $V(1) = 0.0099010$; $P(10) = 0.0067813$. The fixed relay with $G = 0.5$ gives $0.04$
and $0.011875$; as $\tau \to \infty$ it tends to $H_G = 0.0066667$ while $P \to 0$.

### 5.2 Matched variance

Noise of fixed variance $v$ and varying bandwidth: $C_\eta(u) = v e^{-|u|/\tau}$, $S_\eta(\omega) = 2v\tau/(1 + \tau^2\omega^2)$.

**Proposition 22 (optimal filter at matched variance).** The optimal stationary error is the positive root of
$$
A(\tau)P^2 + BP - C = 0,\qquad A = \frac{(1 - \lambda\tau)^2}{\tau},\ B = 4(\Sigma + \lambda v),\ C = 4\Sigma v,
$$
i.e. $P = 2C/(B + \sqrt{B^2 + 4AC})$. Consequently: (1) $P$ is strictly decreasing in $A$, so it is unimodal in $\tau$ with
its maximum at $\tau = 1/\lambda$, $P_{\max} = \Sigma v/(\Sigma + \lambda v)$; (2) $A(\tau) = A(1/(\lambda^2\tau))$, so $P$ is
symmetric in $\log\tau$ about $1/\lambda$; (3) $P \sim 2\sqrt{\Sigma v\tau}$ as $\tau \to 0$ and
$P \sim (2/\lambda)\sqrt{\Sigma v/\tau}$ as $\tau \to \infty$; (4) for $0 < R^2 < P_{\max}$ the failure set is the window
$(\tau_-, \tau_+)$,
$$
\tau_\pm = \frac{(2\lambda + A_R) \pm \sqrt{A_R(4\lambda + A_R)}}{2\lambda^2},
\qquad A_R = \frac{C - BR^2}{R^4},\qquad \tau_-\tau_+ = \frac{1}{\lambda^2},
$$
and for $R^2 \ge P_{\max}$ it is Empty.

*Proof.* The correlated-noise Riccati equation of Proposition 17 holds with $w_\eta$ of intensity $2v/\tau$, so
$R_v = 2\Sigma + 2v/\tau$; multiplying by $-\tau R_v$ gives the quadratic. Its constant term is negative and $B > 0$, so
there is one positive root, decreasing in $A \ge 0$. Items 1–3 follow from the shape of $A$. For item 4, set $P = R^2$, solve
for $A$, then solve $\lambda^2\tau^2 - (2\lambda + A_R)\tau + 1 = 0$. $\square$

**Label:** Proposition (proved; T10.6: three routes agree to $1.0\times10^{-14}$, shape exact to $10^{-50}$; T13 C2 row 16).

**Counterexample 23 (analytic; the optimal filter can window).** Paper 1's "the optimal filter never produces a window"
holds along precision (Theorem 6) and along matched-zero-frequency $\tau$ (Theorem 18), but fails along matched-variance
$\tau$: by Proposition 22 the optimal failure set is a window for every $0 < R^2 < P_{\max}$.

**Label:** Counterexample (analytic; T10.6).

**Proposition 24 (relay at matched variance).** For fixed $G > 0$,
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2v\tau}{1 + a\tau}\right),
$$
strictly increasing from $H_G$ to $(\Sigma + G^2v/a)/a$ and $\ge P$ throughout. Classes: All ($R^2 \le H_G$), upper ray
($H_G < R^2 <$ top), Empty ($R^2 \ge$ top).

**Label:** Proposition (proved; T10.6; T13 C2 row 15).

Reading: the same physical change (narrowing the noise bandwidth) gives a monotone optimal filter at matched
zero-frequency power and a windowed one at matched variance. The normalization is a modelling choice with topological
consequences.

### 5.3 The power-normalized family

OU noise with $S_{\beta,\tau}(\omega) = K\tau^\beta/(1 + \tau^2\omega^2)$, $\operatorname{Var}\eta = v(\tau) = (K/2)\tau^{\beta-1}$,
$\tau \in (0,\infty)$, $K > 0$, $\beta \in \mathbb R$. $\beta = 0$ is matched zero-frequency power ($K = 1/\Pi$), $\beta = 1$
matched variance ($K = 2v$). The optimal error is Proposition 22's root with $v = v(\tau)$.

**Theorem 25 (sharpness of the ordering condition).**
1. $\beta \le 0$: $S_{\beta,\tau}$ decreases in $\tau$ at every $\omega$; the sweep is causally ordered (information
   increasing in $\tau$), so $P$ is non-increasing. Optimal classes: lower ray, Empty.
2. $\beta \ge 2$: $S_{\beta,\tau}$ increases in $\tau$ at every $\omega$; ordered with information decreasing in $\tau$, so
   $P$ is non-decreasing. Optimal classes: upper ray, Empty.
3. $0 < \beta < 2$: every pair $\tau_1 \ne \tau_2$ has crossing spectra, $P \to 0$ at both ends while $P > 0$, so for every
   $0 < R^2 < \max P$ the optimal failure set is bounded away from both ends: a window (exactly one, by Theorem 26).

Hence, in this family: causally ordered $\iff$ $P$ monotone $\iff$ no optimal-filter window $\iff$ $\beta \notin (0, 2)$.

*Proof.* $\partial_\tau\log S = \beta/\tau - 2\tau\omega^2/(1 + \tau^2\omega^2)$, and the second term lies in $[0, 2/\tau)$: it
is $\le 0$ for every $\omega$ if $\beta \le 0$, $> 0$ if $\beta \ge 2$, and changes sign with $\omega$ if $0 < \beta < 2$.
Parts 1–2 follow from Proposition 69 and Corollary 67. For part 3, $P \le 2C/\sqrt{4AC} = \sqrt{C/A} =
\sqrt{2\Sigma K}\,\tau^{\beta/2}/|1 - \lambda\tau|$, which tends to $0$ as $\tau \to 0$ iff $\beta > 0$ and as $\tau \to \infty$ iff
$\beta < 2$. $\square$

*Limits of $P$ itself where the bound does not vanish.* $\beta < 0$, $\tau \to 0$: $P \to F$; $\beta = 0$, $\tau \to 0$:
$P \to \sigma_\star^2(1/K)$; $\beta = 2$, $\tau \to \infty$: $P \to \sigma_\star^2(\lambda^2/K)$ (not $F$); $\beta > 2$,
$\tau \to \infty$: $P \to F$, approached like $\tau^{2-\beta}$.

**Label:** Theorem (proved; T11.3 over 37 values of $\beta$, with the $\beta \ge 2$ limits as corrected in the T11
diagnosis; T13 C2 rows 17–19).

**Theorem 26 (unimodality for $0 < \beta < 2$).** For $0 < \beta < 2$, $P$ has exactly one turning point, a maximum, so the
optimal failure set has $k = 1$.

*Proof.* Let $\Phi(\tau, P) = AP^2 + BP - C$, so $\Phi_P = 2AP + B > 0$. With $A' = (\lambda^2\tau^2 - 1)/\tau^2$,
$A'' = 2/\tau^3$, $v'/v = (\beta - 1)/\tau$ and $v''/v' = (\beta - 2)/\tau$: $\Phi_\tau = A'P^2 - 4v'(\Sigma - \lambda P)$ and
$\Phi_{\tau\tau} = A''P^2 - 4v''(\Sigma - \lambda P)$. At a critical point $P' = 0$, so $\Phi_\tau = 0$ and
$P'' = -\Phi_{\tau\tau}/\Phi_P$. For $\beta \ne 1$, substituting $\Sigma - \lambda P = A'P^2/(4v')$,
$$
\Phi_{\tau\tau} = P^2\Big(A'' - A'\frac{v''}{v'}\Big) = \frac{P^2\,\big(\beta + (2 - \beta)\lambda^2\tau^2\big)}{\tau^3} > 0,
$$
so $P'' < 0$; for $\beta = 1$, $\Phi_\tau = A'P^2$ vanishes only at $\tau = 1/\lambda$, where $A'' > 0$ gives the same sign.
Every critical point is therefore a strict local maximum. Two strict maxima would enclose an interior minimum, a critical
point that is not a strict maximum, so there is at most one critical point; there is at least one because $P > 0$ and
$P \to 0$ at both ends (Theorem 25). $\square$

**Label:** Theorem (proved; T13 A4: symbolic identities and 10,000 curves; T11.3 had recorded it as a numerical result,
12,900/12,900 curves).

**Proposition 27 (duality).** $P_{\beta, K}(\tau) = P_{2-\beta,\ K\lambda^{2-2\beta}}\big(1/(\lambda^2\tau)\big)$.

*Proof.* $A$ is invariant under $\tau \mapsto 1/(\lambda^2\tau)$, and $(K'/2)x^{1-\beta}$ at $x = 1/(\lambda^2\tau)$ equals
$(K/2)\tau^{\beta-1}$ when $K' = K\lambda^{2-2\beta}$. $\square$

**Label:** Proposition (proved; T11.1, T11.3 to $8\times10^{-51}$).

Reading: in the natural one-parameter family of coloured noises the information-ordering condition is exactly sharp; the
two normalizations sit on opposite sides of the boundary.

---

## 6. Sampling interval

**M-P model** (point sampling, matched floor): $x_{k+1} = ax_k + w_k$, $a = e^{-\lambda\Delta t}$,
$\operatorname{Var}w = q = F(1 - a^2)$; $z_k = x_k + v_k$, $\operatorname{Var}v = r = 1/(\Pi\Delta t)$. Write $s = 1 - a^2$
and $\varphi = F\Pi\Delta t$. Metrics: posterior $P^+$ at sample times ("post"), prior $P^- = a^2P^+ + q$ ("prior") and
time average $\bar P = F - (F - P^+)\,s/(2\lambda\Delta t)$ ("avg"). Filters: optimal (steady Kalman); D1, sampled relay,
$L = 1 - e^{-G\Delta t}$; D2, discrete Bayesian weight, $L = c\Pi\Delta t/(\Pi\Delta t + \Pi_0)$ with $0 < c < 2$; D3, discrete Kalman
over-trusting precision by $\rho$. For a fixed gain,
$$
P^+ = \frac{(1-L)^2q + L^2r}{1 - (1-L)^2a^2}.
$$
**M-I model** (integrate-and-dump): $z_k$ is the average of $dy$ over the $k$-th interval; metrics (a) error at sample
times and (b) time average, both from Task 11's closed form.

### 6.1 Excess sets

**Lemma 28 (shared excess set).** For any filter on M-P, $P^- - F = a^2(P^+ - F)$ and
$\bar P - F = (P^+ - F)\,s/(2\lambda\Delta t)$. Hence all three metrics exceed $F$ on the same set, $\{L/(2 - L) > \varphi\}$
(Paper 1's discrete excess condition).

**Label:** Lemma (proved; T12 symbolic A1).

**Proposition 29 (D1: tanh lemma).** $L/(2 - L) = \tanh(G\Delta t/2)$, so the excess set is $\{G\,h(G\Delta t) > F\Pi\}$ with
$h(x) = \tanh(x/2)/x$ strictly decreasing from $1/2$. The excess set is the lower ray $(0, \Delta t_E)$ iff $G > 2F\Pi$ (the
continuous-time condition), and empty otherwise; $\Delta t_E$ solves $\tanh(G\Delta t/2) = F\Pi\Delta t$.

*Proof.* $h'(x) = (x - \sinh x)/(2x^2\cosh^2(x/2)) < 0$ since $\sinh x > x$, and $h \to 1/2$ as $x \to 0$. $\square$

**Label:** Proposition (proved; T12 symbolic A2, 1,000/1,000 sets, $\Delta t_E$ to $10^{-30}$).

Reading: sampling never creates excess that continuous time lacks, and longer intervals remove it.

**Proposition 30 (D2).** The excess set is the lower ray $\Delta t < \Delta t_E = (c - 2F\Pi_0)/((2 - c)F\Pi)$ iff
$\kappa = c/(F\Pi_0) > 2$, and empty otherwise.

**Label:** Proposition (proved; T12 symbolic A3, 1,000/1,000 sets).
The model requires $0 < c < 2$ (so $0 < L < 2$). For $c > 2$ the gain tends to $c$, $L/(2 - L) > \varphi$ no longer
characterizes excess, and the excess set can be all of $(0, \infty)$: with $\lambda = 1$, $\Sigma = 0.01$, $\Pi = \Pi_0 = 1$,
$c = 3$, $P^+ > F$ at every $\Delta t$ and $P^+ \to 4F$.

**Proposition 31 (D3).** The excess set is $\{\varphi < 1$ and $s(1 - \varphi)(\rho(1 + \varphi) - 2) > 4\varphi\}$. Its
small-$\Delta t$ behaviour gives the onset: excess near $\Delta t = 0$ iff $\rho > 2 + u$, which is the continuous excess
condition for $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$ ($\sqrt{1 + \rho u} > 1 + u$).

*Proof.* D3's gain is $L = m/(1 + m)$, with $m$ the positive root of $Q(m) = m^2 + s(1 - \rho\varphi)m - s\rho\varphi$. By
Lemma 28, excess $\iff L/(2 - L) > \varphi \iff m(1 - \varphi) > 2\varphi$. If $\varphi \ge 1$ this fails. If $\varphi < 1$ it
says $m > T = 2\varphi/(1 - \varphi)$, i.e. $Q(T) < 0$ ($Q$ has one positive root and is increasing there), and
$Q(T)(1 - \varphi)^2/\varphi = 4\varphi - s(1 - \varphi)(\rho(1 + \varphi) - 2)$. Near $\Delta t = 0$, with $x = \lambda\Delta t$
and $\varphi = ux/2$, the difference $s(1 - \varphi)(\rho(1 + \varphi) - 2) - 4\varphi$ is $2x(\rho - 2 - u) + O(x^2)$; at
$\rho = 2 + u$ the first two orders cancel and it equals $-u(3u^2 + 6u + 4)x^3/6 + O(x^4) < 0$, so there is no excess near
$0$ in that equality case either. $\square$

**Label:** Proposition (proved; T12 symbolic A4, 1,000/1,000 sets, 0 disagreements in 201,514 membership tests; equality case
checked by series in T13).
The earlier onset "$\rho > 2$" is the condition for excess at *some* precision (Proposition 42); at fixed precision it is
false (178 of 1,000 census sets have $2 < \rho \le 2 + u$ and no excess near $0$).

**Proposition 32 (endpoint limits).**

| Filter | $\Delta t \to 0$ (all metrics) | $\Delta t \to \infty$ |
|---|---|---|
| Optimal | $\sigma_\star^2$ | post $\to 0$; prior, avg $\to F$ from below |
| D1 | $\sigma^2(G, \Pi)$ | post $\to 0$; prior $\to F$ from below (gap $\propto e^{-2\lambda\Delta t}$); avg $\to F$ from below, like $-F/(2\lambda\Delta t)$ |
| D2 | $\sigma^2(c\Pi/\Pi_0, \Pi)$ | post $\to (1-c)^2F$, with $\Delta t\,(P^+ - (1-c)^2F) \to c[c + 2(1-c)F\Pi_0]/\Pi$; prior, avg $\to F$ from below |
| D3 | $\sigma^2(G_\rho, \Pi)$ | post $\to 0$; prior, avg $\to F$ from below |

Here $G_\rho = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$.

**Label:** Proposition (proved; T12 symbolic A5; the D2 coefficient by the series route after `sympy.limit` failed).

### 6.2 The optimal filter along $\Delta t$

**Theorem 33 (optimal M-P error along $\Delta t$).**
(a) $P^+$ is strictly decreasing, from $\sigma_\star^2$ to $0$.
(b) $P^-$ is strictly increasing, from $\sigma_\star^2$ to $F$.
(c) $\bar P$ is strictly increasing, from $\sigma_\star^2$ to $F$.

*Proof.* Write $x = \lambda\Delta t$, $s = 1 - e^{-2x}$, $s' = 2e^{-2x}$, $r = \lambda/(\Pi x)$.

(a) $P^+ = F/(1 + \mu)$, where $\mu > 0$ solves $\mu^2 + (1 - \varphi)\mu - \varphi/s = 0$ and is strictly increasing in
$\varphi$ and in $w := \varphi/s$; both increase in $x$ (since $e^y > 1 + y$).

(b) $M = P^-$ is the positive root of $f(M) = M^2 + s(r - F)M - sFr$; $f'(M) = 2M + s(r - F) > 0$ there because the product of
the roots, $-sFr$, is negative. Implicit differentiation with $r' = -r/x$ gives
$\operatorname{sign}(dM/dx) = \operatorname{sign} B$, $B = FMs' - (F - M)r(s/x - s')$. On $f = 0$, $sr(F - M) = M(M - sF)$, so
$B = M[Fs' - (M - sF)(s/x - s')/s]$. Now $f(F) = F^2(1 - s) > 0$ and $f(sF) = -sFr(1 - s) < 0$ give $sF < M < F$, hence
$0 < M - sF < F(1 - s)$; and $s/x > s'$ since $s - xs' = e^{-2x}(e^{2x} - 1 - 2x) > 0$. So
$B > (MF/s)[ss' - (1 - s)(s/x - s')] = (MF/s)\,(e^{-2x}/x)\,(2x - 1 + e^{-2x}) > 0$, the last factor being positive because
$y \mapsto e^{-y} - 1 + y$ vanishes at $0$ and has derivative $1 - e^{-y} > 0$.

(c) By Lemma 28 and (a), $\bar P = F - (F/2)Q$ with $Q = \mu s/((1 + \mu)x)$, so it suffices that $Q$ decreases. With
$\varphi = wx$ ($w = F\Pi/\lambda$) and $E = 1/x - s'/s > 0$, implicit differentiation of the $\mu$ equation and
$\varphi/s = \mu(\mu + 1 - \varphi)$ give $(2\mu + 1 - \varphi)\mu' = \varphi\mu/x + \mu(\mu + 1 - \varphi)E$, where
$2\mu + 1 - \varphi > 0$ and $\mu + 1 - \varphi > 0$. Then $d\ln Q/dx = \mu'/(\mu(1 + \mu)) - E$, and
$(1 + \mu)(2\mu + 1 - \varphi)E - [w + (\mu + 1 - \varphi)E] = E\mu(2 + 2\mu - \varphi) - w$ with
$\mu(2 + 2\mu - \varphi) = \varphi(2/s + \mu)$. Hence $d\ln Q/dx < 0 \iff 1 < xE(2/s + \mu) = (1 - xs'/s)(2/s + \mu)$. Since
$\mu > 0$ and
$$
\Big(1 - \frac{xs'}{s}\Big)\frac{2}{s} = 1 + \frac{2e^{-2x}(\sinh 2x - 2x)}{s^2} \ge 1,
$$
this holds. The limits are Proposition 32. $\square$

**Label:** Theorem (proved). (a) T12 symbolic A6; (b) and (c) T13 A1, A2: every step symbolic (two identities by a post-hoc
rewrite route, see Section 12) and 10,000 sets at 100 digits with 0 failures in every link. (c) was a numerical result in
Task 12 (400,000 points).

**Optimal classes.** post: lower ray ($R^2 < \sigma_\star^2$) or Empty ($R^2 \ge \sigma_\star^2$); prior and avg: All
($R^2 \le \sigma_\star^2$, since $\sigma_\star^2$ is approached from above), upper ray ($\sigma_\star^2 < R^2 < F$), Empty
($R^2 \ge F$).

**Proposition 34 (M-P is not a causal-garbling family along $\Delta t$).** In neither direction: by Theorem 66 an ordering
would give a pointwise-in-$t$ inequality between the two (cyclostationary) optimal error curves, and post, prior and avg are
the minimum, the supremum and the time mean of each curve over its period, so all three would move the same way; but post
falls while prior and avg rise (Theorem 33).

**Label:** Proposition (proved; T12 A10, 1,000/1,000 pairs $(\Delta t, 2\Delta t)$).

Reading: each sample carries the signal with noise variance $1/(\Pi\Delta t)$, so longer intervals make every sample more
precise; but samples get sparser, so the error grows more between them.

**Corollary 35 (integrate-and-dump, nested grids).** If $\Delta t_2 = m\Delta t_1$ for an integer $m$ and the grids are
aligned, each coarse M-I sample is the average of $m$ fine samples completed by the time it is, a causal garbling. Hence the
optimal error, pointwise in $t$ and time-averaged, satisfies $P(\Delta t_2) \ge P(\Delta t_1)$ along every chain
$\Delta t_0, m\Delta t_0, m^2\Delta t_0, \dots$

**Label:** Corollary (proved; T11.6, 0 violations in 9,000 pairs).

**Theorem 36 (integrate-and-dump on the continuum).** Both M-I optimal metrics, (a) the error at sample times and (b) the time
average, are strictly increasing in $\Delta t$ on the whole continuum, including non-nested pairs.

*Proof.* By scaling, $P_a = F\,p(x, u)$ with $x = \lambda\Delta t$ and $u = 2\Sigma\Pi/\lambda^2$. In reduced units
($\lambda = \Sigma = 1$, $\Pi = u/2$, $E = e^{-x}$) the integrate-and-dump model has process covariances $q_{11} = 1 - E^2$,
$q_{12} = 2[(1 - E) - (1 - E^2)/2]$, $q_{22} = 2[x - 2(1 - E) + (1 - E^2)/2]$ for the state and its interval average, and with
$h = (1 - E)/x$, $r_e = q_{22}/x^2 + 1/(\Pi x)$ and $g = q_{12}/x$ the posterior $p$ is the positive root of
$$
a_2p^2 + a_1p + a_0 = 0,\qquad a_2 = h^2,\quad a_1 = r_e(1 - E^2) - q_{11}h^2 + 2Ehg,\quad a_0 = -(q_{11}r_e - g^2).
$$
These coefficients satisfy $a_0 = -a_1$ identically, and $a_2/a_1 = u(1 - E)/(2K)$ with
$K = u[x(1 + E) - 2(1 - E)] + x(1 + E)$. Hence
$$
p = \frac{2}{1 + \sqrt{1 + 2u/k(x)}},\qquad k(x) = \frac{K}{1 - E} = (1 + u)\,x\coth(x/2) - 2u.
$$
Since $\frac{d}{dx}[x\coth(x/2)] = (\sinh x - x)/(2\sinh^2(x/2)) > 0$, $k$ increases strictly from $k(0^+) = 2$ to $\infty$, so
$p$ increases strictly from $2/(1 + \sqrt{1 + u}) = \sigma_\star^2/F$ to $1$: (a) is strictly increasing, from $\sigma_\star^2$
(approached from above) to $F$ (approached from below).

*Second route (resultant).* Clearing
denominators, the quadratic has leading coefficient $u(1 - E)^2 > 0$ and product of roots
$2[u(x(1 + E) - 2(1 - E)) + x(1 + E)]/(u(E - 1)) < 0$, because $x(1 + E) - 2(1 - E) = e^{-x}f(x)$ with
$f(x) = xe^x + x - 2e^x + 2 = \sum_{n \ge 3}(n - 2)x^n/n! > 0$. So there is exactly one positive root, it is simple, and since
the cleared quadratic equals its leading coefficient at $p = 1$, $p < 1$, i.e. $P_a < F$. Implicit differentiation gives
$dp/dx = -\partial_x Q/\partial_p Q$ at the root, with $\partial_p Q \ne 0$. The resultant in $p$ of the numerator of
$\partial_x Q$ (with $dE/dx = -E$) and the cleared quadratic is
$$
4u^2x^2(u + 1)^2(E - 1)^4\,(E^2 + 2xE - 1)^2,
$$
and on $E = e^{-x}$ the last factor is $-2e^{-x}(\sinh x - x) < 0$; every factor is nonzero for $x, u > 0$. Hence $\partial_x Q$
never vanishes at the root, $dp/dx$ is continuous and nonzero on the connected set $\{x, u > 0\}$, and one evaluation
($dp/dx = 0.031263$ at $x = u = 1$) fixes its sign. For (b),
$P_b = P_a\,\phi + F(1 - \phi)$ with $\phi = (1 - E^2)/(2x)$, $\phi' = -E^2(e^{2x} - 1 - 2x)/(2x^2) < 0$, so
$dP_b/dx = P_a'\phi + (P_a - F)\phi' > 0$. $\square$

**Label:** Theorem (proved; T13 A3: closed form and limits (`t13_A3_closed.py`, 11/11), exact resultant route, 10,000 sets at
100 digits with 0 violations; T11.6, T12 A9: 400,000 points each). It was Numerical result 2.8 / 4.10a.

### 6.3 Sampled relays

**Proposition 37 (two rays from an over-weighted sampled relay).** Let D1 have $G > 2F\Pi$, and assume C2 for these curves
(finitely many turning points; Conjecture 39 would give it). Then prior and avg start at
$\sigma^2(G, \Pi) > F$ and end at $F$ approached from below, so each has an interior minimum below $F$; for $R^2$ between the
lowest minimum and $F$ the failure set contains a lower and an upper ray: two rays, or $(1,1,k)$ with several minima.

**Label:** Proposition (proved: continuity and Proposition 32; T12 A7 diagnosis).

**How deep the dips are.** avg: $\bar P - F \sim -F/(2\lambda\Delta t)$, a modest dip. prior: the gap is multiplied by
$e^{-2\lambda\Delta t}$, and Task 12 measured relative dips from $10^{-17}$ down to $10^{-32{,}880{,}317}$. The prior's two
rays exist mathematically but are practically irrelevant; the avg two rays are real but narrow.

**Worked example** (D1, $G = 0.5$, $\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$): post rises from $0.09$ to a single maximum
$0.20457$ at $\Delta t = 2.4645$ and falls to $0$, a window for $R^2 \in (0.09, 0.20457)$; avg crosses $F$ at $\Delta t_E = 100$
(to 20 digits), dips to $0.0099875$ at $\Delta t = 200$ (a dip of $0.125\%$) and returns to $F$ from below.

**Numerical result 38 (census of sampled relays).** On 2,000 sets per family, every class agreed by both routes:

| Family | Metric | Turning-point shapes | Classes found |
|---|---|---|---|
| D1 | post | none, max | Empty, lower ray, window |
| D1 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D1 | avg | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D2 | post | none, max, min, min–max | All, Empty, lower ray, upper ray, two rays, window, $(1,0,1)$ |
| D2 | prior, avg | none, min | All, Empty, lower ray, upper ray, two rays |
| D3 | post | none, max | Empty, lower ray, window |
| D3 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D3 | avg | none, min | All, Empty, lower ray, upper ray, two rays |

The D3 excess set at $R^2 = F$ (post) was a lower ray or Empty in 1,000/1,000 sets. Two rays in D1 avg also occur with
$G \le 2F\Pi$ (e.g. $G = 0.019$, $\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$: a maximum then a minimum below the starting value),
so $G > 2F\Pi$ is sufficient for two rays (Proposition 37) but not necessary.

**Label:** Numerical result (T12 A8, 6,000 sets × 3 metrics; T12 Part C; T13 C2 rows 24–32).

Natural gains here give two new mixed classes: upper ray + window $(0,1,1)$ (a max–min shape: a hump before the slow return to
$F$) and lower ray + window $(1,0,1)$ (a min–max shape in D2 post).

**Conjecture 39 (at most two turning points).** Along $\Delta t$, D1–D3 have at most two turning points in every metric.

**Label:** Conjecture (T12 census and T13 C2 rows 24–32: never more than two; no proof, T13 A6).

---

## 7. Process noise (moving floor)

Fix $\lambda$ and $\Pi$; $F = \Sigma/\lambda$ moves with $\Sigma$. Two conventions: **absolute** (fixed $R^2$) and
**relative** (failure means $\sigma^2 > rF$).

**Lemma 40 (scaling).** $\sigma^2/F = (1 + g^2/u)/(1 + g)$. For a gain that depends on $(\Sigma, \Pi)$ only through $u$, the
relative-tolerance $\Sigma$ sweep and the precision sweep classify identically in $u$.

**Label:** Lemma (proved; T12 symbolic B1).

**Proposition 41 ($\Sigma$-independent gain).** Absolute: $\sigma^2$ is affine and increasing, from $G^2/(2\Pi(\lambda + G))$
(approached from above) to $\infty$; classes All, upper ray. Relative: $\sigma^2/F$ decreases from $\infty$ to $1/(1 + g)$;
classes All, lower ray. Excess set ($r = 1$): $\Sigma < \lambda G/(2\Pi)$.

**Label:** Proposition (proved; T12 B2; T13 C2 rows 35–36).

**Proposition 42 ($\Sigma$-tracking Kalman, over-trust $\rho$).** Let $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$ and
$w = \sqrt{1 + \rho u}$. Absolute: strictly increasing from $0$, class upper ray. Relative:
$$
\frac{\sigma^2}{F} = \frac{(1 + \rho)w + (1 - \rho)}{w(w + 1)},
$$
starting at $1$ and tending to $0$, with a single maximum at $w_M = [(\rho - 1) + \sqrt{2\rho(\rho - 1)}]/(1 + \rho)$ iff
$\rho > 2$, and strictly decreasing otherwise. Classes: $\rho > 2$: lower ray ($r \le 1$, since the start at $1$ is
approached from above), window ($1 < r <$ peak), Empty (at or above the peak); $\rho \le 2$: lower ray ($r < 1$), Empty ($r \ge 1$).

*Proof.* Absolute: $\sigma^2\Pi/\lambda = [(w^2 - 1)/\rho + (w - 1)^2]/(2w)$, whose $w$-derivative is
$[(w^2 - 1)(1 + 1/\rho) + 2/\rho]/(2w^2) > 0$. Relative: the derivative's numerator,
$-(1 + \rho)w^2 + 2(\rho - 1)w + (\rho - 1)$, is a downward parabola with value $2(\rho - 2)$ at $w = 1$ and vertex at
$(\rho - 1)/(1 + \rho) < 1$; the classes follow from Theorem 2. $\square$

**Label:** Proposition (proved; T12 B3, 2,000 sets, maximum position to $6\times10^{-31}$; T13 C2 rows 37–38).

**Proposition 43 ($\Sigma$-tracking Kalman, misspecified $\lambda'$).** Let $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma\Pi}$.
Absolute: strictly increasing from $0$, class upper ray. Relative: starts at $1$ and tends to $0$, with a single maximum iff
$\lambda' < \lambda/2$ and strictly decreasing otherwise. Classes: $\lambda' < \lambda/2$: lower ray ($r \le 1$), window
($1 < r <$ peak), Empty; otherwise lower ray ($r < 1$), Empty ($r \ge 1$).

*Proof.* With $\Sigma = (G^2 + 2\lambda'G)/(2\Pi)$: absolute $\sigma^2 = G(G + \lambda')/(\Pi(\lambda + G))$ with derivative
numerator $G^2 + 2\lambda G + \lambda\lambda' > 0$; relative $\sigma^2/F = 2\lambda(G + \lambda')/((G + 2\lambda')(G + \lambda))$
with derivative numerator $2\lambda[-G^2 - 2\lambda'G + \lambda'(\lambda - 2\lambda')]$, a downward parabola with vertex at
$G = -\lambda' < 0$ and value $\lambda'(\lambda - 2\lambda')$ at $G = 0$. $\square$

**Label:** Proposition (proved; T12 B4, 2,000 sets; T13 C2 rows 39–40).

**Proposition 44 (optimal).** Absolute: increasing from $0$, class upper ray. Relative: $2/(1 + \sqrt{1 + u})$ is decreasing,
classes lower ray, Empty.

**Label:** Proposition (proved; T12 B5; T13 C2 rows 41–42).

**Proposition 45 (signal sweeps).** $\sigma_\star^2$ is increasing in $\Sigma$, decreasing in $\lambda$ at fixed $\Sigma$, and
increasing in $\lambda$ at fixed $F$ (since $\sigma_\star^2 = 2F/(1 + \sqrt{1 + 2F\Pi/\lambda})$). So the optimal filter never
windows along these sweeps either, for an elementary reason rather than an information-ordering one.

**Label:** Proposition (proved; one-line derivatives; T11.1).

Reading: on a moving floor the tolerance convention decides the topology. With absolute tolerances every family is monotone;
with relative tolerances windows return under the same factor-of-two over-confidence condition as Paper 1 ($\rho > 2$, or
$\lambda' < \lambda/2$, i.e. $F'/F > 2$). The relative-tolerance optimal filter never windows.

---

## 8. Falsification and completeness

### 8.1 Realizability along precision

**Theorem 46 (gain realizability).** Fix $\lambda, \Sigma > 0$. A function $v : (0,\infty) \to (0,\infty)$ equals
$\sigma^2(G(\Pi), \Pi)$ for some continuous gain schedule $G \ge 0$ iff $v$ is continuous and $v \ge \sigma_\star^2$
everywhere. One such gain is the upper-branch inverse $G_+(v, \Pi) = \Pi v + \sqrt{\Pi(\Pi v^2 + 2\lambda v - 2\Sigma)}$.

*Proof.* Necessity is Lemma 5. Sufficiency: $\sigma^2(G, \Pi) = v$ is $G^2 - 2\Pi vG + 2\Pi(\Sigma - \lambda v) = 0$, with roots
$G_\pm = \Pi v \pm \sqrt{\Pi(\Pi v^2 + 2\lambda v - 2\Sigma)}$; the radicand is $\ge 0$ iff $v \ge \sigma_\star^2$, so
$G_+(v(\Pi), \Pi)$ is continuous and $G_+ \ge \Pi v > 0$. $\square$

**Label:** Theorem (proved; T10.1 symbolic, T10.2 101/101 constructions).

**Corollary 47 (forced lower ray).** For every continuous gain schedule and every $R^2 < F$, the failure set contains
$(0, \pi_R)$ with $\pi_R = 2\lambda(F - R^2)/R^4$. Hence $\ell = 1$: at a tolerance tighter than the floor no gain gives
Empty, a pure window, an upper ray alone, or any class with $\ell = 0$.

*Proof.* $\sigma_\star^2$ decreases strictly from $F$ and equals $R^2$ at $\pi_R$ (solve $\Pi R^4 + 2\lambda R^2 - 2\Sigma = 0$);
for $\Pi < \pi_R$, $\sigma^2 \ge \sigma_\star^2 > R^2$. $\square$

**Label:** Corollary (proved; T10.1 with the factor-radicand route, T10.2 24/24 forbidden targets blocked).

Reading: "windows need loose tolerances" holds for every gain schedule, with no regularity assumption.

**Corollary 48 (exact class set along precision).** For continuous, piecewise strictly monotone variance curves: for
$R^2 < F$ the achievable classes are exactly those with $\ell = 1$ (any $u$, any finite $k$, including All); for $R^2 \ge F$
every class with finite $k$ is achievable.

*Proof.* Impossibility is Corollary 47. Achievability: by Theorem 46 it suffices to build a continuous piecewise-monotone
$v \ge \sigma_\star^2$ with the target class: for $R^2 < F$, follow $\sigma_\star^2$ on $(0, \pi_R]$ and then a zigzag (in
$\log\Pi$) with troughs at $R^2$ and peaks above it; for $R^2 \ge F$, troughs at $F$ and peaks above $R^2$, starting above $R^2$
(for $\ell = 1$) or on $\sigma_\star^2$ (for $\ell = 0$). For All, $v = \sigma_\star^2 + R^2$. $\square$

**Label:** Corollary (proved; T10.2, 101/101 targets realized, 24/24 forbidden targets blocked).

**Corollary 49 (unbounded complexity inside the model).** For every $k \ge 1$ there is a $C^\infty$ gain schedule satisfying
Paper 1's regularity ($G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$; $G \to G_\infty \in (0,\infty)$) whose failure set at
$R^2 = 1.25F$ has exactly $k$ windows.

*Proof.* Take the Bayesian-weight gain $G_B$ with $1 < \kappa < 2$: $v_B = \sigma^2(G_B, \cdot) < F$ everywhere (Proposition 8),
$G_B > G^\star$ near $0$ (initial slope $\kappa F > F$) and $G_B < G^\star$ for large $\Pi$, so $G_B$ first meets $G^\star$ at some
$\Pi_c$, where $v_B$ touches $\sigma_\star^2$, and $G_B = G_+(v_B, \cdot)$ on $(0, \Pi_c)$. Choose $k$ disjoint closed intervals inside $(0, \Pi_c)$ and on each
define $v = v_B + b$ with $b \ge 0$ smooth, equal to $0$ near the interval's ends, such that $v$ is strictly increasing up to a
peak value $1.5F$ and strictly decreasing after it. This is possible because $v_B$ is smooth and strictly decreasing there
($\kappa < 2$, Proposition 8): on the rising flank take $b' > |v_B'|$, on the falling flank $b' \le 0$. Set $v = v_B$ elsewhere,
$G = G_+(v, \cdot)$ on $(0, \Pi_c)$ and $G = G_B$ beyond. Outside the bump intervals $G = G_B$, so $G$ is smooth and inherits
Paper 1's regularity at both ends; each bump is strictly increasing then strictly decreasing, so it crosses $1.25F$ exactly twice, and
$v_B < F$ elsewhere. $\square$

**Label:** Corollary (proved; T10.2 supplementary construction, $k = 1, \dots, 5$, $G(10^{12})/G(10^{11}) - 1 = 6\times10^{-10}$).
The upper branch alone cannot give a convergent gain: if $v \to H > 0$ then $G_+/\Pi \to 2H$.

**Corollary 50 (what regularity pins).** Under Paper 1's regularity, $L_- = F$ and $L_+ = H = \Sigma/(\lambda + G_\infty)$. So
$\ell$ is fixed by $R^2$ versus $F$ (plus the approach direction at $R^2 = F$), $u$ by $R^2$ versus $H$, and $k$ is unbounded
(Corollary 49); since $H < F$, there is never an upper ray at $R^2 \ge F$.

**Label:** Corollary (proved).

Reading: along precision the model rules out exactly one thing, being better than optimal; every further restriction is a
property of the gain family.

### 8.2 Natural gain families along precision

**Lemma 51 (excess components).** $\{\sigma^2 > F\} = \{G/\Pi > 2F\}$ pointwise. Hence at $R^2 = F$ the failure set is the
excess set; for $R^2 \ge F$ every failure component lies in an excess component; and if $G/\Pi$ is unimodal or decreasing
there is at most one window at $R^2 = F$.

**Label:** Lemma (proved; Corollary 4).

**Lemma 52 (elasticity form).** For any differentiable $G(\Pi) > 0$ with elasticity $\varepsilon = \Pi G'/G$,
$$
\frac{d\sigma^2}{d\Pi} = \frac{G\,N}{2\Pi^2(\lambda + G)^2},
\qquad
N = \varepsilon\,(G^2 + 2\lambda G - 2\Sigma\Pi) - G(\lambda + G).
$$
Turning points of $\sigma^2(\Pi)$ are the sign changes of $N$. When $G$ is strictly monotone, $N$ is a function of $G$ alone.

*Proof.* $d\sigma^2/d\Pi = \partial_G\sigma^2\,G' + \partial_\Pi\sigma^2 =
\frac{(G^2 + 2\lambda G - 2\Sigma\Pi)G'}{2\Pi(\lambda + G)^2} - \frac{G^2}{2\Pi^2(\lambda + G)}$; use $\Pi G' = \varepsilon G$. $\square$

**Label:** Lemma (proved; T10.1(a)).

**Lemma 53 (bounded gains approach $H$ from above).** If $G < G_\infty$ everywhere, then
$\sigma^2 \ge \Sigma/(\lambda + G) > H$, so $H$ is approached from above and never attained.

**Label:** Lemma (proved).

**Proposition 54 (misspecified Kalman gain).** Let $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma'\Pi}$, $F' = \Sigma'/\lambda'$,
$r = \Sigma/\Sigma'$. If $F' > 2F$, $\sigma^2$ has exactly one turning point, a maximum, at the gain
$$
G_M = \frac{-2r\lambda' + \sqrt{4r^2\lambda'^2 + 2(1 + r)\lambda'(\lambda - 2r\lambda')}}{1 + r},
\qquad \Pi_M = \frac{G_M^2 + 2\lambda'G_M}{2\Sigma'};
$$
if $F' \le 2F$ it is strictly decreasing. $L_- = F$ (from above iff $F' > 2F$), $L_+ = 0$. Classes: $F' > 2F$: lower ray
($0 < R^2 \le F$), window ($F < R^2 < M$), Empty ($R^2 \ge M$); otherwise lower ray ($R^2 < F$), Empty ($R^2 \ge F$). All never
occurs.

*Proof.* $\Pi(G) = (G^2 + 2\lambda'G)/(2\Sigma')$ and $\varepsilon = (G + 2\lambda')/(2(G + \lambda'))$, so by Lemma 52
$N = \frac{G}{2(G + \lambda')}q(G)$ with $q(G) = -(1 + r)G^2 - 4r\lambda'G + 2\lambda'(\lambda - 2r\lambda')$, strictly decreasing
on $G > 0$ with $q(0) > 0$ iff $F' > 2F$. As $\Pi \to \infty$, $G^2/(2\Pi) \to \Sigma'$ while $G \to \infty$, so $\sigma^2 \to 0$; the
direction at $0$ follows from Lemma 51 since $G/\Pi \to F'$. $\square$

**Label:** Proposition (proved; T10.1 with the factor-radicand route, T10.3 2,000/2,000 sets; T13 C2 row 3).

At over-weighting ratio 100 ($F'/F = \kappa = 100$, with $\lambda = \lambda' = c = 1$, $\Sigma = 0.01$) the peak is $M/F = 17.575$ against $9.2875$ for the Bayesian-weight gain, a ratio of $1.892$
(Paper 1: "about twice"). The onset matches the Bayesian-weight onset with $\kappa \to F'/F$.

**Proposition 55 (capped gain).** For $G = \min(g\Pi, c)$: on the linear branch
$d\sigma^2/d\Pi = g(g\lambda/2 - \Sigma)/(\lambda + g\Pi)^2$, of constant sign $g - 2F$; on the capped branch $\sigma^2$ is strictly
decreasing. So: $g > 2F$, one maximum at the kink $\Pi = c/g$; $g < 2F$, strictly decreasing; $g = 2F$, a plateau
$\sigma^2 \equiv F$ on $(0, c/g]$, then strictly decreasing (Theorem 3: All for $R^2 \le H$, lower ray for $H < R^2 < F$, Empty for $R^2 \ge F$). Classes:
All, lower ray, window, Empty.

**Label:** Proposition (proved; T10.3, T10.5; T13 C2 row 4).

**Proposition 56 (precision-blind gain).** For $G = G_0$, $\sigma^2$ decreases strictly from $\infty$ to $H$. Classes: All
($R^2 \le H$), lower ray ($R^2 > H$).

**Label:** Proposition (proved; T10.3; T13 C2 row 5).

**Theorem 57 (Hill gain, every real $n > 1$).** Let $G = c\Pi^n/(\Pi^n + \Pi_0^n)$ with $n > 1$, $t = \Pi/\Pi_0$, $T = t^n$, and
$$
P_n(T) = -(\lambda + c)T^2 + (n - 1)(c + 2\lambda)T + (2n - 1)\lambda,
\qquad
\varphi_n(t) = \frac{t^{n-1}P_n(t^n)}{(1 + t^n)^2}.
$$
(a) $\sigma^2$ has either no turning point or exactly two, a minimum followed by a maximum. The pair exists iff
$\Pi_0 < \Pi_0^{\text{pair}}(n) = c\,\varphi_n(t^*)/(2n\Sigma)$, where $t^*$ is the unique maximizer of $\varphi_n$; at equality
there is a single degenerate stationary point.

(b) For $n = 2$: $t^{*2} = 2\sqrt3 - 3$ and
$$
\Pi_0^{\text{pair}} = \frac{c\,\varphi_*}{4\Sigma},
\qquad
\varphi_* = \frac{t^*\big(\lambda(16\sqrt3 - 24) + c(14\sqrt3 - 24)\big)}{16 - 8\sqrt3}.
$$

*Proof.* With $\varepsilon = n/(1 + T)$, Lemma 52 gives $N(1 + T)^3 = c\,T\,P_n(T) - 2n\Sigma\Pi_0\,t\,(1 + T)^2$, so
$\operatorname{sign}N = \operatorname{sign}\big(c\varphi_n(t)/(2n) - \Sigma\Pi_0\big)$. As a function of $T$,
$\varphi_n = T^aP_n(T)/(1 + T)^2$ with $a = (n - 1)/n \in (0, 1)$, and
$d\varphi_n/dT = T^{a-1}R(T)/(1 + T)^3$ with $R(T) = aP_n(1 + T) + T(1 + T)P_n' - 2TP_n$. Writing
$P_n = p_2T^2 + p_1T + p_0$ ($p_2 = -(\lambda + c) < 0$, $p_1 = (n - 1)(c + 2\lambda) > 0$, $p_0 = (2n - 1)\lambda > 0$), the
cubic $R$ has coefficients $ap_0 > 0$, $a(p_0 + p_1) + p_1 - 2p_0$, $(a - 1)p_1 + (a + 2)p_2 < 0$ and $ap_2 < 0$. Whatever the sign
of the linear coefficient there is exactly one sign change, so by Descartes' rule $R$ has exactly one positive root: $\varphi_n$
rises from $\varphi_n(0^+) = 0$ to its maximum at $t^*$ and then decreases to $-\infty$. Near $t = 0$,
$N(1 + T)^3/t = ct^{n-1}P_n - 2n\Sigma\Pi_0(1 + T)^2 \to -2n\Sigma\Pi_0 < 0$. So $N$ is negative throughout, or changes sign
$-, +, -$: a minimum, then a maximum. For $n = 2$, $R(t^2) = -\tfrac12(t^4 + 6t^2 - 3)((\lambda + c)t^2 + \lambda)$, whose
positive root is $t^{*2} = 2\sqrt3 - 3$. $\square$

**Label:** Theorem (proved; (b) T10.1(e) and T10 proof support, 961 random sets with 0 root-count disagreements; (a) T13 A5:
symbolic identities, $\Pi_0^{\text{pair}}(n)$ regression against Task 10's table for $n = 1.5, 2, 3, 4, 8$, 5,000 random sets
with real $n \in [1.01, 10]$; T10.3 census of 10,000 sets).

At $\lambda = c = 1$, $\Sigma = 0.01$: $\Pi_0^{\text{pair}} = 30.243, 31.475, 37.820, 44.180, 62.711$ for $n = 1.5, 2, 3, 4, 8$.

**Proposition 58 (Hill gain: classification and the mixed class).** Let $H = \Sigma/(\lambda + c)$. $\sigma^2 \to F$ from below
at $0$ (since $G/\Pi \to 0 < 2F$) and $\to H$ from above at $\infty$ (Lemma 53), and $H < m < F$ when the pair exists, so two
rays never occur. With the pair and $M > F$ ($\Pi_0 < c\lambda/(4\Sigma)$ for $n = 2$, Paper 1's window onset):

| Tolerance | Class |
|---|---|
| $R^2 \le H$ | All |
| $H < R^2 < m$ | Lower ray |
| $m \le R^2 < F$ | Lower ray + window $(1,0,1)$ |
| $F \le R^2 < M$ | Window |
| $R^2 \ge M$ | Empty |

With the pair and $M \le F$: All ($R^2 \le H$), lower ray ($H < R^2 < m$), $(1,0,1)$ ($m \le R^2 < M$), lower ray
($M \le R^2 < F$), Empty ($R^2 \ge F$). Without the pair: All, lower ray ($H < R^2 < F$), Empty ($R^2 \ge F$).

**Label:** Proposition (proved, from Theorems 2 and 57; T10.4, 4,868 two-turning-point sets, 77,888 tolerances, 0 mismatches;
T13 C2 rows 6–7).

The mixed class is practically narrow: the band width $(\min(M, F) - m)/F$ has median $5\times10^{-4}$ (range
$4\times10^{-22}$ to $0.96$), and in 16% of sets the mixed band exists without any window above $F$.

**Numerical result 59 (two-stage gains).** Sums of two widely separated natural stages produce more than one maximum:
two-channel Bayesian gains show (max, min, max) in 7 of 2,000 sets, i.e. multi-window failure sets; two-channel Hill gains show
(min, max, min, max) in 63 of 2,000 sets, i.e. mixed multi-window failure sets. No turning-point bound is known. For the
Bayesian sums the windows always lie above $F$ and never join a lower ray (Proposition 7).

**Label:** Numerical result (T10.3 exploratory census; T13 C2 rows 8–9).

### 8.3 Degeneracies

**Corollary 60 (equal-height maxima).** If two interior maxima share the value $M_2$, are separated by a lower minimum, and
just below $M_2$ each lies in a component touching neither end (the equality condition of Theorem 2(c)), then just below $M_2$ both count in $k$, and at and above $M_2$ both windows are gone: $k$ drops by 2 at one tolerance. The
class is otherwise unaffected.

*Proof.* Theorem 2(c),(d). $\square$

**Label:** Corollary (proved; T10.5: $k = 2$ just below, Empty at and above, both routes). Families with at most one maximum
cannot produce this.

**Corollary 61 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a
flat-topped maximum acts as a maximum.

*Proof.* By Theorem 2(d) the class depends only on the ordered turning-point values, the endpoint limits and the approach
directions. $\square$

**Label:** Corollary (proved; T10.5: 1,000 tolerances, identical classes with and without the inflection).

**Proposition 62 (pair birth).** If a minimum–maximum pair is born at $\theta_0$ through a nondegenerate fold of $N$, then at
distance $\delta$ from $\theta_0$ the turning-point positions separate like $\delta^{1/2}$ and the values like
$M - m \sim \delta^{3/2}$; the band of tolerances that sees the pair opens continuously from zero width.

*Proof.* Near the fold $d\sigma^2/d\theta \approx a(x^2 - b\delta)$ in a local coordinate $x$; its roots are $\pm\sqrt{b\delta}$ and
the value change between them is $\tfrac43a(b\delta)^{3/2}$. $\square$

**Label:** Proposition (proved under nondegeneracy; T10.5 diagnosis, Hill $n = 2$: fitted exponents $1.50007$ (values) and
$0.50002$ (positions)).

**Numerical result 63 (narrow windows need root-finding).** Windows of relative width $10^{-8}$ were found by the root-finding
classifier in 20/20 curves (55 windows); a $10^4$-point log grid found none.

**Label:** Numerical result (T10.5).

**Numerical result 64 (blind searches find no unpredicted class).** Randomized searches with tolerances concentrated near every
critical tolerance found no class outside the predicted sets: $10^6$ classifications over the precision, design and $\tau$
sweeps; $4.4\times10^6$ over the $\Delta t$ and $\Sigma$ sweeps; and the T13 audit of every synthesis-matrix row.

**Label:** Numerical result (T10.7, T12 Part C, T13 C2).

---

## 9. The optimality theorem

**Scope: observation sweeps.** The signal $s$ is the same stationary OU process for every $\theta$; only the observation
process $Y_\theta$, jointly stationary with $s$, changes. The optimal filtering error is
$P(\theta) = \mathbb E[(s(t) - \mathbb E[s(t) \mid Y_\theta(u), u \le t])^2]$.

**Definition 65 (causal garbling).** $\theta_1 \preceq_c \theta_2$ ("$\theta_2$ is causally at least as informative") if there are a
random element $U$ independent of $(s, Y_{\theta_2})$ and a process $Y'$ with $Y'(u \le t)$ measurable with respect to
$\mathcal G_t = \sigma(Y_{\theta_2}(u \le t)) \vee \sigma(U)$ for every $t$, such that $(s, Y') \overset{d}{=} (s, Y_{\theta_1})$.

**Label:** Definition (Stage 4).

**Theorem 66 (monotonicity under causal garbling).** If $\theta_1 \preceq_c \theta_2$, then $P(\theta_2) \le P(\theta_1)$.

*Proof.* Equality of joint laws gives $P(\theta_1) = \mathbb E[(s(t) - \mathbb E[s(t) \mid Y'(\le t)])^2]$. Since
$\sigma(Y'(\le t)) \subseteq \mathcal G_t$, conditioning on the larger $\sigma$-field cannot increase mean-square error, and because
$U$ is independent of $(s, Y_{\theta_2})$, $\mathbb E[s(t) \mid \mathcal G_t] = \mathbb E[s(t) \mid Y_{\theta_2}(\le t)]$. $\square$

**Label:** Theorem (proved; T11.1, T11.2 Monte Carlo realization of a garbling). The argument is pointwise in $t$, so it also
holds for cyclostationary observations, and it holds for any square-integrable target measurable with respect to $s$ in place of
$s(t)$ (used in Theorem 70).

**Corollary 67 (no optimal windows along causal orderings).** If $\theta_1 < \theta_2 \Rightarrow \theta_1 \preceq_c \theta_2$ on the
whole domain, $P$ is non-increasing, so every optimal failure set is an initial segment of the domain. If moreover $P$ is
continuous (and satisfies C2′), the optimal failure set is Empty, All or a lower ray at every $R^2$; for the reverse ordering,
Empty, All or an upper ray. Windows, two rays and mixed classes are impossible.

*Proof.* A superlevel set of a non-increasing function is an initial segment; for continuous $P$ it is open, hence Empty, $D$ or
$(\theta_-, x)$; plateaus are allowed by Theorem 3. $\square$

**Label:** Corollary (proved; T11). Strict monotonicity is not needed.

**Corollary 68 (diagnostic).** Along a causally ordered sweep, a failure set with a window, two rays or a mixed class certifies
that the filter is not optimal. With Theorem 46, the precision-sweep picture is complete: the optimal filter sits on the envelope
$\sigma_\star^2$ (classes lower ray and Empty), and every curve strictly above it belongs to some miscalibrated gain.

**Label:** Corollary (proved).

Reading: Paper 1's windows and the Hill mixed class are signatures of the filter, not of the environment.

**Proposition 69 (spectral dominance).** Let $y_\theta = s + \eta_\theta$ with $\eta_\theta$ stationary Gaussian, independent of $s$,
with spectral densities $S_\theta$ (white components in integrated form as constant densities).
1. If $S_{\theta_1} \ge S_{\theta_2}$ almost everywhere, then $\theta_1 \preceq_c \theta_2$.
2. Suppose $S_s > 0$. If $Y' = h * y_{\theta_2} + n$, with $h$ causal LTI and $n$ independent, realizes $\theta_1$, then
   $h = \delta$ and $S_n = S_{\theta_1} - S_{\theta_2} \ge 0$.

*Proof.* 1. Let $\xi$ be stationary Gaussian with density $S_{\theta_1} - S_{\theta_2}$, independent of everything, and
$Y' = y_{\theta_2} + \xi$. 2. The cross-spectrum of $s$ with $Y'$ is $HS_s$, which must equal $S_s$, so $H \equiv 1$; matching the
spectra of $Y'$ gives $S_n$. $\square$

**Label:** Proposition (proved; T11.1, T11.3 spectral checks on 25,000 pairs).

**Theorem 70 (non-linear causal garblings add nothing).** In the setting of Proposition 69 with $S_s > 0$ almost everywhere,
the following are equivalent: (i) $\theta_1 \preceq_c \theta_2$ by some (possibly non-linear) causal garbling; (ii)
$S_{\theta_1} \ge S_{\theta_2}$ almost everywhere; (iii) $\theta_1 \preceq_c \theta_2$ by adding independent stationary Gaussian noise; (iv) $Y_{\theta_1}$ is a (not necessarily
causal) garbling of $Y_{\theta_2}$ as whole paths (pathwise Blackwell ordering).

*Proof.* (ii) ⇒ (iii) is Proposition 69(1); (iii) ⇒ (i) and (i) ⇒ (iv) are trivial. For (iv) ⇒ (ii) the two-sided inequality
below holds directly (a garbling of the whole path cannot lower any smoothing error); for (i) ⇒ (ii): by the proof of Theorem 66 with any
square-integrable target $Z$ measurable with respect to $s$ in place of $s(t)$,
$\mathbb E[(Z - \mathbb E[Z \mid Y_{\theta_1}(\le t)])^2] \ge \mathbb E[(Z - \mathbb E[Z \mid Y_{\theta_2}(\le t)])^2]$ for every $t$. As
$t \to \infty$ the $\sigma$-fields $\sigma(Y_\theta(\le t))$ increase to $\sigma(Y_\theta(\mathbb R))$, so by Lévy's upward theorem both
sides converge to the two-sided (smoothing) errors, and the inequality survives. Take $Z = \int g(u)s(u)\,du$ with $g$ smooth and
compactly supported. Because $(s, Y_\theta)$ is jointly Gaussian, the two-sided conditional mean is linear and its error is
$\int|\hat g(\omega)|^2\,h_\theta(\omega)\,d\omega/2\pi$ with $h_\theta = S_sS_\theta/(S_s + S_\theta)$. So
$\int|\hat g|^2(h_{\theta_1} - h_{\theta_2}) \ge 0$ for every such $g$; taking $g(u) = \psi(u/L)\cos(\omega_0u)$ with $L \to \infty$
concentrates $|\hat g|^2/L$ at $\pm\omega_0$ as an approximate identity (the cross terms vanish for $\omega_0 \ne 0$, and the
spectra are even), so $h_{\theta_1} \ge h_{\theta_2}$ at every Lebesgue point. Since
$x \mapsto S_sx/(S_s + x)$ is strictly increasing where $S_s > 0$ (derivative $S_s^2/(S_s + x)^2$), $S_{\theta_1} \ge S_{\theta_2}$
almost everywhere. $\square$

**Label:** Theorem (proved; T13 A8: written proof, symbolic check of the monotone map, independent referee pass (Section 12);
literature status in Section 12). It was Conjecture 4.11 in Stage 4.

Reading: for additive stationary Gaussian noise, causal ordering, pathwise (Blackwell) ordering and pointwise spectral dominance
coincide; the one-line spectral test of Proposition 69 is exact.

**Proposition 71 (the sweeps studied).**
- (a) Precision: $S_\Pi = 1/\Pi$ decreases in $\Pi$, so the sweep is ordered (Paper 1's monotone optimal filter recovered).
- (b) Matched-zero-frequency $\tau$: $S_\tau(\omega) = (1/\Pi)/(1 + \tau^2\omega^2)$ decreases in $\tau$ at every $\omega$, so for
  $\tau_2 > \tau_1$, $\tau_1 \preceq_c \tau_2$ (information increases with $\tau$). The garbling noise has
  $$
  S_\xi(\omega) = \frac{(\tau_2^2 - \tau_1^2)\omega^2}{\Pi(1 + \tau_1^2\omega^2)(1 + \tau_2^2\omega^2)} = |H_\xi(i\omega)|^2,
  \qquad
  H_\xi(s) = \sqrt{\frac{\tau_2^2 - \tau_1^2}{\Pi}}\;\frac{s}{(1 + \tau_1s)(1 + \tau_2s)},
  $$
  a second-order process (real for $\tau_2 > \tau_1$). Theorem 18's monotonicity follows; its strictness comes from the closed form.
- (c) Matched-variance $\tau$: $S_\tau = 2v\tau/(1 + \tau^2\omega^2)$; every pair crosses (larger at $\omega = 0$ for the larger $\tau$,
  larger as $\omega \to \infty$ for the smaller), so by Theorem 70 no two values are causally ordered by any garbling, linear or not.

**Label:** Proposition (proved; T11.1, T11.3; part (c) for all garblings via Theorem 70).

**Proposition 72 (latency).** Observations $y_d(t) = s(t - d) + $ white noise of intensity $1/\Pi$, $d \ge 0$. All values of $d$ are
pathwise Blackwell-equivalent, yet the optimal filtering error is
$$
P(d) = F - e^{-2\lambda d}\big(F - \sigma_\star^2(\Pi)\big),
$$
strictly increasing in $d$. Along the latency sweep $d(\theta) = \theta e^{-\theta}$, which rises then falls, the optimal filter has a
window in $\theta$ for every $R^2 \in (\sigma_\star^2, P(1/e))$; the causal order ($d_1 < d_2 \Rightarrow d_2 \preceq_c d_1$) reverses at
$\theta = 1$, where the window sits. Classes along $\theta$: All ($R^2 \le \sigma_\star^2$), window, Empty ($R^2 \ge P(1/e)$).

*Proof.* By the OU property $s(t) = e^{-\lambda d}s(t - d) + $ an independent innovation of variance $F(1 - e^{-2\lambda d})$, and
$s(t - d)$ is filtered with error $\sigma_\star^2$. $P(d(\theta)) > \sigma_\star^2$ for every $\theta > 0$, with limit $\sigma_\star^2$ at both
ends and a single maximum at $\theta = 1$. $\square$

**Label:** Proposition (proved; T11.4, Monte Carlo $|z| \le 1.91$; T13 C2 row 20). Example ($\lambda = 1$, $\Sigma = 0.01$,
$\Pi = 1$): $P(0) = 0.0099505$, $P(1/e) = 0.0099763$.

**Counterexample 73 (analytic; pathwise ordering is not enough).** Proposition 72 is a sweep of pathwise Blackwell-equivalent
experiments along which the optimal filtering error is non-monotone, so "Blackwell ordering (pathwise) implies monotone filtering
error" is false; Definition 65 must be causal.

**Label:** Counterexample (analytic; T11.4).

**Proposition 74 (ordering is sufficient, not necessary).** Along matched-variance $\tau$ restricted to $(1/\lambda, \infty)$, $P$ is
strictly decreasing (Proposition 22), yet no two values are causally ordered by any garbling (Proposition 71(c)). So monotone optimal
error does not require an information ordering.

**Label:** Proposition (proved; T11.5, 1,000/1,000 sets; all garblings via Theorem 70).

**Answer to the Stage 4 question.** Along any causally ordered environment sweep, an optimal filter's failure set is Empty, All or a
single ray at the less-informative end; every other class certifies a miscalibrated filter (Corollaries 67–68). Ordering is exactly
sharp in the power-normalized family (Theorem 25) and sufficient but not necessary in general (Proposition 74); causality is
essential (Counterexample 73); and for additive Gaussian noise the ordering is decided by the spectra alone (Theorem 70).

---

## 10. Final synthesis matrix

"#" is the row number of the Task 13 class audit (C2); "Opt." is what the optimal filter can produce along the same sweep. Classes
are written E (Empty), A (All), LR (lower ray), UR (upper ray), 2R (two rays), W (window), and triples $(\ell, u, k)$.

| # | Sweep | Kind | Gain family / filter | Endpoint limits (approach) | Extrema | Critical tolerances | Possible classes | Opt. | Conditions | Label | Verified by |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | $\Pi$ | env. | optimal | $F$ (below) → $0$ | none | $F$ | LR, E | LR, E | — | Thm 6 | Paper 1; T13 C2 |
| 2 | $\Pi$ | env. | Bayesian-weight | $F$ → $H$ (above) | one max iff $\kappa > 2$ | $H, F, M$ | A, LR, W, E | LR, E | $\kappa > 2$ for W | Prop. 8 | Paper 1; T10.3, T10.7; T13 C2 |
| 3 | $\Pi$ | env. | misspecified Kalman | $F$ → $0$ | one max iff $F' > 2F$ | $F, M$ | LR, W, E | LR, E | $F' > 2F$ | Prop. 54 | T10.3, T10.7; T13 C2 |
| 4 | $\Pi$ | env. | capped $\min(g\Pi, c)$ | $F$ → $H$ (above) | one max (kink) iff $g > 2F$; plateau at $g = 2F$ | $H, F, M$ | A, LR, W, E | LR, E | $g > 2F$ | Prop. 55 | T10.3, T10.5, T10.7; T13 C2 |
| 5 | $\Pi$ | env. | precision-blind | $\infty$ → $H$ (above) | none | $H$ | A, LR | LR, E | — | Prop. 56 | T10.3, T10.7; T13 C2 |
| 6 | $\Pi$ | env. | Hill $n = 2$ | $F$ (below) → $H$ (above) | 0, or min then max | $H, m, M, F$ | A, LR, (1,0,1), W, E | LR, E | pair iff $\Pi_0 < \Pi_0^{\text{pair}}$ | Thm 57, Prop. 58 | T10.3, T10.4, T10.7; T13 C2 |
| 7 | $\Pi$ | env. | Hill, real $n > 1$ | $F$ (below) → $H$ (above) | 0, or min then max | $H, m, M, F$ | A, LR, (1,0,1), W, E | LR, E | pair iff $\Pi_0 < \Pi_0^{\text{pair}}(n)$ | Thm 57, Prop. 58 | T10.3; T13 A5, C2 |
| 8 | $\Pi$ | env. | two-stage Bayesian | $F$ → $\Sigma/(\lambda + c_1 + c_2)$ (above) | up to 3 seen | — | A, LR, W, (0,0,2), E | LR, E | no $(1,0,k)$: minima exceed $F$ | Num. 59, Prop. 7 | T10.3; T13 C2 |
| 9 | $\Pi$ | env. | two-stage Hill | $F$ (below) → $\Sigma/(\lambda + c_1 + c_2)$ (above) | up to 4 seen | — | A, LR, (1,0,1), (1,0,2), W, (0,0,2), E | LR, E | — | Num. 59 | T10.3; T13 C2 |
| — | $\Pi$ | env. | any continuous gain | free above $\sigma_\star^2$ | any finite number | — | $R^2 < F$: exactly the classes with $\ell = 1$; $R^2 \ge F$: all | LR, E | — | Thm 46, Cor. 47–49 | T10.2 |
| 10 | $\Pi_0$ | design | Bayesian-weight | $V_c$ → $F$ (below) | one min iff $\Pi < \Pi_A$ | $\sigma_\star^2, V_c, F$ | A, 2R, LR, UR, E | n/a | cases P1–P3 | Prop. 11 | T8.3, T10.7; T13 C2 |
| 11 | $c$ | design | Bayesian-weight | $F$ (below) → $\infty$ | one min | $\sigma_\star^2, F$ | A, 2R, UR | n/a | — | Prop. 13 | T8.3, T10.7; T13 C2 |
| 12 | $\Pi_0$ (any monotone gain at fixed $\Pi$) | design | e.g. $c\tanh(\Pi/\Pi_0)$, $c(1 - e^{-\Pi/\Pi_0})$, $c\Pi^2/(\Pi^2 + \Pi_0^2)$ | $V_c$ → $F$ (below) | at most one min | — | A, 2R, LR, UR, E; never W or mixed | n/a | — | Thm 9 | T8.4; T13 C2 |
| 13 | $\tau$ (zero-freq. power) | env. | relay, any precision-only $G > 0$ | $V_w$ (below) → $H_G$ (above) | none | $H_G, V_w$ | A, LR, E | LR, E | LR at $R^2 = F$ iff $G > 2F\Pi$ | Prop. 16 | T9.4, T10.7; T13 C2 |
| 14 | $\tau$ (zero-freq. power) | env. | optimal | $\sigma_\star^2$ (below) → $0$ | none | $\sigma_\star^2$ | LR, E | LR, E | — | Thm 18, Prop. 19 | T9.4, T10.7; T13 C2 |
| 15 | $\tau$ (matched variance) | env. | relay, fixed $G > 0$ | $H_G$ → top (below) | none | $H_G$, top | A, UR, E | W, E | — | Prop. 24 | T10.6, T10.7; T13 C2 |
| 16 | $\tau$ (matched variance) | env. | optimal | $0$ → $0$ | one max at $1/\lambda$ | $P_{\max}$ | W, E | W, E | — | Prop. 22 | T10.6, T10.7; T13 C2 |
| 17 | $\tau$, power family $\beta \le 0$ | env. | optimal | $F$ ($\beta < 0$) or $\sigma_\star^2(1/K)$ ($\beta = 0$) → $0$ | none | one limit | LR, E | LR, E | ordered (info ↑) | Thm 25 | T11.3; T13 C2 |
| 18 | $\tau$, power family $0 < \beta < 2$ | env. | optimal | $0$ → $0$ | exactly one max | $\max P$ | W, E | W, E | not ordered | Thm 25, Thm 26 | T11.3; T13 A4, C2 |
| 19 | $\tau$, power family $\beta \ge 2$ | env. | optimal | $0$ → $\sigma_\star^2(\lambda^2/K)$ ($\beta = 2$) or $F$ ($\beta > 2$) | none | one limit | UR, E | UR, E | ordered (info ↓) | Thm 25 | T11.3 with diagnosis; T13 C2 |
| 20 | latency $d = \theta e^{-\theta}$ | env. | optimal | $\sigma_\star^2$ (above) → $\sigma_\star^2$ (above) | one max at $\theta = 1$ | $\sigma_\star^2, P(1/e)$ | A, W, E | A, W, E | pathwise-equivalent, causally reversing | Prop. 72 | T11.4; T13 C2 |
| 21 | $\Delta t$ (M-P) | either | optimal, post | $\sigma_\star^2$ → $0$ | none | $\sigma_\star^2$ | LR, E | LR, E | — | Thm 33(a) | T12; T13 C2 |
| 22 | $\Delta t$ (M-P) | either | optimal, prior | $\sigma_\star^2$ → $F$ (below) | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 33(b) | T12; T13 A1, C2 |
| 23 | $\Delta t$ (M-P) | either | optimal, avg | $\sigma_\star^2$ → $F$ (below) | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 33(c) | T12; T13 A2, C2 |
| 24 | $\Delta t$ (M-P) | either | D1 sampled relay, post | $\sigma^2(G, \Pi)$ → $0$ | none or one max | limits, max | E, LR, W | — | excess iff $G > 2F\Pi$ | Prop. 29; Num. 38 | T12; T13 C2 |
| 25 | $\Delta t$ (M-P) | either | D1, prior | $\sigma^2(G, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | 2R if $G > 2F\Pi$ (Proposition 37) | Prop. 37; Num. 38 | T12; T13 C2 |
| 26 | $\Delta t$ (M-P) | either | D1, avg | $\sigma^2(G, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | 2R if $G > 2F\Pi$ (Proposition 37); also seen for $G \le 2F\Pi$ (Numerical result 38) | Prop. 37; Num. 38 | T12; T13 C2 |
| 27 | $\Delta t$ (M-P) | either | D2 discrete Bayesian, post | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $(1-c)^2F$ | none, max, min, min–max | limits, extrema | A, E, LR, UR, 2R, W, (1,0,1) | — | excess iff $\kappa > 2$ | Prop. 30; Num. 38 | T12; T13 C2 |
| 28 | $\Delta t$ (M-P) | either | D2, prior | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 30; Num. 38 | T12; T13 C2 |
| 29 | $\Delta t$ (M-P) | either | D2, avg | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 30; Num. 38 | T12; T13 C2 |
| 30 | $\Delta t$ (M-P) | either | D3 over-trust $\rho$, post | $\sigma^2(G_\rho, \Pi)$ → $0$ | none or one max | limits, max | E, LR, W | — | excess near 0 iff $\rho > 2 + u$ | Prop. 31; Num. 38 | T12; T13 C2 |
| 31 | $\Delta t$ (M-P) | either | D3, prior | $\sigma^2(G_\rho, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | — | Prop. 31; Num. 38 | T12; T13 C2 |
| 32 | $\Delta t$ (M-P) | either | D3, avg | $\sigma^2(G_\rho, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 31; Num. 38 | T12; T13 C2 |
| 33 | $\Delta t$ (M-I) | either | optimal, (a) | $\sigma_\star^2$ → $F$ | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 36 | T11.6, T12; T13 A3, C2 |
| 34 | $\Delta t$ (M-I) | either | optimal, (b) | $\sigma_\star^2$ → $F$ | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 36 | T11.6, T12; T13 A3, C2 |
| 35 | $\Sigma$, absolute | env. | $\Sigma$-independent gain | $G^2/(2\Pi(\lambda+G))$ (above) → $\infty$ | none | lower limit | A, UR | UR | — | Prop. 41 | T12; T13 C2 |
| 36 | $\Sigma$, relative | env. | $\Sigma$-independent gain | $\infty$ → $1/(1+g)$ | none | $1/(1+g)$ | A, LR | LR, E | excess iff $\Sigma < \lambda G/(2\Pi)$ | Prop. 41 | T12; T13 C2 |
| 37 | $\Sigma$, absolute | env. | $\Sigma$-tracking, over-trust $\rho$ | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 42 | T12; T13 C2 |
| 38 | $\Sigma$, relative | env. | $\Sigma$-tracking, over-trust $\rho$ | $1$ → $0$ | one max iff $\rho > 2$ | $1$, peak | LR, W, E | LR, E | W iff $\rho > 2$ | Prop. 42 | T12; T13 C2 |
| 39 | $\Sigma$, absolute | env. | $\Sigma$-tracking, misspecified $\lambda'$ | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 43 | T12; T13 C2 |
| 40 | $\Sigma$, relative | env. | $\Sigma$-tracking, misspecified $\lambda'$ | $1$ → $0$ | one max iff $\lambda' < \lambda/2$ | $1$, peak | LR, W, E | LR, E | W iff $\lambda' < \lambda/2$ | Prop. 43 | T12; T13 C2 |
| 41 | $\Sigma$, absolute | env. | optimal | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 44 | T12; T13 C2 |
| 42 | $\Sigma$, relative | env. | optimal | $1$ → $0$ | none | $1$ | LR, E | LR, E | — | Prop. 44 | T12; T13 C2 |

Rows 1–20 and 35–42 are complete classifications (every class at every tolerance determined, impossibilities proved), except rows
8–9 (two-stage gains, numerical). Rows 21–23 are complete. Rows 33–34 are complete. Rows 24–32 give proved excess sets and limits; their class lists are
numerical.

---

## 11. Open problems

1. **Turning points of sampled relays** (Conjecture 39). *Statement:* D1–D3 have at most two turning points along $\Delta t$ in every
   metric. *Evidence:* Task 12's census (6,000 sets × 3 metrics) and the Task 13 audit (9,000 new curves): never more than two.
   *Best partial result:* proved endpoint asymptotics (Proposition 32) and a single excess component (Propositions 29–31). The
   fixed-gain $P^+$ mixes two exponential rates with $1/\Delta t$, which defeats the polynomial methods used elsewhere.
2. **Two-stage gains** (Numerical result 59). *Statement:* a bound on the number of turning points of sums of natural stages.
   *Evidence:* at most 3 (Bayesian) and 4 (Hill) turning points in 2,000 sets each. *Best partial result:* none beyond Corollary 49
   (arbitrarily many windows for constructed gains).
3. **A necessary condition for monotone optimal error.** Ordering is exactly sharp in the power family (Theorem 25) but not
   necessary in general (Proposition 74). Is there a tidy necessary condition, for instance a one-sided spectral-crossing
   condition, beyond that family?
4. **The fixed α–β filter and multivariate models** (Stage 6). The α–β filter is two-state and does not fit the scalar model;
   the decoupled multivariate case should split into scalar copies, the mixing case is open.

---

## 12. Verification appendix

Verification tasks: T8 (`REPORT.md`, Stage 0–1), T9 (`t9/RESULTS_t9.md`, Stage 2 $\tau$), T10 (`t10/RESULTS_t10.md`, Stage 3),
T11 (`t11/RESULTS_t11.md`, Stage 4), T12 (`t12/RESULTS_t12.md`, Stage 2 completion), T13 (`t13/RESULTS_t13.md`, this document).
Pre-registrations: `PREREG_t8.md` … `PREREG_t13.md`. Paper 1's results carry Paper 1's own verification (`verification/`).
Every failed pre-registered check in T8–T13 stays recorded in its report with a diagnosis; none changed a class or a result
below except where the change log says so.

| No. | Kind | Result | Verified by |
|---|---|---|---|
| 1 | Proposition | topological realizability | T8.5 |
| 2 | Theorem | critical-tolerance theorem | T8.1, T8.3; T9–T13 classifiers |
| 3 | Theorem | plateaus | T10.5 |
| 4 | Corollary | excess identity | Paper 1; T8.1 |
| 5 | Lemma | single minimum in the gain | T8.1 |
| 6 | Theorem | window theorem; optimal monotone along $\Pi$ | Paper 1; T13 C2 |
| 7 | Proposition | no mixed class when $G/\Pi$ decreases | T13 C2 (row-8 diagnosis) |
| 8 | Proposition | Bayesian-weight along $\Pi$ | Paper 1; T10.3, T10.7; T13 C2 |
| 9 | Theorem | monotone gain sweeps cannot window | T8.4; T13 C2 |
| 10 | Proposition | prior precision: endpoints, extrema | T8.1, T8.2 |
| 11 | Proposition | prior precision: classification | T8.3; T13 C2 |
| 12 | Proposition | coupling: endpoints, extrema | T8.1, T8.2 |
| 13 | Proposition | coupling: classification | T8.3; T13 C2 |
| 14 | Lemma | relay variance, zero-frequency $\tau$ | T9.1 |
| 15 | Proposition | relay endpoints, monotone | T9.1, T9.4 |
| 16 | Proposition | relay classification | T9.4; T13 C2 |
| 17 | Proposition | optimal stationary error, zero-frequency $\tau$ | T9.1, T9.2 (Wiener route; ARE route via diagnosis) |
| 18 | Theorem | optimal decreasing in $\tau$ | T9.1, T9.5 |
| 19 | Proposition | optimal classification along $\tau$ | T9.4; T13 C2 |
| 20 | Proposition | best constant-gain relay | T9.5 (with mp diagnosis) |
| 21 | Proposition | strict gap $P < V$ | T13 A7 |
| 22 | Proposition | optimal filter at matched variance | T10.6; T13 C2 |
| 23 | Counterexample | optimal filter windows | T10.6 |
| 24 | Proposition | relay at matched variance | T10.6; T13 C2 |
| 25 | Theorem | sharpness in the power family | T11.3 (with diagnosis); T13 C2 |
| 26 | Theorem | unimodality, $0 < \beta < 2$ | T13 A4; T11.3 (numerical) |
| 27 | Proposition | duality | T11.1, T11.3 |
| 28 | Lemma | shared excess set (M-P) | T12 |
| 29 | Proposition | D1 tanh lemma | T12 |
| 30 | Proposition | D2 excess set | T12 |
| 31 | Proposition | D3 excess set, onset $\rho > 2 + u$ | T12 |
| 32 | Proposition | endpoint limits along $\Delta t$ | T12 (with series-route diagnosis) |
| 33 | Theorem | optimal M-P along $\Delta t$ | T12 (a); T13 A1, A2 (b), (c) |
| 34 | Proposition | M-P not a causal-garbling family | T12 |
| 35 | Corollary | M-I nested grids | T11.6 |
| 36 | Theorem | M-I continuum monotone | T13 A3; T11.6, T12 |
| 37 | Proposition | two rays from over-weighted sampled relay | T12 (with diagnosis) |
| 38 | Numerical result | census of sampled relays | T12; T13 C2 |
| 39 | Conjecture | at most two turning points (sampled relays) | T12; T13 A6, C2 |
| 40 | Lemma | scaling lemma | T12 |
| 41 | Proposition | $\Sigma$-independent gain | T12; T13 C2 |
| 42 | Proposition | $\Sigma$-tracking, over-trust $\rho$ | T12; T13 C2 |
| 43 | Proposition | $\Sigma$-tracking, misspecified $\lambda'$ | T12; T13 C2 |
| 44 | Proposition | optimal along $\Sigma$ | T12; T13 C2 |
| 45 | Proposition | signal sweeps | T11.1 |
| 46 | Theorem | gain realizability | T10.1, T10.2 |
| 47 | Corollary | forced lower ray | T10.1 (factor-radicand route), T10.2 |
| 48 | Corollary | exact class set along $\Pi$ | T10.2 |
| 49 | Corollary | unbounded complexity | T10.2 (supplementary) |
| 50 | Corollary | what regularity pins | T10 (derivation) |
| 51 | Lemma | excess components | T8.1 (Corollary 4) |
| 52 | Lemma | elasticity form | T10.1 |
| 53 | Lemma | bounded gains approach $H$ from above | T10.3, T10.7 |
| 54 | Proposition | misspecified Kalman | T10.1, T10.3; T13 C2 |
| 55 | Proposition | capped gain | T10.3, T10.5; T13 C2 |
| 56 | Proposition | precision-blind gain | T10.3; T13 C2 |
| 57 | Theorem | Hill gain, every real $n > 1$ | T10.1, T10.3 ($n = 2$); T13 A5 |
| 58 | Proposition | Hill classification, mixed class | T10.4; T13 C2 |
| 59 | Numerical result | two-stage gains | T10.3; T13 C2 |
| 60 | Corollary | equal-height maxima | T10.5 |
| 61 | Corollary | degenerate stationary points | T10.5 |
| 62 | Proposition | pair birth | T10.5 (with diagnosis) |
| 63 | Numerical result | narrow windows need root-finding | T10.5 |
| 64 | Numerical result | blind searches | T10.7, T12 Part C, T13 C2 |
| 65 | Definition | causal garbling | — |
| 66 | Theorem | monotonicity under causal garbling | T11.1, T11.2 |
| 67 | Corollary | no optimal windows along causal orderings | T11 |
| 68 | Corollary | diagnostic | T11 |
| 69 | Proposition | spectral dominance | T11.1, T11.3 |
| 70 | Theorem | non-linear causal garblings add nothing | T13 A8 |
| 71 | Proposition | the sweeps studied | T11.1, T11.3 |
| 72 | Proposition | latency | T11.4; T13 C2 |
| 73 | Counterexample | pathwise ordering is not enough | T11.4 |
| 74 | Proposition | ordering sufficient, not necessary | T11.5 |

**Route notes.** Three Task 8–12 identities reduce to 0 only by documented fallback routes (Task 10: two $\sqrt{x^2} = x$ items,
reduced by factoring the radicand under the stated sign condition; Task 12: the D2 $O(1/\Delta t)$ coefficient, by the series route
after `sympy.limit` returned 0). In Task 13, two Part A identities (the sign of $-sFr$ in Theorem 33(b) and the $\sinh$ identity in
Theorem 33(c)) needed a post-hoc rewrite route (`rewrite(exp)`, explicit positive series); the pre-registered check recorded them as
route failures.

**Literature (Theorem 70).** The static analogue is classical: for linear normal experiments with known noise, Blackwell
ordering is equivalent to Loewner ordering of the information matrices (Hansen and Torgersen, *Ann. Statist.* 2 (1974)
367–373; Torgersen, *Comparison of Statistical Experiments*, 1991). A targeted search (Task 13, `t13/literature_check.md`)
found no statement for stationary Gaussian processes ordered by spectral density and nothing on a causal garbling order in
filtering, so Theorem 70 is proved here rather than cited.

**Independent referee (T13 C4).** A separate reader who saw only this document raised 14 points (two wrong condition claims in
the sampling-interval section, unproved hypotheses and missing equality rows); all were valid and are fixed (change log rows
31–44; report verbatim in `t13/referee_report.md`). The referee found no error in Theorems 2, 26, 33, 57 or 70.

---

## 13. Change log

### 13.1 Number map

| Old (document) | New |
|---|---|
| Prop. 1.1 (Stage 0–1) | Proposition 1 |
| Thm 1.2 (Stage 0–1) | Theorem 2 |
| Lemma 3.1 (Stage 0–1; header Lemma, label line "Proposition") | Lemma 5 |
| Thm 3.2 (Stage 0–1) | Theorem 9 |
| Props 4.1, 4.2 (Stage 0–1) | Propositions 10, 11 |
| Props 5.1, 5.2 (Stage 0–1) | Propositions 12, 13 |
| Lemma 2.1 (Stage 2 $\tau$) | Lemma 14 |
| Props 2.2, 2.3 (Stage 2 $\tau$) | Propositions 15, 16 |
| Prop. 3.1 (Stage 2 $\tau$) | Proposition 17 |
| Thm 3.2′ (Stage 2 $\tau$) | Theorem 18 |
| Prop. 3.3 (Stage 2 $\tau$) | Proposition 19 |
| Prop. 3.4 (Stage 2 $\tau$) | Proposition 20 |
| Num. 3.5 (Stage 2 $\tau$; strict gap) | Proposition 21 (proved, T13 A7) |
| Thm 3.1 (Stage 3) | Theorem 46 |
| Cor. 3.2–3.5 (Stage 3) | Corollaries 47–50 |
| Lemma 3.6, 3.7 (Stage 3) | Lemmas 51, 52 |
| §4 general fact (Stage 3) | Lemma 53 |
| §4.1 Bayesian reduction (Stage 3) | proof of Proposition 8 |
| Prop. 3.8 (Stage 3) | Proposition 54 |
| §4.3, §4.4 (Stage 3) | Propositions 55, 56 |
| Prop. 3.9 (Stage 3, Hill $n = 2$) | Theorem 57(b) |
| Conj. 3.10 (Stage 3, Hill $n \ne 2$) | Theorem 57(a) (proved, T13 A5) |
| §4.5 Hill classification (Stage 3) | Proposition 58 |
| §4.6 two-stage (Stage 3) | Numerical result 59 |
| Cor. 3.11, 3.12 (Stage 3) | Corollaries 60, 61 |
| Thm 3.13 (Stage 3) | Theorem 3 |
| Prop. 3.14 (Stage 3) | Proposition 62 |
| §5 narrow windows (Stage 3) | Numerical result 63 |
| adversarial question 5 / T10.7 (Stage 3) | Numerical result 64 |
| Prop. 6.1 (Stage 3) | Proposition 22 |
| Counterexample in §6 (Stage 3; "Proposition + Counterexample") | Counterexample 23 (split from Proposition 22) |
| §6 relay at matched variance (Stage 3) | Proposition 24 |
| Def. 4.1 (Stage 4) | Definition 65 |
| Thm 4.2 (Stage 4) | Theorem 66 |
| Cor. 4.3 (Stage 4) | Corollary 67 |
| Cor. 4.10 (Stage 4; numbered before 4.9) | Corollary 68 |
| Prop. 4.4 (Stage 4) | Proposition 69 |
| Conj. 4.11 (Stage 4) | Theorem 70 (proved, T13 A8) |
| Prop. 4.5 (Stage 4) | Proposition 71 |
| Thm 4.6 (Stage 4) | Theorem 25 |
| Num. 4.6a (Stage 4) | Theorem 26 (proved, T13 A4) |
| Prop. 4.6b (Stage 4) | Proposition 27 |
| Remark on signal sweeps (Stage 4) | Proposition 45 |
| Prop. 4.7 (Stage 4; "Proposition + Counterexample") | Proposition 72 and Counterexample 73 |
| Prop. 4.8 (Stage 4) | Proposition 74 |
| Cor. 4.9 (Stage 4) | Corollary 35 |
| Num. 4.10a (Stage 4) | Theorem 36 (proved, T13 A3) |
| Lemma 2.1 (Stage 2 completion) | Lemma 28 |
| Props 2.2, 2.3, 2.4 (Stage 2 completion) | Propositions 29, 30, 31 |
| §A.3 limits table (Stage 2 completion) | Proposition 32 |
| Prop. 2.6(a), (b) (Stage 2 completion) | Theorem 33(a), (b) |
| Num. 2.6c (Stage 2 completion) | Theorem 33(c) (proved, T13 A2) |
| Prop. 2.7 (Stage 2 completion) | Proposition 34 |
| Num. 2.8 (Stage 2 completion; = Num. 4.10a) | Theorem 36 (proved, T13 A3) |
| Prop. 2.9 (Stage 2 completion) | Proposition 37 |
| Num. 2.10 (Stage 2 completion) | Numerical result 38 |
| Conj. 2.11 (Stage 2 completion) | Conjecture 39 |
| Lemma 2.12 (Stage 2 completion) | Lemma 40 |
| Props 2.13–2.16 (Stage 2 completion) | Propositions 41–44 |
| Paper 1: excess identity, window theorem, Bayesian-weight | Corollary 4, Theorem 6, Proposition 8 |

### 13.2 Corrections applied

| # | Source | Correction | Where |
|---|---|---|---|
| 1 | T8 | C4 parenthetical reversed: from above at $\theta_-$ means the first piece is **increasing**, at $\theta_+$ the last piece is **decreasing**. | C4 |
| 2 | T8 / Stage 0–1 | Lemma 3.1 carried two labels (header Lemma, label line Proposition); now Lemma 5 only. | Lemma 5 |
| 3 | T9 | Prop. 3.1 proof: the Riccati equation is multiplied by $-\tau^2R_v$, not $\tau^2$. | Proposition 17 |
| 4 | T9 | Prop. 2.2 approach directions follow from the corrected C4. | Proposition 15 |
| 5 | T9 | Worked example: $\sigma^2(10) = 0.011875$ exactly (stated as 0.01188 before, a half-unit boundary). | Section 5.1 |
| 6 | T9 | "$V(1) \approx 0.00990$" made precise: $V(1) = 0.0099010$. | Section 5.1 |
| 7 | T10 | Corollary 3.4's construction switches to the lower branch beyond an envelope touch point; bumps compactly supported. | Corollary 49 |
| 8 | T10 | "Hill sextic": $Q$ is a quintic, $tQ$ the sextic (now superseded by the general-$n$ proof). | Theorem 57 |
| 9 | T10 | Lemma 3.7 holds for any differentiable $G > 0$; monotonicity only reduces $N$ to one variable. | Lemma 52 |
| 10 | T10 | "Two rays" removed from the Hill predicted set ($\sigma^2 > H$ everywhere). | Proposition 58 |
| 11 | T10 | Fold exponents: positions $1/2$, values $3/2$. | Proposition 62 |
| 12 | T11 | Prop. 4.5(c) "not ordered by any garbling" needed Conjecture 4.11; now justified by Theorem 70. | Proposition 71(c) |
| 13 | T11 | Numbering: Cor. 4.10 appeared before Cor. 4.9; resolved by renumbering. | Corollaries 35, 68 |
| 14 | T11 | Cor. 4.3's citation of Theorem 3.13 now resolves internally. | Corollary 67 |
| 15 | T11 | Theorem 4.6: the limits of $P$ itself are stated, including $\beta = 2$: $\sigma_\star^2(\lambda^2/K)$, not $F$. | Theorem 25 |
| 16 | T11 | Prop. 4.5(b): garbling direction $\tau_2 > \tau_1$ made explicit ($H_\xi$ real only then). | Proposition 71(b) |
| 17 | T12 | D3 onset at fixed precision is $\rho > 2 + u$, not $\rho > 2$. | Proposition 31 |
| 18 | T12 | Quick-check values for D1 replaced by the computed ones (maximum $0.20457$ at $\Delta t = 2.4645$; crossing at $\Delta t_E = 100$). | Section 6.3 |
| 19 | T12 | D2 post $O(1/\Delta t)$ coefficient confirmed by the series route (`sympy.limit` failed). | Proposition 32 |
| 20 | T13 A1 | Prop. 2.6(b) verified (was "proved, unverified"). | Theorem 33(b) |
| 21 | T13 A2 | Num. 2.6c proved; label Numerical result → Theorem (part (c)). | Theorem 33(c) |
| 22 | T13 A4 | Num. 4.6a proved; label → Theorem. | Theorem 26 |
| 23 | T13 A5 | Conj. 3.10 proved for every real $n > 1$; label → Theorem. | Theorem 57 |
| 24 | T13 A7 | Strict gap $P < V$ proved; label → Proposition. | Proposition 21 |
| 25 | T13 A8 | Conj. 4.11 proved for additive stationary Gaussian noise; label → Theorem. | Theorem 70 |
| 26 | T13 A3 | Num. 2.8 / 4.10a (integrate-and-dump monotone) proved; label → Theorem. | Theorem 36 |
| 27 | Stage 3 / Stage 4 | Results with two labels ("Proposition + Counterexample", "Numerical result + Conjecture") split or relabelled: Proposition 22 + Counterexample 23; Proposition 72 + Counterexample 73; Conjecture 3.10 is now Theorem 57(a). | Sections 5.2, 8.2, 9 |
| 28 | Stage 4 | Theorem 66 noted to hold for any target measurable with respect to $s$ (needed by Theorem 70); no change to its statement. | Theorem 66 |
| 29 | T13 C1 | Worked examples: $G^\star = \sigma_\star^2 = 0.0099505$ at $\Pi = 1$ (the stage documents truncated it to 0.0099504; T8.2 had checked 4 s.f. only). | Sections 4, 5.1 |
| 30 | Stage 3 / T13 | Latency sweep classes stated in full (All for $R^2 \le \sigma_\star^2$, window, Empty); Stage 4 gave only the window. | Proposition 72 |
| 31 | T13 C4 (referee 1) | D2 requires $0 < c < 2$; the $c > 2$ case is a remark with a counterexample to the lower-ray claim. | Section 6, Proposition 30 |
| 32 | T13 C4 (referee 2) | Rows 25–26: two rays occur **if** $G > 2F\Pi$ (Proposition 37), not only then (counterexample $G = 0.019$ for avg). | Section 10, Numerical result 38 |
| 33 | T13 C4 (referee 3) | Theorem 6: above $F$ the failure set is $(0,0,k)$, $k \ge 1$, not necessarily one window. | Theorem 6 |
| 34 | T13 C4 (referee 4) | Optimal prior/avg along $\Delta t$: All for $R^2 \le \sigma_\star^2$ (equality row). | Section 6.2 |
| 35 | T13 C4 (referee 5) | Theorem 36: the M-I quadratic printed, closed form $p = 2/(1 + \sqrt{1 + 2u/k(x)})$ and both limits proved; resultant kept as second route. | Theorem 36 |
| 36 | T13 C4 (referee 6) | Proposition 31: proof added, including the cubic term at $\rho = 2 + u$; census shape moved to Numerical result 38. | Proposition 31 |
| 37 | T13 C4 (referee 7) | Proposition 37 assumes C2; Corollary 67 states the general initial-segment conclusion and adds continuity for the class list. | Proposition 37, Corollary 67 |
| 38 | T13 C4 (referee 8) | Corollary 49: bumps defined so each is strictly increasing then decreasing. | Corollary 49 |
| 39 | T13 C4 (referee 9) | Corollary 60: both maxima must lie in windows. | Corollary 60 |
| 40 | T13 C4 (referee 10) | Theorem 2(d): rule at interior critical tolerances stated; approach directions follow from the sequence. | Theorem 2 |
| 41 | T13 C4 (referee 11) | Proposition 10 first bullet reworded (only $F$ is always approached from below). | Proposition 10 |
| 42 | T13 C4 (referee 12) | Proposition 34: the min/sup/mean step made explicit. | Proposition 34 |
| 43 | T13 C4 (referee 13) | Theorem 70: part (iv) (pathwise Blackwell ordering) added; frequency-localization detail. | Theorem 70 |
| 44 | T13 C4 (referee 14) | Proposition 55, $g = 2F$: All for $R^2 \le H$ (equality row). | Proposition 55 |
| 45 | T13 C2 (row 8 failure, diagnosed) | Row 8 (two-stage Bayesian) listed $(1,0,1)$; it cannot occur. Theorem 6 gains an addendum (proved): for increasing $G$ with $G/\Pi$ strictly decreasing, every interior minimum exceeds $F$. Row 8 class set corrected; Numerical result 59 notes it. | Theorem 6, Numerical result 59, Section 10 |
