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
| 1 | General classification theorem | **Complete.** [[critical-tolerance]] (critical tolerances), [[plateaus]] (plateaus), [[topological-realizability]] (topology excludes nothing) | §2 |
| 2 | Model classification: $\Pi$, $\Pi_0$, $c$, $\tau$, $\Delta t$, $\Sigma$ | **Complete.** Every scalar sweep of v2 Section 6.2 classified | §3 ($\Pi$), §4 ($\Pi_0$, $c$), §5 ($\tau$, both normalizations, power family), §6 ($\Delta t$), §7 ($\Sigma$) |
| 3 | Falsification and completeness | **Complete.** Realizability, forced lower ray, unbounded windows, natural families (Hill for every $n > 1$), degeneracies, blind searches | §8 |
| 4 | The optimality theorem | **Complete.** [[causal-monotonicity]] (causal garbling ⇒ monotone), [[power-family-sharpness]] (exact sharpness in the power family), [[gaussian-orderings-coincide]] (non-linear garblings add nothing for additive Gaussian noise), [[pathwise-not-enough]] (causality essential) | §9 |

Verification: Tasks 8–13 (`REPORT.md`, `t9/`…`t13/RESULTS_t*.md`), all pre-registered; every failed check is recorded with
its diagnosis. Task 13 verified or closed seven of the eight items left open by Stages 2–4 (consolidated §12–13); one remains a conjecture.

**Answers to the v2 sub-questions.**
1. *Possible topologies in principle:* all ([[topological-realizability]]).
2. *What determines the topology:* endpoint limits, approach directions and ordered extremum values ([[critical-tolerance]]).
3. *Which sweeps and gain families give each topology:* the synthesis matrix below.
4. *Completeness and complexity:* complete for every family in the matrix except the two-stage gains; arbitrarily many
   windows are possible for constructed regular gains ([[unbounded-windows]]); natural families have at most two turning points
   along precision ([[hill-turning-points]]).
5. *Impossible for optimal filters:* along any causally ordered sweep, everything except Empty, All and a single ray at the
   less-informative end (Corollaries [[no-optimal-windows|n]]–[[diagnostic|n]]); along non-ordered sweeps the optimal filter can window ([[optimal-can-window]],
   [[power-family-sharpness]], [[latency]]).

---

## 2. Open problems (all items still open after Task 13)

1. **Turning points of sampled relays** ([[dt-two-turning-points]]): at most two turning points along $\Delta t$ for D1–D3 in every
   metric. Evidence: 6,000 sets × 3 metrics (Task 12) and 9,000 new curves (Task 13 audit), never more than two. Best
   partial result: proved limits and a single excess component.
2. **Two-stage gains** ([[two-stage-gains]]): a turning-point bound for sums of natural stages (at most 3 and 4 seen).
3. **A necessary condition for monotone optimal error** beyond the power family ([[power-family-sharpness]] is sharp there; [[ordering-not-necessary]]
   shows ordering is not necessary in general).
4. **The α–β filter and multivariate models** (Stage 6).

Closed by Task 13 (now theorems in the consolidated document): optimal M-P prior and time average increasing ([[dt-optimal-mp]]),
integrate-and-dump monotone on the continuum ([[mi-continuum]]), power-family unimodality ([[power-family-unimodal]]), Hill gain for every
$n > 1$ ([[hill-turning-points]]), strict gap between the optimal filter and the best constant gain along $\tau$ ([[tau-strict-gap]]), and
non-linear causal garblings ([[gaussian-orderings-coincide]]).

---

## 3. Final synthesis matrix (replaces v2 Section 14)

"#" is the row number of the Task 13 class audit (C2); "Opt." is what the optimal filter can produce along the same sweep. Classes
are written E (Empty), A (All), LR (lower ray), UR (upper ray), 2R (two rays), W (window), and triples $(\ell, u, k)$.

{{matrix}}

Rows 1–20 and 35–42 are complete classifications (every class at every tolerance determined, impossibilities proved), except rows
8–9 (two-stage gains, numerical). Rows 21–23 are complete. Rows 33–34 are complete. Rows 24–32 give proved excess sets and limits; their class lists are
numerical.

---

## 4. Stage 5: robustness and practical relevance (restated)

Stage 5 asks whether the possible topologies are robust and whether real systems reach them. Stages 0–4 supply its inputs:

