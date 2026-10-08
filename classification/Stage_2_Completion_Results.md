# Stage 2 Completion: Sampling Interval and Process-Noise Sweeps

**John Holder** · Working results for Paper 2 · 8 October 2026 · verified by Task 12, except Proposition 2.6(b), which is new (see Section 5)

Companion to Roadmap v2 (Section 6.2) and the Stage 0–1, 2, 3 and 4 results.

Notation:
- $F = \Sigma/\lambda$;
- $\sigma^2(G,\Pi) = (\Sigma + G^2/(2\Pi))/(\lambda + G)$;
- $\sigma_\star^2 = 2\Sigma/(\lambda + \sqrt{\lambda^2 + 2\Sigma\Pi})$;
- $u = 2\Sigma\Pi/\lambda^2$;
- classes $(\ell, u, k)$ as in C5. (The class letter $u$ and the variable $u$ are distinguished by context.)

Every result carries a Section 12 label.

**Summary.**
1. **Sampling interval $\Delta t$.** Paper 1's discrete excess condition decides the excess set for all three error metrics at once (Lemma 2.1).
2. **The optimal filter's error moves in opposite directions along $\Delta t$.**
   - Error at sample times falls (proved).
   - Error just before samples rises (proved here, new).
   - Time-averaged error rises (numerical result).
   - So the $\Delta t$ sweep is not an information ordering, consistent with Stage 4.
3. **Natural sampled relays give new classes.** Along $\Delta t$ they produce two rays, upper ray + window $(0,1,1)$, and lower ray + window $(1,0,1)$. These are the first sweeps where natural gains give an upper ray with a window.
4. **Process noise $\Sigma$ (moving floor).** Everything is proved.
   - With a relative tolerance ($\sigma^2 > rF$), the $\Sigma$ sweep is the precision sweep in disguise (scaling lemma).
   - A $\Sigma$-tracking Kalman gain that over-trusts precision by $\rho$ has a window **iff $\rho > 2$**: Paper 1's factor of two again.
   - With an absolute tolerance, every family is monotone.
5. **Two of my predictions were wrong and are corrected here.**
   - The discrete over-trust onset at fixed precision is $\rho > 2 + u$, not $\rho > 2$.
   - My quick-check numbers for the sampled relay were wrong. The picture they described was right.

---

## Part A — the sampling-interval sweep $\Delta t \in (0, \infty)$

### A.1 Model and metrics

