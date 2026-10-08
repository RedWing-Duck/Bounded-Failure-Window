"""T8.4: Theorem 3.2 adversarially: monotone gain sweeps at fixed Pi never give a window or mixed class."""
import sys
import time

import numpy as np

from t8_common import (analyse, classify, coupling_sweep, critical, exp_sweep, hill_sweep, name, prior_sweep,
                       save_json, tanh_sweep)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
NTOL = 10
D = 1e-6
rng = np.random.default_rng(8004)
P = 10.0**rng.uniform(-3, 3, size=(N, 5))          # lambda, Sigma, Pi, c, Pi0
SWEEPS = {
    "prior (theta = Pi0)": lambda l, S, Pi, c, P0: prior_sweep(Pi, c, l, S),
    "coupling (theta = c)": lambda l, S, Pi, c, P0: coupling_sweep(Pi, P0, l, S),
    "c tanh(Pi/Pi0)": lambda l, S, Pi, c, P0: tanh_sweep(Pi, c, l, S),
    "c (1 - exp(-Pi/Pi0))": lambda l, S, Pi, c, P0: exp_sweep(Pi, c, l, S),
    "c Pi^2/(Pi^2 + Pi0^2)": lambda l, S, Pi, c, P0: hill_sweep(Pi, c, l, S),
}
t0 = time.time()
stats = {k: {"sweeps": 0, "classifications": 0, "classes": {}, "windows_or_mixed": 0, "local_max": 0,
             "min_gap_max_R2": None, "limit_check_fail": 0, "flat_piece": 0, "turns_hist": {}} for k in SWEEPS}
bad = []
for i in range(N):
    lam, Sig, Pi, c, P0 = P[i]
    for key, mk in SWEEPS.items():
        st = stats[key]
        A = analyse(*mk(lam, Sig, Pi, c, P0))
        st["sweeps"] += 1
        nt = str(len(A["turns"]))
        st["turns_hist"][nt] = st["turns_hist"].get(nt, 0) + 1
        st["limit_check_fail"] += int(not all(A["limit_check"]))
        st["flat_piece"] += int(any(p["dir"] == 0 for p in A["pieces"]))
        crit_v = critical(A)
        tols = []
        for v in crit_v:
            tols += [v, v * (1 - D), v * (1 + D)]
        tols = tols[:NTOL]
        lo, hi = min(crit_v) / 2, 2 * max(crit_v)
        tols += list(10.0**rng.uniform(np.log10(lo), np.log10(hi), size=NTOL - len(tols)))
        maxima = [t["value"] for t in A["turns"] if t["kind"] == "max"]
        st["local_max"] += len(maxima)
        for r2 in tols:
            cls = classify(A, r2)["class"]
            st["classifications"] += 1
            nm = name(cls)
            st["classes"][nm] = st["classes"].get(nm, 0) + 1
            if cls != "All" and cls[2] >= 1:
                st["windows_or_mixed"] += 1
                bad.append({"sweep": key, "params": [lam, Sig, Pi, c, P0], "R2": r2, "class": nm})
            for m in maxima:
                g = abs(m - r2)
                if st["min_gap_max_R2"] is None or g < st["min_gap_max_R2"]:
                    st["min_gap_max_R2"] = g
    if (i + 1) % 2000 == 0:
        print(f"  {i + 1}/{N} sets, {time.time() - t0:.0f}s", flush=True)

total = sum(s["classifications"] for s in stats.values())
nbad = sum(s["windows_or_mixed"] for s in stats.values())
ok = nbad == 0
for k, s in stats.items():
    print(f"{k}: {s['sweeps']} sweeps, {s['classifications']} classifications, classes {s['classes']}, "
          f"turning points {s['turns_hist']}, local maxima {s['local_max']}, windows/mixed {s['windows_or_mixed']}, "
          f"limit-check failures {s['limit_check_fail']}, flat pieces {s['flat_piece']}")
print(f"T8.4: {'PASS' if ok else 'FAIL'}  {N} parameter sets, {N * len(SWEEPS)} sweeps, {total} classifications, "
      f"{nbad} windows/mixed; local maxima found: {sum(s['local_max'] for s in stats.values())}")
save_json({"N": N, "stats": stats, "total_classifications": total, "windows_or_mixed": nbad, "bad": bad[:50],
           "pass": ok, "seconds": time.time() - t0}, "t8_4.json")
