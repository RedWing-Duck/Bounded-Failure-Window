"""T10.2 diagnosis (post hoc): why A1.3 with the G_+ inverse cannot satisfy G -> G_inf.
G_+ = Pi v + sqrt(Pi^2 v^2 - 2 Pi (Sigma - lambda v)) >= Pi v, and v -> H > 0, so G_+ / Pi -> 2H.
Measured: G_+(Pi)/(2 H Pi) at Pi = 1e6 ... 1e12 for the k = 1 literal construction, and the Bayesian gain itself."""
import mpmath as mp

from t10_common import save_json, sig2

lam, Sig, c = mp.mpf(1), mp.mpf("0.01"), mp.mpf(1)
Pi0 = c * lam / (mp.mpf("1.5") * Sig)
H = Sig / (lam + c)
rows = []
for e in range(6, 13):
    Pi = mp.power(10, e)
    v = sig2(c * Pi / (Pi + Pi0), Pi, lam, Sig)          # bumps at x <= -1 are negligible here (< e^-1000)
    Gp = Pi * v + mp.sqrt(Pi**2 * v**2 - 2 * Pi * (Sig - lam * v))
    Gm = Pi * v - mp.sqrt(Pi**2 * v**2 - 2 * Pi * (Sig - lam * v))
    rows.append({"Pi": Pi, "G_plus": Gp, "G_plus_over_2H_Pi": Gp / (2 * H * Pi), "G_minus": Gm,
                 "G_bayes": c * Pi / (Pi + Pi0)})
    print(f"Pi=1e{e}: G+ = {mp.nstr(Gp, 8)}, G+/(2 H Pi) = {mp.nstr(Gp / (2 * H * Pi), 10)}, G- = {mp.nstr(Gm, 10)}, "
          f"G_Bayes = {mp.nstr(c * Pi / (Pi + Pi0), 10)}")
save_json({"rows": rows, "conclusion": "G_+ grows like 2 H Pi; the lower branch G_- equals the Bayesian gain and converges. "
           "A1.3 needs the branch switch at Pi_c (supplementary construction), not the plan's G_+ alone."}, "t10_2_diag.json")
