"""Builds RESULTS_t12.md from results/*.json. Usage: python3 make_results_t12.py [code_commit_hash]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
PREREG = "6e09e88"
CODE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "(not yet committed)"


def L(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


sym, symd, a8, dt, mi, sg, bl, dg = (L(f"t12_{k}.json") for k in ("symbolic", "symbolic_diag", "a8", "dt", "mi", "sigma", "blind", "diag"))
env = L("env.json")
rt = {}
for fn in ("runtime.tsv", "chain_runtime.tsv"):
    p = os.path.join(RES, fn)
    if os.path.exists(p):
        rt.update({a: float(b) for a, b in (l.split("\t") for l in open(p).read().splitlines() if l.strip())})
for s in ("t12_symbolic", "t12_dt", "t12_mi"):
    p = os.path.join(RES, f"{s}.time")
    if s not in rt and os.path.exists(p):
        for l in open(p):
            if l.startswith("real"):
                m, sec = l.split()[1].rstrip("s").split("m")
                rt[s] = 60 * float(m) + float(sec)
V = lambda ok: "**PASS**" if ok else "**FAIL**"
g = lambda x, f=".3g": format(float(x), f) if x is not None and not isinstance(x, str) else str(x)
FAM = a8["families"] if a8 else {}

# ---------------------------------------------------------------- check rows
sym_items = [it for k, v in sym.items() if isinstance(v, list) and k != "lines" for it in v if "pass" in it]
sym_fail = [it for it in sym_items if not it["pass"]]
ex1, ex2, ex3 = (FAM[f]["excess"] for f in ("D1", "D2", "D3"))
a7p, a7a = FAM["D1"]["a7_prior"], FAM["D1"]["a7_avg"]
cen_dis = {f"{f} {m}": FAM[f][m]["n_disagree_sets"] for f in FAM for m in ("post", "prior", "avg")}
rows = [
    ("Symbolic identities and signs (A1–A6, B1–B5)", V(sym["pass"]), f"{sum(it['pass'] for it in sym_items)}/{len(sym_items)} items; "
     f"failing: " + ("; ".join(it["desc"] for it in sym_fail) or "none"), rt.get("t12_symbolic")),
    ("A2 D1 excess set at R² = F (1,000 sets)", V(a8["A2_pass"]), f"{ex1['n_pass']}/{ex1['n']} match; non-empty predicted "
     f"{ex1['n_nonempty_pred']}; max rel. error of Δt_E {g(ex1['max_rel_err'])}", None),
    ("A3 D2 excess set at R² = F (1,000 sets)", V(a8["A3_pass"]), f"{ex2['n_pass']}/{ex2['n']} match; non-empty predicted "
     f"{ex2['n_nonempty_pred']}; max rel. error of Δt_E {g(ex2['max_rel_err'])}", None),
    ("A4 D3 excess set vs exact condition (1,000 sets)", V(a8["A4_census_pass"]), f"{ex3['n_pass']}/{ex3['n']} agree; membership "
     f"disagreements {ex3['n_disagree_points']} of {ex3['n_test_points']} test points; onset predicted (ρ > 2 + u) "
     f"{ex3['n_onset_pred']}, observed {ex3['n_onset_obs']}; shapes {ex3['shapes']}", None),
    ("A6 regression (optimal M-P, 5 s.f.)", V(dt["A6_regression"]["pass"]), "; ".join(
        f"{r['metric']}({r['dt']}) = {float(r['value']):.8g} (stated {r['stated']})" for r in dt["A6_regression"]["rows"]), None),
    ("A6 numerical monotonicity (record)", "record", f"{dt['A6_monotone']['n_points']:,} points × 3 metrics, λΔt ∈ [1e-8, 1e8]: "
     f"violations {dt['A6_monotone']['n_violations']}; Δt → 0 max rel. dev. from σ*² {g(dt['A6_monotone']['max_lim0_rel'])}", None),
    ("A7 minimum below F and two rays (D1, G > 2FΠ)", V(a8["A7_pass"]), f"prior {a7p['n_pass']}/{a7p['n_sets']} (no minimum found "
     f"{a7p['n_no_min_below_F']}), avg {a7a['n_pass']}/{a7a['n_sets']} (no minimum found {a7a['n_no_min_below_F']})", None),
    ("A8 census: route (i) = route (ii)", V(a8["census_pass"]), "sets with a disagreement: " + ", ".join(f"{k} {v}" for k, v in cen_dis.items()),
     rt.get("t12_a8")),
    ("A8 qualitative regression (prompt's values)", V(dt["A8_regression"]["pass"]), "post single max "
     f"{dt['A8_regression']['post_single_max']}, value within 2% of 0.166 {dt['A8_regression']['max_value_within_2pct_of_0.166']}, "
     f"at Δt within ×2 of 1 {dt['A8_regression']['max_at_dt_within_factor_2_of_1']}; avg crossing within ×1.5 of 50 "
     f"{dt['A8_regression']['crossing_within_factor_1.5_of_50']}; then min below F, back from below "
     f"{dt['A8_regression']['then_min_below_F_and_returns_from_below']}", None),
    ("A9 regression vs Task 11 (1e-12)", V(mi["regression"]["pass"]), "max rel. error " + g(max(max(r["rel_a"], r["rel_b"]) for r in mi["regression"]["rows"])), None),
    ("A9 numerical monotonicity (record)", "record", f"{mi['monotone']['n_points']:,} points × 2 metrics, λΔt ∈ [1e-8, 1e8]: "
     f"violating sets {mi['monotone']['n_violating_sets']}; SymPy sign attempt: (a) {mi['sympy']['a']['result']}, (b) {mi['sympy']['b']['result']}",
     rt.get("t12_mi")),
    ("A10 pairs (Δt, 2Δt)", V(dt["A10"]["pass"]), f"post(2Δt) < post(Δt) in {dt['A10']['n_post_dec']}/{dt['A10']['n_pairs']}, avg(2Δt) > "
     f"avg(Δt) in {dt['A10']['n_avg_inc']}/{dt['A10']['n_pairs']}", rt.get("t12_dt")),
]
if sg:
    for key, lab in (("B235_pass", "B2, B3, B5 census (2,000 sets each, both conventions)"), ("B4_pass", "B4 census (2,000 sets, both conventions)")):
        fams = ("B2", "B3", "B5") if key == "B235_pass" else ("B4",)
        rows.append((lab, V(sg[key]), "; ".join(f"{f} {c}: {sg['by'][f'{f} {c}']['n_pass']}/2000" for f in fams for c in ("abs", "rel"))
                     + "; max error of the maximum's position " + g(max((sg['by'][f'{f} rel']['max_pos_rel_err'] or 0) for f in fams)),
                     rt.get("t12_sigma") if key == "B4_pass" else None))
if bl:
    rows.append(("Part C blind search (22 combos)", V(bl["pass"]), f"{bl['total']:,} classifications; flagged "
                 f"{sum(v['flagged'] for v in bl['by'].values())}; persisting {sum(v['persisting'] for v in bl['by'].values())}", rt.get("t12_blind")))
rtot = sum(rt.values())
T = ["# Task 12 — completing Stage 2 (Δt and Σ sweeps) with Stage 3/4 checks: results", "",
     f"Pre-registration `classification/PREREG_t12.md`, commit **{PREREG}**; code and results commit **{CODE}**. Total measured "
     f"script runtime **{rtot:.0f} s** on {env['cpus']} CPUs (Python {env['python']}, mpmath {env['mpmath']}, SymPy {env['sympy']}).", "",
     "| Check | Verdict | Counts / worst errors | Runtime (s) |", "|---|---|---|---|"]
for n, v, m, t in rows:
    T.append(f"| {n} | {v} | {m} | {'' if t is None else f'{t:.0f}'} |")
fails = [n for n, v, _, _ in rows if v == V(False)]
T += ["", "**Pre-registered checks that FAIL:** " + ("; ".join(fails) if fails else "none") + ". Each is diagnosed below.", ""]

# ---------------------------------------------------------------- plain statements
outset = sum(v["persisting"] for v in bl["by"].values()) if bl else None
mixed = sorted({c for f in FAM for m in ("post", "prior", "avg") for c in FAM[f][m]["classes"] if c.startswith("(")})
T += ["## Plain statements", "",
      "- **Is any prediction falsified?** Yes, two, both disclosed in the pre-registration before the run: (1) the prompt's A4 "
      "conjecture \"the D3 excess set is non-empty as Δt → 0 iff ρ > 2\" is false at fixed Π; the onset is ρ > 2 + u, "
      "u = 2ΣΠ/λ² (proved, and confirmed on every census set; counterexamples below); (2) the prompt's A8 quick-check values "
      "(post maximum ≈ 0.166 near Δt ≈ 1; avg crossing F near Δt ≈ 50) are wrong: the maximum is 0.20457 at Δt = 2.4645 and "
      "the crossing is at Δt_E = 100 exactly (by A1–A2). No theorem or proposition-level claim of the prompt is contradicted "
      "otherwise.",
      "- **Did any class outside the predicted sets appear?** "
      + ("No: Part C found no persisting out-of-set class or route disagreement." if outset == 0 else
         f"Part C: {outset} persisting cases (listed below).")
      + (" The A8 census itself recorded mixed classes " + ", ".join(mixed) + " (they define the D-family allowed sets in Part C)." if mixed else ""),
      "- **Open Stage 2 entries:** monotonicity of the optimal M-P prior and avg along Δt (A6; numerical only); M-I optimal "
      "monotonicity along Δt (A9, Numerical result 4.10a; numerical only); exact turning-point counts for the D1–D3 relay "
      "families along Δt (census only, no proof); the number of minima of D1 prior/avg (census only).", ""]

# ---------------------------------------------------------------- prove items
T += ["## [prove] items: outcome", "", "| Item | Outcome | Basis |", "|---|---|---|",
      "| A1 shared excess set | proved | SymPy identities (A1, 5/5) |",
      "| A2 D1 excess set (0, Δt_E) iff G > 2FΠ | proved | tanh lemma, h′ < 0 (series of sinh x − x), lim h = 1/2; numerics 1,000/1,000 |",
      "| A3 D2 excess set iff κ > 2, closed-form Δt_E | proved | identity for L/(2−L); numerics |",
      "| A4 exact D3 condition φ < 1 and s(1−φ)(ρ(1+φ)−2) > 4φ | proved | Q(T) identity; census agreement |",
      "| A4 prompt conjecture (onset iff ρ > 2) | **disproved** | Δt → 0 limit of the condition is ρ − 2 − u; counterexamples below |",
      "| A5 endpoint limits and first-order coefficients | proved | SymPy limits/series; D2 post O(1/Δt) coefficient by the series route (diagnosis) |",
      "| A6 post strictly decreasing | proved | P⁺ = F/(1 + μ), μ increasing in φ and φ/s (SymPy) |",
      "| A6 prior and avg strictly increasing | unresolved | no sign proof found; 0 violations on 400,000 points |",
      "| A7 interior minimum below F, two rays | proved | A5 limits (σ²(G,Π) > F at 0, F from below at ∞) and continuity |",
      "| A9 M-I monotonicity | unresolved | SymPy sign undecided; 0 violations on 400,000 points |",
      "| A10 M-P is not a causal-garbling family along Δt | proved | post strictly decreasing (A6) and avg − F ~ −F/(2λΔt) increasing at large Δt (A5) |",
      "| B1 scaling lemma | proved | SymPy |", "| B2 Σ-independent gain | proved | SymPy signs, limits |",
      "| B3 single maximum iff ρ > 2 at w_M | proved | SymPy identities, parabola argument |",
      "| B4 abs increasing; rel single maximum iff λ′ < λ/2 | proved | SymPy identities, parabola argument; census |",
      "| B5 optimal | proved | SymPy |", ""]
recs = [l for l in sym["lines"] if "[record]" in l]
T += ["Derivations recorded verbatim by `t12_symbolic.py`:", ""] + [f"- `{l.strip()}`" for l in recs] + [""]
T += ["**A7 argument.** For D1 with G > 2FΠ, prior and avg tend to σ²(G, Π) > F as Δt → 0 (A5; σ²(G,Π) > F ⇔ G > 2FΠ) and "
      "to F from below as Δt → ∞ (prior − F = a²(P⁺ − F) and avg − F = (P⁺ − F)s/(2λΔt) with P⁺ → 0). Both are continuous, "
      "so each crosses F and attains an interior minimum below F; for R² between that minimum and F the failure set "
      "contains a neighbourhood of 0 and of ∞ but not the minimiser: two rays (ℓ = u = 1), or (1,1,k) with several minima.", "",
      "**A10 argument and explanation.** If fine ⪯_c coarse (or the reverse) held along Δt, Theorem 4.2 would order every "
      "pointwise optimal error the same way. But post(2Δt) < post(Δt) for all Δt (A6, proved) while avg(2Δt) > avg(Δt) "
      "for all large Δt (avg − F ~ −F/(2λΔt)), so neither direction holds. *Why:* each sample of M-P carries the signal "
      "with variance 1/(ΠΔt), so a longer interval makes every individual sample more precise and the error just after "
      "an update falls; but samples get sparser, so the error grows more between updates and the prior and time-averaged "
      "errors rise.", ""]

# ---------------------------------------------------------------- census tables
T += ["## A8 census (2,000 sets per family, seed 12008)", "", "| Family | Metric | Turning-point histogram | Classes (10 tolerances per set) | Route disagreements |",
      "|---|---|---|---|---|"]
for f in ("D1", "D2", "D3"):
    for m in ("post", "prior", "avg"):
        e = FAM[f][m]
        T.append(f"| {f} | {m} | {e['kinds_hist']} | {e['classes']} | {e['n_disagree_sets']} |")
T += ["", f"A4 shapes of the D3 excess set at R² = F (post): {ex3['shapes']}. Max |E|/scale of the exact condition at the "
      f"classifier's ends: {g(ex3['max_rel_E_at_ends'])}.", ""]
if sg:
    T += ["## Part B census (2,000 sets each, seed 12020)", "", "| Family | Convention | Turning points | Predicted maxima | Classes | Out of set | Disagreements |",
          "|---|---|---|---|---|---|---|"]
    for k, e in sg["by"].items():
        T.append(f"| {k.split()[0]} | {k.split()[1]} | {e['kinds_hist']} | {e['n_pred_max']} | {e['classes']} | {e['n_out_of_set']} | {e['n_disagree_sets']} |")
    T.append("")
if bl:
    T += ["## Part C blind search (seed 12100)", "", "| Combo | Curves | Classifications | Classes | Allowed | Flagged | Persisting |",
          "|---|---|---|---|---|---|---|"]
    for k, e in bl["by"].items():
        T.append(f"| {k} | {e['curves']} | {e['classifications']:,} | {e['classes']} | {', '.join(e['allowed'])} | {e['flagged']} | {e['persisting']} |")
    if bl["persist"]:
        T += ["", "Persisting cases (first 20): " + "; ".join(f"{x['p']} R² = {g(x['R2'], '.6g')}: {x['route_i']} / {x['route_ii']}" for x in bl["persist"])]
    T.append("")

# ---------------------------------------------------------------- synthesis matrix
T += ["## Synthesis-matrix rows", "", "| Sweep | Filter | Metric / convention | Classes | Label |", "|---|---|---|---|---|"]
cls = lambda f, m: ", ".join(sorted(FAM[f][m]["classes"]))
T += [f"| Δt (M-P) | optimal | post | lower ray, Empty | Theorem (A6 post) |",
      f"| Δt (M-P) | optimal | prior, avg | All, upper ray, Empty | Numerical result (monotonicity unresolved) |"]
for f, lab in (("D1", "Proposition (excess set, A2; two rays, A7); other classes Numerical result"),
               ("D2", "Proposition (excess set, A3); other classes Numerical result"),
               ("D3", "Proposition (exact excess condition, A4); other classes Numerical result")):
    for m in ("post", "prior", "avg"):
        T.append(f"| Δt (M-P) | {f} | {m} | {cls(f, m)} | {lab} |")
T += ["| Δt (M-I) | optimal | (a), (b) | All, upper ray, Empty | Numerical result (4.10a; unresolved) |",
      "| Σ | B2 (Σ-independent gain) | absolute | All, upper ray | Theorem |",
      "| Σ | B2 | relative | All, lower ray | Theorem |",
      "| Σ | B3 (Σ-tracking, over-trust ρ) | absolute | upper ray | Theorem |",
      "| Σ | B3 | relative | lower ray, Empty (ρ ≤ 2); lower ray, window, Empty (ρ > 2) | Theorem |",
      "| Σ | B4 (misspecified λ′) | absolute | upper ray | Theorem |",
      "| Σ | B4 | relative | lower ray, Empty (λ′ ≥ λ/2); lower ray, window, Empty (λ′ < λ/2) | Theorem |",
      "| Σ | B5 (optimal) | absolute | upper ray | Theorem |", "| Σ | B5 | relative | lower ray, Empty | Theorem |", ""]

# ---------------------------------------------------------------- diagnoses
T += ["## Diagnoses of failures", ""]
T += ["### Symbolic: A5 'D2 post at Δt → ∞' (attribution: code — the SymPy check route)", "",
      f"`sympy.limit` returns {symd['sympy_limit_again']} for lim Δt(P⁺ − (1−c)²F). Exact route (`t12_symbolic_diag.py`): replace "
      f"e^{{−2λΔt}} by 0 (beyond all orders), set Δt = 1/t and take t → 0: limit `{symd['series_route_limit']}`, difference from "
      f"the pre-registered c[c + 2(1−c)FΠ0]/Π: {symd['series_route_minus_formula']}. mp (dps ≥ 100) on 200 random sets: worst relative "
      f"error {', '.join(f'{k}: {g(v)}' for k, v in symd['mp_worst_rel_err'].items())} — O(1/Δt). The asymptotic used by the classifier is correct.", ""]
if dg:
    pm = dg["A7_prior_missed"]
    T += ["### A7 (attribution: criterion — the pre-registered zero tolerance is too coarse for the prior dip)", "",
          f"In {a7p['n_no_min_below_F']} of {a7p['n_sets']} D1 sets with G > 2FΠ the T10 method found no minimum of the prior below F "
          f"(avg: {a7a['n_no_min_below_F']}). Past Δt_E, prior − F = e^{{−2λΔt}}(P⁺ − F) and d prior/dΔt = e^{{−2λΔt}}·g(Δt), "
          "g = 2λ(F − P⁺) + dP⁺/dΔt; the pre-registered zero tolerance 1e-40·|prior|/θ treats the derivative as zero once "
          "e^{−2λΔt} is below about 1e-40, so the sign change is never seen. Scanning the sign of g instead (`t12_diag.py`) "
          f"finds a minimum in {pm['n_found_by_scaled_derivative']} of the {pm['n_missed']} missed sets (number of minima "
          f"{pm['n_min_hist']}), at λΔt in [{g(pm['lam_dt_range'][0])}, {g(pm['lam_dt_range'][1])}] with relative dip "
          f"(F − prior)/F between 10^{g(pm['log10_rel_dip_range'][0], '.0f')} and 10^{g(pm['log10_rel_dip_range'][1], '.0f')}. "
          "The existence claim (A7, proved above) holds; the dips are real but far below any practical tolerance. "
          f"avg sets missed: {dg['A7_avg_missed']['n_missed']}.", ""]
    ar = dg["A8_regression_actual"]
    T += ["### A8 qualitative regression (attribution: prediction — the prompt's quick-check numbers)", "",
          f"post rises from σ²(0.5, 1) = {g(ar['post_limit_dt0'], '.6g')} to a single maximum {g(ar['post_turns'][0][2], '.6g')} at "
          f"Δt = {g(ar['post_turns'][0][1], '.6g')}; post(1) = {g(ar['post_at_dt1'], '.6g')} (the prompt's 0.166). avg crosses F at "
          f"Δt = {', '.join(g(x, '.10g') for x in ar['avg_crossing_of_F'] if x is not None)} (= Δt_E of A2, exactly 100 to 20 digits), "
          f"then reaches a minimum ({', '.join(f'{k} at {g(t_, '.4g')}: {g(v, '.8g')}' for k, t_, v in ar['avg_turns'])}) and returns "
          f"to F from below. Classes: window at R² = 0.12 ({ar['window_class_at_R2_0.12']}), two rays between the minimum and F "
          f"({ar['two_ray_class_at_mid']}). The qualitative picture of the prompt is right; its numbers are not.", ""]
    a4 = dg["A4_conjecture"]
    T += ["### A4 conjecture (attribution: prediction)", "",
          f"Among the {a4['n_sets']} D3 sets, ρ > 2 in {a4['n_rho_gt_2']}; {a4['n_2_lt_rho_le_2_plus_u']} have 2 < ρ ≤ 2 + u, where "
          f"the conjecture predicts an excess set at small Δt and the exact condition does not. Observed: ρ > 2 without onset in "
          f"{a4['n_rho_gt_2_no_onset']} sets; onset observed {a4['n_onset_obs']} = predicted by ρ > 2 + u {a4['n_onset_pred_(rho>2+u)']}.", ""]

# ---------------------------------------------------------------- implementation notes
T += ["## Implementation notes and deviations", "",
      "1. **Lambdify with common-subexpression elimination** (`cse=True`) for the Δt metrics and derivatives, added before any "
      "pre-registered run: about 5× faster for D3/optimal; values unchanged (checked on the smoke set).",
      "2. **Tolerances for curves without a finite positive critical value** (B3–B5 absolute: monotone 0 → ∞; not covered "
      "by the pre-registration): R² drawn as values of the curve itself at u log-uniform on [1e-20, 1e20] (10 in Part B, "
      "200 in Part C).",
      "3. **A2–A4 numerical checks** use the first 1,000 A8 census sets of each family (seed 12008; the pre-registration gave "
      "no separate seed). A10 pairs continue the A6 stream (seed 12006) after the 1,000 A6 sets.",
      "4. **A8 was restarted** a few minutes into its first run to also save the per-set excess end points (for figure H3); "
      "later the census, Σ sweep and blind search were relaunched as one detached chain after the first launch hit the "
      "session's background time limit. No partial results were used.",
      "5. **A4 membership check:** 201 log-spaced points over λΔt ∈ [1e-20, 1e20] plus midpoints between, and one decade "
      "beyond, the classifier's ends; points within 1e-8 (in log10) of an end skipped.", ""]
T += ["## Figures", "", "`figs/H1_optimal_MP`, `H2_D1_G05`, `H3_onset_maps`, `H4_B3_relative`, `H5_B2_B3_abs_rel` (PNG + PDF).", ""]
for h in ("H1_optimal_MP", "H2_D1_G05", "H3_onset_maps", "H4_B3_relative", "H5_B2_B3_abs_rel"):
    T += [f"![{h}](figs/{h}.png)", ""]
T += ["## Provenance", "", "Results come from separate invocations of the committed scripts (symbolic and A6/A9 directly; A8, Part B, "
      "Part C, diagnosis and figures as one chain). `run_t12.sh` reproduces everything in one pass. Runtime per script (s): "
      + ", ".join(f"{k} {v:.0f}" for k, v in rt.items()) + "."]
open(os.path.join(HERE, "RESULTS_t12.md"), "w").write("\n".join(T) + "\n")
print("\n".join(T[:30]))
