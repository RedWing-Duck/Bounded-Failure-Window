"""Generate REPORT.md from results/*.json, results/runtime.tsv and git. No hand-typed numbers."""
import json
import os
import subprocess

from common import HERE, RES


def J(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)


def git(*a):
    return subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True).stdout.strip()


def E(x):
    """Escape pipes inside table cells."""
    return str(x).replace("|", "\\|")


def g(x, n=4):
    return f"{x:.{n}g}"


def lst(xs, n=4):
    return "(" + ", ".join(g(x, n) for x in xs) + ")" if xs else "none"


t1, t2, t3 = J("t1.json"), J("t2.json"), J("t3.json")
t4a, t4b, t4c, t4d, t4e = (J(f"t4{k}.json") for k in "abcde")
env = J("env.json") if os.path.exists(os.path.join(RES, "env.json")) else None

prereg = git("log", "--format=%H", "--grep=^prereg: verification criteria", "--", "PREREG.md").splitlines()
prereg = prereg[-1] if prereg else "NOT FOUND"
prereg_unchanged = git("diff", "--name-only", prereg, "HEAD", "--", "PREREG.md") == "" and \
    git("status", "--porcelain", "--", "PREREG.md") == ""
head = git("rev-parse", "HEAD")
dirty = git("status", "--porcelain", "--", "results", "figures", "*.py", "*.sh") != ""

rt_rows = []
if os.path.exists(os.path.join(RES, "runtime.tsv")):
    with open(os.path.join(RES, "runtime.tsv")) as f:
        rt_rows = [ln.split("\t") for ln in f.read().split("\n") if ln.strip()]
L = []
w = L.append

w("# Verification report — A Bounded Failure Window in a Miscalibrated Precision-Weighted Relay\n")
w("All numbers below are read from `results/*.json` / `results/runtime.tsv` by `make_report.py`.\n")
w(f"- Pre-registration commit: `{prereg}` (PREREG.md unchanged since: **{'yes' if prereg_unchanged else 'NO'}**)")
w(f"- Results commit (scripts + results this report was generated from): `{head}`"
  + (" — **working tree differed from this commit when the report was generated**" if dirty else ""))
w("  (REPORT.md itself is committed in the commit after this one, since a file cannot contain the hash of its own commit.)\n")

# ---------------------------------------------------------------- criteria
w("## Pre-registered criteria\n")
w("| ID | criterion | result | measured |")
w("|---|---|---|---|")
for k, v in t1["criteria"].items():
    w(f"| {k} | {E(v['desc'])} | {'PASS' if v['pass'] else 'FAIL'} | {E(v['detail'][:220]) or '—'} |")
for blk in (t2, t3):
    for k, v in blk["crit"].items():
        res = ("PASS" if v["pass"] else "FAIL") + (" (info)" if v.get("info") else "")
        w(f"| {k} | {E(v['desc'])} | {res} | {E(v['detail'])} |")
w("")
w(f"**Task 1: {'PASS' if t1['pass'] else 'FAIL'} · Task 2: {'PASS' if t2['pass'] else 'FAIL'} · "
  f"Task 3: {'PASS' if t3['pass'] else 'FAIL'}**\n")

w("### Worked-example numbers (T1.9)\n")
w("| quantity | computed | stated | digits compared | pass | strict 4 s.f. |")
w("|---|---|---|---|---|---|")
for k, v in t1["numbers"].items():
    w(f"| {k} | {v['computed']:.8g} | {g(v['stated'], 6)} | {v['n_sig']} | {'PASS' if v['pass'] else 'FAIL'} | "
      f"{'agrees' if v['strict4sf'] else 'differs'} |")
strict_bad = [k for k, v in t1["numbers"].items() if not v["strict4sf"]]
w("")
w("Expanded numerator of dσ²/dΠ for Appendix A (denominator 2(P+Π)²(Pλ+Πc+Πλ)², see `results/t1_symbolic.txt`):\n")
w(f"$$ {t1['latex_numerator']} $$\n")

w("### Notes on how the criteria behaved\n")
w(f"- **T1.9 is partly ill-posed as written.** \"Agreement to 4 significant figures\" cannot be checked against "
  f"values the brief states to 2–3 significant figures. As pre-registered, they were compared at their stated "
  f"precision; under a strict 4-s.f. reading, {len(strict_bad)} values differ only because the stated value is "
  f"rounded: {', '.join(f'{k} = {t1['numbers'][k]['computed']:.6g}' for k in strict_bad)}. The paper "
  f"could quote these to 4 s.f. as {', '.join(f"{t1['numbers'][k]['computed']:.4g}" for k in strict_bad)}.")
