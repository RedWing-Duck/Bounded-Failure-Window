"""Task 4e: precision-blind constant gain G = G0."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from common import COLS, F, FIG, Timer, dump, var_cf

G0S = [0.1, 0.5, 1.0, 2.0]
PI = np.logspace(-4, 4, 2001)

with Timer() as T:
    lam, S, Pi, G0 = sp.symbols("lambda Sigma Pi G0", positive=True)
    s2 = (S + G0**2 / (2 * Pi)) / (lam + G0)
    d = sp.simplify(sp.diff(s2, Pi))
    neg = sp.ask(sp.Q.negative(d)) is True
    lim0 = sp.limit(s2, Pi, 0)
    liminf = sp.simplify(sp.limit(s2, Pi, sp.oo))
    rows = []
    for g0 in G0S:
        v = var_cf(PI, np.full_like(PI, g0))
        rows.append({"G0": g0, "monotone_dec": bool(np.all(np.diff(v) < 0)), "v_min_Pi": float(v[0]),
                     "v_max_Pi": float(v[-1]), "limit_inf": float(liminf.subs({S: 0.01, lam: 1, G0: g0}))})
ok = neg and lim0 == sp.oo and all(r["monotone_dec"] for r in rows)
print(f"d sigma^2/dPi = {d}  (negative: {neg}); limit Pi->0 = {lim0}; limit Pi->inf = {liminf}")
for r in rows:
    print(r)
print("no window (monotone decreasing, diverges at 0):", ok, f"runtime {T.dt:.1f}s")
dump("t4e.json", {"derivative": str(d), "derivative_negative": neg, "limit0": str(lim0),
                  "limit_inf": str(liminf), "rows": rows, "no_window": ok, "runtime_s": T.dt})

fig, ax = plt.subplots(figsize=(6.2, 4.3))
for j, g0 in enumerate(G0S):
    ax.plot(PI, var_cf(PI, np.full_like(PI, g0)), color=COLS[j], lw=2, label=f"G0 = {g0:g}")
ax.axhline(F, ls=":", lw=0.8, color="#52514e"); ax.text(1.2e-4, F * 1.15, "F = Σ/λ", fontsize=8, color="#52514e")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("sensory precision Π"); ax.set_ylabel("σ² from (2)")
ax.set_title("Task 4e — precision-blind gain: monotone, diverges as Π → 0", loc="left", fontsize=10)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_t4e_fixed_gain.png", dpi=150)
