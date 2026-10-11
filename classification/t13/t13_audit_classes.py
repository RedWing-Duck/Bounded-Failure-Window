"""C2 (PREREG_t13): class audit of every synthesis-matrix row (rows 1-42 of the pre-registered table).
Per row: 1,000 random parameter sets (seed 13100 + row), 100 tolerances per set (50 log-uniform on [1/2 min, 2 max] of the
finite positive critical tolerances; 50 near-critical: 10 exact, 40 within +-1e-6 relative; monotone 0 -> oo curves: 100 curve
values at log-uniform sweep points over 40 decades). Route (i) mp; route (ii) float64 where a float curve exists, else mp;
every flagged case re-run in mp at dps 60. Pass per row: 0 persisting out-of-set classes, 0 persisting disagreements, every
stated class observed. Rows are saved one by one (results/c2_rows/) so an interrupted run resumes.
Usage: python3 t13_audit_classes.py [N_SETS] [ROW ...]"""
import json
import math
import os
import sys
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t13_common import CLS, RES, save_json

sys.path.insert(0, os.path.join(CLS, "t12"))
from classify import EQ, name, route_i, route_ii  # noqa: E402
from t10_common import ZREL, Curve, FLN, MPN, mpize, pi_curve, sig2, dsig2_dG  # noqa: E402
from t11_common import P_delay, analyse_with_limits, limits_pow, power_curve, sstar  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1000
ONLY = [int(a) for a in sys.argv[2:]] if len(sys.argv) > 2 else None
ROWDIR = os.path.join(RES, "c2_rows" if N == 1000 else f"c2_rows_n{N}")
os.makedirs(ROWDIR, exist_ok=True)
E, A_, LR, UR, TR, W = (0, 0, 0), "All", (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)
M101, M102, M002, M011 = (1, 0, 1), (1, 0, 2), (0, 0, 2), (0, 1, 1)
DT_SETS = {
    "opt post": {LR, E}, "opt prior": {A_, UR, E}, "opt avg": {A_, UR, E},
    "D1 post": {E, LR, W}, "D1 prior": {A_, E, LR, UR, TR, M011}, "D1 avg": {A_, E, LR, UR, TR, M011},
    "D2 post": {A_, E, LR, UR, TR, W, M101}, "D2 prior": {A_, E, LR, UR, TR}, "D2 avg": {A_, E, LR, UR, TR},
    "D3 post": {E, LR, W}, "D3 prior": {A_, E, LR, UR, TR, M011}, "D3 avg": {A_, E, LR, UR, TR},
    "MI a": {A_, UR, E}, "MI b": {A_, UR, E}}
ROWS = {1: ("Pi optimal", {LR, E}), 2: ("Pi bayes", {A_, LR, W, E}), 3: ("Pi misspec", {LR, W, E}),
        4: ("Pi capped", {A_, LR, W, E}), 5: ("Pi blind", {A_, LR}), 6: ("Pi hill2", {A_, LR, M101, W, E}),
        7: ("Pi hilln", {A_, LR, M101, W, E}), 8: ("Pi bayes2", {A_, LR, W, M101, M002, E}),
        9: ("Pi hill2stage", {A_, LR, M101, M102, W, M002, E}), 10: ("Pi0 bayes", {A_, TR, LR, UR, E}),
        11: ("c bayes", {A_, TR, UR}), 12: ("Pi0 monotone", {A_, TR, LR, UR, E}), 13: ("tau ZF relay", {A_, LR, E}),
        14: ("tau ZF optimal", {LR, E}), 15: ("tau var relay", {A_, UR, E}), 16: ("tau var optimal", {W, E}),
        17: ("power beta<=0", {LR, E}), 18: ("power 0<beta<2", {W, E}), 19: ("power beta>=2", {UR, E}),
        20: ("delay", {A_, W, E})}
for i, k in enumerate(["opt post", "opt prior", "opt avg", "D1 post", "D1 prior", "D1 avg", "D2 post", "D2 prior", "D2 avg",
                       "D3 post", "D3 prior", "D3 avg", "MI a", "MI b"]):
    ROWS[21 + i] = ("dt " + k, DT_SETS[k])
