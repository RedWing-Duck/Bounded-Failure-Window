"""Task 4c: drifting signal mean eta(t) = z* + d(t); variance measured about z*. P = 1."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from common import (COLS, DT, F, FIG, GRID, H, LAM, NTRAJ, SIG, T_BURN, T_SAMP, Timer, crossings,
                    dump, est, g_kalman, intervals, run_em, var_cf)

SEED = 1043
P = 1.0
S_RW = 0.01
G = g_kalman(GRID, P)
CASES = [("sin", 0.05, 10.0), ("sin", 0.05, 100.0), ("sin", 0.1, 10.0), ("sin", 0.1, 100.0), ("rw", S_RW, None)]


def make_drive(kind, A, Td, seed):
    if kind == "sin":
        w = 2 * np.pi / Td

        def drive(k, n, ntraj):
            t = (k * n + np.arange(n)) * DT      # time at the start of each step
            return (A * np.sin(w * t) * DT)[None, :]
        return drive
    rng = np.random.default_rng(seed)
    st = {"B": np.zeros((NTRAJ, 1))}

    def drive(k, n, ntraj):
        inc = rng.standard_normal((ntraj, n)) * (A * np.sqrt(DT))
        B = st["B"] + np.cumsum(inc, axis=1) - inc   # value at the start of each step
        st["B"] = B[:, -1:] + inc[:, -1:]
        return B * DT
    return drive


def semi_rw(pi_g, s):
    """Time-averaged E[x_rw^2] over the sampling window, from the moment ODEs of
    dY = (-a Y + B) dt, B Brownian (unit): m_BB' = 1, m_YB' = -a m_YB + m_BB, m_YY' = -2a m_YY + 2 m_YB."""
    a = LAM + pi_g

    def rhs(t, y):
        n = len(a)
        mYB, mYY, I = y[:n], y[n:2 * n], y[2 * n:]
        return np.concatenate([-a * mYB + t, -2 * a * mYY + 2 * mYB, (t >= T_BURN) * mYY])
    sol = solve_ivp(rhs, (0, T_BURN + T_SAMP), np.zeros(3 * len(a)), rtol=1e-10, atol=1e-14,
                    max_step=0.5)
    return pi_g**2 * s**2 * sol.y[2 * len(a):, -1] / T_SAMP


def semi(case, pi, g):
    kind, A, Td = case
    a = LAM + g
    if kind == "sin":
        w = 2 * np.pi / Td
        return var_cf(pi, g) + g**2 * A**2 / (2 * (a**2 + w**2))
    return var_cf(pi, g) + semi_rw(g, A)


def summary(pi, v):
    i = int(np.argmax(v))
    return {"peak_Pi": float(pi[i]), "peak": float(v[i]),
            "window": bool(0 < i < len(pi) - 1 and v[i] > max(v[0], v[-1])),
            "cross_005": crossings(pi, v, 0.05), "n_int_005": len(intervals(v > 0.05)),
            "cross_0008": crossings(pi, v, 0.008), "hi_end": float(v[-1]), "lo_end": float(v[0])}


rows, sims = [], {}
pf = np.logspace(-2, 4, 241)
gf = g_kalman(pf, P)
base = summary(GRID, var_cf(GRID, G))
with Timer() as T:
    for j, case in enumerate(CASES):
        specs = [(LAM + g, g / np.sqrt(p), np.sqrt(2 * SIG), g) for p, g in zip(GRID, G)]
        bm = run_em(specs, SEED, drive=make_drive(*case, seed=SEED + 200 + j))
        m, se = est(bm)
        sa = semi(case, GRID, G)
        r = {"case": {"kind": case[0], "A_or_s": case[1], "Td": case[2]},
             "sim": summary(GRID, m), "semi": summary(GRID, sa), "semi_fine": summary(pf, semi(case, pf, gf)),
             "max_abs_z_vs_semi": float(np.max(abs(m - sa) / se)),
             "max_relerr_vs_semi": float(np.max(abs(m - sa) / sa))}
        rows.append(r)
        sims[j] = (m, se, sa)
        s = r["sim"]
        print(f"{case}: peak {s['peak']:.5f} at {s['peak_Pi']:.3g}; 0.05 crossings "
              f"{['%.3g' % c for c in s['cross_005']]}; 0.008 crossings {['%.3g' % c for c in s['cross_0008']]}; "
              f"sigma2(Pi=100)={s['hi_end']:.5f}; window={s['window']} | max|z| vs semi "
              f"{r['max_abs_z_vs_semi']:.2f}, rel {r['max_relerr_vs_semi']:.2%}; "
              f"semi Pi=1e4: {r['semi_fine']['hi_end']:.5f}")
print(f"baseline: peak {base['peak']:.5f} at {base['peak_Pi']:.3g}, 0.05 {base['cross_005']}, "
      f"0.008 {base['cross_0008']}, sigma2(100)={base['hi_end']:.5f}; H={H}")
print(f"runtime {T.dt:.1f}s")
dump("t4c.json", {"rows": rows, "baseline": base, "runtime_s": T.dt, "H": H,
                  "sim": {j: {"m": v[0], "se": v[1], "semi": v[2]} for j, v in sims.items()}})

fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.plot(pf, var_cf(pf, gf), color="#0b0b0b", lw=2.5, label="no drift (baseline)")
labs = ["A=0.05, T=10", "A=0.05, T=100", "A=0.1, T=10", "A=0.1, T=100", f"random walk, s={S_RW}"]
pal = COLS + ["#e34948"]
for j, case in enumerate(CASES):
    m, se, _ = sims[j]
    ax.plot(pf, semi(case, pf, gf), color=pal[j], lw=1.5, label=labs[j])
    ax.errorbar(GRID, m, yerr=se, fmt="o", ms=3.5, mfc="white", color=pal[j], elinewidth=1, capsize=0)
ax.axhline(0.05, ls="--", lw=1, color="#52514e"); ax.text(1.1e-2, 0.053, "R² = 0.05", fontsize=8, color="#52514e")
ax.axhline(0.008, ls=":", lw=1, color="#52514e"); ax.text(1.1e-2, 0.0083, "R² = 0.008", fontsize=8, color="#52514e")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("sensory precision Π"); ax.set_ylabel("mean squared deviation from z*")
ax.set_title("Task 4c — drifting signal (lines: semi-analytic; points: EM)", loc="left", fontsize=10)
ax.legend(frameon=False, fontsize=8); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_t4c_drift.png", dpi=150)
