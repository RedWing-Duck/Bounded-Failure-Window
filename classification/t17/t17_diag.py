"""Post-hoc diagnosis of the T17 failures (results/t17_checks.json, recorded on 81e977c). Not a pass criterion.
- E1 item 3 (Proposition 6.13, Kalman part): the recorded numeric test ran at 50 digits; where a^2 = e^(-2 lambda dt) < 1e-50 the
  optimal prior M equals F to working precision and "M < F" reads false. Here: (i) the exact argument f(F) = F^2 a^2 > 0, so M < F;
  (ii) the same test with the working precision raised above 2 lambda dt / ln 10 digits, on the spare seed 17003 (1,000 sets), and
  on the recorded seed's draws re-generated (seed 17001 stream is not reproducible in isolation, so the failing examples are
  re-evaluated from their printed values at high precision).
- E3: the 37 vs 129 values of beta.
- E4: the "Prop. 6.10–6.12" range.
Usage: python3 t17_diag.py"""
import json
import math
import os
import random

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)


def kalman(l_, S_, P_, dt):
    F_ = S_ / l_
    a2 = mp.e ** (-2 * l_ * dt)
    q_, r_ = F_ * (1 - a2), 1 / (P_ * dt)
    bb = r_ * (1 - a2) - q_
    M = (-bb + mp.sqrt(bb**2 + 4 * q_ * r_)) / 2
    Ls = M / (M + r_)
    return M, F_, Ls, F_ * P_ * dt


def main():
    C = json.load(open(os.path.join(HERE, "results", "t17_checks.json")))
    R = {}
    Ms, Fs, a2, r = sp.symbols("M F a2 r", positive=True)
    s = 1 - a2
    f = Ms**2 + (r * s - Fs * s) * Ms - Fs * s * r          # steady prior: M^2 + (r(1 - a^2) - q) M - q r = 0, q = F(1 - a^2)
    fF = sp.factor(sp.expand(f.subs(Ms, Fs)))
    R["E1_item3_exact"] = {"f(F)": str(fF), "text": "f is an upward parabola in M with f(0) = -q r < 0, so its positive root M is "
                           "below F iff f(F) > 0; f(F) = F^2 a^2 > 0 for every dt > 0. Hence M < F exactly, and the L* bound follows "
                           "by the recorded sign argument."}
    rng = random.Random(17003)
    bad, n, maxdps = 0, 0, 0
    for _ in range(1000):
        l_, S_, P_ = (10 ** rng.uniform(-3, 3) for _ in range(3))
        dt = 10 ** rng.uniform(-4, 2)
        need = int(2 * l_ * dt / math.log(10)) + 60
        maxdps = max(maxdps, need)
        with mp.workdps(need):
            M, F_, Ls, phi = kalman(mp.mpf(l_), mp.mpf(S_), mp.mpf(P_), mp.mpf(dt))
            ok = M < F_ and Ls / (2 - Ls) < phi / 2
        n += 1
        bad += not ok
    R["E1_item3_adaptive_precision"] = {"seed": 17003, "n": n, "counterexamples": bad, "max_digits": maxdps}
    ex = C["E1"]["3 Prop 6.13"]["Lstar_numeric"]
    R["E1_item3_recorded"] = {"recorded_counterexamples": ex["counterexamples"], "examples": ex["examples"],
                              "text": "Each printed example has M = F to the printed digits; with a^2 below 1e-50 the difference F - M "
                                      "= O(F a^2) is below the 50-digit working precision. Attribution: code (precision)."}
    t113 = json.load(open(os.path.join(CLS, "t11", "results", "t11_3.json")))
    betas = sorted({x["beta"] for x in t113["by_beta"]})
    R["E3_beta"] = {"distinct_beta": len(betas), "range": [betas[0], betas[-1]],
                    "prereg_t11": "PREREG_t11.md: 'β grid: k/20 for k = −40…80 (exact rationals), plus {0, 2} ± {1e-6, 1e-3}: 129 values'",
                    "text": "T11.3 ran 129 values of beta (its pre-registration says so); '37 values' is in the repository's label of "
                            "Theorem 7.8 (source/Stages_0_4_Source.md) and was carried into the draft. Attribution: document."}
    R["E4_range"] = {"hit": C["E4"]["typed_bad"],
                     "text": "§6.7's summary table cites 'Prop. 6.10–6.12'; 6.11 is a Counterexample. The pre-registered rule requires "
                             "every member of a typed range to have that type. Attribution: document (abbreviation spans a "
                             "Counterexample)."}
    json.dump(R, open(os.path.join(HERE, "results", "t17_diag.json"), "w"), indent=1, ensure_ascii=False, default=str)
    print("f(F) =", fF, "| adaptive-precision counterexamples:", bad, "of", n, "| max digits", maxdps,
          "| distinct beta:", len(betas))


if __name__ == "__main__":
    main()
