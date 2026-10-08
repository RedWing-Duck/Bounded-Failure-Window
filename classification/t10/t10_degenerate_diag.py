"""T10.5 diagnosis (post hoc): pair-birth scaling. Near a fold of the turning points, N(x; Pi0) ~ a (x - x0)^2 - b delta,
so the two turning points sit at x0 +- sqrt(b delta/a) (separation ~ delta^{1/2}) and the value gap is the integral of
d sigma2/dx between them, ~ delta^{3/2}. Fits both exponents on finer deltas and reports (M - m)/(x sep)^3, which is
constant at a fold."""
import mpmath as mp
import numpy as np

from t10_census import hill_count, pair_birth
from t10_common import save_json

P0p = pair_birth(2)["transitions"][0]
P0p = P0p["Pi0_double_root"] or P0p["Pi0_bisect"]
rows = []
for e in range(4, 15):
    d = mp.power(10, -e)
    ts = hill_count(2, P0p * (1 - d))["turns"]
    if len(ts) == 2:
        dv, dx = ts[1]["value"] - ts[0]["value"], ts[1]["x"] - ts[0]["x"]
        rows.append({"delta": d, "M_minus_m": dv, "x_sep": dx, "ratio_dv_over_dx3": dv / dx**3})
ld = np.log10([float(r["delta"]) for r in rows])
sv = float(np.polyfit(ld, np.log10([float(r["M_minus_m"]) for r in rows]), 1)[0])
sx = float(np.polyfit(ld, np.log10([float(r["x_sep"]) for r in rows]), 1)[0])
for r in rows:
    print(f"delta={mp.nstr(r['delta'], 2)}: M-m={mp.nstr(r['M_minus_m'], 6)}, x sep={mp.nstr(r['x_sep'], 6)}, "
          f"(M-m)/sep^3={mp.nstr(r['ratio_dv_over_dx3'], 8)}")
print(f"slopes: M - m {sv:.5f} (fold theory 1.5), x separation {sx:.5f} (theory 0.5)")
save_json({"rows": rows, "slope_M_minus_m": sv, "slope_x_sep": sx,
           "conclusion": "criterion error: the value gap scales as delta^{3/2} at a fold; positions separate as delta^{1/2}"},
          "t10_5_diag.json")
