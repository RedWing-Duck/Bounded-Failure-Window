"""T9.5: monotonicity of relay sigma^2 and P in tau, P <= relay, and V = inf_G relay (strictly decreasing, >= P)."""
import sys
import time

import mpmath as mp
import numpy as np

from t9_common import P_opt, V_best, analyse, draw_sets, opt_sweep, relay, relay_sweep, save_json

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
t0 = time.time()
sets = draw_sets(np.random.default_rng(9004), N)
st = {"relay_extrema": 0, "P_extrema": 0, "P_gt_relay": 0, "V_not_decreasing": 0, "V_lt_P": 0, "samples": 0,
      "min_V_minus_P": None, "min_rel_V_minus_P": None, "argmin_abs": None, "argmin_rel": None,
      "max_P_over_relay": 0.0, "V_multi_local_min_grid": 0}
for i in range(N):
    lam, Sig, Pi, G = (float(x) for x in sets[i])
    lm, Sm, Pm, Gm = (mp.mpf(x) for x in (lam, Sig, Pi, G))
    st["relay_extrema"] += len(analyse(*relay_sweep(lm, Sm, Pm, Gm), lm)["turns"])
    st["P_extrema"] += len(analyse(*opt_sweep(lm, Sm, Pm), lm)["turns"])
    taus = np.logspace(-6, 6, 200) / lam
    Vprev = None
    for t in taus:
        tm = mp.mpf(t)
        P = P_opt(tm, lm, Sm, Pm)
        r = relay(tm, lm, Sm, Pm, Gm)
        st["max_P_over_relay"] = max(st["max_P_over_relay"], float(P / r))
        if P > r:
            st["P_gt_relay"] += 1
        V, Gb, nloc = V_best(t, lam, Sig, Pi)
        st["V_multi_local_min_grid"] += int(nloc > 1)
        Pf = float(P)
        if Vprev is not None and not V < Vprev:
            st["V_not_decreasing"] += 1
        Vprev = V
        if V < Pf:
            st["V_lt_P"] += 1
        d, rel = V - Pf, (V - Pf) / Pf
        if st["min_V_minus_P"] is None or d < st["min_V_minus_P"]:
            st["min_V_minus_P"], st["argmin_abs"] = d, {"lam": lam, "Sig": Sig, "Pi": Pi, "tau": t, "V": V, "P": Pf}
        if st["min_rel_V_minus_P"] is None or rel < st["min_rel_V_minus_P"]:
            st["min_rel_V_minus_P"], st["argmin_rel"] = rel, {"lam": lam, "Sig": Sig, "Pi": Pi, "tau": t, "V": V, "P": Pf,
                                                               "lam_tau": lam * t, "G_best": Gb}
        st["samples"] += 1
    if (i + 1) % 200 == 0:
        print(f"  {i + 1}/{N} sets, {time.time() - t0:.0f}s", flush=True)

ok = (st["relay_extrema"] == 0 and st["P_extrema"] == 0 and st["P_gt_relay"] == 0 and st["V_not_decreasing"] == 0
      and st["V_lt_P"] == 0)
print(f"{N} sets x 200 tau = {st['samples']} samples: relay extrema {st['relay_extrema']}, P extrema {st['P_extrema']}, "
      f"P > relay {st['P_gt_relay']} (max P/relay {st['max_P_over_relay']:.6g}), V not strictly decreasing "
      f"{st['V_not_decreasing']}, V < P {st['V_lt_P']}")
print(f"numerical result: min(V - P) = {st['min_V_minus_P']:.3g} at {st['argmin_abs']}; "
      f"min (V - P)/P = {st['min_rel_V_minus_P']:.3g} at {st['argmin_rel']}; V - P <= 0 ever: "
      f"{st['min_V_minus_P'] <= 0}; sets/tau with >1 local min of sigma2 in G on the grid: {st['V_multi_local_min_grid']}")
print(f"T9.5: {'PASS' if ok else 'FAIL'}")
save_json({"N": N, "stats": st, "pass": ok, "seconds": time.time() - t0}, "t9_5.json")
