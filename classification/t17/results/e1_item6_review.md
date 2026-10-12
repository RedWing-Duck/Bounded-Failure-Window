# E1 item 6: does Corollary 7.4 follow from Corollary 7.3 and Proposition 7.7(a), as written? (after the recorded run, 81e977c)

The statement has two sentences; the draft's proof is "Corollary 7.3, and Proposition 7.7(a) below for the precision sweep."

**Sentence 1.** *Along a causally ordered sweep, a failure set with a window, two rays or a mixed class certifies that the filter
is not optimal.* Corollary 7.3's first conclusion (P non-increasing, so every optimal failure set is an initial segment; a final
segment for the reverse order) needs no continuity. A window, two rays or a mixed class is neither an initial nor a final segment,
so no such set is the optimal filter's. **Follows from Corollary 7.3.**

**Sentence 2.** *With Theorem 5.1, the precision-sweep picture is complete: the optimal filter sits on the envelope σ⋆² (classes
lower ray and Empty), and every curve strictly above it belongs to some miscalibrated gain.*
- "Sits on the envelope": the definition of σ⋆² (Proposition 3.5).
- "Classes lower ray and Empty": Proposition 7.7(a) orders the precision sweep and σ⋆² is continuous, so Corollary 7.3 gives
  Empty, All or a lower ray. Excluding **All** needs inf σ⋆² = 0, i.e. σ⋆² → 0 as Π → ∞ (Proposition 3.5, Theorem 3.4). The proof
  does not cite it.
- "Every curve strictly above it belongs to some miscalibrated gain": this is Theorem 5.1 (a continuous v ≥ σ⋆² is realised by G₊,
  and v > σ⋆² means G ≠ G⋆). The statement names Theorem 5.1; the proof does not.

**Verdict: fails as written (ambiguous on a lenient reading).** Every clause of the corollary is true, but the proof as written
(Corollary 7.3 and Proposition 7.7(a)) does not cover the exclusion of All, which needs σ⋆² → 0 (Proposition 3.5), or the last
clause, which is Theorem 5.1. Reading "With Theorem 5.1" in the statement as part of the proof still leaves σ⋆² → 0 uncited.
Suggested proof: "Corollary 7.3 with Proposition 7.7(a); σ⋆² decreases strictly from F to 0 (Proposition 3.5), which excludes
All; and Theorem 5.1."
