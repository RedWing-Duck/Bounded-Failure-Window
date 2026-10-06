# Verification report — A Bounded Failure Window in a Miscalibrated Precision-Weighted Relay

All numbers below are read from `results/*.json` / `results/runtime.tsv` by `make_report.py`.

- Pre-registration commit: `d21f193f2a50a779e284fc8bc4a1236c67117d05` (PREREG.md unchanged since: **yes**)
- Results commit (scripts + results this report was generated from): `70ebb55e707d7f600ab4a9ad42e31fa7bfd1dfad`
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

The Prop 4 prediction (a window iff the initial gain slope is more than 2× the correct slope 0.01) holds in all 10 cases. Factor 2 is the exact boundary and gives no window. Miscalibrations A and B give identical filters for equal factors: the steady-state gain depends only on the assumed ratio q/r, so an inflated k·q and an inflated κ·Π are the same error. The two arms are therefore not independent tests. In this parameterisation (var(v) = 1/Π per sample) the excess is small for modest miscalibration: factor 3 lifts the peak only to 0.01075 (F = 0.01), and only factor 100 crosses R² = 0.05, on (0.00461, 7.29). Because Π here is a per-sample precision, these locations are not directly comparable with the continuous (1/9, 4). The exact steady-state variances were confirmed by simulation in 30/30 checks (max relative error 0.34%, max |z| 1.74).

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

The window **persists**. Its lower edge is unchanged and its upper edge moves out slightly, to at most 4.38 (random walk). This is because a precision-weighted relay passes the drift with gain G/(λ+G), so the drift adds most at high Π. In one sentence: drift does not replace the low-R² window, but it raises the high-precision floor and so pushes the threshold regime into failure. With the sinusoids the floor stays below 0.008, but the R² = 0.008 threshold moves from 83.03 to 133.4–142 for A = 0.1. With the random walk the floor reaches 0.008006 > 0.008, so R² = 0.008 is never met anywhere on Π ≤ 1e4: the relay tracks the walk. The margin is small (6e-06) and depends on s. The random-walk number is not stationary. It grows with the averaging horizon (here t ∈ [20, 220]), so a longer run would make the high-precision failure worse.

### 4d Non-Kalman gains

| gain | Prop 4 holds (P grid) | largest P with initial rise | largest P with any peak | peaks without initial rise | max # excess intervals | max # R²=0.05 intervals |
|---|---|---|---|---|---|---|
| tanh | 61/61 | 39.81 | 39.81 | none | 1 | 1 |
| exp | 61/61 | 39.81 | 39.81 | none | 1 | 1 |
| hill2 | 61/61 | none | 19.95 | 34 values of P, 0.01–20 | 1 | 1 |

Prop 4's small-Π claim holds for every gain and every P tested. For tanh and 1 − e^(−x), rise ⇔ g0 > 2Σ/λ = 0.02 ⇔ P < 50, and a peak appears exactly when the initial rise does. The Hill n = 2 gain never rises at small Π, as Prop 4 predicts (g0 = 0). It still has a **later peak above F** for every tested P up to 19.95, matching the exact condition max_Π G/Π = c/(2P) > 2Σ/λ ⇔ P < 25 (from T1.8: σ² > F ⇔ G/Π > 2Σ/λ). So Prop 4 is a statement about the small-Π behaviour, not a test for the window: sigmoidal gains can open one without any initial rise. In every case the excess set and the R² = 0.05 failure set are a single interval; no multi-interval case was found.

### 4e Precision-blind gain

With constant G = G0, dσ²/dΠ = `-G0**2/(2*Pi**2*(G0 + lambda))`, which is negative. The limit as Π → 0 is ∞ and the limit as Π → ∞ is Sigma/(G0 + lambda). The numerical grid is monotone decreasing for all G0 ∈ {0.1, 0.5, 1, 2}. There is no window (confirmed): this relay fails at low precision instead of inside a bounded band.

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

Python 3.13.16, NumPy 2.5.3, SciPy 1.18.1, SymPy 1.14.0, Matplotlib 3.11.2; Linux-6.18.44-fc-v70-x86_64-with-glibc2.39, 4 CPUs.

