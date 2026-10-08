# Stage 2: The Correlation-Time Sweep

**John Holder** · Working results for Paper 2 · 7 October 2026 · *unverified (Task 9 pending)*

Companion to Roadmap v2 and `Stage_0_1_Classification_Results.md`. Conventions C1–C6, Theorem 1.2 and Lemma 3.1 are used as stated there. Every result carries a Section 12 label.

**Assumption (stated, not derived).** The relay's gain is set by precision alone, $G = G(\Pi)$ (e.g. the Bayesian-weight gain). Along a $\tau$ sweep at fixed $\Pi$ it is therefore a constant $G > 0$. The relay does not know the noise is coloured. ($G = 0$ is trivial: $\sigma^2 \equiv F$, so the class is All for $R^2 < F$ and Empty otherwise.) A $\tau$-dependent gain is outside this document.

---

## 1. Model at matched zero-frequency power

Sensory noise $\eta$ is Ornstein–Uhlenbeck with correlation time $\tau > 0$ and autocovariance
$$
C_\eta(u) = \frac{1}{2\Pi\tau}\,e^{-|u|/\tau},
\qquad
S_\eta(\omega) = \frac{1/\Pi}{1 + \tau^2\omega^2}.
$$
$S_\eta(0) = 1/\Pi$ for every $\tau$ (matched zero-frequency power), and $\eta \to$ white noise of intensity $1/\Pi$ as $\tau \to 0$. Note $\operatorname{Var}\eta = 1/(2\Pi\tau) \to 0$ as $\tau \to \infty$.

Domain: $\tau \in D = (0, \infty)$ (C1). White noise enters only as the limit $\tau \to 0$.

---

## 2. The relay along $\tau$

The error obeys $\dot x = -a x + G\eta + \xi_{\text{sim}}$ with $a = \lambda + G$.

**Lemma 2.1 (relay variance).**
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2}{2\Pi\,(1 + a\tau)}\right).
$$
*Proof.* The process-noise part contributes $2\Sigma/(2a)$. For the coloured part, a first-order filter $1/(s+a)$ driven by an OU input of variance $v$ and rate $1/\tau$ has output variance $v/(a(a + 1/\tau))$; with $v = G^2/(2\Pi\tau)$ this is $G^2/(2\Pi a(1 + a\tau))$. The two parts are independent. $\square$

*Check:* $\sigma^2 - F = \dfrac{G\big(\lambda G/(2\Pi(1 + a\tau)) - \Sigma\big)}{\lambda a}$, so $\sigma^2 > F \iff G/\Pi > 2F(1 + a\tau)$, which is Paper 1's coloured-noise excess condition. At $\tau \to 0$ the white-noise formula is recovered.

**Label:** Lemma (proved).

**Proposition 2.2 (endpoints, monotonicity).** For $G > 0$, $\sigma^2$ is strictly decreasing in $\tau$ on $D$ (C2 holds with no turning points), with
- $L_- = V_w := \dfrac{\Sigma + G^2/(2\Pi)}{\lambda + G}$ (the white-noise relay variance), approached **from below**;
- $L_+ = H_G := \dfrac{\Sigma}{\lambda + G}$, approached **from above**.

Always $H_G < F$; and $V_w > F \iff G > 2F\Pi$, $V_w = F \iff G = 2F\Pi$.

*Proof.* The only $\tau$-dependence is $1/(1 + a\tau)$, strictly decreasing. Approach directions follow from C4 for a decreasing function. $V_w$ versus $F$ is Lemma 3.1 at this $G$. $\square$

**Label:** Proposition (proved).

**Proposition 2.3 (complete classification, every tolerance).** Critical tolerances $\mathcal{C} = \{H_G, V_w\}$.

| Tolerance | Class |
|---|---|
| $R^2 < H_G$ | All |
| $R^2 = H_G$ | All ($H_G$ is approached from above, never attained) |
| $H_G < R^2 < V_w$ | Lower ray $(0, \tau_R)$ |
| $R^2 \ge V_w$ | Empty ($V_w$ is approached from below) |

with the boundary in closed form:
$$
\tau_R = \frac{1}{a}\left(\frac{G^2}{2\Pi\,(aR^2 - \Sigma)} - 1\right).
$$

**At the floor.** $R^2 = F$ always lies above $H_G$. Hence:
- if $G > 2F\Pi$: lower ray $(0, \tau_F)$ with $\tau_F = \dfrac{1}{a}\left(\dfrac{G}{2F\Pi} - 1\right)$;
- if $G \le 2F\Pi$: Empty.

