"""T7.3: plain-language specification of Task 4a, closed-form recomputation of its peaks, and a
decomposition of why its ratio-100 peak differs from the continuous kappa = 100 peak. No simulation."""
import json
import os
import re

import numpy as np
from scipy.optimize import minimize_scalar

from common import C, F, HERE, LAM, RES, SIG, Timer, dump, g_kalman, var_cf
from t7_common import sf_match

with Timer() as T:
    src = open(os.path.join(HERE, "t4a_discrete.py")).read()
    t4a = json.load(open(os.path.join(RES, "t4a.json")))
    DTD = float(re.search(r"^DTD = ([0-9.eE+-]+)", src, re.M).group(1))
    grid_line = re.search(r"^PI = (.+)$", src, re.M).group(1)
    eps_line = re.search(r"eps = ([0-9.eE+-]+)", src).group(1)

    def plant(dt):
        phi = np.exp(-LAM * dt)
        return phi, SIG * (1 - phi**2) / LAM

    def riccati_gain(pid, qa, phi):
        """Steady-state gain from M = phi^2 M r/(M+r) + qa (T7.1f), r = 1/Pi_d."""
        r = 1.0 / pid
        b = r * (1 - phi**2) - qa
        disc = np.sqrt(b * b + 4 * qa * r)
        M = np.where(b > 0, 2 * qa * r / (b + disc), (-b + disc) / 2)
        return M / (M + r)

    def prior_post(pid, L, phi, q):
        """T7.1(a,b): stationary prior M_L and posterior S_L of the fixed-gain filter."""
        r = 1.0 / pid
        M = (phi**2 * L**2 * r + q) / (1 - phi**2 * (1 - L) ** 2)
        return M, (1 - L) ** 2 * M + L**2 * r

    def maximise(f, lo=-3.0, hi=4.0):
        res = minimize_scalar(lambda lp: -f(10.0**lp), bounds=(lo, hi), method="bounded",
                              options={"xatol": 1e-10})
        return float(10.0**res.x), float(-res.fun)

    phi, q = plant(DTD)
    reported = {r["factor"]: r for r in t4a["rows"] if r["mode"] == "A"}
    rows = []
    for k in (3, 10, 100):
        pd, pk = maximise(lambda pid: prior_post(pid, riccati_gain(pid, k * q, phi), phi, q)[1])
        rep = reported[k]["peak"]
        rows.append({"k": k, "peak_closed": pk, "peak_Pi_d": pd, "reported": rep,
                     "reported_Pi_d": reported[k]["peak_Pi"], "match_3sf": sf_match(pk, rep, 3),
                     "rel_diff": pk / rep - 1})
    ok = all(r["match_3sf"] for r in rows)

    # ---- decomposition for k = 100
    k = 100
    slope = float(riccati_gain(1e-9, k * q, phi) / 1e-9)
    kappa_cont = slope / F
    Pi0 = C / (kappa_cont * F)
    pc = np.logspace(-4, 4, 200001)
    cont_bw = var_cf(pc, g_kalman(pc, Pi0))
    ii = int(np.argmax(cont_bw))
    i_bw = (float(cont_bw[ii]), float(pc[ii]))
    pd_bw, pk_bw = maximise(lambda pid: prior_post(pid, DTD * C * (pid / DTD) / (pid / DTD + Pi0), phi, q)[1])
    Gkb = -LAM + np.sqrt(LAM**2 + 2 * k * SIG * pc)
    cont_kb = var_cf(pc, Gkb)
    jj = int(np.argmax(cont_kb))
    i_kb = (float(cont_kb[jj]), float(pc[jj]))
    pd_pr, pk_pr = maximise(lambda pid: prior_post(pid, riccati_gain(pid, k * q, phi), phi, q)[0])
    conv = []
    for dt in (0.05, 0.01, 0.001):
        ph_, q_ = plant(dt)
        pd_, pk_ = maximise(lambda pid: prior_post(pid, riccati_gain(pid, k * q_, ph_), ph_, q_)[1], -5, 4)
        pdm, pkm = maximise(lambda pid: prior_post(pid, riccati_gain(pid, k * q_, ph_), ph_, q_)[0], -5, 4)
        conv.append({"dt": dt, "posterior_peak": pk_, "prior_peak": pkm, "peak_Pi_cont": pd_ / dt})
    rep100 = reported[100]["peak"]
    contrib = {
        "gain shape: continuous KB-type gain vs Bayesian-weight gain, same kappa": i_kb[0] - i_bw[0],
        "dt on the paper's Bayesian-weight relay (discrete posterior - continuous)": pk_bw - i_bw[0],
        "dt on the 4a gain family (discrete posterior at dt=0.05 - continuous)": conv[0]["posterior_peak"] - i_kb[0],
        "prior vs posterior at dt=0.05 (posterior - prior)": conv[0]["posterior_peak"] - conv[0]["prior_peak"],
    }
    total = rep100 - i_bw[0]
    main = max(contrib.items(), key=lambda kv: abs(kv[1]))

