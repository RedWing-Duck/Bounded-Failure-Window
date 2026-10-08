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
     f"`classification/PREREG_t10.md`, commit **{PREREG}**; code and results commit **{CODE}**. Total runtime of `run_t10.sh`: "
     f"**{sum(rt.values()):.0f} s** on {env['cpus'] if env else '?'} CPUs (Python {env['python'] if env else '?'}, mpmath "
     f"{env['mpmath'] if env else '?'}, SymPy {env['sympy'] if env else '?'}).", "",
     "| Check | Verdict | Counts / worst errors | Runtime (s) |", "|---|---|---|---|"]
for n, v, m, t in rows:
    T.append(f"| {n} | {v} | {m} | {'' if t is None else f'{t:.0f}'} |")
open(os.path.join(HERE, "RESULTS_t10.md"), "w").write("\n".join(T) + "\n")
print("\n".join(T))
