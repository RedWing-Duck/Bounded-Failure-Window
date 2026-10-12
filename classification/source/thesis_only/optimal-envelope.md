*Thesis-only text, imported verbatim from the thesis draft (`t17/input/Thesis_Draft_ch1-7.md`, §3.4, lines 382–394; citations written [n]). Task 17.*

**Proposition 3.5 (optimal gain).** For this plant the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives

```latex
G^\star(\Pi) = p\,\Pi = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
\qquad
\sigma_\star^2(\Pi) = p = \frac{2\Sigma}{\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}}
```

G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.

**Lemma 3.6 (single minimum in the gain).** At fixed Π, σ² is strictly decreasing in G on (0, G⋆) and strictly increasing on (G⋆, ∞).

*Proof of Proposition 3.5 and Lemma 3.6.* The Riccati equation and its positive root give the steady-state Kalman–Bucy filter [1, 39, 40]. Differentiating the formula of Proposition 3.1 in G gives ∂σ²/∂G = (G² + 2λG − 2ΣΠ)/(2Π(λ + G)²), whose only positive zero is G⋆; this is Lemma 3.6, and it gives the minimality in Proposition 3.5. σ⋆² decreases strictly in Π because √(λ² + 2ΣΠ) increases, and it tends to 2Σ/(2λ) = F as Π → 0. Dividing G⋆ by FΠ with ν = 2ΣΠ/λ² gives q⋆ = 2(√(1 + ν) − 1)/ν = 2/(1 + √(1 + ν)). ∎
