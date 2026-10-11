"""Task 15 register updates (Parts A, B, C.1, F.2 pre-run).
- results.yaml: citations jazwinski1970 -> latency; simon2006 -> tau-relay-variance, stationary-variance (Part A.2);
  3.2 and 6.5 verified by "T14 G", status proved (Part F.2).
- references.yaml: the prompt's frozen numbering; first_cited from the thesis draft (first [n] occurrence, by section).
- figures.yaml: the prompt's fixed B.n mapping.
Usage: python3 t15_register.py"""
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REG = os.path.join(CLS, "register")
FROZEN = ["kalmanbucy1961", "ernstbanks2002", "friston2010", "heffes1966", "friedland1967", "nishimura1967", "griffin1968",
          "sangsukiam1990", "ge2016", "teunissen2021", "crouse2023", "singh2009", "boominathan2022", "hotzskelton1987",
          "xuskelton1992", "heeger1992", "carandiniheeger2012", "blackwell1951", "blackwell1953", "greenshtein1996",
          "yuksellinder2012", "yukselbasar2013", "yukselbasar2024", "hansentorgersen1974", "kalata1984", "sahomasugi2016",
          "brysonjohansen1965", "brysonhenrikson1968", "jazwinski1970", "edelsbrunnerharer2010", "cohensteiner2007", "carr2003",
          "milnor1963", "edelsbrunner2002", "oudot2015", "deyst1968", "kurt2025", "simon2006", "kalman1960", "andersonmoore1979",
          "hotzskelton1985", "collinsskelton1987", "yasuda1993", "skeltonikeda1989", "chang2014", "shmaliy2020", "ren2021",
          "martinezrey2017", "lecam1964", "torgersen1991", "hogeboomburr2021", "barshalom2002", "yoder2018"]
FIGS = [("B.1", "stage1-schematic", "fig01_stage1_schematic", "t13/t13_figures_paper2.py"),
        ("B.2", "normal-form-plane", None, "t15/make_fig_B2.py"),
        ("B.3", "design-sweeps", "fig_t8_sweeps", "t8_figures.py"),
        ("B.4", "realizability", "fig02_realizability", "t13/t13_figures_paper2.py"),
        ("B.5", "hill-phase", "fig03_hill_phase", "t13/t13_figures_paper2.py"),
        ("B.6", "peak-heights", "fig04_peak_heights", "t13/t13_figures_paper2.py"),
        ("B.7", "tau-normalizations", "fig05_tau_normalizations", "t13/t13_figures_paper2.py"),
        ("B.8", "optimal-sampling", "fig08_optimal_sampling", "t13/t13_figures_paper2.py"),
        ("B.9", "sampled-relay", "fig09_sampled_relay", "t13/t13_figures_paper2.py"),
        ("B.10", "process-noise", "fig10_process_noise", "t13/t13_figures_paper2.py"),
        ("B.11", "power-family", "fig06_power_family", "t13/t13_figures_paper2.py"),
        ("B.12", "delay", "fig07_delay", "t13/t13_figures_paper2.py")]


