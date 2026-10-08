# Stage 3 Plan: Falsification and Completeness

**John Holder** · Plan for Paper 2 · 8 October 2026 · *plan; nothing below is proved yet unless marked*

Companion to Roadmap v2 (Section 7), `Stage_0_1_Classification_Results.md` and `Stage_2_Tau_Sweep_Results.md`. The aim of Stage 3 is to break the classification before a referee does: bound how complex failure sets can get, settle the six adversarial questions, and run a search for classes the analysis does not predict.

Quick numerical checks (float64, 8 October) were run before writing this plan, so that no prediction below is a guess. They are marked **[checked]**. They are leads for Task 10, not results.

---

## 1. What "done" means for Stage 3

1. For the precision sweep, the exact set of classes achievable by *any* continuous gain schedule, at every tolerance.
2. For each natural gain family, a proved bound on the number of turning points of $\sigma^2(\Pi)$, or a labelled numerical result plus conjecture if a proof is out of reach.
3. A written answer, with a label, to each of the six adversarial questions in Roadmap Section 7.
4. A pre-registered search (Task 10) that finds no class outside the predictions, or a recorded counterexample if it does.

---

## 2. Analytic program

### A1. Gain-realizability theorem (precision sweep) — the organizing result

**Claim.** Fix $\lambda, \Sigma$. A function $v: (0,\infty) \to (0,\infty)$ is the stationary-variance curve $\sigma^2(G(\Pi), \Pi)$ of some continuous gain schedule $G \ge 0$ **iff** $v$ is continuous and $v(\Pi) \ge \sigma_\star^2(\Pi)$ for every $\Pi$.

**Why it should hold.** By Lemma 3.1, at each $\Pi$ the map $G \mapsto \sigma^2$ on $[G^\star, \infty)$ is a continuous strictly increasing bijection onto $[\sigma_\star^2, \infty)$. Solving $\sigma^2(G,\Pi) = v$ gives the explicit upper-branch inverse
$$
G_+(v, \Pi) = \Pi v + \sqrt{\Pi^2 v^2 - 2\Pi(\Sigma - \lambda v)},
$$
whose discriminant is $\ge 0$ exactly when $\Pi v^2 + 2\lambda v - 2\Sigma \ge 0$, i.e. $v \ge \sigma_\star^2(\Pi)$. So $G = G_+(v(\Pi), \Pi)$ is continuous and realizes $v$.

**Corollaries to prove.**
- **A1.1 Forced lower ray.** For every continuous gain schedule and every $R^2 < F$, the failure set contains $(0, \pi_R)$ with $\pi_R = 2\lambda(F - R^2)/R^4$. Hence at tolerances tighter than the floor there is never Empty, a pure window, or an upper ray alone. This generalizes Paper 1's "windows need loose tolerances" from the Bayesian-weight gain to **every** gain schedule, with no regularity assumptions.
- **A1.2 Exact class set.** Along the precision sweep, with continuous piecewise-monotone gains:
  - for $R^2 < F$, the achievable classes are exactly those with a lower ray (any $u$, any finite $k$);
  - for $R^2 \ge F$, every class is achievable.
- **A1.3 Unbounded complexity inside the model.** For every $k$ there is a smooth gain schedule satisfying Paper 1's regularity ($G \to 0$, $G^2/\Pi \to 0$ at 0, $G \to G_\infty$ finite) with $k$ windows at some $R^2 > F$. This answers adversarial question 1 inside the filtering model, not just topologically.
- **A1.4 What regularity pins.** Under Paper 1's regularity the endpoint limits are pinned to $F$ and $H$, so $\ell$ and $u$ are fixed by where $R^2$ sits relative to $F$ and $H$, while $k$ stays unbounded.

**Consequence for the thesis.** The model's only constraint on a precision-sweep curve is the optimal envelope $\sigma_\star^2$. All further restrictions (one peak, no mixed class) come from the **shape of the gain family**. That is why the natural-family bounds in A4 carry the thesis content.

**Target label:** Theorem + Corollaries.

### A2. Excess-component lemma

By the excess identity, $\{\sigma^2 > F\} = \{G/\Pi > 2F\}$ exactly. So:
- at $R^2 = F$, the failure set *is* the excess set;
- for $R^2 \ge F$, every failure component lies inside an excess component;
- if $G/\Pi$ is unimodal (Bayesian-weight, Hill, misspecified Kalman), there is at most one excess component, so at most one window at $R^2 = F$.

**Target label:** Lemma (short).

### A3. Elasticity lemma — the counting method

For a strictly increasing gain with inverse $\Pi(G)$ and elasticity $\varepsilon(G) = \Pi G'/G$, turning points of $\sigma^2(\Pi)$ are exactly the sign changes of
$$
N = \varepsilon(G)\,\big(G^2 + 2\lambda G - 2\Sigma\,\Pi(G)\big) - G(\lambda + G).
$$
Each family then reduces to counting positive roots of a polynomial in $G$ (or in $t = \Pi/\Pi_0$).