for i, (fam, conv, st) in enumerate([("B2", "abs", {A_, UR}), ("B2", "rel", {A_, LR}), ("B3", "abs", {UR}),
                                      ("B3", "rel", {LR, W, E}), ("B4", "abs", {UR}), ("B4", "rel", {LR, W, E}),
                                      ("B5", "abs", {UR}), ("B5", "rel", {LR, E})]):
    ROWS[35 + i] = (f"Sigma {fam} {conv}", st)


def U(rng):
    return float(10.0**rng.uniform(-2, 2))


# ---------------------------------------------------------------- curves (curve, L-, L+, x-, x+)
def c_pi_optimal(p):
    lam, Sig = mp.mpf(p["lam"]), mp.mpf(p["Sig"])
    f = lambda Pi: 2 * Sig / (lam + mp.sqrt(lam**2 + 2 * Sig * Pi))
    d = lambda Pi: -2 * Sig * Sig / (mp.sqrt(lam**2 + 2 * Sig * Pi) * (lam + mp.sqrt(lam**2 + 2 * Sig * Pi))**2)
    lf, sf = p["lam"], p["Sig"]
    ffl = lambda Pi: 2 * sf / (lf + math.sqrt(lf**2 + 2 * sf * float(Pi))) if math.isfinite(float(Pi)) else 0.0
    return Curve(f, d, lambda t: ZREL * abs(f(t)) / t, 0, [], ffl, "Pi optimal"), Sig / lam, mp.mpf(0), -80, 80


def c_pi(fam, p):
    q = mpize(p)
    lam, Sig = q["lam"], q["Sig"]
    F = Sig / lam
    if fam == "bayes":
        Lm, Lp = F, Sig / (lam + q["c"])
    elif fam == "misspec":
        Lm, Lp = F, mp.mpf(0)
    elif fam == "capped":
        Lm, Lp = F, Sig / (lam + q["c"])
    elif fam == "blind":
        Lm, Lp = mp.inf, Sig / (lam + q["G0"])
    elif fam == "hill":
        Lm, Lp = F, Sig / (lam + q["c"])
    else:                                                     # bayes2, hill2
        Lm, Lp = F, Sig / (lam + q["c1"] + q["c2"])
    return pi_curve(fam, q), Lm, Lp, -80, 80


def c_pi0_monotone(p):
    q = mpize({k: v for k, v in p.items() if k != "g"})
    lam, Sig, Pi, c = q["lam"], q["Sig"], q["Pi"], q["c"]
    g = p["g"]
    if g == "tanh":
        Gm = lambda P0: c * mp.tanh(Pi / P0)
        dG = lambda P0: -c * Pi / P0**2 / mp.cosh(Pi / P0)**2
        Gf = lambda P0: p["c"] * math.tanh(p["Pi"] / P0)
    elif g == "exp":
        Gm = lambda P0: c * (-mp.expm1(-Pi / P0))
        dG = lambda P0: -c * Pi / P0**2 * mp.exp(-Pi / P0)
        Gf = lambda P0: p["c"] * (-math.expm1(-p["Pi"] / P0))
    else:
        Gm = lambda P0: c * Pi**2 / (Pi**2 + P0**2)
        dG = lambda P0: -2 * c * Pi**2 * P0 / (Pi**2 + P0**2)**2
        Gf = lambda P0: p["c"] * p["Pi"]**2 / (p["Pi"]**2 + P0**2)
    f = lambda P0: sig2(Gm(P0), Pi, lam, Sig)
    d = lambda P0: dsig2_dG(Gm(P0), Pi, lam, Sig) * dG(P0)

    def ffl(P0):
        P0 = float(P0)
        if not math.isfinite(P0) or P0 <= 0:
            return float("nan")
        G = Gf(P0)
        return (p["Sig"] + G * G / (2 * p["Pi"])) / (p["lam"] + G)
    return Curve(f, d, lambda t: ZREL * abs(f(t)) / t, 0, [], ffl, "Pi0 monotone"), sig2(c, Pi, lam, Sig), Sig / lam, -80, 80


