"""Figure: relay sigma^2(tau) (G = 0.5) and optimal P(tau) at the worked example."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from t9_common import COLS, HERE, P_opt, crit, relay

lam, Sig, Pi, G = 1.0, 0.01, 1.0, 0.5
c = {k: float(v) for k, v in crit(mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi), mp.mpf(G)).items()}
tau = np.logspace(-3, 4, 600)
rel = np.array([float(relay(mp.mpf(t), lam, Sig, Pi, G)) for t in tau])
P = np.array([float(P_opt(mp.mpf(t), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))) for t in tau])
INK, MUTED = "#222222", "#6b6b6b"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
fig, ax = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
ax.plot(tau, rel, color=COLS[0], lw=2, zorder=3)
ax.plot(tau, P, color=COLS[1], lw=2, zorder=3)
ax.annotate(r"relay $\sigma^2(\tau)$, $G = 0.5$", (2e-3, rel[np.searchsorted(tau, 2e-3)]), xytext=(0, 6),
            textcoords="offset points", color=INK)
ax.annotate(r"optimal $P(\tau)$", (1e2, P[np.searchsorted(tau, 1e2)]), xytext=(4, -14), textcoords="offset points",
            color=INK)
for y, lab, ls in ((c["F"], r"$F$", "--"), (c["H_G"], r"$H_G$", "-."), (c["s2"], r"$\sigma_\star^2$", ":"),
                   (c["V_w"], r"$V_w$", (0, (1, 3)))):
    ax.axhline(y, color=MUTED, lw=0.9, ls=ls, zorder=1, label=f"{lab} = {y:.4g}")
ax.axvline(16.0, color=COLS[0], lw=0.8, ls=":", zorder=1, label=r"$\tau_F = 16$ (relay crosses $F$)")
ax.legend(loc="lower left", frameon=False, fontsize=8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"noise correlation time $\tau$"); ax.set_ylabel("stationary error variance")
ax.grid(True, which="major", color="#e6e6e6", lw=0.6)
p = os.path.join(HERE, "fig_t9_tau.png")
fig.savefig(p, dpi=300)
print(f"wrote {p}")
