"""T11.5: ordering is sufficient, not necessary (Prop. 4.8): beta = 1, tau1 < tau2 in (1/lam, 100/lam)."""
import time

import mpmath as mp
import numpy as np

from t11_common import P_pow, save_json, sign_changes_spectra

t0 = time.time()
rng = np.random.default_rng(11005)
beta = mp.mpf(1)
dec, cross, rows = 0, 0, []
for i in range(1000):
    lam, Sig, K = (mp.mpf(float(10.0**rng.uniform(-2, 2))) for _ in range(3))
    a, b = sorted(rng.uniform(0, 2, 2))
    t1, t2 = mp.power(10, mp.mpf(float(a))) / lam, mp.power(10, mp.mpf(float(b))) / lam
    p1, p2 = P_pow(t1, beta, K, lam, Sig), P_pow(t2, beta, K, lam, Sig)
    n, _ = sign_changes_spectra(t1, t2, beta, K)
    dec += int(p2 < p1)
    cross += int(n == 1)
    if not (p2 < p1 and n == 1):
        rows.append({"lam": lam, "Sig": Sig, "K": K, "tau1": t1, "tau2": t2, "P1": p1, "P2": p2, "sign_changes": n})
R = {"n": 1000, "P_decreasing": dec, "spectra_cross_once": cross, "fails": rows[:20], "pass": dec == 1000 and cross == 1000,
     "seconds": time.time() - t0}
print(f"P(tau2) < P(tau1) in {dec}/1000; spectra cross exactly once in {cross}/1000")
print(f"T11.5: {'PASS' if R['pass'] else 'FAIL'}")
save_json(R, "t11_5.json")
