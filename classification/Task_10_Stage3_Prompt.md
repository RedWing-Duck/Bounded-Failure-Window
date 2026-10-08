# Task 10: Stage 3 falsification and completeness (computations, proof checks, figures)

You are testing the predictions in `Stage_3_Plan.md` (attached or in `classification/`). Read it first, together with `Stage_0_1_Classification_Results.md` and `Stage_2_Tau_Sweep_Results.md`. Follow Roadmap v2 Section 13 and the Task 8/9 protocol.

Notation: $\sigma^2(G,\Pi) = (\Sigma + G^2/(2\Pi))/(\lambda + G)$, $F = \Sigma/\lambda$, $G^\star = -\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi}$, $\sigma_\star^2 = G^\star/\Pi$. Class = $(\ell, u, k)$ as in Convention C5.

## Protocol
1. **Pre-register first.** Write `classification/PREREG_t10.md` listing every check below with its exact pass/fail criterion. Commit it before running anything and record the hash.
2. Implement in `classification/t10/`, one script per check, plus `run_t10.sh` and `make_results_t10.py` that builds `RESULTS_t10.md` from `results/*.json`.
3. **Never change a criterion after the pre-registration commit.** Record failures, diagnose them post hoc in separate `*_diag.py` scripts, and say whether the fault is in the plan, the code or the criterion.
4. **Task 9 lessons, mandatory in the pre-registered method:**
   - **Turning points.** Count them as sign changes of the analytic derivative numerator $N$ (Plan A3), evaluated in mpmath at ≥ 50 digits. Use an adaptive log grid followed by bisection or `findroot`. Never use differences of $\sigma^2$: it is flat to $10^{-15}$ near domain ends.
   - **Failure-set components.** Find them by root-finding $\sigma^2 - R^2$ on each monotone piece, never by grid membership.
   - **Regularization limits.** Scale $\varepsilon$ to each parameter set and check convergence before extrapolating. Use mpmath for the smallest $\varepsilon$.
   - **Zero limits.** Use absolute criteria, not relative ones.
5. Use one shared classifier module, `classify.py`, everywhere. It takes a curve given by turning points (positions, values), endpoint limits and approach directions, and returns $(\ell, u, k)$ plus component endpoints. Every class reported below must come from two independent routes:
   - (i) Theorem 1.2 applied to the turning-point sequence;
   - (ii) direct root-finding of $\sigma^2 = R^2$.

   Any disagreement between the two routes is a failure.

## T10.1 Symbolic (SymPy; every item must simplify to exactly 0, no numeric fallback)
- **Elasticity lemma.** $\operatorname{sign}(d\sigma^2/d\Pi) = \operatorname{sign} N$, with $N = \varepsilon(G)(G^2 + 2\lambda G - 2\Sigma\Pi) - G(\lambda + G)$ and $\varepsilon = \Pi G'/G$. Show that $d\sigma^2/d\Pi = G\,N / \big(2\Pi^2(\lambda+G)^2\big)$ for a general differentiable $G(\Pi)$.
- **Bayesian-weight.** $N = 0$ reduces to $G^2 + 2\lambda G + 2\Sigma\Pi_0 - \lambda c = 0$.
- **Misspecified Kalman** ($G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma'\Pi}$, $r = \Sigma/\Sigma'$). $N = 0$ reduces to $(1+r)G^2 + 4r\lambda' G - 2\lambda\lambda' + 4r\lambda'^2 = 0$. Its single positive root exists iff $\Sigma'/\lambda' > 2F$.
- **Capped** $\min(g\Pi, c)$. On the linear branch, $d\sigma^2/d\Pi = g(g\lambda/2 - \Sigma)/(\lambda + g\Pi)^2$.
- **Hill**, $n = 2$, $t = \Pi/\Pi_0$. The sign of $N$ equals the sign of
  $Q(t) = -c(\lambda+c)t^5 - 4\Sigma\Pi_0 t^4 + c(c+2\lambda)t^3 - 8\Sigma\Pi_0 t^2 + 3\lambda c\,t - 4\Sigma\Pi_0$.
  State the exact positive factor relating them.
