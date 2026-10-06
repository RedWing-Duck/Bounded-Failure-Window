# Pre-registration — verification of "A Bounded Failure Window in a Miscalibrated Precision-Weighted Relay"

Written and committed **before any simulation was run**. This file is not edited after
its commit. If a criterion turns out to be badly posed, that is reported in
`REPORT.md`; the criterion is not changed.

## Model (fixed)

Scalar relay, x = z − z*:

    dx = −(λ + G(Π)) x dt + G(Π) dW_s / sqrt(Π) + sqrt(2Σ) dW_sim,   G(Π) = c·Π/(Π + P)

Worked example: λ = c = 1, Σ = 0.01. Miscalibrated P = 1, calibrated P = 100.
Throughout, a = λ + G, D = G²/Π + 2Σ, so closed form (2) is σ² = D/(2a).

## Common simulation settings (Tasks 2, 3, 4b, 4c)

| item | value |
|---|---|
| Π grid ("main grid") | `numpy.logspace(-2, 2, 40)` ∪ {1/9, 0.687, 4}, sorted → 43 points |
| integrator | Euler–Maruyama, dt = 1e-3, x(0) = 0 |
| trajectories | 256 per Π (per relay) |
| burn-in | 20 time units (20 000 steps), discarded |
| sampling | 200 time units (200 000 steps), every step used |
| estimator | σ̂² = mean of x² over all sampled steps and trajectories (z* is known, mean not subtracted) |
| SE | batch means. Batch length 10 time units (= 10 × the longest relaxation time 1/λ = 1, since a ≥ λ) → 20 batches per trajectory × 256 = 5120 batch means; SE = sd(batch means, ddof=1)/sqrt(5120). In 4b batch length is max(10, 10·τ) time units. |
| SE of a comparison between two simulated quantities | batch-means SE of the per-batch **difference** (all relays and all Π share noise, see below, so estimates are paired) |
| noise | common random numbers: within one script, the same dW_s and dW_sim arrays drive every Π and every relay. Generated sequentially in 10-time-unit chunks from `numpy.random.default_rng(seed)` (PCG64), float64. |
| time stepping | the linear recursion x_{n+1} = (1 − a·dt)·x_n + u_n is evaluated with `scipy.signal.lfilter` (no Python loop over steps; loops only over chunks and Π) |

Seeds: T2 = 1002, T3 = 1003, T4a = 1041, T4b = 1042, T4c = 1043. (T1, T4d, T4e are deterministic.)

Runtime rule: if any script exceeds ~5 min, the number of trajectories for that
script is halved (repeatedly if needed), the change is documented in REPORT.md and
the resulting SE is reported. Tolerances are never changed.

## Task 1 — symbolic (`t1_symbolic.py`, output `results/t1_symbolic.txt`)

Criteria (each PASS iff the stated difference simplifies to exactly 0 with SymPy, or
the stated logical equivalence is proven):

- T1.1 Stationary variance of the OU SDE (from the Itô second-moment/Lyapunov equation
  d E[x²]/dt = −2a E[x²] + G²/Π + 2Σ = 0) minus (2) ≡ 0.
- T1.2 F = lim_{Π→0} σ² = Σ/λ and H = lim_{Π→∞} σ² = Σ/(λ+c) (for the Kalman gain).
- T1.3 Numerator of dσ²/dΠ (Kalman gain, after `together`) equals −k(Π)·(AΠ² + BΠ + C)
  with k(Π) > 0 for Π > 0, and A, B, C as stated: difference ≡ 0.
- T1.4 Slope at Π → 0 minus c(cλ − 2PΣ)/(2P²λ²) ≡ 0; and it is positive iff P < cλ/(2Σ)
  (sign of the factor (cλ − 2PΣ), all other factors positive).
- T1.5 Interior max exists iff P < cλ/(2Σ): with A>0, B>0, the quadratic has exactly
  one positive root iff C < 0 ⇔ P < cλ/(2Σ), and it is a max (derivative goes + → −).
- T1.6 Minimising (2) over free G at fixed Π gives G* = −λ + sqrt(λ² + 2ΣΠ) (the positive
  stationary point, a minimum), σ*² − G*/Π ≡ 0, σ*² − 2Σ/(λ + sqrt(λ²+2ΣΠ)) ≡ 0,
  and dσ*²/dΠ < 0 for Π > 0.
