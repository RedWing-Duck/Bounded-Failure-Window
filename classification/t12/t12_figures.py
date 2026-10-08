"""Figures H1-H5 for Task 12 (PNG + PDF in figs/). H3 uses results/t12_a8.json (A2/A3 excess checks)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from t12_common import COLS, FIGS, RES, analyse_dt, classify, dt_funcs, sig_funcs, sstar

INK, MUTED, GRID = "#222222", "#6b6b6b", "#e6e6e6"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED})


def save(fig, nm):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIGS, f"{nm}.{ext}"), dpi=300)
    plt.close(fig)


def curve(fam, met, p, ts):
    f, _ = dt_funcs(fam, met, p)
    return np.array([float(f(mp.mpf(float(t)))) for t in ts])


# ---------------- H1 optimal M-P
p1 = {"lam": 1, "Sig": "0.01", "Pi": 1}
F = 0.01
s2 = float(sstar(mp.mpf(1), mp.mpf("0.01"), mp.mpf(1)))
ts = np.logspace(-3, 4, 400)
fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
for met, col, ls, lab in (("post", COLS[0], "-", "post (after update)"), ("prior", COLS[1], "--", "prior (before update)"),
                          ("avg", COLS[2], "-.", "avg (time average)")):
    ax.plot(ts, curve("opt", met, p1, ts), color=col, lw=2, ls=ls, label=lab)
ax.axhline(s2, color=MUTED, lw=0.8, ls=":", label=r"$\sigma_\star^2$ (continuous observation)")
ax.axhline(F, color=MUTED, lw=0.8, ls="--", label=r"$F = \Sigma/\lambda$")
ax.set_xscale("log"); ax.set_xlabel(r"sampling interval $\Delta t$"); ax.set_ylabel("optimal error (M-P)")
ax.set_title(r"Optimal sampled filter, $\lambda = 1$, $\Sigma = 0.01$, $\Pi = 1$", fontsize=9, loc="left", color=INK)
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8, loc="center left")
save(fig, "H1_optimal_MP")

# ---------------- H2 D1 at G = 0.5
q = {"lam": 1, "Sig": "0.01", "Pi": 1, "G": "0.5"}
Ap, Aa = analyse_dt("D1", "post", q), analyse_dt("D1", "avg", q)
Mx = float(Ap["turns"][0]["value"])
mn = float(min(t["value"] for t in Aa["turns"] if t["kind"] == "min"))
s2G = float(Ap["L_minus"])
ts = np.logspace(-2, 4, 500)
post, avg = curve("D1", "post", q, ts), curve("D1", "avg", q, ts)
from t12_a8 import root_D1  # noqa: E402
dtE = float(root_D1(mp.mpf("0.5"), mp.mpf("0.01"), mp.mpf(1)))
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
ax = axs[0]
ax.plot(ts, post, color=COLS[0], lw=2, label="post")
ax.axhspan(s2G, Mx, color=COLS[0], alpha=0.12, lw=0, label=rf"window band $R^2 \in ({s2G:.3g}, {Mx:.4g})$")
ax.axhline(F, color=MUTED, lw=0.8, ls="--", label=r"$F$")
ax.axvline(dtE, color=COLS[1], lw=0.9, ls=":", label=rf"$\Delta t_E = {dtE:.4g}$")
ax.set_xscale("log"); ax.set_xlabel(r"$\Delta t$"); ax.set_ylabel("error"); ax.grid(True, color=GRID, lw=0.6)
ax.set_title("D1, G = 0.5: post", fontsize=9, loc="left", color=INK); ax.legend(frameon=False, fontsize=7.5)
ax = axs[1]
ax.plot(ts, avg, color=COLS[2], lw=2, label="avg")
ax.axhspan(mn, F, color=COLS[2], alpha=0.25, lw=0, label=rf"two-ray band $R^2 \in ({mn:.6g}, F)$")
ax.axhline(F, color=MUTED, lw=0.8, ls="--", label=r"$F$")
ax.axvline(dtE, color=COLS[1], lw=0.9, ls=":", label=r"$\Delta t_E$ (avg crosses $F$)")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel(r"$\Delta t$"); ax.grid(True, color=GRID, lw=0.6)
ax.set_title("D1, G = 0.5: avg (log scale; the dip below F is about 1e-3 relative)", fontsize=9, loc="left", color=INK)
ax.legend(frameon=False, fontsize=7.5)
ins = ax.inset_axes([0.55, 0.45, 0.42, 0.3])
tz = np.logspace(1.5, 3.5, 300)
ins.plot(tz, curve("D1", "avg", q, tz) / F - 1, color=COLS[2], lw=1.5)
ins.axhline(0, color=MUTED, lw=0.6, ls="--"); ins.set_xscale("log"); ins.tick_params(labelsize=6)
ins.set_title(r"avg/$F$ − 1", fontsize=6.5)
save(fig, "H2_D1_G05")

# ---------------- H3 excess onset maps
a8 = json.load(open(os.path.join(RES, "t12_a8.json")))
sets = [s for s in a8["sets"]]
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)

k = np.logspace(0.001, 4, 400)
y = []
for kk in k:
    G = 2 * kk
    y.append(float(root_D1(mp.mpf(G), mp.mpf(1), mp.mpf(1)) * G))
ax = axs[0]
ax.plot(k, y, color=INK, lw=1.2, label=r"closed form: $\tanh(y/2)/y = 1/(2k)$")
pts = [(e["G_over_2FPi"], e["end"] * e["p"]["G"]) for e in a8["families"]["D1"].get("excess_points", [])]
if pts:
    ax.plot(*zip(*pts), "o", ms=3, mfc="none", color=COLS[0], label="classifier (A2 sets)")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel(r"$k = G/(2F\Pi)$"); ax.set_ylabel(r"$G\,\Delta t_E$")
ax.set_title("D1 excess onset", fontsize=9, loc="left", color=INK); ax.grid(True, color=GRID, lw=0.6)
ax.legend(frameon=False, fontsize=8)
ax = axs[1]
kap = np.logspace(0.001, 4, 400)
ax.plot(kap, 1 - 2 / kap, color=INK, lw=1.2, label=r"closed form: $1 - 2/\kappa$")
pts = [(e["kappa"], e["end"] * e["F"] * e["p"]["Pi"] * (2 - e["p"]["c"]) / e["p"]["c"])
       for e in a8["families"]["D2"].get("excess_points", [])]
if pts:
    ax.plot(*zip(*pts), "o", ms=3, mfc="none", color=COLS[1], label="classifier (A3 sets)")
ax.set_xscale("log"); ax.set_xlabel(r"$\kappa = c/(F\Pi_0)$"); ax.set_ylabel(r"$F\Pi\,\Delta t_E\,(2-c)/c$")
ax.set_title("D2 excess onset", fontsize=9, loc="left", color=INK); ax.grid(True, color=GRID, lw=0.6)
ax.legend(frameon=False, fontsize=8)
save(fig, "H3_onset_maps")

# ---------------- H4 B3 relative vs u
us = np.logspace(-3, 4, 400)
fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
for j, rho in enumerate((0.5, 1, 2, 3, 10)):
    w = np.sqrt(1 + rho * us)
    ax.plot(us, ((1 + rho) * w + 1 - rho) / (w * (w + 1)), lw=2, color=(COLS + ["#888888"])[j % 5], label=rf"$\rho = {rho}$")
rho = 10
wM = ((rho - 1) + np.sqrt(2 * rho * (rho - 1))) / (1 + rho)
peak = ((1 + rho) * wM + 1 - rho) / (wM * (wM + 1))
r_ = (1 + peak) / 2
w = np.sqrt(1 + rho * us)
inside = ((1 + rho) * w + 1 - rho) / (w * (w + 1)) > r_
ax.fill_between(us, 0, 1, where=inside, color=COLS[3], alpha=0.12, transform=ax.get_xaxis_transform(), lw=0,
                label=rf"window at $\rho = 10$, $r = {r_:.3g}$")
ax.axhline(r_, color=COLS[3], lw=0.8, ls=":")
ax.axhline(1, color=MUTED, lw=0.8, ls="--")
ax.set_xscale("log"); ax.set_xlabel(r"$u = 2\Sigma\Pi/\lambda^2$"); ax.set_ylabel(r"relative error $\sigma^2/F$")
ax.set_title(r"B3: $\Sigma$-tracking gain with precision over-trust $\rho$", fontsize=9, loc="left", color=INK)
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8)
save(fig, "H4_B3_relative")

# ---------------- H5 B2 and B3 absolute vs relative
ps = {"lam": 1, "Pi": 1, "G": 1, "rho": 3}
us = np.logspace(-4, 4, 400)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
for ax, conv, ttl in ((axs[0], "abs", r"absolute: $\sigma^2$"), (axs[1], "rel", r"relative: $\sigma^2/F$")):
    for fam, col, lab in (("B2", COLS[0], r"B2 ($G = 1$ fixed)"), ("B3", COLS[1], r"B3 ($\rho = 3$)"), ("B5", COLS[2], "B5 (optimal)")):
        f, _, _ = sig_funcs(fam, conv, ps)
        ax.plot(us, [float(f(mp.mpf(float(u)))) for u in us], color=col, lw=2, label=lab)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel(r"$u = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)")
    ax.set_title(ttl, fontsize=9, loc="left", color=INK); ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8)
axs[1].axhline(1, color=MUTED, lw=0.8, ls="--")
save(fig, "H5_B2_B3_abs_rel")
print("figures written")