- **Realizability inverse.** $G_+ = \Pi v + \sqrt{\Pi^2 v^2 - 2\Pi(\Sigma - \lambda v)}$ satisfies $\sigma^2(G_+, \Pi) = v$ and $G_+ \ge G^\star$. Its discriminant equals $\Pi\,(\Pi v^2 + 2\lambda v - 2\Sigma)$, which is $\ge 0 \iff v \ge \sigma_\star^2$.
- **Forced ray.** $\sigma_\star^2(\pi_R) = R^2$ at $\pi_R = 2\lambda(F - R^2)/R^4$.
- **Matched variance** ($\operatorname{Var}\eta = v$, $C_\eta(u) = v e^{-|u|/\tau}$):
  - the differenced Riccati, multiplied by $-\tau R_v$ (state the exact factor you used), gives $A P^2 + 4(\Sigma + \lambda v)P - 4\Sigma v = 0$ with $A = (1-\lambda\tau)^2/\tau$;
  - $A(\tau) = A(1/(\lambda^2\tau))$;
  - at $A = 0$, $P = \Sigma v/(\Sigma + \lambda v)$;
  - the window endpoints satisfy $\tau_-\tau_+ = 1/\lambda^2$;
  - the relay variance $(\Sigma + G^2 v\tau/(1 + a\tau))/a$ follows from the 2×2 Lyapunov equation.

## T10.2 Realizability (Plan A1)
- **Every class.** For $k = 0..5$, every $(\ell, u)$, and $R^2 \in \{0.5F, 0.99F, F, 1.01F, 3F\}$ ($\lambda = 1$, $\Sigma = 0.01$):
  - construct a continuous piecewise-monotone $v \ge \sigma_\star^2$ targeting that class;
  - compute $G = G_+(v, \Pi)$;
  - confirm $G$ is continuous and $\ge 0$;
  - recompute $\sigma^2(G, \Pi)$ and classify.

  **Pass:** every target class with $\ell = 1$ is realized at $R^2 < F$, and every target class is realized at $R^2 \ge F$.
- **Forbidden classes.** For each target with $\ell = 0$ at $R^2 < F$, confirm that any $v$ with $v \le R^2$ on some $(0, \delta)$ violates $v \ge \sigma_\star^2$ (discriminant negative somewhere in $(0, \pi_R)$). **Pass:** 100% of attempts are blocked.
- **Regular smooth multi-window (A1.3).**
  - Take the Bayesian-weight curve with $\kappa = 1.5$ (monotone, $\le F$). Add $k = 1..5$ smooth Gaussian bumps in $\log\Pi$ of height $0.5F$.
  - Invert to $G$. Confirm Paper 1's regularity numerically: $G \to 0$ and $G^2/\Pi \to 0$ at $\Pi = 10^{-12}$, and $G$ converges at $\Pi = 10^{12}$.
  - Confirm $k$ windows at $R^2 = 1.25F$.

  **Pass:** all five cases.

## T10.3 Turning-point census of natural families (Plan A4)
Draw 2,000 random parameter sets per family, log-uniform over four decades per parameter, plus a targeted set near each onset. Count turning points with the T10 method.

- **Bayesian-weight. Pass:**
  - 0 turning points when $\kappa \le 2$;
  - exactly 1 (a maximum) when $\kappa > 2$;
  - position matches the A3 root to relative $10^{-10}$.
- **Misspecified Kalman. Pass:**
  - 0 turning points when $F' \le 2F$;
  - exactly 1 maximum when $F' > 2F$, at the predicted root to relative $10^{-10}$;
  - regression values ($\lambda = 1$, $\Sigma = 0.01$):
    - $(\lambda', \Sigma') = (1, 0.05)$: peak at $\Pi = 19.610$, value $0.01351$;
    - $(0.5, 0.1)$: peak at $\Pi = 7.4380$, value $0.03025$ (4 s.f.).
- **Capped. Pass:**
  - $g < 2F$: strictly decreasing;
  - $g > 2F$: one maximum at $\Pi = c/g$;
  - $g = 2F$ exactly: $\sigma^2 = F$ to 50 digits on $(0, c/g]$, then strictly decreasing.