- T1.7 For G = g0Π + g1Π² + O(Π³): d σ²/dΠ at 0 minus (g0²/(2λ) − Σg0/λ²) ≡ 0.
- T1.8 (extra, stated now) σ² − F ≡ G(λG/(2Π) − Σ)/(λ(λ+G)) for any G, hence σ² > F ⇔ G/Π > 2Σ/λ.
- T1.9 Worked-example numbers (crossings by `scipy.optimize.brentq`, peak by solving the
  quadratic): peak 0.0929 at Π* ≈ 0.687; R² = 0.05 crossings 1/9 and 4; R² = 0.008
  threshold 82.67; calibrated (P=100) σ² = 0.0100, 0.00995, 0.0075 at Π = 0.01, 1, 100;
  optimal σ*² = 0.0100, 0.00995, 0.00732 at the same Π.
  "Agreement to 4 significant figures" is operationalised as follows (decided now,
  because several stated values carry fewer than 4 significant digits):
  n = min(4, number of significant digits in the stated value) — "1/9" and "4" are
  exact, so n = 4 — and PASS iff |computed − stated| ≤ 0.5·10^(floor(log10|stated|) − n + 1).
  A strict 4-significant-figure comparison (stated value padded with zeros) is also
  printed for information; it is not the pass criterion.
- T1 PASS iff every item above passes.
- Output includes the fully expanded derivative numerator in LaTeX.

## Task 2 — Euler–Maruyama check of (2) (`t2_em.py`)

P = 1, main grid, common settings. EM stationary variance D/(2a − a²dt) is reported
as "EM-corrected" prediction.

- T2.1 At every Π: |σ̂² − σ²_(2)| < max(3·SE, 0.03·σ²_(2)), with σ²_(2) the uncorrected
  closed form (2). (Also reported against the EM-corrected value, for information.)
- T2.2 |σ̂²(1/9) − 0.05| < 3·SE(1/9) and |σ̂²(4) − 0.05| < 3·SE(4).
- T2 PASS iff T2.1 and T2.2.
- Figure: closed form line, simulation points with ±SE error bars (log-log).

## Task 3 — paired comparison (`t3_paired.py`)

Relays (a) Kalman P = 1, (b) Kalman P = 100, (c) optimal G = G*(Π); identical noise
arrays for all three and all Π; main grid; common settings.

- T3.1 (a) argmax of σ̂² over the grid is not the first or last grid point.
- T3.2 (a) the sequence σ̂²(Π_i) − 0.05 over the sorted grid has exactly 2 sign changes.
  Each crossing is located by linear interpolation in (log Π, σ̂² − 0.05) between the
  bracketing grid points; the lower must satisfy |Π_lo/(1/9) − 1| < 0.15 and the upper
  |Π_hi/4 − 1| < 0.15.
- T3.3 For (b) and for (c) separately: for every Π_i, σ̂²(Π_i) − σ̂²(Π_1) < 3·SE_diff,
  where Π_1 = 0.01 (the "Π→0 value" is the simulated value at the smallest grid point).
- T3.4 For (b) and for (c): for every adjacent pair, σ̂²(Π_{i+1}) − σ̂²(Π_i) < 3·SE_diff.
- T3.5 For every Π: σ̂²_c − σ̂²_a < 3·SE_diff and σ̂²_c − σ̂²_b < 3·SE_diff.
- T3 PASS iff T3.1–T3.5 all pass.
- Fig 1a: three curves, closed form lines + simulation points, log-log, R²=0.05 dashed,
  (1/9, 4) shaded. Fig 1b: regime bands vs R² for P = 1 from closed form, boundaries
  H, F, M (M = peak): R² ≤ H never; H < R² < F threshold; F ≤ R² < M window; R² ≥ M always.

## Task 4 — assumption breaks (exploratory; outcomes reported either way)

Definitions used throughout Task 4:
- "bounded window exists" ⇔ the variance curve has an interior maximum that strictly
  exceeds both its Π→0 limit and its Π→∞ limit (so for every R² between max(limits)
  and the peak, the failure set is bounded away from 0 and ∞).
- Also reported: peak Π and height; excess-over-floor set {σ² > F}; R² = 0.05 window
  {σ² > 0.05} (crossings), and the number of disjoint intervals of each set.
