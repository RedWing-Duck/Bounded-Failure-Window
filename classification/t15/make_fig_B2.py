"""Task 15 Part C.3: Figure B.2, the normal-form plane (nu, q).
V(nu, q) = (1 + nu q^2/4)/(1 + nu q/2) = sigma^2/F with nu = 2 Sigma Pi/lambda^2 and q = G/(F Pi).
Axes: nu on a log axis, 1e-2 to 1e3; q from 0 to 5. Drawn: the floor crossing q = 2 (sigma^2 > F iff q > 2); the optimal envelope q*(nu) = 2/(1 + sqrt(1 + nu)), where V* = q*;
the tolerance boundaries V = r for r = R^2_rel in {0.5, 1, 2}: q = r +- sqrt(r^2 - 4(1 - r)/nu), real only for nu >= nu_R =
4(1 - r)/r^2 when r < 1. Only q >= 0 is drawn. Labels use words and symbols only, never result numbers.
Usage: python3 make_fig_B2.py"""
import os
import pickle
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
OUT = os.path.join(CLS, "figs_thesis", "B.2_normal-form-plane")
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
INK, MUTED, GRID = "#222222", "#6b6b6b", "#e6e6e6"
RS = (0.5, 1.0, 2.0)
NU = np.logspace(-2, 3, 4000)


def q_star(nu):
    return 2.0 / (1.0 + np.sqrt(1.0 + nu))


def V(nu, q):
    return (1 + nu * q**2 / 4) / (1 + nu * q / 2)


def nu_R(r):
    return 4 * (1 - r) / r**2


def branches(nu, r):
    """(q_minus, q_plus) of the boundary V = r; NaN where it does not exist. |disc| < 1e-12 is treated as 0."""
    nu = np.asarray(nu, dtype=float)
    disc = r**2 - 4 * (1 - r) / nu
    disc = np.where(np.abs(disc) < 1e-12, 0.0, disc)
    root = np.sqrt(np.where(disc >= 0, disc, np.nan))
    return r - root, r + root


def curves():
    """Exactly the arrays drawn (q >= 0 only)."""
    out = {"floor q=2": (NU, np.full_like(NU, 2.0)), "envelope": (NU, q_star(NU))}
    for r in RS:
        qm, qp = branches(NU, r)
        for tag, q in (("minus", qm), ("plus", qp)):
            keep = np.isfinite(q) & (q >= 0)
            if r < 1 and tag == "minus":   # include the touch point so the two branches meet on the envelope
                nuR = nu_R(r)
                x = np.concatenate([[nuR], NU[keep & (NU > nuR)]])
                y = np.concatenate([[r], q[keep & (NU > nuR)]])
                out[f"r={r} {tag}"] = (x, y)
            elif r < 1:
                nuR = nu_R(r)
                out[f"r={r} {tag}"] = (np.concatenate([[nuR], NU[keep & (NU > nuR)]]), np.concatenate([[r], q[keep & (NU > nuR)]]))
            else:
                out[f"r={r} {tag}"] = (NU[keep], q[keep])
    return out


def main(capture=False):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "axes.labelcolor": INK,
                         "legend.frameon": False, "legend.fontsize": 8, "lines.linewidth": 2})
    cv = curves()
    fig, ax = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    ax.plot(*cv["floor q=2"], color=INK, lw=1.2, label=r"floor crossing $q = 2$ ($\sigma^2 > F$ above)")
    ax.plot(*cv["envelope"], color=C1, lw=2.2, label=r"optimal envelope $q_\star(\nu)$, where $\mathcal{V}_\star = q_\star$")
    style = {0.5: (C2, "--"), 1.0: (C3, ":"), 2.0: (C4, "-.")}
    for r in RS:
        col, ls = style[r]
        first = True
        for tag in ("minus", "plus"):
            x, y = cv[f"r={r} {tag}"]
            if len(x):
                ax.plot(x, y, color=col, ls=ls, lw=1.8, label=(rf"boundary $R^2_{{\mathrm{{rel}}}} = {r:g}$" if first else None))
                first = False
    r = 0.5
    ax.plot([nu_R(r)], [r], "o", color=C2, ms=5, label=r"envelope touch $(\nu_R, R^2_{\mathrm{rel}})$")
    ax.set_xscale("log")
    ax.set_xlim(1e-2, 1e3)
    ax.set_ylim(0, 5)   # "q from 0 to about 4": 5 so the R^2_rel = 2 boundary (asymptote q = 4 from above) is visible
    ax.set_xlabel(r"$\nu = 2\Sigma\Pi/\lambda^2$")
    ax.set_ylabel(r"$q = G/(F\Pi)$")
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    if capture:
        sys.path.insert(0, HERE)
        import fig_harness
        rec = {"B.2_normal-form-plane": {"arrays": fig_harness._arrays(fig), "texts": fig_harness._texts(fig)}}
        with open(os.path.join(HERE, "results", "cap_B2.pkl"), "wb") as fh:
            pickle.dump(rec, fh)
    for ext in ("png", "pdf"):
        fig.savefig(f"{OUT}.{ext}", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main(capture=True)
