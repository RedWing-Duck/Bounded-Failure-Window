# Task 16 A2: statements side by side (draft chapters 1–5 vs the repository at the artifacts commit)

Extracted mechanically (PREREG_t16.md, D2). Repository text: `Stages_0_4_Thesis.md` (rendered from `source/Stages_0_4_Source.md` and `source/thesis_only/`). 3.1 and 3.5 have no labelled block in the repository; their statements are the §1 model paragraph and the reference-quantities bullet. Classification: `a2_classification.yaml`.

## Proposition 2.1 (`topological-realizability`)

**Draft:**

**Proposition 2.1 (realizability).** For every ℓ, u ∈ {0, 1} and every finite k ≥ 0 there is a continuous, piecewise strictly monotone function on (0, ∞) and a tolerance whose failure set has class (ℓ, u, k); All is realised too. Classes with k = ∞ need infinitely many turning points and are excluded by C2.

**Repository:**

**Proposition 2.1 (topological realizability).** For every $\ell, u \in \{0,1\}$ and every finite $k \ge 0$ there is a
continuous piecewise strictly monotone function on $(0,\infty)$ and a tolerance whose failure set has class
$(\ell, u, k)$; All is realized too. Classes with $k = \infty$ need infinitely many turning points and are excluded by C2.

---

## Theorem 2.2 (`critical-tolerance`)

**Draft:**

**Theorem 2.2.** Assume C1–C6.

1. **Local constancy.** The class of 𝓕(R²) is constant on each connected component of (0, ∞) \\ 𝒞. It can change only when R² crosses or equals a critical tolerance.
2. **Rays.** ℓ = 1 if R² < L₋ and ℓ = 0 if R² > L₋. If R² = L₋, then ℓ = 1 iff σ² approaches L₋ from above. The same holds for u with L₊.
3. **Window components.** Each window component contains an interior local maximum tⱼ with σ²(tⱼ) > R², and distinct components contain distinct maxima. Hence k is at most the number of interior maxima above R², with equality iff each such maximum lies in its own component touching neither end.
4. **Determining data.** The class of 𝓕(R²), for every R², is determined by the ordered sequence (L₋, σ²(t₁), …, σ²(tₙ), L₊) and the two approach directions. The positions tⱼ are needed only to locate the components.

**Repository:**

**Theorem 2.2 (critical-tolerance theorem).** Assume C1–C6.

(a) *Local constancy.* The class of $\mathcal F(R^2)$ is constant on each connected component of $(0,\infty)\setminus\mathcal C$.

(b) *Rays.* $\ell = 1$ if $R^2 < L_-$ and $\ell = 0$ if $R^2 > L_-$. If $R^2 = L_-$, then $\ell = 1$ iff $\sigma^2$
approaches $L_-$ from above. The same holds for $u$ with $L_+$.

(c) *Windows.* Each window contains an interior local maximum $t_j$ with $\sigma^2(t_j) > R^2$, and distinct windows
contain distinct maxima, so $k \le \#\{\text{interior local maxima with value} > R^2\}$, with equality iff each such
maximum lies in a component that touches neither end and contains no other such maximum.

(d) *Determining data.* The class at every $R^2$ is determined by the ordered sequence
$(L_-, \sigma^2(t_1), \dots, \sigma^2(t_n), L_+)$ and the two approach directions.

---

## Definition 2.3 (`signature`)

**Draft:**

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

**Repository:**

**Definition 2.3.** The *critical-value signature* of a curve satisfying C2 is

```latex
S(\sigma^2) = \big(L_-,\ \sigma^2(t_1),\ \dots,\ \sigma^2(t_n),\ L_+;\ d_-,\ d_+\big)
```

where d± ∈ {above, below} are the approach directions. Its **critical-tolerance diagram** is the (θ, R²) half-plane cut by horizontal lines at the values in 𝒞: each band between consecutive lines carries one class, and each line carries its own equality class.

*Thesis-only text, imported verbatim from the thesis draft (`t15/input/Thesis_Draft_ch1-4.md`, §2.7, lines 222–224).*

---

## Theorem 2.4 (`plateaus`)

**Draft:**

(not found)

**Repository:**

**Theorem 2.4 (plateaus).** Under C2′ instead of C2, Theorem 2.2 holds with three changes: plateau values join the critical
tolerances; at $R^2$ equal to a plateau value the plateau is excluded from $\mathcal F$, which can split or remove
components; an end adjacent to a plateau at value $L$ carries a ray iff $R^2 < L$.

