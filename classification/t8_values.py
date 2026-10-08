"""T8.2: worked-example values (lambda = c = 1, Sigma = 0.01) by bounded scalar minimization."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

from t8_common import C, LAM, SIG, analyse, coupling_sweep, g_star, prior_sweep, save_json, sf_match, sigma2

F = SIG / LAM
rows = []


def rec(label, got, stated):
    ok = sf_match(got, stated)
    rows.append({"quantity": label, "computed": got, "stated": stated, "match": ok})
    print(f"  {label:<28} computed {got:.8g}  stated {stated}  {'ok' if ok else 'MISMATCH'}")


def bounded_min(f):
    r = minimize_scalar(lambda x: f(10.0**x), bounds=(-6.0, 6.0), method="bounded",
                        options={"xatol": 1e-12, "maxiter": 1000})
    return r.x, 10.0**r.x, float(r.fun)


rec("Pi_B", C * LAM / (2 * SIG), 50.00)
rec("Pi_A", C * (C + 2 * LAM) / (2 * SIG), 150.0)

print("Pi = 1 (P3)")
f, _ = prior_sweep(1.0, C)
_, p0, vmin = bounded_min(f)
rec("Pi=1: G*", g_star(1.0), 0.009950)
rec("Pi=1: Pi0*", p0, 99.50)
rec("Pi=1: sigma*^2", vmin, 0.009950)
rec("Pi=1: V_c", sigma2(C, 1.0), 0.2550)

print("Pi = 60 (P2)")
f, _ = prior_sweep(60.0, C)
_, p0, vmin = bounded_min(f)
rec("Pi=60: Pi0*", p0, 64.16)
rec("Pi=60: sigma*^2", vmin, 0.008054)
rec("Pi=60: V_c", sigma2(C, 60.0), 0.009167)

print("Pi = 500 (P1)")
f, df = prior_sweep(500.0, C)
x, p0, vmin = bounded_min(f)
A = analyse(f, df)
no_ext = len(A["turns"]) == 0 and abs(x - (-6.0)) <= 1e-6
rows.append({"quantity": "Pi=500: no interior extremum", "computed": {"turning_points": len(A["turns"]),
             "argmin_log10": x}, "stated": "none", "match": no_ext})
print(f"  Pi=500: turning points {len(A['turns'])}, bounded argmin log10 = {x:.9f} -> "
      f"{'no interior extremum' if no_ext else 'MISMATCH'}")
rec("Pi=500: V_c", sigma2(C, 500.0), 0.005500)

print("Coupling, Pi = Pi0 = 1")
f, _ = coupling_sweep(1.0, 1.0)
_, cst, vmin = bounded_min(f)
cF = brentq(lambda cc: f(cc) - F, cst, 1e6, xtol=1e-15, rtol=4 * np.finfo(float).eps)
rec("coupling: c*", cst, 0.01990)
rec("coupling: sigma*^2", vmin, 0.009950)
rec("coupling: c_F", cF, 0.04000)

ok = all(r["match"] for r in rows)
print(f"T8.2: {'PASS' if ok else 'FAIL'} ({sum(r['match'] for r in rows)}/{len(rows)})")
save_json({"rows": rows, "pass": ok}, "t8_2.json")
