*Thesis-only text, imported verbatim from the thesis draft (`t17/input/Thesis_Draft_ch1-7.md`, §3.1, lines 306–316; citations written [n]). Task 17.*

A scalar error x is corrected toward a noisy signal with a gain G that depends on the observation precision Π:

```latex
\dot x = -(\lambda + G)\,x + G\,\xi_s + \xi_{\mathrm{sim}},
\qquad
\sigma^2 = \frac{\Sigma + G^2/(2\Pi)}{\lambda + G}
```

**Proposition 3.1 (stationary variance).** Here ξ\_s is white noise of intensity 1/Π and ξ\_sim white noise of intensity 2Σ, and the stationary variance is the formula above. If G → 0 and G²/Π → 0 as Π → 0, σ² tends to the floor F = Σ/λ; if G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit H = Σ/(λ + G∞) < F. So Σ is half the diffusion intensity: without correction the state obeys dx = −λx dt + √(2Σ) dW, whose stationary variance is the floor F = Σ/λ. Under the other common convention, dx = −λx dt + σ dW, every F below reads σ²/(2λ). The equation is exactly the error equation of a constant-gain filter for a hidden Ornstein–Uhlenbeck state, so σ² is an actual error variance, as in the sensitivity analysis of mismatched filters [4–9, 36–38].

*Proof.* The state x is an Ornstein–Uhlenbeck process with rate a = λ + G and noise intensity D = G²/Π + 2Σ, so its stationary variance is D/(2a), which is the formula above. The two limits follow by substitution. ∎