---

## Corollary 2.5 (`equal-height-maxima`)

**Draft:**

(not found)

**Repository:**

**Corollary 2.5 (equal-height maxima).** If two interior maxima share the value $M_2$, are separated by a lower minimum, and
just below $M_2$ each lies in a component touching neither end (the equality condition of Theorem 2.2(c)), then just below $M_2$ both count in $k$, and at and above $M_2$ both windows are gone: $k$ drops by 2 at one tolerance. The
class is otherwise unaffected.

---

## Corollary 2.6 (`degenerate-points`)

**Draft:**

(not found)

**Repository:**

**Corollary 2.6 (degenerate stationary points).** A stationary point that is not a turning point never changes the class, and a
flat-topped maximum acts as a maximum.

---

## Proposition 2.7 (`pair-birth`)

**Draft:**

(not found)

**Repository:**

**Proposition 2.7 (pair birth).** If a minimum–maximum pair is born at $\theta_0$ through a nondegenerate fold of $N$, then at
distance $\delta$ from $\theta_0$ the turning-point positions separate like $\delta^{1/2}$ and the values like
$M - m \sim \delta^{3/2}$; the band of tolerances that sees the pair opens continuously from zero width.

---

## Corollary 2.8 (`reparameterisation`)

**Draft:**

**Corollary 2.8.** Let φ : D′ → D be a continuous strictly monotone bijection between open intervals, and set σ̃² = σ² ∘ φ. For every R², the failure set 𝓕̃(R²) = φ⁻¹(𝓕(R²)) has the same k. If φ is increasing it has the same (ℓ, u); if φ is decreasing, ℓ and u are exchanged. The signature is preserved, reversed when φ is decreasing.

**Repository:**

**Corollary 2.8.** Let φ : D′ → D be a continuous strictly monotone bijection between open intervals, and set σ̃² = σ² ∘ φ. For every R², the failure set 𝓕̃(R²) = φ⁻¹(𝓕(R²)) has the same k. If φ is increasing it has the same (ℓ, u); if φ is decreasing, ℓ and u are exchanged. The signature is preserved, reversed when φ is decreasing.

---

## Proposition 2.9 (`structural-stability`)

**Draft:**

**Proposition 2.9.** Let σ² satisfy C2 and let R² ∉ 𝒞. Then the crossing set {θ : σ²(θ) = R²} is finite, say {x₁, …, x\_m}. Choose disjoint compact intervals Nᵢ ⊂ D, each inside one monotone piece, with xᵢ in the interior of Nᵢ, and set

```latex
\eta = \inf\big\{\,|\sigma^2(\theta) - R^2| : \theta \in D \setminus \textstyle\bigcup_i \operatorname{int} N_i\big\}
```

Then η > 0, and every continuous σ̃² on D with

1. sup over D of |σ̃² − σ²| < η, and
2. σ̃² strictly monotone on each Nᵢ

has failure set 𝓕̃(R²) of the same class as 𝓕(R²).

**Repository:**

**Proposition 2.9.** Let σ² satisfy C2 and let R² ∉ 𝒞. Then the crossing set {θ : σ²(θ) = R²} is finite, say {x₁, …, x\_m}. Choose disjoint compact intervals Nᵢ ⊂ D, each inside one monotone piece, with xᵢ in the interior of Nᵢ, and set

```latex
\eta = \inf\big\{\,|\sigma^2(\theta) - R^2| : \theta \in D \setminus \textstyle\bigcup_i \operatorname{int} N_i\big\}
```

Then η > 0, and every continuous σ̃² on D with

1. sup over D of |σ̃² − σ²| < η, and
2. σ̃² strictly monotone on each Nᵢ

has failure set 𝓕̃(R²) of the same class as 𝓕(R²).

---

## Proposition 3.1 (`stationary-variance`)

**Draft:**

A scalar error x is corrected toward a noisy signal with a gain G that depends on the observation precision Π:

```latex
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\mathrm{sim}},
\qquad
\sigma^2 = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}
```

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters \[4–9, 36–38\].

**Repository:**

**Model.** A scalar Ornstein–Uhlenbeck signal $s$ ($\dot s = -\lambda s + w_s$, $w_s$ white of intensity $2\Sigma$) is
corrected toward a noisy observation with a gain $G \ge 0$ that is constant in time. The error $x$ of the constant-gain
filter (the **relay**) obeys
$$
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\text{sim}},
$$
with $\xi_s$ white sensory noise of intensity $1/\Pi$ (precision $\Pi > 0$) and $\xi_{\text{sim}}$ of intensity $2\Sigma$.
All variances are **actual** stationary error variances, never filter-reported ones. The stationary variance (Proposition 3.1) is
$$
\sigma^2(G, \Pi) = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}.
$$

