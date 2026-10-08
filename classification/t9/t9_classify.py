"""T9.4: Propositions 2.3 and 3.3 checked row by row on 2,000 random sets (+ G at 2F Pi (1 + delta))."""
import sys
import time

import mpmath as mp
import numpy as np

from t9_common import (analyse, classify, crit, draw_sets, name, opt_sweep, relay_sweep, save_json, tau_F, tau_R,
                       tau_star_R)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
D6 = mp.mpf("1e-6")
t0 = time.time()
sets = draw_sets(np.random.default_rng(9004), N)


def pred_relay(R2, c, G2FP):
    if R2 <= c["H_G"]:
        return "All"
    if R2 < c["V_w"]:
        return "lower ray"
    return "Empty"


stats = {"relay": 0, "optimal": 0, "class_mismatch": 0, "endpoint_mismatch": 0, "limit_check_fail": 0,
         "turning_points": 0, "classes": {}, "max_endpoint_rel": 0.0,
         "limit_check_fail_by": {"optimal L-": 0, "optimal L+": 0, "relay L-": 0, "relay L+": 0}, "optimal_L_plus_max": 0.0}
bad = []
opt_cache = {}


def record(kind, params, label, R2, got, want, comp, ref_end):
    stats[kind] += 1
    stats["classes"][got] = stats["classes"].get(got, 0) + 1
    if got != want:
        stats["class_mismatch"] += 1
        bad.append({"kind": kind, "params": params, "row": label, "R2": R2, "got": got, "expected": want})
        return
    if want == "lower ray":
        end = comp[0][1]
        e = abs(end - ref_end) / ref_end
        stats["max_endpoint_rel"] = max(stats["max_endpoint_rel"], float(e))
        if e > mp.mpf("1e-8"):
            stats["endpoint_mismatch"] += 1
            bad.append({"kind": kind, "params": params, "row": label, "R2": R2, "end": end, "expected_end": ref_end})


for i in range(N):
    lam, Sig, Pi, G0 = (mp.mpf(float(x)) for x in sets[i])
    F = Sig / lam
    # optimal filter does not depend on G: once per set
    c = crit(lam, Sig, Pi, G0)
    A = analyse(*opt_sweep(lam, Sig, Pi), lam)
    stats["limit_check_fail"] += int(not all(A["limit_check"]))
    stats["limit_check_fail_by"]["optimal L-"] += int(not A["limit_check"][0])
    stats["limit_check_fail_by"]["optimal L+"] += int(not A["limit_check"][1])
    stats["optimal_L_plus_max"] = max(stats["optimal_L_plus_max"], float(A["L_plus"]))
    stats["turning_points"] += len(A["turns"])
    s2 = c["s2"]
    for label, R2 in (("s2*1e-3", s2 * mp.mpf("1e-3")), ("s2/2", s2 / 2), ("s2", s2), ("s2(1-d)", s2 * (1 - D6)),
                      ("s2(1+d)", s2 * (1 + D6)), ("1.5 s2", 1.5 * s2)):
        out = classify(A, R2)
        want = "lower ray" if R2 < s2 else "Empty"
        record("optimal", [lam, Sig, Pi], label, R2, name(out["class"]), want, out["components"],
               tau_star_R(R2, lam, Sig, Pi) if want == "lower ray" else None)
    for gkind, G in (("random G", G0), ("G = 2F Pi", 2 * F * Pi), ("G = 2F Pi (1-d)", 2 * F * Pi * (1 - D6)),
                     ("G = 2F Pi (1+d)", 2 * F * Pi * (1 + D6))):
        c = crit(lam, Sig, Pi, G)
        A = analyse(*relay_sweep(lam, Sig, Pi, G), lam)
        stats["limit_check_fail"] += int(not all(A["limit_check"]))
        stats["limit_check_fail_by"]["relay L-"] += int(not A["limit_check"][0])
        stats["limit_check_fail_by"]["relay L+"] += int(not A["limit_check"][1])
        stats["turning_points"] += len(A["turns"])
        H, Vw = c["H_G"], c["V_w"]
        tols = [("H/2", H / 2), ("H", H), ("H(1-d)", H * (1 - D6)), ("H(1+d)", H * (1 + D6)), ("(H+Vw)/2", (H + Vw) / 2),
                ("Vw", Vw), ("Vw(1-d)", Vw * (1 - D6)), ("Vw(1+d)", Vw * (1 + D6)), ("1.5 Vw", 1.5 * Vw)]
        for label, R2 in tols:
            out = classify(A, R2)
            want = pred_relay(R2, c, None)
            record("relay", [lam, Sig, Pi, G, gkind], label, R2, name(out["class"]), want, out["components"],
                   tau_R(R2, lam, Sig, Pi, G) if want == "lower ray" else None)
        out = classify(A, F)       # "at the floor"
        want = "lower ray" if G > 2 * F * Pi else "Empty"
        record("relay", [lam, Sig, Pi, G, gkind], "F", F, name(out["class"]), want, out["components"],
               tau_F(lam, Sig, Pi, G) if want == "lower ray" else None)
    if (i + 1) % 200 == 0:
        print(f"  {i + 1}/{N} sets, {time.time() - t0:.0f}s", flush=True)

ok = stats["class_mismatch"] == 0 and stats["endpoint_mismatch"] == 0
print(f"relay classifications {stats['relay']}, optimal {stats['optimal']}; classes {stats['classes']}; "
      f"class mismatches {stats['class_mismatch']}; endpoint mismatches {stats['endpoint_mismatch']} "
      f"(max rel {stats['max_endpoint_rel']:.3g}); turning points found {stats['turning_points']}; "
      f"limit-check failures {stats['limit_check_fail_by']} (largest optimal L+ = P(1e80/lam) = {stats['optimal_L_plus_max']:.3g})")
for b in bad[:10]:
    print("  ", b)
print(f"T9.4: {'PASS' if ok else 'FAIL'}")
save_json({"N": N, "stats": stats, "bad": bad[:100], "pass": ok, "seconds": time.time() - t0}, "t9_4.json")