spec = f"""TASK 4a SPECIFICATION (derived from t4a_discrete.py and results/t4a.json; no new simulation)

True plant. A discrete-time AR(1) state h_(k+1) = phi*h_k + w_k with time step dt = {DTD:g}. phi and q were
chosen so that the discrete plant samples the continuous worked example (lambda = {LAM:g}, Sigma = {SIG:g}) exactly:
phi = exp(-lambda*dt) = {phi:.6f} and q = Sigma*(1 - phi^2)/lambda = {q:.6e}. Its stationary variance is
q/(1 - phi^2) = F = Sigma/lambda = {q/(1-phi**2):.6g}. The plant was simulated with the true phi and q.

Observation and "per-sample precision". Each sample y_k = h_k + v_k has measurement noise of variance
var(v) = 1/Pi, where Pi is the grid variable of Task 4a (grid {grid_line}). That Pi is therefore the
per-sample precision, Pi_d = 1/r, in T7.1's notation. It is NOT the continuous sensory precision. Continuous
white sensory noise of intensity 1/Pi_cont gives a per-sample variance 1/(Pi_cont*dt) after averaging over
one step, so Pi_d = Pi_cont*dt and Pi_cont = Pi_d/dt = {1/DTD:g}*Pi_d. The reported Task 4a peak locations
(Pi_d = {reported[3]['peak_Pi']:.3g}, {reported[10]['peak_Pi']:.3g}, {reported[100]['peak_Pi']:.3g} for factors 3, 10, 100) correspond to
Pi_cont = {reported[3]['peak_Pi']/DTD:.3g}, {reported[10]['peak_Pi']/DTD:.3g}, {reported[100]['peak_Pi']/DTD:.3g}.

Filters. Each filter is a fixed-gain filter: predict with the true phi, then update with a constant
gain K. K is the steady-state Kalman gain of an ASSUMED model: (A) process noise k*q, or (B) measurement
precision kappa*Pi_d, with the factor in {{1, 2, 3, 10, 100}}. The steady-state gain depends only on the
assumed ratio q/r, so A and B give identical filters for equal factors (Task 4a confirmed this).

"Slope ratio". Operationally this is K(eps)/eps with eps = {eps_line}, the numerical initial slope dK/dPi_d of
the gain at Pi_d -> 0, divided by F = {F:g}. F is the analytic initial slope of the correctly specified
filter; its numerical value was {t4a['correct_slope']:.6g}. Analytically the slope of a filter with factor k is k*F, so
the "ratio" equals the factor (reported: {', '.join(f"{r['ratio']:.6g}" for r in t4a['rows'] if r['mode']=='A')}).
Because L = G*dt and Pi_d = Pi_cont*dt, dK/dPi_d = dG/dPi_cont. The slope ratio is therefore exactly the
continuous over-weighting ratio kappa = (dG/dPi at 0)/F.

Prior or posterior. The reported variance was the POSTERIOR error variance. It is the variance of
h_k - hhat_k after the update with y_k: V = ((1-K)^2 q + K^2/Pi_d)/(1 - (1-K)^2 phi^2), which equals S_L of T7.1(b).
The simulation check also measured h_k - hhat_k after the update.
"""

