"""T10.3: turning-point census of natural gain families (T10 method), regression values, Hill pair birth,
Hill proof support, exploratory two-channel census."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np
import sympy as sp

from t10_common import analyse, mpize, pi_curve, save_json, sf_match

D_TARGET = [0, 1e-3, -1e-3, 1e-6, -1e-6, 1e-9, -1e-9]
N_HILL = [1.5, 2, 3, 4, 8]


def summarize(A):
    return {"n_tp": len(A["turns"]), "kinds": [t["kind"] for t in A["turns"]],
            "thetas": [t["theta"] for t in A["turns"]], "values": [t["value"] for t in A["turns"]],
            "L_minus": A["L_minus"], "L_plus": A["L_plus"], "limit_ok": A["limit_ok"], "dirs": A["dirs"]}


def grid_signs_negative(A):
    from t10_common import _sgn, grid
    c = A["curve"]
    return all(_sgn(c, x)[0] == -1 for x in grid(c))


def job(args, delta=None):
    """delta (targeted sets): the onset side is taken from the sign of delta, exactly, instead of the
    floating comparison kappa > 2 (which rounds at delta = 0)."""
    fam, p = args
    q = mpize(p)
    A = analyse(pi_curve(fam, q))
    s = summarize(A)
    lam, Sig = q["lam"], q["Sig"]
    F = Sig / lam
    ok, info = True, {}
    if fam == "bayes":
        kap = q["c"] * lam / (Sig * q["Pi0"])
        if (kap > 2) if delta is None else (delta > 0):
            Gr = -lam + mp.sqrt(lam**2 + lam * q["c"] - 2 * Sig * q["Pi0"])
            Pr = q["Pi0"] * Gr / (q["c"] - Gr)
            ok = s["kinds"] == ["max"] and abs(s["thetas"][0] - Pr) <= mp.mpf("1e-10") * Pr
            info["pos_rel_err"] = abs(s["thetas"][0] - Pr) / Pr if s["n_tp"] == 1 else None
        else:
            ok = s["n_tp"] == 0
        info["kappa"] = kap
    elif fam == "misspec":
        Fp = q["Sig1"] / q["lam1"]
        if (Fp > 2 * F) if delta is None else (delta > 0):
            r, l1 = Sig / q["Sig1"], q["lam1"]
            a2, b1, c0 = 1 + r, 4 * r * l1, 2 * lam * l1 - 4 * r * l1**2
            G = 2 * c0 / (b1 + mp.sqrt(b1**2 + 4 * a2 * c0))
            Pr = (G**2 + 2 * l1 * G) / (2 * q["Sig1"])
            ok = s["kinds"] == ["max"] and abs(s["thetas"][0] - Pr) <= mp.mpf("1e-10") * Pr
            info["pos_rel_err"] = abs(s["thetas"][0] - Pr) / Pr if s["n_tp"] == 1 else None
        else:
            ok = s["n_tp"] == 0
        info["Fp_over_F"] = Fp / F
    elif fam == "capped":
        g, c = q["g"], q["c"]
        side = (1 if g > 2 * F else (-1 if g < 2 * F else 0)) if delta is None else (1 if delta > 0 else (-1 if delta < 0 else 0))
        if side > 0:
            ok = s["kinds"] == ["max"] and abs(s["thetas"][0] - c / g) <= mp.mpf("1e-10") * c / g
        elif side < 0:
            ok = s["n_tp"] == 0 and grid_signs_negative(A)
        else:
            from t10_common import grid, T
            pl = [abs(A["curve"].f(T(x)) - F) / F for x in grid(A["curve"]) if T(x) <= c / g]
            info["plateau_max_rel_dev"] = max(pl)
            ok = s["n_tp"] == 0 and max(pl) <= mp.mpf("1e-48")
        info["g_over_2F"] = g / (2 * F)
    elif fam == "blind":
        ok = s["n_tp"] == 0 and grid_signs_negative(A) and A["L_minus"] == mp.inf
    elif fam == "hill":
        ok = s["n_tp"] in (0, 2) and (s["n_tp"] == 0 or s["kinds"] == ["min", "max"])
        if p["n"] == 2:
            R_ = lambda v: sp.Rational(float(v))
            t = sp.symbols("t")
            lam_, Sig_, c_, P0_ = R_(p["lam"]), R_(p["Sig"]), R_(p["c"]), R_(p["Pi0"])
            Q = (-c_ * (lam_ + c_) * t**5 - 4 * Sig_ * P0_ * t**4 + c_ * (c_ + 2 * lam_) * t**3
                 - 8 * Sig_ * P0_ * t**2 + 3 * lam_ * c_ * t - 4 * Sig_ * P0_)
            info["exact_count"] = int(sp.Poly(Q, t).count_roots(0, sp.oo))
            info["count_agrees"] = info["exact_count"] == s["n_tp"]
            ok = ok and info["count_agrees"]
    return {"fam": fam, "p": p, **s, "pass": bool(ok), **info}


def draw(rng, fam, n):
    U = lambda: 10.0**rng.uniform(-2, 2)
    out = []
    for _ in range(n):
        p = {"lam": U(), "Sig": U()}
        if fam == "bayes":
            p.update(c=U(), Pi0=U())
        elif fam == "misspec":
            p.update(lam1=U(), Sig1=U())
        elif fam == "capped":
            p.update(g=U(), c=U())
        elif fam == "blind":
            p.update(G0=U())
        elif fam in ("bayes2", "hill2"):
            Pi01 = U()
            p.update(c1=U(), c2=U(), Pi01=Pi01, Pi02=Pi01 * 10.0**rng.uniform(1, 6))
        out.append(p)
    return out


def targeted(rng):
    """Base sets with the onset parameter placed at 2(1 + delta) exactly (strings keep delta exact in mp)."""
    jobs = []
    for _ in range(20):
        lam, Sig, c = (10.0**rng.uniform(-2, 2) for _ in range(3))
        for d in D_TARGET:
            jobs.append(("bayes", {"lam": lam, "Sig": Sig, "c": c, "Pi0": ("onsetB", d)}))
            jobs.append(("misspec", {"lam": lam, "Sig": Sig, "lam1": c, "Sig1": ("onsetM", d)}))
            jobs.append(("capped", {"lam": lam, "Sig": Sig, "c": c, "g": ("onsetC", d)}))
    return jobs


def resolve(p):
    """Turn ('onset*', delta) placeholders into exact mp values: kappa, F'/F or g/(2F) = 2(1+delta)."""
    q = dict(p)
    for k, v in p.items():
        if isinstance(v, tuple):
            tag, d = v
            lam, Sig = mp.mpf(p["lam"]), mp.mpf(p["Sig"])
            F, fac = Sig / lam, 1 + mp.mpf(d)
            if tag == "onsetB":       # kappa = c lam/(Sig Pi0) = 2(1+d)
                q[k] = mp.mpf(p["c"]) * lam / (Sig * 2 * fac)
            elif tag == "onsetM":     # F' = Sig1/lam1 = 2F(1+d)
                q[k] = 2 * F * fac * mp.mpf(p["lam1"])
            elif tag == "onsetC":     # g = 2F(1+d)
                q[k] = 2 * F * fac
            q["delta"] = d
    return q


