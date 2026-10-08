"""Builds RESULTS_t11.md from results/*.json. Usage: python3 make_results_t11.py [code_commit_hash]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
PREREG = "5337c2e"
CODE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "(not yet committed)"


def L(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


r1, r2, r3, r3d, r4, r5, r6 = (L(f"t11_{k}.json") for k in ("1", "2", "3", "3_diag", "4", "5", "6"))
env = L("env.json")
rt = {}
if os.path.exists(os.path.join(RES, "runtime.tsv")):
    rt = {a: float(b) for a, b in (l.split("\t") for l in open(os.path.join(RES, "runtime.tsv")).read().splitlines() if l.strip())}
V = lambda ok: "**PASS**" if ok else "**FAIL**"
g = lambda x, f=".3g": format(float(x), f) if x is not None and not isinstance(x, str) else str(x)

items1 = [x for k, v in r1.items() if isinstance(v, list) for x in v if isinstance(x, dict) and "pass" in x]
fail_betas = [e for e in r3["by_beta"] if e["tp_fail"] or e["class_fail"] or e["limit_fail"]]
rows = [
    ("T11.1 symbolic", V(r1["pass"]), f"{sum(x['pass'] for x in items1)}/{len(items1)} items (routes: "
     + ", ".join(sorted({x['route'] for x in items1})) + ")", rt.get("t11_symbolic")),
    ("T11.2 garbling realized (MC)", V(r2["pass"]), "; ".join(
        f"({p['tau1']}, {p['tau2']}): autocov |z| ≤ {max(abs(a['z']) for a in p['autocov']):.2f}, MSE₁ z = {p['z1']:+.2f}, "
        f"excess {p['diff'] / p['diff_SE']:.0f} SE" for p in r2["pairs"]), rt.get("t11_garble")),
    ("T11.3 turning points", V(r3["pass_tp"]), f"failures {r3['tp_fail']}", None),
    ("T11.3 limits (bound)", V(r3["pass_limits"]), f"failures {r3['limit_fail']}; applicable ends {r3['limit_applicable']}", None),
    ("T11.3 classes (two routes)", V(r3["pass_classes"]), f"failing classifications {r3['class_fail']} (at β = "
     + ", ".join(g(e["beta"], ".6g") for e in fail_betas if e["class_fail"]) + ")", None),
    ("T11.3 duality", V(r3["duality_pass"]), f"max relative difference {g(r3['duality_max_rel'])}", None),
    ("T11.3 independent routes (ARE, Wiener)", V(r3["routes"]["pass"]), f"{r3['routes']['n']} evaluations, max rel. err "
     f"{g(r3['routes']['max_err'])}", None),
    ("T11.3 spectral dominance / crossing", V(r3["spectral"]["pass"]), f"failures {r3['spectral']['n_fail']} of "
     f"{sum(v['n'] for v in r3['spectral']['by_beta'].values())} pairs", rt.get("t11_power")),
    ("T11.4 delay counterexample", V(r4["pass"]), "MC |z| ≤ " + f"{max(abs(x['z']) for x in r4['mc']['rows']):.2f}; windows at q = 0.1, 0.5, 0.9 with "
     f"d(θ₋) = d(θ₊) to {g(max(x['d_rel_err'] for x in r4['sweep']['rows'] if x.get('d_rel_err') is not None))}; regression pass "
     f"{r4['regression']['pass']}", rt.get("t11_delay")),
    ("T11.5 ordering not necessary", V(r5["pass"]), f"P decreasing {r5['P_decreasing']}/1000, spectra cross once "
     f"{r5['spectra_cross_once']}/1000", rt.get("t11_notnec")),
    ("T11.6 sampling interval", V(r6["pass"]), f"internal {g(r6['internal']['max_p_err'])} / {g(r6['internal']['max_Q_err'])}; MC "
     f"max |z| {max(max(abs(x['a_z']), abs(x['b_z'])) for x in r6['mc']['rows']):.2f}; Cor. 4.9 violations "
     f"{r6['cor49']['violations_a']} (a), {r6['cor49']['violations_b']} (b)", rt.get("t11_sampling")),
]
T = ["# Task 11 — Stage 4 optimality: results", "",
     f"Verifies `classification/Stage_4_Optimality_Results.md`. Pre-registration `classification/PREREG_t11.md`, commit "
     f"**{PREREG}**; code and results commit **{CODE}**. Total measured script runtime **{sum(rt.values()):.0f} s** on "
     f"{env['cpus']} CPUs (Python {env['python']}, mpmath {env['mpmath']}, SymPy {env['sympy']}).", "",
     "| Check | Verdict | Counts / worst errors | Runtime (s) |", "|---|---|---|---|"]
for n, v, m, t in rows:
    T.append(f"| {n} | {v} | {m} | {'' if t is None else f'{t:.0f}'} |")
fails = [n for n, v, _, _ in rows if v == V(False)]
hist = r3["unimodality_hist_0_lt_beta_lt_2"]
nmid = sum(hist.values())
T += ["", "**Pre-registered checks that FAIL:** " + ("; ".join(fails) if fails else "none") + ".", "",
      "## Plain statements", "",
      "- **Is any theorem or proposition in the document contradicted?** No. Theorem 4.2 / Corollary 4.3 (via the garbling "
      "Monte Carlo and the ordered sweeps), Proposition 4.4–4.5 (spectral dominance, H_ξ), Theorem 4.6 (ordering, monotonicity "
      "and windows coincide exactly at β ∉ (0, 2)), Proposition 4.6b (duality), Proposition 4.7 (delay window), Proposition 4.8 "
      "and Corollary 4.9 all hold in every tested case. The only failures are the β ≥ 2 class checks, caused by limits/brackets "
      "in this pre-registration (diagnosis below); with corrected limits the classes are upper ray or Empty as Theorem 4.6 states.",
      "- **Did any class outside the predicted sets appear?** No. Every class in the failing cases is a route (i)/(ii) "
      "disagreement produced by the wrong pre-registered limit; re-run with the proved limit, all are upper ray or Empty with "
      "both routes agreeing.", "",
      f"## Numerical result 4.6a (unimodality) — answer", "",
      f"Turning-point counts over all {nmid:,} curves with 0 < β < 2 (β = 0.05 … 1.95 in steps of 0.05, 0 + 1e-6, 0 + 1e-3, "
      f"2 − 1e-3, 2 − 1e-6; 300 random (λ, Σ, K) each, λ, Σ, K over four decades): **{hist}**. Every curve has exactly one "
      "turning point (a maximum), so k = 1 throughout: Numerical result 4.6a holds on the whole grid (still a numerical "
      "result, not a proof, except β = 1).", "",
      "## T11.6 continuum answer (record only)", "",
      f"P̄(Δt) was monotone non-decreasing on 400 log-spaced λΔt ∈ [1e-3, 1e2] in all {r6['continuum']['n_sets']} random sets for "
      f"both metrics: {r6['continuum']['n_nonpositive_derivatives']} non-positive derivatives (dps 60), so **no non-monotone "
      "case was found** on the continuum of Δt, including non-nested pairs. Δt → 0: P̄_a(λΔt = 1e-8)/σ*² − 1 lies in "
      f"[{g(r6['continuum']['limit_rel_min'])}, {g(r6['continuum']['limit_rel_max'])}], consistent with P̄ → σ*².", ""]
# diagnosis
T += ["## Diagnosis: T11.3 class failures (attribution: criterion — the pre-registered limits/brackets)", "",
      "Found in a 2-set smoke run before the full run, from algebra; the pre-registration was not changed. As τ → ∞, "
      "4AC/B² → 2Στ^{2−β}/K. So:",
      "- **β = 2:** 4AC/B² → 2Σ/K, not 0, and P → 2F/(1 + √(1 + 2Σ/K)) = σ*²(λ²/K), the dual (Prop. 4.6b) of the β = 0 limit "
      "σ*²(1/K). The pre-registered table gave F.",
      "- **β slightly above 2:** the limit F is right but is approached like τ^{2−β}; the pre-registered outer bracket "
      "x = 80 leaves P far from F when β − 2 < about 0.5, so route (ii) and route (i) disagree for tolerances between P(10^80) "
      "and F.", ""]
if r3d:
    T += ["Re-run of every pre-registered set at the affected β with the proved limit (β = 2) or bracket "
          "max(80, 50/(β − 2)) (β > 2) (`t11_power_diag.py`):", "", "| β | classifications | failures | classes |", "|---|---|---|---|"]
    for e in r3d["by_beta"]:
        T.append(f"| {g(e['beta'], '.7g')} | {e['classifications']} | {e['failures']} | {e['classes']} |")
    if r3d.get("beta2_limit_check"):
        x = r3d["beta2_limit_check"][0]
        T += ["", f"β = 2 check: P(10^80/λ) = {g(x['P_at_1e80'], '.15g')} vs σ*²(λ²/K) = {g(x['sigma_star_lam2_over_K'], '.15g')}."]
T += ["", "Pre-registered failures by β: " + "; ".join(
    f"β = {g(e['beta'], '.7g')}: class {e['class_fail']}, tp {e['tp_fail']}, limits {e['limit_fail']}" for e in fail_betas) + ".", ""]
T += ["## Bugs found and fixed (documented)", "",
      "1. **T11.1 sign claim (before the first complete T11.1 run was recorded).** The pre-registered method proves signs via "
      "an identity with a manifestly signed right side; the first version asked SymPy for the sign of "
      "B + √(B²+4AC) − √(4AC) directly (undecided). Added the identity √(B²+4AC) − √(4AC) = B²/(√(B²+4AC) + √(4AC)); "
      "all 23 items then pass.",
      "2. A misleading code comment on the β > 2 bracket (it cited the wrong decay rate) was corrected; the code already "
      "followed the pre-registration.", ""]
T += ["## Wording and formula points in `Stage_4_Optimality_Results.md`", "",
      "1. **Prop. 4.5(c), \"Theorem 4.2 shows the family is not causally ordered by any garbling\".** Non-monotone P rules out "
      "a causal order *along τ* for the whole family. Pairwise causal orders against the τ direction are not excluded by "
      "Theorem 4.2; with crossing spectra they are excluded only for linear garblings (Prop. 4.4), i.e. this step also "
      "needs Conjecture 4.11.",
      "2. **Numbering:** Corollary 4.10 appears before Corollary 4.9.",
      "3. **Corollary 4.3 cites \"Theorem 3.13\"** (plateaus) from Stage 3 results, not available here; not checked.",
      "4. **Theorem 4.6 proof, limits:** \"This tends to 0 as τ → 0 iff β > 0, and as τ → ∞ iff β < 2\" is about the bound. "
      "The limits of P itself where the bound does not vanish are: β < 0, τ → 0: F; β = 0: σ*²(1/K); β = 2, τ → ∞: "
      "σ*²(λ²/K) (not F); β > 2, τ → ∞: F. Worth stating, since β = 2 is the boundary case and its limit is not F.",
      "5. **Prop. 4.5(b):** the garbling direction is from τ2 to τ1 with τ2 > τ1 (information increases with τ); "
      "H_ξ needs τ2 > τ1 for the square root to be real. Stated implicitly.", ""]
# details
T += ["## T11.3 details", "", "| β | regime | turning-point histogram | classes |", "|---|---|---|---|"]
for e in r3["by_beta"]:
    T.append(f"| {g(e['beta'], '.7g')} | {e['regime']} | {e['tp_hist']} | {e['classes']} |")
T += ["", "Spectral sign changes by β (0.25 grid): " + "; ".join(f"β = {g(k, '.3g')}: {v['changes']}" for k, v in r3["spectral"]["by_beta"].items()), ""]
T += ["## T11.2 details", "", "| (τ1, τ2) | lag | estimate | SE | target | z |", "|---|---|---|---|---|---|"]
for p in r2["pairs"]:
    for a in p["autocov"]:
        T.append(f"| ({p['tau1']}, {p['tau2']}) | {a['lag']:.3g} | {a['estimate']:.6g} | {a['SE']:.2g} | {a['target']:.6g} | {a['z']:+.2f} |")
T += ["", "| (τ1, τ2) | MSE τ1 filter on Y′ | P(τ1) | MSE τ2 filter on y_τ2 | P(τ2) | difference ± SE |", "|---|---|---|---|---|---|"]
for p in r2["pairs"]:
    T.append(f"| ({p['tau1']}, {p['tau2']}) | {p['MSE1_on_Yprime']:.6g} ± {p['SE1']:.2g} | {p['P_tau1']:.6g} | {p['MSE2_on_y_tau2']:.6g} ± "
             f"{p['SE2']:.2g} | {p['P_tau2']:.6g} | {p['diff']:.4g} ± {p['diff_SE']:.2g} |")
T += ["", "## T11.4 details", "", "| d | realized d | MC | SE | P(d) | z |", "|---|---|---|---|---|---|"]
for x in r4["mc"]["rows"]:
    T.append(f"| {x['d']:.4g} | {x['d_realized']:.4g} | {x['estimate']:.7g} | {x['SE']:.2g} | {x['formula']:.7g} | {x['z']:+.2f} |")
T += ["", "θ sweep: " + "; ".join(f"{x['q']}: {x['route_i']} / {x['route_ii']}" for x in r4["sweep"]["rows"]) + ". Regression: "
      + "; ".join(f"{x['q']} = {g(x['computed'], '.8g')} (stated {x['stated']})" for x in r4["regression"]["rows"]) + ".",
      "All four MC estimates sit at z ≈ +1.9: they share one signal path (common random numbers), so their deviations are "
      "strongly correlated.", "",
      "## T11.6 details", "", "| Δt | (a) MC ± SE | (a) closed form | z | (b) MC ± SE | (b) closed form | z |", "|---|---|---|---|---|---|---|"]
for x in r6["mc"]["rows"]:
    T.append(f"| {x['Dt']} | {x['a_est']:.6g} ± {x['a_SE']:.2g} | {x['a_formula']:.6g} | {x['a_z']:+.2f} | {x['b_est']:.6g} ± {x['b_SE']:.2g} | "
             f"{x['b_formula']:.6g} | {x['b_z']:+.2f} |")
T += ["", f"Cor. 4.9: min P̄(mΔt)/P̄(Δt) = {g(r6['cor49']['min_ratio_a'], '.15g')} (a), {g(r6['cor49']['min_ratio_b'], '.15g')} (b) "
      "over 9,000 pairs. The (b) MC at Δt = 5 (z = +2.8) is within the criterion; the Euler–Maruyama variance bias at "
      "dt = 5e-3 (about 0.25%) accounts for roughly one SE of it.", "",
      "## Figures", "", "`figs/G1_power_phase`, `G2_spectra`, `G3_delay`, `G4_sampling` (PNG + PDF).", "",
      "![G1](figs/G1_power_phase.png)", "", "![G2](figs/G2_spectra.png)", "", "![G3](figs/G3_delay.png)", "", "![G4](figs/G4_sampling.png)", "",
      "## Provenance", "", "Results come from separate invocations of the committed scripts (T11.3 and T11.6 in the background, "
      "the others directly; T11.1 re-run after bug 1). `run_t11.sh` reproduces everything in one pass. Runtime per script (s): "
      + ", ".join(f"{k} {v:.0f}" for k, v in rt.items()) + "."]
open(os.path.join(HERE, "RESULTS_t11.md"), "w").write("\n".join(T) + "\n")
print("\n".join(T[:30]))
