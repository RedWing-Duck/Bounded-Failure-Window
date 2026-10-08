"""T8.3: Propositions 4.2 and 5.2 checked row by row with the root-finding classifier."""
import numpy as np

from t8_common import C, LAM, SIG, analyse, classify, coupling_sweep, g_star, name, prior_sweep, save_json, sigma2

F = SIG / LAM
D = 1e-6
R = {"cases": {}}


def run_case(label, A, tests, extra=None):
    rows = []
    for desc, r2, want in tests:
        out = classify(A, r2)
        got = name(out["class"])
        rows.append({"test": desc, "R2": r2, "expected": want, "got": got, "match": got == want,
                     "components_theta": [(10.0**a, 10.0**b) for a, b in out["components"]]})
    ok = all(r["match"] for r in rows)
    if extra:
        ok = ok and all(e["pass"] for e in extra)
    R["cases"][label] = {"rows": rows, "extra": extra or [], "pass": ok,
                         "turns": [(t["theta"], t["value"], t["kind"]) for t in A["turns"]],
                         "L_minus": A["L_minus"], "L_plus": A["L_plus"],
                         "approach": [A["approach_minus"], A["approach_plus"]]}
    print(f"{label}: turning points {R['cases'][label]['turns']}, limits {A['L_minus']:.6g} ({A['approach_minus']}) "
          f"-> {A['L_plus']:.6g} ({A['approach_plus']})")
    for r in rows:
        print(f"   {r['test']:<26} R2 = {r['R2']:.10g}: {r['got']:<10} (expected {r['expected']}) "
              f"{'ok' if r['match'] else 'MISMATCH'}")
    for e in extra or []:
        print(f"   [{'ok' if e['pass'] else 'MISMATCH'}] {e['desc']}")
    return ok


def crit(label, v, eq, below, above):
    return [(f"{label} exact", v, eq), (f"{label} x(1-1e-6)", v * (1 - D), below),
            (f"{label} x(1+1e-6)", v * (1 + D), above)]


def comp_join(A, r2, where):
    """At R2 = sigma*^2 the two rays meet at the minimiser."""
    cs = classify(A, r2)["components"]
    if len(cs) != 2:
        return {"desc": f"two rays meet at {where:.8g}", "pass": False}
    a, b = 10.0**cs[0][1], 10.0**cs[1][0]
    ok = abs(a - where) <= 1e-6 * where and abs(b - where) <= 1e-6 * where
    return {"desc": f"at R2 = sigma*^2 the rays meet at {a:.10g} / {b:.10g} (expected {where:.10g})", "pass": ok}


