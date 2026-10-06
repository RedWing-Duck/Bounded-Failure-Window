"""Task 3: paired comparison of miscalibrated, calibrated and optimal relays (Figure 1)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, minimize_scalar

from common import (COLS, DT, F, FIG, GRID, H, LAM, NTRAJ, SIG, T_BATCH, T_BURN, T_SAMP,
                    Timer, crossings, dump, est, g_kalman, g_opt, run_em, var_cf)

SEED = 1003
gains = {"a": g_kalman(GRID, 1.0), "b": g_kalman(GRID, 100.0), "c": g_opt(GRID)}
labels = {"a": "miscalibrated, P = 1", "b": "calibrated, P = 100", "c": "optimal, G = G*(Π)"}

with Timer() as T:
    specs = [(LAM + g, g / np.sqrt(p), np.sqrt(2 * SIG)) for k in "abc" for p, g in zip(GRID, gains[k])]
    bm = run_em(specs, SEED).reshape(3, len(GRID), -1)
bm = dict(zip("abc", bm))
m = {k: est(v)[0] for k, v in bm.items()}
se = {k: est(v)[1] for k, v in bm.items()}
cf = {k: var_cf(GRID, g) for k, g in gains.items()}
n = len(GRID)

crit = {}
# T3.1
im = int(np.argmax(m["a"]))
crit["T3.1"] = {"desc": "(a) maximum strictly inside the grid", "pass": 0 < im < n - 1,
                "detail": f"argmax at Pi={GRID[im]:.4g} (index {im} of 0..{n-1}), sim max={m['a'][im]:.5f}"}
# T3.2
xs = crossings(GRID, m["a"], 0.05)
ok32 = len(xs) == 2 and abs(xs[0] / (1 / 9) - 1) < 0.15 and abs(xs[1] / 4 - 1) < 0.15
crit["T3.2"] = {"desc": "(a) crosses R2=0.05 exactly twice, crossings within 15% of 1/9 and 4", "pass": ok32,
                "detail": f"crossings={['%.4f' % x for x in xs]}; rel. err = "
                          f"{[f'{x/t-1:+.2%}' for x, t in zip(xs, (1/9, 4))] if len(xs) == 2 else 'n/a'}"}


def diff_z(k, i, j):
    """(sim_i - sim_j) and its paired batch-means SE."""
    d = bm[k][i] - bm[k][j]
    return d.mean(), d.std(ddof=1) / np.sqrt(d.size)


for k in "bc":
    dz = [diff_z(k, i, 0) for i in range(n)]
    worst = max(range(1, n), key=lambda i: dz[i][0] / dz[i][1])
    ok = all(d < 3 * s for d, s in dz[1:])
    crit[f"T3.3{k}"] = {"desc": f"({k}) no point exceeds its Pi=0.01 value by > 3 SE_diff", "pass": ok,
                        "detail": f"max (sim_i - sim_0)/SE = {dz[worst][0]/dz[worst][1]:.2f} at Pi={GRID[worst]:.4g}"}
    adj = [diff_z(k, i + 1, i) for i in range(n - 1)]
    zs = [d / s for d, s in adj]
    w = int(np.argmax(zs))
    crit[f"T3.4{k}"] = {"desc": f"({k}) no adjacent rise > 3 SE_diff", "pass": max(zs) < 3,
                        "detail": f"max adjacent rise z = {zs[w]:.2f} between Pi={GRID[w]:.4g} and {GRID[w+1]:.4g}"}
for o in "ab":
    d = bm["c"] - bm[o]
    dm, ds = d.mean(1), d.std(1, ddof=1) / np.sqrt(d.shape[1])
    z = dm / ds
    w = int(np.argmax(z))
    crit[f"T3.5{o}"] = {"desc": f"(c) <= ({o}) within noise at every Pi (c-{o} < 3 SE_diff)", "pass": bool(np.all(dm < 3 * ds)),
                        "detail": f"max z(c-{o}) = {z[w]:.2f} at Pi={GRID[w]:.4g} (c-{o} = {dm[w]:.2e})"}

ok_all = all(v["pass"] for v in crit.values())
for k_, v in crit.items():
    print(f"[{'PASS' if v['pass'] else 'FAIL'}] {k_}: {v['desc']} -- {v['detail']}")

# closed-form regime boundaries for P=1 (Fig 1b)
s1 = lambda p: var_cf(p, g_kalman(p, 1.0))
opt = minimize_scalar(lambda lp: -s1(np.exp(lp)), bounds=(-5, 5), method="bounded", options={"xatol": 1e-12})
M, pM = s1(np.exp(opt.x)), float(np.exp(opt.x))
print(f"H={H}, F={F}, M={M:.6f} at Pi={pM:.5f}; runtime {T.dt:.1f}s")

dump("t3.json", {"grid": GRID, "sim": m, "se": se, "cf": cf, "crit": crit, "pass": ok_all,
                 "crossings_sim": xs, "regimes": {"H": H, "F": F, "M": M, "Pi_M": pM},
                 "settings": {"seed": SEED, "dt": DT, "ntraj": NTRAJ, "t_burn": T_BURN, "t_samp": T_SAMP,
                              "t_batch": T_BATCH}, "runtime_s": T.dt})

# ---------------- Figure 1a
fig, ax = plt.subplots(figsize=(6.6, 4.6))
pf = np.logspace(-2, 2, 500)
ax.axvspan(1 / 9, 4, color="#f3e1d9", zorder=0, lw=0)
ax.text(np.sqrt(4 / 9), 0.0115, "failure window (1/9, 4)", ha="center", va="bottom", fontsize=8, color="#52514e")
ax.axhline(0.05, ls="--", lw=1, color="#52514e")
ax.text(1.15e-2, 0.053, "R² = 0.05", fontsize=8, color="#52514e")
gf = {"a": g_kalman(pf, 1.0), "b": g_kalman(pf, 100.0), "c": g_opt(pf)}
mk = {"a": "o", "b": "s", "c": "^"}
for i, k in enumerate("abc"):
    ax.plot(pf, var_cf(pf, gf[k]), color=COLS[i], lw=2, label=f"({k}) {labels[k]}")
    ax.errorbar(GRID, m[k], yerr=se[k], fmt=mk[k], ms=4.5, color=COLS[i], mfc="white", mew=1.2,
                elinewidth=1, capsize=0, zorder=3)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("sensory precision Π"); ax.set_ylabel("stationary variance σ²")
ax.set_title("Figure 1a — paired simulation on identical noise (lines: closed form; points: EM ±1 SE)",
             loc="left", fontsize=9.5)
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig1a_paired.png", dpi=150); plt.close(fig)

# ---------------- Figure 1b: regimes vs R2, P = 1, closed form
fig, ax = plt.subplots(figsize=(6.6, 4.6))
pf = np.logspace(-3, 4, 800)
sf = s1(pf)
ylo, yhi = 3e-3, 0.2
bands = [(ylo, H, "never satisfied", "#e8e8e6"), (H, F, "threshold: satisfied only for Π above a cutoff", "#d9e7f7"),
         (F, M, "window: fails only inside a bounded Π interval", "#f8ddd0"), (M, yhi, "always satisfied", "#ffffff")]
for lo, hi, lab, col in bands:
    ax.axhspan(lo, hi, color=col, lw=0, zorder=0)
    ax.text(1.3e-3, np.sqrt(lo * hi), lab, va="center", fontsize=8, color="#0b0b0b")
ax.fill_between(pf, ylo, sf, color="#0b0b0b", alpha=0.10, lw=0, label="fails (σ² > R²)")
ax.plot(pf, sf, color=COLS[0], lw=2, label="σ²(Π), P = 1")
for v, name in ((H, "H = Σ/(λ+c)"), (F, "F = Σ/λ"), (M, f"M = {M:.4f}")):
    ax.axhline(v, color="#52514e", lw=0.8)
    ax.text(1.2e4, v, name, va="center", ha="left", fontsize=8, color="#52514e")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(ylo, yhi); ax.set_xlim(1e-3, 1e4)
ax.set_xlabel("sensory precision Π"); ax.set_ylabel("requirement R² (pass iff σ² ≤ R²)")
ax.set_title("Figure 1b — regimes of the miscalibrated relay (P = 1) by requirement R²", loc="left", fontsize=9.5)
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig1b_regimes.png", dpi=150); plt.close(fig)
