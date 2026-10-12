## Proposition 3.1

### Draft

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters \[4–9, 36–38\].

### Thesis render

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters [4–9, 36–38].

## Proposition 3.5

### Draft

**Proposition 3.5 (optimal gain).** For this plant the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives

```latex
G^\star(\Pi) = p\,\Pi = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
\qquad
\sigma_\star^2(\Pi) = p = \frac{2\Sigma}{\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}}
```

G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.

### Thesis render

**Proposition 3.5 (optimal gain).** For this plant the steady-state Riccati equation 0 = 2Σ − 2λp − Πp² gives

```latex
G^\star(\Pi) = p\,\Pi = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi},
\qquad
\sigma_\star^2(\Pi) = p = \frac{2\Sigma}{\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}}
```

G⋆ also minimises σ² over constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain. σ⋆² decreases strictly from F as Π grows, so G⋆ = σ⋆²Π < FΠ for every Π > 0. In the coordinates of §3.2, q⋆ = G⋆/(FΠ) and σ⋆²/F = 𝒱⋆ = q⋆.

