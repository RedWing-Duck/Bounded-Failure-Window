*Thesis-only text, imported verbatim from the thesis draft (`t17/input/Thesis_Draft_ch1-7.md`, §6.3, lines 1014–1024; citations written [n]). Task 17.*

**Proposition 6.13 (discrete excess condition).** For a fixed gain 0 ≤ L < 2, the prior error is

```latex
P^- = \frac{a^2 L^2 r + q}{1 - a^2(1 - L)^2},
\qquad
P^+ - F = \frac{P^- - F}{a^2}
```

and P⁻ > F iff P⁺ > F iff L/(2 − L) > φ. The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < φ/2 for every Δt > 0.

*Proof.* With q = F(1 − a²), the numerator of P⁻ − F is a²L²r + F(1 − a²) − F + Fa²(1 − L)² = a²L(Lr − F(2 − L)), and the denominator is positive for 0 ≤ L < 2; so P⁻ > F iff Lr > F(2 − L), that is L/(2 − L) > F/r = φ. P⁻ = a²P⁺ + q gives P⁺ − F = (P⁻ − F)/a². For the optimal filter, L⋆ = P⁻/(P⁻ + r) with P⁻ < F, so L⋆/(2 − L⋆) = P⁻/(P⁻ + 2r). This is below F/(2r) iff P⁻(2r − F) < 2rF, which holds because P⁻ < F. ∎