**M-P (Paper 1's discrete model, point-sampled, matched floor).**
- State: $x_{k+1} = a x_k + w_k$, with $a = e^{-\lambda\Delta t}$ and $\operatorname{Var} w = q = F(1 - a^2)$.
- Observation: $z_k = x_k + v_k$, with $\operatorname{Var} v = r = 1/(\Pi\Delta t)$.

Write $s = 1 - a^2 = 1 - e^{-2\lambda\Delta t}$ and $\varphi = F\Pi\Delta t$.

**Metrics.** Let $P^+$ be the posterior error at sample times.
- prior: $P^- = a^2P^+ + q$;
- time-averaged: $\bar P = F - (F - P^+)\,s/(2\lambda\Delta t)$.

**Filters.**
- Optimal: steady-state Kalman.
- D1, sampled continuous relay: $L = 1 - e^{-G\Delta t}$.
- D2, discrete Bayesian weight: $L = c\Pi\Delta t/(\Pi\Delta t + \Pi_0)$.
- D3, discrete Kalman over-trusting precision by $\rho$.

For a fixed gain:
$$
P^+ = \frac{(1-L)^2 q + L^2 r}{1 - (1-L)^2a^2}.
$$

### A.2 Excess sets

**Lemma 2.1 (shared excess set).** For any filter on M-P,
$$
P^- - F = a^2(P^+ - F),
\qquad
\bar P - F = (P^+ - F)\,\frac{s}{2\lambda\Delta t}.
$$
Hence all three metrics exceed $F$ on the same set, namely $\{L/(2-L) > \varphi\}$ (Paper 1, Proposition 6).

**Label:** Lemma (proved; Task 12, symbolic).

**Proposition 2.2 (D1: tanh lemma).** $L/(2-L) = \tanh(G\Delta t/2)$. So the excess set is $\{G\,h(G\Delta t) > F\Pi\}$ with
$$
h(x) = \frac{\tanh(x/2)}{x},
$$
which is strictly decreasing from $1/2$.

Consequently:
- the excess set is a lower ray $(0, \Delta t_E)$ iff $G > 2F\Pi$, which is exactly the continuous-time condition;
- otherwise it is empty;
- $\Delta t_E$ solves $\tanh(G\Delta t/2) = F\Pi\Delta t$.

**Label:** Proposition (proved: $h' < 0$ because $\sinh x > x$; Task 12, 1000/1000 sets, $\Delta t_E$ to $10^{-30}$).

Reading: sampling never creates excess that continuous time lacks, and longer intervals always remove it.

**Proposition 2.3 (D2).** The excess set is the lower ray $\Delta t < \Delta t_E$, where
$$
\Delta t_E = \frac{c - 2F\Pi_0}{(2-c)\,F\,\Pi},
$$
iff $\kappa = c/(F\Pi_0) > 2$ (Paper 1's onset). Otherwise it is empty.

**Label:** Proposition (proved; 1000/1000).

**Proposition 2.4 (D3, corrected).** The excess set is
$$
\{\varphi < 1\ \text{ and }\ s(1-\varphi)\big(\rho(1+\varphi) - 2\big) > 4\varphi\}.
$$
Its small-$\Delta t$ limit gives the onset
$$
\text{excess near } \Delta t = 0 \iff \rho > 2 + u.
$$
This is the continuous excess condition $G > 2F\Pi$ for the over-trusting Kalman gain $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$:
$$
\sqrt{1 + \rho u} > 1 + u \iff \rho > 2 + u.
$$
Census shape: lower ray or Empty.

**Label:** Proposition (proved; 1000/1000 sets, 0 disagreements in 201,514 membership tests).

**Correction.** I conjectured the onset was $\rho > 2$. That is the condition for excess to occur at *some* precision (Section B.3). At a *fixed* precision the threshold is $2 + u$. My conjecture was false in 178 of 1,000 sets.

### A.3 Endpoint limits

| Filter | $\Delta t \to 0$ (all metrics) | $\Delta t \to \infty$ |
|---|---|---|
| Optimal | $\sigma_\star^2$ | post → 0; prior, avg → $F$ |
| D1 | $\sigma^2(G, \Pi)$ | post → 0; prior → $F$ (below); avg → $F$ (below, like $-F/(2\lambda\Delta t)$) |
| D2 | $\sigma^2(c\Pi/\Pi_0, \Pi)$ | post → $(1-c)^2F$; prior, avg → $F$ |

For D1, the prior approaches $F$ through $a^2(P^+ - F)$, so its gap from $F$ shrinks like $e^{-2\lambda\Delta t}$.

**Label:** Proposition (proved; Task 12, symbolic and series). For D2 post, the coefficient of the $O(1/\Delta t)$ correction was confirmed by a series route after SymPy's `limit` failed (Section 5).

### A.4 The optimal filter along $\Delta t$

**Proposition 2.6.**
- **(a)** $P^+$ is strictly decreasing, from $\sigma_\star^2$ to $0$.
- **(b)** $P^-$ is strictly increasing, from $\sigma_\star^2$ to $F$.

*Proof of (a).* (Task 12.) $P^+ = F/(1+\mu)$, where $\mu$ is strictly increasing in $\varphi$ and in $\varphi/s$. Both of those increase in $\Delta t$, since $e^y > 1 + y$. $\square$

*Proof of (b) (new).* Write $x = \lambda\Delta t$, so $s = 1 - e^{-2x}$, $q = sF$, and $r = \lambda/(\Pi x)$. The prior error $M = P^-$ is the positive root of
$$
f(M) = M^2 + s(r - F)M - sFr = 0.
$$
- $f'(M) > 0$ at the positive root, because the product of the roots is negative.
- Implicit differentiation, with $r' = -r/x$, gives
$$
\operatorname{sign}\frac{dM}{dx} = \operatorname{sign}\Big[FMs' - (F - M)\,r\,\big(\tfrac{s}{x} - s'\big)\Big].
$$
- From $f = 0$: $sr(F - M) = M(M - sF)$. So the bracket equals
$$
M\Big[Fs' - \frac{(M - sF)(s/x - s')}{s}\Big].
$$
- Now use three facts:
  - $sF = q < M < F$, because the prior lies between the process noise and the floor;
  - $s/x > s'$, because $s$ is concave with $s(0) = 0$;
  - hence $0 < M - sF < F(1 - s)$.
- So it suffices that $s s' \ge (1-s)(s/x - s')$, i.e. $s' \ge (1-s)s/x$. With $s' = 2e^{-2x}$ and $1 - s = e^{-2x}$, this reads
$$
2x \ge 1 - e^{-2x},
$$
which is true. $\square$

