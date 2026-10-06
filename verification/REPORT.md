# Verification report — A Bounded Failure Window in a Miscalibrated Precision-Weighted Relay

All numbers below are read from `results/*.json` / `results/runtime.tsv` by `make_report.py`.

- Pre-registration commit: `d21f193f2a50a779e284fc8bc4a1236c67117d05` (PREREG.md unchanged since: **yes**)
- Results commit (scripts + results this report was generated from): `6457bada93cff220a36492dcfd1a19b6631de043` — **working tree differed from this commit when the report was generated**
  (REPORT.md itself is committed in the commit after this one, since a file cannot contain the hash of its own commit.)

## Pre-registered criteria

| ID | criterion | result | measured |
|---|---|---|---|
| T1.1 | OU stationary variance - (2) == 0 | PASS | stat=(G**2/2 + Pi*Sigma)/(Pi*(G + lambda)) |
| T1.1b | lim_{t->inf} of ODE solution with m2(0)=0 equals (2) | PASS | — |
| T1.2 | F = Sigma/lambda and H = Sigma/(lambda+c) | PASS | F=Sigma/lambda, H=Sigma/(c + lambda) |
| T1.3 | numerator = -k(Pi)*(A Pi^2+B Pi+C), A,B,C as stated, k>0 | PASS | k=c, denominator=2*(P + Pi)**2*(P*lambda + Pi*c + Pi*lambda)**2 |
| T1.4 | slope at Pi->0 equals c(c lam - 2PSigma)/(2P^2 lam^2) | PASS | slope0=c*(-2*P*Sigma + c*lambda)/(2*P**2*lambda**2) |
| T1.4b | slope>0 iff P < c lam/(2 Sigma) | PASS | slope/(c lam-2P Sigma)=c/(2*P**2*lambda**2) |
| T1.5 | A,B>0; one positive root iff C<0 iff P<c lam/(2 Sigma); derivative +->- (max) | PASS | positive root=(-4*P**2*Sigma + sqrt(16*P**4*Sigma**2 - P**2*(2*P*Sigma - c*lambda)*(8*P*Sigma + 4*c**2 + 4*c*lambda)))/(4*P*Sigma + 2*c**2 + 2*c*lambda) |
| T1.6 | G* = -lam+sqrt(lam^2+2 Sigma Pi) is stationary min; sigma*^2 = G*/Pi = 2Sigma/(lam+sqrt(..)); d/dPi<0 | PASS | roots=[-lambda + sqrt(2*Pi*Sigma + lambda**2)]; d2sig/dG2 at G*=1/(Pi*sqrt(2*Pi*Sigma + lambda**2)); dsig*/dPi=-2*Sigma**2/((lambda + sqrt(2*Pi*Sigma + lambda**2))**2*sqrt(2*Pi*Sigma + lambda**2)) |
| T1.6b | second derivative at G* positive on numeric grid | PASS | — |
| T1.7 | slope at 0 for G=g0 Pi+O(Pi^2) equals g0^2/(2 lam) - Sigma g0/lam^2 | PASS | slope=(-2*Sigma*g0 + g0**2*lambda)/(2*lambda**2) |
| T1.8 | sigma^2 - F = G(lam G/(2Pi) - Sigma)/(lam(lam+G))  => excess iff G/Pi > 2Sigma/lam | PASS | — |
| T1.9 | worked-example numbers match at stated precision (<=4 s.f.) | PASS | — |
| T2.1 | \|sim-cf\| < max(3SE, 3% cf) at every Pi (raw, vs (2)) | PASS | 43/43 points; max \|sim-cf\|/cf = 0.288%; max \|z\| = 0.66 |
| T2.1c | (info) same test vs EM-corrected D/(2a-a^2 dt) | PASS (info) | 43/43; max \|z\| = 0.43 |
| T2.2 | sim at Pi=1/9 and Pi=4 within 3SE of 0.05 | PASS | Pi=1/9: 0.04994+-0.00029 (z=-0.22); Pi=4: 0.04999+-0.00023 (z=-0.02) |
| T3.1 | (a) maximum strictly inside the grid | PASS | argmax at Pi=0.687 (index 19 of 0..42), sim max=0.09259 |
| T3.2 | (a) crosses R2=0.05 exactly twice, crossings within 15% of 1/9 and 4 | PASS | crossings=['0.1118', '3.9891']; rel. err = ['+0.58%', '-0.27%'] |
| T3.3b | (b) no point exceeds its Pi=0.01 value by > 3 SE_diff | PASS | max (sim_i - sim_0)/SE = -1.95 at Pi=0.01266 |
| T3.4b | (b) no adjacent rise > 3 SE_diff | PASS | max adjacent rise z = -1.95 between Pi=0.01 and 0.01266 |
| T3.3c | (c) no point exceeds its Pi=0.01 value by > 3 SE_diff | PASS | max (sim_i - sim_0)/SE = -1.95 at Pi=0.01266 |
| T3.4c | (c) no adjacent rise > 3 SE_diff | PASS | max adjacent rise z = -1.95 between Pi=0.01 and 0.01266 |
| T3.5a | (c) <= (a) within noise at every Pi (c-a < 3 SE_diff) | PASS | max z(c-a) = -24.28 at Pi=100 (c-a = -1.65e-04) |
| T3.5b | (c) <= (b) within noise at every Pi (c-b < 3 SE_diff) | PASS | max z(c-b) = -0.17 at Pi=0.01 (c-b = -5.25e-12) |

