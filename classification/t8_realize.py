"""T8.5: Proposition 1.1 realizability with piecewise-linear zigzags in s = theta/(1+theta)."""
import numpy as np

from t8_common import analyse, classify, name, save_json


def zigzag(nodes):
    """Piecewise linear in s = theta/(1+theta) through equally spaced nodes on s in [0, 1]."""
    sk = np.linspace(0.0, 1.0, len(nodes))
    v = np.asarray(nodes, float)
    slopes = np.diff(v) / np.diff(sk)

    def s_of(th):
        th = np.asarray(th, float)
        return np.where(np.isinf(th), 1.0, th / (1.0 + th))

    def f(th):
        return np.interp(s_of(th), sk, v)

    def df(th):
        th = np.asarray(th, float)
        s = s_of(th)
        j = np.clip(np.searchsorted(sk, s, side="right") - 1, 0, len(slopes) - 1)
        with np.errstate(all="ignore"):
            ds = 1.0 / (1.0 + th)**2
        return slopes[j] * ds
    return f, df


rows = []
for ell in (0, 1):
    for u in (0, 1):
        for k in range(5):
            nodes = ([2.0] if ell else []) + [0.0] + [2.0, 0.0] * k + ([2.0] if u else [])
            if len(nodes) == 1:
                nodes = [0.0, 0.5]
            A = analyse(*zigzag(nodes))
            got = classify(A, 1.0)["class"]
            want = (ell, u, k)
            rows.append({"intended": want, "nodes": nodes, "got": got, "name": name(got), "match": got == want,
                         "turning_points": len(A["turns"])})
A = analyse(*zigzag([3.0, 2.0, 3.0]))
got = classify(A, 1.0)["class"]
rows.append({"intended": "All", "nodes": [3.0, 2.0, 3.0], "got": got, "name": name(got), "match": got == "All",
             "turning_points": len(A["turns"])})
for r in rows:
    print(f"  intended {str(r['intended']):<10} nodes {r['nodes']}: got {str(r['got']):<10} ({r['name']}) "
          f"{'ok' if r['match'] else 'MISMATCH'}")
ok = all(r["match"] for r in rows)
print(f"T8.5: {'PASS' if ok else 'FAIL'} ({sum(r['match'] for r in rows)}/{len(rows)})")
save_json({"rows": rows, "pass": ok}, "t8_5.json")
