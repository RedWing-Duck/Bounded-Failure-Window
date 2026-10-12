"""Part E: compare the scan's sign-change counts with the parity predicted by the endpoint asymptotics (e3): post and prior odd iff
g > nu (G > 2 F Pi); avg odd iff g^2 + 4g > 4 nu. Re-runs the scan's counter at each grid point (same code)."""
import json
import numpy as np
from multiprocessing import Pool
import e2_scan as S


def job(a):
    gi, ni, res = S.count(a)
    g, nu = 10.0**gi, 10.0**ni
    pred = {"post": g > nu, "prior": g > nu, "avg": g * g + 4 * g > 4 * nu}
    return gi, ni, res, {k: (res[k] % 2 == 1) == pred[k] for k in res}


if __name__ == "__main__":
    grid = [(gi, ni) for gi in np.linspace(-4, 4, 41) for ni in np.linspace(-4, 4, 41)]
    with Pool(2) as p:
        rr = p.map(job, grid, chunksize=8)
    bad = [(gi, ni, res) for gi, ni, res, ok in rr if not all(ok.values())]
    two = [(gi, ni, res) for gi, ni, res, ok in rr if max(res.values()) == 2]
    out = {"points": len(rr), "parity_mismatches": bad, "points_with_two": two[:60], "n_two": len(two)}
    json.dump(out, open("e4_parity.json", "w"), indent=1)
    print(len(rr), "points; parity mismatches", len(bad), "; points with 2 turning points", len(two), bad[:5])