| script | wall time (s) |
|---|---|
| t1_symbolic | 2.8 |
| t2_em | 43.0 |
| t3_paired | 118.4 |
| t4a_discrete | 13.0 |
| t4b_colored | 157.5 |
| t4c_drift | 227.4 |
| t4d_gains | 5.2 |
| t4e_fixed_gain | 3.2 |
| **total** | **570.5** |

No script went over the 5-minute budget, so trajectory counts were never reduced.
Reproduce with `bash run_all.sh`. Seeds are fixed, so a rerun gives the same numbers on the same library versions.

## Task 6 — coloured-noise symbolic check

Pre-registration: `824ca06236046b97343fb974d8703370d709c5ac` (`PREREG_t6.md` unchanged since: **yes**). Script: `t6_colored_symbolic.py`; full output: `results/t6_colored.txt`.

**Noise normalisation in t4b.** t4b generates a unit OU process eta_u by exact AR(1) discretisation, rho = exp(-dt/tau), innovation sd = sqrt((1/(2tau))(1-rho^2)), started from its stationary law, so eta_u has stationary variance 1/(2tau) and integrated autocovariance 2*tau*(1/(2tau)) = 1, i.e. d eta_u = -eta_u/tau dt + (1/tau) dW_s. The relay multiplies eta_u*dt by gs = G/sqrt(Pi), so the effective sensory noise is eta = eta_u/sqrt(Pi): stationary variance 1/(2 Pi tau), integrated autocovariance 1/Pi, d eta = -eta/tau dt + (1/(tau sqrt(Pi))) dW_s. This MATCHES the expected normalisation.

**Lyapunov solution.** The stationary covariance of (x, η) gives
$$ C_{xx} = \frac{\frac{G^{2}}{2} + G \Pi \Sigma \tau + \Pi \Sigma \lambda \tau + \Pi \Sigma}{\Pi \left(G^{2} \tau + 2 G \lambda \tau + G + \lambda^{2} \tau + \lambda\right)} $$

SymPy's factorisation of C_xx − F (C3), verbatim:
$$ C_{xx} - F = - \frac{G \left(2 G \Pi \Sigma \tau - G \lambda + 2 \Pi \Sigma \lambda \tau + 2 \Pi \Sigma\right)}{2 \Pi \lambda \left(G + \lambda\right) \left(G \tau + \lambda \tau + 1\right)} $$

Small-Π series with the Kalman gain (C4):
$$ C_{xx} = \frac{\Sigma}{\lambda} + \frac{c \left(- 2 P \Sigma \lambda \tau - 2 P \Sigma + c \lambda\right)}{2 P^{2} \lambda^{2} \left(\lambda \tau + 1\right)}\,\Pi + O(\Pi^2) $$

| ID | criterion | result | measured |
|---|---|---|---|
| C1 | C_xx == (Sigma + G^2/(2 Pi (1+a tau)))/a | PASS | simplify(diff)==0: True; numeric 20 sets @50 digits: max rel err 0.00e+00 (ok) |
| C2 | lim_{tau->0} C_xx == (Sigma + G^2/(2Pi))/(lambda+G) | PASS | simplify(diff)==0: True; numeric 20 sets @50 digits: max rel err 0.00e+00 (ok); direct tau=0 substitution matches: True |
| C3 | coloured excess identity; C_xx > F iff G/Pi > 2F(1+a tau) | PASS | C_xx-F == G(lam G/(2Pi(1+a tau)) - Sigma)/(lam a): simplify True, numeric max rel 0.00e+00; bracket*2(1+a tau)/lam == G/Pi - 2F(1+a tau): simplify True, numeric max rel 0.00e+00; multipliers 2(1+a tau)/lam and G/(lam a) proven positive: True |
| C4 | series F + s1 Pi, s1 = c(c lam - 2P Sigma(1+lam tau))/(2P^2 lam^2(1+lam tau)); rise iff c/P > 2F(1+lam tau) | PASS | constant term == F: True; s1 == stated: simplify True, numeric max rel 0.00e+00; sign(s1) == sign(c/P - 2F(1+lam tau)): True |
| C5 | peaks on 200,001-pt grid match t4b semi-analytic peaks to 3 s.f. (height and location) | FAIL | tau=0.01: 0.0917 at 0.683 vs 0.0917 at 0.684; tau=0.1: 0.0823 at 0.655 vs 0.0823 at 0.654; tau=1: 0.0433 at 0.538 vs 0.0433 at 0.539; tau=10: 0.0136 at 0.33 vs 0.0136 at 0.33 |
| C6 | sign of numeric slope at Pi->0 matches 'rise iff tau < 49' (P=1) | PASS | tau=48: slope=2.0408e-04 (s1=2.0408e-04); tau=48.9: slope=2.0040e-05 (s1=2.0040e-05); tau=49.1: slope=-1.9960e-05 (s1=-1.9960e-05); tau=50: slope=-1.9608e-04 (s1=-1.9608e-04) |