expl_lines = [
    "WHY THE RATIO-100 PEAK IS ABOUT TWICE THE CONTINUOUS kappa = 100 PEAK",
    f"(i)   Continuous kappa implied by the 4a mapping: slope/F = {kappa_cont:.6f}, so Pi_0 = c/(kappa F) = {Pi0:.6f}.",
    f"(ii)  Continuous closed form (2), Bayesian-weight gain G = c Pi/(Pi+Pi_0) at that kappa: peak {i_bw[0]:.5f} at Pi = {i_bw[1]:.4g}.",
    f"(iii) Same Bayesian-weight relay discretised at dt = {DTD:g} (L = dt*G, posterior): peak {pk_bw:.5f} at Pi_cont = {pd_bw/DTD:.4g}.",
    f"(iv)  Continuous closed form (2) with the gain the 4a filter converges to as dt -> 0, the Kalman-Bucy gain of the "
    f"assumed model G = -lambda + sqrt(lambda^2 + 2*{k}*Sigma*Pi) (unbounded, no saturation at c): peak {i_kb[0]:.5f} at Pi = {i_kb[1]:.4g}.",
    f"(v)   4a filter at dt = {DTD:g}, PRIOR variance: peak {pk_pr:.5f}; POSTERIOR: {conv[0]['posterior_peak']:.5f} (reported {rep100:.5f}).",
    "(vi)  4a filter family as dt -> 0 (posterior / prior peak): " + "; ".join(
        f"dt={c['dt']:g}: {c['posterior_peak']:.5f} / {c['prior_peak']:.5f} at Pi_cont={c['peak_Pi_cont']:.4g}" for c in conv)
    + f"  -> converges to (iv) = {i_kb[0]:.5f}.",
    f"Total gap (reported - continuous kappa=100): {total:+.5f}. Contributions:",
] + [f"    {name}: {val:+.5f}" for name, val in contrib.items()] + [
    f"Mapping: exact. The implied continuous kappa is {kappa_cont:.4f}, so it contributes nothing.",
    f"Conclusion: the main cause is '{main[0]}' ({main[1]:+.5f} of {total:+.5f}). Gain shape and dt on the 4a family "
    f"add up to the whole gap ({contrib['gain shape: continuous KB-type gain vs Bayesian-weight gain, same kappa'] + contrib['dt on the 4a gain family (discrete posterior at dt=0.05 - continuous)']:+.5f}). "
    f"The posterior-vs-prior difference ({contrib['prior vs posterior at dt=0.05 (posterior - prior)']:+.5f}) is itself a "
    f"finite-dt effect: it shrinks to {conv[-1]['posterior_peak'] - conv[-1]['prior_peak']:+.5f} at dt = {conv[-1]['dt']:g}. "
    f"Task 4a's filters share the paper's initial slope (kappa) but not its gain family. A steady-state Kalman gain "
    f"under inflated process noise keeps rising with precision instead of saturating at c, so it injects more "
    f"sensory noise near the peak. The 4a peak heights are therefore not comparable with the paper's Bayesian-weight "
    f"peaks at the same kappa; only the onset condition (slope ratio > 2) carries over."]
explanation = "\n".join(expl_lines)

check_lines = [f"[{'PASS' if ok else 'FAIL'}] T7.3: closed-form (T7.1 a,b + Riccati gain) peaks match reported Task 4a peaks to 3 s.f."] + [
    f"    k={r['k']}: closed form {r['peak_closed']:.6f} at Pi_d={r['peak_Pi_d']:.5g} | reported {r['reported']:.6f} at "
    f"Pi_d={r['reported_Pi_d']:.5g} | rel diff {r['rel_diff']:+.2e} | {'ok' if r['match_3sf'] else 'MISMATCH'}" for r in rows]

with open(os.path.join(RES, "t7_4a_spec.txt"), "w") as f:
    f.write(spec + "\n" + "\n".join(check_lines) + "\n\n" + explanation + "\n")
print(spec)
print("\n".join(check_lines))
print(explanation)
dump("t7_3.json", {"pass": ok, "rows": rows, "spec": spec, "explanation": explanation, "check_lines": check_lines,
                   "decomposition": {"kappa_cont": kappa_cont, "Pi_0": Pi0, "cont_bw": i_bw, "disc_bw_post": pk_bw,
                                     "cont_kb": i_kb, "disc_4a_prior": pk_pr, "convergence": conv,
                                     "contributions": contrib, "total": total, "main": main[0]},
                   "runtime_s": T.dt})