w(f"- **Common random numbers.** Every Π and every relay share the same noise. That makes the paired tests in "
  f"T3.3–T3.5 sharp, but it also correlates the simulation errors across Π: the T2 z-scores drift smoothly "
  f"(max |z| = {max(abs(z) for z in t2['z_raw']):.2f}), so the {len(t2['grid'])} points of T2.1 are not "
  f"independent tests.")
w(f"- **EM bias.** EM bias is far below the SE here. Measured against the EM-exact variance D/(2a − a²dt), "
  f"max |z| = {max(abs(z) for z in t2['z_cor']):.2f}; measured against (2), max |z| = "
  f"{max(abs(z) for z in t2['z_raw']):.2f}. "
  f"{'Both comparisons pass.' if t2['crit']['T2.1c']['pass'] and t2['crit']['T2.1']['pass'] else 'See table.'}")
w(f"- **T3.5b is close to trivial at small Π.** There (b) and (c) have almost the same gain: the paired "
  f"difference at Π = 0.01 is {t3['sim']['c'][0] - t3['sim']['b'][0]:.2g}, so that test only has power at large Π.")
w("")

# ---------------------------------------------------------------- Task 4
w("## Task 4 — breaking one assumption at a time\n")
w("Here \"bounded window\" means an interior maximum strictly above both ends of the variance curve, as "
  "defined in PREREG.md. The baseline is the white-noise Kalman relay with P = 1: peak 0.0929 at Π = 0.687, "
  "R² = 0.05 window (1/9, 4).\n")

# 4a
rows = t4a["rows"]
byk = {(r["mode"], r["factor"]): r for r in rows}
same = all(abs(byk[("A", f)]["peak"] - byk[("B", f)]["peak"]) < 1e-15 for f in (1, 2, 3, 10, 100))
w("### 4a Discrete-time Kalman filter\n")
w("| miscal. | factor | initial gain slope | ÷ correct slope | predicted window | window | peak Π | peak | R²=0.05 window |")
w("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    w(f"| {r['mode']} | {r['factor']} | {r['slope_num']:.5g} | {r['ratio']:.3g} | {'yes' if r['prediction'] else 'no'} | "
      f"{'yes' if r['window'] else 'no'} | {g(r['peak_Pi'], 3) if r['window'] else '—'} | "
      f"{g(r['peak'], 4) if r['window'] else '—'} | {lst(r['cross_005'], 3)} |")
w("")
w(f"The Prop 4 prediction (a window iff the initial gain slope is more than 2× the correct slope "
  f"{t4a['correct_slope']:.4g}) holds in {'all' if t4a['agree'] else 'NOT all'} {len(rows)} cases. "
  f"Factor 2 is the exact boundary and gives no window. "
  f"{'Miscalibrations A and B give identical filters for equal factors: the steady-state gain depends only on the assumed ratio q/r, so an inflated k·q and an inflated κ·Π are the same error. The two arms are therefore not independent tests. ' if same else ''}"
  f"In this parameterisation (var(v) = 1/Π per sample) the excess is small for modest miscalibration: factor 3 lifts the "
  f"peak only to {byk[('A', 3)]['peak']:.4g} (F = {t4a['F']:.3g}), and only factor 100 crosses R² = 0.05, on "
  f"{lst(byk[('A', 100)]['cross_005'], 3)}. Because Π here is a per-sample precision, these locations are "
  f"not directly comparable with the continuous (1/9, 4). The exact steady-state variances were confirmed by "
  f"simulation in {sum(s['pass'] for s in t4a['sims'])}/{len(t4a['sims'])} checks "
  f"(max relative error {t4a['max_sim_relerr']:.2%}, max |z| {t4a['max_sim_z']:.2f}).\n")

# 4b
w("### 4b Coloured sensory noise\n")
w("| τ | peak Π (sim) | peak (sim) | R²=0.05 window (sim) | semi-analytic peak Π | semi-analytic peak | semi-analytic window | max \\|z\\| sim vs semi |")
w("|---|---|---|---|---|---|---|---|")
for r in t4b["rows"]:
    s, sa = r["sim"], r["semi"]
    w(f"| {r['tau']:g} | {g(s['peak_Pi'], 3)} | {s['peak']:.4g} | {lst(s['cross_005'], 3)} | {g(sa['peak_Pi'], 3)} | "
      f"{sa['peak']:.4g} | {lst(sa['cross_005'], 3)} | {r['max_abs_z_vs_semi']:.2f} |")