def c_blind(kind, p):
    from t10_blind import make
    q = mpize(p)
    lam, Sig = q["lam"], q["Sig"]
    cur = make(kind, p)
    sh = cur.shift
    if kind == "Pi0 bayes":
        Lm, Lp = sig2(q["c"], q["Pi"], lam, Sig), Sig / lam
    elif kind == "c bayes":
        Lm, Lp = Sig / lam, mp.inf
    elif kind == "tau ZF relay":
        G = q["G"]
        Lm, Lp = sig2(G, q["Pi"], lam, Sig), Sig / (lam + G)
    elif kind == "tau ZF optimal":
        Lm, Lp = sstar(lam, Sig, q["Pi"]), mp.mpf(0)
    elif kind == "tau var relay":
        G, v = q["G"], q["v"]
        a = lam + G
        Lm, Lp = Sig / a, (Sig + G**2 * v / a) / a
    else:                                                     # tau var optimal
        Lm, Lp = mp.mpf(0), mp.mpf(0)
    return cur, Lm, Lp, -80 + sh, 80 + sh


def c_power(p):
    beta, K, lam, Sig = (mp.mpf(p[k]) for k in ("beta", "K", "lam", "Sig"))
    Lm, Lp, xm, xp = limits_pow(beta, K, lam, Sig)
    l10 = mp.log10(lam)
    if beta == 2:                                             # T11 diagnosis: proved limit at beta = 2
        Lp, xp = sstar(lam, Sig, lam**2 / K), mp.mpf(80) - l10
    elif beta > 2:                                            # T11 diagnosis: bracket from the tau^{2-beta} approach
        xp = max(mp.mpf(80), 50 / (beta - 2)) - l10
    return power_curve(beta, K, lam, Sig), Lm, Lp, xm, xp


def c_delay(p):
    lam, Sig, Pi = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi"))
    s2 = sstar(lam, Sig, Pi)
    F = Sig / lam
    f = lambda th: P_delay(th * mp.exp(-th), lam, Sig, Pi)
    d = lambda th: 2 * lam * mp.exp(-2 * lam * th * mp.exp(-th)) * (F - s2) * (1 - th) * mp.exp(-th)
    lf, Ff, s2f = p["lam"], float(F), float(s2)

    def ffl(th):
        th = float(th)
        if not math.isfinite(th) or th <= 0:
            return float("nan")
        dd = th * math.exp(-th) if th < 700 else 0.0
        return Ff - math.exp(-2 * lf * dd) * (Ff - s2f)
    return Curve(f, d, lambda th: ZREL * abs(f(th)) / th, 0, [mp.mpf(0)], ffl, "delay"), s2, s2, -80, 80