# ---- Proposition 4.2
for Pi, case in ((500.0, "P1"), (60.0, "P2"), (1.0, "P3"), (50.0, "boundary Pi_B"), (150.0, "boundary Pi_A")):
    f, df = prior_sweep(Pi, C)
    A = analyse(f, df)
    Gs = g_star(Pi)
    s2 = Gs / Pi
    Vc = sigma2(C, Pi)
    P0s = Pi * (C / Gs - 1) if C > Gs else None
    extra = []
    if case in ("P1", "boundary Pi_A"):
        tests = ([("row R2 <= V_c (interior)", Vc / 2, "All"), ("row V_c<R2<F (interior)", (Vc + F) / 2, "upper ray"),
                  ("row R2 >= F (interior)", 1.5 * F, "Empty")]
                 + crit("V_c", Vc, "All", "All", "upper ray") + crit("F", F, "Empty", "upper ray", "Empty"))
        if case == "boundary Pi_A":
            extra.append({"desc": f"c = G* (G* = {Gs!r}); no turning point found ({len(A['turns'])}); "
                                  f"V_c = sigma*^2 ({Vc!r} vs {s2!r})",
                          "pass": len(A["turns"]) == 0 and abs(Gs - C) <= 1e-12 and abs(Vc - s2) <= 1e-12 * Vc})
    elif case in ("P2",):
        tests = ([("row R2 < s*^2 (interior)", s2 / 2, "All"), ("row s*^2<R2<V_c (interior)", (s2 + Vc) / 2, "two rays"),
                  ("row V_c<=R2<F (interior)", (Vc + F) / 2, "upper ray"), ("row R2 >= F (interior)", 1.5 * F, "Empty")]
                 + crit("sigma*^2", s2, "two rays", "All", "two rays") + crit("V_c", Vc, "upper ray", "two rays", "upper ray")
                 + crit("F", F, "Empty", "upper ray", "Empty"))
        extra.append(comp_join(A, s2, P0s))
    elif case == "P3":
        tests = ([("row R2 < s*^2 (interior)", s2 / 2, "All"), ("row s*^2<R2<F (interior)", (s2 + F) / 2, "two rays"),
                  ("row F<=R2<V_c (interior)", (F + Vc) / 2, "lower ray"), ("row R2 >= V_c (interior)", 1.5 * Vc, "Empty")]
                 + crit("sigma*^2", s2, "two rays", "All", "two rays") + crit("F", F, "lower ray", "two rays", "lower ray")
                 + crit("V_c", Vc, "Empty", "lower ray", "Empty"))
        extra.append(comp_join(A, s2, P0s))
    else:  # boundary Pi_B: V_c = F, upper-ray row empty
        tests = ([("row R2 < s*^2 (interior)", s2 / 2, "All"), ("row s*^2<R2<V_c (interior)", (s2 + F) / 2, "two rays"),
                  ("row R2 >= F (interior)", 1.5 * F, "Empty")]
                 + crit("sigma*^2", s2, "two rays", "All", "two rays") + crit("F = V_c", F, "Empty", "two rays", "Empty"))
        extra.append({"desc": f"V_c = F to 1e-12 relative ({Vc!r} vs {F!r})", "pass": abs(Vc - F) <= 1e-12 * F})
        extra.append(comp_join(A, s2, P0s))
    ok = run_case(f"Prop 4.2 {case} (Pi = {Pi:g})", A, tests, extra)
    if case == "boundary Pi_B":
        got = [r["got"] for r in R["cases"][f"Prop 4.2 {case} (Pi = {Pi:g})"]["rows"]]
        R["cases"][f"Prop 4.2 {case} (Pi = {Pi:g})"]["upper_ray_seen"] = "upper ray" in got

# ---- Proposition 5.2
Pi, Pi0 = 1.0, 1.0
f, df = coupling_sweep(Pi, Pi0)
A = analyse(f, df)
K = Pi / (Pi + Pi0)
s2 = g_star(Pi) / Pi
cst = g_star(Pi) / K
cF = 2 * F * (Pi + Pi0)
tests = ([("row R2 < s*^2 (interior)", s2 / 2, "All"), ("row s*^2<R2<F (interior)", (s2 + F) / 2, "two rays"),
          ("row R2 >= F (interior)", 1.5 * F, "upper ray")]
         + crit("sigma*^2", s2, "two rays", "All", "two rays") + crit("F", F, "upper ray", "two rays", "upper ray"))
cs_F = classify(A, F)["components"]
cs_15 = classify(A, 1.5 * F)["components"]
start_F = 10.0**cs_F[-1][0]
start_15 = 10.0**cs_15[-1][0]
extra = [{"desc": f"R2 = F: upper ray starts at {start_F:.12g} (c_F = {cF:.12g})",
          "pass": abs(start_F - cF) <= 1e-9 * cF},
         {"desc": f"R2 = 1.5F: upper ray starts at c_R = {start_15:.10g} >= c_F", "pass": start_15 >= cF},
         comp_join(A, s2, cst)]
run_case("Prop 5.2 coupling (Pi = Pi0 = 1)", A, tests, extra)

R["pass"] = all(v["pass"] for v in R["cases"].values()) and not R["cases"]["Prop 4.2 boundary Pi_B (Pi = 50)"]["upper_ray_seen"]
R["n_tests"] = sum(len(v["rows"]) for v in R["cases"].values())
R["n_match"] = sum(r["match"] for v in R["cases"].values() for r in v["rows"])
print(f"T8.3: {'PASS' if R['pass'] else 'FAIL'} ({R['n_match']}/{R['n_tests']} classes match)")
save_json(R, "t8_3.json")