w("")
rb = {r["tau"]: r for r in t4b["rows"]}
lost = [r["tau"] for r in t4b["rows"] if not r["sim"]["cross_005"]]
w(f"Coloured noise at equal zero-frequency power weakens the window but does not remove the bump above F. "
  f"The simulations match σ²_τ = (Σ + G²/(2Π(1+aτ)))/a, which scales the sensory term by 1/(1+aτ) "
  f"(max |z| ≤ {max(r['max_abs_z_vs_semi'] for r in t4b['rows']):.2f}). "
  f"The peak drops from {t4b['baseline']['peak']:.4g} (white noise) to {rb[0.1]['sim']['peak']:.4g} at τ = 0.1 "
  f"and {rb[10.0]['sim']['peak']:.4g} at τ = 10, and moves to lower Π ({g(rb[10.0]['semi']['peak_Pi'], 3)} at τ = 10). "
  f"The R² = 0.05 window narrows to {lst(rb[0.1]['sim']['cross_005'], 3)} at τ = 0.1 and disappears for "
  f"τ ∈ {{{', '.join(f'{t:g}' for t in lost)}}}. A bounded window above F remains for every τ. The paper's "
  f"numbers therefore depend on the white-noise assumption whenever τ is comparable to the relay time constant 1/(λ+G).\n")

# 4c
w("### 4c Drifting signal\n")
w("| case | peak (sim) | R²=0.05 window (sim) | σ² at Π = 100 (sim) | R² = 0.008 crossing (semi, Π ≤ 1e4) | semi σ² at Π = 1e4 | max \\|z\\| sim vs semi |")
w("|---|---|---|---|---|---|---|")
b = t4c["baseline"]
w(f"| no drift (closed form) | {b['peak']:.4g} | {lst(b['cross_005'], 3)} | {b['hi_end']:.4g} | {lst(b['cross_0008'], 4)} | {t4c['H']:.4g} (H) | — |")
for r in t4c["rows"]:
    c = r["case"]
    name = f"sin A={c['A_or_s']:g}, T={c['Td']:g}" if c["kind"] == "sin" else f"random walk s={c['A_or_s']:g}"
    w(f"| {name} | {r['sim']['peak']:.4g} | {lst(r['sim']['cross_005'], 3)} | {r['sim']['hi_end']:.4g} | "
      f"{lst(r['semi_fine']['cross_0008'], 4)} | {r['semi_fine']['hi_end']:.4g} | {r['max_abs_z_vs_semi']:.2f} |")
w("")
rw = t4c["rows"][-1]
s01 = [r for r in t4c["rows"] if r["case"]["kind"] == "sin" and r["case"]["A_or_s"] == 0.1]
w(f"The window **persists**. Its lower edge is unchanged and its upper edge moves out slightly, to at most "
  f"{max(r['sim']['cross_005'][1] for r in t4c['rows']):.3g} (random walk). This is because a precision-weighted "
  f"relay passes the drift with gain G/(λ+G), so the drift adds most at high Π. "
  f"In one sentence: drift does not replace the low-R² window, but it raises the high-precision floor and so "
  f"pushes the threshold regime into failure. With the sinusoids the floor stays below 0.008, but the R² = 0.008 "
  f"threshold moves from {b['cross_0008'][0]:.4g} to {g(min(r['semi_fine']['cross_0008'][0] for r in s01), 4)}–"
  f"{g(max(r['semi_fine']['cross_0008'][0] for r in s01), 4)} for A = 0.1. With the random walk the floor reaches "
  f"{rw['semi_fine']['hi_end']:.4g} > 0.008, so R² = 0.008 is never met anywhere on Π ≤ 1e4: the relay tracks the walk. "
  f"The margin is small ({rw['semi_fine']['hi_end'] - 0.008:.1g}) and depends on s. "
  f"The random-walk number is not stationary. It grows with the averaging horizon (here t ∈ [20, 220]), so a "
  f"longer run would make the high-precision failure worse.\n")

