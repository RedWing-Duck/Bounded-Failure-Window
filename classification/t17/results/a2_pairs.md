# Task 17 A2: statements side by side (draft vs repository source)

Extracted mechanically (PREREG_t17.md, E2). Repository text: `source/Stages_0_4_Source.md` rendered with thesis numbering and no thesis overrides; 6.5 from `source/thesis_only/tau-optimal-normal-form.md`; 6.13 from the manuscript. Classification: `a2_classification.yaml`.

## Theorem 2.4 (`plateaus`)

**Draft:**

**Theorem 2.4 (plateaus).** Under C2′ instead of C2, Theorem 2.2 holds with three changes: plateau values join the critical tolerances; at R² equal to a plateau value the plateau is excluded from 𝓕, which can split or remove components; and an end adjacent to a plateau at value L carries a ray iff R² < L.

**Repository:**

**Theorem 2.4 (plateaus).** Under C2′ instead of C2, Theorem 2.2 holds with three changes: plateau values join the critical
tolerances; at $R^2$ equal to a plateau value the plateau is excluded from $\mathcal F$, which can split or remove
components; an end adjacent to a plateau at value $L$ carries a ray iff $R^2 < L$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Corollary 2.5 (`equal-height-maxima`)

**Draft:**

**Corollary 2.5 (equal-height maxima).** Suppose two interior maxima share the value M₂, are separated by a lower minimum, and just below M₂ each lies in a component touching neither end (the equality condition of Theorem 2.2(3)). Then just below M₂ both count in k, and at and above M₂ both windows are gone: k drops by 2 at one tolerance. The class is otherwise unaffected.

**Repository:**

**Corollary 2.5 (equal-height maxima).** If two interior maxima share the value $M_2$, are separated by a lower minimum, and
just below $M_2$ each lies in a component touching neither end (the equality condition of Theorem 2.2(c)), then just below $M_2$ both count in $k$, and at and above $M_2$ both windows are gone: $k$ drops by 2 at one tolerance. The
class is otherwise unaffected.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Corollary 2.6 (`degenerate-points`)

**Draft:**

**Corollary 2.6 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a flat-topped maximum acts as a maximum.

**Repository:**

**Corollary 2.6 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a
flat-topped maximum acts as a maximum.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 2.7 (`pair-birth`)

**Draft:**

**Proposition 2.7 (pair birth).** Suppose a minimum–maximum pair is born as a family parameter passes δ = 0 through a nondegenerate fold: near the birth point, in a local coordinate x, dσ²/dθ ≈ a(x² − bδ) with a, b ≠ 0. Then for bδ > 0 the turning-point positions separate like δ^(1/2) and the values like M − m \~ δ^(3/2), so the band of tolerances that sees the pair opens continuously from zero width.

**Repository:**

**Proposition 2.7 (pair birth).** If a minimum–maximum pair is born at $\theta_0$ through a nondegenerate fold of $N$, then at
distance $\delta$ from $\theta_0$ the turning-point positions separate like $\delta^{1/2}$ and the values like
$M - m \sim \delta^{3/2}$; the band of tolerances that sees the pair opens continuously from zero width.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Lemma 6.1 (`tau-relay-variance`)

**Draft:**

**Lemma 6.1 (relay variance).**

```latex
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2}{2\Pi(1 + a\tau)}\right),
\qquad
\sigma^2 > F \iff \frac{G}{\Pi} > 2F(1 + a\tau)
```

**Repository:**

**Lemma 6.1 (relay variance).**
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2}{2\Pi(1 + a\tau)}\right),
\qquad
\sigma^2 > F \iff G/\Pi > 2F(1 + a\tau).
$$

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.2 (`tau-relay-monotone`)

**Draft:**

**Proposition 6.2 (relay: endpoints and monotonicity).** σ² is strictly decreasing in τ, from V\_w = (Σ + G²/(2Π))/(λ + G) (approached from below) to H\_G = Σ/(λ + G) (approached from above). Always H\_G < F, and V\_w > F iff G > 2FΠ.

**Repository:**

**Proposition 6.2 (relay: endpoints and monotonicity).** $\sigma^2$ is strictly decreasing in $\tau$, from
$V_w = (\Sigma + G^2/(2\Pi))/(\lambda + G)$ (approached from below) to $H_G = \Sigma/(\lambda + G)$ (approached from above).
Always $H_G < F$; $V_w > F \iff G > 2F\Pi$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.3 (`tau-relay-classes`)

**Draft:**

**Proposition 6.3 (relay: classification).** The classes are All (R² ≤ H\_G), lower ray (0, τ\_R) (H\_G < R² < V\_w) and Empty (R² ≥ V\_w), with

```latex
\tau_R = \frac{1}{a}\left(\frac{G^2}{2\Pi(aR^2 - \Sigma)} - 1\right)
```

At R² = F the class is the lower ray (0, τ\_F), τ\_F = (G/(2FΠ) − 1)/a, if G > 2FΠ, and Empty otherwise.

**Repository:**

**Proposition 6.3 (relay: classification).** All ($R^2 \le H_G$); lower ray $(0, \tau_R)$ ($H_G < R^2 < V_w$); Empty
($R^2 \ge V_w$), with
$$
\tau_R = \frac{1}{a}\left(\frac{G^2}{2\Pi(aR^2 - \Sigma)} - 1\right).
$$
At $R^2 = F$: lower ray $(0, \tau_F)$, $\tau_F = (G/(2F\Pi) - 1)/a$, if $G > 2F\Pi$; Empty otherwise.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.4 (`tau-optimal-error`)

**Draft:**