- **Precision-blind. Pass:** strictly decreasing, $L_- = \infty$.
- **Hill**, $n \in \{1.5, 2, 3, 4, 8\}$.
  - **Prediction:** 0 turning points, or exactly 2 (a minimum, then a maximum).
  - **Pass:** no parameter set has 1, 3 or ≥ 4 turning points.
  - **Regression values** ($n = 2$, $\lambda = c = 1$, $\Sigma = 0.01$):
    - $\Pi_0 = 5$: min at $\Pi = 0.3348$ (value $0.0099852$), max at $6.9817$ ($0.024858$);
    - $\Pi_0 = 26$: min at $10.723$ ($0.0095911$), max at $25.283$ ($0.0098730$).
  - **Also report (not pass/fail):**
    - the pair-birth $\Pi_0^{\text{pair}}(n)$, found by bisection on the turning-point count, for each $n$ at $\lambda = c = 1$, $\Sigma = 0.01$;
    - Paper 1's window onset $\Pi_0 = c\lambda/(4\Sigma) = 25$ for $n = 2$, confirmed as the $\Pi_0$ where $M = F$ (regression, pass/fail at relative $10^{-8}$).
  - **Hill proof support (not pass/fail):**
    - compute the Sturm sequence or discriminant of $Q(t)$ symbolically;
    - attempt to show it never has 4 positive roots for $\lambda, \Sigma, \Pi_0, c > 0$;
    - report what you get, including partial results, e.g. the discriminant locus in the reduced variables $\alpha = \lambda/c$, $\beta = \Sigma\Pi_0/c^2$, which reduce $Q$ to two parameters.
- **Exploratory census (record only):**
  - two-channel Bayesian $c_1\Pi/(\Pi+\Pi_{01}) + c_2\Pi/(\Pi+\Pi_{02})$;
  - two-channel Hill;
  - in both, $\Pi_{02}/\Pi_{01} \in [10, 10^6]$.

  Report the turning-point histogram, and any parameter set with ≥ 2 maxima (multi-window in a semi-natural family).

## T10.4 Mixed class in the Hill family (Plan A4)
On the T10.3 Hill sets with 2 turning points (min $m$, max $M$), predict class $(1, 0, 1)$ for every $R^2 \in (\max(m, H), \min(M, F))$, with $H = \Sigma/(\lambda + c)$. Test 10 tolerances inside the band, both band edges exactly, and $\pm 10^{-6}$ relative.

**Pass:** both classification routes agree with the prediction everywhere. Edge classes must follow Theorem 1.2 equality rules.

Report:
- the band's relative width $(\min(M,F) - \max(m,H))/F$ across sets (median, min, max);
- the fraction of sets where the mixed band exists while $M < F$.

## T10.5 Degeneracies (Plan A5)
- **Equal-height maxima.** Construct, via A1, a curve with two maxima of equal value $M_2$. **Pass:**
  - $k = 2$ just below $M_2$;
  - $k = 0$ at and above $M_2$.
- **Inflection.** Construct a curve with a degenerate non-turning stationary point (a cubic inflection). **Pass:** the class sequence over 1,000 tolerances is identical to that of the same curve with the inflection smoothed away.
- **Plateau.** Capped gain at $g = 2F$. Classify at $R^2 \in \{F(1 - 10^{-6}), F, F(1 + 10^{-6})\}$ and report the classes. The pre-registered prediction under C2′ is:
  - $R^2 < F$: All on the plateau part, merged into a lower-ray-type component that extends past $c/g$ until $\sigma^2 = R^2$;
  - $R^2 = F$: Empty;
  - $R^2 > F$: Empty.

  Pass if both routes agree with this. The direct route must handle plateaus correctly.
- **Pair birth.** For Hill $n = 2$ at $\Pi_0 = \Pi_0^{\text{pair}} \pm 10^{-6}$ relative, report $M - m$. **Pass:** it is $\to 0$ continuously, $O(\sqrt{\text{distance}})$ (fit an exponent in $[0.4, 0.6]$).
- **Narrow windows.** Construct windows of relative width $10^{-8}$ via A1. **Pass:** the root-finding classifier finds 100%, and report what a 10⁴-point log grid finds.

## T10.6 Optimal filter along matched-variance $\tau$ (Plan A6) — highest stakes
Use $\operatorname{Var}\eta = v$ fixed and $\tau \in (0, \infty)$.

- **Three independent routes for $P(\tau)$** on 1,000 random sets ($\lambda, \Sigma, v$ log-uniform over four decades; $\tau$ over $[10^{-4}, 10^4]/\lambda$, including $\lambda\tau = 1$ exactly and $1 \pm 10^{-12}$):
  1. the Plan quadratic, in rationalized form $P = 8\Sigma v/(B + \sqrt{B^2 + 16\Sigma v A})$ with $B = 4(\Sigma + \lambda v)$;
  2. a regularized 2-state ARE ($y = s + \eta + \sqrt\varepsilon\,w$), solved in mpmath by the stable Hamiltonian subspace, with $\varepsilon$ scaled per set and a convergence check down to relative step change $< 10^{-12}$;
  3. a closed-form causal Wiener filter by spectral factorization of $S_y(\omega) = 2\Sigma/(\lambda^2+\omega^2) + 2v\tau/(1 + \tau^2\omega^2)$.

  **Pass:** all three agree to relative $10^{-8}$ on every set.
