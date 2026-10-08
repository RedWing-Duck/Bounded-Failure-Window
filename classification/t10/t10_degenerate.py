"""T10.5: degeneracies — equal-height maxima, inflection, plateau, pair birth, narrow windows."""
import time

import mpmath as mp
import numpy as np

from classify import classify, name
from t10_census import hill_count, pair_birth
from t10_common import T, analyse, mpize, pi_curve, save_json
from t10_construct import PL, Target, envelope_target, v0, v0_dx

t0 = time.time()
lam, Sig = mp.mpf(1), mp.mpf("0.01")
F = Sig / lam
D6 = mp.mpf("1e-6")
R = {}

# ---------------- equal-height maxima
M2, lo = 2 * F, F / 4
tg = envelope_target(lam, Sig, PL([lo, M2, lo, M2, lo], 0, 0))
A = analyse(tg.curve())
rows = []
for lab, R2, want in (("M2(1-1e-6)", M2 * (1 - D6), (0, 0, 2)), ("M2", M2, (0, 0, 0)), ("M2(1+1e-6)", M2 * (1 + D6), (0, 0, 0))):
    r = classify(A, R2)
    rows.append({"R2": lab, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]), "expected": name(want),
                 "pass": r["route_i"] == want and r["route_ii"] == want})
R["equal_maxima"] = {"turns": [(t["theta"], t["value"], t["kind"]) for t in A["turns"]], "rows": rows,
                     "pass": all(x["pass"] for x in rows)}
print("equal maxima:", [(x["R2"], x["route_i"], x["route_ii"]) for x in rows])


# ---------------- inflection vs smoothed
def infl_curve(smooth):
    P_, Aa, B = 3 * F, mp.mpf("1.5") * F, F / 2
    lo_ = F / 4
    xs = [mp.mpf(6), mp.mpf(7), mp.mpf(8), mp.mpf(10), mp.mpf(11)]
    beta = mp.mpf("0.1")

    def cub(x):
        z = x - 9
        return Aa - B * ((z**3 + beta * z) / (1 + beta) if smooth else z**3)

    def dcub(x):
        z = x - 9
        return -B * ((3 * z**2 + beta) / (1 + beta) if smooth else 3 * z**2)
    base = PL([lo_, P_, Aa + B, Aa - B, lo_], 0, 0, xs=xs)

    def w(x):
        return cub(x) if 8 <= x <= 10 else base(x)

    def dw(x):
        return dcub(x) if 8 <= x <= 10 else base.d(x)

    def val(x):
        return max(v0(T(x), lam, Sig), w(x))

    def dval(x):
        return dw(x) if w(x) >= v0(T(x), lam, Sig) else v0_dx(T(x), lam, Sig)
    # crossing of v0 and w on the left tail
    h = lambda x: w(x) - v0(T(x), lam, Sig)
    xc = mp.findroot(h, (mp.mpf(0), mp.mpf(6)), solver="bisect", tol=mp.mpf("1e-45"))
    return Target(lam, Sig, val, dval, xs + [mp.mpf(9), xc])


Ai, As = analyse(infl_curve(False).curve()), analyse(infl_curve(True).curve())
same_tp = (len(Ai["turns"]) == len(As["turns"]) and all(
    a["kind"] == b["kind"] and abs(a["value"] - b["value"]) <= mp.mpf("1e-20") for a, b in zip(Ai["turns"], As["turns"])))
crit_v = [v for v in [Ai["L_minus"], Ai["L_plus"]] + [t["value"] for t in Ai["turns"]] if mp.isfinite(v) and v > 0]
rng = np.random.default_rng(10005)
tols = [mp.mpf(10) ** mp.mpf(float(x)) for x in rng.uniform(float(mp.log10(min(crit_v) / 2)), float(mp.log10(2 * max(crit_v))), 1000)]
mism, disagree = 0, 0
for R2 in tols:
    ri, rs = classify(Ai, R2), classify(As, R2)
    disagree += int(not ri["agree"]) + int(not rs["agree"])
    mism += int(ri["route_i"] != rs["route_i"] or ri["route_ii"] != rs["route_ii"])
R["inflection"] = {"tp_inflection": [(t["theta"], t["value"], t["kind"]) for t in Ai["turns"]],
                   "tp_smoothed": [(t["theta"], t["value"], t["kind"]) for t in As["turns"]], "same_turning_points": same_tp,
                   "n_tolerances": len(tols), "class_mismatches": mism, "route_disagreements": disagree,
                   "pass": bool(same_tp and mism == 0 and disagree == 0)}
print(f"inflection: same TPs {same_tp}, mismatches {mism}, route disagreements {disagree}")

# ---------------- plateau (capped, g = 2F)
q = mpize({"lam": 1.0, "Sig": 0.01, "c": 1.0})
q["g"] = 2 * F
Ap = analyse(pi_curve("capped", q))
rows = []
for lab, R2, want in (("F(1-1e-6)", F * (1 - D6), (1, 0, 0)), ("F", F, (0, 0, 0)), ("F(1+1e-6)", F * (1 + D6), (0, 0, 0))):
    r = classify(Ap, R2)
    ok = r["route_i"] == want and r["route_ii"] == want
    if want == (1, 0, 0) and ok:
        ok = r["ends"][0][1] > q["c"] / q["g"]
    rows.append({"R2": lab, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]), "expected": name(want),
                 "ends": r["ends"], "pass": bool(ok)})
