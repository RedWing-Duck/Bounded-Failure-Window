# Pre-registration — Task 6: coloured-noise symbolic check (`t6_colored_symbolic.py`)

Committed **before** `t6_colored_symbolic.py` is run. This file is not edited after
its commit. If a criterion turns out to be badly posed, that is reported in the
results; the criterion is not changed.

## Model
State (x, η), a = λ + G (G a free positive symbol unless a gain is substituted):

    dx = (−a x + G η) dt + sqrt(2Σ) dW_sim
    dη = (−η/τ) dt + (1/(τ√Π)) dW_s

Drift A = [[−a, G], [0, −1/τ]], diffusion B = diag(sqrt(2Σ), 1/(τ√Π)). The stationary
covariance C solves A·C + C·Aᵀ + B·Bᵀ = 0 (three linear equations for C_xx, C_xη, C_ηη,
solved exactly with SymPy). F = Σ/λ.

## Step 1 — normalisation of t4b (reported, not a pass/fail criterion)
The script reads `t4b_colored.py` without modifying or running it as a whole. It quotes
the `make_sensory` source and the line that multiplies the sensory increment by
G/√Π. It then executes only `make_sensory` (extracted with `ast`), zeroes its internal
state and feeds a unit impulse to recover ρ and the innovation scale. From those it
derives the stationary variance and integrated autocovariance of the noise that
actually multiplies G·dt. Expected: variance 1/(2Πτ), ∫autocov = 1/Π, i.e.
dη = −η/τ dt + (1/(τ√Π)) dW_s. Any discrepancy is reported, and the derivation
uses t4b's actual normalisation.

## Criteria
Symbolic identities are first tested with `sympy.simplify(difference) == 0`.
Independently, every identity in C1–C4 is evaluated at 20 random positive parameter
sets. Each of λ, c, Σ, P, Π, τ, G is drawn log-uniformly in [1e-2, 1e2] with
`numpy.random.default_rng(6006)`, converted to exact rationals and evaluated with
SymPy `evalf(50)` (50 significant digits). It passes if
|L − R| ≤ 1e-12 · max(|L|, |R|) at all 20 sets. A criterion PASSES if the
simplification returns 0. If the simplification does not return 0 but the numeric
check passes, the result is reported as "PASS (numeric only; simplification
inconclusive)". Both results are always reported.

- **C1.** C_xx − (Σ + G²/(2Π(1+aτ)))/a ≡ 0.
- **C2.** lim_{τ→0} C_xx − (Σ + G²/(2Π))/(λ+G) ≡ 0. The limit is taken with `sympy.limit`,
  and τ = 0 is also substituted directly.
- **C3.** `sympy.factor(C_xx − F)` is reported verbatim. Then
  C_xx − F − G(λG/(2Π(1+aτ)) − Σ)/(λa) ≡ 0, and
  (λG/(2Π(1+aτ)) − Σ)·(2(1+aτ)/λ) − (G/Π − 2F(1+aτ)) ≡ 0, whose multiplier 2(1+aτ)/λ
  is positive. Since G/(λa) > 0, these give C_xx > F ⇔ G/Π > 2F(1+aτ).
  PASS iff both identities hold.
- **C4.** With G = cΠ/(Π+P), and a = λ + G substituted, the series of C_xx at Π = 0 to
  O(Π²) has constant term F ≡ Σ/λ and linear coefficient s1 with
  s1 − c(cλ − 2PΣ(1+λτ))/(2P²λ²(1+λτ)) ≡ 0. The ratio s1/(c/P − 2F(1+λτ)) must
  simplify to an expression that SymPy proves positive for positive symbols. If s1
  differs, it is reported verbatim with the condition it implies. PASS iff all three hold.
- **C5.** At λ = c = 1, Σ = 0.01, P = 1, maximise C_xx over Π on
  `numpy.logspace(-4, 4, 200001)` for τ ∈ {0.01, 0.1, 1, 10}. Peak height and location
  must match the t4b semi-analytic peaks reported in REPORT.md (read from
  `results/t4b.json`; displayed there as 0.09169 at 0.684, 0.08234 at 0.654,
  0.04326 at 0.539, 0.01356 at 0.33) to 3 significant figures. "Match" means both
  values round to the same 3-s.f. number. PASS iff all 8 comparisons match.
  *Anticipated risk, stated before running:* t4b located its peaks on
  `logspace(-3, 4, 4001)`, a step of 0.00175 decades (≈0.4 % in Π), which is coarser than 3 s.f.
  for locations. A location mismatch may therefore come from t4b's grid rather than
  from the formula. As an informational diagnostic, C_xx is also maximised on t4b's
  exact grid and compared with the t4b values (relative tolerance 1e-12).
- **C6.** At P = 1 (λ = c = 1, Σ = 0.01), C4 predicts an initial rise iff τ < 49. For
  τ ∈ {48, 48.9, 49.1, 50}, the numeric slope (C_xx(ε) − F)/ε with ε = 1e-10 is
  computed in 50-digit arithmetic from the Lyapunov solution. The value of s1 is
  also reported. PASS iff the sign of the numeric slope is positive for 48 and 48.9,
  and negative for 49.1 and 50.
  *Informational:* for τ ∈ {50, 100, 1000}, the script reports on the C5 grid
  max_Π(C_xx) − F, computed in the cancellation-free form from C3, and
  sup_Π [G/Π − 2F(1+aτ)], with the Π at which each is attained.

## Outputs
`results/t6_colored.txt` (human-readable) and `results/t6.json` (machine-readable). The
REPORT.md section "Task 6 — coloured-noise symbolic check" is generated from
`results/t6.json` by `t6_report.py`, which appends to REPORT.md (or replaces the T6
section if it is already there) and leaves the earlier sections untouched.
`run_all.sh` runs t6 and then `t6_report.py` after `make_report.py`.
