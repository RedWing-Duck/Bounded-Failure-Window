"""T10.2: realizability (A1): every class, forbidden classes, A1.3 regular multi-window (literal + supplementary)."""
import time

import mpmath as mp

from classify import classify, name
from t10_common import T, analyse, dsig2_dG, gstar, save_json, sig2
from t10_construct import LN10, PL, Target, envelope_target

t0 = time.time()
lam, Sig = mp.mpf(1), mp.mpf("0.01")
F = Sig / lam
R = {"every": [], "forbidden": [], "a13": [], "a13_supp": []}


def target_nodes(ell, u, k, R2):
    hi, lo = 2 * R2, R2 / 2
    nodes = ([hi] if ell else []) + [lo] + [hi, lo] * k + ([hi] if u else [])
    return nodes, (3 * R2 if ell else 0), (3 * R2 if u else 0)


def check_target(tg, A, R2, want):
    """G >= 0, continuity at breakpoints, sigma2 == v, both routes == want."""
    c = A["curve"]
    xs = [mp.mpf(-25) + mp.mpf(i) / 12 for i in range(601)] + tg.breaks
    Gmin = min(tg.G(T(x))[0] for x in xs)
    cont = max(abs(tg.G(T(b) * (1 + mp.mpf("1e-30")))[0] - tg.G(T(b) * (1 - mp.mpf("1e-30")))[0])
               / max(tg.G(T(b))[0], mp.mpf("1e-30")) for b in tg.breaks) if tg.breaks else mp.mpf(0)
    dv = max(abs(c.f(T(x)) - tg.val(x)) / tg.val(x) for x in xs)
    r = classify(A, R2)
    ok = Gmin >= 0 and cont <= mp.mpf("1e-20") and dv <= mp.mpf("1e-40") and r["route_i"] == want and r["route_ii"] == want
    return {"G_min": Gmin, "cont_rel": cont, "sigma2_minus_v_rel": dv, "route_i": name(r["route_i"]),
            "route_ii": name(r["route_ii"]), "target": name(want), "pass": bool(ok)}


# ---------------- every class
for rf in ("0.5", "0.99", "1", "1.01", "3"):
    R2 = F * mp.mpf(rf)
    targets = [(ell, u, k) for ell in (0, 1) for u in (0, 1) for k in range(6)] + ["All"]
    for tgt in targets:
        if tgt != "All" and tgt[0] == 0 and R2 < F:
            # forbidden: v = w unclipped, v <= R2 near 0; discriminant at pi_R/2 must be negative
            nodes, L, Rl = target_nodes(0, tgt[1], tgt[2], R2)
            w = PL(nodes, L, Rl)
            piR = 2 * lam * (F - R2) / R2**2
            P = piR / 2
            vP = w(mp.log10(P))
            disc = P * vP**2 + 2 * lam * vP - 2 * Sig
            blocked = disc < 0 and vP <= R2
            R["forbidden"].append({"R2_over_F": rf, "target": name(tgt), "pi_R": piR, "v_at_piR_half": vP,
                                   "disc": disc, "blocked": bool(blocked)})
            continue
        if tgt == "All":
            w = PL([2 * R2, mp.mpf("2.5") * R2, 2 * R2], 3 * R2, 3 * R2)
        else:
            nodes, L, Rl = target_nodes(*tgt, R2)
            w = PL(nodes, L, Rl)
        tg = envelope_target(lam, Sig, w)
        A = analyse(tg.curve())
        rec = check_target(tg, A, R2, tgt)
        rec["R2_over_F"] = rf
        R["every"].append(rec)
        if not rec["pass"]:
            print("  FAIL", rec)
print(f"every class: {sum(r['pass'] for r in R['every'])}/{len(R['every'])} realized; forbidden blocked "
      f"{sum(r['blocked'] for r in R['forbidden'])}/{len(R['forbidden'])}  ({time.time() - t0:.0f}s)")

# ---------------- A1.3
c = mp.mpf(1)
kappa = mp.mpf("1.5")
Pi0 = c * lam / (kappa * Sig)


def vB(x):
    Pi = T(x)
    return sig2(c * Pi / (Pi + Pi0), Pi, lam, Sig)


def vB_dx(x):
    Pi = T(x)
    G = c * Pi / (Pi + Pi0)
    dG = c * Pi0 / (Pi + Pi0)**2
    dPi = dsig2_dG(G, Pi, lam, Sig) * dG - G**2 / (2 * Pi**2 * (lam + G))
    return dPi * Pi * LN10


Pic = mp.findroot(lambda P: c * P / (P + Pi0) - gstar(P, lam, Sig), 50)
centers = [mp.mpf(-5 + j) for j in range(5)]


