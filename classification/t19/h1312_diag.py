"""Post-hoc diagnosis of H-13.C2-12 (not a pass criterion; the recorded verdict stands). For every persisting case of the recorded
run: is R^2 exactly L_-? Is the curve monotone increasing with no turning point? What is the relative gap f - R^2 at route (ii)'s
single sample point, evaluated at enough digits to resolve it (dps raised until the gap is resolved, up to 20,000)?"""
import json
import os
import sys

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(CLS, "t13"), os.path.join(CLS, "t10")]
import t13_audit_classes as AC  # noqa: E402
from t10_common import T  # noqa: E402

rec = json.load(open(os.path.join(HERE, "results", "h", "H-13.C2-12.json")))
rng = np.random.default_rng(13100 + 12)
draws = {}
for i in range(1000):
    p = AC.draw(12, rng, i)
    draws[i] = (p, int(rng.integers(2**63)))
# the recorded json keeps the first 10 examples; recompute the full persisting list from the recorded run's per-set data is not stored,
# so re-derive it: every set whose index appears among the examples, and every set re-run here with the same first pass
from t19_routes import _h1312_job  # noqa: E402
rows = []
for i in range(1000):
    p, seed = draws[i]
    r = _h1312_job((12, i, p, seed))
    for c in r["persist"]:
        A = AC.analyse_row(12, p)
        R2 = mp.mpf(c["R2"])
        out = {"i": i, "g": p["g"], "route_i": c["route_i"], "route_ii": c["route_ii"], "n_turns": len(A["turns"]),
               "dirs": [int(d) for d in A["dirs"]]}
        with mp.workdps(60):
            out["R2_rel_to_Lminus"] = float(abs(R2 / A["L_minus"] - 1)) if A["L_minus"] else None
        for d in (400, 2000, 20000):
            with mp.workdps(d):
                gap = A["curve"].f(T(A["curve"].shift)) - mp.mpf(c["R2"])
                if gap != 0 and abs(gap) > mp.mpf(10) ** (-d + 30):
                    out["log10_rel_gap"] = float(mp.log10(abs(gap) / mp.mpf(c["R2"])))
                    out["gap_sign"] = int(mp.sign(gap))
                    out["dps_needed"] = d
                    break
        rows.append(out)
s = {"n_persisting": len(rows), "sets": sorted({r["i"] for r in rows}),
     "all_route_i_All_route_ii_Empty": all(r["route_i"] == "All" and r["route_ii"] == "Empty" for r in rows),
     "all_monotone_increasing_no_tp": all(r["n_turns"] == 0 and r["dirs"] == [1] for r in rows),
     "max_R2_rel_to_Lminus": max((r["R2_rel_to_Lminus"] or 0) for r in rows) if rows else None,
     "log10_rel_gap_range": [min(r.get("log10_rel_gap", 0) for r in rows), max(r.get("log10_rel_gap", 0) for r in rows)] if rows else None,
     "all_gaps_positive": all(r.get("gap_sign") == 1 for r in rows), "g_hist": {}}
for r in rows:
    s["g_hist"][r["g"]] = s["g_hist"].get(r["g"], 0) + 1
json.dump({"summary": s, "rows": rows}, open(os.path.join(HERE, "results", "h", "H-13.C2-12_diag.json"), "w"), indent=1, default=str)
print(json.dumps(s, default=str))