DESC = {
    "B.1": "Left: a schematic piecewise strictly monotone curve sigma^2(theta) on theta in [0, 10] (a sum of three Gaussian bumps "
           "and a logistic step; no filtering parameters), its endpoint limits and turning-point values as dotted horizontal lines "
           "(the critical tolerances), turning points marked, and the failure set at the dashed tolerance R^2 = 1.25 shaded. Right: "
           "the class read off in each band between consecutive critical tolerances.",
    "B.2": "The (nu, q) plane, nu = 2 Sigma Pi/lambda^2 on a log axis from 1e-2 to 1e3 and q = G/(F Pi) from 0 to 5: the floor "
           "crossing q = 2, the optimal envelope q*(nu) = 2/(1 + sqrt(1 + nu)) (where the optimal variance ratio equals q*), and "
           "the tolerance boundaries V(nu, q) = R^2_rel for R^2_rel = 0.5, 1 and 2, with the point (nu_R, 0.5) where the "
           "R^2_rel = 0.5 boundary touches the envelope marked; only q >= 0 is drawn.",
    "B.3": "sigma^2 (log scale) at lambda = c = 1, Sigma = 0.01 along three design sweeps: (a) the prior sweep over Pi_0 from "
           "1e-2 to 1e5 at Pi = 1 (case P3, U-shaped, with F, V_c, the minimum sigma*^2 and Pi_0* marked and a zoom inset near the "
           "minimum); (b) the prior sweep at Pi = 500 (case P1, monotone, with F and V_c marked); (c) the coupling sweep over c "
           "from 1e-4 to 10 at Pi = Pi_0 = 1, with F, sigma*^2, c* and c_F marked and a zoom inset.",
    "B.4": "sigma^2 against precision Pi (log axis) at lambda = 1, Sigma = 0.01 (F = 0.01): the optimal envelope sigma*^2(Pi) "
           "with the region below it shaded as unreachable, a Bayesian-weight base curve (kappa = 1.5) with three compactly "
           "supported bumps of peak 1.5F placed before the envelope touch point Pi_c = 56.7, the tolerance R^2 = 1.25F (three "
           "windows) and the tolerance R^2 = 0.6F with the forced lower ray (0, pi_R), pi_R = 222.2, marked.",
    "B.5": "Hill gain with n = 2 at lambda = c = 1, Sigma = 0.01: over the half-saturation Pi_0 (log axis), the turning-point "
           "values m/F (dashed) and M/F (solid) as tolerances R^2/F, the band m <= R^2 < min(M, F) shaded as the mixed class "
           "lower ray + window and the band F <= R^2 < M shaded as window, with vertical lines at the pair birth "
           "Pi_0^pair = 31.475 and the window onset c lambda/(4 Sigma) = 25.",
    "B.6": "Peak variance M/F against the initial over-weighting x for the Bayesian-weight gain (x = kappa) and the misspecified "
           "Kalman gain (x = F'/F) at lambda = lambda' = c = 1, Sigma = 0.01; both rise from 1 at x = 2, and the end values at "
           "x = 100 (9.2875 and 17.575) are annotated.",
    "B.7": "Stationary error against correlation time tau (log axes) at lambda = 1, Sigma = 0.01, Pi = 1 for the relay with "
           "G = 0.5 and the optimal filter. Left, matched zero-frequency power: both decrease, with F marked. Right, matched "
           "variance v = 0.05: the relay increases and the optimal error is unimodal with maximum P_max = 0.008333 at "
           "tau = 1/lambda; the optimal-filter failure set at R^2 = 0.8 P_max is shaded.",
    "B.8": "Optimal error against the sampling interval Delta t (log axis) in the point-sampled model at lambda = 1, "
           "Sigma = 0.01, Pi = 1 (per-sample noise variance 1/(Pi Delta t)): the error at sample times (post) falls from "
           "sigma*^2 towards 0, while the prior error and the time average rise from sigma*^2 to F; sigma*^2 and F are marked.",
    "B.9": "Sampled relay D1 (gain 1 - exp(-G Delta t), G = 0.5, lambda = 1, Sigma = 0.01, Pi = 1) along Delta t (log axis). "
           "Left: the error at sample times with the window band R^2 in (0.09, 0.20457) shaded and the excess crossing "
           "Delta t_E = 100 marked. Right: the time average as avg/F - 1 on a symmetric-log axis, with the two-ray band between its "
           "minimum and F shaded and Delta t_E marked.",
    "B.10": "The process-noise sweep at lambda = Pi = 1, against u = 2 Sigma Pi/lambda^2 (log axes), for the Sigma-independent "
            "gain (G = 1), the Sigma-tracking gain over-trusting precision by rho = 10, and the optimal filter. Left: absolute "
            "error. Right: relative error sigma^2/F, where the over-trusting gain rises above 1 to a peak of about 2.17 before "
            "falling.",
    "B.11": "Colour map of the optimal error relative to its supremum over tau, P/sup P, for the power-normalised family "
            "S = K tau^beta/(1 + tau^2 omega^2) at lambda = 1, Sigma = 0.01, K = 1, over the exponent beta (horizontal) and "
            "log10(lambda tau) (vertical); the position of the single maximum for 0 < beta < 2 is drawn, and the three regimes "
            "(ordered with information increasing in tau; spectra cross; ordered with information decreasing in tau) are labelled "
            "in words.",
    "B.12": "Optimal filtering error P(d(theta)) for observations delayed by d(theta) = theta exp(-theta), at lambda = 1, "
            "Sigma = 0.01, Pi = 1, against theta (log axis): it rises from sigma*^2 = 0.0099505 to P(1/e) = 0.0099763 at "
            "theta = 1 and falls back; the optimal-filter failure set at R^2 = 0.0099634 is shaded, and theta = 1, where the causal "
            "order reverses, is marked.",
}