---

## Theorem 3.2 (`normal-form`)

**Draft:**

**Theorem 3.2 (normal form).**

```latex
\frac{\sigma^2}{F} = \mathcal V(\nu, q) = \frac{1 + \nu q^2/4}{1 + \nu q/2}
```

**Repository:**

**Theorem 3.2 (normal form).**

```latex
\frac{\sigma^2}{F} = \mathcal V(\nu, q) = \frac{1 + \nu q^2/4}{1 + \nu q/2}
```

---

## Corollary 3.3 (`excess-identity`)

**Draft:**

Subtracting the floor gives

```latex
\mathcal V(\nu, q) - 1 = \frac{\nu\, q\,(q - 2)}{4 + 2\nu q}
```

so σ² > F if and only if q > 2, whatever λ, Σ and Π are. This is **Corollary 3.3 (excess identity)**; in dimensional form it reads G > 2FΠ. The numerator of 𝒱 adds the noise the correction injects, νq²/4 in units of F; the denominator divides by the variance it removes, 1 + νq/2. Injection beats removal exactly when q > 2.


**Repository:**

**Corollary 3.3 (excess identity; the starting study (Tasks 1–7)).**
$$
\sigma^2 - F = \frac{G\big(\lambda G/(2\Pi) - \Sigma\big)}{\lambda(\lambda + G)},
\qquad
\sigma^2 > F \iff G > 2F\Pi.
$$

---

## Theorem 3.4 (`window-theorem`)

**Draft:**

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

**Repository:**

**Theorem 3.4 (window theorem; the starting study (Tasks 1–7)).** Assume $G$ is continuous, $G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$, and
$G \to G_\infty \in (0,\infty)$. Then some tolerance fails on a bounded set of precisions away from zero (a window) iff
$\sup_{\Pi > 0} G(\Pi)/\Pi > 2F$; every $R^2 \in (F, \sup\sigma^2)$ then gives a failure set of class $(0,0,k)$ with $k \ge 1$ (a single window when
$\sigma^2$ has one interior maximum, as in Proposition 5.8; $k > 1$ is possible, Corollary 5.4). The optimal variance
$\sigma_\star^2(\Pi)$ decreases strictly from $F$ to $0$, so the optimal filter never windows along $\Pi$: its classes are
lower ray ($R^2 < F$) and Empty ($R^2 \ge F$).

---

## Proposition 3.5 (`optimal-envelope`)

**Draft:**

**Proposition 3.5 (optimal gain).** For this plant the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives

```latex
G^\star(\Pi) = p\,\Pi = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
\qquad
\sigma_\star^2(\Pi) = p = \frac{2\Sigma}{\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}}
```

G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.

**Repository:**

- Optimal (Kalman–Bucy) gain $G^\star(\Pi) = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}$ and optimal variance
  $\sigma_\star^2(\Pi) = G^\star/\Pi = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})$ (Proposition 3.5).

---

## Lemma 3.6 (`single-minimum-gain`)

**Draft:**

**Lemma 3.6 (single minimum in the gain).** At fixed Π, σ² is strictly decreasing in G on (0, G⋆) and strictly increasing on (G⋆, ∞).

**Repository:**

**Lemma 3.6 (single minimum in the gain).** Fix $\Pi > 0$. On $G \in [0,\infty)$,
$$
\frac{\partial\sigma^2}{\partial G} = \frac{G^2 + 2\lambda G - 2\Sigma\Pi}{2\Pi(\lambda + G)^2}.
$$
The numerator has exactly one positive root, $G^\star(\Pi)$, so $\sigma^2(\cdot, \Pi)$ is strictly decreasing on
$[0, G^\star]$ and strictly increasing on $[G^\star, \infty)$, with minimum value $\sigma_\star^2(\Pi) = G^\star/\Pi < F$.
Moreover $\sigma^2(0, \Pi) = F$, $\sigma^2 \to \infty$ as $G \to \infty$, and $\sigma^2(G, \Pi) \le F \iff 0 \le G \le 2F\Pi$,
with equality exactly at $G = 0$ and $G = 2F\Pi$.

---

## Lemma 3.7 (`elasticity`)

**Draft:**

