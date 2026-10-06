"""T7.4: revision figures (no titles; 300 dpi; 4.7 in wide = 72 % of a 6.5 in text width).
Uses saved Task 3 simulation points; no simulation is run."""
import json
import os
import struct

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import C, COLS, F, FIG, H, RES, Timer, dump, g_kalman, g_opt, var_cf
from t7_common import peak, pi0_of

W, HGT, DPI = 4.7, 3.3, 300
plt.rcParams.update({"font.size": 8, "axes.labelsize": 9, "legend.fontsize": 7.5,
                     "xtick.labelsize": 8, "ytick.labelsize": 8})
MUTED = "#52514e"


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)


TITLES = {}


def save(fig, name):
    TITLES[name] = [t for a in fig.get_axes() for t in (a.get_title("left"), a.get_title("center"),
                                                         a.get_title("right")) if t] + \
        ([fig._suptitle.get_text()] if fig._suptitle else [])
    path = os.path.join(FIG, name)
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


with Timer() as T:
    t3 = json.load(open(os.path.join(RES, "t3.json")))
    grid = np.array(t3["grid"])
    sim = {k: np.array(v) for k, v in t3["sim"].items()}
    se = {k: np.array(v) for k, v in t3["se"].items()}

    # ---------------- Figure 1: paired relays + inset (calibrated - optimal)
    fig, ax = plt.subplots(figsize=(W, HGT))
    pf = np.logspace(-2, 2, 500)
    gf = {"a": g_kalman(pf, 1.0), "b": g_kalman(pf, 100.0), "c": g_opt(pf)}
    lab = {"a": r"$\Pi_0 = 1$ ($\kappa = 100$)", "b": r"$\Pi_0 = 100$ ($\kappa = 1$)", "c": "optimal"}
    mk = {"a": "o", "b": "s", "c": "^"}
    ax.axvspan(1 / 9, 4, color="#f3e1d9", zorder=0, lw=0)
    ax.axhline(0.05, ls="--", lw=0.9, color=MUTED)
    ax.text(1.12e-2, 0.053, "R² = 0.05", fontsize=7, color=MUTED)
    for i, k in enumerate("abc"):
        ax.plot(pf, var_cf(pf, gf[k]), color=COLS[i], lw=1.6, label=lab[k])
        ax.errorbar(grid, sim[k], yerr=se[k], fmt=mk[k], ms=3.2, color=COLS[i], mfc="white", mew=0.9,
                    elinewidth=0.8, capsize=0, zorder=3)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_ylim(6e-3, 0.5)
    ax.set_xlabel("sensory precision Π"); ax.set_ylabel("stationary variance σ²")
    ax.legend(frameon=False, loc="upper right")
    style(ax)
    ins = ax.inset_axes([0.12, 0.70, 0.36, 0.27])
    pi_in = np.logspace(-2, 2, 400)
    d = var_cf(pi_in, g_kalman(pi_in, 100.0)) - var_cf(pi_in, g_opt(pi_in))
    ins.plot(pi_in, d * 1e4, color=COLS[1], lw=1.3)
    ins.set_xscale("log")
    ins.set_xticks([1e-2, 1, 1e2])
    ins.tick_params(labelsize=6.5, length=2)
    ins.set_ylabel(r"$\Delta\sigma^2$ ($\times 10^{-4}$)", fontsize=6.5, labelpad=1)
    ins.text(0.03, 0.95, r"$\Pi_0 = 100$ minus optimal", transform=ins.transAxes, fontsize=6.5,
             va="top", color=MUTED)
    ins.set_xlabel(r"$\Pi$", fontsize=6.5, labelpad=0)
    ins.set_facecolor("white")
    style(ins)
    p1 = save(fig, "fig1_paired.png")
    inset_info = {"diff_at_0.01": float(d[0]), "diff_at_1": float(np.interp(0, np.log(pi_in), d)),
                  "diff_at_100": float(d[-1])}

    # ---------------- Figure 2: regimes (Pi_0 = 1, kappa = 100)
    s1 = lambda p: var_cf(p, g_kalman(p, 1.0))
    _, M = peak(1.0)
    fig, ax = plt.subplots(figsize=(W, HGT))
    pf = np.logspace(-3, 4, 800)
    ylo, yhi = 3e-3, 0.2
    bands = [(ylo, H, "never satisfied", "#e8e8e6", 1.3e-3, "left"),
             (H, F, r"threshold: satisfied above a cutoff $\Pi$", "#d9e7f7", 1.3e-3, "left"),
             (F, M, "window: fails inside\na bounded $\\Pi$ interval", "#f8ddd0", 8e3, "right"),
             (M, yhi, "always satisfied", "#ffffff", 1.3e-3, "left")]
    for lo, hi, lb, col, xt, ha in bands:
        ax.axhspan(lo, hi, color=col, lw=0, zorder=0)
        ax.text(xt, np.sqrt(lo * hi), lb, va="center", ha=ha, fontsize=7)
    ax.fill_between(pf, ylo, s1(pf), color="#0b0b0b", alpha=0.10, lw=0, label="fails (σ² > R²)")
    ax.plot(pf, s1(pf), color=COLS[0], lw=1.6, label=r"$\sigma^2(\Pi)$, $\Pi_0 = 1$ ($\kappa = 100$)")
    for v, nm in ((H, "H"), (F, "F"), (M, "M")):
        ax.axhline(v, color=MUTED, lw=0.7)
        ax.text(1.15e4, v, nm, va="center", ha="left", fontsize=7.5, color=MUTED)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(ylo, yhi); ax.set_xlim(1e-3, 1e4)
    ax.set_xlabel("sensory precision Π"); ax.set_ylabel("requirement R² (pass iff σ² ≤ R²)")
    ax.legend(frameon=False, loc="upper right")
    style(ax)
    p2 = save(fig, "fig2_regimes.png")

    # ---------------- Figure 3: M/F vs kappa
    kg = np.logspace(0, 3, 2000)
    MF = np.array([peak(pi0_of(k))[1] for k in kg]) / F
    tab = [2, 3, 5, 10, 20, 50, 100]
    MFt = np.array([peak(pi0_of(k))[1] for k in tab]) / F
    fig, ax = plt.subplots(figsize=(W, HGT))
    ax.plot(kg, MF, color=COLS[0], lw=1.6, label="closed form")
    ax.plot(tab, MFt, "o", ms=4.5, mfc="white", mec=COLS[0], mew=1.1, zorder=3, label="Section 4 table")
    ax.axhline(5, ls="--", lw=0.9, color=MUTED)
    ax.text(950, 5.4, "R²/F = 5 (R² = 0.05)", fontsize=7, color=MUTED, ha="right")
    for kv, txt in ((2, "κ = 2\nonset of window"), (50, "κ = 50\nM = R²")):
        ax.axvline(kv, ls=":", lw=0.9, color=MUTED)
        ax.text(kv * 1.08, 30, txt, fontsize=7, color=MUTED, va="center")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1, 1000)
    ax.set_xlabel(r"over-weighting ratio $\kappa = (c/\Pi_0)/F$"); ax.set_ylabel("peak height M/F")
    ax.legend(frameon=False, loc="lower right")
    style(ax)
    p3 = save(fig, "fig3_peak_vs_kappa.png")


def png_info(path):
    with open(path, "rb") as f:
        data = f.read()
    w, h = struct.unpack(">II", data[16:24])
    i = data.find(b"pHYs")
    ppm = struct.unpack(">I", data[i + 4:i + 8])[0] if i > 0 else None
    return {"px": [w, h], "dpi": round(ppm * 0.0254) if ppm else None, "width_in": w / DPI}


info = {os.path.basename(p): png_info(p) for p in (p1, p2, p3)}
no_titles = all(not t for t in TITLES.values())
ok = all(v["dpi"] == DPI and abs(v["width_in"] - W) < 0.01 for v in info.values()) and no_titles
for k, v in info.items():
    print(k, v)
print("inset (calibrated - optimal):", inset_info)
print(f"T7.4: {'PASS' if ok else 'FAIL'}  ({T.dt:.1f}s)")
dump("t7_4.json", {"pass": ok, "files": info, "inset": inset_info, "no_titles": no_titles, "titles_found": TITLES,
                   "M_over_F_at_1000": float(MF[-1]), "runtime_s": T.dt})