# ---------------------------------------------------------------- parameter draws
def draw(row, rng, i):
    nm = ROWS[row][0]
    if row == 1:
        return {"lam": U(rng), "Sig": U(rng)}
    if row in (2, 3, 4, 5, 6, 7, 8, 9):
        p = {"lam": U(rng), "Sig": U(rng)}
        if row == 2:
            p.update(c=U(rng), Pi0=U(rng))
        elif row == 3:
            p.update(lam1=U(rng), Sig1=U(rng))
        elif row == 4:
            p.update(g=U(rng), c=U(rng))
        elif row == 5:
            p.update(G0=U(rng))
        elif row == 6:
            p.update(c=U(rng), Pi0=U(rng), n=2.0)
        elif row == 7:
            p.update(c=U(rng), Pi0=U(rng), n=float(10.0**rng.uniform(np.log10(1.01), 1)))
        else:
            Pi01 = U(rng)
            p.update(c1=U(rng), c2=U(rng), Pi01=Pi01, Pi02=Pi01 * float(10.0**rng.uniform(1, 6)))
        return p
    if row == 10:
        return {"lam": U(rng), "Sig": U(rng), "Pi": U(rng), "c": U(rng)}
    if row == 11:
        return {"lam": U(rng), "Sig": U(rng), "Pi": U(rng), "Pi0": U(rng)}
    if row == 12:
        return {"lam": U(rng), "Sig": U(rng), "Pi": U(rng), "c": U(rng), "g": ["tanh", "exp", "hill"][int(rng.integers(3))]}
    if row in (13, 14):
        p = {"lam": U(rng), "Sig": U(rng), "Pi": U(rng)}
        if row == 13:
            p["G"] = U(rng)
        return p
    if row in (15, 16):
        p = {"lam": U(rng), "Sig": U(rng), "v": U(rng)}
        if row == 15:
            p["G"] = U(rng)
        return p
    if row in (17, 18, 19):
        if row == 17:
            beta = 0.0 if i >= 900 else float(rng.uniform(-2, 0))
            while beta == 0.0 and i < 900:
                beta = float(rng.uniform(-2, 0))
        elif row == 18:
            beta = float(rng.uniform(0, 2))
            while beta == 0.0:
                beta = float(rng.uniform(0, 2))
        else:
            beta = 2.0 if i >= 900 else float(4 - rng.uniform(0, 2))
        return {"beta": beta, "K": U(rng), "lam": U(rng), "Sig": U(rng)}
    if row == 20:
        return {"lam": U(rng), "Sig": U(rng), "Pi": U(rng)}
    if 21 <= row <= 34:
        fam = nm.split()[1]
        p = {"lam": U(rng), "Sig": U(rng), "Pi": U(rng)}
        if fam == "D1":
            p["G"] = U(rng)
        elif fam == "D2":
            p.update(c=float(2 * 10.0**rng.uniform(-4, 0)), Pi0=U(rng))
        elif fam == "D3":
            p["rho"] = U(rng)
        return p
    fam = nm.split()[1]
    p = {"lam": U(rng), "Pi": U(rng)}
    p.update({"B2": {"G": U(rng)}, "B3": {"rho": U(rng)}, "B4": {"lam1": U(rng)}, "B5": {}}[fam])
    return p


def analyse_row(row, p):
    nm = ROWS[row][0]
    if row == 1:
        cur, Lm, Lp, xm, xp = c_pi_optimal(p)
    elif row <= 9:
        fam = {2: "bayes", 3: "misspec", 4: "capped", 5: "blind", 6: "hill", 7: "hill", 8: "bayes2", 9: "hill2"}[row]
        cur, Lm, Lp, xm, xp = c_pi(fam, p)
    elif row in (10, 11, 13, 14, 15, 16):
        cur, Lm, Lp, xm, xp = c_blind({10: "Pi0 bayes", 11: "c bayes", 13: "tau ZF relay", 14: "tau ZF optimal",
                                       15: "tau var relay", 16: "tau var optimal"}[row], p)
    elif row == 12:
        cur, Lm, Lp, xm, xp = c_pi0_monotone(p)
    elif row in (17, 18, 19):
        cur, Lm, Lp, xm, xp = c_power(p)
    elif row == 20:
        cur, Lm, Lp, xm, xp = c_delay(p)
    elif row <= 34:
        from t12_common import analyse_dt
        fam, met = nm.split()[1], nm.split()[2]
        return analyse_dt(fam, met, p)
    else:
        from t12_common import analyse_sig
        fam, conv = nm.split()[1], nm.split()[2]
        return analyse_sig(fam, conv, p)
    return analyse_with_limits(cur, Lm, Lp, mp.mpf(xm), mp.mpf(xp))


def tolerances(A, rng):
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    if not crit:
        sh = A["curve"].shift
        return [A["curve"].f(mp.power(10, sh + mp.mpf(float(x)))) for x in rng.uniform(-20, 20, 100)], 0
    lo, hi = float(mp.log10(min(crit) / 2)), float(mp.log10(2 * max(crit)))
    out = [mp.power(10, mp.mpf(float(x))) for x in rng.uniform(lo, hi, 50)]
    for i in range(50):
        cv = crit[int(rng.integers(len(crit)))]
        out.append(cv if i < 10 else cv * (1 + mp.mpf(float(rng.uniform(-1, 1))) * mp.mpf("1e-6")))
    return out, len(crit)