- **Shape. Pass:**
  - $P$ unimodal, with its unique turning point at $\tau = 1/\lambda$ (relative $10^{-10}$);
  - $P_{\max} = \Sigma v/(\Sigma + \lambda v)$;
  - $P(\tau) = P(1/(\lambda^2\tau))$ to relative $10^{-12}$;
  - $P \to 0$ at both ends (absolute criterion: $P < 10^{-6} P_{\max}$ at $\lambda\tau = 10^{\mp 12}$).
- **Classes. Pass:**
  - window $(\tau_-, \tau_+)$ for $0 < R^2 < P_{\max}$, with $\tau_-\tau_+ = 1/\lambda^2$ (relative $10^{-10}$);
  - Empty for $R^2 \ge P_{\max}$.
- **Relay** (fixed $G$). **Pass:**
  - strictly increasing in $\tau$, from $H_G$ to $(\Sigma + G^2 v/a)/a$;
  - relay $\ge P$ at every sample.
- **Monte Carlo**, at $\lambda = 1$, $\Sigma = 0.01$, $v = 0.05$, $\tau \in \{0.1, 1, 10\}$:
  - simulate the optimal (differenced) filter and the relay at $G = 0.5$;
  - **pass:** within 3 standard errors, with standard error ≤ 2%.
- **Regression values** ($v = 0.05$, $\lambda = 1$, $\Sigma = 0.01$): $P(1) = 0.0083333$, $P(0.3) = 0.0079078$, $P(0.01) = P(100) = 0.0034559$.

## T10.7 Blind search for unpredicted classes
Cover these families:
- along $\Pi$: Bayesian, misspecified Kalman, capped, precision-blind, Hill;
- along $\Pi_0$ and $c$: Bayesian;
- along $\tau$, both normalizations: relay and optimal.

Draw random parameters, and draw tolerances 50% uniform in log over the curve's range and 50% within $10^{-6}$ relative of a critical tolerance. Run $10^6$ classifications in total.

For each (sweep, family), the predicted set of classes is the union listed in the synthesis matrix (Stage 0–1, Stage 2) plus Plan A4/A6. **Pass:** zero classes outside the predicted set, and zero disagreements between the two classification routes. Any flagged case is reproduced at 60 digits before being counted.

## Figures (save PNG + PDF in `classification/t10/figs/`; colourblind-safe; log axes where natural)
1. **F1 Realizability.** $\sigma_\star^2(\Pi)$ envelope (shaded "forbidden" region below it), $F$, and a constructed 3-window curve with its failure set shaded at $R^2 = 1.25F$. Inset: the forced lower ray $(0, \pi_R)$ at $R^2 = 0.9F$.
2. **F2 Hill family.** $\sigma^2(\Pi)$ for $n = 2$, $\Pi_0 \in \{5, 20, 25, 26, 40\}$. Inset zoom near $F$ showing $m$, $M$ and the mixed band.
3. **F3 Hill phase diagram** ($n = 2$, $\lambda = c = 1$, $\Pi_0$ vs $\Sigma$, log–log). Regions: monotone, min–max pair below $F$, window above $F$. Colour by log mixed-band width.
4. **F4 Peak heights.** Peak $M/F$ vs over-weighting ratio for Bayesian-weight ($\kappa$) and misspecified Kalman ($F'/F$) on one axis, $2 < x \le 100$, at $\lambda = c = 1$, $\Sigma = 0.01$ (and $\lambda' = 1$ for misspecified Kalman). Annotate $x = 100$. Report the ratio there; Paper 1's exploratory value was about 2.
5. **F5 Matched-variance $\tau$.** Optimal $P(\tau)$ (hump, window shaded at $R^2 = 0.8P_{\max}$, $\tau = 1/\lambda$ marked) and relay $\sigma^2(\tau)$ at $G = 0.5$; $\lambda = 1$, $\Sigma = 0.01$, $v = 0.05$.

## Report (`RESULTS_t10.md`)
- One row per check: verdict, counts, worst errors, runtime, commit hashes.
- For each failure, a diagnosis section.
- Every wording or formula error found in `Stage_3_Plan.md`.
- The Hill proof-support findings verbatim (polynomials, discriminant factors).
- The exploratory census tables.
- State plainly:
  - whether any prediction in the Plan is falsified;
  - whether any class outside the predicted set was found.