- **Hill mixed band.** The lower ray + window class $(1,0,1)$ occurs in a natural family but in a band of median relative
  width $5\times10^{-4}$ (range $4\times10^{-22}$ to $0.96$); in 16% of sets it exists without any window above $F$
  ([[hill-classification]]). Question: how far is a realistic Hill-type gain schedule from that band, in tolerance and in $\Pi_0$?
- **Dip sizes along $\Delta t$.** The sampled relay's time-average dip below $F$ is modest (0.125% in the worked example,
  $\bar P - F \sim -F/(2\lambda\Delta t)$); the prior dip is multiplied by $e^{-2\lambda\Delta t}$ and measured between
  $10^{-17}$ and $10^{-32{,}880{,}317}$ ([[dt-two-rays]]). Two-ray classes along $\Delta t$ are mathematically real but
  only the time-average ones could matter in practice.
- **Peak ratio 1.89.** At the same initial over-weighting (ratio 100) the misspecified Kalman gain peaks $1.89$ times higher
  than the Bayesian-weight gain ([[misspecified-kalman]]): peak height, not onset, separates gain families.
- **Structural stability.** By [[critical-tolerance]] the class is locally constant away from critical tolerances; [[pair-birth]] gives the
  fold exponents (positions $\delta^{1/2}$, values $\delta^{3/2}$) for the distance to a classification boundary.
- **Applied case.** Unchanged from v2: one setting with published gains and specifications (GNSS/INS fix weighting first),
  asking whether a specification looser than the uncorrected error ever meets a miscalibration large enough to clear it
  ([[forced-lower-ray]] shows this is necessary for any window).

## 5. Stage 6: extensions (restated)

- **Fixed α–β filter.** A two-state filter; it does not fit the scalar model and is the first Stage 6 item.
- **Multivariate.** (1) Decoupled case: simultaneously diagonalizable dynamics, noises and gain split into scalar copies;
  prove first. (2) Mixing case: search 2×2 systems for windows no single direction predicts. (3) Choose and justify the vector
  failure criterion (trace, largest eigenvalue, fixed direction).
- **Discrete time and coloured noise** are now covered for scalar models (Sections 5–6 of the consolidated document);
  [[gaussian-orderings-coincide]]'s spectral criterion is the natural starting point for vector-valued noise.

---

## 6. Paper 2 outline

