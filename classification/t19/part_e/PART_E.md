# Task 19 Part E: Conjecture 6.22, exploratory notes

Not pass/fail; the conjecture's status is unchanged. Summary in RESULTS_t19.md, For the author 7.

- `e1_structure.py` / `.json`: the D1 derivatives as exponential polynomials (post, prior 6 terms, avg 11); Pólya–Szegő bounds 13, 13, 25.
- `e2_scan.py` / `.json`: dimensionless reduction (t, g, ν) checked symbolically; prior counted through p′ − 2(p − 1); 41 × 41 grid of
  (g, ν) ∈ [1e-4, 1e4]², t ∈ [1e-8, 1e8]: post {0: 861, 1: 820}, avg {0: 745, 1: 936}, prior {0: 765, 1: 861, 2: 55}; never > 2.
  (A first 5 × 5 smoke run used the raw prior derivative, whose e^(−2t) factor is unresolvable at large t; it was replaced before the
  full scan.)
- `e3_ends.py` and the endpoint expansions in RESULTS_t19: parity of the number of turning points (post, prior odd iff g > ν; avg odd
  iff g² + 4g > 4ν).
- `e4_parity.py` / `.json`: the scan's counts against the parity rule: 41 disagreements, all on g = ν, where the rule does not apply.