**Re-derivation check.** For the Bayesian-weight gain, $\varepsilon = 1 - G/c$, and $N = 0$ reduces to $G^2 + 2\lambda G + 2\Sigma\Pi_0 - \lambda c = 0$. This has one positive root iff $\kappa > 2$, which is Paper 1's onset, recovered in three lines.

**Target label:** Lemma.

### A4. Natural-family turning-point bounds

| Family | Prediction | Evidence | Target label |
|---|---|---|---|
| Bayesian-weight $c\Pi/(\Pi+\Pi_0)$ | ≤ 1 turning point (max), iff $\kappa > 2$ | Paper 1; A3 re-derivation | Proposition |
| Misspecified Kalman $-\lambda' + \sqrt{\lambda'^2 + 2\Sigma'\Pi}$ | ≤ 1 (max), iff $F' = \Sigma'/\lambda' > 2F$. Peak at the positive root of $(1+r)G^2 + 4r\lambda' G - 2\lambda\lambda' + 4r\lambda'^2 = 0$, $r = \Sigma/\Sigma'$. $H = 0$. | **[checked]**: predicted peak $\Pi$ 19.610 vs numerical 19.611; 7.4380 vs 7.4378; no peak when $F'/F = 1.5$ | Proposition. Upgrades Paper 1's exploratory finding to a closed form. |
| Capped $\min(g\Pi, c)$ | Linear branch monotone with sign of $g - 2F$; max at the kink iff $g > 2F$; **plateau at exactly $F$** when $g = 2F$ | derivative sign is constant on the linear branch | Proposition |
| Precision-blind $G_0$ | strictly decreasing from $\infty$ to $H$ | trivial | Proposition |
| Hill $c\Pi^n/(\Pi^n + \Pi_0^n)$, $n > 1$ | either no turning point, or exactly a **min then a max**. Gives a **mixed class** (lower ray + window). | **[checked]** $n = 2, 3$, several $\Pi_0$ | Proposition if A3's sextic can be tamed; otherwise Numerical result + Conjecture |
| Two-channel Bayesian / two-channel Hill (sums of two widely separated stages) | unknown | none | exploratory census only |
| Fixed $\alpha$–$\beta$ | out of scope: it is a two-state filter, so it moves to Stage 6 | — | — |

**The Hill result matters most.** Its gain has zero initial slope, so $\sigma^2 < F$ near $\Pi = 0$. The curve dips to a minimum $m$, rises to a maximum $M$, then falls to $H$. The class sequence is $(F, m, M, H)$. For $R^2 \in (\max(m, H), \min(M, F))$ the failure set is a **lower ray plus a window**, i.e. class $(1, 0, 1)$. That answers adversarial question 2 (a mixed class in a natural family): yes.

Three features to pin down in Task 10:
- The mixed band exists even when $M < F$ (no window above the floor). Example: $n = 2$, $\Pi_0 = 26$, $m = 0.009591$, $M = 0.009873 < F$.
- So the min–max pair is born at a larger $\Pi_0$ than Paper 1's window onset $\Pi_0 = c\lambda/(4\Sigma)$. The pair-birth value is to be found.
- The band is narrow (for $n = 2$, $\Pi_0 = 5$: $m = 0.0099852$, about 0.15% below $F$). This is a Stage 5 relevance point.

**Hill sextic (derived; for the proof attempt).** With $t = \Pi/\Pi_0$, the sign of $N$ is the sign of
$$
Q(t) = -c(\lambda + c)t^5 - 4\Sigma\Pi_0 t^4 + c(c + 2\lambda)t^3 - 8\Sigma\Pi_0 t^2 + 3\lambda c\, t - 4\Sigma\Pi_0 .
$$
Descartes allows 4, 2 or 0 positive roots; numerics show 2 or 0. The proof must exclude 4: try a discriminant or Sturm argument, or a substitution exploiting the $\Sigma\Pi_0$ terms ($Q = c\,t\,(\ldots) - 4\Sigma\Pi_0 (1 + t^2)^2$).

### A5. Degeneracies (adversarial questions 3 and 4)

- **Equal-height maxima.** These do not change the class away from the shared value. At $R^2 =$ the shared value, two windows vanish together, so $k$ jumps by 2. Realizable via A1; impossible in families with ≤ 1 maximum. *Target:* Corollary of Theorem 1.2.
- **Degenerate stationary points.** A stationary point that is not a turning point (an inflection) never changes the class. Theorem 1.2(d) says the class depends only on the turning-point values. A flat-topped maximum behaves like a maximum. *Answer to question 4: no.* *Target:* Corollary.
- **Plateaus.** These violate C2. Extend Theorem 1.2 to finitely many constant pieces (C2′): plateau values join the critical tolerances, and at $R^2$ equal to a plateau value the plateau is excluded from the failure set and can split components. A natural instance is the capped gain at $g = 2F$ (plateau at $F$). More generally, by the excess identity a plateau at $F$ occurs exactly where $G = 2F\Pi$ on an interval. *Target:* Proposition (Theorem 1.2′).
- **Pair births.** At the parameter where a min–max pair is born, the new band of tolerances has zero width. So the class is continuous in the parameter except on a measure-zero set of tolerances. Hill's pair-birth $\Pi_0$ is the worked instance. *Target:* Proposition.

