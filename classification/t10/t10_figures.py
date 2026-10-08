"""Figures F1-F5 for Task 10 (PNG + PDF in figs/)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from classify import classify
from t10_common import COLS, FIGS, T, analyse, gstar, mpize, pi_curve, sig2
from t10_construct import PL, envelope_target
from t10_tau import P_rat

INK, MUTED, GRID = "#222222", "#6b6b6b", "#e6e6e6"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED})
lam, Sig = 1.0, 0.01
F = Sig / lam


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIGS, f"{name}.{ext}"), dpi=300)
    plt.close(fig)


def s2star(P):
    return (-lam + np.sqrt(lam**2 + 2 * Sig * P)) / P


# ---------------- F1 realizability
R2 = 1.25 * F
nodes = [R2 / 2] + [2 * R2, R2 / 2] * 3
tg = envelope_target(1, 0.01, PL(nodes, 0, 0))
A = analyse(tg.curve())
ends = classify(A, mp.mpf(R2))["ends"]
x = np.linspace(-4, 14, 1500)
P = 10.0**x
env = s2star(P)
vv = np.array([float(tg.val(mp.mpf(float(xx)))) for xx in x])
fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)
ax.fill_between(P, 1e-9, env, color=MUTED, alpha=0.18, lw=0, label=r"forbidden: $v < \sigma_\star^2(\Pi)$")
ax.plot(P, env, color=MUTED, lw=1.2, label=r"envelope $\sigma_\star^2(\Pi)$")
ax.plot(P, vv, color=COLS[0], lw=2, label="constructed curve (3 windows)")
ax.axhline(F, color=INK, lw=0.9, ls="--", label=r"$F$")
ax.axhline(R2, color=COLS[1], lw=0.9, ls=":", label=r"$R^2 = 1.25F$")
for a_, b_ in ends:
    ax.axvspan(float(a_), float(b_), color=COLS[1], alpha=0.2, lw=0)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(1e-6, 0.05)
ax.set_xlabel(r"precision $\Pi$"); ax.set_ylabel(r"stationary variance $\sigma^2$")
ax.grid(True, color=GRID, lw=0.6)
ax.legend(loc="lower left", frameon=False, fontsize=8)
ins = ax.inset_axes([0.6, 0.62, 0.38, 0.33])
r2b = 0.9 * F
piR = 2 * lam * (F - r2b) / r2b**2
xi = np.logspace(-1, 3.5, 400)
ins.plot(xi, s2star(xi), color=MUTED, lw=1.2)
ins.axhline(r2b, color=COLS[1], lw=0.8, ls=":")
ins.axvspan(xi[0], piR, color=COLS[1], alpha=0.2, lw=0)
ins.axvline(piR, color=COLS[1], lw=0.8)
ins.set_xscale("log"); ins.tick_params(labelsize=6)
ins.set_title(rf"forced lower ray $(0, \pi_R)$, $R^2 = 0.9F$, $\pi_R = {piR:.1f}$", fontsize=7, color=INK, loc="left")
save(fig, "F1_realizability")

# ---------------- F2 Hill family
fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)
xs = np.logspace(-3, 4, 700)
styles = ["-", "--", "-.", ":", (0, (5, 1, 1, 1))]
cols5 = [COLS[0], COLS[1], COLS[2], COLS[3], INK]
for P0, ls, col in zip((5, 20, 25, 26, 40), styles, cols5):
    G = xs**2 / (xs**2 + P0**2)
    ax.plot(xs, sig2(G, xs, lam, Sig), color=col, lw=1.6, ls=ls, label=rf"$\Pi_0 = {P0}$")
ax.axhline(F, color=MUTED, lw=0.9, ls="--")
ax.annotate(r"$F$", (xs[-1], F), xytext=(2, 2), textcoords="offset points", color=INK)
ax.set_xscale("log"); ax.set_xlabel(r"precision $\Pi$"); ax.set_ylabel(r"$\sigma^2$")
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8, loc="upper left")
ins = ax.inset_axes([0.58, 0.5, 0.4, 0.42])
A26 = analyse(pi_curve("hill", mpize({"lam": 1.0, "Sig": 0.01, "c": 1.0, "n": 2, "Pi0": 26.0})))
m26, M26 = (float(t["value"]) for t in A26["turns"])
xi = np.logspace(0, 3, 400)
ins.plot(xi, sig2(xi**2 / (xi**2 + 26**2), xi, lam, Sig), color=COLS[3], lw=1.4, ls=":")
ins.axhspan(max(m26, Sig / 2), min(M26, F), color=COLS[2], alpha=0.25, lw=0)
for y, lab in ((m26, "m"), (M26, "M"), (F, "F")):
    ins.axhline(y, color=MUTED, lw=0.6, ls="--")
    ins.annotate(lab, (xi[0], y), xytext=(2, 1), textcoords="offset points", fontsize=7, color=INK)
ins.set_xscale("log"); ins.set_ylim(0.0094, 0.0101); ins.tick_params(labelsize=6)
ins.set_title(r"$\Pi_0 = 26$: mixed band $(m, M)$ below $F$", fontsize=7, color=INK, loc="left")
save(fig, "F2_hill_family")

# ---------------- F3 Hill phase diagram (n = 2, lam = c = 1)
P0s = np.logspace(-2, 4, 160)
Sgs = np.logspace(-4, 0, 140)
Z = np.full((len(Sgs), len(P0s)), np.nan)
REG = np.zeros_like(Z)
for i, S_ in enumerate(Sgs):
    for j, P0 in enumerate(P0s):
        co = [-2.0, -4 * S_ * P0, 3.0, -8 * S_ * P0, 3.0, -4 * S_ * P0]   # Q(t), lam = c = 1
        rts = np.roots(co)
        pos = np.sort([r.real for r in rts if abs(r.imag) < 1e-9 and r.real > 0])
        if len(pos) == 2:
            vals = [sig2(t**2 / (1 + t**2), P0 * t, 1.0, S_) for t in pos]
            m_, M_ = vals
            Fs, Hs = S_, S_ / 2
            band = (min(M_, Fs) - max(m_, Hs)) / Fs
            Z[i, j] = np.log10(band) if band > 0 else np.nan
            REG[i, j] = 2 if M_ > Fs else 1
fig, ax = plt.subplots(figsize=(6.4, 4.6), constrained_layout=True)
pc = ax.pcolormesh(P0s, Sgs, Z, cmap="viridis", shading="auto")
cb = fig.colorbar(pc, ax=ax)
cb.set_label(r"$\log_{10}$ mixed-band width $/F$")
ax.contour(P0s, Sgs, REG, levels=[0.5, 1.5], colors=[INK, COLS[1]], linewidths=[1.2, 1.2], linestyles=["-", "--"])
ax.plot(P0s, 1 / (4 * P0s), color=COLS[1], lw=0.8, ls=":", label=r"$\Pi_0 = c\lambda/(4\Sigma)$ (window onset)")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(Sgs[0], Sgs[-1])
ax.set_xlabel(r"$\Pi_0$"); ax.set_ylabel(r"$\Sigma$")
ax.text(0.03, 0.05, "monotone (no turning point)", transform=ax.transAxes, color=INK, fontsize=8)
ax.text(0.5, 0.92, "min-max pair: window above F (left of dashed),\npair below F (between dashed and solid)",
        transform=ax.transAxes, color=INK, fontsize=7, ha="center", va="top")
ax.legend(frameon=False, fontsize=7, loc="lower right")
save(fig, "F3_hill_phase")

# ---------------- F4 peak heights
xg = np.linspace(2.0005, 100, 600)


def peak_bayes(kap):
    c = 1.0
    P0 = c * lam / (kap * Sig)
    Gr = -lam + np.sqrt(lam**2 + lam * c - 2 * Sig * P0)
    Pr = P0 * Gr / (c - Gr)
    return sig2(Gr, Pr, lam, Sig) / F


def peak_mis(x):
    l1 = 1.0
    S1 = x * F * l1
    r = Sig / S1
    a2, b1, c0 = 1 + r, 4 * r * l1, 2 * lam * l1 - 4 * r * l1**2
    G = 2 * c0 / (b1 + np.sqrt(b1**2 + 4 * a2 * c0))
    Pr = (G**2 + 2 * l1 * G) / (2 * S1)
    return sig2(G, Pr, lam, Sig) / F


yb = np.array([peak_bayes(k) for k in xg])
ym = np.array([peak_mis(k) for k in xg])
fig, ax = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
ax.plot(xg, yb, color=COLS[0], lw=2, label=r"Bayesian-weight, $x = \kappa$")
ax.plot(xg, ym, color=COLS[1], lw=2, ls="--", label=r"misspecified Kalman, $x = F'/F$ ($\lambda' = 1$)")
b100, m100 = peak_bayes(100.0), peak_mis(100.0)
for y, col in ((b100, COLS[0]), (m100, COLS[1])):
    ax.plot([100], [y], "o", color=col, ms=6)
ax.annotate(f"x = 100: {b100:.3f} and {m100:.3f}\nratio {m100 / b100:.3f}", (100, m100), xytext=(-150, -10),
            textcoords="offset points", color=INK, fontsize=8)
ax.set_xlabel("over-weighting ratio x"); ax.set_ylabel(r"peak height $M/F$")
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8, loc="upper left")
save(fig, "F4_peak_heights")
F4_VALUES = {"bayes_M_over_F_at_100": b100, "misspec_M_over_F_at_100": m100, "ratio_misspec_over_bayes": m100 / b100}

# ---------------- F5 matched-variance tau
v, G = 0.05, 0.5
a = lam + G
tau = np.logspace(-4, 4, 800)
Pt = np.array([float(P_rat(mp.mpf(float(t)), mp.mpf(lam), mp.mpf(Sig), mp.mpf(v))) for t in tau])
rel = (Sig + G**2 * v * tau / (1 + a * tau)) / a
Pmax = Sig * v / (Sig + lam * v)
r2c = 0.8 * Pmax
B = 4 * (Sig + lam * v)
AR = (4 * Sig * v - B * r2c) / r2c**2
disc = (2 * lam + AR)**2 - 4 * lam**2
tm, tp = ((2 * lam + AR) - np.sqrt(disc)) / (2 * lam**2), ((2 * lam + AR) + np.sqrt(disc)) / (2 * lam**2)
fig, ax = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
ax.plot(tau, Pt, color=COLS[1], lw=2, label=r"optimal $P(\tau)$")
ax.plot(tau, rel, color=COLS[0], lw=2, ls="--", label=r"relay $\sigma^2(\tau)$, $G = 0.5$")
ax.axvspan(tm, tp, color=COLS[1], alpha=0.15, lw=0, label=rf"optimal window at $R^2 = 0.8P_{{\max}}$ ($\tau_-\tau_+ = 1/\lambda^2$)")
ax.axhline(r2c, color=COLS[1], lw=0.8, ls=":")
ax.axvline(1 / lam, color=MUTED, lw=0.8, ls="-.", label=r"$\tau = 1/\lambda$")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"noise correlation time $\tau$ (Var $\eta = v$ fixed)"); ax.set_ylabel("stationary error variance")
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8, loc="lower center")
save(fig, "F5_matched_variance")

import json  # noqa: E402
from t10_common import RES  # noqa: E402
json.dump(F4_VALUES, open(os.path.join(RES, "t10_fig.json"), "w"), indent=1)
print("figures written;", F4_VALUES)
