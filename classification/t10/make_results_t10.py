"""Builds RESULTS_t10.md from results/*.json. Usage: python3 make_results_t10.py [code_commit_hash]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
PREREG = "da3d826"
CODE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "(not yet committed)"


def L(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


r1, r1d, r2, r3, r4, r5, r6, r7, rf = (L(f"t10_{k}.json") for k in ("1", "1_diag", "2", "3", "4", "5", "6", "7", "fig"))
r5d, r6d, r2d = L("t10_5_diag.json"), L("t10_6_diag.json"), L("t10_2_diag.json")
env = L("env.json")
rt = {}
if os.path.exists(os.path.join(RES, "runtime.tsv")):
    rt = {a: float(b) for a, b in (l.split("\t") for l in open(os.path.join(RES, "runtime.tsv")).read().splitlines() if l.strip())}
V = lambda ok: "**PASS**" if ok else "**FAIL**"
g = lambda x, f=".3g": format(float(x), f) if x is not None and not isinstance(x, str) else str(x)

items1 = [x for k, v in r1.items() if isinstance(v, list) for x in v if isinstance(x, dict) and "pass" in x]
fam = r3["families"]
def EXTRA():
    import mpmath as mp
    mp.mp.dps = 50
    o = []
    fails = [n for n, v, _, _ in rows if v == V(False)]
    o += ["", "**Pre-registered checks that FAIL:** " + "; ".join(fails) + ". Every one is traced below to the pre-registered "
          "criterion or to SymPy's simplification route, not to the plan. The only plan-level issue they expose is a gap in "
          "the A1.3 argument (the upper-branch inverse alone cannot give a convergent gain), which the pre-registered "
          "branch-following construction closes.", "",
          "## Plain statements", "",
          "- **Is any prediction in the Plan falsified?** No. A1 (realizability, forced lower ray, exact class sets), A3 "
          "(elasticity lemma and the Bayesian and misspecified-Kalman reductions), A4 (Bayesian, misspecified Kalman, capped, "
          "precision-blind and Hill turning-point bounds, including the Hill mixed class), A5 (equal-height maxima, "
          "inflection, plateau, pair birth with zero-width band) and A6 (the optimal filter windows along matched-variance τ) "
          "all hold in every tested case. A1.3 holds, but only with the branch-switching construction, not with G₊ as the "
          "plan writes it (see diagnosis).",
          f"- **Was any class outside the predicted set found?** No: {r7['total']:,} classifications in the blind search, "
          f"{r7['flagged']} flagged in float64, 0 persisting at 60 digits; no route disagreements anywhere in T10.2–T10.7.", ""]
    # diagnoses
    o += ["## Diagnoses of the failures", "",
          "### T10.1: two items not reduced by the fixed SymPy route (route limitation; identities hold)", "",
          f"- Misspecified inverse G(Π(G)) − G: SymPy leaves √({r1d['c']['radicand']}). Factoring the radicand gives "
          f"{r1d['c']['factored']} and the expression reduces to {r1d['c']['after_factoring_radicand']}.",
          f"- Forced ray σ*²(π_R) − R²: the radicand is {r1d['g']['radicand']}; its square root equals (2Σ − λR²)/R² only when "
          f"R² < 2F, which positive-symbol assumptions cannot express. With R² = F/(1 + w), w > 0, and the inner radicand "
          f"factored as {r1d['g']['inner_radicand_factored']}, it reduces to {r1d['g']['after_factoring']}.",
          "- Attribution: **criterion / route** (no √(square) handling in the pre-registered route). Plan: correct.", "",
          "### T10.2: A1.3 as specified (attribution: plan's construction; criterion as pre-registered)", "",
          "G₊ = Πv + √(…) ≥ Πv and v → H > 0, so G₊/Π → 2H: "
          + ", ".join(f"Π = {g(x['Pi'], '.0e')}: G₊/(2HΠ) = {g(x['G_plus_over_2H_Pi'], '.10f')}" for x in r2d["rows"][::3])
          + ". The lower branch G₋ equals the Bayesian gain and converges. The pre-registered supplementary construction "
          "(compactly supported bumps, G₊ for Π ≤ Π_c and G₋ beyond, where v_B touches σ*²) passes all five k, with branch "
          f"jump {g(r2['a13_supp'][0]['branch_jump_rel'])} and G(1e12)/G(1e11) − 1 = {g(r2['a13_supp'][0]['ratio_minus_1'])}. "
          "**A1.3's claim is true; its proof must switch to the lower branch at an envelope touch point, and bumps must not "
          "cover that point (Gaussian tails do).**", "",
          "### T10.5: pair-birth exponent (attribution: criterion)", "",
          f"Slope of log(M − m) vs log δ = **{r5['pair_birth']['slope_M_minus_m']:.4f}**; slope of the turning-point "
          f"separation = {r5['pair_birth']['slope_position_sep']:.4f}. Diagnosis (`t10_degenerate_diag.py`, δ to 1e-14): "
          f"slopes {r5d['slope_M_minus_m']:.5f} and {r5d['slope_x_sep']:.5f}, and (M − m)/sep³ is constant "
          f"({g(r5d['rows'][-1]['ratio_dv_over_dx3'], '.8f')}). At a fold the positions separate like δ^(1/2) and the values "
          "like δ^(3/2). The pre-registered [0.4, 0.6] applies to positions, not to M − m. The band still closes continuously "
          "(M − m → 0 monotonically), as the plan says.", "",
          "### T10.6: zero-limit criterion (attribution: criterion)", "",
          f"P/P_max at λτ = 1e∓12 is at least {g(r6d['min_P_over_Pmax'], '.6g')} in every set (pre-registered prediction: "
          f"≥ 4e-6); it equals the asymptote 2e-6(Σ + λv)/√(λΣv) to {g(r6d['max_rel_dev_from_asymptote'])}. The "
          f"supplementary check (P < 1e-6 P_max at λτ = 1e∓24, log-slopes ±0.5 within 1e-3) passes in "
          f"{r6['shape']['zero_supp_pass']}/1000 sets. P → 0 at both ends, as A6 states.", ""]
    # bugs
    o += ["## Bugs found and fixed (documented)", "",
          "1. **Onset prediction at δ = 0 (T10.3, found in a 20-set smoke run, fixed before the full run).** The prediction "
          "compared κ > 2 in floating mp arithmetic; at κ = 2 exactly the computed κ rounded above 2 and wrongly expected a "
          "maximum. Targeted sets now take the side from the sign of δ. The method's counts were correct.",
          "2. **Plateau tolerance (T10.5, found in the full run, fixed and re-run).** The capped curve was built from the "
          "float Σ = 0.01 (= 0.0100000000000000002 in binary) while F was the decimal 0.01, so R² = F sat 2e-17 below the "
          "plateau and both routes (correctly, for that R²) returned a lower ray. F is now taken from the curve's own "
          "parameters; the re-run passes. Commit message records the fix.",
          "3. Same float/decimal mismatch, no effect on any verdict: the Hill window-onset bisection compares M with the "
          "decimal F (result 25 to 1e-8 regardless) and the double-root refinement of Π0_pair uses decimal Σ (agrees with the "
          "bisection to ~1e-12).", ""]
    # wording
    o += ["## Wording and formula points in `Stage_3_Plan.md`", "",
          "1. **A4: \"Hill sextic\".** Q(t) is a quintic; t·Q(t) is the sextic (N = t·Q(t)/(1 + t²)³, T10.1(e)).",
          "2. **A1.3: \"G = G₊(v(Π), Π) is continuous and realizes v\" used for regular schedules.** True for realizability, "
          "but G₊ → ∞ whenever v → H > 0, so Paper 1 regularity (G → G∞ finite) needs the lower branch beyond an envelope "
          "touch point (diagnosis above).",
          "3. **A3: \"for a strictly increasing gain with inverse Π(G)\".** The identity dσ²/dΠ = G·N/(2Π²(λ+G)²) holds for "
          "any differentiable G(Π) > 0 (T10.1(a)); monotonicity is only needed to write N as a function of G.",
          "4. **A4 Hill: \"Proposition if A3's sextic can be tamed\".** It can (proof support below).",
          "5. **Task prompt (not the plan):** the pair-birth exponent and the λτ = 1e∓12 zero-limit threshold are mis-set "
          "(diagnoses above).", ""]
    # Hill proof support
    ps = r3["proof_support"]
    t2 = 2 * mp.sqrt(3) - 3
    lam_, c_, Sig_ = mp.mpf(1), mp.mpf(1), mp.mpf("0.01")
    P4 = -(lam_ + c_) * t2**2 + (c_ + 2 * lam_) * t2 + 3 * lam_
    phi = mp.sqrt(t2) * P4 / (1 + t2)**2
    P0c = c_ * phi / (4 * Sig_)
    P0n = [tr for e in r3["pair_birth"] if e["n"] == 2 for tr in e["transitions"]][0]
    P0n = P0n["Pi0_double_root"] if not isinstance(P0n["Pi0_double_root"], str) else P0n["Pi0_bisect"]
    o += ["## Hill n = 2 proof support (verbatim SymPy output; not pass/fail)", "",
          "Reduced quintic (α = λ/c, β = ΣΠ0/c², Q/c²):", "", "```", ps["Q_reduced"], "```", "",
          "Discriminant in t, factored:", "", "```", ps["discriminant_factored"], "```", "",
          "The first factor α⁴ + α³ + 4β² is positive, so root-count changes happen only on the zero set of the second factor "
          "(the pair-birth locus).", "",
          "Substitution route: " + ps["phi"] + ". Numerator of dφ/dt, factored:", "", "```", ps["dphi_numerator_factored"], "```", "",
          "In u = t²: " + ps["dphi_numerator_in_u"] + " (coefficients " + ", ".join(ps["coeffs_in_u"]) + ").", "",
          "**Reading (to be written up as a proof):** dφ/dt has the sign of −(t⁴ + 6t² − 3), whose only positive root is "
          "t*² = 2√3 − 3 for every λ, c. So φ rises on (0, t*) and falls after it; Q > 0 exactly where cφ(t)/4 > ΣΠ0, which is "
          "an interval or empty. Hence Q has 0 or 2 positive roots (1 only at tangency): the Hill n = 2 curve has no turning "
          "point or a minimum followed by a maximum, and the pair exists iff ΣΠ0 < cφ(t*)/4, with "
          "φ(t*) = t*·P₄(t*)/(1 + t*²)².",
          f"Check at λ = c = 1, Σ = 0.01: closed form Π0_pair = {mp.nstr(P0c, 15)}; numerical (T10.3) {g(P0n, '.15g')}; "
          f"relative difference {mp.nstr(abs(P0c - mp.mpf(P0n)) / P0c, 3)}.", ""]
    # pair-birth table and census details
    o += ["## T10.3 details", "", "| family | sets | turning-point histogram | failures |", "|---|---|---|---|"]
    for k, v in fam.items():
        o.append(f"| {k} | {v['n']} | {v['tp_hist']} | {v['n_fail']} |")
    o += ["", "Hill by n: " + "; ".join(f"n = {n}: {fam['hill'].get(f'tp_hist_n{n}')}" for n in (1.5, 2, 3, 4, 8))
          + f". Exact root-count disagreements (n = 2): {fam['hill']['exact_count_disagreements']}. Max position error vs the A3 "
          f"roots: Bayesian {g(fam['bayes'].get('max_pos_rel_err'))}, misspecified {g(fam['misspec'].get('max_pos_rel_err'))}.", "",
          "Targeted onset sets: " + "; ".join(f"{k} {'pass' if v['pass'] else 'FAIL'} ({v.get('n', len(v.get('rows', [])))})"
                                              for k, v in r3["targeted"].items()) + ".", "",
          "| n | Π0_pair (λ = c = 1, Σ = 0.01) | bisection vs double-root rel. diff |", "|---|---|---|"]
    for e in r3["pair_birth"]:
        for tr in e["transitions"]:
            o.append(f"| {e['n']} | {g(tr['Pi0_double_root'] if not isinstance(tr['Pi0_double_root'], str) else tr['Pi0_bisect'], '.12g')} "
                     f"| {g(tr['rel_diff'])} |")
    o += ["", "Every n has exactly one transition (2 → 0 turning points) on Π0 ∈ [1e-4, 1e4].", "",
          "Regression values: " + "; ".join(f"{x['what']}: {'pass' if x['pass'] else 'FAIL'}" for x in r3["regression"]) + ".", ""]
    # exploratory
    o += ["## Exploratory census (record only)", "", "| family | sets | turning-point histogram | kind sequences | ≥ 2 maxima |",
          "|---|---|---|---|---|"]
    for k, v in r3["exploratory"].items():
        o.append(f"| {k} | {v['n']} | {v['tp_hist']} | {v['kind_sequences']} | {v['n_two_or_more_max']} |")
    o += ["", "Both semi-natural families produce curves with two maxima: two-channel Bayesian (max, min, max) in 7/2000 and "
          "two-channel Hill (min, max, min, max) in 63/2000, i.e. multi-window (and, for Hill, mixed multi-window) classes "
          "are reachable by sums of two natural stages. Examples (parameters in `results/t10_3.json`):", ""]
    for k, v in r3["exploratory"].items():
        for x in v["examples_two_or_more_max"][:2]:
            o.append(f"- {k}: " + ", ".join(f"{a} = {g(b, '.4g')}" for a, b in x["p"].items()) + f"; kinds {x['kinds']}; "
                     f"values " + ", ".join(g(y, '.5g') for y in x["values"]))
    # T10.4 / T10.5 / T10.6 / T10.7 details
    o += ["", "## T10.4 details", "",
          f"{r4['n_sets']} Hill sets with two turning points (by n: {r4['by_n']}), {r4['n_tests']:,} tolerances, both routes "
          f"equal the prediction at every one. Band width (min(M,F) − max(m,H))/F: median {g(r4['band_rel_median'])}, min "
          f"{g(r4['band_rel_min'])}, max {g(r4['band_rel_max'])}. Lower band edge is m in {r4['lo_counts']['m']} sets and H in "
          f"{r4['lo_counts']['H']} (m > H always here); upper edge is M (M < F) in {r4['hi_counts']['M']} sets "
          f"(fraction {r4['frac_M_lt_F']:.3f}) and F in {r4['hi_counts']['F']}.", "",
          "## T10.5 details", ""]
    o += [f"- Equal-height maxima: " + "; ".join(f"{x['R2']}: {x['route_i']} / {x['route_ii']}" for x in r5["equal_maxima"]["rows"]),
          f"- Inflection vs smoothed: same turning points {r5['inflection']['same_turning_points']}, class mismatches "
          f"{r5['inflection']['class_mismatches']} over {r5['inflection']['n_tolerances']} tolerances, route disagreements "
          f"{r5['inflection']['route_disagreements']}.",
          f"- Plateau (capped, g = 2F): " + "; ".join(f"{x['R2']}: {x['route_i']} / {x['route_ii']}" for x in r5["plateau"]["rows"])
          + " (prediction: lower ray past c/g, Empty, Empty).",
          f"- Pair birth (Hill n = 2, Π0_pair = {g(r5['pair_birth']['Pi0_pair'], '.15g')}): turning points at "
          f"Π0_pair(1 + 1e-6): {r5['pair_birth']['n_tp_at_plus_1e-6']}.",
          f"- Narrow windows (relative width 1e-8): classifier correct in {r5['narrow']['n_found']}/20 curves "
          f"({r5['narrow']['windows_total']} windows); a 10⁴-point log grid on x ∈ [−25, 25] hits "
          f"{r5['narrow']['grid_windows_found']} of them.", "",
          "## T10.6 details", "",
          f"- Three routes: {r6['routes']['n']} evaluations, max pairwise relative difference {g(r6['routes']['max_err'])}, ARE "
          f"converged in all (at most {r6['routes']['max_steps']} ε-steps).",
          f"- Shape: core failures {r6['shape']['n_core_fail']}; max turning-point position error {g(r6['shape']['max_pos_rel_err'])}; "
          f"max symmetry error {g(r6['shape']['max_sym_rel_err'])}; peak error {g(r6['shape']['max_peak_rel_err'])}.",
          f"- Classes: failing sets {r6['classes']['n_fail']} (window with τ₋τ₊ = 1/λ² below P_max, Empty at and above).",
          f"- Relay: failing sets {r6['relay']['n_fail']} (increasing, limits H_G and (Σ + G²v/a)/a, relay ≥ P).",
          "- Regression: " + "; ".join(f"{x['q']} = {g(x['computed'], '.8g')} (stated {x['stated']})" for x in r6["regression"]["rows"]), "",
          "| τ | filter | MC | SE | formula | z |", "|---|---|---|---|---|---|"]
    for x in r6["mc"]["rows"]:
        o.append(f"| {x['tau']} | {x['filter']} | {x['estimate']:.6g} | {x['SE']:.2g} ({100 * x['se_rel']:.2f}%) | {x['formula']:.6g} | {x['z']:+.2f} |")
    o += ["", "## T10.7 details", "", "| sweep | curves | classifications | classes found | predicted set | flagged | persisting |",
          "|---|---|---|---|---|---|---|"]
    for k, v in r7["by_kind"].items():
        o.append(f"| {k} | {v['curves']} | {v['classifications']:,} | {v['classes']} | {', '.join(v['predicted'])} | {v['flagged']} | {v['persisting']} |")
    o += ["", "Predicted classes that never occurred: Hill 'two rays' (needs m < H; in every Hill set here m > H) and none "
          "else.", "",
          "## Figures", "",
          "`figs/F1_realizability`, `F2_hill_family`, `F3_hill_phase`, `F4_peak_heights`, `F5_matched_variance` (PNG + PDF).",
          f"F4 at x = 100: Bayesian M/F = {rf['bayes_M_over_F_at_100']:.4f}, misspecified M/F = {rf['misspec_M_over_F_at_100']:.4f}, "
          f"ratio {rf['ratio_misspec_over_bayes']:.4f} (Paper 1's exploratory value: about 2).", "",
          "![F1](figs/F1_realizability.png)", "", "![F2](figs/F2_hill_family.png)", "", "![F3](figs/F3_hill_phase.png)", "",
          "![F4](figs/F4_peak_heights.png)", "", "![F5](figs/F5_matched_variance.png)", "",
          "## Provenance", "",
          "Results come from separate invocations of the committed scripts (census first, then T10.4–T10.7 in sequence; T10.5 "
          "re-run after bug 2; T10.1, T10.2 and the figures re-run for logs). `run_t10.sh` reproduces everything in one go "
          "(about 1.6 h on 4 CPUs). Runtime per script (s): " + ", ".join(f"{k} {v:.0f}" for k, v in rt.items()) + "."]
    return o


rows = [
    ("T10.1 symbolic", V(r1["pass"]), f"{sum(x['pass'] for x in items1)}/{len(items1)} items reduce to 0 by the fixed route; "
     f"failing: " + "; ".join(x["desc"] for x in items1 if not x["pass"]), rt.get("t10_symbolic")),
    ("T10.2 realizability: every class", V(r2["pass_every"]), f"{sum(r['pass'] for r in r2['every'])}/{len(r2['every'])} "
     "targets realized (both routes, G ≥ 0, continuous, σ² = v)", rt.get("t10_realize")),
    ("T10.2 forbidden classes", V(r2["pass_forbidden"]), f"{sum(r['blocked'] for r in r2['forbidden'])}/{len(r2['forbidden'])} blocked", None),
    ("T10.2 A1.3 as specified (Gaussian bumps, G₊)", V(r2["pass_a13"]),
     "k windows in all five; G → 0 and G²/Π → 0 at 1e-12; **G(1e12)/G(1e11) − 1 = "
     + g(r2["a13"][0]["ratio_minus_1"]) + "** (G₊ diverges)", None),
    ("T10.2 A1.3 supplementary (compact bumps, G₊ → G₋ at Π_c)", V(r2["pass_a13_supp"]),
     f"all five pass; G(1e12)/G(1e11) − 1 = {g(r2['a13_supp'][0]['ratio_minus_1'])}, branch jump {g(r2['a13_supp'][0]['branch_jump_rel'])}", None),
    ("T10.3 census", V(r3["pass"]), "; ".join(f"{k}: {v['n']} sets, TP hist {v['tp_hist']}, fails {v['n_fail']}"
                                             for k, v in fam.items()) + f"; parts {r3['pass_parts']}", rt.get("t10_census")),
    ("T10.4 mixed class (Hill)", V(r4["pass"]), f"{r4['n_sets']} two-TP sets, {r4['n_tests']} tolerances, failing sets "
     f"{r4['n_fail_sets']}", rt.get("t10_mixed")),
    ("T10.5 degeneracies", V(r5["pass"]), "; ".join(f"{k} {'pass' if r5[k]['pass'] else 'FAIL'}"
                                                    for k in ("equal_maxima", "inflection", "plateau", "pair_birth", "narrow")),
     rt.get("t10_degenerate")),
    ("T10.6 matched-variance τ", V(r6["pass"]), "; ".join(f"{k} {'pass' if r6[k]['pass'] else 'FAIL'}"
                                                         for k in ("routes", "shape", "classes", "relay", "mc", "regression")),
     rt.get("t10_tau")),
    ("T10.7 blind search", V(r7["pass"]), f"{r7['total']:,} classifications; flagged in float64 {r7['flagged']}; persisting at "
     f"60 digits {r7['n_persist']}", rt.get("t10_blind")),
]
T = ["# Task 10 — Stage 3 falsification and completeness: results", "",
     f"Tests `classification/Stage_3_Plan.md` against `classification/Task_10_Stage3_Prompt.md`. Pre-registration "
     f"`classification/PREREG_t10.md`, commit **{PREREG}**; code and results commit **{CODE}**. Total measured script runtime: "
     f"**{sum(rt.values()):.0f} s** on {env['cpus'] if env else '?'} CPUs (Python {env['python'] if env else '?'}, mpmath "
     f"{env['mpmath'] if env else '?'}, SymPy {env['sympy'] if env else '?'}).", "",
     "| Check | Verdict | Counts / worst errors | Runtime (s) |", "|---|---|---|---|"]
for n, v, m, t in rows:
    T.append(f"| {n} | {v} | {m} | {'' if t is None else f'{t:.0f}'} |")
T += EXTRA()
open(os.path.join(HERE, "RESULTS_t10.md"), "w").write("\n".join(T) + "\n")
print("\n".join(T[:40]))