*Proof.* Theorem 1.2 with sequence $(V_w, H_G)$ and the approach directions of Proposition 2.2. Solving $\sigma^2(\tau) = R^2$ from Lemma 2.1 gives $\tau_R$; $\tau_R > 0 \iff R^2 < V_w$, and it is finite iff $R^2 > H_G$. $\square$

**Label:** Proposition (proved).

**Reading.** At matched zero-frequency power, colouring the noise always helps a fixed-gain relay. Failure concentrates at short correlation times, i.e. near the white limit. No window, upper ray or two-ray class can occur in $\tau$ for any precision-only gain schedule. This is a fourth instance of the pattern behind Theorem 3.2: windows need the sweep to move the variance curve non-monotonically, and $\tau$ moves it monotonically.

**Worked example** ($\lambda = c = 1$, $\Sigma = 0.01$, $\Pi = \Pi_0 = 1$, so $G = 0.5$, $F = 0.01$):
$V_w = 0.090000$, $H_G = 0.0066667$, $\tau_F = 16$; $\sigma^2(1) = 0.040000$, $\sigma^2(10) = 0.011875$, $\sigma^2(16) = 0.010000$.

---

## 3. The optimal filter along $\tau$

The observation $y = s + \eta$ has no white component, so the Kalman–Bucy filter is singular. Use measurement differencing.

**Reduction.** Let $z = \dot y + y/\tau$. Since $\dot\eta + \eta/\tau = w_\eta$ (white, intensity $1/(\Pi\tau^2)$) and $\dot s = -\lambda s + w_s$ (intensity $2\Sigma$),
$$
z = h\,s + v,\qquad h = \tfrac1\tau - \lambda,\qquad v = w_s + w_\eta,
$$
with measurement intensity $R_v = 2\Sigma + 1/(\Pi\tau^2)$ and cross-intensity $\mathbb{E}[w_s v] = 2\Sigma$. Over the infinite past $y(t) = \int_{-\infty}^t e^{-(t-u)/\tau} z(u)\,du$, so $z$ and $y$ carry the same information.

**Proposition 3.1 (optimal stationary error).** The minimum-mean-square stationary error $P(\tau)$ is the positive root of
$$
(1 - \lambda\tau)^2 P^2 + \left(4\Sigma\tau + \frac{2\lambda}{\Pi}\right) P - \frac{2\Sigma}{\Pi} = 0,
$$
namely
$$
P(\tau) = \frac{4\Sigma}{\Pi\,(b + \sqrt{D})},
\qquad
b = 4\Sigma\tau + \frac{2\lambda}{\Pi},
\quad
D = b^2 + \frac{8\Sigma(1 - \lambda\tau)^2}{\Pi}.
$$
This form has no singularity at $\lambda\tau = 1$, where the equation is linear and $P = (2\Sigma/\Pi)/b$.

*Proof.* The steady-state Riccati equation with correlated noise is $0 = -2\lambda P + 2\Sigma - (hP + 2\Sigma)^2/R_v$. Expanding, $S^2 - QR_v = -2\Sigma/(\Pi\tau^2)$ and $2hS + 2\lambda R_v = 4\Sigma/\tau + 2\lambda/(\Pi\tau^2)$; multiplying by $\tau^2$ gives the quadratic. Its constant term is negative and leading coefficient non-negative, so it has exactly one positive root, written above in rationalized form. $\square$

**Label:** Proposition (proved).

**Theorem 3.2′ (monotonicity of the optimal filter in $\tau$).** $P$ is strictly decreasing on $(0, \infty)$, with
$$
\lim_{\tau\to0} P = \sigma_\star^2(\Pi) = \frac{G^\star}{\Pi},
\qquad
P(\tau) \sim \frac{1}{\Pi\tau\left(1 + \sqrt{1 + \lambda^2/(2\Sigma\Pi)}\right)} \to 0 \quad (\tau\to\infty).
$$

*Proof.* $b$ is strictly increasing in $\tau$. And
$$
\frac{dD}{d\tau} = 8\Sigma b - \frac{16\Sigma\lambda(1 - \lambda\tau)}{\Pi} = 32\Sigma^2\tau + \frac{16\Sigma\lambda^2\tau}{\Pi} > 0 \quad (\tau > 0),
$$
so the denominator $b + \sqrt D$ is strictly increasing. At $\tau = 0$: $b = 2\lambda/\Pi$, $\sqrt D = (2/\Pi)\sqrt{\lambda^2 + 2\Sigma\Pi}$, so $P = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}) = G^\star/\Pi$. For large $\tau$, $b \sim 4\Sigma\tau$ and $\sqrt D \sim 4\Sigma\tau\sqrt{1 + \lambda^2/(2\Sigma\Pi)}$. $\square$