**Lemma 3.7 (elasticity form).** For any differentiable gain G(Π) > 0 with elasticity ε = ΠG′/G,

```latex
\frac{d\sigma^2}{d\Pi} = \frac{G\,N}{2\Pi^2(\lambda + G)^2},
\qquad
N = \varepsilon\,(G^2 + 2\lambda G - 2\Sigma\Pi) - G(\lambda + G)
```

The turning points of σ²(Π) are the sign changes of N. When G is strictly monotone, N is a function of G alone.

**Repository:**

**Lemma 3.7 (elasticity form).** For any differentiable $G(\Pi) > 0$ with elasticity $\varepsilon = \Pi G'/G$,
$$
\frac{d\sigma^2}{d\Pi} = \frac{G\,N}{2\Pi^2(\lambda + G)^2},
\qquad
N = \varepsilon\,(G^2 + 2\lambda G - 2\Sigma\Pi) - G(\lambda + G).
$$
Turning points of $\sigma^2(\Pi)$ are the sign changes of $N$. When $G$ is strictly monotone, $N$ is a function of $G$ alone.

---

## Theorem 4.1 (`monotone-gain-sweeps`)

**Draft:**

**Theorem 4.1 (monotone gain sweeps cannot window).** Fix Π. Let θ ↦ G(θ) be continuous and strictly monotone on D. Then σ²(G(θ), Π) is strictly monotone or strictly decreasing-then-increasing on D. Every failure set is therefore Empty, All, a lower ray, an upper ray or two rays; no window component and no mixed class can occur.

**Repository:**

**Theorem 4.1 (monotone gain sweeps cannot window).** Fix $\Pi$. Let $\theta \mapsto G(\theta)$ be continuous and strictly
monotone on $D$. Then $\sigma^2(G(\theta), \Pi)$ is strictly monotone or strictly decreasing-then-increasing, so every
failure set is Empty, All, a lower ray, an upper ray or two rays. No window and no mixed class occur.

---

## Proposition 4.2 (`prior-endpoints`)

**Draft:**

**Proposition 4.2 (prior precision: endpoints and extrema).**

- L₊ = F, approached from below; L₋ = V\_c, with the approach direction below.
- If Π ≥ Π\_A (c ≤ G⋆), σ² increases strictly from V\_c, approached from above, to F. There is no interior extremum.
- If Π < Π\_A (c > G⋆), there is exactly one interior extremum, a global minimum at Π₀⋆ = Π(c/G⋆ − 1) with value σ⋆²(Π); V\_c is then approached from below.
- V\_c > F iff Π < Π\_B, and V\_c = F iff Π = Π\_B.

**Repository:**

**Proposition 4.2 (prior precision: endpoints and extrema).**
- $L_+ = F$, approached from below; $L_- = V_c$, with the approach direction given below.
- If $c \le G^\star$ (i.e. $\Pi \ge \Pi_A$): $\sigma^2$ increases strictly from $V_c$ (approached from above) to $F$.
- If $c > G^\star$ ($\Pi < \Pi_A$): one interior extremum, a global minimum at $\Pi_0^\star = \Pi(c/G^\star - 1)$ with value
  $\sigma_\star^2(\Pi)$; $V_c$ is then approached from below.
- $V_c > F \iff c > 2F\Pi \iff \Pi < \Pi_B$, and $V_c = F \iff \Pi = \Pi_B$.

---

## Proposition 4.3 (`prior-classification`)

**Draft:**

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

**Repository:**

**Proposition 4.3 (prior precision: classification at every tolerance).**

*Case P1, $\Pi \ge \Pi_A$.* Sequence $(V_c, F)$: All ($R^2 \le V_c$), upper ray ($V_c < R^2 < F$), Empty ($R^2 \ge F$).

*Case P2, $\Pi_B \le \Pi < \Pi_A$.* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < V_c \le F$: All
($R^2 < \sigma_\star^2$); two rays ($R^2 = \sigma_\star^2$, the domain minus $\Pi_0^\star$; and $\sigma_\star^2 < R^2 < V_c$);
upper ray ($V_c \le R^2 < F$); Empty ($R^2 \ge F$). At $\Pi = \Pi_B$ the upper-ray row is empty.

*Case P3, $\Pi < \Pi_B$.* Sequence $(V_c, \sigma_\star^2, F)$ with $\sigma_\star^2 < F < V_c$: All ($R^2 < \sigma_\star^2$);
two rays ($\sigma_\star^2 \le R^2 < F$); lower ray ($F \le R^2 < V_c$); Empty ($R^2 \ge V_c$).

