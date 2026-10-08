"""Figures G1-G4 for Task 11 (PNG + PDF in figs/)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np

from t11_common import (COLS, FIGS, P_delay, Curve, ZREL, analyse_with_limits, classify, limits_pow, power_curve,
                        samp_metrics, sstar)

INK, MUTED, GRID = "#222222", "#6b6b6b", "#e6e6e6"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED})
lam, Sig, K, Pi = 1.0, 0.01, 1.0, 1.0


def save(fig, nm):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIGS, f"{nm}.{ext}"), dpi=300)
    plt.close(fig)


def P_np(tau, beta):
    v = K / 2 * tau**(beta - 1)
    A = (1 - lam * tau)**2 / tau
    B = 4 * (Sig + lam * v)
    C = 4 * Sig * v
    return 2 * C / (B + np.sqrt(B**2 + 4 * A * C))


# ---------------- G1
betas = np.linspace(-2, 4, 241)
y = np.linspace(-6, 6, 241)
dense = np.logspace(-14, 14, 4001)
Z = np.zeros((len(y), len(betas)))
for j, b in enumerate(betas):
    with np.errstate(all="ignore"):
        sup = np.nanmax(P_np(dense, b))
    Z[:, j] = P_np(10.0**y, b) / sup
locus_b, locus_y = [], []
for k in range(1, 40):
    b = mp.mpf(k) / 20
    Lm, Lp, xm, xp = limits_pow(b, mp.mpf(K), mp.mpf(lam), mp.mpf(Sig))
    A = analyse_with_limits(power_curve(b, mp.mpf(K), mp.mpf(lam), mp.mpf(Sig)), Lm, Lp, xm, xp)
    for t in A["turns"]:
        locus_b.append(float(b))
        locus_y.append(float(mp.log10(t["theta"])))
fig, ax = plt.subplots(figsize=(7, 4.4), constrained_layout=True)
pc = ax.pcolormesh(betas, y, Z, cmap="viridis", shading="auto", vmin=0, vmax=1)
fig.colorbar(pc, ax=ax, label=r"$P / \sup_\tau P$")
ax.plot(locus_b, locus_y, color="white", lw=1.6, label="turning point (maximum)")
for xb, lab in ((0, "ordered\n(info ↑ in τ)"), (2, "ordered\n(info ↓ in τ)")):
    ax.axvline(xb, color="white", lw=1.0, ls="--")
ax.text(1.0, 5.3, "spectra cross\n(window)", color="white", ha="center", va="top", fontsize=8)
ax.text(-1.0, 5.3, "ordered\n(lower ray)", color="white", ha="center", va="top", fontsize=8)
ax.text(3.0, 5.3, "ordered\n(upper ray)", color=INK, ha="center", va="top", fontsize=8)
ax.plot([0], [-5.4], marker="v", color=COLS[1], ms=8)
ax.plot([1], [-5.4], marker="v", color=COLS[1], ms=8)
ax.text(0.05, -5.4, "Stage 2", color="white", fontsize=7, va="center")
ax.text(1.05, -5.4, "Stage 3", color="white", fontsize=7, va="center")
ax.set_xlabel(r"power exponent $\beta$"); ax.set_ylabel(r"$\log_{10} \lambda\tau$")
ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor="white")
save(fig, "G1_power_phase")

# ---------------- G2 spectra
om = np.logspace(-3, 3, 400)
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True, sharey=False)
for ax, b, ttl in ((axs[0], 0.0, r"$\beta = 0$ (matched zero-frequency power): nested"),
                   (axs[1], 1.0, r"$\beta = 1$ (matched variance): spectra cross")):
    for t, col, ls in ((0.5, COLS[0], "-"), (2.0, COLS[1], "--")):
        ax.plot(om, K * t**b / (1 + t**2 * om**2), color=col, lw=2, ls=ls, label=rf"$S_\tau$, $\tau = {t}$")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(True, color=GRID, lw=0.6)
    ax.set_xlabel(r"frequency $\omega$"); ax.set_ylabel(r"noise spectrum $S(\omega)$")
    ax.set_title(ttl, fontsize=9, loc="left", color=INK); ax.legend(frameon=False, fontsize=8)
w_star = np.sqrt((2.0 - 0.5) / (0.25 * 4 * (1 / 0.5 - 1 / 2.0)))
axs[1].axvline(w_star, color=MUTED, lw=0.8, ls=":")
axs[1].annotate(rf"$\omega^\star = {w_star:.3g}$", (w_star, axs[1].get_ylim()[0]), xytext=(4, 10), textcoords="offset points", color=INK, fontsize=8)
save(fig, "G2_spectra")

# ---------------- G3 delay
lm, Sm, Pm = mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi)
s2 = sstar(lm, Sm, Pm)
Pe = P_delay(1 / mp.e, lm, Sm, Pm)
F = Sm / lm
f = lambda th: P_delay(th * mp.exp(-th), lm, Sm, Pm)
dd = lambda th: 2 * lm * mp.exp(-2 * lm * th * mp.exp(-th)) * (F - s2) * (1 - th) * mp.exp(-th)
A = analyse_with_limits(Curve(f, dd, lambda th: ZREL * abs(f(th)) / th, 0, [mp.mpf(0)], None, "d"), s2, s2, mp.mpf(-80), mp.mpf(80))
R2 = s2 + (Pe - s2) / 2
a, b = (float(x) for x in classify(A, R2)["ends"][0])
th = np.logspace(-2, 1.5, 500)
fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
ax.plot(th, [float(f(mp.mpf(float(x)))) for x in th], color=COLS[0], lw=2, label=r"optimal $P(d(\theta))$, $d = \theta e^{-\theta}$")
ax.axvspan(a, b, color=COLS[1], alpha=0.18, lw=0, label=r"window at $R^2 = \sigma_\star^2 + \frac{1}{2}(P(1/e) - \sigma_\star^2)$")
ax.axhline(float(R2), color=COLS[1], lw=0.8, ls=":")
ax.axhline(float(s2), color=MUTED, lw=0.8, ls="--", label=r"$\sigma_\star^2$ (no delay)")
ax.axvline(1, color=MUTED, lw=0.8, ls="-.", label=r"$\theta = 1$ ($d = 1/e$)")
ax.set_xscale("log"); ax.set_xlabel(r"$\theta$"); ax.set_ylabel("optimal filtering error")
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=8, loc="upper left")
save(fig, "G3_delay")

# ---------------- G4 sampling
dts = np.logspace(-3, 2, 300)
ma = np.array([float(samp_metrics(mp.mpf(float(x)), lm, Sm, Pm)[0]) for x in dts])
mb = np.array([float(samp_metrics(mp.mpf(float(x)), lm, Sm, Pm)[1]) for x in dts])
fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
ax.plot(dts, ma, color=COLS[0], lw=2, label=r"(a) posterior MSE at sample times")
ax.plot(dts, mb, color=COLS[1], lw=2, ls="--", label=r"(b) time-averaged MSE")
for base, mk, col, lab in ((2, "o", COLS[2], r"chain $0.01\cdot 2^k$"), (3, "s", COLS[3], r"chain $0.01\cdot 3^k$")):
    ch = [0.01 * base**k for k in range(0, 20) if 0.01 * base**k <= 100]
    ax.plot(ch, [float(samp_metrics(mp.mpf(c), lm, Sm, Pm)[1]) for c in ch], mk, color=col, ms=5, mfc="none", label=lab)
ax.axhline(float(s2), color=MUTED, lw=0.8, ls=":", label=r"$\sigma_\star^2$ (continuous observation)")
ax.axhline(float(F), color=MUTED, lw=0.8, ls="--", label=r"$F$")
ax.set_xscale("log"); ax.set_xlabel(r"sampling interval $\Delta t$"); ax.set_ylabel("optimal error")
ax.grid(True, color=GRID, lw=0.6); ax.legend(frameon=False, fontsize=7.5, loc="center left")
save(fig, "G4_sampling")
print("figures written")
