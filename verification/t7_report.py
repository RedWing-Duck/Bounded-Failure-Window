"""T7.6: write results/t7.txt and append (or replace) the 'Task 7 — revision checks' section of REPORT.md.
Everything is read from results/t7_*.json and git; earlier REPORT.md sections are untouched."""
import json
import os
import subprocess

from common import HERE, RES

HEAD = "## Task 7 — revision checks"


def J(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


def git(*a):
    return subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True).stdout.strip()


def E(x):
    return str(x).replace("|", "\\|")


t1, t2, t3, t4, rt = J("t7_1.json"), J("t7_2.json"), J("t7_3.json"), J("t7_4.json"), J("t7_runtime.json")
pre = git("log", "--format=%h", "--abbrev=7", "--grep=^prereg: t7 revision checks", "--", "PREREG_t7.md").splitlines()
pre = pre[-1] if pre else "NOT FOUND"
pre_unchanged = pre != "NOT FOUND" and git("diff", "--name-only", pre, "HEAD", "--", "PREREG_t7.md") == "" and \
    git("status", "--porcelain", "--", "PREREG_t7.md") == ""
fin = git("log", "-1", "--format=%h", "--abbrev=7", "--grep=^t7: revision checks and figures")
fin = fin or "not yet committed"

# ------------------------------------------------------------- criterion rows
rows = []
for k, v in t1["criteria"].items():
    if "verdict" in v and k in ("T7.1a", "T7.1b", "T7.1c", "T7.1d"):
        m = f"{v['verdict']}; numeric check at 20 rational points: max rel err {v['numeric_max_rel']:.1e}"
        if v.get("residual"):
            m += f"; SymPy residual: {v['residual']}"
    elif k == "T7.1e":
        m = (f"algebraic identity {v['algebraic']['verdict']}; prefactors positive: "
             f"{all(v['positive_factors'].values())}; {v['n_sets']:,} exact rational sets: {v['mismatches']} mismatches "
             f"({v['n_excess_true']} with M > F)")
    elif k == "T7.1f":
        m = (f"difference identity {v['difference_identity']['verdict']}; gap identity {v['gap_identity']['verdict']}; "
             f"gap > 0 proven: {v['gap_positive']}; {v['n_sets']:,} float64 sets: max ratio {v['max_ratio']:.9f}, "
             f"{v['n_ratio_ge_1']} with ratio >= 1; L* in (a) recovers Riccati M: {v['riccati_consistent_with_a']}")
    else:
        m = (f"Δt⁰ term = {v['coef0']}; Δt¹ term = {v['coef1']} ({v['coef1_identity']['verdict']}); "
             f"Δt² term = {v['coef2']}")
    rows.append((k, v["desc"], "PASS" if v["pass"] else "FAIL", m))
c2 = t2["criteria"]
rows.append(("T7.2a", c2["T7.2a"]["desc"], c2["T7.2a"]["verdict"],
             f"positive root p = {c2['T7.2a']['positive_root']}; pΠ = G*: {c2['T7.2a']['pPi_eq_Gstar']['verdict']}; "
             f"p = σ*²: {c2['T7.2a']['p_eq_sigma_star']['verdict']}; p = (2) at G*: {c2['T7.2a']['p_eq_closed_form_at_Gstar']['verdict']}"))
rows.append(("T7.2b", c2["T7.2b"]["desc"], c2["T7.2b"]["verdict"],
             "; ".join(f"κ={r['kappa']}: {r['M_over_F']:.5f}" for r in c2["T7.2b"]["rows"])))
rows.append(("T7.2c", c2["T7.2c"]["desc"], c2["T7.2c"]["verdict"],
             f"Π₀ = {c2['T7.2c']['Pi_0']}, Π* = {c2['T7.2c']['Pi_star']}, M = {c2['T7.2c']['M']}"))
rows.append(("T7.2d", c2["T7.2d"]["desc"], c2["T7.2d"]["verdict"],
             f"κ = {c2['T7.2d']['kappa_root']:.12f} (|err| {c2['T7.2d']['abs_err']:.1e}); M increasing in κ: {c2['T7.2d']['monotone']}"))