---

## Proposition 4.4 (`coupling-endpoints`)

**Draft:**

**Proposition 4.4 (coupling: endpoints and extrema).** L₋ = F, approached from below, and L₊ = ∞. There is exactly one interior extremum, a global minimum at

```latex
c^\star = \frac{G^\star(\Pi)}{K} = \frac{(\Pi + \Pi_0)\big(\sqrt{\lambda^2 + 2\Sigma\Pi} - \lambda\big)}{\Pi}
```

with value σ⋆²(Π). The variance returns to F at c\_F = 2FΠ/K = 2F(Π + Π₀), and σ² > F iff c > c\_F.

**Repository:**

**Proposition 4.4 (coupling: endpoints and extrema).** $L_- = F$ (from below), $L_+ = \infty$. One interior extremum, a
global minimum at $c^\star = G^\star(\Pi)/K$ with value $\sigma_\star^2(\Pi)$. $\sigma^2 = F$ again at
$c_F = 2F(\Pi + \Pi_0)$, and $\sigma^2 > F$ iff $c > c_F$.

---

## Proposition 4.5 (`coupling-classification`)

**Draft:**

**Proposition 4.5 (coupling: classification at every tolerance).** There is no case split.

| Tolerance | Class |
| --- | --- |
| R² < σ⋆² | All |
| R² = σ⋆² | Two rays (D minus the single point c⋆) |
| σ⋆² < R² < F | Two rays |
| R² ≥ F | Upper ray (c\_R, ∞), equal to (c\_F, ∞) at R² = F |

The class is never Empty, because σ² → ∞ as c → ∞, and never a window.

**Repository:**

**Proposition 4.5 (coupling: classification).** All ($R^2 < \sigma_\star^2$); two rays ($\sigma_\star^2 \le R^2 < F$; at
$R^2 = \sigma_\star^2$ the domain minus $c^\star$); upper ray ($R^2 \ge F$, equal to $(c_F, \infty)$ at $R^2 = F$). Never
Empty and never a window.

---

## Theorem 5.1 (`realizability`)

**Draft:**

**Theorem 5.1 (gain realizability).** Fix λ, Σ > 0. A function v : (0, ∞) → (0, ∞) is the variance curve σ²(G(Π), Π) of some continuous gain schedule G ≥ 0 if and only if v is continuous and v ≥ σ⋆² everywhere. One such gain is the upper-branch inverse

```latex
G_+(v, \Pi) = \Pi v + \sqrt{\Pi\,(\Pi v^2 + 2\lambda v - 2\Sigma)}
```

**Repository:**

**Theorem 5.1 (gain realizability).** Fix $\lambda, \Sigma > 0$. A function $v : (0,\infty) \to (0,\infty)$ equals
$\sigma^2(G(\Pi), \Pi)$ for some continuous gain schedule $G \ge 0$ iff $v$ is continuous and $v \ge \sigma_\star^2$
everywhere. One such gain is the upper-branch inverse $G_+(v, \Pi) = \Pi v + \sqrt{\Pi(\Pi v^2 + 2\lambda v - 2\Sigma)}$.

---

## Corollary 5.2 (`forced-lower-ray`)

**Draft:**

**Corollary 5.2 (forced lower ray).** For every continuous gain schedule and every R² < F, the failure set contains (0, π\_R), with π\_R = 2λ(F − R²)/R⁴. Hence ℓ = 1: at a tolerance tighter than the floor, no gain gives Empty, a pure window, an upper ray alone, or any other class with ℓ = 0.

**Repository:**

**Corollary 5.2 (forced lower ray).** For every continuous gain schedule and every $R^2 < F$, the failure set contains
$(0, \pi_R)$ with $\pi_R = 2\lambda(F - R^2)/R^4$. Hence $\ell = 1$: at a tolerance tighter than the floor no gain gives
Empty, a pure window, an upper ray alone, or any class with $\ell = 0$.

---

## Corollary 5.3 (`exact-class-set`)

**Draft:**

**Corollary 5.3 (exact class set along precision).** For continuous, piecewise strictly monotone variance curves: for R² < F the achievable classes are exactly those with ℓ = 1 (any u, any finite k, including All); for R² ≥ F every class with finite k is achievable.

**Repository:**

**Corollary 5.3 (exact class set along precision).** For continuous, piecewise strictly monotone variance curves: for
$R^2 < F$ the achievable classes are exactly those with $\ell = 1$ (any $u$, any finite $k$, including All); for $R^2 \ge F$
every class with finite $k$ is achievable.

