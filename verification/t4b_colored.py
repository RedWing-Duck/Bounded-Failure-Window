"""Task 4b: coloured (OU) sensory noise with correlation time tau, P = 1."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

from common import (COLS, DT, F, FIG, GRID, LAM, NTRAJ, SIG, Timer, crossings, dump, est,
                    g_kalman, intervals, run_em, var_cf)

SEED = 1042
TAUS = [0.01, 0.1, 1.0, 10.0]
P = 1.0
G = g_kalman(GRID, P)
pf = np.logspace(-3, 4, 4001)
Gf = g_kalman(pf, P)


def var_tau(pi, g, tau):
    """Semi-analytic: sensory contribution scaled by 1/(1 + a tau)."""
    a = LAM + g
    return (SIG + g**2 / (2 * pi * (1 + a * tau))) / a


def summary(pi, v, lim0):
    i = int(np.argmax(v))
    return {"peak_Pi": float(pi[i]), "peak": float(v[i]),
            "window": bool(0 < i < len(pi) - 1 and v[i] > lim0 * (1 + 1e-9)),
            "cross_005": crossings(pi, v, 0.05), "n_int_005": len(intervals(v > 0.05)),
            "excess_F_upper": crossings(pi, v, F)}


def make_sensory(tau, seed):
    """Unit OU noise (integrated autocovariance 1), returned as eta*dt increments."""
    rho = np.exp(-DT / tau)
    var = 1.0 / (2 * tau)
    innov = np.sqrt(var * (1 - rho**2))
    state = {"z": np.random.default_rng(seed).standard_normal((NTRAJ, 1)) * np.sqrt(var) * rho}

    def sensory(k, dWs):
        xi = dWs / np.sqrt(DT)                 # reuse the common white draws as OU innovations
        eta, state["z"] = lfilter([innov], [1.0, -rho], xi, axis=1, zi=state["z"])
        return eta * DT
    return sensory


rows, sims = [], {}
base = summary(pf, var_cf(pf, Gf), F)
with Timer() as T:
    for j, tau in enumerate(TAUS):
        specs = [(LAM + g, g / np.sqrt(p), np.sqrt(2 * SIG)) for p, g in zip(GRID, G)]
        bm = run_em(specs, SEED, t_batch=max(10.0, 10 * tau), sensory=make_sensory(tau, SEED + 100 + j))
        m, se = est(bm)
        sa = var_tau(GRID, G, tau)
        z = (m - sa) / se
        r = {"tau": tau, "sim": summary(GRID, m, m[0]), "semi": summary(pf, var_tau(pf, Gf, tau), F),
             "max_abs_z_vs_semi": float(np.max(abs(z))), "max_relerr_vs_semi": float(np.max(abs(m - sa) / sa)),
             "agree_semi": bool(np.all(abs(m - sa) < np.maximum(3 * se, 0.03 * sa))),
             "nbatches": int(bm.shape[1])}
        rows.append(r)
        sims[tau] = (m, se)
        print(f"tau={tau:5g}: sim peak {r['sim']['peak']:.5f} at {r['sim']['peak_Pi']:.3g}, "
              f"0.05-crossings {['%.3g' % c for c in r['sim']['cross_005']]} | semi peak {r['semi']['peak']:.5f} "
              f"at {r['semi']['peak_Pi']:.3g}, crossings {['%.3g' % c for c in r['semi']['cross_005']]}, "
              f"window={r['semi']['window']} | max|z| vs semi {r['max_abs_z_vs_semi']:.2f}, "
              f"max rel err {r['max_relerr_vs_semi']:.2%}")
print(f"baseline (white): peak {base['peak']:.5f} at {base['peak_Pi']:.3g}, crossings {base['cross_005']}")
print(f"runtime {T.dt:.1f}s")
dump("t4b.json", {"rows": rows, "baseline": base, "runtime_s": T.dt, "grid": GRID,
                  "sim": {str(t): {"m": v[0], "se": v[1]} for t, v in sims.items()}})

fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.plot(pf, var_cf(pf, Gf), color="#0b0b0b", lw=2.5, label="white noise (baseline)")
for j, tau in enumerate(TAUS):
    ax.plot(pf, var_tau(pf, Gf, tau), color=COLS[j], lw=1.8, label=f"τ = {tau:g}")
    m, se = sims[tau]
    ax.errorbar(GRID, m, yerr=se, fmt="o", ms=3.5, mfc="white", color=COLS[j], elinewidth=1, capsize=0)
ax.axhline(0.05, ls="--", lw=1, color="#52514e"); ax.text(1.2e-3, 0.053, "R² = 0.05", fontsize=8, color="#52514e")
ax.axhline(F, ls=":", lw=0.8, color="#52514e"); ax.text(1.2e-3, F * 1.05, "F", fontsize=8, color="#52514e")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1e-3, 1e4)
ax.set_xlabel("sensory precision Π"); ax.set_ylabel("stationary variance σ²")
ax.set_title("Task 4b — OU sensory noise, equal zero-frequency power (lines: semi-analytic; points: EM)",
             loc="left", fontsize=9)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_t4b_colored.png", dpi=150)
