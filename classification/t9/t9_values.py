"""T9.3: worked-example values (lambda = c = 1, Sigma = 0.01, Pi = Pi0 = 1, G = 0.5)."""
import mpmath as mp

from t9_common import P_opt, V_best, _bisect, crit, relay, save_json, sf_match

lam, Sig, Pi, G = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1), mp.mpf("0.5")
c = crit(lam, Sig, Pi, G)
tF = mp.power(10, _bisect(lambda x: relay(mp.power(10, x), lam, Sig, Pi, G) - c["F"], mp.mpf(-10), mp.mpf(10)))
vals = [("V_w", c["V_w"], 0.09000), ("H_G", c["H_G"], 0.006667), ("tau_F", tF, 16.00),
        ("sigma2(1)", relay(1, lam, Sig, Pi, G), 0.04000), ("sigma2(10)", relay(10, lam, Sig, Pi, G), 0.01188),
        ("sigma2(16)", relay(16, lam, Sig, Pi, G), 0.01000), ("sigma*^2", c["s2"], 0.009950),
        ("P(1)", P_opt(mp.mpf(1), lam, Sig, Pi), 0.009804), ("P(10)", P_opt(mp.mpf(10), lam, Sig, Pi), 0.006781)]
rows = []
for n, v, st in vals:
    ok = sf_match(v, st)
    rows.append({"quantity": n, "computed": float(v), "stated": st, "match": ok})
    print(f"  {n:<11} computed {mp.nstr(v, 10):<14} stated {st}  {'ok' if ok else 'MISMATCH'}")
V1, Gopt, nloc = V_best(1.0, 1.0, 0.01, 1.0)
okV = abs(V1 - 0.00990) <= 0.5e-5
rows.append({"quantity": "V(1) (3 s.f.)", "computed": V1, "stated": 0.00990, "match": okV, "argmin_G": Gopt,
             "grid_local_minima": nloc})
print(f"  V(1)        computed {V1:.10g} (G = {Gopt:.6g}) stated about 0.00990  {'ok' if okV else 'MISMATCH'}")
ok = all(r["match"] for r in rows)
print(f"T9.3: {'PASS' if ok else 'FAIL'} ({sum(r['match'] for r in rows)}/{len(rows)})")
save_json({"rows": rows, "pass": ok}, "t9_3.json")