h = c2["T7.2e"]["hill"]
rows.append(("T7.2e", c2["T7.2e"]["desc"], c2["T7.2e"]["verdict"],
             "; ".join(f"Π₀={float(k):g}: max(σ²−F) = {v['max_direct']:.4e} at Π = {v['at_Pi_direct']:.4g}" for k, v in h.items())))
rows.append(("T7.3", "closed-form Task 4a peaks match reported 0.01075, 0.02224, 0.1837 (3 s.f.)",
             "PASS" if t3["pass"] else "FAIL",
             "; ".join(f"k={r['k']}: {r['peak_closed']:.6f} vs {r['reported']:.6f}" for r in t3["rows"])))
rows.append(("T7.4", "figures: 300 dpi, 4.7 in wide, no titles", "PASS" if t4["pass"] else "FAIL",
             "; ".join(f"{k}: {v['px'][0]}×{v['px'][1]} px, {v['dpi']} dpi" for k, v in t4["files"].items())
             + f"; titles found: {sum(len(x) for x in t4['titles_found'].values())}"))
if rt:
    rows.append(("T7.5", "full run_all.sh (incl. Task 7) completes", "PASS" if rt["pass"] else "FAIL",
                 f"exit code {rt['exit_code']}; wall time {rt['wall_s']:.1f} s"))
else:
    rows.append(("T7.5", "full run_all.sh (incl. Task 7) completes", "NOT RUN", "results/t7_runtime.json missing"))
all_ok = all(r[2].startswith("PASS") for r in rows)

# ------------------------------------------------------------- results/t7.txt
T = []
T.append("TASK 7 — REVISION CHECKS")
T.append(f"prereg {pre}")
T.append("")
for k, d, res, m in rows:
    T.append(f"[{res}] {k}: {d}\n    {m}")
T.append(f"\nTask 7 overall: {'PASS' if all_ok else 'FAIL'}\n")
f = t1["criteria"]["T7.1f"]
T.append("T7.1(d) sympy.factor(M − F), verbatim:")
T.append("    " + t1["criteria"]["T7.1d"]["factor"])
T.append("    LaTeX: " + t1["criteria"]["T7.1d"]["factor_latex"])
T.append("T7.1(f) difference (M + rs)(M + 2r) − 2rs(M + r), expanded by SymPy:")
T.append("    LaTeX: " + f["difference_latex"] + "  =  " + f["difference_rhs_latex"])
T.append("")
T.append(t3["spec"])
T.append("\n".join(t3["check_lines"]))
T.append("")
T.append(t3["explanation"])
T.append("")
T.append("T7.2(b) table (κ, Π₀, Π*, M, M/F):")
for r in c2["T7.2b"]["rows"]:
    T.append(f"    {r['kappa']:>4} {r['Pi_0']:>9.4g} {r['Pi_star']:>9.5g} {r['M']:.6f} {r['M_over_F']:.5f}")
if rt:
    T.append("\nT7.5 runtime of the full run_all.sh in a fresh copy:")
    for p in rt["per_script"]:
        T.append(f"    {p['script']:<24} {p['seconds']:8.1f} s")
    T.append(f"    {'total wall time':<24} {rt['wall_s']:8.1f} s (sum of scripts {rt['sum_scripts_s']:.1f} s)")
    T.append(f"    regenerated results identical to committed (ignoring runtimes): {len(rt['json_identical'])}/"
             f"{len(rt['json_identical']) + len(rt['json_differ']) + len(rt['json_missing'])} json files"
             f"{'; differ: ' + ', '.join(rt['json_differ']) if rt['json_differ'] else ''}; "
             f"figures byte-identical: {rt['figures_identical']}/{rt['figures_total']}")
txt = "\n".join(T) + "\n"
open(os.path.join(RES, "t7.txt"), "w").write(txt)

# ------------------------------------------------------------- REPORT.md section
L = [HEAD, ""]
w = L.append
w(f"Pre-registration: `{pre}` (`PREREG_t7.md` unchanged since: **{'yes' if pre_unchanged else 'NO'}**). "
  f"Task 7 scripts and results: `{fin}` (this section is committed in the commit after it). "
  f"Full output: `results/t7.txt`; Task 4a specification: `results/t7_4a_spec.txt`.\n")