def job(args):
    row, i, p, seed = args
    rng = np.random.default_rng(seed)
    allowed = ROWS[row][1]
    t0 = time.time()
    A = analyse_row(row, p)
    R2s, ncrit = tolerances(A, rng)
    has_fl = A["curve"].ffl is not None
    counts, flagged, persist = {}, 0, []
    for R2 in R2s:
        ci = route_i(A, R2, EQ)
        if has_fl:
            try:
                cii, _ = route_ii(A, R2, prec="fl")
            except Exception as e:  # noqa: BLE001
                cii = f"float error: {type(e).__name__}"
        else:
            cii, _ = route_ii(A, R2, prec="mp")
        if ci != cii or ci not in allowed or cii not in allowed:
            flagged += 1
            with mp.workdps(60):
                ci2 = route_i(A, R2, EQ)
                cii2, _ = route_ii(A, R2, prec="mp")
            if ci2 != cii2 or ci2 not in allowed:
                persist.append({"p": p, "R2": R2, "route_i": name(ci2), "route_ii": name(cii2)})
            ci = ci2
        counts[name(ci)] = counts.get(name(ci), 0) + 1
    return {"i": i, "counts": counts, "flagged": flagged, "persist": persist,
            "kinds": "-".join(t["kind"] for t in A["turns"]) or "none", "limit_ok": bool(all(A["limit_check"])),
            "n_crit": ncrit, "float_route": has_fl, "seconds": time.time() - t0}


def run_row(row):
    fn = os.path.join(ROWDIR, f"row_{row:02d}.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    rng = np.random.default_rng(13100 + row)
    jobs = []
    for i in range(N):
        p = draw(row, rng, i)
        jobs.append((row, i, p, int(rng.integers(2**63))))
    t0 = time.time()
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=5)
    cnt, kh = {}, {}
    for r in res:
        for c_, v in r["counts"].items():
            cnt[c_] = cnt.get(c_, 0) + v
        kh[r["kinds"]] = kh.get(r["kinds"], 0) + 1
    stated = sorted(name(c) for c in ROWS[row][1])
    per = [x for r in res for x in r["persist"]]
    out = {"row": row, "name": ROWS[row][0], "stated": stated, "curves": len(res), "classifications": sum(cnt.values()),
           "classes": cnt, "kinds_hist": kh, "flagged": sum(r["flagged"] for r in res), "persisting": len(per),
           "persist_examples": per[:10], "missing_stated": [c for c in stated if c not in cnt],
           "out_of_set": [c for c in cnt if c not in stated], "n_limit_fail": sum(not r["limit_ok"] for r in res),
           "float_route": all(r["float_route"] for r in res), "max_turning_points": max(len(r["kinds"].split("-")) if r["kinds"] != "none" else 0 for r in res),
           "seconds": time.time() - t0}
    out["pass"] = not per and not out["missing_stated"] and not out["out_of_set"]
    with open(fn, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"row {row:2d} {ROWS[row][0]:22s} {'PASS' if out['pass'] else 'FAIL'} classes {cnt} missing {out['missing_stated']} "
          f"out {out['out_of_set']} flagged {out['flagged']} persisting {len(per)} limit_fail {out['n_limit_fail']} "
          f"tp {kh} {out['seconds']:.0f}s", flush=True)
    return out


def main():
    t0 = time.time()
    rows = ONLY or sorted(ROWS)
    allr = [run_row(r) for r in rows]
    R = {"N": N, "rows": allr, "pass": all(r["pass"] for r in allr),
         "n_pass": sum(r["pass"] for r in allr), "total_classifications": sum(r["classifications"] for r in allr),
         "seconds": time.time() - t0}
    print(f"C2: {'PASS' if R['pass'] else 'FAIL'} ({R['n_pass']}/{len(allr)} rows), {R['total_classifications']:,} classifications")
    if ONLY is None:
        save_json(R, "t13_audit_classes.json" if N == 1000 else f"t13_audit_classes_n{N}.json")


if __name__ == "__main__":
    main()