**Label:** (a) Proposition (proved; Task 12). (b) Proposition (proved here; checked numerically in 80-digit arithmetic: 3,000 random sets, 0 sign violations, every link of the chain holds; awaiting Task 13).

**Numerical result 2.6c.** $\bar P$ is strictly increasing from $\sigma_\star^2$ to $F$.
- Task 12: 400,000 points, 0 violations.
- The avenue tried so far writes $\bar P = F - (F - M)(e^{2x} - 1)/(2x)$. That is a decreasing factor times an increasing one, so it does not settle the sign.

**Optimal classes.**
- post: lower ray or Empty.
- prior and avg: All ($R^2 < \sigma_\star^2$), upper ray, or Empty ($R^2 \ge F$).

**Stage 4 cross-check (Proposition 2.7).** M-P is not a causal-garbling family along $\Delta t$ in either direction. By Theorem 4.2, an ordering would move all metrics the same way, but post falls while prior and avg rise.

Reading: each sample carries the signal with noise variance $1/(\Pi\Delta t)$, so longer intervals make every sample more precise. But samples get sparser, so error grows more between them.

**Label:** Proposition (proved; Task 12, all pairs $(\Delta t, 2\Delta t)$ checked).

**Numerical result 2.8 (integrate-and-dump M-I).** Both of Task 11's metrics are non-decreasing on the continuum. This is Stage 4 Numerical result 4.10a.
- Task 12: 400,000 points, 0 violations, and the values match Task 11 to $10^{-16}$.
- The SymPy sign attempt is unresolved.

### A.5 Sampled relays: classes

**Proposition 2.9 (two rays from an over-weighted sampled relay).** Let D1 have $G > 2F\Pi$. Then prior and avg:
- start at $\sigma^2(G,\Pi) > F$;
- end at $F$, approached from below;
- so each has an interior minimum below $F$.

For $R^2$ between that minimum and $F$, the failure set contains a lower ray and an upper ray: two rays, or $(1,1,k)$ if there are several minima.

**Label:** Proposition (proved: continuity plus A.3).

**How deep the dips are** (this matters for Stage 5).
- **avg:** the dip is modest, because $\bar P - F \sim -F/(2\lambda\Delta t)$. At $G = 0.5$, $\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$: minimum $0.0099875$ at $\Delta t \approx 200$, a dip of 0.125%.
- **prior:** the dip is invisibly small, because the prior's gap from $F$ is multiplied by $e^{-2\lambda\Delta t}$. Task 12 measured relative dips between $10^{-17}$ and $10^{-32{,}880{,}317}$.

So the prior's two rays exist mathematically but are practically irrelevant. The avg two rays are real but narrow.

**Worked example** (D1, $G = 0.5$, $\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$; Task 12 values):
- **post:** rises from $0.09$ to a single maximum $0.20457$ at $\Delta t = 2.4645$, then falls to 0. This gives a **window** for $R^2 \in (0.09, 0.20457)$.
- **avg:** crosses $F$ at $\Delta t_E = 100$ (to 20 digits, since $\tanh 25 \approx 1$), then dips to $0.0099875$ and returns to $F$ from below.

(My earlier quick check gave $0.166$ near $\Delta t = 1$. That is $P^+(1)$, not the maximum.)

**Numerical result 2.10 (census of sampled relays).** 2,000 sets per family; every class found agreed by both routes.

| Family | Metric | Turning-point shapes | Classes found |
|---|---|---|---|
| D1 | post | none, max | Empty, lower ray, window |
| D1 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D1 | avg | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D2 | post | none, max, min, min–max | All, Empty, lower ray, upper ray, two rays, window, $(1,0,1)$ |
| D2 | prior, avg | none, min | All, Empty, lower ray, upper ray, two rays |
| D3 | post | none, max | Empty, lower ray, window |
| D3 | prior | none, min, max–min | All, Empty, lower ray, upper ray, two rays, $(0,1,1)$ |
| D3 | avg | none, min | All, Empty, lower ray, upper ray, two rays |

Every family has at most two turning points.

**Label:** Numerical result (Task 12; no turning-point count is proved for D1–D3).

**Conjecture 2.11.** Along $\Delta t$, D1–D3 have at most two turning points in every metric.

**New classes from natural gains.**
- **Upper ray + window, $(0,1,1)$.** A max–min shape in prior or avg. It comes from a hump before the slow return to $F$.
- **Lower ray + window, $(1,0,1)$.** A min–max shape in D2 post, analogous to the Hill gain along $\Pi$.

