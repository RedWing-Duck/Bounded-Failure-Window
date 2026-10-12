*Thesis-only text, imported verbatim from the thesis draft (`t16/input/Thesis_Draft_ch1-5.md`, §2.8, lines 232–251 and 257; refreshed in Task 16 from `t15/input/Thesis_Draft_ch1-4.md`, lines 232–251, adding the "Direction in condition 2" remark).*

**Proposition 2.9.** Let σ² satisfy C2 and let R² ∉ 𝒞. Then the crossing set {θ : σ²(θ) = R²} is finite, say {x₁, …, x\_m}. Choose disjoint compact intervals Nᵢ ⊂ D, each inside one monotone piece, with xᵢ in the interior of Nᵢ, and set

```latex
\eta = \inf\big\{\,|\sigma^2(\theta) - R^2| : \theta \in D \setminus \textstyle\bigcup_i \operatorname{int} N_i\big\}
```

Then η > 0, and every continuous σ̃² on D with

1. sup over D of |σ̃² − σ²| < η, and
2. σ̃² strictly monotone on each Nᵢ

has failure set 𝓕̃(R²) of the same class as 𝓕(R²).

*Proof.*

- **Finitely many crossings.** Since R² is not a turning-point value, crossings lie inside pieces, at most one per strictly monotone piece.
- **η > 0.** The function |σ² − R²| is continuous and positive on the closed set K = D \\ ∪ int Nᵢ, which contains no crossing. Near θ± it tends to |L± − R²|, which is positive because L± ∈ 𝒞 when finite (or to ∞). So it is bounded below on the tails, and on the compact remainder.
- **Signs off the crossings.** On K, condition 1 gives σ̃² − R² the same sign as σ² − R².
- **One crossing per Nᵢ.** The ends of Nᵢ lie in K, where σ² − R² takes opposite signs; so does σ̃² − R². By condition 2, σ̃² crosses R² exactly once in Nᵢ, in the same direction.
- **Conclusion.** σ̃² − R² and σ² − R² have the same ordered pattern of positive and negative intervals along D, ends included. Components correspond one to one, and so do the components touching each end. ∎

**Direction in condition 2.** Condition 2 names no direction, and none is needed: by condition 1, σ̃² − R² has the same sign as σ² − R² at both ends of Nᵢ, and those signs are opposite, so a strictly monotone σ̃² on Nᵢ is monotone in the same direction as σ².
