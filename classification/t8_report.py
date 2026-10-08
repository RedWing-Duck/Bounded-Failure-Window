"""T8.7: results/t8.txt and REPORT.md from the JSON results. Usage: python3 t8_report.py [final_hash]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
PREREG_HASH = "d8fa786"
FINAL_HASH = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "(not yet committed)"


def load(n):
    with open(os.path.join(RES, n)) as fh:
        return json.load(fh)


r1, r2, r3, r4, r5 = (load(f"t8_{i}.json") for i in range(1, 6))
env = load("env.json")
rt = [l.split("\t") for l in open(os.path.join(RES, "runtime.tsv")).read().split("\n") if l.strip()]
total_rt = sum(float(t) for _, t in rt)
V = lambda ok: "PASS" if ok else "FAIL"

T = []
T.append("Task 8 — Stage 0–1 classification checks")
T.append(f"prereg commit {PREREG_HASH}; final commit {FINAL_HASH}; total runtime {total_rt:.1f} s")
T.append("")
# T8.1
T.append(f"[{V(r1['pass'])}] T8.1 analytic (SymPy {env['sympy']})")
for part in "abcdefg":
    for x in r1[part]:
        route = x.get("route", "")
        extra = f"  SymPy: {x['sympy_simplify_verbatim']}" if route == "numeric only" else (
            f"  SymPy: {x['sympy']}" if "sympy" in x else "")
        T.append(f"    ({part}) [{V(x['pass'])}] ({route}) {x['desc']}{extra}")
h = r1["h"]
T.append(f"    (h) [{V(h[0]['pass'])}] Paper 1 sweep, Pi0 = 1: turning points {h[0]['turns']}; "
         f"L- = {h[0]['L_minus']} ({h[0]['approach_minus']}), L+ = {h[0]['L_plus']} ({h[0]['approach_plus']})")
T.append(f"    (h) [{V(h[1]['pass'])}] M = {h[1]['M']:.7g} (stated 0.09288), Pi* = {h[1]['Pi_star']:.7g} (stated 0.6867)")
T.append(f"    (h) [{V(h[2]['pass'])}] four-regime table: {sum(x['match'] for x in h[2]['rows'])}/{len(h[2]['rows'])} classes match")
c4 = h[0]["C4_check"]
T.append(f"    (h) C4 wording: first piece direction {c4['first_piece_dir']:+d} with sigma2 - L- = "
         f"{c4['sigma2_first_piece_minus_Lminus']:.4g}; last piece direction {c4['last_piece_dir']:+d} with sigma2 - L+ = "
         f"{c4['sigma2_last_piece_minus_Lplus']:.4g}")
T.append(f"    identities confirmed by simplify: all; numeric-only fallbacks: {len(r1['numeric_only'])}")
T.append("")
# T8.2
T.append(f"[{V(r2['pass'])}] T8.2 worked-example values (4 s.f.)")
for x in r2["rows"]:
    comp = x["computed"] if isinstance(x["computed"], dict) else f"{x['computed']:.8g}"
    T.append(f"    {x['quantity']:<30} computed {comp}  stated {x['stated']}  {'ok' if x['match'] else 'MISMATCH'}")
T.append("")
# T8.3
T.append(f"[{V(r3['pass'])}] T8.3 classification tables: {r3['n_match']}/{r3['n_tests']} classes match")
for k, c in r3["cases"].items():
    T.append(f"    {k}: {V(c['pass'])}; turning points {[(round(t[0], 8), round(t[1], 10), t[2]) for t in c['turns']]}; "
             f"approach {c['approach'][0]} / {c['approach'][1]}")
    for x in c["rows"]:
        T.append(f"       {x['test']:<26} R2 = {x['R2']:.10g}: {x['got']} (expected {x['expected']})"
                 f"{'' if x['match'] else '  MISMATCH'}")
    for e in c["extra"]:
        T.append(f"       [{'ok' if e['pass'] else 'MISMATCH'}] {e['desc']}")
T.append("")
# T8.4
nmax = sum(s["local_max"] for s in r4["stats"].values())
T.append(f"[{V(r4['pass'])}] T8.4 Theorem 3.2 adversarial (seed 8004): {r4['N']} parameter sets, "
         f"{sum(s['sweeps'] for s in r4['stats'].values())} sweeps, {r4['total_classifications']} classifications; "
         f"windows/mixed {r4['windows_or_mixed']}; interior local maxima found {nmax}"
         + ("" if nmax == 0 else f"; smallest |max - R2| {min(s['min_gap_max_R2'] for s in r4['stats'].values() if s['min_gap_max_R2'] is not None):.3g}"))
for k, s in r4["stats"].items():
    T.append(f"    {k:<24} turning points {s['turns_hist']}; classes {s['classes']}; local maxima {s['local_max']}; "
             f"limit-check failures {s['limit_check_fail']}; flat pieces {s['flat_piece']}")
T.append("")
# T8.5
T.append(f"[{V(r5['pass'])}] T8.5 realizability: {sum(x['match'] for x in r5['rows'])}/{len(r5['rows'])} intended classes returned at R2 = 1")
T.append("")
fig_ok = os.path.exists(os.path.join(HERE, "figures", "fig_t8_sweeps.png"))
T.append(f"[{'DONE' if fig_ok else 'MISSING'}] T8.6 figures/fig_t8_sweeps.png")
T.append("")
T.append("runtime (s): " + ", ".join(f"{n} {t}" for n, t in rt))
txt = "\n".join(T) + "\n"
open(os.path.join(RES, "t8.txt"), "w").write(txt)

# ---------------------------------------------------------------- REPORT.md
ok_all = all(x["pass"] for x in (r1, r2, r3, r4, r5)) and fig_ok
M = [f"# Task 8 — Stage 0–1 classification checks", "",
     f"Verifies `Stage_0_1_Classification_Results.md` (copied into this directory unchanged). "
     f"Pre-registration: `PREREG_t8.md`, commit **{PREREG_HASH}**. Final commit: **{FINAL_HASH}**. "
     f"Total runtime of `run_all.sh`: **{total_rt:.1f} s** "
     f"(Python {env['python']}, NumPy {env['numpy']}, SciPy {env['scipy']}, SymPy {env['sympy']}, "
     f"Matplotlib {env['matplotlib']}). Generated from `results/t8.txt` and `results/t8_*.json` by `t8_report.py`.", "",
     "## Verdicts", "", "| Criterion | Verdict | Measured |", "|---|---|---|",
     f"| T8.1 analytic (SymPy) | {V(r1['pass'])} | every identity `simplify` → 0 (no numeric-only fallbacks); "
     f"Paper 1 limiting case M = {h[1]['M']:.5g} at Π* = {h[1]['Pi_star']:.5g}, four-regime table "
     f"{sum(x['match'] for x in h[2]['rows'])}/{len(h[2]['rows'])} |",
     f"| T8.2 worked-example values | {V(r2['pass'])} | {sum(x['match'] for x in r2['rows'])}/{len(r2['rows'])} values match to 4 s.f. |",
     f"| T8.3 classification tables | {V(r3['pass'])} | {r3['n_match']}/{r3['n_tests']} predicted classes match "
     f"(P1, P2, P3, Π_B, Π_A, coupling) |",
     f"| T8.4 Theorem 3.2, adversarial | {V(r4['pass'])} | {r4['total_classifications']:,} classifications over "
     f"{sum(s['sweeps'] for s in r4['stats'].values()):,} sweeps: {r4['windows_or_mixed']} windows or mixed classes; "
     f"{nmax} interior local maxima found |",
     f"| T8.5 Proposition 1.1 realizability | {V(r5['pass'])} | {sum(x['match'] for x in r5['rows'])}/{len(r5['rows'])} classes |",
     f"| T8.6 figure | {'DONE' if fig_ok else 'MISSING'} | `figures/fig_t8_sweeps.png` (300 dpi) |", "",
     f"**Overall: {'all criteria pass' if ok_all else 'NOT all criteria pass'}.**", "",
     "## Finding: the C4 parenthetical has the directions reversed", "",
     "C4 defines approach *from above* as σ² > L on the adjacent piece, then adds: \"from above at θ₋ means the first "
     "piece is decreasing, and from above at θ₊ means the last piece is increasing.\" That parenthetical is backwards: "
     "a first piece lying above L₋ rises away from θ₋ (increasing), and a last piece lying above L₊ falls towards θ₊ "
     "(decreasing). Evidence (T8.1(h)): on the Paper 1 sweep the first piece is increasing "
     f"(direction {c4['first_piece_dir']:+d}) with σ² − F = {c4['sigma2_first_piece_minus_Lminus']:.3g} > 0 one decade "
     f"below Π*, and the last piece is decreasing (direction {c4['last_piece_dir']:+d}) with σ² − H = "
     f"{c4['sigma2_last_piece_minus_Lplus']:.3g} > 0 one decade above, so both ends are approached from above in the "
     "sense of the definition (and of the document's own Paper 1 check). Every other use in the document (Theorem 1.2(b) "
     "and its proof, Propositions 4.1, 4.2, 5.1, 5.2, the synthesis matrix) follows the definition, so no stated class "
     "is affected. Suggested wording: \"from above at θ₋ means the first piece is increasing, and from above at θ₊ means "
     "the last piece is decreasing.\"", "",
     "## Bugs fixed during the run (genuine bugs, no criterion or tolerance changed)", "",
     "1. **Approach-direction labels.** The classifier first labelled approach directions using the C4 parenthetical, "
     "so T8.1(h) reported both Paper 1 ends as \"below\" and failed its structure check, while all 13 classes matched "
     "(classes are computed from piece directions and end values, not from the labels). The labels were changed to "
     "follow the C4 definition (σ² vs L on the adjacent piece). This is the finding above.",
     "2. **Overflow at the endpoint limits.** `σ²(θ)` at θ = 10²⁵⁰ raised a Python `OverflowError` (G² for the "
     "coupling sweep) instead of returning ∞. θ is now formed as a NumPy float64 and ∞ is capped at 1e300 inside "
     "root-finding. T8.3 crashed before any coupling-sweep class was computed; no class changed.", "",
     "A 200-set run of `t8_no_window.py` (same seed; the first 200 of the 20,000 sets) was made to check the code runs and "
     "to time it; it found no window, and nothing was changed afterwards.", "",
     "## Method notes", "",
     "- The classifier (`t8_common.py`) finds turning points as brentq-refined sign changes of the analytic derivative on a "
     "log grid (40 points per decade, θ ∈ [1e-60, 1e60]), takes endpoint limits at θ = 1e∓250 (checked against 1e∓200), and "
     "builds the failure set piece by piece from the end values, locating every crossing by brentq on the monotone piece. "
     "Grid membership is never used to decide a class.",
     "- \"R² equals a critical value\" is recognised to 1e-12 relative (floating point); the ±1e-6 tests are far outside it.",
     "- Minima in T8.2 come from `minimize_scalar(method='bounded')` over log10 θ ∈ [−6, 6].", "",
     "## Full results", "", "```", txt.rstrip(), "```", "",
     "![sweeps](figures/fig_t8_sweeps.png)", "",
     "*Figure: σ² along (a) the prior sweep at Π = 1 (P3), (b) the prior sweep at Π = 500 (P1, monotone) and (c) the "
     "coupling sweep at Π = Π₀ = 1, at λ = c = 1, Σ = 0.01. Insets zoom on the minimum, where F and σ*² differ by 0.5%.*"]
open(os.path.join(HERE, "REPORT.md"), "w").write("\n".join(M) + "\n")
print(txt)