def job_t(args):
    fam, p = args
    q = resolve(p)
    d = q.pop("delta")
    r = job((fam, q), delta=d)
    r["delta"] = d
    return r


def hill_count(n, Pi0):
    A = analyse(pi_curve("hill", mpize({"lam": 1.0, "Sig": 0.01, "c": 1.0, "n": n, "Pi0": Pi0})))
    return A


def pair_birth(n):
    """Scan Pi0 for TP-count transitions, bisect each to 1e-10, then refine by the double-root system."""
    xs = [mp.mpf(-4) + mp.mpf(i) / 8 for i in range(65)]
    counts = [len(hill_count(n, mp.power(10, x))["turns"]) for x in xs]
    trans = []
    for i in range(len(xs) - 1):
        if counts[i] != counts[i + 1]:
            a, b = xs[i], xs[i + 1]
            ca = counts[i]
            while (mp.power(10, b) - mp.power(10, a)) / mp.power(10, a) > mp.mpf("1e-11"):
                m = (a + b) / 2
                if len(hill_count(n, mp.power(10, m))["turns"]) == ca:
                    a = m
                else:
                    b = m
            P0b = mp.power(10, (a + b) / 2)
            # refine: N(Pi; Pi0) = 0 and dN/dPi = 0 starting from the TPs just on the pair side
            side = a if ca > counts[i + 1] else b
            A = hill_count(n, mp.power(10, side))
            Pst = sum(t["theta"] for t in A["turns"]) / len(A["turns"]) if A["turns"] else mp.mpf(1)

            def Nf(Pi, P0):
                c = pi_curve("hill", mpize({"lam": 1.0, "Sig": 0.01, "c": 1.0, "n": n, "Pi0": 1.0}))
                from t10_common import N_of
                lam, Sig, cc, nn = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1), mp.mpf(n)
                rr = mp.power(P0 / Pi, nn)
                return N_of(cc / (1 + rr), nn * rr / (1 + rr), Pi, lam, Sig)
            try:
                sol = mp.findroot([lambda Pi, P0: Nf(Pi, P0), lambda Pi, P0: mp.diff(lambda y: Nf(y, P0), Pi)],
                                  (Pst, P0b))
                P0d = sol[1]
            except Exception as e:  # noqa: BLE001
                P0d = None
            trans.append({"from_count": ca, "to_count": counts[i + 1], "Pi0_bisect": P0b, "Pi0_double_root": P0d,
                          "rel_diff": (abs(P0d - P0b) / P0b) if P0d is not None else None})
    return {"n": n, "scan_counts": dict(zip([float(mp.power(10, x)) for x in xs], counts)), "transitions": trans}