- "Moved relative to baseline" = compared with the white-noise Kalman P = 1 baseline
  (peak 0.0929 at 0.687, window (1/9, 4)).

### 4a Discrete-time Kalman (`t4a_discrete.py`)
Δt = 0.05, φ = e^{−λΔt}, q = Σ(1−φ²)/λ, var(v) = 1/Π. Steady-state gain from assumed
model (scalar DARE): A) assumed process noise k·q, k ∈ {1,2,3,10,100}; B) assumed
precision κ·Π, κ ∈ {1,2,3,10,100}. True steady-state posterior error variance of the
fixed-gain filter: V = ((1−K)²q + K²/Π)/(1 − (1−K)²φ²). Π grid: `logspace(-3, 4, 2001)`.
Initial slopes dK/dΠ at 0 computed numerically (K(ε)/ε, ε = 1e-9) and analytically.
Simulation check at Π ∈ {0.1, 1, 10} for all 10 filters: 256 trajectories, 2000 burn-in
steps, 40 000 sampled steps, batch length 400 steps; criterion |sim − exact| <
max(3·SE, 3%).
Prediction: a window appears iff initial slope > 2 × correct slope, i.e. for k, κ ∈
{3, 10, 100} and not for 1; k = κ = 2 is the exact boundary (Prop 4 analogue predicts no
initial rise; second-order terms decide — predicted no window).

### 4b Colored sensory noise (`t4b_colored.py`)
OU sensory noise η with correlation time τ ∈ {0.01, 0.1, 1, 10}, dη = −η/τ dt + b dW,
b = 1/(τ sqrt(Π)) so ∫ autocov = 1/Π; drift term G·η dt replaces G dW_s/sqrt(Π). η is
discretised exactly (AR(1)), started stationary. P = 1, main grid, common settings
(batch length max(10,10τ)). Semi-analytic prediction (derived before running):
σ²_τ = (Σ + G²/(2Π(1 + aτ)))/a. Prediction: rise near 0 persists for all τ (condition
1+λτ < cλ/(2PΣ) = 50); peak lowers and shifts as τ grows; R²=0.05 window shrinks and
disappears for large τ (τ = 1, 10 predicted to lose the 0.05 window).

### 4c Drifting signal (`t4c_drift.py`)
Signal mean η(t) = z* + d(t); the relay's sensory correction pulls toward η(t):
dx = −(λ+G)x dt + G d(t) dt + G dW_s/sqrt(Π) + sqrt(2Σ) dW_sim. Variance measured about z*
(mean of x²). Cases: d = A sin(2πt/T_d), A ∈ {0.05, 0.1}, T_d ∈ {10, 100}; and a slow
random walk d = s·B(t), s = 0.01 per sqrt(time unit), independent per trajectory, B(0)=0.
P = 1, main grid, common settings. Semi-analytic prediction for sinusoids:
σ² + G²A²/(2(a² + ω²)). Prediction: window at R² = 0.05 persists with small shift; the
high-precision plateau rises (H → H + c²A²/(2((λ+c)²+ω²)) ≤ 0.00625), which moves the
R² = 0.008 threshold; random walk adds a precision-increasing term (tracking) and may
make the high-precision end fail at low R².

### 4d Non-Kalman gains (`t4d_gains.py`)
Closed form (2) with G = c·tanh(Π/P), c(1−e^{−Π/P}), cΠ²/(Π²+P²); P ∈ `logspace(-2, 4, 61)`;
Π ∈ `logspace(-8, 8, 40001)`. g0 computed analytically and numerically. Prop 4 check:
rise near 0 (sign of (σ²(ε) − F) at ε = 1e-6·min(P,1)) iff g0 > 2Σ/λ. Prediction:
tanh, exp: rise iff P < 50; Hill: never an initial rise; Hill later excess iff P < 25
(from T1.8); excess set a single interval in all cases.

### 4e Precision-blind gain (`t4e_fixed_gain.py`)
G = G0 ∈ {0.1, 0.5, 1, 2}: closed form monotone decreasing in Π (symbolic derivative
sign and numeric check on `logspace(-4, 4, 2001)`) and diverges as Π → 0. Prediction: no window.

## Task 5 — report
`REPORT.md` generated by `make_report.py` from `results/*.json` only; contains the
prereg commit hash, the results commit hash, the criterion table, Task 4 findings,
figure list, package versions and total runtime. `run_all.sh` reproduces everything.