w("Notation: the prior precision P is now Π₀; κ = (c/Π₀)/F.\n")
w("| ID | criterion | result | measured |")
w("|---|---|---|---|")
for k, d, res, m in rows:
    w(f"| {k} | {E(d)} | {res} | {E(m)} |")
w("")
w(f"**Task 7: {'PASS' if all_ok else 'FAIL'}**\n")
w("T7.1(d), SymPy's factorisation of M − F (verbatim):")
w(f"$$ M_L - F = {t1['criteria']['T7.1d']['factor_latex']} $$\n")
w("T7.1(f), the difference that proves L*/(2−L*) < ½FΠ_d:")
w(f"$$ (M + rs)(M + 2r) - 2rs(M + r) = {f['difference_latex']} = {f['difference_rhs_latex']} $$\n")
dec = t3["decomposition"]
cb = dec["contributions"]
w("### Task 4a, specified\n")
w(f"The Task 4a grid variable is a per-sample precision, Π_d = 1/var(v). It maps to the continuous precision by "
  f"Π = Π_d/Δt, with Δt = 0.05. The \"slope ratio\" is the numerical initial gain slope K(ε)/ε divided by F. That equals the "
  f"continuous κ exactly, because L = GΔt and Π_d = ΠΔt. The reported variances were posterior. The closed form "
  f"reproduces all three reported peaks (largest relative difference "
  f"{max(abs(r['rel_diff']) for r in t3['rows']):.1e}).\n")
w(f"The ratio-100 peak ({t3['rows'][-1]['reported']:.4f}) is {t3['rows'][-1]['reported'] / dec['cont_bw'][0]:.2f}× the continuous "
  f"κ = 100 peak ({dec['cont_bw'][0]:.4f}). The mapping is exact: implied κ = {dec['kappa_cont']:.4f}. Most of the gap, "
  f"{cb['gain shape: continuous KB-type gain vs Bayesian-weight gain, same kappa']:+.4f} of {dec['total']:+.4f}, is a "
  f"**gain-shape** effect. As Δt → 0 the 4a filter's gain becomes the Kalman–Bucy gain of the assumed model, "
  f"−λ + sqrt(λ² + 2κΣΠ), whose continuous peak is {dec['cont_kb'][0]:.4f}. That gain keeps growing instead of saturating "
  f"at c. Δt adds the remaining {cb['dt on the 4a gain family (discrete posterior at dt=0.05 - continuous)']:+.4f}. Prior vs "
  f"posterior ({cb['prior vs posterior at dt=0.05 (posterior - prior)']:+.4f}) is itself a finite-Δt effect that vanishes "
  f"as Δt → 0. On the paper's own Bayesian-weight relay, Δt = 0.05 changes the peak by only "
  f"{cb['dt on the paper' + chr(39) + 's Bayesian-weight relay (discrete posterior - continuous)']:+.4f}. Only the onset "
  f"condition (κ > 2) transfers from Task 4a to the paper; the peak heights do not.\n")
w("### Figures (revision)\n")
for k in t4["files"]:
    w(f"- `figures/{k}`")
w("")
if rt:
    w(f"**Runtime (T7.5).** The full `run_all.sh`, Task 7 included, took {rt['wall_s']:.1f} s wall time in a fresh copy "
      f"(Task 7 scripts: {sum(p['seconds'] for p in rt['per_script'] if p['script'].startswith('t7_')):.1f} s). "
      f"{len(rt['json_identical'])} of "
      f"{len(rt['json_identical']) + len(rt['json_differ']) + len(rt['json_missing'])} regenerated results files "
      f"matched the committed ones apart from timings, and {rt['figures_identical']}/{rt['figures_total']} figures were "
      f"byte-identical.\n")

path = os.path.join(HERE, "REPORT.md")
rep = open(path).read()
if HEAD in rep:
    rep = rep[:rep.index(HEAD)].rstrip("\n") + "\n"
rep = rep.rstrip("\n") + "\n\n" + "\n".join(L) + "\n"
open(path, "w").write(rep)
print(txt)