**Task 1: PASS · Task 2: PASS · Task 3: PASS**

### Worked-example numbers (T1.9)

| quantity | computed | stated | digits compared | pass | strict 4 s.f. |
|---|---|---|---|---|---|
| peak sigma^2 | 0.092875272 | 0.0929 | 3 | PASS | differs |
| Pi* (peak location) | 0.68669541 | 0.687 | 3 | PASS | differs |
| R2=0.05 lower crossing | 0.11111111 | 0.111111 | 4 | PASS | agrees |
| R2=0.05 upper crossing | 4 | 4 | 4 | PASS | agrees |
| R2=0.008 threshold | 82.670699 | 82.67 | 4 | PASS | agrees |
| calibrated Pi=0.01 | 0.0099995 | 0.01 | 3 | PASS | agrees |
| calibrated Pi=1 | 0.009950495 | 0.00995 | 3 | PASS | agrees |
| calibrated Pi=100 | 0.0075 | 0.0075 | 2 | PASS | agrees |
| optimal Pi=0.01 | 0.0099995 | 0.01 | 3 | PASS | agrees |
| optimal Pi=1 | 0.0099504938 | 0.00995 | 3 | PASS | agrees |
| optimal Pi=100 | 0.0073205081 | 0.00732 | 3 | PASS | differs |

Expanded numerator of dσ²/dΠ for Appendix A (denominator 2(P+Π)²(Pλ+Πc+Πλ)², see `results/t1_symbolic.txt`):

$$ - 2 P^{3} \Sigma c - 4 P^{2} \Pi \Sigma c + P^{2} c^{2} \lambda - 2 P \Pi^{2} \Sigma c - \Pi^{2} c^{3} - \Pi^{2} c^{2} \lambda $$

### Notes on how the criteria behaved

- **T1.9 is partly ill-posed as written.** "Agreement to 4 significant figures" cannot be checked against values the brief states to 2–3 significant figures. As pre-registered, they were compared at their stated precision; under a strict 4-s.f. reading, 3 values differ only because the stated value is rounded: peak sigma^2 = 0.0928753, Pi* (peak location) = 0.686695, optimal Pi=100 = 0.00732051. The paper could quote these to 4 s.f. as 0.09288, 0.6867, 0.007321.
- **Common random numbers.** Every Π and every relay share the same noise. That makes the paired tests in T3.3–T3.5 sharp, but it also correlates the simulation errors across Π: the T2 z-scores drift smoothly (max |z| = 0.66), so the 43 points of T2.1 are not independent tests.
- **EM bias.** EM bias is far below the SE here. Measured against the EM-exact variance D/(2a − a²dt), max |z| = 0.43; measured against (2), max |z| = 0.66. Both comparisons pass.
- **T3.5b is close to trivial at small Π.** There (b) and (c) have almost the same gain: the paired difference at Π = 0.01 is -5.2e-12, so that test only has power at large Π.