def proof_support():
    t, al, be, u = sp.symbols("t alpha beta u", positive=True)
    Qr = -(al + 1) * t**5 - 4 * be * t**4 + (1 + 2 * al) * t**3 - 8 * be * t**2 + 3 * al * t - 4 * be
    disc = sp.discriminant(Qr, t)
    dfac = sp.factor(disc)
    lam, c = sp.symbols("lambda c", positive=True)
    P4 = -(lam + c) * t**4 + (c + 2 * lam) * t**2 + 3 * lam
    phi = t * P4 / (1 + t**2)**2
    num = sp.factor(sp.numer(sp.together(sp.diff(phi, t))))
    cub = sp.expand(sp.cancel(num.subs(t, sp.sqrt(u))))
    cubp = sp.Poly(cub, u)
    coeffs = cubp.all_coeffs()
    return {"Q_reduced": str(Qr), "discriminant_factored": str(dfac),
            "phi": "phi(t) = t P4(t)/(1+t^2)^2, Q = c t P4 - 4 Sigma Pi0 (1+t^2)^2, so Q > 0 iff c phi/4 > Sigma Pi0",
            "dphi_numerator_factored": str(num), "dphi_numerator_in_u": str(cub), "coeffs_in_u": [str(x) for x in coeffs]}


NSET = int(__import__("os").environ.get("T10_NSET", "2000"))