R["plateau"] = {"turns": len(Ap["turns"]), "rows": rows, "c_over_g": q["c"] / q["g"], "pass": all(x["pass"] for x in rows)}
print("plateau:", [(x["R2"], x["route_i"], x["route_ii"]) for x in rows])

# ---------------- pair birth (Hill n = 2)
pbr = pair_birth(2)["transitions"][0]
P0p = pbr["Pi0_double_root"] or pbr["Pi0_bisect"]
rows = []
for e in range(6, 13):
    d = mp.power(10, -e)
    A_ = hill_count(2, P0p * (1 - d))
    ts = A_["turns"]
    if len(ts) == 2:
        rows.append({"delta": d, "M_minus_m": ts[1]["value"] - ts[0]["value"], "x_sep": ts[1]["x"] - ts[0]["x"]})
    else:
        rows.append({"delta": d, "n_tp": len(ts)})
plus = len(hill_count(2, P0p * (1 + D6))["turns"])
good = [r for r in rows if "M_minus_m" in r]
mono = all(good[i + 1]["M_minus_m"] < good[i]["M_minus_m"] for i in range(len(good) - 1)) and len(good) == 7
ld = np.log10([float(r["delta"]) for r in good])
slope_v = float(np.polyfit(ld, np.log10([float(r["M_minus_m"]) for r in good]), 1)[0]) if len(good) > 1 else None
slope_x = float(np.polyfit(ld, np.log10([float(r["x_sep"]) for r in good]), 1)[0]) if len(good) > 1 else None
R["pair_birth"] = {"Pi0_pair": P0p, "rows": rows, "n_tp_at_plus_1e-6": plus, "monotone": bool(mono),
                   "slope_M_minus_m": slope_v, "slope_position_sep": slope_x,
                   "pass": bool(mono and slope_v is not None and 0.4 <= slope_v <= 0.6)}
print(f"pair birth: Pi0_pair = {mp.nstr(P0p, 15)}; slope(M - m) = {slope_v:.4f}, slope(x sep) = {slope_x:.4f}, "
      f"TPs at +1e-6: {plus}")

# ---------------- narrow windows
R2 = mp.mpf("1.01") * F
lo_, hi_ = R2 / 2, 2 * R2
hw = mp.log10(1 + mp.mpf("1e-8")) / 2
nw_rows = []
for i in range(20):
    k = int(rng.integers(1, 6))
    while True:
        cs = np.sort(rng.uniform(6, 15, size=k))
        if k == 1 or np.min(np.diff(cs)) >= 0.5:
            break
    xs, vs = [mp.mpf(5)], [lo_]
    for cc in cs:
        cm = mp.mpf(float(cc))
        xs += [cm - hw, cm, cm + hw]
        vs += [lo_, hi_, lo_]
    xs.append(mp.mpf(16))
    vs.append(lo_)
    w = PL(vs, 0, 0, xs=xs)
    tg = envelope_target(lam, Sig, w)
    A_ = analyse(tg.curve())
    r = classify(A_, R2)
    widths = [(b / a - 1) for a, b in r["ends"] if a is not None and b is not None]
    wok = len(widths) == k and all(mp.mpf("0.5e-8") <= x <= mp.mpf("2e-8") for x in widths)
    gx = np.linspace(-25, 25, 10000)
    hits = 0
    for cc in cs:
        lo_x, hi_x = float(cc) - float(hw), float(cc) + float(hw)
        hits += int(np.any((gx > lo_x) & (gx < hi_x)))
    ok = r["route_i"] == (0, 0, k) and r["route_ii"] == (0, 0, k) and wok
    nw_rows.append({"k": k, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]),
                    "widths_rel": widths, "grid_1e4_windows_found": hits, "pass": bool(ok)})
R["narrow"] = {"rows": nw_rows, "n_found": sum(r["pass"] for r in nw_rows),
               "windows_total": sum(r["k"] for r in nw_rows),
               "grid_windows_found": sum(r["grid_1e4_windows_found"] for r in nw_rows),
               "pass": all(r["pass"] for r in nw_rows)}
print(f"narrow windows: classifier correct in {R['narrow']['n_found']}/20 curves; a 1e4-point log grid hits "
      f"{R['narrow']['grid_windows_found']}/{R['narrow']['windows_total']} windows")

R["pass"] = all(R[k]["pass"] for k in ("equal_maxima", "inflection", "plateau", "pair_birth", "narrow"))
R["seconds"] = time.time() - t0
print(f"T10.5: {'PASS' if R['pass'] else 'FAIL'} " + str({k: R[k]["pass"] for k in ("equal_maxima", "inflection", "plateau", "pair_birth", "narrow")}))
save_json(R, "t10_5.json")
