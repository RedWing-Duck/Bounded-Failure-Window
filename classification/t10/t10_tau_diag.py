"""T10.6 diagnosis (post hoc): the zero-limit criterion P < 1e-6 P_max at lam tau = 1e-12 is unattainable.
Asymptote: A ~ 1/tau as tau -> 0, so P ~ sqrt(4 Sigma v / A) = 2 sqrt(Sigma v tau); at lam tau = 1e-12,
P/P_max ~ 2e-6 (Sigma + lam v)/sqrt(lam Sigma v) >= 4e-6 (equality at Sigma = lam v). Checked on the same 1,000 sets."""
import mpmath as mp
import numpy as np

from t10_common import save_json
from t10_tau import P_rat

rng = np.random.default_rng(10006)
S = 10.0**rng.uniform(-2, 2, size=(1000, 4))
worst, mn = mp.mpf(0), mp.mpf(1)
for i in range(1000):
    lam, Sig, v = (mp.mpf(x) for x in S[i, :3])
    Pmax = Sig * v / (Sig + lam * v)
    for s in (-12, 12):
        r = P_rat(mp.power(10, s) / lam, lam, Sig, v) / Pmax
        pred = 2 * mp.mpf("1e-6") * (Sig + lam * v) / mp.sqrt(lam * Sig * v)
        worst = max(worst, abs(r / pred - 1))
        mn = min(mn, r)
out = {"min_P_over_Pmax": mn, "max_rel_dev_from_asymptote": worst, "lower_bound": 4e-6,
       "conclusion": "criterion error: P/P_max at lam tau = 1e-+12 equals the asymptote 2e-6 (Sigma+lam v)/sqrt(lam Sigma v) >= 4e-6"}
print({k: (mp.nstr(v_, 6) if isinstance(v_, mp.mpf) else v_) for k, v_ in out.items()})
save_json(out, "t10_6_diag.json")
