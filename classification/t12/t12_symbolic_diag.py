"""Post-hoc diagnosis of the one t12_symbolic failure: A5 'D2 post at dt->oo: lim dt (P+ - (1-c)^2 F) = c[c + 2(1-c) F Pi0]/Pi'.
sympy.limit returned 0. Here: (1) the same limit by series in t = 1/dt with e^{-2 lam / t} dropped (it is beyond all
orders), exact; (2) mp evaluation (dps 80) of dt (P+ - (1-c)^2 F) at dt = 1e10, 1e20, 1e40 on 200 random sets."""
import mpmath as mp
import numpy as np
import sympy as sp

from t12_common import SYM, P0, Pi, Sig, c, _lamb, lam, save_json, x

R = {}
Fs = Sig / lam
target = c * (c + 2 * (1 - c) * Fs * P0) / Pi
e = x * (SYM["D2"]["post"] - (1 - c)**2 * Fs)
R["sympy_limit_again"] = str(sp.limit(e, x, sp.oo))
t, E = sp.symbols("t E", positive=True)
e_t = e.subs(sp.exp(-2 * lam * x), E).subs(x, 1 / t).subs(E, 0)        # e^{-2 lam dt} -> 0 beyond all orders
lim_t = sp.limit(sp.simplify(e_t), t, 0, "+")
R["series_route_limit"] = str(sp.factor(lim_t))
R["series_route_minus_formula"] = str(sp.simplify(lim_t - target))
R["series_route_pass"] = sp.simplify(lim_t - target) == 0
rng = np.random.default_rng(1)
worst = {}
for _ in range(200):
    U = lambda: float(10.0**rng.uniform(-2, 2))
    p = {"lam": U(), "Sig": U(), "Pi": U(), "c": float(2 * 10.0**rng.uniform(-4, 0)), "Pi0": U()}
    fl = _lamb("D2", "post")[0]          # evaluated directly at the outer precision (dt_funcs caps it at dps_for)
    lam_, Sig_, Pi_, c_, P0_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "c", "Pi0"))
    F = Sig_ / lam_
    tg = c_ * (c_ + 2 * (1 - c_) * F * P0_) / Pi_
    for D in (10, 20, 40):
        with mp.workdps(80 + 2 * D):
            lam_, Sig_, Pi_, c_, P0_ = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "c", "Pi0"))
            F = Sig_ / lam_
            tg = c_ * (c_ + 2 * (1 - c_) * F * P0_) / Pi_
            dt = mp.power(10, D)
            v = dt * (fl(dt, lam_, Sig_, Pi_, mp.mpf(1), c_, P0_, mp.mpf(1)) - (1 - c_)**2 * F)
            worst[D] = max(worst.get(D, 0), abs(v / tg - 1))
R["mp_worst_rel_err"] = {f"dt=1e{D}": v for D, v in worst.items()}
R["mp_pass"] = all(worst[D] < mp.power(10, -D + 6) for D in worst)
R["attribution"] = ("code: sympy.limit returns 0 for this expression (a SymPy limit failure in the check route); the "
                    "pre-registered asymptotic is correct (exact series route and mp agree, error O(1/dt))")
print(R)
save_json(R, "t12_symbolic_diag.json")