**Label:** Theorem (proved). The asymptote lies below $\operatorname{Var}\eta = 1/(2\Pi\tau)$, as it must.

**Proposition 3.3 (optimal classification).** For $R^2 > 0$, critical tolerances $\{\sigma_\star^2\}$ (the other limit, $0$, lies outside the tolerance range):

| Tolerance | Class |
|---|---|
| $0 < R^2 < \sigma_\star^2$ | Lower ray $(0, \tau^\star_R)$ |
| $R^2 \ge \sigma_\star^2$ | Empty ($\sigma_\star^2$ is approached from below) |

with
$$
\tau^\star_R = \frac{2\lambda R^2 - 4\Sigma + \sqrt{\Delta}}{2\lambda^2 R^2},
\qquad
\Delta = 16\Sigma^2 - 16\lambda\Sigma R^2 + \frac{8\lambda^2(\Sigma - \lambda R^2)}{\Pi}.
$$
The optimal filter never produces All, a window, an upper ray or two rays along $\tau$.

*Proof.* Theorem 1.2 with Theorem 3.2′. Setting $P = R^2$ in Proposition 3.1 gives a quadratic in $\tau$ with leading coefficient $\lambda^2 R^4 > 0$ and constant term $R^4 + 2\lambda R^2/\Pi - 2\Sigma/\Pi$, which is negative iff $R^2 < \sigma_\star^2$. So there is exactly one positive root. $\square$

**Label:** Proposition (proved).

**Proposition 3.4 (best constant-gain relay).** Let $V(\tau) = \inf_{G \ge 0} \sigma^2(G, \tau)$. Then $P(\tau) \le V(\tau)$, $V$ is strictly decreasing, $V(0^+) = \sigma_\star^2$ and $V(\infty) = 0$.

*Proof.* A constant-gain relay is a causal linear estimator, so $P \le V$. $G = 0$ is never the infimizer ($\partial_G\sigma^2 = -\Sigma/\lambda^2 < 0$ there). For $\tau_1 < \tau_2$: if the infimum at $\tau_1$ is attained at $G_1 > 0$, then $V(\tau_2) \le \sigma^2(G_1, \tau_2) < V(\tau_1)$; if it is approached as $G \to \infty$, its value is $1/(2\Pi\tau_1)$ and $V(\tau_2) \le 1/(2\Pi\tau_2) < V(\tau_1)$. As $\tau \to \infty$, $\sigma^2(G, \tau) \to \Sigma/(\lambda + G)$ for each $G$, and $\inf_G$ of that is $0$. $\square$

**Label:** Proposition (proved). Whether $P < V$ strictly for all $\tau > 0$ is a **numerical result** pending (example below: $0.0098039$ versus about $0.00990$ at $\tau = 1$).

**Worked example** ($\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$): $\sigma_\star^2 = 0.0099504$; $P(1) = 0.0098039$ (the linear case $\lambda\tau = 1$); $P(10) = 0.0067813$. The fixed relay with $G = 0.5$ stays above: $0.040000$ and $0.011875$. As $\tau \to \infty$ the relay tends to $H_G = 0.0066667$ while $P \to 0$, so their ratio grows like $\tau$.

---

## 4. Consequences for Stage 4

The roadmap listed $\tau$ at matched zero-frequency power as an open, possibly non-information-ordering sweep. **The optimal filter is strictly monotone along it (Theorem 3.2′), so it produces no window.** This is proved directly, without deciding whether the $\tau$ family is Blackwell-ordered. That question stays open; if it is not, this sweep is evidence that the Stage 4 conjecture's monotonicity conclusion extends beyond information orderings.

Remaining open environment sweeps: $\Delta t$ and $\Sigma$ (moving floor).

---

## 5. Synthesis-matrix entries

| Sweep | Kind | Gain family | Endpoint limits (approach) | Extrema | Critical tolerances | Possible classes | Optimal can produce | Conditions | Label |
|---|---|---|---|---|---|---|---|---|---|
| $\tau$ | env. | any precision-only gain, $G > 0$ | $V_w$ (below) → $H_G$ (above) | none | $H_G, V_w$ | All, lower ray, Empty | — | lower ray at $R^2 = F$ iff $G > 2F\Pi$ | Proposition 2.3 |
| $\tau$ | env. | optimal (differenced Kalman–Bucy) | $\sigma_\star^2$ (below) → $0$ (above) | none | $\sigma_\star^2$ | lower ray, Empty | lower ray, Empty | none | Theorem 3.2′, Prop. 3.3 |
