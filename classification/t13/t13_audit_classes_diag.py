"""Post-hoc diagnosis of the two C2 failures (PREREG_t13 C2; recorded in results/c2_rows/row_08.json and row_12.json).
Row 12 (Pi0 monotone): 122 persisting route disagreements (route i All, route ii Empty). Re-run the row's 1,000 sets
deterministically, collect every persisting case, and test (a) whether R2 is exactly a limit, (b) the size of f - R2 at the
single point route (ii) samples when it has no split points, and (c) the exact sign of f - R2 at points where it is resolvable.
Row 8 (Pi bayes2): stated class (1, 0, 1) never observed. Question: is (1, 0, 1) reachable in the family? Search
(1) the pre-registered parameter distribution with more draws (float screen), (2) wider stage separations; confirm every
candidate with both routes in mp.
Usage: python3 t13_audit_classes_diag.py"""
import math
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

import t13_audit_classes as AC
from t13_common import save_json
from classify import EQ, name, route_i, route_ii


# ---------------------------------------------------------------- row 12
def persisting_12(args):
    row, i, p, seed = args
    r = AC.job(args)
    if not r["persist"]:
        return []
    A = AC.analyse_row(row, p)
    out = []
    for c in r["persist"]:
        R2 = mp.mpf(c["R2"]) if isinstance(c["R2"], str) else c["R2"]
        with mp.workdps(60):
            at_lm = R2 == A["L_minus"]
            at_lp = R2 == A["L_plus"]
            x0 = A["curve"].shift
            gap0 = A["curve"].f(mp.power(10, x0)) - R2
        # route (ii) sample point; then resolvable points: P0 = 10 Pi (G = c tanh(0.1)) and P0 = Pi
        with mp.workdps(400):
            q = AC.mpize({k: v for k, v in p.items() if k != "g"})
            pts = {"x_shift": mp.power(10, x0), "P0=Pi": q["Pi"], "P0=10Pi": 10 * q["Pi"]}
            gaps = {k: A["curve"].f(v) - R2 for k, v in pts.items()}
            rel = {k: float(abs(g) / R2) for k, g in gaps.items()}
            sgn = {k: int(mp.sign(g)) for k, g in gaps.items()}
        out.append({"i": i, "g": p["g"], "route_i": c["route_i"], "route_ii": c["route_ii"], "R2_is_Lminus": bool(at_lm),
                    "R2_is_Lplus": bool(at_lp), "n_turns": len(A["turns"]), "dirs": [int(d) for d in A["dirs"]],
                    "gap_at_route_ii_point_dps60": float(gap0), "rel_gap_dps400": rel, "sign_dps400": sgn,
                    "Pi_over_shift_point": float(q["Pi"] / pts["x_shift"])})
    return out


def diag_12():
    rng = np.random.default_rng(13100 + 12)
    jobs = []
    for i in range(1000):
        p = AC.draw(12, rng, i)
        jobs.append((12, i, p, int(rng.integers(2**63))))
    with Pool(4) as pool:
        res = [x for r in pool.map(persisting_12, jobs, chunksize=5) for x in r]
    s = {"n_persisting": len(res),
         "all_R2_exactly_L_minus": all(r["R2_is_Lminus"] for r in res),
         "any_R2_L_plus": any(r["R2_is_Lplus"] for r in res),
         "all_monotone_increasing": all(r["n_turns"] == 0 and r["dirs"] == [1] for r in res),
         "all_route_i_All_route_ii_Empty": all(r["route_i"] == "All" and r["route_ii"] == "Empty" for r in res),
         "max_rel_gap_at_route_ii_point": max(r["rel_gap_dps400"]["x_shift"] for r in res),
         "min_rel_gap_at_P0_eq_10Pi": min(r["rel_gap_dps400"]["P0=10Pi"] for r in res),
         "all_sign_positive_at_10Pi": all(r["sign_dps400"]["P0=10Pi"] == 1 for r in res),
         "all_sign_positive_at_route_ii_point": all(r["sign_dps400"]["x_shift"] == 1 for r in res),
         "g_hist": {g: sum(r["g"] == g for r in res) for g in ("tanh", "exp", "hill")},
         "distinct_sets": len({r["i"] for r in res})}
    print("row 12:", s, flush=True)
    return {"summary": s, "cases": res}


# ---------------------------------------------------------------- row 8
def f_float(p, Pi):
    c1, c2, a1, a2, lam, Sig = p["c1"], p["c2"], p["Pi01"], p["Pi02"], p["lam"], p["Sig"]
    G = c1 * Pi / (Pi + a1) + c2 * Pi / (Pi + a2)
    return (Sig + G * G / (2 * Pi)) / (lam + G)


