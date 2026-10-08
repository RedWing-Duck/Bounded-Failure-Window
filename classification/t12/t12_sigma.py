"""Part B census: B2, B3, B4, B5 x {absolute, relative}, 2,000 sets each (seed 12020), 10 tolerances, both routes (mp).
PASS iff turning-point counts and classes match the B2-B5 predictions and the routes agree everywhere."""
import time
from multiprocessing import Pool

import mpmath as mp
import numpy as np

from t12_a8 import tolerances as _tol_crit
from t12_common import analyse_sig, classify, name, save_json

FAMS = ("B2", "B3", "B4", "B5")
EXTRA = {"B2": ("G",), "B3": ("rho",), "B4": ("lam1",), "B5": ()}
LR, UR, WIN, EMP = (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)
ALLOWED = {("B2", "abs"): {"All", UR}, ("B2", "rel"): {"All", LR}, ("B3", "abs"): {UR, "All"},
           ("B3", "rel"): {LR, WIN, EMP}, ("B4", "abs"): {UR, "All"}, ("B4", "rel"): {LR, WIN, EMP},
           ("B5", "abs"): {UR, "All"}, ("B5", "rel"): {LR, EMP}}


def predicted_turns(fam, conv, p):
    """Predicted kinds sequence and (for a maximum) its position u_M."""
    if conv == "abs" or fam in ("B2", "B5"):
        return [], None
    lam = mp.mpf(p["lam"])
    if fam == "B3":
        rho = mp.mpf(p["rho"])
        if rho <= 2:
            return [], None
        wM = ((rho - 1) + mp.sqrt(2 * rho * (rho - 1))) / (1 + rho)
        return ["max"], (wM**2 - 1) / rho
    l1 = mp.mpf(p["lam1"])
    if l1 >= lam / 2:
        return [], None
    GM = -l1 + mp.sqrt(lam * l1 - l1**2)
    return ["max"], (GM**2 + 2 * l1 * GM) / lam**2


def tolerances(A, rng):
    """As A8; a curve with no finite positive critical value (0 -> oo, monotone; not covered by the pre-registration)
    gets 10 values of the curve itself at u log-uniform on [1e-20, 1e20] (recorded in RESULTS_t12.md)."""
    crit = [v for v in [A["L_minus"], A["L_plus"]] + [t["value"] for t in A["turns"]] if mp.isfinite(v) and v > 0]
    if crit:
        return _tol_crit(A, rng)
    return [A["curve"].f(mp.power(10, mp.mpf(float(x)))) for x in rng.uniform(-20, 20, 10)]


def draw(rng, fam):
    U = lambda: float(10.0**rng.uniform(-2, 2))
    p = {"lam": U(), "Pi": U()}
    for k in EXTRA[fam]:
        p[k] = U()
    return p


def job(args):
    fam, i, p, seed = args
    rng = np.random.default_rng(seed)
    out = {"fam": fam, "i": i, "p": p, "conv": {}}
    for conv in ("abs", "rel"):
        A = analyse_sig(fam, conv, p)
        kinds = [t["kind"] for t in A["turns"]]
        pk, uM = predicted_turns(fam, conv, p)
        pos_err = abs(A["turns"][0]["theta"] / uM - 1) if (pk and kinds == pk) else None
        cls, agree, outset = {}, True, []
        for R2 in tolerances(A, rng):
            C = classify(A, R2)
            agree &= C["agree"]
            k = name(C["route_i"])
            cls[k] = cls.get(k, 0) + 1
            if C["route_i"] not in ALLOWED[(fam, conv)] or C["route_ii"] not in ALLOWED[(fam, conv)]:
                outset.append({"R2": R2, "route_i": name(C["route_i"]), "route_ii": name(C["route_ii"])})
        ok = kinds == pk and agree and not outset and all(A["limit_check"]) and (pos_err is None or pos_err <= mp.mpf("1e-10"))
        out["conv"][conv] = {"kinds": kinds, "pred_kinds": pk, "pos_rel_err": pos_err, "classes": cls, "agree": bool(agree),
                             "out_of_set": outset, "limit_check": A["limit_check"], "pass": bool(ok),
                             "turns": [(t["kind"], t["theta"], t["value"]) for t in A["turns"]]}
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(12020)
    jobs = [(fam, i, draw(rng, fam), int(rng.integers(2**63))) for fam in FAMS for i in range(2000)]
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=10)
    R = {"by": {}}
    for fam in FAMS:
        for conv in ("abs", "rel"):
            rr = [r["conv"][conv] for r in res if r["fam"] == fam]
            hist, cls = {}, {}
            for r in rr:
                k = "-".join(r["kinds"]) or "none"
                hist[k] = hist.get(k, 0) + 1
                for c_, v in r["classes"].items():
                    cls[c_] = cls.get(c_, 0) + v
            pe = [r["pos_rel_err"] for r in rr if r["pos_rel_err"] is not None]
            R["by"][f"{fam} {conv}"] = {
                "n": len(rr), "n_pass": sum(r["pass"] for r in rr), "kinds_hist": hist, "classes": cls,
                "allowed": sorted(name(c) for c in ALLOWED[(fam, conv)]),
                "n_pred_max": sum(r["pred_kinds"] == ["max"] for r in rr),
                "n_count_mismatch": sum(r["kinds"] != r["pred_kinds"] for r in rr),
                "n_disagree_sets": sum(not r["agree"] for r in rr), "n_out_of_set": sum(len(r["out_of_set"]) for r in rr),
                "n_limit_fail": sum(not all(r["limit_check"]) for r in rr),
                "max_pos_rel_err": max(pe) if pe else None,
                "fails": [dict(r, p=q["p"]) for q, r in ((q, q["conv"][conv]) for q in res if q["fam"] == fam) if not r["pass"]][:20]}
            print(fam, conv, R["by"][f"{fam} {conv}"]["n_pass"], hist, cls, flush=True)
    R["B4_pass"] = all(R["by"][f"B4 {c}"]["n_pass"] == 2000 for c in ("abs", "rel"))
    R["B235_pass"] = all(R["by"][f"{f} {c}"]["n_pass"] == 2000 for f in ("B2", "B3", "B5") for c in ("abs", "rel"))
    R["seconds"] = time.time() - t0
    print("B4", R["B4_pass"], "B2/B3/B5", R["B235_pass"])
    save_json(R, "t12_sigma.json")


if __name__ == "__main__":
    main()