---

## Part B — the process-noise sweep $\Sigma \in (0, \infty)$, moving floor

Fix $\lambda$ and $\Pi$. There are two tolerance conventions:
- **absolute:** fixed $R^2$;
- **relative:** failure means $\sigma^2 > rF$.

**Lemma 2.12 (scaling).** With $g = G/\lambda$,
$$
\frac{\sigma^2}{F} = \frac{1 + g^2/u}{1+g}.
$$
For a gain that depends on $(\Sigma, \Pi)$ only through $u$, the relative-tolerance $\Sigma$ sweep and the precision sweep classify identically in $u$.

**Label:** Lemma (proved; Task 12).

**Proposition 2.13 ($\Sigma$-independent gain).**
- **Absolute:** $\sigma^2$ is affine and increasing. Classes: All, upper ray.
- **Relative:** $\sigma^2/F$ decreases from $\infty$ to $1/(1+g)$. Classes: All, lower ray.
- Excess set: $\Sigma < \lambda G/(2\Pi)$.

**Label:** Proposition (proved).

**Proposition 2.14 ($\Sigma$-tracking Kalman, over-trust $\rho$).** Let $G = -\lambda + \sqrt{\lambda^2 + 2\rho\Sigma\Pi}$ and $w = \sqrt{1 + \rho u}$.
- **Absolute:** strictly increasing. Class: upper ray.
- **Relative:**
$$
\frac{\sigma^2}{F} = \frac{(1+\rho)w + (1-\rho)}{w(w+1)}.
$$
  This starts at 1 and tends to 0. It has a single maximum, at
$$
w_M = \frac{(\rho - 1) + \sqrt{2\rho(\rho-1)}}{1+\rho},
$$
  **iff $\rho > 2$**. Otherwise it is strictly decreasing.
  - $\rho > 2$: lower ray ($r \le 1$), window ($1 < r <$ peak), Empty.
  - $\rho \le 2$: lower ray or Empty.

*Proof.* The derivative's numerator is a downward parabola in $w$, with value $2(\rho - 2)$ at $w = 1$ and vertex at $(\rho-1)/(1+\rho) < 1$. $\square$

**Label:** Proposition (proved; 2,000 sets, maximum position to $6\times10^{-31}$).