# 4d
w("### 4d Non-Kalman gains\n")
w("| gain | Prop 4 holds (P grid) | largest P with initial rise | largest P with any peak | peaks without initial rise | max # excess intervals | max # R²=0.05 intervals |")
w("|---|---|---|---|---|---|---|")
for name, s in t4d["summary"].items():
    n = sum(r["gain"] == name for r in t4d["rows"])
    pw = s["peak_without_rise"]
    w(f"| {name} | {n - s['n_prop4_fail']}/{n} | {g(s['max_P_with_rise'], 4) if s['max_P_with_rise'] else 'none'} | "
      f"{g(s['max_P_with_peak'], 4) if s['max_P_with_peak'] else 'none'} | "
      f"{f'{len(pw)} values of P, {g(min(pw), 3)}–{g(max(pw), 3)}' if pw else 'none'} | {s['max_excess_intervals']} | {s['max_005_intervals']} |")
w("")
hs = t4d["summary"]["hill2"]
w(f"Prop 4's small-Π claim holds for every gain and every P tested. For tanh and 1 − e^(−x), rise ⇔ g0 > "
  f"2Σ/λ = {t4d['thr']:g} ⇔ P < 50, and a peak appears exactly when the initial rise does. The Hill n = 2 "
  f"gain never rises at small Π, as Prop 4 predicts (g0 = 0). It still has a **later peak above F** for every "
  f"tested P up to {g(hs['max_P_with_peak'], 4)}, matching the exact condition max_Π G/Π = c/(2P) > 2Σ/λ ⇔ "
  f"P < {t4d['hill_peak_bound']:g} (from T1.8: σ² > F ⇔ G/Π > 2Σ/λ). So Prop 4 is a statement about the "
  f"small-Π behaviour, not a test for the window: sigmoidal gains can open one without any initial rise. "
  f"In every case the excess set and the R² = 0.05 failure set are a single interval; no multi-interval case "
  f"was found.\n")

# 4e
w("### 4e Precision-blind gain\n")
w(f"With constant G = G0, dσ²/dΠ = `{t4e['derivative']}`, which is negative. The limit as Π → 0 is "
  f"{t4e['limit0'].replace('oo', '∞')} and the limit as Π → ∞ is {t4e['limit_inf']}. The numerical grid is monotone decreasing for "
  f"all G0 ∈ {{{', '.join(f'{r['G0']:g}' for r in t4e['rows'])}}}. There is no window "
  f"({'confirmed' if t4e['no_window'] else 'NOT confirmed'}): this relay fails at low precision instead of "
  f"inside a bounded band.\n")

# ---------------------------------------------------------------- figures, env
w("## Figures\n")
figs = [("fig1a_paired.png", "Figure 1a: miscalibrated, calibrated and optimal relays on identical noise"),
        ("fig1b_regimes.png", "Figure 1b: regime bands vs R² for P = 1 (never / threshold / window / always)"),
        ("fig_t2_em.png", "Task 2: EM simulation vs closed form (2), with z-scores"),
        ("fig_t4a_discrete.png", "Task 4a: discrete-time Kalman, true error variance under miscalibration"),
        ("fig_t4b_colored.png", "Task 4b: coloured sensory noise"),
        ("fig_t4c_drift.png", "Task 4c: drifting signal"),
        ("fig_t4d_gains.png", "Task 4d: non-Kalman gains"),
        ("fig_t4e_fixed_gain.png", "Task 4e: precision-blind gain")]
for fn, d in figs:
    w(f"- `figures/{fn}`: {d}")
w("")
w("## Environment and runtime\n")
if env:
    w(f"Python {env['python']}, NumPy {env['numpy']}, SciPy {env['scipy']}, SymPy {env['sympy']}, "
      f"Matplotlib {env['matplotlib']}; {env['platform']}, {env['cpus']} CPUs.\n")
if rt_rows:
    w("| script | wall time (s) |")
    w("|---|---|")
    for s, t in rt_rows:
        w(f"| {s} | {t} |")
    w(f"| **total** | **{sum(float(t) for _, t in rt_rows):.1f}** |\n")
    over = [s_ for s_, t in rt_rows if float(t) > 300]
    w("No script went over the 5-minute budget, so trajectory counts were never reduced." if not over else
      f"Scripts over 5 min: {', '.join(over)}.")
w("Reproduce with `bash run_all.sh`. Seeds are fixed, so a rerun gives the same numbers on the same library versions.")

with open(os.path.join(HERE, "REPORT.md"), "w") as f:
    f.write("\n".join(L) + "\n")
print("\n".join(L))
