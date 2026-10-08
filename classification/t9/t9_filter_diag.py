"""T9.2 diagnosis (post hoc, not a pass criterion): why the ARE route misses Prop 3.1 on some sets.

For each failing set of t9_2.json: (1) the same ARE solved in mpmath (60 digits) by the Hamiltonian
stable-subspace method at the pre-registered eps and at eps down to 1e-40; (2) the Wiener route at those
parameters; (3) scipy's own P_eps vs the mp ARE at the same eps (solver accuracy)."""
import json
import os

import mpmath as mp
import numpy as np

from t9_common import P_opt, RES, save_json
from t9_filter import p_eps, wiener

mp.mp.dps = 60


def are_mp(lam, Sig, Pi, tau, eps):
    lam, Sig, Pi, tau, eps = (mp.mpf(x) for x in (lam, Sig, Pi, tau, eps))
    A = mp.matrix([[-lam, 0], [0, -1 / tau]])
    Q = mp.matrix([[2 * Sig, 0], [0, 1 / (Pi * tau**2)]])
    CC = mp.matrix([[1, 1], [1, 1]]) / eps
    H = mp.matrix(4, 4)
    for i in range(2):
        for j in range(2):
            H[i, j] = A[j, i]
            H[i, j + 2] = -CC[i, j]
            H[i + 2, j] = -Q[i, j]
            H[i + 2, j + 2] = -A[i, j]
    E, V = mp.eig(H)
    idx = [k for k in range(4) if mp.re(E[k]) < 0]
    U1 = mp.matrix([[V[i, k] for k in idx] for i in range(2)])
    U2 = mp.matrix([[V[i + 2, k] for k in idx] for i in range(2)])
    X = U2 * U1**-1
    return mp.re(X[0, 0])


def wiener_closed(lam, Sig, Pi, tau):
    """Same factorization, causal part A/(s+lam) integrated in closed form: MMSE = Sig/lam - A^2/(2 lam)."""
    lam, Sig, Pi, tau = (mp.mpf(x) for x in (lam, Sig, Pi, tau))
    k2 = 2 * Sig * tau**2 + 1 / Pi
    beta = mp.sqrt((2 * Sig + lam**2 / Pi) / k2)
    A = 2 * Sig * (1 + tau * lam) / (mp.sqrt(k2) * (beta + lam))
    return Sig / lam - A**2 / (2 * lam)


d = json.load(open(os.path.join(RES, "t9_2.json")))
out = []
for f in d["are"]["fails"]:
    lam, Sig, Pi, tau = f["lam"], f["Sig"], f["Pi"], f["tau"]
    ref = P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
    row = {"lam": lam, "Sig": Sig, "Pi": Pi, "tau": tau, "prereg_err": f["err"]}
    row["scipy_vs_mp_rel"] = {}
    for e in (1e-4, 1e-6, 1e-8, 1e-10):
        pm = are_mp(lam, Sig, Pi, tau, e)
        row["scipy_vs_mp_rel"][str(e)] = float(abs(mp.mpf(p_eps(lam, Sig, Pi, tau, e)) - pm) / pm)
    row["mp_are_rel_to_prop31"] = {str(e): float(abs(are_mp(lam, Sig, Pi, tau, e) - ref) / ref)
                                   for e in (1e-10, 1e-20, 1e-30, 1e-40)}
    row["wiener_rel_to_prop31"] = float(abs(wiener(lam, Sig, Pi, tau) - ref) / ref)
    row["wiener_closed_rel_to_prop31"] = float(abs(wiener_closed(lam, Sig, Pi, tau) - ref) / ref)
    out.append(row)
    print(f"lam={lam:.3g} Sig={Sig:.3g} Pi={Pi:.3g} tau={tau:.3g}: prereg err {f['err']:.2g}; "
          f"scipy vs mp ARE at eps=1e-10: {row['scipy_vs_mp_rel']['1e-10']:.2g}; "
          f"mp ARE vs Prop 3.1 at eps 1e-10/1e-20/1e-30/1e-40: "
          + "/".join(f"{v:.2g}" for v in row["mp_are_rel_to_prop31"].values())
          + f"; Wiener (quad / closed) vs Prop 3.1: {row['wiener_rel_to_prop31']:.2g} / "
          f"{row['wiener_closed_rel_to_prop31']:.2g}")

# all 2,001 pre-registered cases: mp ARE at eps = 1e-40 and closed-form Wiener vs Prop 3.1
rng = np.random.default_rng(9002)
S = 10.0**rng.uniform(-3, 3, size=(1000, 4))
lt = 10.0**rng.uniform(-3, 3, size=1000)
cases = [(S[i, 0], S[i, 1], S[i, 2], t) for i in range(1000) for t in (lt[i] / S[i, 0], 1.0 / S[i, 0])]
cases.append((1.0, 0.01, 1.0, 1.0))
e_are, e_w = [], []
for lam, Sig, Pi, tau in cases:
    ref = P_opt(mp.mpf(tau), mp.mpf(lam), mp.mpf(Sig), mp.mpf(Pi))
    e_are.append(float(abs(are_mp(lam, Sig, Pi, tau, mp.mpf("1e-40")) - ref) / ref))
    e_w.append(float(abs(wiener_closed(lam, Sig, Pi, tau) - ref) / ref))
allc = {"n": len(cases), "mp_are_1e-40_max_rel": max(e_are), "mp_are_1e-40_n_over_1e-5": sum(e > 1e-5 for e in e_are),
        "wiener_closed_max_rel": max(e_w), "wiener_closed_n_over_1e-6": sum(e > 1e-6 for e in e_w)}
print(f"all {len(cases)} cases: mp ARE (eps = 1e-40) max rel err {allc['mp_are_1e-40_max_rel']:.3g} "
      f"({allc['mp_are_1e-40_n_over_1e-5']} over 1e-5); closed-form Wiener max rel err {allc['wiener_closed_max_rel']:.3g} "
      f"({allc['wiener_closed_n_over_1e-6']} over 1e-6)")
save_json({"rows": out, "all_cases": allc}, "t9_2_diag.json")