---

## Corollary 5.4 (`unbounded-windows`)

**Draft:**

**Corollary 5.4 (unbounded windows for regular gains).** For every k ≥ 1 there is a C^∞ gain schedule with the regularity of Theorem 3.4 (G → 0 and G²/Π → 0 as Π → 0; G → G∞ ∈ (0, ∞)) whose failure set at R² = 1.25F has exactly k windows.

**Repository:**

**Corollary 5.4 (unbounded complexity inside the model).** For every $k \ge 1$ there is a $C^\infty$ gain schedule satisfying
the starting study's regularity ($G \to 0$ and $G^2/\Pi \to 0$ as $\Pi \to 0$; $G \to G_\infty \in (0,\infty)$) whose failure set at
$R^2 = 1.25F$ has exactly $k$ windows.

---

## Corollary 5.5 (`regularity-pins`)

**Draft:**

**Corollary 5.5 (what regularity pins).** Under the regularity of Theorem 3.4, L₋ = F and L₊ = H = Σ/(λ + G∞). So ℓ is fixed by R² against F (with the approach direction when R² = F), u by R² against H, and k is unbounded (Corollary 5.4). Since H < F, there is never an upper ray when R² ≥ F.

**Repository:**

**Corollary 5.5 (what regularity pins).** Under the starting study's regularity, $L_- = F$ and $L_+ = H = \Sigma/(\lambda + G_\infty)$. So
$\ell$ is fixed by $R^2$ versus $F$ (plus the approach direction at $R^2 = F$), $u$ by $R^2$ versus $H$, and $k$ is unbounded
(Corollary 5.4); since $H < F$, there is never an upper ray at $R^2 \ge F$.

---

## Lemma 5.6 (`excess-components`)

**Draft:**

**Lemma 5.6 (excess components).** {σ² > F} = {G/Π > 2F} pointwise. Hence at R² = F the failure set is the excess set; for R² ≥ F every failure component lies in an excess component; and if G/Π is unimodal or decreasing, there is at most one window at R² = F.

**Repository:**

**Lemma 5.6 (excess components).** $\{\sigma^2 > F\} = \{G/\Pi > 2F\}$ pointwise. Hence at $R^2 = F$ the failure set is the
excess set; for $R^2 \ge F$ every failure component lies in an excess component; and if $G/\Pi$ is unimodal or decreasing
there is at most one window at $R^2 = F$.

---

## Lemma 5.7 (`bounded-gain-limit`)

**Draft:**

**Lemma 5.7 (bounded gains approach H from above).** If G < G∞ everywhere, then σ² ≥ Σ/(λ + G) > H, so H is approached from above and never attained.

**Repository:**

**Lemma 5.7 (bounded gains approach $H$ from above).** If $G < G_\infty$ everywhere, then
$\sigma^2 \ge \Sigma/(\lambda + G) > H$, so $H$ is approached from above and never attained.

---

## Proposition 5.8 (`bayesian-weight`)

**Draft:**

**Proposition 5.8 (Bayesian-weight gain along precision).** Let G = cΠ/(Π + Π₀), with over-weighting ratio κ = (c/Π₀)/F. Then σ² has one turning point, a maximum M, iff κ > 2, and is strictly decreasing otherwise. The endpoint limits are F (approached from above iff κ > 2) and H = Σ/(λ + c) (approached from above). The classes are:

- κ > 2: All (R² ≤ H), lower ray (H < R² ≤ F), window (F < R² < M), Empty (R² ≥ M);
- κ ≤ 2: All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F).

**Repository:**

**Proposition 5.8 (Bayesian-weight gain along precision).** For $G = c\Pi/(\Pi + \Pi_0)$, with over-weighting ratio
$\kappa = (c/\Pi_0)/F$: $\sigma^2$ has one turning point, a maximum $M$, iff $\kappa > 2$, and is strictly decreasing
otherwise. Endpoint limits $F$ (from above iff $\kappa > 2$) and $H = \Sigma/(\lambda + c)$ (from above). Classes: if
$\kappa > 2$, All ($R^2 \le H$), lower ray ($H < R^2 \le F$), window ($F < R^2 < M$), Empty ($R^2 \ge M$); if $\kappa \le 2$,
All ($R^2 \le H$), lower ray ($H < R^2 < F$), Empty ($R^2 \ge F$).

---

## Proposition 5.9 (`misspecified-kalman`)