## Task 4 — breaking one assumption at a time

Here "bounded window" means an interior maximum strictly above both ends of the variance curve, as defined in PREREG.md. The baseline is the white-noise Kalman relay with P = 1: peak 0.0929 at Π = 0.687, R² = 0.05 window (1/9, 4).

### 4a Discrete-time Kalman filter

| miscal. | factor | initial gain slope | ÷ correct slope | predicted window | window | peak Π | peak | R²=0.05 window |
|---|---|---|---|---|---|---|---|---|
| A | 1 | 0.01 | 1 | no | no | — | — | none |
| A | 2 | 0.02 | 2 | no | no | — | — | none |
| A | 3 | 0.03 | 3 | yes | yes | 0.718 | 0.01075 | none |
| A | 10 | 0.1 | 10 | yes | yes | 0.784 | 0.02224 | none |
| A | 100 | 1 | 100 | yes | yes | 0.115 | 0.1837 | (0.00461, 7.29) |
| B | 1 | 0.01 | 1 | no | no | — | — | none |
| B | 2 | 0.02 | 2 | no | no | — | — | none |
| B | 3 | 0.03 | 3 | yes | yes | 0.718 | 0.01075 | none |
| B | 10 | 0.1 | 10 | yes | yes | 0.784 | 0.02224 | none |
| B | 100 | 1 | 100 | yes | yes | 0.115 | 0.1837 | (0.00461, 7.29) |

The Prop 4 prediction (a window iff the initial gain slope is more than 2× the correct slope 0.01) holds in all 10 cases. Factor 2 is the exact boundary and gives no window. Miscalibrations A and B give identical filters for equal factors: the steady-state gain depends only on the assumed ratio q/r, so an inflated k·q and an inflated κ·Π are the same error. The two arms are therefore not independent tests. The window survives discretisation but is weaker. With var(v) = 1/Π per sample, factor 3 lifts the peak only to 0.01075 (F = 0.01), and only factor 100 crosses R² = 0.05, on (0.00461, 7.29). Because Π here is a per-sample precision, these locations are not directly comparable with the continuous (1/9, 4). The exact steady-state variances were confirmed by simulation in 30/30 checks (max relative error 0.34%, max |z| 1.74).

### 4b Coloured sensory noise

| τ | peak Π (sim) | peak (sim) | R²=0.05 window (sim) | semi-analytic peak Π | semi-analytic peak | semi-analytic window | max \|z\| sim vs semi |
|---|---|---|---|---|---|---|---|
| 0.01 | 0.687 | 0.09205 | (0.112, 3.92) | 0.684 | 0.09169 | (0.113, 3.9) | 0.85 |
| 0.1 | 0.687 | 0.08255 | (0.129, 3.16) | 0.654 | 0.08234 | (0.13, 3.14) | 0.97 |
| 1 | 0.554 | 0.04342 | none | 0.539 | 0.04326 | none | 0.95 |
| 10 | 0.346 | 0.01368 | none | 0.33 | 0.01356 | none | 0.91 |

Coloured noise at equal zero-frequency power weakens the window but does not remove the bump above F. The simulations match σ²_τ = (Σ + G²/(2Π(1+aτ)))/a, which scales the sensory term by 1/(1+aτ) (max |z| ≤ 0.97). The peak drops from 0.09288 (white noise) to 0.08255 at τ = 0.1 and 0.01368 at τ = 10, and moves to lower Π (0.33 at τ = 10). The R² = 0.05 window narrows to (0.129, 3.16) at τ = 0.1 and disappears for τ ∈ {1, 10}. A bounded window above F remains for every τ. The paper's numbers therefore depend on the white-noise assumption whenever τ is comparable to the relay time constant 1/(λ+G).

### 4c Drifting signal