**Task 6: FAIL**

### C5 detail: peak height and location

| τ | peak (200,001-pt grid) | t4b peak | match | Π* (200,001-pt grid) | t4b Π* | match | exact Π* (nsolve, post hoc) | formula reproduces t4b on t4b's grid |
|---|---|---|---|---|---|---|---|---|
| 0.01 | 0.091686 | 0.091686 | yes | 0.68303 | 0.68391 | no | 0.683038 | yes |
| 0.1 | 0.082337 | 0.082337 | yes | 0.65476 | 0.65426 | no | 0.654753 | yes |
| 1 | 0.043262 | 0.043262 | yes | 0.53832 | 0.53920 | no | 0.538307 | yes |
| 10 | 0.013556 | 0.013556 | yes | 0.32991 | 0.32980 | yes | 0.329918 | yes |

C5 fails on 3 peak locations (τ = 0.01: 0.683 vs 0.684, τ = 0.1: 0.655 vs 0.654, τ = 1: 0.538 vs 0.539). All peak heights match. This is the risk named in PREREG_t6.md before the run. t4b located its peaks on a grid with steps of about 0.4 % in Π, which is coarser than 3 significant figures. On t4b's own grid the derived C_xx reproduces t4b's peaks exactly (relative error < 1e-12). A post-hoc exact solve of dC_xx/dΠ = 0 agrees with the fine grid. So the derivation agrees with t4b's formula, and the third significant figure of the t4b peak locations is a grid artefact. The correct values to 3 s.f. are 0.683 (τ = 0.01), 0.655 (τ = 0.1), 0.538 (τ = 1), 0.33 (τ = 10). The criterion was left unchanged and is recorded as FAIL.

### C6 detail: boundary τ = 49 at P = 1

| τ | numeric slope at Π → 0 | s1 from series | predicted rise | sign matches |
|---|---|---|---|---|
| 48 | 2.0408e-04 | 2.0408e-04 | yes | yes |
| 48.9 | 2.0040e-05 | 2.0040e-05 | yes | yes |
| 49.1 | -1.9960e-05 | -1.9960e-05 | no | yes |
| 50 | -1.9608e-04 | -1.9608e-04 | no | yes |

Informational: does a peak above F exist for τ > 49 anyway?

| τ | max_Π (C_xx − F) | at Π | sup_Π [G/Π − 2F(1+aτ)] | at Π | limit Π → 0 |
|---|---|---|---|---|---|
| 50 | -1.9798e-08 | 0.0001 | -0.020200 | 0.0001 | -0.020000 |
| 100 | -5.0495e-07 | 0.0001 | -1.020300 | 0.0001 | -1.020000 |
| 1000 | -9.4987e-07 | 0.0001 | -19.022100 | 0.0001 | -19.020000 |

For τ > 49 no grid point lies above F. Each supremum is reached at the smallest grid Π and approaches its negative Π → 0 limit. This is general for the Kalman gain: d/dΠ [G/Π − 2F(1+aτ)] = `c*(-2*P*Sigma*tau - lambda)/(lambda*(P + Pi)**2)`, which is proven negative for all positive parameters. The condition is therefore largest at Π → 0. For the Kalman gain with coloured noise, the small-Π condition c/P > 2F(1+λτ) is both sufficient and necessary for any excess above F. This is unlike the Hill gain in Task 4d.