**Draft:**

**Proposition 5.9 (misspecified Kalman gain).** Let G = −λ′ + √(λ′² + 2Σ′Π), the steady-state gain designed for wrong parameters λ′ and Σ′, with F′ = Σ′/λ′ and r = Σ/Σ′. If F′ > 2F, σ² has exactly one turning point, a maximum, at the gain

```latex
G_M = \frac{-2r\lambda' + \sqrt{4r^2\lambda'^2 + 2(1 + r)\lambda'(\lambda - 2r\lambda')}}{1 + r},
\qquad
\Pi_M = \frac{G_M^2 + 2\lambda' G_M}{2\Sigma'}
```

If F′ ≤ 2F, σ² is strictly decreasing. L₋ = F (approached from above iff F′ > 2F) and L₊ = 0. The classes are lower ray (0 < R² ≤ F), window (F < R² < M) and Empty (R² ≥ M) when F′ > 2F, and lower ray (R² < F) and Empty (R² ≥ F) otherwise. All never occurs.

**Repository:**

**Proposition 5.9 (misspecified Kalman gain).** Let $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma'\Pi}$, $F' = \Sigma'/\lambda'$,
$r = \Sigma/\Sigma'$. If $F' > 2F$, $\sigma^2$ has exactly one turning point, a maximum, at the gain
$$
G_M = \frac{-2r\lambda' + \sqrt{4r^2\lambda'^2 + 2(1 + r)\lambda'(\lambda - 2r\lambda')}}{1 + r},
\qquad \Pi_M = \frac{G_M^2 + 2\lambda'G_M}{2\Sigma'};
$$
if $F' \le 2F$ it is strictly decreasing. $L_- = F$ (from above iff $F' > 2F$), $L_+ = 0$. Classes: $F' > 2F$: lower ray
($0 < R^2 \le F$), window ($F < R^2 < M$), Empty ($R^2 \ge M$); otherwise lower ray ($R^2 < F$), Empty ($R^2 \ge F$). All never
occurs.

---

## Proposition 5.10 (`capped-gain`)

**Draft:**

**Proposition 5.10 (capped gain).** Let G = min(gΠ, c). On the linear branch dσ²/dΠ = g(gλ/2 − Σ)/(λ + gΠ)², of constant sign g − 2F; on the capped branch σ² is strictly decreasing. So:

- g > 2F: one maximum, at the kink Π = c/g;
- g < 2F: σ² is strictly decreasing;
- g = 2F: a plateau σ² ≡ F on (0, c/g\], then strictly decreasing. By Theorem 2.4 the classes are All (R² ≤ H), lower ray (H < R² < F) and Empty (R² ≥ F).

The classes that occur are All, lower ray, window and Empty.

**Repository:**

**Proposition 5.10 (capped gain).** For $G = \min(g\Pi, c)$: on the linear branch
$d\sigma^2/d\Pi = g(g\lambda/2 - \Sigma)/(\lambda + g\Pi)^2$, of constant sign $g - 2F$; on the capped branch $\sigma^2$ is strictly
decreasing. So: $g > 2F$, one maximum at the kink $\Pi = c/g$; $g < 2F$, strictly decreasing; $g = 2F$, a plateau
$\sigma^2 \equiv F$ on $(0, c/g]$, then strictly decreasing (Theorem 2.4: All for $R^2 \le H$, lower ray for $H < R^2 < F$, Empty for $R^2 \ge F$). Classes:
All, lower ray, window, Empty.

---

## Proposition 5.11 (`precision-blind`)

**Draft:**

**Proposition 5.11 (precision-blind gain).** For a constant gain G = G₀, σ² decreases strictly from ∞ to H = Σ/(λ + G₀). The classes are All (R² ≤ H) and lower ray (R² > H).

A precision-blind gain over-gains at low precision without bound (q = G₀/(FΠ) → ∞), so its curve starts at ∞ and never returns to F; it fails the regularity of Theorem 3.4 at the low-precision end, and it never windows.

**Repository:**

**Proposition 5.11 (precision-blind gain).** For $G = G_0$, $\sigma^2$ decreases strictly from $\infty$ to $H$. Classes: All
($R^2 \le H$), lower ray ($R^2 > H$).

---

## Theorem 5.12 (`hill-turning-points`)

**Draft:**

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

**Repository:**

**Theorem 5.12 (Hill gain, every real $n > 1$).** Let $G = c\Pi^n/(\Pi^n + \Pi_0^n)$ with $n > 1$, $t = \Pi/\Pi_0$, $T = t^n$, and
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