| § | Section | Results (thesis numbering) | Figures (`figs_paper2/`; thesis captions in `figs_thesis/`) |
|---|---|---|---|
| 1 | Introduction: {{phase1}}'s window, the question of failure-set topology | [[window-theorem]], [[bayesian-weight]] | — |
| 2 | Setting and conventions; the class $(\ell, u, k)$ | C1–C6, [[excess-identity]], [[single-minimum-gain]] | — |
| 3 | The critical-tolerance theorem | [[topological-realizability]], Theorems [[critical-tolerance|n]], [[plateaus|n]] | Fig. 1 |
| 4 | What the model allows along precision: realizability and the forced lower ray | [[realizability]], Corollaries [[forced-lower-ray|n]]–[[regularity-pins|n]] | Fig. 2 |
| 5 | Natural gain families and the mixed class | Lemmas [[excess-components|n]], [[elasticity|n]], [[bounded-gain-limit|n]], Propositions [[misspecified-kalman|n]]–[[precision-blind|n]], [[hill-turning-points]], [[hill-classification]], [[no-mixed-decreasing-ratio]], [[two-stage-gains]] | Figs 3, 4 |
| 6 | Design sweeps never window | [[monotone-gain-sweeps]], Propositions [[prior-endpoints|n]]–[[coupling-classification|n]] | — |
| 7 | Environment sweeps: correlation time (two normalizations, power family) | [[tau-relay-variance]], Propositions [[tau-relay-monotone|n]], [[tau-relay-classes|n]], [[tau-optimal-error|n]], [[tau-optimal-monotone]], Propositions [[tau-optimal-classes|n]], [[tau-best-constant-gain|n]], [[tau-strict-gap|n]], [[matched-variance-optimal|n]], [[optimal-can-window]], [[matched-variance-relay]], Theorems [[power-family-sharpness|n]], [[power-family-unimodal|n]], [[power-family-duality]] | Figs 5, 6 |
| 8 | Sampling interval | [[shared-excess-set]], Propositions [[d1-excess|n]], [[d2-excess|n]], [[d3-excess|n]], [[dt-endpoint-limits|n]], [[dt-optimal-mp]], [[mp-not-ordered]], [[mi-nested]], [[mi-continuum]], [[dt-two-rays]], [[dt-relay-census]], [[dt-two-turning-points]] | Figs 8, 9 |
| 9 | Process noise and the tolerance convention | [[sigma-scaling]], Propositions [[sigma-independent-gain|n]], [[sigma-overtrust|n]], [[sigma-misspecified-lambda|n]], [[sigma-optimal|n]], [[signal-sweeps|n]] | Fig. 10 |
| 10 | The optimality theorem: causal information orderings | [[causal-garbling]], [[causal-monotonicity]], Corollaries [[no-optimal-windows|n]], [[diagnostic|n]], [[spectral-dominance]], [[gaussian-orderings-coincide]], Propositions [[sweeps-ordered|n]], [[latency|n]], [[pathwise-not-enough]], [[ordering-not-necessary]] | Fig. 7 |
| 11 | Synthesis matrix, degeneracies and open problems | Corollaries [[equal-height-maxima|n]]–[[degenerate-points|n]], [[pair-birth]], Numerical results [[narrow-windows|n]], [[blind-searches|n]]; Section 10–11 of the consolidated document | — |
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
| 11 | (second search set, cluster 11: comparison of statistical and sequential experiments; query text not supplied to Task 14) | [greenshtein1996], [lecam1964], [torgersen1991], [hansentorgersen1974], [blackwell1951], [blackwell1953] | R (garbling order and monotone optimal performance; static and sequential, not filtering): cited for [[causal-monotonicity]], [[spectral-dominance]], [[gaussian-orderings-coincide]] |
| 12 | (second search set, cluster 12: information structures in stochastic control and teams; query text not supplied to Task 14) | [yuksellinder2012], [yukselbasar2013], [yukselbasar2024], [hogeboomburr2021] | R (Blackwell ordering of information structures in control): cited for [[causal-monotonicity]], [[gaussian-orderings-coincide]] |
| 13 | (second search set, cluster 13: covariance control and state covariance assignment; query text not supplied to Task 14) | [hotzskelton1985], [hotzskelton1987], [collinsskelton1987], [xuskelton1992], [yasuda1993], [skeltonikeda1989] | P (which covariances a gain can assign): related to [[realizability]] |
| 14 | (second search set, cluster 14: optimal sampling rate for state estimation; query text not supplied to Task 14) | [martinezrey2017] | P (sampling interval and estimation error): related to [[dt-optimal-mp]], [[mp-not-ordered]] |
| 15 | (second search set, cluster 15: state estimation with coloured measurement noise; query text not supplied to Task 14) | [shmaliy2020] | P (methods for coloured noise): related to [[matched-variance-optimal]], [[power-family-sharpness]] |
| 16 | (second search set, cluster 16: divisive normalization; query text not supplied to Task 14) | [heeger1992], [carandiniheeger2012] | P (Hill-type gain shapes in neural computation): related to [[hill-turning-points]], [[hill-classification]] |
| 17 | (second search set, cluster 17: persistence, contour trees and Morse theory; query text not supplied to Task 14) | [cohensteiner2007], [edelsbrunnerharer2010], [edelsbrunner2002], [carr2003], [oudot2015], [milnor1963] | P (topology of sublevel and superlevel sets of a function): related to [[critical-tolerance]], [[structural-stability]] |

**Finding (novelty, targeted).** None of the ten searches of the first set returned work that classifies the topology of
tolerance-exceedance sets of stationary filtering error along a parameter (rays, windows, mixed classes, critical
tolerances). Related strands exist: variance-constrained and robust filtering (design to a bound), sensitivity of the
Kalman filter to mis-specified covariances (filter-calculated versus true error), coloured-noise and delayed-measurement
filtering (methods), and Blackwell comparison of linear normal experiments (static).

Garbling-order monotonicity of optimal performance is established for sequential experiments [greenshtein1996] and for stochastic control and teams [yuksellinder2012], [yukselbasar2013], [yukselbasar2024]. [[causal-monotonicity]] is presented as the filtering instance of that principle: a causal garbling of observation processes and its consequence for filtering error. [[gaussian-orderings-coincide]] extends the static result for linear normal experiments [hansentorgersen1974] to stationary Gaussian processes.

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