def gauss(k):
    sg = mp.mpf("0.15")
    val = lambda x: vB(x) + sum(F / 2 * mp.exp(-(x - centers[j])**2 / (2 * sg**2)) for j in range(k))
    dval = lambda x: vB_dx(x) + sum(-F / 2 * (x - centers[j]) / sg**2 * mp.exp(-(x - centers[j])**2 / (2 * sg**2))
                                    for j in range(k))
    return val, dval


def compact(k):
    wd = mp.mpf("0.4")

    def b(x, j):
        z = (x - centers[j]) / wd
        return mp.exp(1 - 1 / (1 - z**2)) if abs(z) < 1 else mp.mpf(0)

    def db(x, j):
        z = (x - centers[j]) / wd
        if abs(z) >= 1:
            return mp.mpf(0)
        return b(x, j) * (-2 * z / (1 - z**2)**2) / wd
    val = lambda x: vB(x) + sum(F / 2 * b(x, j) for j in range(k))
    dval = lambda x: vB_dx(x) + sum(F / 2 * db(x, j) for j in range(k))
    brk = [centers[j] + s * wd for j in range(k) for s in (-1, 1)]
    return val, dval, brk


def regularity(tg):
    g0 = tg.G(mp.mpf("1e-12"))[0]
    g11, g12 = tg.G(mp.mpf("1e11"))[0], tg.G(mp.mpf("1e12"))[0]
    return {"G_1e-12": g0, "G2_over_Pi_1e-12": g0**2 / mp.mpf("1e-12"), "G_1e11": g11, "G_1e12": g12,
            "ratio_minus_1": g12 / g11 - 1,
            "ok_zero": bool(g0 < mp.mpf("1e-9") and g0**2 / mp.mpf("1e-12") < mp.mpf("1e-9")),
            "ok_converge": bool(abs(g12 / g11 - 1) <= mp.mpf("1e-6"))}


for k in range(1, 6):
    for kind in ("literal", "supp"):
        if kind == "literal":
            val, dval = gauss(k)
            tg = Target(lam, Sig, val, dval, [])
        else:
            val, dval, brk = compact(k)
            tg = Target(lam, Sig, val, dval, brk, branch=lambda P: 1 if P <= Pic else -1)
        reg = regularity(tg)
        A = analyse(tg.curve())
        r = classify(A, mp.mpf("1.25") * F)
        win = r["route_i"] == (0, 0, k) and r["route_ii"] == (0, 0, k)
        rec = {"k": k, **reg, "route_i": name(r["route_i"]), "route_ii": name(r["route_ii"]), "k_windows": bool(win)}
        if kind == "literal":
            rec["pass"] = bool(reg["ok_zero"] and reg["ok_converge"] and win)
            R["a13"].append(rec)
        else:
            Gp = Pic * vB(mp.log10(Pic)) + mp.sqrt(max(mp.mpf(0), Pic**2 * vB(mp.log10(Pic))**2
                                                       - 2 * Pic * (Sig - lam * vB(mp.log10(Pic)))))
            Gm = Pic * vB(mp.log10(Pic)) - mp.sqrt(max(mp.mpf(0), Pic**2 * vB(mp.log10(Pic))**2
                                                       - 2 * Pic * (Sig - lam * vB(mp.log10(Pic)))))
            jump = abs(Gp - Gm) / gstar(Pic, lam, Sig)
            gneg = min(tg.G(T(mp.log10(Pic) + mp.mpf(i) / 12))[0] for i in range(1, 300))
            rec.update({"Pi_c": Pic, "branch_jump_rel": jump, "G_minus_min": gneg})
            rec["pass"] = bool(reg["ok_zero"] and reg["ok_converge"] and win and jump <= mp.mpf("1e-30") and gneg >= 0)
            R["a13_supp"].append(rec)
        print(f"A1.3 {kind} k={k}: G(1e-12)={mp.nstr(reg['G_1e-12'], 4)}, G(1e12)/G(1e11)-1={mp.nstr(reg['ratio_minus_1'], 4)}, "
              f"classes {name(r['route_i'])}/{name(r['route_ii'])} -> {'PASS' if rec['pass'] else 'FAIL'}")

ok_every = all(r["pass"] for r in R["every"])
ok_forb = all(r["blocked"] for r in R["forbidden"])
ok_a13 = all(r["pass"] for r in R["a13"])
R["pass_every"], R["pass_forbidden"], R["pass_a13"] = ok_every, ok_forb, ok_a13
R["pass_a13_supp"] = all(r["pass"] for r in R["a13_supp"])
R["pass"] = ok_every and ok_forb and ok_a13
R["seconds"] = time.time() - t0
print(f"T10.2: {'PASS' if R['pass'] else 'FAIL'} (every {ok_every}, forbidden {ok_forb}, A1.3 literal {ok_a13}; "
      f"A1.3 supplementary {R['pass_a13_supp']})")
save_json(R, "t10_2.json")
