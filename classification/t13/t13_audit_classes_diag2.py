"""Post-hoc diagnosis of C2 row 8 (part 2): (1, 0, 1) is impossible for the two-stage Bayesian gain.
Claim: let G > 0, G' > 0 and Pi G' < G (G(Pi)/Pi strictly decreasing), and f = (Sig + G^2/(2 Pi))/(lam + G), F = Sig/lam.
Then f' < 0 wherever f <= F. Hence every interior local minimum of f exceeds F, so no tolerance R2 < F lies above a
minimum: a lower ray (needs R2 < F) and a window (needs R2 > m >= ... > F) never coexist, and (1, 0, k), k >= 1, is impossible.
Proof steps checked here with SymPy:
 (1) 2 Pi^2 (lam + G)^2 f' = Pi G' (2 lam G + G^2 - 2 Pi Sig) - G^2 (lam + G)          (identity)
 (2) f <= F  <=>  lam G^2 <= 2 Pi Sig G  <=>  2 Pi Sig >= lam G                          (G > 0)
 (3) then the bracket in (1) is <= G (lam + G), so (1) <= G (lam + G)(Pi G' - G) < 0     (G' > 0, Pi G' < G)
 (4) Bayes stages G_i = c_i Pi/(Pi + a_i): Pi G_i' - G_i = -c_i Pi^2/(Pi + a_i)^2 < 0, so any sum of stages qualifies.
Numerical check: min over the C2 row-8 curves of m/F at interior minima (must be > 1).
Usage: python3 t13_audit_classes_diag2.py"""
import mpmath as mp
import numpy as np
import sympy as sp

import t13_audit_classes as AC
from t13_common import save_json


def symbolic():
    Pi, lam, Sig, G, Gp, c, a = sp.symbols("Pi lam Sig G Gp c a", positive=True)
    g = sp.Function("g")(Pi)
    f = (Sig + g**2 / (2 * Pi)) / (lam + g)
    lhs = sp.simplify(2 * Pi**2 * (lam + g)**2 * sp.diff(f, Pi))
    rhs = Pi * sp.diff(g, Pi) * (2 * lam * g + g**2 - 2 * Pi * Sig) - g**2 * (lam + g)
    s1 = sp.simplify(sp.expand(lhs - rhs)) == 0
    # (2): F - f = (2 Pi Sig - lam G) G / (2 Pi lam (lam + G))
    s2 = sp.simplify(Sig / lam - (Sig + G**2 / (2 * Pi)) / (lam + G) - (2 * Pi * Sig - lam * G) * G / (2 * Pi * lam * (lam + G))) == 0
    # (3): bracket - G(lam+G) = lam G - 2 Pi Sig = -(2 Pi Sig - lam G) <= 0 on f <= F
    s3 = sp.simplify((2 * lam * G + G**2 - 2 * Pi * Sig) - G * (lam + G) + (2 * Pi * Sig - lam * G)) == 0
    Gi = c * Pi / (Pi + a)
    s4 = sp.simplify(Pi * sp.diff(Gi, Pi) - Gi + c * Pi**2 / (Pi + a)**2) == 0
    return {"(1) derivative identity": bool(s1), "(2) f <= F iff 2 Pi Sig >= lam G": bool(s2),
            "(3) bracket bound": bool(s3), "(4) Bayes stage Pi G' - G": bool(s4)}


def numeric():
    rng = np.random.default_rng(13100 + 8)
    ratios = []
    for i in range(1000):
        p = AC.draw(8, rng, i)
        rng.integers(2**63)
        A = AC.analyse_row(8, p)
        F = mp.mpf(p["Sig"]) / mp.mpf(p["lam"])
        ratios += [float(t["value"] / F) for t in A["turns"] if t["kind"] == "min"]
    return {"row8_curves_with_min": len(ratios), "row8_min_m_over_F": min(ratios) if ratios else None}


def main():
    R = {"symbolic": symbolic()}
    print(R["symbolic"], flush=True)
    R["numeric"] = numeric()
    print(R["numeric"], flush=True)
    ok = all(R["symbolic"].values()) and R["numeric"]["row8_min_m_over_F"] > 1
    R["text"] = ("Row 8: proved that f' < 0 wherever f <= F for any positive increasing gain with G/Pi strictly decreasing, "
                 "which includes every sum of Bayesian stages; so interior minima exceed F and (1, 0, k), k >= 1, cannot occur. "
                 f"SymPy steps: {R['symbolic']}; smallest m/F over the {R['numeric']['row8_curves_with_min']} row-8 interior minima: "
                 f"{R['numeric']['row8_min_m_over_F']}. Attribution: document (row 8's stated set wrongly includes (1, 0, 1)). "
                 f"All checks pass: {ok}.")
    R["pass"] = ok
    print(R["text"])
    save_json(R, "t13_audit_classes_diag2.json")


if __name__ == "__main__":
    main()
