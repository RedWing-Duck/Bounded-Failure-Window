"""T9.5 diagnosis (post hoc, not a pass criterion): are the 'V not strictly decreasing' and 'V < P' samples real?

Recomputes the pre-registered float64 V along each set's grid, collects the failing samples, and recomputes V there in
mpmath (60 digits): the stationary point of sigma2 in G is refined by findroot from the float64 argmin, and V_mp is the
smaller of that value and the G -> oo limit 1/(2 Pi tau)."""
import mpmath as mp
import numpy as np
import sympy as sp

from t9_common import P_opt, V_best, draw_sets, save_json

mp.mp.dps = 60
_G, _t, _l, _S, _P = sp.symbols("G tau lambda Sigma Pi", positive=True)
_a = _l + _G
_s2 = (_S + _G**2 / (2 * _P * (1 + _a * _t))) / _a
s2f = sp.lambdify((_G, _t, _l, _S, _P), _s2, "mpmath")
ds2f = sp.lambdify((_G, _t, _l, _S, _P), sp.diff(_s2, _G), "mpmath")


def V_mp(tau, lam, Sig, Pi, G0):
    t, l, S, P = (mp.mpf(x) for x in (tau, lam, Sig, Pi))
    cand = [1 / (2 * P * t)]
    try:
        g = mp.findroot(lambda u: ds2f(mp.exp(u), t, l, S, P), mp.log(mp.mpf(G0)))
        cand.append(s2f(mp.exp(g), t, l, S, P))
    except (ValueError, ZeroDivisionError):
        pass
    return min(cand)


sets = draw_sets(np.random.default_rng(9004), 2000)
bad_dec, bad_lt = [], []
for i in range(2000):
    lam, Sig, Pi, _ = (float(x) for x in sets[i])
    taus = np.logspace(-6, 6, 200) / lam
    prev = None
    for j, t in enumerate(taus):
        V, Gb, _n = V_best(t, lam, Sig, Pi)
        Pm = P_opt(mp.mpf(t), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
        if prev is not None and not V < prev[0]:
            bad_dec.append((i, j, t, prev, (V, Gb)))
        if V < float(Pm):
            bad_lt.append((i, j, t, V, Gb, Pm))
        prev = (V, Gb, t)

dec_rows, n_dec_real = [], 0
for i, j, t, (Vp, Gp, tp), (V, Gb) in bad_dec:
    lam, Sig, Pi, _ = (float(x) for x in sets[i])
    v1, v2 = V_mp(tp, lam, Sig, Pi, Gp), V_mp(t, lam, Sig, Pi, Gb)
    real = not v2 < v1
    n_dec_real += int(real)
    dec_rows.append({"set": i, "lam_tau": lam * t, "float_V_prev": Vp, "float_V": V,
                     "mp_rel_drop": float((v1 - v2) / v1), "mp_strictly_decreasing": not real,
                     "on_G_inf_limit": bool(abs(V - 1 / (2 * Pi * t)) <= 1e-15 * V)})
lt_rows, n_lt_real = [], 0
for i, j, t, V, Gb, Pm in bad_lt:
    lam, Sig, Pi, _ = (float(x) for x in sets[i])
    vm = V_mp(t, lam, Sig, Pi, Gb)
    real = vm < Pm
    n_lt_real += int(real)
    lt_rows.append({"set": i, "lam_tau": lam * t, "float_V_minus_P_rel": float((V - Pm) / Pm),
                    "mp_V_minus_P_rel": float((vm - Pm) / Pm), "real": bool(real)})

out = {"n_not_decreasing": len(dec_rows), "n_not_decreasing_real_in_mp": n_dec_real,
       "max_mp_rel_drop_at_flagged": max((r["mp_rel_drop"] for r in dec_rows), default=None),
       "min_mp_rel_drop_at_flagged": min((r["mp_rel_drop"] for r in dec_rows), default=None),
       "lam_tau_range_not_decreasing": [min((r["lam_tau"] for r in dec_rows), default=None),
                                        max((r["lam_tau"] for r in dec_rows), default=None)],
       "n_on_G_inf_limit": sum(r["on_G_inf_limit"] for r in dec_rows),
       "n_V_lt_P": len(lt_rows), "n_V_lt_P_real_in_mp": n_lt_real,
       "min_mp_V_minus_P_rel_at_flagged": min((r["mp_V_minus_P_rel"] for r in lt_rows), default=None),
       "lam_tau_range_V_lt_P": [min((r["lam_tau"] for r in lt_rows), default=None),
                                max((r["lam_tau"] for r in lt_rows), default=None)],
       "dec_rows": dec_rows[:60], "lt_rows": lt_rows}
print(f"not strictly decreasing (float64): {len(dec_rows)}; real in mp: {n_dec_real}; mp relative drop at flagged "
      f"points in [{out['min_mp_rel_drop_at_flagged']:.3g}, {out['max_mp_rel_drop_at_flagged']:.3g}]; lam*tau in "
      f"{out['lam_tau_range_not_decreasing']}; on the G -> oo limit: {out['n_on_G_inf_limit']}")
print(f"V < P (float64): {len(lt_rows)}; real in mp: {n_lt_real}; min mp (V - P)/P at flagged points "
      f"{out['min_mp_V_minus_P_rel_at_flagged']:.3g}; lam*tau in {out['lam_tau_range_V_lt_P']}")
save_json(out, "t9_5_diag.json")
