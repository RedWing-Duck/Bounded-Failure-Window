"""Task 4a: discrete-time steady-state Kalman filter with a miscalibrated assumed model."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

from common import COLS, FIG, LAM, SIG, Timer, crossings, dump, intervals

SEED = 1041
DTD = 0.05
PHI = np.exp(-LAM * DTD)
Q = SIG * (1 - PHI**2) / LAM
F = Q / (1 - PHI**2)                       # = Sigma/lambda
PI = np.logspace(-3, 4, 2001)
FACT = [1, 2, 3, 10, 100]


def gain(pi, qa, kappa=1.0):
    """Steady-state Kalman gain for assumed process noise qa, measurement variance 1/(kappa*pi)."""
    ra = 1.0 / (kappa * pi)
    b = ra * (1 - PHI**2) - qa
    disc = np.sqrt(b * b + 4 * qa * ra)
    pm = np.where(b > 0, 2 * qa * ra / (b + disc), (-b + disc) / 2)   # stable root of DARE
    return pm / (pm + ra)


def true_var(pi, K):
    return ((1 - K) ** 2 * Q + K**2 / pi) / (1 - (1 - K) ** 2 * PHI**2)


def describe(pi, v):
    i = int(np.argmax(v))
    lim0, liminf = F, 0.0
    win = 0 < i < len(pi) - 1 and v[i] > lim0 * (1 + 1e-9) and v[i] > liminf
    ex = intervals(v > F * (1 + 1e-9))
    w05 = intervals(v > 0.05)
    return {"window": bool(win), "peak_Pi": float(pi[i]), "peak": float(v[i]),
            "excess_F": [[float(pi[a]), float(pi[b])] for a, b in ex],
            "cross_005": crossings(pi, v, 0.05), "n_int_005": len(w05)}


with Timer() as T:
    eps = 1e-9
    rows = []
    filt = {}
    for mode in "AB":
        for f in FACT:
            K = gain(PI, f * Q) if mode == "A" else gain(PI, Q, f)
            K_eps = gain(eps, f * Q) if mode == "A" else gain(eps, Q, f)
            slope_num = float(K_eps / eps)
            slope_an = f * F
            d = describe(PI, true_var(PI, K))
            d.update(mode=mode, factor=f, slope_num=slope_num, slope_an=slope_an,
                     ratio=slope_num / F, prediction=bool(slope_num > 2 * F))
            rows.append(d)
            filt[(mode, f)] = K
    correct_slope = float(gain(eps, Q) / eps)

    # simulation check
    rng = np.random.default_rng(SEED)
    ntraj, nburn, nsamp, nb = 256, 2000, 40000, 400
    N = nburn + nsamp
    w = rng.standard_normal((ntraj, N)) * np.sqrt(Q)
    v0 = rng.standard_normal((ntraj, N))
    x0 = rng.standard_normal((ntraj, 1)) * np.sqrt(F)
    x = lfilter([1.0], [1.0, -PHI], w, axis=1, zi=PHI * x0)[0]
    sims = []
    for p in (0.1, 1.0, 10.0):
        y = x + v0 / np.sqrt(p)
        for (mode, f) in filt:
            K = float(gain(p, f * Q) if mode == "A" else gain(p, Q, f))
            xh = lfilter([K], [1.0, -(1 - K) * PHI], y, axis=1)
            e2 = ((x - xh) ** 2)[:, nburn:].reshape(ntraj, -1, nb).mean(-1).ravel()
            m, se = e2.mean(), e2.std(ddof=1) / np.sqrt(e2.size)
            ex = float(true_var(p, K))
            sims.append({"Pi": p, "mode": mode, "factor": f, "sim": m, "se": se, "exact": ex,
                         "pass": bool(abs(m - ex) < max(3 * se, 0.03 * ex))})

print(f"phi={PHI:.6f} q={Q:.4e} F={F:.4f}; correct initial slope dK/dPi = {correct_slope:.6f} (= F)")
print(f"{'mis':>4s} {'f':>4s} {'slope':>9s} {'ratio':>6s} {'pred':>5s} {'window':>6s} {'peakPi':>8s} {'peak':>8s} excess>F     R2=.05 crossings")
for r in rows:
    print(f"{r['mode']:>4s} {r['factor']:4d} {r['slope_num']:9.5f} {r['ratio']:6.2f} {str(r['prediction']):>5s} "
          f"{str(r['window']):>6s} {r['peak_Pi']:8.3g} {r['peak']:8.5f} {r['excess_F']} {['%.3g' % c for c in r['cross_005']]}")
agree = all(r["prediction"] == r["window"] for r in rows)
print("prediction (window iff slope > 2x correct) agrees in all cases:", agree)
print("simulation checks pass:", sum(s["pass"] for s in sims), "/", len(sims))
for s in sims:
    if not s["pass"]:
        print("  FAIL", s)
print(f"runtime {T.dt:.1f}s")
dump("t4a.json", {"rows": rows, "sims": sims, "agree": agree, "correct_slope": correct_slope, "F": F,
                  "phi": PHI, "q": Q, "dt": DTD, "runtime_s": T.dt,
                  "sim_pass": all(s["pass"] for s in sims),
                  "max_sim_relerr": max(abs(s["sim"] - s["exact"]) / s["exact"] for s in sims),
                  "max_sim_z": max(abs(s["sim"] - s["exact"]) / s["se"] for s in sims)})

fig, axs = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
pal = ["#0b0b0b"] + COLS
for ax, mode, name in zip(axs, "AB", ("A: assumed process noise k·q", "B: assumed precision κ·Π")):
    for j, f in enumerate(FACT):
        ax.plot(PI, true_var(PI, filt[(mode, f)]), color=pal[j], lw=2 if f != 1 else 2.5,
                label=f"{'k' if mode == 'A' else 'κ'} = {f}" + (" (correct)" if f == 1 else ""))
    for s in sims:
        if s["mode"] == mode:
            ax.plot(s["Pi"], s["sim"], "o", ms=5, mfc="white", mec=pal[FACT.index(s["factor"])], zorder=3)
    ax.axhline(F, color="#52514e", lw=0.8, ls=":")
    ax.text(1.2e-3, F * 1.04, "F", fontsize=8, color="#52514e")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("observation precision Π (var v = 1/Π)")
    ax.set_title(name, loc="left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8)
axs[0].set_ylabel("true steady-state error variance")
fig.suptitle("Task 4a — discrete-time Kalman filter, Δt = 0.05 (points: simulation)", x=0.01, ha="left", fontsize=11)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_t4a_discrete.png", dpi=150)
