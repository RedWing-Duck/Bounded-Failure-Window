"""T11.3 diagnosis (post hoc, not a pass criterion): the class failures at beta = 2 and just above 2.

Cause (derived after the smoke run, before the full run; the pre-registration was not changed):
- beta = 2: 4AC/B^2 -> 2 Sigma/K (not 0) as tau -> oo, so L+ = 2F/(1 + sqrt(1 + 2 Sigma/K)) = sigma*^2(lam^2/K)
  (the dual of beta = 0 by Prop. 4.6b), not F as the PREREG table says.
- beta > 2: L+ = F is correct, but P approaches it like tau^(2 - beta) (4AC/B^2 = 2 Sigma tau^(2-beta)/K), so the
  pre-registered outer bracket x = 80 is too short when beta - 2 is small.
Re-run of every pre-registered set at the failing betas with the corrected limit / bracket
(x_end = max(80, 50/(beta - 2)) - log10 lam): both routes must agree and give upper ray or Empty."""
import mpmath as mp
import numpy as np

from t11_common import P_pow, analyse_with_limits, classify, limits_pow, name, power_curve, save_json, sstar
from t11_power import BETAS, NSET

rng = np.random.default_rng(11003)
sets = {}
for bi in range(len(BETAS)):
    for _ in range(NSET):
        p = {k: float(10.0**rng.uniform(-2, 2)) for k in ("lam", "Sig", "K")}
        sets.setdefault(bi, []).append((p, int(rng.integers(2**63))))
targets = [bi for bi, b in enumerate(BETAS) if 2 <= b < mp.mpf("2.6")]


def job(args):
    bi, p, seed = args
    beta = BETAS[bi]
    K, lam, Sig = (mp.mpf(p[k]) for k in ("K", "lam", "Sig"))
    Lm, Lp, xm, xp = limits_pow(beta, K, lam, Sig)
    chk = None
    if beta == 2:
        Lp = sstar(lam, Sig, lam**2 / K)
        chk = {"P_at_1e80": P_pow(mp.power(10, 80) / lam, beta, K, lam, Sig), "sigma_star_lam2_over_K": Lp}
    else:
        xp = max(mp.mpf(80), 50 / (beta - 2)) - mp.log10(lam)
    A = analyse_with_limits(power_curve(beta, K, lam, Sig), Lm, Lp, xm, xp)
    r_ = np.random.default_rng(seed)
    Pref = Lp
    tols = [Pref * mp.power(10, mp.mpf(float(x))) for x in r_.uniform(-3, float(mp.log10(2)), 7)]
    tols += [Pref * (1 - mp.mpf("1e-6")), Pref, Pref * (1 + mp.mpf("1e-6"))]
    res = []
    for R2 in tols:
        r = classify(A, R2)
        res.append((r["route_i"] == r["route_ii"] and r["route_i"] in {(0, 1, 0), (0, 0, 0)}, name(r["route_i"])))
    return bi, res, chk


if __name__ == "__main__":
    from multiprocessing import Pool
    jobs = [(bi, p, seed) for bi in targets for p, seed in sets[bi]]
    with Pool(4) as pool:
        allres = pool.map(job, jobs, chunksize=10)
    out = {"by_beta": [], "beta2_limit_check": [c for _, _, c in allres if c is not None][:20]}
    for bi in targets:
        rr = [x for b_, res, _ in allres if b_ == bi for x in res]
        counts = {}
        for ok, nm in rr:
            counts[nm] = counts.get(nm, 0) + 1
        bad = sum(not ok for ok, _ in rr)
        out["by_beta"].append({"beta": BETAS[bi], "classifications": len(rr), "failures": bad, "classes": counts})
        print(f"beta = {mp.nstr(BETAS[bi], 8)}: corrected classifications {len(rr)}, failures {bad}, classes {counts}", flush=True)
    for x in out["beta2_limit_check"][:3]:
        print("beta = 2: P(1e80/lam) =", mp.nstr(x["P_at_1e80"], 15), " sigma*^2(lam^2/K) =", mp.nstr(x["sigma_star_lam2_over_K"], 15))
    save_json(out, "t11_3_diag.json")
