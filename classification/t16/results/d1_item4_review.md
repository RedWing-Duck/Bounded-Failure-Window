# D1 item 4: logical review of "Direction in condition 2" (Proposition 2.9), written after the recorded run (bc0a72c)

The remark: *Condition 2 names no direction, and none is needed: by condition 1, σ̃² − R² has the same sign as σ² − R² at both
ends of Nᵢ, and those signs are opposite, so a strictly monotone σ̃² on Nᵢ is monotone in the same direction as σ².*

Step by step, with Nᵢ = [a, b]:

1. **The ends lie in K.** K = D \ ∪ int Nⱼ. The points a, b are not interior points of Nᵢ, and the Nⱼ are disjoint, so a, b ∈ K.
   (Stated in the proof's step "One crossing per Nᵢ".)
2. **σ² − R² is nonzero at a and b, with |σ² − R²| ≥ η there.** By the definition of η as the infimum over K, and η > 0.
3. **Same sign for σ̃².** Condition 1 gives |σ̃² − σ²| < η ≤ |σ² − R²| at a and b, so σ̃² − R² has the sign of σ² − R² there.
   This is the remark's "by condition 1".
4. **Opposite signs.** Nᵢ lies inside one strictly monotone piece of σ² and contains the crossing xᵢ in its interior. σ² − R² is
   strictly monotone on [a, b] and vanishes at xᵢ ∈ (a, b), so it has opposite signs at a and b. Other crossings cannot lie in Nᵢ
   (each lies in the interior of its own, disjoint Nⱼ; and a strictly monotone piece has at most one crossing).
5. **Direction.** Say σ² increases on Nᵢ: σ²(a) < R² < σ²(b). By step 3, σ̃²(a) < R² < σ̃²(b), so σ̃²(a) < σ̃²(b). A strictly
   monotone function with f(a) < f(b) is increasing. The decreasing case is symmetric.

Every step follows from the statement's hypotheses and the definitions; nothing is assumed beyond them. The remark is complete as
written. Steps 1, 2 and 4 are left implicit in the remark ("at both ends", "those signs are opposite"), but each is established
in the proof's own steps ("η > 0", "One crossing per Nᵢ").

The numeric part (t16_checks.json, D1 item 4: 1,000 (curve, Nᵢ) pairs with perturbations satisfying conditions 1 and 2, seed
16002) found no counterexample.

**Verdict: holds.**
