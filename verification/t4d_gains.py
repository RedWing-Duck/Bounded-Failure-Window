"""Task 4d: closed form (2) with non-Kalman gains; Prop 4 check."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import C, COLS, F, FIG, LAM, SIG, Timer, crossings, dump, intervals

PS = np.logspace(-2, 4, 61)
PI = np.logspace(-8, 8, 40001)
THR = 2 * SIG / LAM
GAINS = {
    "tanh": (lambda p, P: C * np.tanh(p / P), lambda P: C / P),
    "exp": (lambda p, P: -C * np.expm1(-p / P), lambda P: C / P),
    "hill2": (lambda p, P: C * p**2 / (p**2 + P**2), lambda P: 0.0),
}


def excess(pi, g):
    """sigma^2 - F in the cancellation-free form G(lam G/(2Pi) - Sigma)/(lam(lam+G)) (T1.8)."""
    return g * (LAM * g / (2 * pi) - SIG) / (LAM * (LAM + g))


rows = []
with Timer() as T:
    for name, (gfun, g0fun) in GAINS.items():
        for P in PS:
            g = gfun(PI, P)
            ex = excess(PI, g)
            v = F + ex
            eps = 1e-6 * min(P, 1.0)
            rise = bool(excess(eps, gfun(eps, P)) > 0)
            g0n = float(gfun(1e-9 * P, P) / (1e-9 * P))
            g0 = g0fun(P)
            pred = g0 > THR
            ints = intervals(ex > 0)
            i = int(np.argmax(v))
            rows.append({"gain": name, "P": float(P), "g0": g0, "g0_num": g0n, "pred_rise": bool(pred),
                         "rise": rise, "prop4_ok": bool(pred == rise),
                         "peak_exists": bool(ex[i] > 0 and 0 < i < len(PI) - 1), "peak_Pi": float(PI[i]),
                         "peak": float(v[i]), "n_excess_int": len(ints),
                         "excess_set": [[float(PI[a]), float(PI[b])] for a, b in ints],
                         "n_005_int": len(intervals(v > 0.05)), "cross_005": crossings(PI, v, 0.05)})

summ = {}
for name in GAINS:
    rs = [r for r in rows if r["gain"] == name]
    peakP = [r["P"] for r in rs if r["peak_exists"]]
    riseP = [r["P"] for r in rs if r["rise"]]
    summ[name] = {"prop4_all_ok": all(r["prop4_ok"] for r in rs),
                  "n_prop4_fail": sum(not r["prop4_ok"] for r in rs),
                  "max_P_with_rise": max(riseP) if riseP else None,
                  "max_P_with_peak": max(peakP) if peakP else None,
                  "min_P_without_peak": min([r["P"] for r in rs if not r["peak_exists"]], default=None),
                  "max_excess_intervals": max(r["n_excess_int"] for r in rs),
                  "max_005_intervals": max(r["n_005_int"] for r in rs),
                  "max_g0_rel_err": max(abs(r["g0_num"] - r["g0"]) / max(r["g0"], 1e-300) if r["g0"] > 0
                                        else abs(r["g0_num"]) for r in rs),
                  "peak_without_rise": [r["P"] for r in rs if r["peak_exists"] and not r["rise"]]}
    s = summ[name]
    print(f"{name:6s}: Prop4 ok {len(rs)-s['n_prop4_fail']}/{len(rs)}; largest P with initial rise "
          f"{s['max_P_with_rise']}; largest P with a peak {s['max_P_with_peak']}; first P without "
          f"{s['min_P_without_peak']}; max #excess intervals {s['max_excess_intervals']}; max #R2=0.05 "
          f"intervals {s['max_005_intervals']}; peaks without initial rise at P={['%.3g' % p for p in s['peak_without_rise']]}")
hill_peak_bound = C * LAM / (4 * SIG)
print(f"Hill n=2 analytic: excess iff max_Pi G/Pi = c/(2P) > 2Sigma/lam  <=>  P < {hill_peak_bound}")
print(f"runtime {T.dt:.1f}s")
dump("t4d.json", {"rows": rows, "summary": summ, "hill_peak_bound": hill_peak_bound, "thr": THR,
                  "runtime_s": T.dt})

fig, axs = plt.subplots(1, 3, figsize=(12, 3.9), sharey=True)
pp = np.logspace(-3, 4, 800)
for ax, (name, (gfun, _)) in zip(axs, GAINS.items()):
    for j, P in enumerate((1.0, 10.0, 30.0, 100.0)):
        ax.plot(pp, F + excess(pp, gfun(pp, P)), color=COLS[j], lw=1.8, label=f"P = {P:g}")
    ax.axhline(F, ls=":", lw=0.8, color="#52514e"); ax.axhline(0.05, ls="--", lw=0.8, color="#52514e")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_title({"tanh": "c·tanh(Π/P)", "exp": "c·(1 − e^(−Π/P))", "hill2": "c·Π²/(Π²+P²)  (g0 = 0)"}[name],
                 loc="left", fontsize=10)
    ax.set_xlabel("Π"); ax.spines[["top", "right"]].set_visible(False)
axs[0].set_ylabel("σ² from (2)"); axs[0].legend(frameon=False, fontsize=8)
fig.suptitle("Task 4d — non-Kalman gains (dotted: F, dashed: R² = 0.05)", x=0.01, ha="left", fontsize=11)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_t4d_gains.png", dpi=150)