### A6. The optimal filter can produce a window (adversarial question 6)

**Sweep.** Correlation time $\tau$ at **matched variance**: $\operatorname{Var}\eta = v$ fixed, as for a sensor of fixed noise level but varying bandwidth. This contrasts with Stage 2's matched zero-frequency power.

**Prediction.** Measurement differencing as in Stage 2 gives the optimal error as the positive root of
$$
A(\tau)P^2 + 4(\Sigma + \lambda v)P - 4\Sigma v = 0,
\qquad
A(\tau) = \frac{(1 - \lambda\tau)^2}{\tau}.
$$
$P$ is decreasing in $A$, and $A$ is minimized (at 0) at $\tau = 1/\lambda$. Hence:
- $P$ is unimodal, with peak $P_{\max} = \Sigma v/(\Sigma + \lambda v)$ at $\tau = 1/\lambda$;
- $P(\tau) = P(1/(\lambda^2\tau))$, i.e. symmetric in $\log\tau$;
- $P \to 0$ at both ends;
- so for every $0 < R^2 < P_{\max}$ the **optimal filter's failure set is a window** $(\tau_-, \tau_+)$ with $\tau_-\tau_+ = 1/\lambda^2$.

**[checked]:** with $v = 0.05$ the regularized Riccati solution matches: $P(1) = 0.0083333 = P_{\max}$, and $P(0.01) = P(100) = 0.0034559$.

**Why this matters.** A Blackwell-ordered family must have monotone optimal error, so this family is not an information ordering. The result therefore does **not** refute the Stage 4 conjecture. It shows the information-ordering hypothesis is **necessary**: without it, optimal filters do produce windows. That turns Stage 4 from "is the conjecture true?" into "is information ordering exactly the right condition?"

Also: the fixed-gain relay along this sweep is increasing, from $H_G$ to $(\Sigma + G^2 v/a)/a$, so its classes are All, upper ray and Empty.

**Target label:** Proposition + Counterexample (analytic) to the unrestricted claim "optimal filters never window".

---

## 3. Computational program (Task 10)

The pre-registered Claude Code run, in `Task_10_Stage3_Prompt.md`, tests every prediction above. Its design carries the Task 9 lessons:
- count turning points by sign changes of the **analytic derivative numerator** $N$ in extended precision, not by differences of $\sigma^2$ (which is flat to $10^{-15}$ near the ends);
- regularization limits use per-set scaled $\varepsilon$ with a convergence check;
- zero limits get absolute criteria.

Its outputs:
- symbolic checks;
- a turning-point census;
- realizability constructions for every class;
- the degeneracy cases;
- three independent routes for A6;
- a $10^6$-classification blind search;
- five figures.

---

## 4. Decision rules (written before the run)

- **Hill shows 4 turning points anywhere:** the Hill conjecture is false. Record it as a counterexample, map the region, and classify the extra classes it creates.
- **A6 fails on an independent route:** re-derive the matched-variance differencing before anything else. A6 is the highest-stakes claim in Stage 3.
- **A blind-search class falls outside the predicted list:** stop, reproduce it in 60-digit arithmetic, then either find the analytic reason (and add it) or record it as a counterexample.
- **Misspecified-Kalman quadratic fails:** fall back to a numerical result, since Paper 1 only claimed it as exploratory.
- **Realizability construction fails:** check the $G_+$ branch formula symbolically first. The theorem is two lines, so a failure is most likely code.

---

## 5. Deliverables after Task 10

1. `Stage_3_Falsification_Results.md`: proofs of A1–A6, each labelled; answers to the six questions; verification section.
2. Synthesis-matrix rows: misspecified Kalman, capped, precision-blind, Hill along $\Pi$; matched-variance $\tau$ for relay and optimal filter; an "arbitrary continuous gain" row from A1.
3. Roadmap updates:
   - Stage 4 reframed (information ordering is necessary);
   - $\alpha$–$\beta$ moved to Stage 6;
   - "windows need loose tolerances" upgraded to all gain schedules.

---

## 6. Answers expected to the six adversarial questions

| # | Question | Expected answer | Source |
|---|---|---|---|
| 1 | Three or more separated windows from a continuous gain? | Yes, any $k$, even smooth and Paper-1-regular | A1.3 |
| 2 | Mixed class in a natural family? | Yes: Hill gain, lower ray + window | A4 |
| 3 | Equal-height extrema change the class? | Only at that one tolerance ($k$ jumps by 2) | A5 |
| 4 | Degenerate stationary point changes the class without changing extrema? | No | A5, Thm 1.2(d) |
| 5 | Numerical search finds an unpredicted class? | Expected no; Task 10 decides | Task 10 |
| 6 | Optimal filter non-monotone along a non-information sweep? | Yes: matched-variance $\tau$, window for the optimal filter | A6 |
