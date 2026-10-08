"""Post-hoc diagnoses (Task 12), run after the pre-registered scripts; nothing here changes a verdict.
(1) A7: D1 prior/avg sets where the T10 method found no minimum below F. Uses the scaled derivative
    g(dt) = 2 lam (F - P+) + dP+/ddt, with d prior/ddt = e^{-2 lam dt} g (exact), so a sign change of g locates the prior
    minimum without the e^{-2 lam dt} factor that drives the pre-registered zero tolerance (1e-40 |f|/theta) to miss it;
    for avg the same grid search is run on d avg/ddt at dps raised with lam dt.
(2) A8 qualitative regression: the actual values behind the prompt's quick check.
(3) A4: sets with 2 < rho <= 2 + u (the prompt's conjecture predicts excess onset there; the exact condition does not)."""
import json
import os

import mpmath as mp
import numpy as np
import sympy as sp

from t12_common import RES, SYM, ARGS, analyse_dt, classify, dps_for, dt_funcs, name, save_json, x

a8 = json.load(open(os.path.join(RES, "t12_a8.json")))
R = {}

# ---------------- (1) A7
post = SYM["D1"]["post"]
lam_s, Sig_s = ARGS[1], ARGS[2]
g_expr = 2 * lam_s * (Sig_s / lam_s - post) + sp.diff(post, x)
g_num = sp.lambdify(ARGS, g_expr, "mpmath", cse=True)


def a7_scaled(p):
    lam, Sig, Pi, G = (mp.mpf(p[k]) for k in ("lam", "Sig", "Pi", "G"))
    F = Sig / lam
    xs = [mp.mpf(v) - mp.log10(lam) for v in np.linspace(-8, 8, 801)]
    sg = []
    for xx in xs:
        t = mp.power(10, xx)
        with mp.workdps(dps_for(lam * t) + 20):
            sg.append(mp.sign(g_num(t, lam, Sig, Pi, G, 1, 1, 1)))
    mins = []
    for i in range(len(xs) - 1):
        if sg[i] < 0 < sg[i + 1]:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(120):
                m = (lo + hi) / 2
                with mp.workdps(dps_for(lam * mp.power(10, m)) + 20):
                    v = g_num(mp.power(10, m), lam, Sig, Pi, G, 1, 1, 1)
                lo, hi = (m, hi) if v < 0 else (lo, m)
            t = mp.power(10, (lo + hi) / 2)
            fpost, _ = dt_funcs("D1", "post", p)
            with mp.workdps(dps_for(lam * t) + 20):
                dip = mp.exp(-2 * lam * t) * (F - fpost(t)) / F       # (F - prior)/F at the minimum, exact form
            mins.append({"dt": t, "lam_dt": lam * t, "rel_dip": dip})
    return {"n_min": len(mins), "mins": mins, "sign_changes": sum(1 for i in range(len(sg) - 1) if sg[i] != sg[i + 1])}


rows = []
for s in a8["sets"]:
    if s["fam"] != "D1":
        continue
    p = s["p"]
    F = p["Sig"] / p["lam"]
    if not p["G"] > 2 * F * p["Pi"]:
        continue
    found = any(k == "min" and v < F for k, v in zip(s["prior"]["kinds"], s["prior"]["values"]))
    if not found:
        rows.append({"p": p, **a7_scaled(p)})
R["A7_prior_missed"] = {"n_missed": len(rows), "n_found_by_scaled_derivative": sum(r["n_min"] >= 1 for r in rows),
                        "n_min_hist": {str(k): sum(r["n_min"] == k for r in rows) for k in sorted({r["n_min"] for r in rows})},
                        "lam_dt_range": [min((m["lam_dt"] for r in rows for m in r["mins"]), default=None),
                                         max((m["lam_dt"] for r in rows for m in r["mins"]), default=None)],
                        "log10_rel_dip_range": [min((mp.log10(m["rel_dip"]) for r in rows for m in r["mins"]), default=None),
                                                max((mp.log10(m["rel_dip"]) for r in rows for m in r["mins"]), default=None)],
                        "examples": rows[:5]}
