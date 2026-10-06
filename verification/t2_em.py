"""Task 2: Euler-Maruyama check of closed form (2), P = 1."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import (COLS, DT, FIG, GRID, LAM, NTRAJ, SIG, T_BATCH, T_BURN, T_SAMP,
                    Timer, dump, est, g_kalman, run_em, var_cf, var_em)

SEED = 1002
P = 1.0

with Timer() as T:
    G = g_kalman(GRID, P)
    specs = [(LAM + g, g / np.sqrt(p), np.sqrt(2 * SIG)) for p, g in zip(GRID, G)]
    bm = run_em(specs, SEED)
    m, se = est(bm)

cf = var_cf(GRID, G)
cfem = var_em(GRID, G)
tol = np.maximum(3 * se, 0.03 * cf)
ok_raw = np.abs(m - cf) < tol
ok_cor = np.abs(m - cfem) < np.maximum(3 * se, 0.03 * cfem)
i9, i4 = np.argmin(abs(GRID - 1 / 9)), np.argmin(abs(GRID - 4))
ok22 = [abs(m[i] - 0.05) < 3 * se[i] for i in (i9, i4)]

print(f"{'Pi':>10s} {'sim':>10s} {'SE':>9s} {'cf(2)':>10s} {'z_raw':>7s} {'cf_EM':>10s} {'z_cor':>7s} ok")
for i, p in enumerate(GRID):
    print(f"{p:10.4g} {m[i]:10.6f} {se[i]:9.2e} {cf[i]:10.6f} {(m[i]-cf[i])/se[i]:7.2f} "
          f"{cfem[i]:10.6f} {(m[i]-cfem[i])/se[i]:7.2f} {'ok' if ok_raw[i] else 'FAIL'}")
print(f"Pi=1/9: {m[i9]:.6f} +- {se[i9]:.2e}; Pi=4: {m[i4]:.6f} +- {se[i4]:.2e}")
print(f"runtime {T.dt:.1f}s")

zr, zc = (m - cf) / se, (m - cfem) / se
res = {
    "grid": GRID, "sim": m, "se": se, "cf": cf, "cf_em": cfem, "z_raw": zr, "z_cor": zc,
    "crit": {
        "T2.1": {"desc": "|sim-cf| < max(3SE, 3% cf) at every Pi (raw, vs (2))", "pass": bool(ok_raw.all()),
                 "detail": f"{ok_raw.sum()}/{len(GRID)} points; max |sim-cf|/cf = {np.max(abs(m-cf)/cf):.3%}; "
                           f"max |z| = {np.max(abs(zr)):.2f}"},
        "T2.1c": {"desc": "(info) same test vs EM-corrected D/(2a-a^2 dt)", "pass": bool(ok_cor.all()),
                  "detail": f"{ok_cor.sum()}/{len(GRID)}; max |z| = {np.max(abs(zc)):.2f}", "info": True},
        "T2.2": {"desc": "sim at Pi=1/9 and Pi=4 within 3SE of 0.05", "pass": bool(all(ok22)),
                 "detail": f"Pi=1/9: {m[i9]:.5f}+-{se[i9]:.5f} (z={(m[i9]-0.05)/se[i9]:.2f}); "
                           f"Pi=4: {m[i4]:.5f}+-{se[i4]:.5f} (z={(m[i4]-0.05)/se[i4]:.2f})"},
    },
    "settings": {"seed": SEED, "dt": DT, "ntraj": NTRAJ, "t_burn": T_BURN, "t_samp": T_SAMP, "t_batch": T_BATCH},
    "runtime_s": T.dt,
}
res["pass"] = res["crit"]["T2.1"]["pass"] and res["crit"]["T2.2"]["pass"]
dump("t2.json", res)

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 6.4), sharex=True, gridspec_kw={"height_ratios": [3, 1.3]})
pf = np.logspace(-2, 2, 400)
ax.plot(pf, var_cf(pf, g_kalman(pf, P)), color=COLS[0], lw=2, label="closed form (2), P = 1")
ax.errorbar(GRID, m, yerr=se, fmt="o", ms=4, color="#0b0b0b", mfc="white", elinewidth=1, capsize=0,
            label="EM simulation (±1 SE)")
ax.axhline(0.05, ls="--", color="#52514e", lw=1)
ax.text(1.2e-2, 0.052, "R² = 0.05", color="#52514e", fontsize=8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_ylabel("stationary variance σ²")
ax.set_title("Task 2 — Euler–Maruyama vs closed form (2)", loc="left", fontsize=11)
ax.legend(frameon=False, fontsize=9)
ax2.axhline(0, color="#52514e", lw=1)
ax2.plot(GRID, zr, "o", ms=4, color=COLS[0], label="vs (2)")
ax2.plot(GRID, zc, "s", ms=3, color=COLS[1], label="vs EM-corrected")
ax2.axhspan(-3, 3, color="#e9e8e4", zorder=0)
ax2.set_ylabel("(sim − cf)/SE"); ax2.set_xlabel("sensory precision Π")
ax2.legend(frameon=False, fontsize=8, ncol=2)
for a_ in (ax, ax2):
    a_.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(f"{FIG}/fig_t2_em.png", dpi=150)