---

## Proposition 5.13 (`hill-classification`)

**Draft:**

**Proposition 5.13 (Hill gain: classification and the mixed class).** Let H = Σ/(λ + c). σ² tends to F from below as Π → 0 (since G/Π → 0 < 2F) and to H from above as Π → ∞ (Lemma 5.7), and H < m < F when the pair exists, so two rays never occur. With the pair and M > F (for n = 2, Π₀ < cλ/(4Σ), the window condition of Theorem 3.4):

| Tolerance | Class |
| --- | --- |
| R² ≤ H | All |
| H < R² < m | Lower ray |
| m ≤ R² < F | Lower ray + window (1, 0, 1) |
| F ≤ R² < M | Window |
| R² ≥ M | Empty |

With the pair and M ≤ F: All (R² ≤ H), lower ray (H < R² < m), (1, 0, 1) (m ≤ R² < M), lower ray (M ≤ R² < F), Empty (R² ≥ F). Without the pair: All (R² ≤ H), lower ray (H < R² < F), Empty (R² ≥ F).

**Repository:**

**Proposition 5.13 (Hill gain: classification and the mixed class).** Let $H = \Sigma/(\lambda + c)$. $\sigma^2 \to F$ from below
at $0$ (since $G/\Pi \to 0 < 2F$) and $\to H$ from above at $\infty$ (Lemma 5.7), and $H < m < F$ when the pair exists, so two
rays never occur. With the pair and $M > F$ ($\Pi_0 < c\lambda/(4\Sigma)$ for $n = 2$, the starting study's window onset):

| Tolerance | Class |
|---|---|
| $R^2 \le H$ | All |
| $H < R^2 < m$ | Lower ray |
| $m \le R^2 < F$ | Lower ray + window $(1,0,1)$ |
| $F \le R^2 < M$ | Window |
| $R^2 \ge M$ | Empty |

With the pair and $M \le F$: All ($R^2 \le H$), lower ray ($H < R^2 < m$), $(1,0,1)$ ($m \le R^2 < M$), lower ray
($M \le R^2 < F$), Empty ($R^2 \ge F$). Without the pair: All, lower ray ($H < R^2 < F$), Empty ($R^2 \ge F$).

---

## Proposition 5.14 (`no-mixed-decreasing-ratio`)

**Draft:**

**Proposition 5.14 (no mixed class when G/Π decreases).** In the setting of Theorem 3.4, suppose moreover that G is increasing and G(Π)/Π is strictly decreasing, as for any sum of Bayesian stages cᵢΠ/(Π + Π₀,ᵢ). Then σ² is strictly decreasing wherever σ² ≤ F. So every interior minimum lies above F, and no failure set combines a lower ray with a window: the classes (1, 0, k), k ≥ 1, do not occur.

**Repository:**

**Proposition 5.14 (no mixed class when $G/\Pi$ decreases).** In the setting of Theorem 3.4, if moreover $G$ is increasing and $G(\Pi)/\Pi$ is strictly decreasing (e.g. any sum of Bayesian stages
$c_i\Pi/(\Pi + \Pi_{0,i})$), then $\sigma^2$ is strictly decreasing wherever $\sigma^2 \le F$, so every interior minimum exceeds
$F$ and no failure set combines a lower ray with a window: the classes $(1,0,k)$, $k \ge 1$, do not occur.

---

## Numerical result 5.15 (`two-stage-gains`)

**Draft:**

**Numerical result 5.15 (two-stage gains).** Sums of two widely separated natural stages produce more than one maximum. Two-channel Bayesian gains show (max, min, max) in 7 of 2,000 parameter sets, giving multi-window failure sets. Two-channel Hill gains show (min, max, min, max) in 63 of 2,000 sets, giving mixed multi-window failure sets. For the Bayesian sums the windows always lie above F and never join a lower ray, as Proposition 5.14 requires. No bound on the number of turning points of such sums is known (chapter 9).

**Repository:**

**Numerical result 5.15 (two-stage gains).** Sums of two widely separated natural stages produce more than one maximum:
two-channel Bayesian gains show (max, min, max) in 7 of 2,000 sets, i.e. multi-window failure sets; two-channel Hill gains show
(min, max, min, max) in 63 of 2,000 sets, i.e. mixed multi-window failure sets. No turning-point bound is known. For the
Bayesian sums the windows always lie above $F$ and never join a lower ray (Proposition 5.14).

---
