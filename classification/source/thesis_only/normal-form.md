*Thesis-only text, imported verbatim from the thesis draft (`t16/input/Thesis_Draft_ch1-5.md`, §3.2, lines 298–322; refreshed in Task 16 from `t15/input/Thesis_Draft_ch1-4.md`, lines 292–316).*

Two dimensionless numbers carry all the dependence on λ, Σ, Π and G:

```latex
\nu = \frac{2F\Pi}{\lambda} = \frac{2\Sigma\Pi}{\lambda^2},
\qquad
q = \frac{G}{F\Pi}
```

ν is the signal-to-noise ratio accumulated over one relaxation time 1/λ; q is the gain measured against the floor precision FΠ. In them the variance takes one form.

**Theorem 3.2 (normal form).**

```latex
\frac{\sigma^2}{F} = \mathcal V(\nu, q) = \frac{1 + \nu q^2/4}{1 + \nu q/2}
```

*Proof.* Divide σ² by F = Σ/λ: σ²/F = (1 + G²/(2ΠΣ))/(1 + G/λ). With G = qFΠ, G/λ = νq/2 and G²/(2ΠΣ) = q²FΠ/(2λ) = νq²/4. ∎

This is Lemma 6.23 in better coordinates: with g = G/λ = νq/2 it reads (1 + g²/ν)/(1 + g). The coordinate q is preferred because the floor crossing and the optimal filter become simple in it (§3.3–3.4). Reducing filter performance to dimensionless indices is not new: Kalata's tracking index \[25\] does it with one parameter for α–β trackers. The contribution here is this two-parameter form for the continuous-time relay, and its use as a map of failure regions. Two partial derivatives are used throughout:

```latex
\frac{\partial \mathcal V}{\partial q} = \frac{\nu\,(\nu q^2 + 4q - 4)}{2(\nu q + 2)^2},
\qquad
\frac{\partial \mathcal V}{\partial \nu} = \frac{q\,(q - 2)}{(\nu q + 2)^2}
```
