# G1 (B1): citation judgements (manual reading after the recorded run)

**Access, 2026-10-12.** Every full-text host tried was refused by the network policy: tandfonline.com (Roberts), scribd.com (a copy of
Roberts), mast.queensu.ca and arxiv.org (Yüksel & Linder), pmc.ncbi.nlm.nih.gov (Ren et al.), pages.stern.nyu.edu and dii.unimore.it
(Anderson & Moore). WebFetch: "host not resolved"; curl: CONNECT 403. The session's web search (standard and extended modes) was
used, and its summaries are paraphrased below. The scope of each judgement is stated.

| Source | Sentence(s) | Scope used | What the scope shows | Judgement |
|---|---|---|---|---|
| [26] Roberts (1959), Technometrics 1(3), 239–250 | §1.7 "the discrete variance factor α/(2 − α) [26]"; §6.3 "the discrete-time variance factor α/(2 − α) of an exponentially weighted average [26]" | bibliographic record and a summary of the paper (weight r on the most recent observation; "limit lines … based on the asymptotic standard deviation of the averages"); secondary sources (EWMA chart descriptions crediting Roberts with limits L·σ·√(λ/(2 − λ)), and the finite-t form (λ/(2 − λ))(1 − (1 − λ)^(2t))) | the paper defines the geometric moving average with weight r and bases its limits on the asymptotic standard deviation; the factor r/(2 − r) itself was **not seen in Roberts's text**, only in secondary sources that attribute it to him | **cannot be determined** from the source (consistent with every secondary source; not a pass under the criterion) |
| §6.3 identity | α²v/(1 − (1 − α)²) = αv/(2 − α) | SymPy and the fallback (run) | `simplify` reduces the difference to 0; 1 − (1 − α)² = α(2 − α) > 0 on (0, 2); fallback 1,000 sets, max relative residual 0 | **holds** |
| [29] Jazwinski (1970) | §7.4 "the error of a delayed estimate follows from the standard prediction step of the Kalman filter [29, 40]" | table of contents and reviews | Chapter 7 "Linear Filtering Theory" (pp. 194–265), sections on the continuous–discrete and discrete filters; reviews say "linear filters and predictors are developed" there. A continuous–discrete Kalman filter propagates the error covariance between observations (the prediction step) | **holds** at contents scope (the equation itself not seen) |
| [40] Anderson & Moore (1979) | same sentence | table of contents and catalogue description | Chapter 3 "The Discrete-Time Kalman Filter"; the book is the standard reference for the discrete Kalman filter, whose recursion includes the time update P(k+1|k) = F P(k|k) Fᵀ + G Q Gᵀ | **holds** at contents scope (the equation itself not seen) |
| [21] Yüksel & Linder (2012), SIAM J. Control Optim. 50(2), 864–887 | §1.6 "in stochastic control, where observation channels are themselves design variables [21]" | abstract (journal and arXiv versions, via search summaries) | the paper studies the optimization of observation channels (stochastic kernels) in partially observed stochastic control: existence, continuity, convexity/concavity in the channel, compactness, applications to quantizer design | **holds** (consistent) |
| [21] | §7.1 "the comparison of information structures in stochastic control and teams [22, 23], where observation channels are also treated as design variables [21]" | same | same; [21] is cited only for channels as design variables, which the abstract states | **holds** (consistent) |

**G1 verdict: FAIL.** The identity, [29], [40] and both [21] sentences hold; [26] cannot be determined from the source within the
session's reach (attribution: input — the source text is unreachable; every secondary source agrees with the draft's use).
Note: the Task 18 report said Kalata's DOI was "not confirmed from this session"; the bibliography already carried
doi:10.1109/TAES.1984.310438 for [25].
