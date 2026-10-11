# Roadmap v3: Classifying Failure-Set Topology in Stationary Linear Filters

**Author:** John Holder · **Status:** Stages 0–4 complete (Paper 2 / minimal thesis); Stages 5–6 planned · Revised
October 2026 (Task 13); result numbers rendered from `register/results.yaml` (thesis numbering, Task 14)

Roadmap v2 set out a formally specified classification program in seven stages. Stages 0–4 are now complete for scalar
models and are consolidated in `Stages_0_4_Thesis.md` (the "consolidated document" below, cited by section and
thesis result number; source `source/Stages_0_4_Source.md`, consolidated v1 frozen in `archive/Stages_0_4_Consolidated_v1.md`). This version records what was done, lists what remains open, replaces the Section 14 matrix with the
final one, and restates Stages 5–6 in light of the results. Notation, terminology and the verification protocol of v2
(Sections 1, 2, 12, 13) are unchanged; the consolidated document's Section 1 restates them.

---

## 1. Status of Stages 0–4

| Stage | Roadmap v2 question | Status | Where |
|---|---|---|---|
| 0 | Define the classification problem | **Complete.** Conventions C1–C6, C2′; class $(\ell, u, k)$ | Consolidated §1 |
| 1 | General classification theorem | **Complete.** Theorem 2.2 (critical tolerances), Theorem 2.4 (plateaus), Proposition 2.1 (topology excludes nothing) | §2 |
| 2 | Model classification: $\Pi$, $\Pi_0$, $c$, $\tau$, $\Delta t$, $\Sigma$ | **Complete.** Every scalar sweep of v2 Section 6.2 classified | §3 ($\Pi$), §4 ($\Pi_0$, $c$), §5 ($\tau$, both normalizations, power family), §6 ($\Delta t$), §7 ($\Sigma$) |
| 3 | Falsification and completeness | **Complete.** Realizability, forced lower ray, unbounded windows, natural families (Hill for every $n > 1$), degeneracies, blind searches | §8 |
| 4 | The optimality theorem | **Complete.** Theorem 7.2 (causal garbling ⇒ monotone), Theorem 7.8 (exact sharpness in the power family), Theorem 7.6 (non-linear garblings add nothing for additive Gaussian noise), Counterexample 7.12 (causality essential) | §9 |

Verification: Tasks 8–13 (`REPORT.md`, `t9/`…`t13/RESULTS_t*.md`), all pre-registered; every failed check is recorded with
its diagnosis. Task 13 verified or closed seven of the eight items left open by Stages 2–4 (consolidated §12–13); one remains a conjecture.

**Answers to the v2 sub-questions.**
1. *Possible topologies in principle:* all (Proposition 2.1).
2. *What determines the topology:* endpoint limits, approach directions and ordered extremum values (Theorem 2.2).
3. *Which sweeps and gain families give each topology:* the synthesis matrix below.
4. *Completeness and complexity:* complete for every family in the matrix except the two-stage gains; arbitrarily many
   windows are possible for constructed regular gains (Corollary 5.4); natural families have at most two turning points
   along precision (Theorem 5.12).
5. *Impossible for optimal filters:* along any causally ordered sweep, everything except Empty, All and a single ray at the
   less-informative end (Corollaries 7.3–7.4); along non-ordered sweeps the optimal filter can window (Counterexample 6.11,
   Theorem 7.8, Proposition 7.11).

---

## 2. Open problems (all items still open after Task 13)

1. **Turning points of sampled relays** (Conjecture 6.22): at most two turning points along $\Delta t$ for D1–D3 in every
   metric. Evidence: 6,000 sets × 3 metrics (Task 12) and 9,000 new curves (Task 13 audit), never more than two. Best
   partial result: proved limits and a single excess component.
2. **Two-stage gains** (Numerical result 5.15): a turning-point bound for sums of natural stages (at most 3 and 4 seen).
3. **A necessary condition for monotone optimal error** beyond the power family (Theorem 7.8 is sharp there; Proposition 7.13
   shows ordering is not necessary in general).