# sets where a minimum below F was found but the class at (min + F)/2 is not two rays: dip vs the classifier's 1e-40
wrong = []
for s in a8["sets"]:
    if s["fam"] != "D1":
        continue
    p = s["p"]
    F = mp.mpf(p["Sig"]) / mp.mpf(p["lam"])
    if not (mp.mpf(p["G"]) > 2 * F * mp.mpf(p["Pi"]) and "min" in s["prior"]["kinds"]):
        continue
    if min(v for k, v in zip(s["prior"]["kinds"], s["prior"]["values"]) if k == "min") > p["Sig"] / p["lam"] * (1 - 1e-12):
        A = analyse_dt("D1", "prior", p)
        m = min(t["value"] for t in A["turns"] if t["kind"] == "min")
        if m < F:
            C = classify(A, (m + F) / 2)
            if C["route_i"] != (1, 1, 0):
                wrong.append({"p": p, "rel_dip": 1 - m / F, "class_i": name(C["route_i"]), "class_ii": name(C["route_ii"])})
R["A7_prior_class_not_two_rays"] = {"n": len(wrong), "cases": wrong,
                                    "all_dips_below_1e-40": all(w["rel_dip"] < mp.mpf("1e-40") for w in wrong)}
avg_missed = []
for s in a8["sets"]:
    if s["fam"] != "D1":
        continue
    p = s["p"]
    F = p["Sig"] / p["lam"]
    if p["G"] > 2 * F * p["Pi"] and not any(k == "min" and v < F for k, v in zip(s["avg"]["kinds"], s["avg"]["values"])):
        avg_missed.append(p)
R["A7_avg_missed"] = {"n_missed": len(avg_missed), "examples": avg_missed[:10]}
print("A7 diag", {k: v for k, v in R["A7_prior_missed"].items() if k != "examples"}, "avg missed", len(avg_missed), flush=True)

# ---------------- (2) A8 qualitative regression: actual values
q = {"lam": 1, "Sig": "0.01", "Pi": 1, "G": "0.5"}
Ap, Aa = analyse_dt("D1", "post", q), analyse_dt("D1", "avg", q)
fp, _ = dt_funcs("D1", "post", q)
R["A8_regression_actual"] = {"post_limit_dt0": Ap["L_minus"], "post_turns": [(t["kind"], t["theta"], t["value"]) for t in Ap["turns"]],
                             "post_at_dt1": fp(mp.mpf(1)), "avg_turns": [(t["kind"], t["theta"], t["value"]) for t in Aa["turns"]],
                             "avg_crossing_of_F": [e[1] for e in classify(Aa, mp.mpf("0.01"))["ends"]],
                             "window_class_at_R2_0.12": name(classify(Ap, mp.mpf("0.12"))["route_i"]),
                             "two_ray_class_at_mid": name(classify(Aa, (Aa["turns"][-1]["value"] + mp.mpf("0.01")) / 2)["route_i"])}
print("A8 regression actual", R["A8_regression_actual"], flush=True)

# ---------------- (3) A4 conjecture: 2 < rho <= 2 + u
d3 = a8["families"]["D3"]["excess"]
d3sets = [s_ for s_ in a8["sets"] if s_["fam"] == "D3"][:d3["n"]]
u_ = lambda p: 2 * p["Sig"] * p["Pi"] / p["lam"]**2
R["A4_conjecture"] = {"n_sets": d3["n"], "n_rho_gt_2": sum(s_["p"]["rho"] > 2 for s_ in d3sets),
                      "n_2_lt_rho_le_2_plus_u": sum(2 < s_["p"]["rho"] <= 2 + u_(s_["p"]) for s_ in d3sets), "n_rho_gt_2_no_onset": d3["n_rho_gt_2_no_onset"],
                      "n_onset_pred_(rho>2+u)": d3["n_onset_pred"], "n_onset_obs": d3["n_onset_obs"]}
print("A4", R["A4_conjecture"])
save_json(R, "t12_diag.json")