**Proposition 2.15 ($\Sigma$-tracking Kalman, misspecified $\lambda'$).** Let $G = -\lambda' + \sqrt{\lambda'^2 + 2\Sigma\Pi}$.
- **Absolute:** increasing. Class: upper ray.
- **Relative:** a single maximum iff $\lambda' < \lambda/2$. Classes: lower ray, window, Empty; or lower ray, Empty.

*Proof.* The numerator is $-G^2 - 2\lambda' G + \lambda'(\lambda - 2\lambda')$, a downward parabola with vertex at $G < 0$. $\square$

**Label:** Proposition (proved; 2,000 sets).

**Proposition 2.16 (optimal).**
- **Absolute:** increasing. Class: upper ray.
- **Relative:** $2/(1 + \sqrt{1+u})$ is decreasing. Classes: lower ray, Empty.

**Label:** Proposition (proved).

**Reading.** On a moving floor, the tolerance convention decides the topology.
- With absolute tolerances, every family is monotone: more process noise is simply worse.
- With relative tolerances, windows return under the same factor-of-two over-confidence condition as Paper 1: $\rho > 2$, or $\lambda' < \lambda/2$, which is $F'/F > 2$.

The relative-tolerance optimal filter never windows, so Stage 4's diagnostic reading carries over.

---

## 5. Verification (Task 12)

Pre-registration `PREREG_t12.md` (commit `6e09e88`); results at commit `82edc1b`; 8,935 s on 4 CPUs. **Eleven checks pass and three fail**: one on SymPy's route, one on a pre-registered tolerance, and one on my wrong quick-check numbers. All three stay recorded as failures.

| Check | Verdict | Note |
|---|---|---|
| Symbolic (A1–A6, B1–B5) | **FAIL** | 66/67. SymPy's `limit` returned 0 for the D2 post $O(1/\Delta t)$ coefficient. A series route and 100-digit numerics confirm the pre-registered value. **Code route.** |
| A2, A3, A4 excess sets | PASS | 1000/1000 each |
| A6 regression | PASS | 6/6 |
| A7 two rays | **FAIL** | The prior minimum went undetected in 538 sets: the dip lies below the $10^{-40}$ zero tolerance. Scanning the sign of the derivative's factor finds it in 590/590. **Criterion.** The proved claim stands. |
| A8 census | PASS | 0 route disagreements |
| A8 qualitative regression | **FAIL** | My quick-check numbers were wrong (Section A.5). **Prediction**, qualitative picture right. |
| A9, A10 | PASS | |
| Part B census | PASS | 8 × 2,000 sets |
| Part C blind search | PASS | 4.4 million classifications; 1,109 float flags, 0 persisting at 60 digits |

**Predictions falsified.** Both were disclosed in the pre-registration before the run:
1. the D3 onset (corrected to $\rho > 2 + u$, Proposition 2.4);
2. the quick-check numbers.

No class outside the predicted and census sets appeared.

**Not yet verified.** Proposition 2.6(b), the new proof that the prior error increases. The Task 13 items at the end check it.

---

## 6. Synthesis-matrix rows (Stage 2 completion)

| Sweep | Kind | Filter | Metric / convention | Possible classes | Label |
|---|---|---|---|---|---|
| $\Delta t$ (M-P) | either | optimal | post | lower ray, Empty | Prop. 2.6(a) |
| $\Delta t$ (M-P) | either | optimal | prior | All, upper ray, Empty | Prop. 2.6(b) |
| $\Delta t$ (M-P) | either | optimal | avg | All, upper ray, Empty | Num. 2.6c |
| $\Delta t$ (M-I) | either | optimal | (a), (b) | All, upper ray, Empty | Num. 2.8 |
| $\Delta t$ (M-P) | either | D1 sampled relay | post | Empty, lower ray, window | Prop. 2.2 (excess); Num. 2.10 |
| $\Delta t$ (M-P) | either | D1 | prior, avg | All, Empty, lower/upper ray, two rays, $(0,1,1)$ | Prop. 2.9; Num. 2.10 |
| $\Delta t$ (M-P) | either | D2 discrete Bayesian | post | adds $(1,0,1)$ and window to the above | Prop. 2.3; Num. 2.10 |
| $\Delta t$ (M-P) | either | D2 | prior, avg | All, Empty, lower/upper ray, two rays | Prop. 2.3; Num. 2.10 |
| $\Delta t$ (M-P) | either | D3 over-trust | post | Empty, lower ray, window | Prop. 2.4; Num. 2.10 |
| $\Delta t$ (M-P) | either | D3 | prior | as D1 prior | Prop. 2.4; Num. 2.10 |
| $\Delta t$ (M-P) | either | D3 | avg | All, Empty, lower/upper ray, two rays | Prop. 2.4; Num. 2.10 |
| $\Sigma$ | env. | $\Sigma$-independent gain | absolute / relative | All, upper ray / All, lower ray | Prop. 2.13 |
| $\Sigma$ | env. | $\Sigma$-tracking, over-trust $\rho$ | absolute / relative | upper ray / lower ray, window ($\rho > 2$), Empty | Prop. 2.14 |
| $\Sigma$ | env. | $\Sigma$-tracking, $\lambda'$ | absolute / relative | upper ray / lower ray, window ($\lambda' < \lambda/2$), Empty | Prop. 2.15 |
| $\Sigma$ | env. | optimal | absolute / relative | upper ray / lower ray, Empty | Prop. 2.16 |

**Stage 2 status: complete.** Every sweep in Roadmap Section 6.2 is classified. The following remain open, each under its label:
- Numerical result 2.6c (optimal avg monotone);
- Numerical result 2.8 / 4.10a (integrate-and-dump);
- Conjecture 2.11 (at most two turning points for sampled relays).

---

## Task 13 items (short verification of Proposition 2.6(b))

Run this under the usual protocol: pre-register, commit, never change criteria.

1. **SymPy.** Verify each step symbolically:
   - the implicit derivative;
   - the identity $sr(F-M) = M(M - sF)$;
   - the rewritten bracket;
   - the final inequality $2x \ge 1 - e^{-2x}$.
   
   Allow factor-then-simplify.
2. **mpmath, 100 digits.** On 10,000 random sets with $\lambda\Delta t \in [10^{-8}, 50]$, check $dM/dx > 0$ and each link of the chain ($sF < M < F$; $s/x > s'$; final inequality). Pass: 0 failures.
3. **Optional attempt on Numerical result 2.6c.** Write $\bar P$ in terms of $M$, and try the same implicit-derivative route with bounds from $f(M) = 0$. Report proved, disproved or unresolved.