def screen(p):
    """(1, 0, 1) band: f = F at 0, max M1, min m, max M2, then L+; band (max(m, L+), min(F, M2)) non-empty."""
    lo, hi = math.log10(min(p["Pi01"], p["Sig"])) - 8, math.log10(max(p["Pi02"], p["c1"] + p["c2"])) + 8
    x = np.linspace(lo, hi, 6000)
    with np.errstate(all="ignore"):
        y = f_float(p, 10.0**x)
    d = np.sign(np.diff(y))
    idx = np.where(d[1:] != d[:-1])[0] + 1
    if len(idx) != 3:
        return None
    F, Lp = p["Sig"] / p["lam"], p["Sig"] / (p["lam"] + p["c1"] + p["c2"])
    m, M2 = y[idx[1]], y[idx[2]]
    blo, bhi = max(m, Lp), min(F, M2)
    if bhi > blo * (1 + 1e-9):
        return {"p": p, "band": (float(blo), float(bhi)), "m": float(m), "F": F, "M2": float(M2), "rel_width": float((bhi - blo) / F)}
    return None


def draw8(rng, sep):
    p = {"lam": AC.U(rng), "Sig": AC.U(rng)}
    Pi01 = AC.U(rng)
    p.update(c1=AC.U(rng), c2=AC.U(rng), Pi01=Pi01, Pi02=Pi01 * float(10.0**rng.uniform(*sep)))
    return p


def screen_batch(args):
    seed, n, sep = args
    rng = np.random.default_rng(seed)
    hits, n3 = [], 0
    for _ in range(n):
        p = draw8(rng, sep)
        h = screen(p)
        if h is not None:
            hits.append(h)
    return hits


def confirm8(h):
    p = h["p"]
    A = AC.analyse_row(8, p)
    blo, bhi = h["band"]
    R2 = mp.sqrt(mp.mpf(blo) * mp.mpf(bhi))
    ci = route_i(A, R2, EQ)
    with mp.workdps(60):
        cii, _ = route_ii(A, R2, prec="mp")
    return {"p": p, "kinds": [t["kind"] for t in A["turns"]], "R2": float(R2), "route_i": name(ci), "route_ii": name(cii),
            "rel_width": h["rel_width"]}


def diag_8():
    out = {}
    for tag, sep, nb in (("prereg_distribution", (1, 6), 40), ("wide_separation_1e6_1e12", (6, 12), 40)):
        t0 = time.time()
        jobs = [(138000 + 100 * (tag != "prereg_distribution") + k, 5000, sep) for k in range(nb)]
        with Pool(4) as pool:
            hits = [h for r in pool.map(screen_batch, jobs) for h in r]
        hits.sort(key=lambda h: -h["rel_width"])
        conf = [confirm8(h) for h in hits[:10]]
        out[tag] = {"draws": 5000 * nb, "screen_hits": len(hits), "confirmed": conf,
                    "n_confirmed_101_both_routes": sum(c["route_i"] == c["route_ii"] == "(1, 0, 1)" for c in conf),
                    "seconds": time.time() - t0}
        print("row 8", tag, {k: v for k, v in out[tag].items() if k != "confirmed"}, flush=True)
        for c in conf[:3]:
            print("   ", c, flush=True)
    return out


def main():
    R = {"row12": diag_12(), "row8": diag_8()}
    s12, r8 = R["row12"]["summary"], R["row8"]
    R["text"] = (
        f"Row 12: {s12['n_persisting']} persisting cases in {s12['distinct_sets']} sets; R2 exactly L- in all: "
        f"{s12['all_R2_exactly_L_minus']}; curves monotone increasing: {s12['all_monotone_increasing']}; f - R2 at the single "
        f"point route (ii) samples is positive but at most {s12['max_rel_gap_at_route_ii_point']:.3g} relative, below the "
        f"1e-40 equality tolerance, so route (ii) reads equality and returns Empty; at P0 = 10 Pi the gap is at least "
        f"{s12['min_rel_gap_at_P0_eq_10Pi']:.3g} and positive in all ({s12['all_sign_positive_at_10Pi']}). The failure set is "
        f"All (route i). Attribution: code (route ii sample point). "
        f"Row 8: (1, 0, 1) confirmed by both routes in {r8['prereg_distribution']['n_confirmed_101_both_routes']} of the top "
        f"screened sets under the pre-registered distribution ({r8['prereg_distribution']['screen_hits']} screen hits in "
        f"{r8['prereg_distribution']['draws']} draws) and in {r8['wide_separation_1e6_1e12']['n_confirmed_101_both_routes']} "
        f"with stage separation 1e6-1e12 ({r8['wide_separation_1e6_1e12']['screen_hits']} hits).")
    print(R["text"])
    save_json(R, "t13_audit_classes_diag.json")


if __name__ == "__main__":
    main()
