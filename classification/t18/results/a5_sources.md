# Part A5: the two citations Task 17 could not settle (reported, not pass/fail)

**Access.** Full texts could not be fetched from this session: `pmc.ncbi.nlm.nih.gov`, `springerplus.springeropen.com` and
`api.pageplace.de` are refused (curl: CONNECT 403; the fetch tool: host not resolved), as are doi.org and Crossref (Task 17). The
session's web search (extended mode, 2026-10-12) was used instead; its summaries are paraphrased below.

## [26] Saho, K. & Masugi, M. (2016). α–β–γ tracking filters using acceleration measurements. SpringerPlus 5, 309. doi:10.1186/s40064-016-1960-8

- **What the source contains (from the search summaries):** a short report proposing two α–β–γ filters that use acceleration
  measurements (position–acceleration-measured, PAM; position–velocity–acceleration-measured, PVAM), with performance indices
  (steady-state tracking errors) derived from the authors' earlier work on position–velocity-measured filters, and numerical
  comparisons with the position-only-measured α–β–γ filter; derivations in its Additional file 1.
- **Does it state or use α/(2 − α) (or L/(2 − L)) for an exponentially weighted or α-type filter?** **Cannot be determined.** The
  summaries show no α-filter noise-reduction ratio and no exponentially weighted average; the extracted formulas were garbled.
  Its subject (three-state trackers with acceleration measurements) makes the scalar α-filter factor at most incidental.
- **Candidate standard references for "the variance factor α/(2 − α) of an exponentially weighted average":**
  1. Roberts, S. W. (1959). Control chart tests based on geometric moving averages. *Technometrics* 1(3), 239–250.
     doi:10.1080/00401706.1959.10489860 (DOI confirmed by the search from a published reference list). The EWMA control chart; the
     asymptotic EWMA variance factor λ/(2 − λ) is the standard result attributed to it (the search confirmed the factor from a
     secondary source, not from Roberts's text).
  2. Kalata, P. R. (1984). The tracking index: a generalized parameter for α–β and α–β–γ target trackers. *IEEE Transactions on
     Aerospace and Electronic Systems* AES-20(2), 174–182. DOI not confirmed from this session. The standard reference for steady-state
     α–β(–γ) tracker indices; whether it prints the α-filter ratio α/(2 − α) was not confirmed.

## [29] Jazwinski, A. H. (1970). Stochastic Processes and Filtering Theory. Mathematics in Science and Engineering 64. Academic Press.

- **What the source contains (from the search summaries):** nine chapters; Chapter 7 "Linear Filtering Theory" (pp. 194–265), with
  sections Introduction, Continuous–Discrete Filter, Discrete Filter, Continuous Filter, Observability and Information; the book
  introduces filtering, prediction and smoothing as problems, and a review says the linear chapters discuss "filtering and
  prediction". No section titled "prediction" was returned, and no statement about delayed estimates.
- **Does it give the prediction-error covariance for an estimate of a delayed state, or the prediction step in a form that covers
  it?** **Cannot be determined from the available text.** The continuous–discrete filter's between-observation covariance
  propagation is the prediction step that covers the delayed-state case (P(t | t − d) = e^(−2λd)P + F(1 − e^(−2λd)) for the scalar
  OU state), but the table of contents and review do not show it explicitly.
- **Candidate standard references for the prediction covariance:**
  1. Anderson, B. D. O. & Moore, J. B. (1979). *Optimal Filtering*. Prentice-Hall, Englewood Cliffs (ISBN 0-13-638122-7); Dover
     reprint 2005 (ISBN 0-486-43938-0). No DOI. Covers the discrete Kalman filter, prediction and smoothing (the search confirmed
     the bibliographic details and the topics, not the specific equation).
  2. Gelb, A. (ed.) (1974). *Applied Optimal Estimation*. MIT Press (ISBN 0-262-57048-3). No DOI. Standard treatment of
     covariance propagation between measurements. Not checked by search in this session.

The bibliography and the register are unchanged; the decision is the author's.
