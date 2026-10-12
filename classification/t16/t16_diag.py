"""Post-hoc diagnosis of the T16 failures (results/t16_checks.json, recorded on bc0a72c). Not a pass criterion.
- D1 item 2(b): the recorded check asked SymPy's assumption system whether -lambda + sqrt(lambda^2 + 2 Sigma Pi) is positive; it
  returned None (undecided). Here: the radicand minus lambda^2 is 2 Sigma Pi > 0, and 1,000 random sets (seed 16003, the spare).
- D1 item 9: the residual contains sqrt(R2^2 + 4 d (R2 + d)), a square that the three pre-registered routes did not denest.
- D6: the three hits with their contexts.
- Coverage note for D7: escaped citations \\[n\\] in the thesis renders, which T15's bracket pattern (kept by D7) does not see.
Usage: python3 t16_diag.py"""
import json
import os
import random
import re
import sys

import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
sys.path[:0] = [HERE, os.path.join(CLS, "t15")]
mp.mp.dps = 50


def main():
    C = json.load(open(os.path.join(HERE, "results", "t16_checks.json")))
    R = {}
    lam, Sig, Pi, R2, d = sp.symbols("lambda Sigma Pi R2 d", positive=True)
    root = -lam + sp.sqrt(lam**2 + 2 * Sig * Pi)
    gap = sp.expand((lam**2 + 2 * Sig * Pi) - lam**2)
    rng = random.Random(16003)
    bad = 0
    for _ in range(1000):
        l_, S_, P_ = (mp.mpf(10) ** mp.mpf(rng.uniform(-3, 3)) for _ in range(3))
        if not -l_ + mp.sqrt(l_**2 + 2 * S_ * P_) > 0:
            bad += 1
    R["D1_item2b"] = {"recorded": C["D1"]["2 Prop 3.5 / Lemma 3.6"]["b_only_positive_zero"],
                      "sympy_is_positive_of_root": str(root.is_positive), "radicand_minus_lambda2": str(gap),
                      "radicand_minus_lambda2_positive": bool(gap.is_positive), "numeric_n": 1000, "numeric_counterexamples": bad,
                      "other_root_negative": bool((-lam - sp.sqrt(lam**2 + 2 * Sig * Pi)).is_negative),
                      "text": "The positive zero of G^2 + 2 lambda G - 2 Sigma Pi is G* = -lambda + sqrt(lambda^2 + 2 Sigma Pi): "
                              "sqrt(lambda^2 + 2 Sigma Pi) > lambda because 2 Sigma Pi > 0, and the other root is negative. The "
                              "recorded failure is the code's reliance on SymPy's assumption system, which returns None for this "
                              "expression. Attribution: code. The claim holds."}
    rad = R2**2 + 4 * d * (R2 + d)
    fac = sp.factor(rad)
    piR = 2 * lam * (Sig / lam - R2) / R2**2
    sstar = 2 * Sig / (lam + sp.sqrt(lam**2 + 2 * Sig * piR))
    e = sstar.subs(Sig, lam * (R2 + d))
    sq = next(x for x in e.atoms(sp.Pow) if x.exp == sp.S.Half)
    den = lam * (R2 + 2 * d) / R2                       # candidate denested root, positive
    sq_check = sp.simplify(den**2 - sq.base)             # 0 iff den^2 equals the radicand
    e2 = sp.simplify(e.subs(sq, den) - R2)
    sqrts = [str(x) for x in e.atoms(sp.Pow) if x.exp == sp.S.Half]
    e3 = sp.simplify(sp.factor(sp.expand(e.subs(Sig, lam * (R2 + d))), deep=True))
    e4 = sp.simplify(sp.powdenest(sp.factor_terms(e), force=True))
    R["D1_item9"] = {"recorded_residual": C["D1"]["9 Cor 5.2"]["sstar_at_piR"]["residual"],
                     "recorded_numeric_max_abs": C["D1"]["9 Cor 5.2"]["sstar_at_piR"]["numeric_max_abs"],
                     "radicand_factored": str(fac), "sqrt_of_factored": str(sp.sqrt(fac)),
                     "sqrt_terms": sqrts, "denested_root": str(den), "denested_root_squared_minus_radicand": str(sq_check),
                     "residual_after_sqrt_substitution": str(e2), "other_routes": [str(e3)[:200], str(e4)[:200]],
                     "text": "The radicand R2^2 + 4 d (R2 + d) is (R2 + 2d)^2, so its square root is R2 + 2d (all positive) and "
                             "the recorded residual R2 (R2 + 2d - sqrt(...))/(R2 + sqrt(...)) is 0. The three pre-registered "
                             "routes do not denest the square root of a square (the Task 10 and Task 13 route failures had the "
                             "same cause). Attribution: code (route). The identity holds."}
    hits = C["D6"]["bare_legacy_labels"]
    R["D6"] = {"hits": hits, "paper1": C["D6"]["paper1"],
               "text": "Three items, none a legacy label: (1) 'Paper 1' inside the T15 C10 failure line of Appendix D "
                       "(\"0 'Paper 1', no legacy label remains\"), a quotation of the checked phrase written after the T15 run; "
                       "(2) 'B.4' in the Appendix E render-chain comment added in Task 16 ('... result 5.6 wording, B.4 Pi_c'); "
                       "(3) 'B.2' in Appendix E's 'figures B.1, B.3-B.12 (text-only edits) and B.2', where 'figures' lies more "
                       "than 40 characters before the label. (2) and (3) are figure labels outside the exemption window; "
                       "(1) is the phrase quoted. Attribution: criterion (the exemption rule's 40-character window and its "
                       "treatment of quotations) and document (wording of two appendix lines). Bare legacy labels in the "
                       "thesis renders: 0; false hits on 'Figure B.n': 0."}
    import t15_checks  # noqa: E402
    esc = {}
    for p in t15_checks.THESIS_RENDERS:
        t = open(p).read()
        n = len(re.findall(r"\\\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\\\]", t))
        if n:
            esc[os.path.relpath(p, os.path.dirname(CLS))] = n
    R["D7_coverage"] = {"escaped_citation_groups": esc,
                        "text": "T15's bracket pattern, kept by D7, skips groups written \\[n\\] (a preceding backslash). These are "
                                "real citations in the thesis renders; neither T15 C4 nor D7 tests them. Not a failure of D7 as "
                                "pre-registered; reported for the author."}
    V = sp.symbols("nu q", positive=True)
    nu, q = V
    Vf = (1 + nu * q**2 / 4) / (1 + nu * q / 2)
    R["excess_identity_normal_form"] = {"residual": str(sp.simplify(Vf - 1 - nu * q * (q - 2) / (4 + 2 * nu * q))),
                                        "text": "Draft §3.3: V - 1 = nu q (q - 2)/(4 + 2 nu q) (post hoc; not in D1's list)."}
    json.dump(R, open(os.path.join(HERE, "results", "t16_diag.json"), "w"), indent=1, ensure_ascii=False, default=str)
    for k, v in R.items():
        print(k, ":", v.get("text", "")[:160])
    print("item 9 after substitution:", R["D1_item9"]["residual_after_sqrt_substitution"], R["D1_item9"]["sqrt_terms"], "| radicand:", fac,
          "| item 2b numeric counterexamples:", bad, "| escaped groups:", sum(esc.values()), "| excess residual:",
          R["excess_identity_normal_form"]["residual"])


if __name__ == "__main__":
    main()