| case | peak (sim) | R²=0.05 window (sim) | σ² at Π = 100 (sim) | R² = 0.008 crossing (semi, Π ≤ 1e4) | semi σ² at Π = 1e4 | max \|z\| sim vs semi |
|---|---|---|---|---|---|---|
| no drift (closed form) | 0.09288 | (0.111, 4) | 0.007488 | (83.03) | 0.005 (H) | — |
| sin A=0.05, T=10 | 0.09326 | (0.11, 4.05) | 0.007801 | (91.41) | 0.00531 | 1.05 |
| sin A=0.05, T=100 | 0.09326 | (0.11, 4.06) | 0.007827 | (92.37) | 0.005337 | 0.98 |
| sin A=0.1, T=10 | 0.09352 | (0.11, 4.15) | 0.008638 | (133.4) | 0.006163 | 0.98 |
| sin A=0.1, T=100 | 0.09356 | (0.11, 4.15) | 0.008744 | (142) | 0.006274 | 0.98 |
| random walk s=0.01 | 0.09435 | (0.11, 4.38) | 0.01053 | none | 0.008006 | 1.59 |

The window **persists**. Its lower edge is unchanged and its upper edge moves out slightly, to at most 4.38 (random walk). This is because a precision-weighted relay passes the drift with gain G/(λ+G), so the drift adds most at high Π. In one sentence: drift does not replace the low-R² window, but it raises the high-precision floor and so pushes the threshold regime into failure. With the sinusoids the floor stays below 0.008, but the R² = 0.008 threshold moves from 83.03 to 133.4–142 for A = 0.1. With the random walk the floor reaches 0.008006 > 0.008, so R² = 0.008 is never met at high precision: the relay tracks the walk. The random-walk number is not stationary. It grows with the averaging horizon (here t ∈ [20, 220]), so a longer run would make the high-precision failure worse.

### 4d Non-Kalman gains

| gain | Prop 4 holds (P grid) | largest P with initial rise | largest P with any peak | peaks without initial rise | max # excess intervals | max # R²=0.05 intervals |
|---|---|---|---|---|---|---|
| tanh | 61/61 | 39.81 | 39.81 | none | 1 | 1 |
| exp | 61/61 | 39.81 | 39.81 | none | 1 | 1 |
| hill2 | 61/61 | none | 19.95 | 34 values of P, 0.01–20 | 1 | 1 |

Prop 4's small-Π claim holds for every gain and every P tested. For tanh and 1 − e^(−x), rise ⇔ g0 > 2Σ/λ = 0.02 ⇔ P < 50, and a peak appears exactly when the initial rise does. The Hill n = 2 gain never rises at small Π, as Prop 4 predicts (g0 = 0). It still has a **later peak above F** for every tested P up to 19.95, matching the exact condition max_Π G/Π = c/(2P) > 2Σ/λ ⇔ P < 25 (from T1.8: σ² > F ⇔ G/Π > 2Σ/λ). So Prop 4 is a statement about the small-Π behaviour, not a test for the window: sigmoidal gains can open one without any initial rise. In every case the excess set and the R² = 0.05 failure set are a single interval; no multi-interval case was found.

### 4e Precision-blind gain

With constant G = G0, dσ²/dΠ = `-G0**2/(2*Pi**2*(G0 + lambda))`, which is negative. The limit as Π → 0 is oo and the limit as Π → ∞ is Sigma/(G0 + lambda). The numerical grid is monotone decreasing for all G0 ∈ {0.1, 0.5, 1, 2}. There is no window (confirmed): this relay fails at low precision instead of inside a bounded band.

## Figures

- `figures/fig1a_paired.png`: Figure 1a: miscalibrated, calibrated and optimal relays on identical noise
- `figures/fig1b_regimes.png`: Figure 1b: regime bands vs R² for P = 1 (never / threshold / window / always)
- `figures/fig_t2_em.png`: Task 2: EM simulation vs closed form (2), with z-scores
- `figures/fig_t4a_discrete.png`: Task 4a: discrete-time Kalman, true error variance under miscalibration
- `figures/fig_t4b_colored.png`: Task 4b: coloured sensory noise
- `figures/fig_t4c_drift.png`: Task 4c: drifting signal
- `figures/fig_t4d_gains.png`: Task 4d: non-Kalman gains
- `figures/fig_t4e_fixed_gain.png`: Task 4e: precision-blind gain

## Environment and runtime

Reproduce with `bash run_all.sh`. Seeds are fixed, so a rerun gives the same numbers on the same library versions.