**Proposition 6.4 (optimal stationary error).** With measurement differencing \[27, 28, 45\], z = ẏ + y/τ, the optimal stationary error is the positive root of

```latex
(1 - \lambda\tau)^2 P^2 + \Big(4\Sigma\tau + \frac{2\lambda}{\Pi}\Big)P - \frac{2\Sigma}{\Pi} = 0,
\qquad
P(\tau) = \frac{4\Sigma}{\Pi\,(b + \sqrt{D})}
```

with b = 4Στ + 2λ/Π and D = b² + 8Σ(1 − λτ)²/Π. The rationalised form has no singularity at λτ = 1.

**Repository:**

**Proposition 6.4 (optimal stationary error).** With measurement differencing ($z = \dot y + y/\tau$), the optimal
stationary error is the positive root of
$$
(1 - \lambda\tau)^2P^2 + \Big(4\Sigma\tau + \frac{2\lambda}{\Pi}\Big)P - \frac{2\Sigma}{\Pi} = 0,
\qquad
P(\tau) = \frac{4\Sigma}{\Pi(b + \sqrt D)},\quad b = 4\Sigma\tau + \frac{2\lambda}{\Pi},\quad D = b^2 + \frac{8\Sigma(1-\lambda\tau)^2}{\Pi}.
$$
The rationalized form has no singularity at $\lambda\tau = 1$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Corollary 6.5 (`tau-optimal-normal-form`)

**Draft:**

**Corollary 6.5 (normalised optimal error).** With ν = 2ΣΠ/λ² and t = λτ,

```latex
\frac{P}{F} = \frac{2}{1 + \nu t + \sqrt{(1 + \nu t)^2 + \nu\,(1 - t)^2}}
```

**Repository:**

*Thesis-only text, imported verbatim from the thesis draft (`t15/input/Thesis_Draft_ch1-4.md`, §3.8, lines 435–443).*

One extension is immediate. Under matched-power coloured noise, handled by measurement differencing [27, 28, 45], Lemma 6.1 becomes a three-coordinate surface with t = λτ:

```latex
\mathcal V_\tau(\nu, q, t) = \frac{1 + \dfrac{\nu q^2}{4\,\big(1 + t\,(1 + \nu q/2)\big)}}{1 + \nu q/2},
\qquad
\frac{P}{F} = \frac{2}{1 + \nu t + \sqrt{(1 + \nu t)^2 + \nu (1 - t)^2}}
```

The second formula is the optimal filter along τ (Corollary 6.5); at t = 0 both reduce to the white-noise surface and its envelope. Chapter 6 uses them.


*Proof in the draft:* yes; *in the repository source:* no

---

## Theorem 6.6 (`tau-optimal-monotone`)

**Draft:**

**Theorem 6.6 (optimal error decreases in τ).** P is strictly decreasing on (0, ∞), with P(0⁺) = σ⋆²(Π) and P(τ) \~ 1/(Πτ(1 + √(1 + λ²/(2ΣΠ)))) → 0.

**Repository:**

**Theorem 6.6 (optimal error decreases in $\tau$).** $P$ is strictly decreasing on $(0,\infty)$, with
$P(0^+) = \sigma_\star^2(\Pi)$ and $P(\tau) \sim 1/\big(\Pi\tau(1 + \sqrt{1 + \lambda^2/(2\Sigma\Pi)})\big) \to 0$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.7 (`tau-optimal-classes`)

**Draft:**

**Proposition 6.7 (optimal: classification).** The failure set is the lower ray (0, τ⋆\_R) for 0 < R² < σ⋆², and Empty for R² ≥ σ⋆², with

```latex
\tau^\star_R = \frac{2\lambda R^2 - 4\Sigma + \sqrt{\Delta}}{2\lambda^2 R^2},
\qquad
\Delta = 16\Sigma^2 - 16\lambda\Sigma R^2 + \frac{8\lambda^2(\Sigma - \lambda R^2)}{\Pi}
```

The optimal filter never produces All, a window, an upper ray or two rays along τ.

**Repository:**

**Proposition 6.7 (optimal: classification).** Lower ray $(0, \tau_R^\star)$ for $0 < R^2 < \sigma_\star^2$; Empty for
$R^2 \ge \sigma_\star^2$, with
$$
\tau_R^\star = \frac{2\lambda R^2 - 4\Sigma + \sqrt\Delta}{2\lambda^2R^2},
\qquad
\Delta = 16\Sigma^2 - 16\lambda\Sigma R^2 + \frac{8\lambda^2(\Sigma - \lambda R^2)}{\Pi}.
$$
The optimal filter never produces All, a window, an upper ray or two rays along $\tau$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.8 (`tau-best-constant-gain`)

**Draft:**

**Proposition 6.8 (best constant-gain relay).** Let V(τ) = inf over G ≥ 0 of σ²(G, τ). Then P ≤ V, V is strictly decreasing, V(0⁺) = σ⋆² and V(∞) = 0.

**Repository:**

**Proposition 6.8 (best constant-gain relay).** Let $V(\tau) = \inf_{G \ge 0}\sigma^2(G, \tau)$. Then $P \le V$, $V$ is
strictly decreasing, $V(0^+) = \sigma_\star^2$ and $V(\infty) = 0$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.9 (`tau-strict-gap`)

**Draft:**

**Proposition 6.9 (strict gap).** P(τ) < V(τ) for every τ > 0: no constant-gain relay is optimal under coloured noise.

**Repository:**

**Proposition 6.9 (strict gap).** $P(\tau) < V(\tau)$ for every $\tau > 0$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.10 (`matched-variance-optimal`)

**Draft:**

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

**Repository:**