def first_cited():
    draft = open(os.path.join(HERE, "input", "Thesis_Draft_ch1-4.md")).read().split("## Appendices")[0]
    sec, out = None, {}
    for ln in draft.split("\n"):
        h = re.match(r"^#{2,3} (\S+)", ln)
        if h:
            sec = ln.lstrip("#").strip()
        for g in re.findall(r"\\\[([0-9–, ]+)\\\]", ln):
            for part in g.split(","):
                part = part.strip()
                a, _, b = part.partition("–")
                for n in range(int(a), int(b or a) + 1):
                    out.setdefault(n, f"draft §{sec}")
    return out


def main():
    res = yaml.safe_load(open(os.path.join(REG, "results.yaml")))
    add = {"latency": ["jazwinski1970"], "tau-relay-variance": ["simon2006"], "stationary-variance": ["simon2006"]}
    for e in res:
        for c in add.get(e["key"], []):
            if c not in e["citations"]:
                e["citations"].append(c)
        if e["thesis_no"] in ("3.2", "6.5"):
            e["verified_by"], e["status"] = ["T14 G"], "proved"
    head = "".join(l for l in open(os.path.join(REG, "results.yaml")) if l.startswith("#"))
    with open(os.path.join(REG, "results.yaml"), "w") as fh:
        fh.write(head)
        yaml.safe_dump(res, fh, allow_unicode=True, sort_keys=False, width=200, default_flow_style=None)
    fc = first_cited()
    refs = [{"number": i + 1, "key": k, "first_cited": fc.get(i + 1, "planned: chapters 6–7 (results.yaml attachments)"),
             "status": "planned" if i + 1 >= 46 else "cited"} for i, k in enumerate(FROZEN)]
    with open(os.path.join(REG, "references.yaml"), "w") as fh:
        fh.write("# Reference register (Task 15). Numbers are assigned by first citation in the thesis and frozen; a new reference\n"
                 "# takes the next free number. Full entries: classification/references.bib; rendered list: Appendix_C_References.md.\n")
        yaml.safe_dump(refs, fh, allow_unicode=True, sort_keys=False, width=200)
    figs = [{"label": l, "key": k, "source_file": (f"figs_paper2/{s}" if s and s.startswith("fig0") or s and s.startswith("fig1")
                                                   else ("figures/fig_t8_sweeps" if s else None)),
             "script": sc, "output": f"figs_thesis/{l}_{k}", "description": DESC[l], "caption_source": (f"source/figs/{s}.txt" if s and s.startswith("fig") and s != "fig_t8_sweeps" else None)}
            for l, k, s, sc in FIGS]
    with open(os.path.join(REG, "figures.yaml"), "w") as fh:
        fh.write("# Figure register (Task 15). The text cites Figure B.n; images carry no result or figure numbers.\n")
        yaml.safe_dump(figs, fh, allow_unicode=True, sort_keys=False, width=200)
    missing = [n for n in range(1, 46) if n not in fc]
    print("first_cited found for", len([n for n in range(1, 46) if n in fc]), "of 45; missing", missing)


if __name__ == "__main__":
    main()
