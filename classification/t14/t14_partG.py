"""Task 14 Part G (PREREG_t14.md): SymPy checks of thesis-only results 3.2 (normal form) and 6.5 (normalised optimal error
along tau), in the reading nu = 2 Sigma Pi / lambda^2, q = G/(F Pi), t = lambda tau.
Usage: python3 t14_partG.py"""
import random

import mpmath as mp
import sympy as sp

from t14_common import save_json

lam, Sig, Pi, G, nu, q, v, t, tau = sp.symbols("lambda Sigma Pi G nu q v t tau", positive=True)
F = Sig / lam
V = (1 + nu * q**2 / 4) / (1 + nu * q / 2)


def zero(e):
    e = sp.simplify(e)
    if e != 0:
        e = sp.simplify(sp.together(sp.expand(e)))
    return e == 0


def main():
    R = {}
    sub = {G: q * F * Pi, nu: 2 * Sig * Pi / lam**2}
    sig2 = (Sig + G**2 / (2 * Pi)) / (lam + G)
    R["G1 normal form"] = zero((sig2 / F).subs(G, q * F * Pi) - V.subs(nu, 2 * Sig * Pi / lam**2))
    R["G2 dV/dq"] = zero(sp.diff(V, q) - nu * (nu * q**2 / 4 + q - 1) / (2 * (1 + nu * q / 2)**2))
    R["G2 dV/dnu"] = zero(sp.diff(V, nu) - q * (q - 2) / (4 * (1 + nu * q / 2)**2))
    qp = v + sp.sqrt(v**2 - 4 * (1 - v) / nu)
    qm = v - sp.sqrt(v**2 - 4 * (1 - v) / nu)
    R["G3 level-set root q+"] = zero(V.subs(q, qp) - v)
    R["G3 level-set root q-"] = zero(V.subs(q, qm) - v)
    qs = 2 * (sp.sqrt(1 + nu) - 1) / nu
    R["G4 q* solves nu q^2/4 + q - 1 = 0"] = zero(nu * qs**2 / 4 + qs - 1)
    R["G4 V(q*) = q*"] = zero(V.subs(q, qs) - qs)
    sstar = 2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * Pi))
    R["G4 q* = sigma*^2/F"] = zero(qs.subs(nu, 2 * Sig * Pi / lam**2) - sstar / F)
    # G5: G = q+(v/F) F Pi equals G+(v, Pi) = Pi v + sqrt(Pi (Pi v^2 + 2 lam v - 2 Sigma))
    w = sp.symbols("w", positive=True)   # w = variance v (not normalised)
    Gq = (qp.subs(v, w / F) * F * Pi).subs(nu, 2 * Sig * Pi / lam**2)
    Gplus = Pi * w + sp.sqrt(Pi * (Pi * w**2 + 2 * lam * w - 2 * Sig))
    d = sp.simplify(Gq - Gplus)
    if d != 0:   # compare the square-root parts (both non-negative where real)
        ra = sp.simplify((Gq - Pi * w)**2 - (Gplus - Pi * w)**2)
        d = ra
    R["G5 inverse map reproduces G+"] = d == 0
    # G6: P/F from Proposition 16 (v1) equals 2/(1 + nu t + sqrt((1 + nu t)^2 + nu (1 - t)^2))
    b = 4 * Sig * tau + 2 * lam / Pi
    D = b**2 + 8 * Sig * (1 - lam * tau)**2 / Pi
    P = 4 * Sig / (Pi * (b + sp.sqrt(D)))
    form = 2 / (1 + nu * t + sp.sqrt((1 + nu * t)**2 + nu * (1 - t)**2))
    e6 = (P / F) - form.subs({nu: 2 * Sig * Pi / lam**2, t: lam * tau})
    R["G6 symbolic"] = zero(e6)
    mp.mp.dps = 60
    rng = random.Random(14001)
    worst = mp.mpf(0)
    f6 = sp.lambdify((lam, Sig, Pi, tau), e6, "mpmath")
    for _ in range(20):
        vals = [mp.mpf(rng.randint(1, 1000)) / rng.randint(1, 1000) for _ in range(4)]
        worst = max(worst, abs(f6(*vals)))
    R["G6 numeric 20 rational points (max |diff|)"] = mp.nstr(worst, 5)
    R["G6 numeric pass"] = worst < mp.mpf("1e-50")
    ok = all(v_ for k, v_ in R.items() if isinstance(v_, bool))
    for k, v_ in R.items():
        print(f"{k}: {v_}")
    print("Part G:", "PASS" if ok else "FAIL")
    R["pass"] = ok
    save_json(R, "t14_partG.json")


if __name__ == "__main__":
    main()