**Proposition 6.10 (optimal filter at matched variance).** The optimal stationary error is the positive root of
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

*Proof in the draft:* yes; *in the repository source:* yes

---

## Counterexample 6.11 (`optimal-can-window`)

**Draft:**

**Counterexample 6.11 (the optimal filter can window).** The statement "the optimal filter never produces a window" holds along precision (Theorem 3.4) and along matched-zero-frequency τ (Theorem 6.6), but fails along matched-variance τ: by Proposition 6.10 the optimal failure set is a window for every 0 < R² < P\_max.

**Repository:**

**Counterexample 6.11 (analytic; the optimal filter can window).** The starting study's "the optimal filter never produces a window"
holds along precision (Theorem 3.4) and along matched-zero-frequency $\tau$ (Theorem 6.6), but fails along matched-variance
$\tau$: by Proposition 6.10 the optimal failure set is a window for every $0 < R^2 < P_{\max}$.

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 6.12 (`matched-variance-relay`)

**Draft:**

**Proposition 6.12 (relay at matched variance).** For fixed G > 0,

```latex
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2 v\,\tau}{1 + a\tau}\right)
```

which is strictly increasing, from H\_G to (Σ + G²v/a)/a, and at least P throughout. The classes are All (R² ≤ H\_G), upper ray (H\_G < R² below the top value) and Empty (R² at or above the top value).

The same change of bandwidth gives a monotone optimal filter at matched zero-frequency power and a windowed one at matched variance. The normalisation is a modelling choice, and it changes the topology. Chapter 7 explains the difference: at matched zero-frequency power the observations are ordered by causal garbling along τ (Proposition 7.7), and at matched variance they cannot be, since an ordering would rule out the optimal window (Corollary 7.3).

**Repository:**

**Proposition 6.12 (relay at matched variance).** For fixed $G > 0$,
$$
\sigma^2(\tau) = \frac{1}{a}\left(\Sigma + \frac{G^2v\tau}{1 + a\tau}\right),
$$
strictly increasing from $H_G$ to $(\Sigma + G^2v/a)/a$ and $\ge P$ throughout. Classes: All ($R^2 \le H_G$), upper ray
($H_G < R^2 <$ top), Empty ($R^2 \ge$ top).

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 6.13 (`discrete-excess`)

**Draft:**

**Proposition 6.13 (discrete excess condition).** For a fixed gain 0 ≤ L < 2, the prior error is

```latex
P^- = \frac{a^2 L^2 r + q}{1 - a^2(1 - L)^2},
\qquad
P^+ - F = \frac{P^- - F}{a^2}
```

and P⁻ > F iff P⁺ > F iff L/(2 − L) > φ. The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < φ/2 for every Δt > 0.

**Repository:**

(manuscript, Paper 1, Proposition 6, p. 7, as quoted in RESULTS_t15.md) "M_L = (ϕ²L²r + q)/(1 − ϕ²(1 − L)²), S_L = (1 − L)²M_L + L²r, S_L − F = (M_L − F)/ϕ², and M_L > F ⟺ S_L > F ⟺ L/(2 − L) > FΠ_d. (10) The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < ½FΠ_d for every Π_d > 0." Proof: see the manuscript's Appendix A (p. 14).

*Proof in the draft:* yes; *in the repository source:* no

---

## Lemma 6.14 (`shared-excess-set`)

**Draft:**

**Lemma 6.14 (shared excess set).** For any filter on M-P, P⁻ − F = a²(P⁺ − F) and P̄ − F = (P⁺ − F)·s/(2λΔt). Hence all three metrics exceed F on the same set, {L/(2 − L) > φ}.

**Repository:**

