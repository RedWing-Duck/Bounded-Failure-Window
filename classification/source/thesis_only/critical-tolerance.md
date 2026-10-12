*Thesis-only text, imported verbatim from the thesis draft (`t18/input/Thesis_Draft_full.md`, §2.3, lines 158–165; citations written [n]). Task 18.*

**Theorem 2.2.** Assume C1–C6.

1. **Local constancy.** The class of 𝓕(R²) is constant on each connected component of (0, ∞) \\ 𝒞. It can change only when R² crosses or equals a critical tolerance.
2. **Rays.** ℓ = 1 if R² < L₋ and ℓ = 0 if R² > L₋. If R² = L₋, then ℓ = 1 iff σ² approaches L₋ from above. The same holds for u with L₊.
3. **Window components.** Each window component contains an interior local maximum tⱼ with σ²(tⱼ) > R², and distinct components contain distinct maxima. Hence k is at most the number of interior maxima above R², with equality iff each such maximum lies in its own component touching neither end.
4. **Determining data.** The class of 𝓕(R²), for every R², is determined by the ordered sequence (L₋, σ²(t₁), …, σ²(tₙ), L₊) and the two approach directions. The positions tⱼ are needed only to locate the components.

*Proof.* (1) On each piece, σ² is a strictly monotone bijection onto the open interval between its end values, all of which lie in 𝒞 or are infinite. For R² ∉ 𝒞, the piece's contribution to 𝓕 is empty, the whole piece, or a one-sided subinterval at its larger end, decided by where R² sits relative to the end values. Adjacent contributions join exactly when the shared turning-point value exceeds R². All of this is constant between critical tolerances. (2) Near θ₋, σ² is close to L₋; at equality the first piece is strictly monotone, so it lies entirely above or entirely below L₋. (3) A window component (a, b) has a, b ∈ D with σ²(a) = σ²(b) = R² and σ² > R² between, so σ² attains an interior maximum there, which is a turning point. Disjoint components contain distinct maxima. (4) The construction in (1) uses only the end values of each piece, and (2) adds the approach directions. ∎
