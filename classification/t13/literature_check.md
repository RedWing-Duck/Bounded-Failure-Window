# Task 13 literature check (A8 and Roadmap Section 15 novelty step)

Run on 2026-10-11 with the session's web search tool (US results). **Targeted, not exhaustive**: ten queries, top results
read from the search summaries only (full texts were not read unless stated). Relevance: D = directly relevant,
P = partially relevant, N = not relevant.

## A. Comparison of Gaussian experiments (for Theorem 69, ex Conjecture 4.11)

| # | Query | Sources found (as returned) | Relevance |
|---|---|---|---|
| 1 | Hansen Torgersen 1974 comparison of linear normal experiments Annals of Statistics | O. H. Hansen and E. N. Torgersen, "Comparison of Linear Normal Experiments", Ann. Statist. 2(2):367–373 (1974), doi:10.1214/aos/1176342672 (Project Euclid); H. Heyer, Monatsh. Math. (1988), extension to Loewner-ordered comparison; E. N. Torgersen, *Comparison of Statistical Experiments*, Cambridge UP (1991), chapter on linear models | D (static case) |
| 2 | Blackwell comparison of experiments Gaussian processes spectral density ordering | No source on spectral-density ordering of Gaussian processes. arXiv 2602.20581 (empirical-Bayes design) states that Loewner-smaller noise covariance gives Blackwell dominance for any prior, citing Hansen–Torgersen; arXiv 2104.11547 (transitional conditional independence) gives the garbling definition | P |
| 3 | causal Blackwell ordering filtering comparison of experiments stochastic processes nonanticipative garbling | Nothing on a causal / nonanticipative Blackwell order for processes. Returned: arXiv 2104.11547, 2010.07416 (Markov categories), 2410.21694 (weighted garbling), 2404.15158 (Lehmann order) | N for the causal question |
| 4 | comparison of information structures stochastic control garbling Blackwell Yuksel Linder | I. Hogeboom-Burr and S. Yüksel, "Comparison of information structures for zero-sum games and a partial converse to Blackwell ordering in standard Borel spaces", SIAM J. Control Optim. (2021), arXiv 2005.06673; Kim–Obara weighted garbling, arXiv 2308.09211 | P |
| 5 | Witsenhausen "on information structures, feedback and causality" comparison of information structures | Andersland–Teneketzis (information structures, causality, nonsequential control); Illinois chapter "Characterization and comparison of information structures"; arXiv 2408.03037, 2408.02807 (Witsenhausen counterexamples with feedback) | P |

**Finding (A8).** The static result is classical: for linear normal experiments with known noise, Blackwell ordering is
equivalent to Loewner ordering of the information matrices (Hansen and Torgersen 1974; Torgersen 1991). The searches
found no statement for stationary Gaussian *processes* ordered by spectral density, and nothing on a *causal*
(nonanticipative) garbling order in filtering. Theorem 69 is therefore proved in the consolidated document (Task 13 A8)
rather than cited; it is the process analogue of the Hansen–Torgersen result, obtained by reducing the causal order to
two-sided (smoothing) errors with Lévy's upward theorem and localizing in frequency.

## B. Novelty step (Roadmap Section 15)

| # | Query | Sources found (as returned) | Relevance |
|---|---|---|---|
| 6 | steady-state filtering error variance exceeds tolerance set of parameters classification bounded failure window | Variance-constrained filtering (Wang, Ho and Liu, IEEE TAC 2003); worst-case variance bounds (Shaked and de Souza 1995); Sayed (IEEE TAC 2001); robust Kalman filtering, least-favourable model, arXiv 1804.06321 | P (design to a variance bound; no classification of exceedance sets along a parameter) |
| 7 | Kalman filter error variance non-monotone in sampling interval | Kalman filtering with random sampling (MTNS paper, mtns.math.nd.edu/papers/1149_3.pdf); Błachuta and Grygiel, sampled-signal Kalman filtering over sampling periods (ACC 2008); Kalman–Bucy (1961) | P (snippets do not report non-monotonicity) |
| 8 | mismatched Kalman filter error worse than no filtering over-confident measurement noise covariance | "Kalman filtering with uncertain noise covariances" (Cleveland State, D. Simon); "Recursive performance ranking of Kalman filter with mismatched noise covariances" (IET 2019); arXiv 2511.22034 | P (orders filter-calculated, ideal and true MSE; not failure-set topology) |
| 9 | Kalman filter colored measurement noise correlation time estimation error non-monotone | Coloured-noise filtering by state augmentation and measurement differencing (Bryson–Henrikson line; NASA 1967 memo; FIG 2003; ISPRS 2014) | P (methods; no study of the error along the correlation time) |
| 10 | measurement delay optimal filtering error increases latency Kalman Bucy Ornstein Uhlenbeck | Delayed-measurement Kalman–Bucy filtering (IFAC 2014, ACC 2011, Abstr. Appl. Anal.); finite-dimensional suboptimal filters for bounded delays | P (delay adds an error term; nothing on non-monotone delay sweeps or Blackwell equivalence) |

**Finding (novelty, targeted).** None of the ten searches returned work that classifies the topology of
tolerance-exceedance sets of stationary filtering error along a parameter (rays, windows, mixed classes, critical
tolerances). Related strands exist: variance-constrained and robust filtering (design to a bound), sensitivity of the
Kalman filter to mis-specified covariances (filter-calculated versus true error), coloured-noise and delayed-measurement
filtering (methods), and Blackwell comparison of linear normal experiments (static). No source on a causal Blackwell
ordering in filtering was found. This is a targeted check, not an exhaustive one; Paper 2 should repeat it with database
searches (MathSciNet, Scopus) before submission.

## Queries still to run (suggested)
- "Loewner order spectral density Gaussian process informativeness"; "Blackwell order filtrations" / "nonanticipative Blackwell dominance".
- "steady-state Kalman filter covariance versus correlation time Gauss-Markov measurement noise".
- "more measurements worse mis-specified Kalman filter precision", "over-weighting measurements relay worse than open loop".