**Lemma 6.14 (shared excess set).** For any filter on M-P, $P^- - F = a^2(P^+ - F)$ and
$\bar P - F = (P^+ - F)\,s/(2\lambda\Delta t)$. Hence all three metrics exceed $F$ on the same set, $\{L/(2 - L) > \varphi\}$
(the starting study's discrete excess condition, Proposition 6.13).

*Proof in the draft:* yes; *in the repository source:* no

---

## Proposition 6.15 (`d1-excess`)

**Draft:**

**Proposition 6.15 (D1: the tanh lemma).** L/(2 − L) = tanh(GΔt/2), so the excess set is {G·h(GΔt) > FΠ} with h(x) = tanh(x/2)/x strictly decreasing from 1/2. The excess set is the lower ray (0, Δt\_E) iff G > 2FΠ, the continuous-time condition, and is empty otherwise; Δt\_E solves tanh(GΔt/2) = FΠΔt.

**Repository:**

**Proposition 6.15 (D1: tanh lemma).** $L/(2 - L) = \tanh(G\Delta t/2)$, so the excess set is $\{G\,h(G\Delta t) > F\Pi\}$ with
$h(x) = \tanh(x/2)/x$ strictly decreasing from $1/2$. The excess set is the lower ray $(0, \Delta t_E)$ iff $G > 2F\Pi$ (the
continuous-time condition), and empty otherwise; $\Delta t_E$ solves $\tanh(G\Delta t/2) = F\Pi\Delta t$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.16 (`d2-excess`)

**Draft:**

**Proposition 6.16 (D2).** The excess set is the lower ray Δt < Δt\_E = (c − 2FΠ₀)/((2 − c)FΠ) iff κ = c/(FΠ₀) > 2, and empty otherwise.

The model requires 0 < c < 2, so that 0 < L < 2. For c > 2 the gain tends to c, L/(2 − L) > φ no longer characterises excess, and the excess set can be all of (0, ∞): with λ = 1, Σ = 0.01, Π = Π₀ = 1 and c = 3, P⁺ > F at every Δt and P⁺ → 4F.

**Repository:**

**Proposition 6.16 (D2).** The excess set is the lower ray $\Delta t < \Delta t_E = (c - 2F\Pi_0)/((2 - c)F\Pi)$ iff
$\kappa = c/(F\Pi_0) > 2$, and empty otherwise.

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 6.17 (`d3-excess`)

**Draft:**

**Proposition 6.17 (D3).** The excess set is {φ < 1 and s(1 − φ)(ρ(1 + φ) − 2) > 4φ}. Its small-Δt behaviour gives the onset: with u = 2ΣΠ/λ², there is excess near Δt = 0 iff ρ > 2 + u. This is the continuous-time excess condition for G = −λ + √(λ² + 2ρΣΠ), since √(1 + ρu) > 1 + u iff ρ > 2 + u.

**Repository:**

**Proposition 6.17 (D3).** The excess set is $\{\varphi < 1$ and $s(1 - \varphi)(\rho(1 + \varphi) - 2) > 4\varphi\}$. Its
small-$\Delta t$ behaviour gives the onset: excess near $\Delta t = 0$ iff $\rho > 2 + u$, which is the continuous excess
condition for $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$ ($\sqrt{1 + \rho u} > 1 + u$).

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.18 (`dt-endpoint-limits`)

**Draft:**

**Proposition 6.18 (endpoint limits).** With G\_ρ = −λ + √(λ² + 2ρΣΠ):

| Filter | Δt → 0 (all metrics) | Δt → ∞ |
| --- | --- | --- |
| Optimal | σ⋆² | post → 0; prior and avg → F from below |
| D1 | σ²(G, Π) | post → 0; prior → F from below (gap ∝ e^(−2λΔt)); avg → F from below, like −F/(2λΔt) |
| D2 | σ²(cΠ/Π₀, Π) | post → (1 − c)²F, with Δt·(P⁺ − (1 − c)²F) → c\[c + 2(1 − c)FΠ₀\]/Π; prior and avg → F from below |
| D3 | σ²(G\_ρ, Π) | post → 0; prior and avg → F from below |

**Repository:**

**Proposition 6.18 (endpoint limits).**

| Filter | $\Delta t \to 0$ (all metrics) | $\Delta t \to \infty$ |
|---|---|---|
| Optimal | $\sigma_\star^2$ | post $\to 0$; prior, avg $\to F$ from below |
| D1 | $\sigma^2(G, \Pi)$ | post $\to 0$; prior $\to F$ from below (gap $\propto e^{-2\lambda\Delta t}$); avg $\to F$ from below, like $-F/(2\lambda\Delta t)$ |
| D2 | $\sigma^2(c\Pi/\Pi_0, \Pi)$ | post $\to (1-c)^2F$, with $\Delta t\,(P^+ - (1-c)^2F) \to c[c + 2(1-c)F\Pi_0]/\Pi$; prior, avg $\to F$ from below |
| D3 | $\sigma^2(G_\rho, \Pi)$ | post $\to 0$; prior, avg $\to F$ from below |

Here $G_\rho = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$.

*Proof in the draft:* no; *in the repository source:* no

---

## Theorem 6.19 (`dt-optimal-mp`)

**Draft:**

**Theorem 6.19 (optimal M-P error along Δt).**

(a) P⁺ is strictly decreasing, from σ⋆² to 0.

(b) P⁻ is strictly increasing, from σ⋆² to F.

(c) P̄ is strictly increasing, from σ⋆² to F.

**Repository:**

**Theorem 6.19 (optimal M-P error along $\Delta t$).**
(a) $P^+$ is strictly decreasing, from $\sigma_\star^2$ to $0$.
(b) $P^-$ is strictly increasing, from $\sigma_\star^2$ to $F$.
(c) $\bar P$ is strictly increasing, from $\sigma_\star^2$ to $F$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.20 (`dt-two-rays`)

**Draft:**

**Proposition 6.20 (two rays from an over-weighted sampled relay).** Let D1 have G > 2FΠ, and assume C2 for these curves (finitely many turning points; Conjecture 6.22 would give it). Then prior and avg start at σ²(G, Π) > F and end at F, approached from below, so each has an interior minimum below F. For R² between the lowest minimum and F, the failure set contains a lower and an upper ray: two rays, or (1, 1, k) if there are several minima.

**Repository:**

**Proposition 6.20 (two rays from an over-weighted sampled relay).** Let D1 have $G > 2F\Pi$, and assume C2 for these curves
(finitely many turning points; Conjecture 6.22 would give it). Then prior and avg start at
$\sigma^2(G, \Pi) > F$ and end at $F$ approached from below, so each has an interior minimum below $F$; for $R^2$ between the
lowest minimum and $F$ the failure set contains a lower and an upper ray: two rays, or $(1,1,k)$ with several minima.

*Proof in the draft:* yes; *in the repository source:* no

---

## Numerical result 6.21 (`dt-relay-census`)

**Draft:**

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

**Repository:**

**Numerical result 6.21 (census of sampled relays).** On 2,000 sets per family, every class agreed by both routes:

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
so $G > 2F\Pi$ is sufficient for two rays (Proposition 6.20) but not necessary.

*Proof in the draft:* no; *in the repository source:* no

---

## Conjecture 6.22 (`dt-two-turning-points`)

**Draft:**

**Conjecture 6.22 (at most two turning points).** Along Δt, D1–D3 have at most two turning points in every metric.

No case with more than two was found in the census or in the Task 13 audit, and no proof is known (chapter 9).

**Repository:**

**Conjecture 6.22 (at most two turning points).** Along $\Delta t$, D1–D3 have at most two turning points in every metric.

*Proof in the draft:* no; *in the repository source:* no

---

## Lemma 6.23 (`sigma-scaling`)

**Draft:**

**Lemma 6.23 (Σ scaling).** σ²/F = (1 + g²/u)/(1 + g). For a gain that depends on (Σ, Π) only through u, the relative-tolerance Σ sweep and the precision sweep classify identically in u.

**Repository:**

**Lemma 6.23 (scaling).** $\sigma^2/F = (1 + g^2/u)/(1 + g)$. For a gain that depends on $(\Sigma, \Pi)$ only through $u$, the
relative-tolerance $\Sigma$ sweep and the precision sweep classify identically in $u$.

*Proof in the draft:* yes; *in the repository source:* no

---

## Proposition 6.24 (`sigma-independent-gain`)

**Draft:**

**Proposition 6.24 (Σ-independent gain).** Absolute: σ² is affine and increasing in Σ, from G²/(2Π(λ + G)) (approached from above) to ∞; the classes are All and upper ray. Relative: σ²/F decreases from ∞ to 1/(1 + g); the classes are All and lower ray. The excess set (r = 1) is Σ < λG/(2Π).

**Repository:**

**Proposition 6.24 ($\Sigma$-independent gain).** Absolute: $\sigma^2$ is affine and increasing, from $G^2/(2\Pi(\lambda + G))$
(approached from above) to $\infty$; classes All, upper ray. Relative: $\sigma^2/F$ decreases from $\infty$ to $1/(1 + g)$;
classes All, lower ray. Excess set ($r = 1$): $\Sigma < \lambda G/(2\Pi)$.

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 6.25 (`sigma-overtrust`)

**Draft:**

**Proposition 6.25 (Σ-tracking Kalman gain, over-trust ρ).** Let G = −λ + √(λ² + 2ρΣΠ) and w = √(1 + ρu). Absolute: σ² is strictly increasing from 0, class upper ray. Relative:

```latex
\frac{\sigma^2}{F} = \frac{(1 + \rho)\,w + (1 - \rho)}{w\,(w + 1)}
```

which starts at 1 and tends to 0, with a single maximum at w\_M = \[(ρ − 1) + √(2ρ(ρ − 1))\]/(1 + ρ) iff ρ > 2, and is strictly decreasing otherwise. The classes are:

- ρ > 2: lower ray (r ≤ 1, since the start at 1 is approached from above), window (1 < r below the peak), Empty (at or above the peak);
- ρ ≤ 2: lower ray (r < 1), Empty (r ≥ 1).

**Repository:**

**Proposition 6.25 ($\Sigma$-tracking Kalman, over-trust $\rho$).** Let $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$ and
$w = \sqrt{1 + \rho u}$. Absolute: strictly increasing from $0$, class upper ray. Relative:
$$
\frac{\sigma^2}{F} = \frac{(1 + \rho)w + (1 - \rho)}{w(w + 1)},
$$
starting at $1$ and tending to $0$, with a single maximum at $w_M = [(\rho - 1) + \sqrt{2\rho(\rho - 1)}]/(1 + \rho)$ iff
$\rho > 2$, and strictly decreasing otherwise. Classes: $\rho > 2$: lower ray ($r \le 1$, since the start at $1$ is
approached from above), window ($1 < r <$ peak), Empty (at or above the peak); $\rho \le 2$: lower ray ($r < 1$), Empty ($r \ge 1$).

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.26 (`sigma-misspecified-lambda`)

**Draft:**

**Proposition 6.26 (Σ-tracking Kalman gain, misspecified λ′).** Let G = −λ′ + √(λ′² + 2ΣΠ). Absolute: σ² is strictly increasing from 0, class upper ray. Relative: σ²/F starts at 1 and tends to 0, with a single maximum iff λ′ < λ/2, and is strictly decreasing otherwise. The classes are lower ray (r ≤ 1), window (1 < r below the peak) and Empty when λ′ < λ/2, and lower ray (r < 1) and Empty (r ≥ 1) otherwise.

**Repository:**

**Proposition 6.26 ($\Sigma$-tracking Kalman, misspecified $\lambda'$).** Let $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma\Pi}$.
Absolute: strictly increasing from $0$, class upper ray. Relative: starts at $1$ and tends to $0$, with a single maximum iff
$\lambda' < \lambda/2$ and strictly decreasing otherwise. Classes: $\lambda' < \lambda/2$: lower ray ($r \le 1$), window
($1 < r <$ peak), Empty; otherwise lower ray ($r < 1$), Empty ($r \ge 1$).

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 6.27 (`sigma-optimal`)

**Draft:**

**Proposition 6.27 (optimal filter along Σ).** Absolute: σ⋆² is increasing from 0, class upper ray. Relative: σ⋆²/F = 2/(1 + √(1 + u)) is decreasing, classes lower ray and Empty.

**Repository:**

**Proposition 6.27 (optimal).** Absolute: increasing from $0$, class upper ray. Relative: $2/(1 + \sqrt{1 + u})$ is decreasing,
classes lower ray, Empty.

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 6.28 (`signal-sweeps`)

**Draft:**

**Proposition 6.28 (signal sweeps).** σ⋆² is increasing in Σ, decreasing in λ at fixed Σ, and increasing in λ at fixed F, since σ⋆² = 2F/(1 + √(1 + 2FΠ/λ)). So the optimal filter never windows along these sweeps either, for an elementary reason rather than an information-ordering one.

On a moving floor the tolerance convention decides the topology. With absolute tolerances every family is monotone. With relative tolerances, windows return under the same factor-of-two over-confidence condition as in chapters 3 and 5: ρ > 2, or λ′ < λ/2 (that is F′/F > 2). Under either convention, the optimal filter never windows along Σ.

**Repository:**

**Proposition 6.28 (signal sweeps).** $\sigma_\star^2$ is increasing in $\Sigma$, decreasing in $\lambda$ at fixed $\Sigma$, and
increasing in $\lambda$ at fixed $F$ (since $\sigma_\star^2 = 2F/(1 + \sqrt{1 + 2F\Pi/\lambda})$). So the optimal filter never
windows along these sweeps either, for an elementary reason rather than an information-ordering one.

*Proof in the draft:* no; *in the repository source:* no

---

## Definition 7.1 (`causal-garbling`)

**Draft:**

**Definition 7.1 (causal garbling).** Write θ₁ ⪯\_c θ₂ ("θ₂ is causally at least as informative as θ₁") if there are a random element U, independent of (s, Y\_θ₂), and a process Y′ such that, for every t, Y′(u ≤ t) is measurable with respect to 𝒢\_t = σ(Y\_θ₂(u ≤ t)) ∨ σ(U), and (s, Y′) has the same joint law as (s, Y\_θ₁).

In words: the worse observations can be manufactured from the better ones as they arrive, using only the past and present of the better process plus independent randomness.

**Repository:**

**Definition 7.1 (causal garbling).** $\theta_1 \preceq_c \theta_2$ ("$\theta_2$ is causally at least as informative") if there are a
random element $U$ independent of $(s, Y_{\theta_2})$ and a process $Y'$ with $Y'(u \le t)$ measurable with respect to
$\mathcal G_t = \sigma(Y_{\theta_2}(u \le t)) \vee \sigma(U)$ for every $t$, such that $(s, Y') \overset{d}{=} (s, Y_{\theta_1})$.

*Proof in the draft:* no; *in the repository source:* no

---

## Theorem 7.2 (`causal-monotonicity`)

**Draft:**

**Theorem 7.2 (monotonicity under causal garbling).** If θ₁ ⪯\_c θ₂, then P(θ₂) ≤ P(θ₁).

**Repository:**

**Theorem 7.2 (monotonicity under causal garbling).** If $\theta_1 \preceq_c \theta_2$, then $P(\theta_2) \le P(\theta_1)$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Corollary 7.3 (`no-optimal-windows`)

**Draft:**

**Corollary 7.3 (no optimal windows along causal orderings).** Suppose θ₁ < θ₂ implies θ₁ ⪯\_c θ₂ on the whole domain. Then P is non-increasing, so every optimal failure set is an initial segment of the domain. If moreover P is continuous (and satisfies C2′), the optimal failure set is Empty, All or a lower ray at every R². For the reverse ordering it is Empty, All or an upper ray. Windows, two rays and mixed classes are impossible.

**Repository:**

**Corollary 7.3 (no optimal windows along causal orderings).** If $\theta_1 < \theta_2 \Rightarrow \theta_1 \preceq_c \theta_2$ on the
whole domain, $P$ is non-increasing, so every optimal failure set is an initial segment of the domain. If moreover $P$ is
continuous (and satisfies C2′), the optimal failure set is Empty, All or a lower ray at every $R^2$; for the reverse ordering,
Empty, All or an upper ray. Windows, two rays and mixed classes are impossible.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Corollary 7.4 (`diagnostic`)

**Draft:**

**Corollary 7.4 (diagnostic).** Along a causally ordered sweep, a failure set with a window, two rays or a mixed class certifies that the filter is not optimal. With Theorem 5.1, the precision-sweep picture is complete: the optimal filter sits on the envelope σ⋆² (classes lower ray and Empty), and every curve strictly above it belongs to some miscalibrated gain.

**Repository:**

**Corollary 7.4 (diagnostic).** Along a causally ordered sweep, a failure set with a window, two rays or a mixed class certifies
that the filter is not optimal. With Theorem 5.1, the precision-sweep picture is complete: the optimal filter sits on the envelope
$\sigma_\star^2$ (classes lower ray and Empty), and every curve strictly above it belongs to some miscalibrated gain.

*Proof in the draft:* yes; *in the repository source:* no

---

## Proposition 7.5 (`spectral-dominance`)

**Draft:**

**Proposition 7.5 (spectral dominance).** Let y\_θ = s + η\_θ, with η\_θ stationary Gaussian, independent of s, with spectral density S\_θ (white components written as constant densities).

1. If S\_θ₁ ≥ S\_θ₂ almost everywhere, then θ₁ ⪯\_c θ₂.
2. Suppose S\_s > 0. If Y′ = h ∗ y\_θ₂ + n, with h causal and linear time-invariant and n independent, realises θ₁, then h = δ and S\_n = S\_θ₁ − S\_θ₂ ≥ 0.

**Repository:**

**Proposition 7.5 (spectral dominance).** Let $y_\theta = s + \eta_\theta$ with $\eta_\theta$ stationary Gaussian, independent of $s$,
with spectral densities $S_\theta$ (white components in integrated form as constant densities).
1. If $S_{\theta_1} \ge S_{\theta_2}$ almost everywhere, then $\theta_1 \preceq_c \theta_2$.
2. Suppose $S_s > 0$. If $Y' = h * y_{\theta_2} + n$, with $h$ causal LTI and $n$ independent, realizes $\theta_1$, then
   $h = \delta$ and $S_n = S_{\theta_1} - S_{\theta_2} \ge 0$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Theorem 7.6 (`gaussian-orderings-coincide`)

**Draft:**

**Theorem 7.6 (the orderings coincide for Gaussian noise).** In the setting of Proposition 7.5, with S\_s > 0 almost everywhere, the following are equivalent:

- (i) θ₁ ⪯\_c θ₂ by some causal garbling, possibly non-linear;
- (ii) S\_θ₁ ≥ S\_θ₂ almost everywhere;
- (iii) θ₁ ⪯\_c θ₂ by adding independent stationary Gaussian noise;
- (iv) Y\_θ₁ is a garbling of Y\_θ₂ as whole paths, not necessarily causal (pathwise Blackwell ordering).

**Repository:**

**Theorem 7.6 (non-linear causal garblings add nothing).** In the setting of Proposition 7.5 with $S_s > 0$ almost everywhere,
the following are equivalent: (i) $\theta_1 \preceq_c \theta_2$ by some (possibly non-linear) causal garbling; (ii)
$S_{\theta_1} \ge S_{\theta_2}$ almost everywhere; (iii) $\theta_1 \preceq_c \theta_2$ by adding independent stationary Gaussian noise; (iv) $Y_{\theta_1}$ is a (not necessarily
causal) garbling of $Y_{\theta_2}$ as whole paths (pathwise Blackwell ordering).

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 7.7 (`sweeps-ordered`)

**Draft:**

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

**Repository:**

**Proposition 7.7 (the sweeps studied).**
- (a) Precision: $S_\Pi = 1/\Pi$ decreases in $\Pi$, so the sweep is ordered (the starting study's monotone optimal filter recovered).
- (b) Matched-zero-frequency $\tau$: $S_\tau(\omega) = (1/\Pi)/(1 + \tau^2\omega^2)$ decreases in $\tau$ at every $\omega$, so for
  $\tau_2 > \tau_1$, $\tau_1 \preceq_c \tau_2$ (information increases with $\tau$). The garbling noise has
  $$
  S_\xi(\omega) = \frac{(\tau_2^2 - \tau_1^2)\omega^2}{\Pi(1 + \tau_1^2\omega^2)(1 + \tau_2^2\omega^2)} = |H_\xi(i\omega)|^2,
  \qquad
  H_\xi(s) = \sqrt{\frac{\tau_2^2 - \tau_1^2}{\Pi}}\;\frac{s}{(1 + \tau_1s)(1 + \tau_2s)},
  $$
  a second-order process (real for $\tau_2 > \tau_1$). Theorem 6.6's monotonicity follows; its strictness comes from the closed form.
- (c) Matched-variance $\tau$: $S_\tau = 2v\tau/(1 + \tau^2\omega^2)$; every pair crosses (larger at $\omega = 0$ for the larger $\tau$,
  larger as $\omega \to \infty$ for the smaller), so by Theorem 7.6 no two values are causally ordered by any garbling, linear or not.

*Proof in the draft:* yes; *in the repository source:* no

---

## Theorem 7.8 (`power-family-sharpness`)

**Draft:**

**Theorem 7.8 (sharpness in the power family).**

1. β ≤ 0: S\_β,τ decreases in τ at every ω. The sweep is causally ordered, with information increasing in τ, so P is non-increasing. Optimal classes: lower ray and Empty.
2. β ≥ 2: S\_β,τ increases in τ at every ω. The sweep is ordered with information decreasing in τ, so P is non-decreasing. Optimal classes: upper ray and Empty.
3. 0 < β < 2: every pair τ₁ ≠ τ₂ has crossing spectra, and P → 0 at both ends while P > 0. So for every 0 < R² < max P the optimal failure set is bounded away from both ends: a window, and exactly one by Theorem 7.9.

Hence, in this family: causally ordered ⇔ P monotone ⇔ no optimal-filter window ⇔ β ∉ (0, 2).

**Repository:**

**Theorem 7.8 (sharpness of the ordering condition).**
1. $\beta \le 0$: $S_{\beta,\tau}$ decreases in $\tau$ at every $\omega$; the sweep is causally ordered (information
   increasing in $\tau$), so $P$ is non-increasing. Optimal classes: lower ray, Empty.
2. $\beta \ge 2$: $S_{\beta,\tau}$ increases in $\tau$ at every $\omega$; ordered with information decreasing in $\tau$, so
   $P$ is non-decreasing. Optimal classes: upper ray, Empty.
3. $0 < \beta < 2$: every pair $\tau_1 \ne \tau_2$ has crossing spectra, $P \to 0$ at both ends while $P > 0$, so for every
   $0 < R^2 < \max P$ the optimal failure set is bounded away from both ends: a window (exactly one, by Theorem 7.9).

Hence, in this family: causally ordered $\iff$ $P$ monotone $\iff$ no optimal-filter window $\iff$ $\beta \notin (0, 2)$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Theorem 7.9 (`power-family-unimodal`)

**Draft:**

**Theorem 7.9 (unimodality for 0 < β < 2).** For 0 < β < 2, P has exactly one turning point, a maximum, so the optimal failure set has k = 1.

**Repository:**

**Theorem 7.9 (unimodality for $0 < \beta < 2$).** For $0 < \beta < 2$, $P$ has exactly one turning point, a maximum, so the
optimal failure set has $k = 1$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 7.10 (`power-family-duality`)

**Draft:**

**Proposition 7.10 (duality).** P\_β,K(τ) = P\_(2−β), Kλ^(2−2β)(1/(λ²τ)).

**Repository:**

**Proposition 7.10 (duality).** $P_{\beta, K}(\tau) = P_{2-\beta,\ K\lambda^{2-2\beta}}\big(1/(\lambda^2\tau)\big)$.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 7.11 (`latency`)

**Draft:**

**Proposition 7.11 (latency).** Let y\_d(t) = s(t − d) + white noise of intensity 1/Π, with d ≥ 0. All values of d are pathwise Blackwell-equivalent, yet the optimal filtering error is

```latex
P(d) = F - e^{-2\lambda d}\big(F - \sigma_\star^2(\Pi)\big)
```

which is strictly increasing in d. Along the latency sweep d(θ) = θe^(−θ), which rises and then falls, the optimal filter has a window in θ for every R² ∈ (σ⋆², P(1/e)). The causal order (d₁ < d₂ ⇒ d₂ ⪯\_c d₁) reverses at θ = 1, where the window sits. The classes along θ are All (R² ≤ σ⋆²), window (σ⋆² < R² < P(1/e)) and Empty (R² ≥ P(1/e)).

**Repository:**

**Proposition 7.11 (latency).** Observations $y_d(t) = s(t - d) + $ white noise of intensity $1/\Pi$, $d \ge 0$. All values of $d$ are
pathwise Blackwell-equivalent, yet the optimal filtering error is
$$
P(d) = F - e^{-2\lambda d}\big(F - \sigma_\star^2(\Pi)\big),
$$
strictly increasing in $d$. Along the latency sweep $d(\theta) = \theta e^{-\theta}$, which rises then falls, the optimal filter has a
window in $\theta$ for every $R^2 \in (\sigma_\star^2, P(1/e))$; the causal order ($d_1 < d_2 \Rightarrow d_2 \preceq_c d_1$) reverses at
$\theta = 1$, where the window sits. Classes along $\theta$: All ($R^2 \le \sigma_\star^2$), window, Empty ($R^2 \ge P(1/e)$).

*Proof in the draft:* yes; *in the repository source:* yes

---

## Counterexample 7.12 (`pathwise-not-enough`)

**Draft:**

**Counterexample 7.12 (pathwise ordering is not enough).** Proposition 7.11 is a sweep of pathwise Blackwell-equivalent experiments along which the optimal filtering error is not monotone. So "Blackwell ordering of whole paths implies monotone filtering error" is false, and Definition 7.1 must be causal.

The causal order also cannot be reversed into a characterisation of monotonicity.

**Repository:**

**Counterexample 7.12 (analytic; pathwise ordering is not enough).** Proposition 7.11 is a sweep of pathwise Blackwell-equivalent
experiments along which the optimal filtering error is non-monotone, so "Blackwell ordering (pathwise) implies monotone filtering
error" is false; Definition 7.1 must be causal.

*Proof in the draft:* no; *in the repository source:* no

---

## Proposition 7.13 (`ordering-not-necessary`)

**Draft:**

**Proposition 7.13 (ordering is sufficient, not necessary).** Along matched-variance τ restricted to (1/λ, ∞), P is strictly decreasing (Proposition 6.10), yet no two values are causally ordered by any garbling (Proposition 7.7(c)). So a monotone optimal error does not require an information ordering.

**Repository:**

**Proposition 7.13 (ordering is sufficient, not necessary).** Along matched-variance $\tau$ restricted to $(1/\lambda, \infty)$, $P$ is
strictly decreasing (Proposition 6.10), yet no two values are causally ordered by any garbling (Proposition 7.7(c)). So monotone optimal
error does not require an information ordering.

*Proof in the draft:* no; *in the repository source:* no

---

## Corollary 7.14 (`mi-nested`)

**Draft:**

**Corollary 7.14 (integrate-and-dump, nested grids).** If Δt₂ = mΔt₁ for an integer m and the grids are aligned, each coarse M-I sample is the average of the m fine samples completed by the time it is taken: a causal garbling. Hence the optimal error, pointwise in t and time-averaged, satisfies P(Δt₂) ≥ P(Δt₁) along every chain Δt₀, mΔt₀, m²Δt₀, …

**Repository:**

**Corollary 7.14 (integrate-and-dump, nested grids).** If $\Delta t_2 = m\Delta t_1$ for an integer $m$ and the grids are
aligned, each coarse M-I sample is the average of $m$ fine samples completed by the time it is, a causal garbling. Hence the
optimal error, pointwise in $t$ and time-averaged, satisfies $P(\Delta t_2) \ge P(\Delta t_1)$ along every chain
$\Delta t_0, m\Delta t_0, m^2\Delta t_0, \dots$

*Proof in the draft:* yes; *in the repository source:* no

---

## Theorem 7.15 (`mi-continuum`)

**Draft:**

**Theorem 7.15 (integrate-and-dump on the continuum).** Both M-I optimal metrics, (a) the error at sample times and (b) the time average, are strictly increasing in Δt on the whole continuum, including non-nested pairs.

**Repository:**

**Theorem 7.15 (integrate-and-dump on the continuum).** Both M-I optimal metrics, (a) the error at sample times and (b) the time
average, are strictly increasing in $\Delta t$ on the whole continuum, including non-nested pairs.

*Proof in the draft:* yes; *in the repository source:* yes

---

## Proposition 7.16 (`mp-not-ordered`)

**Draft:**

**Proposition 7.16 (M-P is not a causal-garbling family).** Along Δt, the point-sampled model is ordered in neither direction.

**Repository:**

**Proposition 7.16 (M-P is not a causal-garbling family along $\Delta t$).** In neither direction: by Theorem 7.2 an ordering
would give a pointwise-in-$t$ inequality between the two (cyclostationary) optimal error curves, and post, prior and avg are
the minimum, the supremum and the time mean of each curve over its period, so all three would move the same way; but post
falls while prior and avg rise (Theorem 6.19).

*Proof in the draft:* yes; *in the repository source:* no

---
