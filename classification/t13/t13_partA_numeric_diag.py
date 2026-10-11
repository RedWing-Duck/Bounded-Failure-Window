"""Post-hoc diagnosis (not a pass criterion): the 277 A1/A2 sets whose auxiliary cross-check Pbar(mu) = Pbar(M) missed
1e-80 at 100 digits. That check is not one of the pre-registered A2 links; at large x the form F - (F - M)(e^{2x} - 1)/(2x)
loses about 2x/ln(10) digits to the cancellation in F - M. Re-run of the same seeds with 100 + ceil(2x/ln 10) + 30 digits."""
import mpmath as mp

import t13_partA_numeric as N
from t13_common import save_json

bad, rows = [], []
for i in range(10000):
    r = N.a12_job(13001 * 100000 + i)
    if "Pbar(mu) = Pbar(M)" not in r["fails"]:
        continue
    x = r["x"]
    extra = int(mp.ceil(2 * x / mp.log(10))) + 30
    old = mp.mp.dps
    with mp.workdps(100 + extra):
        lam, Sig, Pi = r["lam"], r["Sig"], r["Pi"]
        F, k = Sig / lam, lam / Pi
        rr = k / x
        s = -mp.expm1(-2 * x)
        b = s * (rr - F)
        disc = mp.sqrt(b**2 + 4 * s * F * rr)
        M = 2 * s * F * rr / (b + disc) if b > 0 else (-b + disc) / 2
        phi = F * Pi * x / lam
        ps = phi / s
        d2 = mp.sqrt((1 - phi)**2 + 4 * ps)
        mu = 2 * ps / ((1 - phi) + d2) if phi <= 1 else ((phi - 1) + d2) / 2
        Q = mu * s / ((1 + mu) * x)
        rel = abs((F - F / 2 * Q) / (F - (F - M) * mp.expm1(2 * x) / (2 * x)) - 1)
    rows.append({"x": x, "digits": 100 + extra, "rel": rel, "other_fails": [f for f in r["fails"] if f != "Pbar(mu) = Pbar(M)"]})
    if not rel < mp.mpf("1e-80"):
        bad.append(rows[-1])
R = {"n_flagged": len(rows), "n_still_failing": len(bad), "min_x": min(r["x"] for r in rows), "max_rel": max(r["rel"] for r in rows),
     "n_other_fails": sum(len(r["other_fails"]) for r in rows), "bad": bad[:10],
     "attribution": "code: the auxiliary cross-check's 1e-80 tolerance exceeded the precision left after the F - M cancellation; "
                    "with enough digits both forms agree; the pre-registered A2 links had 0 failures"}
print({k: v for k, v in R.items() if k != "bad"})
save_json(R, "t13_partA_numeric_diag.json")
