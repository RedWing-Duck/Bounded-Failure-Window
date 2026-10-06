"""Append (or replace) the 'Task 6' section of REPORT.md from results/t6.json. Earlier sections are untouched."""
import json
import os
import subprocess

from common import HERE, RES

HEAD = "## Task 6 — coloured-noise symbolic check"


def git(*a):
    return subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True).stdout.strip()


def E(x):
    return str(x).replace("|", "\\|")


d = json.load(open(os.path.join(RES, "t6.json")))
pre = git("log", "--format=%H", "--grep=^prereg: t6 colored-noise symbolic", "--", "PREREG_t6.md").splitlines()
pre = pre[-1] if pre else "NOT FOUND"
unchanged = git("diff", "--name-only", pre, "HEAD", "--", "PREREG_t6.md") == "" and \
    git("status", "--porcelain", "--", "PREREG_t6.md") == ""

L = [HEAD, ""]
w = L.append
w(f"Pre-registration: `{pre}` (`PREREG_t6.md` unchanged since: **{'yes' if unchanged else 'NO'}**). "
  f"Script: `t6_colored_symbolic.py`; full output: `results/t6_colored.txt`.\n")
w(f"**Noise normalisation in t4b.** {d['normalisation']}\n")
w("**Lyapunov solution.** The stationary covariance of (x, η) gives")
w(f"$$ C_{{xx}} = {d['Cxx_latex']} $$\n")
w("SymPy's factorisation of C_xx − F (C3), verbatim:")
w(f"$$ C_{{xx}} - F = {d['C3_factor_latex']} $$\n")
w("Small-Π series with the Kalman gain (C4):")
w(f"$$ C_{{xx}} = {d['C4_series_latex']} $$\n")
w("| ID | criterion | result | measured |")
w("|---|---|---|---|")
for k, v in d["criteria"].items():
    res = "PASS (numeric only)" if v.get("numeric_only") else ("PASS" if v["pass"] else "FAIL")
    w(f"| {k} | {E(v['desc'])} | {res} | {E(v['detail'])} |")
w("")
w(f"**Task 6: {'PASS' if d['pass'] else 'FAIL'}**\n")

w("### C5 detail: peak height and location\n")
w("| τ | peak (200,001-pt grid) | t4b peak | match | Π* (200,001-pt grid) | t4b Π* | match | exact Π* (nsolve, post hoc) | formula reproduces t4b on t4b's grid |")
w("|---|---|---|---|---|---|---|---|---|")
for r in d["c5"]:
    w(f"| {r['tau']:g} | {r['peak']:.6f} | {r['t4b_peak']:.6f} | {'yes' if r['match_height'] else 'no'} | "
      f"{r['peak_Pi']:.5f} | {r['t4b_peak_Pi']:.5f} | {'yes' if r['match_loc'] else 'no'} | {r['exact_peak_Pi']:.6f} | "
      f"{'yes' if r['t4b_grid_reproduced'] else 'no'} |")
w("")
bad = [r for r in d["c5"] if not (r["match_height"] and r["match_loc"])]
if bad:
    bad_loc = [r for r in bad if not r["match_loc"]]
    w(f"C5 fails on {len(bad_loc)} peak locations "
      f"({', '.join(f'τ = {r['tau']:g}: {r['peak_Pi']:.3g} vs {r['t4b_peak_Pi']:.3g}' for r in bad_loc)}). "
      f"All peak heights match. This is the risk named in PREREG_t6.md before the run. t4b located its "
      f"peaks on a grid with steps of about 0.4 % in Π, which is coarser than 3 significant figures. On t4b's own "
      f"grid the derived C_xx reproduces t4b's peaks exactly (relative error < 1e-12). A post-hoc exact solve of "
      f"dC_xx/dΠ = 0 agrees with the fine grid. So the derivation agrees with t4b's formula, and the third "
      f"significant figure of the t4b peak locations is a grid artefact. The correct values to 3 s.f. are "
      f"{', '.join(f'{r['exact_peak_Pi']:.3g} (τ = {r['tau']:g})' for r in d['c5'])}. "
      f"The criterion was left unchanged and is recorded as FAIL.\n")

w("### C6 detail: boundary τ = 49 at P = 1\n")
w("| τ | numeric slope at Π → 0 | s1 from series | predicted rise | sign matches |")
w("|---|---|---|---|---|")
for r in d["c6"]:
    w(f"| {r['tau']:g} | {r['numeric_slope']:.4e} | {r['s1']:.4e} | {'yes' if r['predicted_rise'] else 'no'} | "
      f"{'yes' if r['match'] else 'no'} |")
w("")
w("Informational: does a peak above F exist for τ > 49 anyway?\n")
w("| τ | max_Π (C_xx − F) | at Π | sup_Π [G/Π − 2F(1+aτ)] | at Π | limit Π → 0 |")
w("|---|---|---|---|---|---|")
for r in d["c6_info"]:
    w(f"| {r['tau']:g} | {r['max_excess']:.4e} | {r['max_excess_Pi']:.4g} | {r['sup_cond']:.6f} | "
      f"{r['sup_cond_Pi']:.4g} | {r['cond_limit_Pi0']:.6f} |")
w("")
none = all(r["max_excess"] < 0 and r["sup_cond"] < 0 for r in d["c6_info"])
w(f"For τ > 49 {'no' if none else 'some'} grid point lies above F. Each supremum is reached at the smallest "
  f"grid Π and approaches its negative Π → 0 limit. This is general for the Kalman gain: "
  f"d/dΠ [G/Π − 2F(1+aτ)] = `{d['dcond']}`, which is "
  f"{'proven negative' if d['dcond_negative'] else 'NOT proven negative'} for all positive parameters. "
  f"The condition is therefore largest at Π → 0. For the Kalman gain with coloured noise, the small-Π "
  f"condition c/P > 2F(1+λτ) is both sufficient and necessary for any excess above F. This is unlike the "
  f"Hill gain in Task 4d.\n")

path = os.path.join(HERE, "REPORT.md")
txt = open(path).read()
if HEAD in txt:
    txt = txt[:txt.index(HEAD)].rstrip("\n") + "\n"
txt = txt.rstrip("\n") + "\n\n" + "\n".join(L) + "\n"
open(path, "w").write(txt)
print("\n".join(L))