4. **The α–β filter and multivariate models** (Stage 6).

Closed by Task 13 (now theorems in the consolidated document): optimal M-P prior and time average increasing (Theorem 6.19),
integrate-and-dump monotone on the continuum (Theorem 7.15), power-family unimodality (Theorem 7.9), Hill gain for every
$n > 1$ (Theorem 5.12), strict gap between the optimal filter and the best constant gain along $\tau$ (Proposition 6.9), and
non-linear causal garblings (Theorem 7.6).

---

## 3. Final synthesis matrix (replaces v2 Section 14)

"#" is the row number of the Task 13 class audit (C2); "Opt." is what the optimal filter can produce along the same sweep. Classes
are written E (Empty), A (All), LR (lower ray), UR (upper ray), 2R (two rays), W (window), and triples $(\ell, u, k)$.

| # | Sweep | Kind | Gain family / filter | Endpoint limits (approach) | Extrema | Critical tolerances | Possible classes | Opt. | Conditions | Label | Verified by |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | $\Pi$ | env. | optimal | $F$ (below) → $0$ | none | $F$ | LR, E | LR, E | — | Thm 3.4 | the starting study (Tasks 1–7); T13 C2 |
| 2 | $\Pi$ | env. | Bayesian-weight | $F$ → $H$ (above) | one max iff $\kappa > 2$ | $H, F, M$ | A, LR, W, E | LR, E | $\kappa > 2$ for W | Prop. 5.8 | the starting study (Tasks 1–7); T10.3, T10.7; T13 C2 |
| 3 | $\Pi$ | env. | misspecified Kalman | $F$ → $0$ | one max iff $F' > 2F$ | $F, M$ | LR, W, E | LR, E | $F' > 2F$ | Prop. 5.9 | T10.3, T10.7; T13 C2 |
| 4 | $\Pi$ | env. | capped $\min(g\Pi, c)$ | $F$ → $H$ (above) | one max (kink) iff $g > 2F$; plateau at $g = 2F$ | $H, F, M$ | A, LR, W, E | LR, E | $g > 2F$ | Prop. 5.10 | T10.3, T10.5, T10.7; T13 C2 |
| 5 | $\Pi$ | env. | precision-blind | $\infty$ → $H$ (above) | none | $H$ | A, LR | LR, E | — | Prop. 5.11 | T10.3, T10.7; T13 C2 |
| 6 | $\Pi$ | env. | Hill $n = 2$ | $F$ (below) → $H$ (above) | 0, or min then max | $H, m, M, F$ | A, LR, (1,0,1), W, E | LR, E | pair iff $\Pi_0 < \Pi_0^{\text{pair}}$ | Thm 5.12, Prop. 5.13 | T10.3, T10.4, T10.7; T13 C2 |
| 7 | $\Pi$ | env. | Hill, real $n > 1$ | $F$ (below) → $H$ (above) | 0, or min then max | $H, m, M, F$ | A, LR, (1,0,1), W, E | LR, E | pair iff $\Pi_0 < \Pi_0^{\text{pair}}(n)$ | Thm 5.12, Prop. 5.13 | T10.3; T13 A5, C2 |
| 8 | $\Pi$ | env. | two-stage Bayesian | $F$ → $\Sigma/(\lambda + c_1 + c_2)$ (above) | up to 3 seen | — | A, LR, W, (0,0,2), E | LR, E | no $(1,0,k)$: minima exceed $F$ | Num. 5.15, Prop. 5.14 | T10.3; T13 C2 |
| 9 | $\Pi$ | env. | two-stage Hill | $F$ (below) → $\Sigma/(\lambda + c_1 + c_2)$ (above) | up to 4 seen | — | A, LR, (1,0,1), (1,0,2), W, (0,0,2), E | LR, E | — | Num. 5.15 | T10.3; T13 C2 |
| — | $\Pi$ | env. | any continuous gain | free above $\sigma_\star^2$ | any finite number | — | $R^2 < F$: exactly the classes with $\ell = 1$; $R^2 \ge F$: all | LR, E | — | Thm 5.1, Cor. 5.2–5.4 | T10.2 |
| 10 | $\Pi_0$ | design | Bayesian-weight | $V_c$ → $F$ (below) | one min iff $\Pi < \Pi_A$ | $\sigma_\star^2, V_c, F$ | A, 2R, LR, UR, E | n/a | cases P1–P3 | Prop. 4.3 | T8.3, T10.7; T13 C2 |
| 11 | $c$ | design | Bayesian-weight | $F$ (below) → $\infty$ | one min | $\sigma_\star^2, F$ | A, 2R, UR | n/a | — | Prop. 4.5 | T8.3, T10.7; T13 C2 |
| 12 | $\Pi_0$ (any monotone gain at fixed $\Pi$) | design | e.g. $c\tanh(\Pi/\Pi_0)$, $c(1 - e^{-\Pi/\Pi_0})$, $c\Pi^2/(\Pi^2 + \Pi_0^2)$ | $V_c$ → $F$ (below) | at most one min | — | A, 2R, LR, UR, E; never W or mixed | n/a | — | Thm 4.1 | T8.4; T13 C2 |
| 13 | $\tau$ (zero-freq. power) | env. | relay, any precision-only $G > 0$ | $V_w$ (below) → $H_G$ (above) | none | $H_G, V_w$ | A, LR, E | LR, E | LR at $R^2 = F$ iff $G > 2F\Pi$ | Prop. 6.3 | T9.4, T10.7; T13 C2 |
| 14 | $\tau$ (zero-freq. power) | env. | optimal | $\sigma_\star^2$ (below) → $0$ | none | $\sigma_\star^2$ | LR, E | LR, E | — | Thm 6.6, Prop. 6.7 | T9.4, T10.7; T13 C2 |
| 15 | $\tau$ (matched variance) | env. | relay, fixed $G > 0$ | $H_G$ → top (below) | none | $H_G$, top | A, UR, E | W, E | — | Prop. 6.12 | T10.6, T10.7; T13 C2 |
| 16 | $\tau$ (matched variance) | env. | optimal | $0$ → $0$ | one max at $1/\lambda$ | $P_{\max}$ | W, E | W, E | — | Prop. 6.10 | T10.6, T10.7; T13 C2 |
| 17 | $\tau$, power family $\beta \le 0$ | env. | optimal | $F$ ($\beta < 0$) or $\sigma_\star^2(1/K)$ ($\beta = 0$) → $0$ | none | one limit | LR, E | LR, E | ordered (info ↑) | Thm 7.8 | T11.3; T13 C2 |
| 18 | $\tau$, power family $0 < \beta < 2$ | env. | optimal | $0$ → $0$ | exactly one max | $\max P$ | W, E | W, E | not ordered | Thm 7.8, Thm 7.9 | T11.3; T13 A4, C2 |
| 19 | $\tau$, power family $\beta \ge 2$ | env. | optimal | $0$ → $\sigma_\star^2(\lambda^2/K)$ ($\beta = 2$) or $F$ ($\beta > 2$) | none | one limit | UR, E | UR, E | ordered (info ↓) | Thm 7.8 | T11.3 with diagnosis; T13 C2 |
| 20 | latency $d = \theta e^{-\theta}$ | env. | optimal | $\sigma_\star^2$ (above) → $\sigma_\star^2$ (above) | one max at $\theta = 1$ | $\sigma_\star^2, P(1/e)$ | A, W, E | A, W, E | pathwise-equivalent, causally reversing | Prop. 7.11 | T11.4; T13 C2 |
| 21 | $\Delta t$ (M-P) | either | optimal, post | $\sigma_\star^2$ → $0$ | none | $\sigma_\star^2$ | LR, E | LR, E | — | Thm 6.19(a) | T12; T13 C2 |
| 22 | $\Delta t$ (M-P) | either | optimal, prior | $\sigma_\star^2$ → $F$ (below) | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 6.19(b) | T12; T13 A1, C2 |
| 23 | $\Delta t$ (M-P) | either | optimal, avg | $\sigma_\star^2$ → $F$ (below) | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 6.19(c) | T12; T13 A2, C2 |
| 24 | $\Delta t$ (M-P) | either | D1 sampled relay, post | $\sigma^2(G, \Pi)$ → $0$ | none or one max | limits, max | E, LR, W | — | excess iff $G > 2F\Pi$ | Prop. 6.15; Num. 6.21 | T12; T13 C2 |
| 25 | $\Delta t$ (M-P) | either | D1, prior | $\sigma^2(G, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | 2R if $G > 2F\Pi$ (Proposition 6.20) | Prop. 6.20; Num. 6.21 | T12; T13 C2 |
| 26 | $\Delta t$ (M-P) | either | D1, avg | $\sigma^2(G, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | 2R if $G > 2F\Pi$ (Proposition 6.20); also seen for $G \le 2F\Pi$ (Numerical result 6.21) | Prop. 6.20; Num. 6.21 | T12; T13 C2 |
| 27 | $\Delta t$ (M-P) | either | D2 discrete Bayesian, post | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $(1-c)^2F$ | none, max, min, min–max | limits, extrema | A, E, LR, UR, 2R, W, (1,0,1) | — | excess iff $\kappa > 2$ | Prop. 6.16; Num. 6.21 | T12; T13 C2 |
| 28 | $\Delta t$ (M-P) | either | D2, prior | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 6.16; Num. 6.21 | T12; T13 C2 |
| 29 | $\Delta t$ (M-P) | either | D2, avg | $\sigma^2(c\Pi/\Pi_0, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 6.16; Num. 6.21 | T12; T13 C2 |
| 30 | $\Delta t$ (M-P) | either | D3 over-trust $\rho$, post | $\sigma^2(G_\rho, \Pi)$ → $0$ | none or one max | limits, max | E, LR, W | — | excess near 0 iff $\rho > 2 + u$ | Prop. 6.17; Num. 6.21 | T12; T13 C2 |
| 31 | $\Delta t$ (M-P) | either | D3, prior | $\sigma^2(G_\rho, \Pi)$ → $F$ (below) | none, min, max–min | limits, extrema | A, E, LR, UR, 2R, (0,1,1) | — | — | Prop. 6.17; Num. 6.21 | T12; T13 C2 |
| 32 | $\Delta t$ (M-P) | either | D3, avg | $\sigma^2(G_\rho, \Pi)$ → $F$ (below) | none, min | limits, min | A, E, LR, UR, 2R | — | — | Prop. 6.17; Num. 6.21 | T12; T13 C2 |
| 33 | $\Delta t$ (M-I) | either | optimal, (a) | $\sigma_\star^2$ → $F$ | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 7.15 | T11.6, T12; T13 A3, C2 |
| 34 | $\Delta t$ (M-I) | either | optimal, (b) | $\sigma_\star^2$ → $F$ | none | $\sigma_\star^2, F$ | A, UR, E | A, UR, E | — | Thm 7.15 | T11.6, T12; T13 A3, C2 |
| 35 | $\Sigma$, absolute | env. | $\Sigma$-independent gain | $G^2/(2\Pi(\lambda+G))$ (above) → $\infty$ | none | lower limit | A, UR | UR | — | Prop. 6.24 | T12; T13 C2 |
| 36 | $\Sigma$, relative | env. | $\Sigma$-independent gain | $\infty$ → $1/(1+g)$ | none | $1/(1+g)$ | A, LR | LR, E | excess iff $\Sigma < \lambda G/(2\Pi)$ | Prop. 6.24 | T12; T13 C2 |
| 37 | $\Sigma$, absolute | env. | $\Sigma$-tracking, over-trust $\rho$ | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 6.25 | T12; T13 C2 |
| 38 | $\Sigma$, relative | env. | $\Sigma$-tracking, over-trust $\rho$ | $1$ → $0$ | one max iff $\rho > 2$ | $1$, peak | LR, W, E | LR, E | W iff $\rho > 2$ | Prop. 6.25 | T12; T13 C2 |
| 39 | $\Sigma$, absolute | env. | $\Sigma$-tracking, misspecified $\lambda'$ | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 6.26 | T12; T13 C2 |
| 40 | $\Sigma$, relative | env. | $\Sigma$-tracking, misspecified $\lambda'$ | $1$ → $0$ | one max iff $\lambda' < \lambda/2$ | $1$, peak | LR, W, E | LR, E | W iff $\lambda' < \lambda/2$ | Prop. 6.26 | T12; T13 C2 |
| 41 | $\Sigma$, absolute | env. | optimal | $0$ → $\infty$ | none | — | UR | UR | — | Prop. 6.27 | T12; T13 C2 |
| 42 | $\Sigma$, relative | env. | optimal | $1$ → $0$ | none | $1$ | LR, E | LR, E | — | Prop. 6.27 | T12; T13 C2 |

Rows 1–20 and 35–42 are complete classifications (every class at every tolerance determined, impossibilities proved), except rows
8–9 (two-stage gains, numerical). Rows 21–23 are complete. Rows 33–34 are complete. Rows 24–32 give proved excess sets and limits; their class lists are
numerical.

---

## 4. Stage 5: robustness and practical relevance (restated)

Stage 5 asks whether the possible topologies are robust and whether real systems reach them. Stages 0–4 supply its inputs:

- **Hill mixed band.** The lower ray + window class $(1,0,1)$ occurs in a natural family but in a band of median relative
  width $5\times10^{-4}$ (range $4\times10^{-22}$ to $0.96$); in 16% of sets it exists without any window above $F$
  (Proposition 5.13). Question: how far is a realistic Hill-type gain schedule from that band, in tolerance and in $\Pi_0$?
- **Dip sizes along $\Delta t$.** The sampled relay's time-average dip below $F$ is modest (0.125% in the worked example,
  $\bar P - F \sim -F/(2\lambda\Delta t)$); the prior dip is multiplied by $e^{-2\lambda\Delta t}$ and measured between
  $10^{-17}$ and $10^{-32{,}880{,}317}$ (Proposition 6.20). Two-ray classes along $\Delta t$ are mathematically real but
  only the time-average ones could matter in practice.
- **Peak ratio 1.89.** At the same initial over-weighting (ratio 100) the misspecified Kalman gain peaks $1.89$ times higher
  than the Bayesian-weight gain (Proposition 5.9): peak height, not onset, separates gain families.
- **Structural stability.** By Theorem 2.2 the class is locally constant away from critical tolerances; Proposition 2.7 gives the
  fold exponents (positions $\delta^{1/2}$, values $\delta^{3/2}$) for the distance to a classification boundary.
- **Applied case.** Unchanged from v2: one setting with published gains and specifications (GNSS/INS fix weighting first),
  asking whether a specification looser than the uncorrected error ever meets a miscalibration large enough to clear it
  (Corollary 5.2 shows this is necessary for any window).

## 5. Stage 6: extensions (restated)

- **Fixed α–β filter.** A two-state filter; it does not fit the scalar model and is the first Stage 6 item.
- **Multivariate.** (1) Decoupled case: simultaneously diagonalizable dynamics, noises and gain split into scalar copies;
  prove first. (2) Mixing case: search 2×2 systems for windows no single direction predicts. (3) Choose and justify the vector
  failure criterion (trace, largest eigenvalue, fixed direction).
- **Discrete time and coloured noise** are now covered for scalar models (Sections 5–6 of the consolidated document);
  Theorem 7.6's spectral criterion is the natural starting point for vector-valued noise.

---

## 6. Paper 2 outline

| § | Section | Results (thesis numbering) | Figures (`figs_paper2/`; thesis captions in `figs_thesis/`) |
|---|---|---|---|
| 1 | Introduction: the starting study's window, the question of failure-set topology | Theorem 3.4, Proposition 5.8 | — |
| 2 | Setting and conventions; the class $(\ell, u, k)$ | C1–C6, Corollary 3.3, Lemma 3.6 | — |
| 3 | The critical-tolerance theorem | Proposition 2.1, Theorems 2.2, 2.4 | Fig. 1 |
| 4 | What the model allows along precision: realizability and the forced lower ray | Theorem 5.1, Corollaries 5.2–5.5 | Fig. 2 |
| 5 | Natural gain families and the mixed class | Lemmas 5.6, 3.7, 5.7, Propositions 5.9–5.11, Theorem 5.12, Proposition 5.13, Proposition 5.14, Numerical result 5.15 | Figs 3, 4 |
| 6 | Design sweeps never window | Theorem 4.1, Propositions 4.2–4.5 | — |
| 7 | Environment sweeps: correlation time (two normalizations, power family) | Lemma 6.1, Propositions 6.2, 6.3, 6.4, Theorem 6.6, Propositions 6.7, 6.8, 6.9, 6.10, Counterexample 6.11, Proposition 6.12, Theorems 7.8, 7.9, Proposition 7.10 | Figs 5, 6 |
| 8 | Sampling interval | Lemma 6.14, Propositions 6.15, 6.16, 6.17, 6.18, Theorem 6.19, Proposition 7.16, Corollary 7.14, Theorem 7.15, Proposition 6.20, Numerical result 6.21, Conjecture 6.22 | Figs 8, 9 |
| 9 | Process noise and the tolerance convention | Lemma 6.23, Propositions 6.24, 6.25, 6.26, 6.27, 6.28 | Fig. 10 |
| 10 | The optimality theorem: causal information orderings | Definition 7.1, Theorem 7.2, Corollaries 7.3, 7.4, Proposition 7.5, Theorem 7.6, Propositions 7.7, 7.11, Counterexample 7.12, Proposition 7.13 | Fig. 7 |
| 11 | Synthesis matrix, degeneracies and open problems | Corollaries 2.5–2.6, Proposition 2.7, Numerical results 8.2, 8.1; Section 10–11 of the consolidated document | — |
| A | Verification (pre-registration, routes, reproduction) | Consolidated §12; `reproduce_all.sh` | — |

---

## 7. Novelty step (v2 Section 15), Task 13

The check was run with web access on 2026-10-11 and is **targeted, not exhaustive**. Queries, sources and relevance are
recorded in `t13/literature_check.md`; the novelty part is reproduced here.

| # | Query | Sources found (as returned) | Relevance |
|---|---|---|---|
| 6 | steady-state filtering error variance exceeds tolerance set of parameters classification bounded failure window | Variance-constrained filtering (Wang, Ho and Liu, IEEE TAC 2003); worst-case variance bounds (Shaked and de Souza 1995); Sayed (IEEE TAC 2001); robust Kalman filtering, least-favourable model, arXiv 1804.06321 | P (design to a variance bound; no classification of exceedance sets along a parameter) |
| 7 | Kalman filter error variance non-monotone in sampling interval | Kalman filtering with random sampling (MTNS paper, mtns.math.nd.edu/papers/1149_3.pdf); Błachuta and Grygiel, sampled-signal Kalman filtering over sampling periods (ACC 2008); Kalman–Bucy (1961) | P (snippets do not report non-monotonicity) |
| 8 | mismatched Kalman filter error worse than no filtering over-confident measurement noise covariance | "Kalman filtering with uncertain noise covariances" (Cleveland State, D. Simon); "Recursive performance ranking of Kalman filter with mismatched noise covariances" (IET 2019); arXiv 2511.22034 | P (orders filter-calculated, ideal and true MSE; not failure-set topology) |
| 9 | Kalman filter colored measurement noise correlation time estimation error non-monotone | Coloured-noise filtering by state augmentation and measurement differencing (Bryson–Henrikson line; NASA 1967 memo; FIG 2003; ISPRS 2014) | P (methods; no study of the error along the correlation time) |
| 10 | measurement delay optimal filtering error increases latency Kalman Bucy Ornstein Uhlenbeck | Delayed-measurement Kalman–Bucy filtering (IFAC 2014, ACC 2011, Abstr. Appl. Anal.); finite-dimensional suboptimal filters for bounded delays | P (delay adds an error term; nothing on non-monotone delay sweeps or Blackwell equivalence) |
| 11 | (second search set, cluster 11: comparison of statistical and sequential experiments; query text not supplied to Task 14) | [greenshtein1996], [lecam1964], [torgersen1991], [hansentorgersen1974], [blackwell1951], [blackwell1953] | R (garbling order and monotone optimal performance; static and sequential, not filtering): cited for Theorem 7.2, Proposition 7.5, Theorem 7.6 |
| 12 | (second search set, cluster 12: information structures in stochastic control and teams; query text not supplied to Task 14) | [yuksellinder2012], [yukselbasar2013], [yukselbasar2024], [hogeboomburr2021] | R (Blackwell ordering of information structures in control): cited for Theorem 7.2, Theorem 7.6 |
| 13 | (second search set, cluster 13: covariance control and state covariance assignment; query text not supplied to Task 14) | [hotzskelton1985], [hotzskelton1987], [collinsskelton1987], [xuskelton1992], [yasuda1993], [skeltonikeda1989] | P (which covariances a gain can assign): related to Theorem 5.1 |
| 14 | (second search set, cluster 14: optimal sampling rate for state estimation; query text not supplied to Task 14) | [martinezrey2017] | P (sampling interval and estimation error): related to Theorem 6.19, Proposition 7.16 |
| 15 | (second search set, cluster 15: state estimation with coloured measurement noise; query text not supplied to Task 14) | [shmaliy2020] | P (methods for coloured noise): related to Proposition 6.10, Theorem 7.8 |
| 16 | (second search set, cluster 16: divisive normalization; query text not supplied to Task 14) | [heeger1992], [carandiniheeger2012] | P (Hill-type gain shapes in neural computation): related to Theorem 5.12, Proposition 5.13 |
| 17 | (second search set, cluster 17: persistence, contour trees and Morse theory; query text not supplied to Task 14) | [cohensteiner2007], [edelsbrunnerharer2010], [edelsbrunner2002], [carr2003], [oudot2015], [milnor1963] | P (topology of sublevel and superlevel sets of a function): related to Theorem 2.2, Proposition 2.9 |

**Finding (novelty, targeted).** None of the ten searches of the first set returned work that classifies the topology of
tolerance-exceedance sets of stationary filtering error along a parameter (rays, windows, mixed classes, critical
tolerances). Related strands exist: variance-constrained and robust filtering (design to a bound), sensitivity of the
Kalman filter to mis-specified covariances (filter-calculated versus true error), coloured-noise and delayed-measurement
filtering (methods), and Blackwell comparison of linear normal experiments (static).

Garbling-order monotonicity of optimal performance is established for sequential experiments [greenshtein1996] and for stochastic control and teams [yuksellinder2012], [yukselbasar2013], [yukselbasar2024]. Theorem 7.2 is presented as the filtering instance of that principle: a causal garbling of observation processes and its consequence for filtering error. Theorem 7.6 extends the static result for linear normal experiments [hansentorgersen1974] to stationary Gaussian processes.

This is a targeted check, not an exhaustive one; Paper 2 should repeat it with database
searches (MathSciNet, Scopus) before submission.

## Queries still to run (suggested)
- "Loewner order spectral density Gaussian process informativeness"; "Blackwell order filtrations" / "nonanticipative Blackwell dominance".
- "steady-state Kalman filter covariance versus correlation time Gauss-Markov measurement noise".
- "more measurements worse mis-specified Kalman filter precision", "over-weighting measurements relay worse than open loop".

---

## 8. Order of work

1. Paper 2 from the consolidated document (Sections 1–11 above).
2. Stage 5 (robustness, applied case) using the inputs of Section 4.
3. Stage 6 (α–β, multivariate), starting with the decoupled case.
4. Open problems 1–3 of Section 2 as they become tractable; each needs its own pre-registered task.