def main():
    t0 = time.time()
    rng = np.random.default_rng(10003)
    jobs = []
    for fam in ("bayes", "misspec", "capped", "blind"):
        jobs += [(fam, p) for p in draw(rng, fam, NSET)]
    for n in N_HILL:
        jobs += [("hill", {**p, "n": n, "c": 10.0**rng.uniform(-2, 2), "Pi0": 10.0**rng.uniform(-2, 2)})
                 for p in draw(rng, "blind", NSET)]
    expl = [(fam, p) for fam in ("bayes2", "hill2") for p in draw(rng, fam, NSET)]
    tj = targeted(rng)
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=20)
        res_t = pool.map(job_t, tj, chunksize=10)
        res_e = pool.map(job, expl, chunksize=20)
        pb = pool.map(pair_birth, N_HILL)
    print(f"  census done {time.time() - t0:.0f}s", flush=True)
    R = {"families": {}, "targeted": {}, "exploratory": {}}
    for fam in ("bayes", "misspec", "capped", "blind", "hill"):
        rr = [r for r in res if r["fam"] == fam]
        hist = {}
        for r in rr:
            hist[r["n_tp"]] = hist.get(r["n_tp"], 0) + 1
        ent = {"n": len(rr), "pass": all(r["pass"] for r in rr), "n_fail": sum(not r["pass"] for r in rr),
               "tp_hist": hist, "fails": [r for r in rr if not r["pass"]][:20],
               "limit_check_fail": sum(not all(r["limit_ok"]) for r in rr)}
        pe = [r["pos_rel_err"] for r in rr if r.get("pos_rel_err") is not None]
        if pe:
            ent["max_pos_rel_err"] = max(pe)
        if fam == "hill":
            for n in N_HILL:
                h = {}
                for r in rr:
                    if r["p"]["n"] == n:
                        h[r["n_tp"]] = h.get(r["n_tp"], 0) + 1
                ent[f"tp_hist_n{n}"] = h
            ent["exact_count_disagreements"] = sum(1 for r in rr if r["p"]["n"] == 2 and not r.get("count_agrees", True))
        R["families"][fam] = ent
        print(f"{fam}: {ent['n']} sets, TP histogram {hist}, failures {ent['n_fail']}", flush=True)
    for fam in ("bayes", "misspec", "capped"):
        rr = [r for r in res_t if r["fam"] == fam]
        R["targeted"][fam] = {"n": len(rr), "pass": all(r["pass"] for r in rr),
                              "by_delta": {str(d): [r["n_tp"] for r in rr if r["delta"] == d][:20] for d in D_TARGET},
                              "fails": [r for r in rr if not r["pass"]][:20]}
        print(f"targeted {fam}: {len(rr)} sets, failures {sum(not r['pass'] for r in rr)}", flush=True)
    # Hill near pair birth (targeted) and the pair-birth table
    R["pair_birth"] = pb
    hill_t = []
    for e in pb:
        for tr in e["transitions"]:
            for d in (1e-3, -1e-3, 1e-6, -1e-6):
                P0 = (tr["Pi0_double_root"] or tr["Pi0_bisect"]) * (1 + mp.mpf(d))
                A = hill_count(e["n"], P0)
                k = len(A["turns"])
                hill_t.append({"n": e["n"], "delta": d, "n_tp": k, "kinds": [t["kind"] for t in A["turns"]],
                               "pass": k in (0, 2) and (k == 0 or [t["kind"] for t in A["turns"]] == ["min", "max"])})
    R["targeted"]["hill"] = {"rows": hill_t, "pass": all(r["pass"] for r in hill_t)}
    for e in pb:
        print(f"Hill n={e['n']}: transitions " + "; ".join(
            f"{tr['from_count']}->{tr['to_count']} at Pi0 = {mp.nstr(tr['Pi0_double_root'] or tr['Pi0_bisect'], 12)} "
            f"(bisection vs double root rel {mp.nstr(tr['rel_diff'], 3) if tr['rel_diff'] is not None else 'n/a'})"
            for tr in e["transitions"]), flush=True)
    # regression values
    reg = []
    for (l1, S1), (pP, pV) in (((1.0, 0.05), ("19.610", "0.01351")), ((0.5, 0.1), ("7.4380", "0.03025"))):
        A = analyse(pi_curve("misspec", mpize({"lam": 1.0, "Sig": 0.01, "lam1": l1, "Sig1": S1})))
        t_ = A["turns"][0]
        reg.append({"what": f"misspec ({l1}, {S1})", "Pi": t_["theta"], "value": t_["value"],
                    "pass": sf_match(t_["theta"], pP) and sf_match(t_["value"], pV)})
    for P0, vals in ((5.0, ("0.3348", "0.0099852", "6.9817", "0.024858")),
                     (26.0, ("10.723", "0.0095911", "25.283", "0.0098730"))):
        A = hill_count(2, mp.mpf(P0))
        tm, tM = A["turns"]
        reg.append({"what": f"Hill n=2 Pi0={P0}", "min": (tm["theta"], tm["value"]), "max": (tM["theta"], tM["value"]),
                    "pass": sf_match(tm["theta"], vals[0]) and sf_match(tm["value"], vals[1])
                    and sf_match(tM["theta"], vals[2]) and sf_match(tM["value"], vals[3])})
    # window onset (n = 2): M(Pi0) = F
    F = mp.mpf("0.01")
    Mof = lambda P0: [t["value"] for t in hill_count(2, P0)["turns"] if t["kind"] == "max"][0]
    a, b = mp.mpf(20), mp.mpf(30)
    while (b - a) / a > mp.mpf("1e-13"):
        m = (a + b) / 2
        if Mof(m) > F:
            a = m
        else:
            b = m
    onset = (a + b) / 2
    reg.append({"what": "Hill n=2 window onset (M = F)", "Pi0": onset, "expected": 25,
                "pass": bool(abs(onset - 25) <= mp.mpf("1e-8") * 25)})
    R["regression"] = reg
    for r in reg:
        print("regression:", {k: (mp.nstr(v, 10) if isinstance(v, mp.mpf) else v) for k, v in r.items()}, flush=True)
    # exploratory
    for fam in ("bayes2", "hill2"):
        rr = [r for r in res_e if r["fam"] == fam]
        hist, kinds = {}, {}
        for r in rr:
            hist[r["n_tp"]] = hist.get(r["n_tp"], 0) + 1
            kk = ",".join(r["kinds"]) or "-"
            kinds[kk] = kinds.get(kk, 0) + 1
        multi = [r for r in rr if r["kinds"].count("max") >= 2]
        R["exploratory"][fam] = {"n": len(rr), "tp_hist": hist, "kind_sequences": kinds, "n_two_or_more_max": len(multi),
                                 "examples_two_or_more_max": multi[:10]}
        print(f"exploratory {fam}: TP histogram {hist}; >= 2 maxima in {len(multi)} sets", flush=True)
    R["proof_support"] = proof_support()
    print("proof support:", R["proof_support"]["dphi_numerator_in_u"], flush=True)
    fam_ok = all(R["families"][f]["pass"] for f in ("bayes", "misspec", "capped", "blind", "hill"))
    tgt_ok = all(R["targeted"][f]["pass"] for f in ("bayes", "misspec", "capped", "hill"))
    reg_ok = all(r["pass"] for r in reg)
    R["pass"] = bool(fam_ok and tgt_ok and reg_ok)
    R["pass_parts"] = {"families": fam_ok, "targeted": tgt_ok, "regression": reg_ok}
    R["seconds"] = time.time() - t0
    print(f"T10.3: {'PASS' if R['pass'] else 'FAIL'} {R['pass_parts']}")
    save_json(R, "t10_3.json")


if __name__ == "__main__":
    main()
