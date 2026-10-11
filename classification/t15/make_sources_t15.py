"""Task 15 source edits (Parts B, C.5, D, F.1, H.1). Every edit is asserted to apply exactly once.
- source/thesis_only/<key>.md: thesis-only statements imported verbatim from t15/input/Thesis_Draft_ch1-4.md (line ranges below),
  included in the thesis render only.
- Stages_0_4_Source.md: thesis-only include blocks; the split "Paper 1" (Part H.1); the §12 literature sentence as citations in
  the thesis render.
- Roadmap_v3_Source.md: citation tokens; rows 11-17 replaced by the Part D table; figure references as {{fig:...}}.
- source/figs/*: "Figure N" and image links through the figure register.
Usage: python3 make_sources_t15.py"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
SRC = os.path.join(CLS, "source")
DRAFT = open(os.path.join(HERE, "input", "Thesis_Draft_ch1-4.md")).read().split("\n")
# key: (first line, last line, first-line prefix, draft section)
IMPORTS = {"signature": (173, 179, "**Definition 2.3.**", "§2.4"), "reparameterisation": (222, 224, "**Corollary 2.8.**", "§2.7"),
           "structural-stability": (232, 251, "**Proposition 2.9.**", "§2.8"), "normal-form": (292, 316, "Two dimensionless numbers", "§3.2"),
           "tau-optimal-normal-form": (435, 443, "One extension is immediate.", "§3.8")}
OLDFIG = {"1": "stage1-schematic", "2": "realizability", "3": "hill-phase", "4": "peak-heights", "5": "tau-normalizations",
          "6": "power-family", "7": "delay", "8": "optimal-sampling", "9": "sampled-relay", "10": "process-noise"}
PART_D = """| # | Cluster (thesis results) | Searched as | Verdict | Closest prior work | Use in thesis |
|---|---|---|---|---|---|
| 11 | Causal information ordering (Def. 7.1, Thm 7.2, Prop. 7.5, Thm 7.6) | comparison of sequential experiments · Blackwell filtration · causal garbling · comparison of information structures · dynamic Blackwell | Close prior: the general principle | [@greenshtein1996; @yuksellinder2012; @yukselbasar2013; @yukselbasar2024; @blackwell1951; @blackwell1953; @hansentorgersen1974; @lecam1964; @torgersen1991; @hogeboomburr2021]: garbling monotonicity for sequential experiments and control/team costs; no filtering-error version found | Claim only the causal-process definition and the filtering-error monotonicity; cite first |
| 12 | Delay counterexample (Cex. 7.12) | Blackwell equivalent time shift · filtering versus smoothing information · delayed observations comparison of experiments · latency value of information | No close prior found | Delayed-measurement filtering: [@jazwinski1970; @barshalom2002; @yoder2018]; that delay hurts filtering is folklore | Claim as a counterexample about orders on experiments, not as "delay hurts" |
| 13 | Power-family sharpness (Thm 7.8; Prop. 6.10) | correlation time Kalman non-monotone · fixed variance vs fixed spectral density · colored noise bandwidth estimation error · noise normalization OU | No close prior found | Coloured-noise methods: [@brysonjohansen1965; @brysonhenrikson1968; @chang2014; @shmaliy2020]; no normalisation comparison or exponent threshold found | Claimable |
| 14 | Realizability (Thm 5.1) | covariance assignment · covariance control · achievable error variance · attainable covariance suboptimal gain · performance envelope Kalman | Known variant | Covariance assignment, matrix state feedback: [@hotzskelton1985; @hotzskelton1987; @collinsskelton1987; @xuskelton1992; @yasuda1993; @skeltonikeda1989] | Claim the scalar filtering attainability and explicit inverse gain as the filtering analogue |
| 15 | Hill mixed class (Thm 5.12, Prop. 5.13) | sigmoidal gain precision · Hill function gain estimation · divisive normalization precision weighting · neural gain control noise non-monotone | No close prior found | Gain form from divisive normalisation: [@heeger1992; @carandiniheeger2012]; no estimation use with a multi-component failure set | Claimable; credit the gain form to [@carandiniheeger2012] |
| 16 | Sampling interval (Thm 6.19, Prop. 7.16) | sampling period steady-state Kalman error · sampled-data Kalman filter sampling rate · optimal sampling interval estimation · a priori a posteriori error sampling interval · intersample error | Known variant | Sampled-data filtering: [@andersonmoore1979]; optimal sampling rate with delays: [@martinezrey2017] | Remark on which error functional is quoted; state the Δt noise scaling |
| 17 | The framework (Thm 2.2, Prop. 2.9) | persistent homology superlevel sets · merge tree · Morse theory one-dimensional · excursion set · level crossings · persistence diagram stability | Citation only | Persistence and merge trees: [@edelsbrunnerharer2010; @cohensteiner2007; @carr2003; @milnor1963; @edelsbrunner2002; @oudot2015] | Cite; the fixed-level versus all-levels stability contrast stays a remark |

Second-set priority combination searches: all four returned no prior work. 'No close prior found' describes these searches, not worldwide novelty."""


def edit(text, a, b):
    assert text.count(a) == 1, (text.count(a), a[:80])
    return text.replace(a, b)


def block(key):
    return "<!--thesis-->\n{{include:thesis_only/" + key + ".md}}\n\n<!--/thesis-->\n"


def main():
    os.makedirs(os.path.join(SRC, "thesis_only"), exist_ok=True)
    for key, (a, b, pre, sec) in IMPORTS.items():
        lines = DRAFT[a - 1:b]
        assert lines[0].startswith(pre), (key, lines[0][:60])
        head = f"*Thesis-only text, imported verbatim from the thesis draft (`t15/input/Thesis_Draft_ch1-4.md`, {sec}, lines {a}–{b}).*"
        open(os.path.join(SRC, "thesis_only", key + ".md"), "w").write(head + "\n\n" + "\n".join(lines).rstrip() + "\n")
    p = os.path.join(SRC, "Stages_0_4_Source.md")
    s = open(p).read()
    s = edit(s, "inherits Paper\n1's regularity", "inherits\n{{phase1}}'s regularity")
    s = edit(s, "\n---\n\n## 3. The model along precision", "\n" + block("signature") + block("reparameterisation") +
             block("structural-stability") + "---\n\n## 3. The model along precision")
    s = edit(s, "\n**[[excess-identity]] (excess identity; {{phase1}}).**", "\n" + block("normal-form") +
             "**[[excess-identity]] (excess identity; {{phase1}}).**")
    s = edit(s, "\n**[[tau-optimal-monotone]] (optimal error decreases", "\n" + block("tau-optimal-normal-form") +
             "**[[tau-optimal-monotone]] (optimal error decreases")
    s = edit(s, "(Hansen and Torgersen, *Ann. Statist.* 2 (1974)\n367–373; Torgersen, *Comparison of Statistical Experiments*, 1991)",
             "{{paper:(Hansen and Torgersen, *Ann. Statist.* 2 (1974)\n367–373; Torgersen, *Comparison of Statistical Experiments*, 1991)}}"
             "{{thesis:[@hansentorgersen1974; @torgersen1991]}}")
    open(p, "w").write(s)
    p = os.path.join(SRC, "Roadmap_v3_Source.md")
    s = open(p).read()
    lines = s.split("\n")
    i0 = next(i for i, l in enumerate(lines) if l.startswith("| 11 | (second search set"))
    i1 = next(i for i, l in enumerate(lines) if l.startswith("| 17 | (second search set"))
    s = "\n".join(lines[:i0] + [""] + PART_D.split("\n") + lines[i1 + 1:])
    s = edit(s, "[yuksellinder2012], [yukselbasar2013], [yukselbasar2024]", "[@yuksellinder2012; @yukselbasar2013; @yukselbasar2024]")
    s = re.sub(r"\[(greenshtein1996|hansentorgersen1974)\]", r"[@\1]", s)
    for old, new in [("| Fig. 1 |", "| {{fig:stage1-schematic}} |"), ("| Fig. 2 |", "| {{fig:realizability}} |"),
                     ("| Figs 3, 4 |", "| Figures {{fig:hill-phase|n}}, {{fig:peak-heights|n}} |"),
                     ("| Figs 5, 6 |", "| Figures {{fig:tau-normalizations|n}}, {{fig:power-family|n}} |"),
                     ("| Figs 8, 9 |", "| Figures {{fig:optimal-sampling|n}}, {{fig:sampled-relay|n}} |"),
                     ("| Fig. 10 |", "| {{fig:process-noise}} |"), ("| Fig. 7 |", "| {{fig:delay}} |"),
                     ("| Figures (`figs_paper2/`; thesis captions in `figs_thesis/`) |", "| Figures (Appendix B; images in `figs_thesis/`) |")]:
        s = edit(s, old, new)
    open(p, "w").write(s)
    for f in sorted(os.listdir(os.path.join(SRC, "figs"))):
        p = os.path.join(SRC, "figs", f)
        t = open(p).read()
        t = re.sub(r"(?m)^Figure (\d+)\.", lambda m: "{{fig:" + OLDFIG[m.group(1)] + "}}.", t)
        if f == "README.md":
            t = edit(t, "Generated by `classification/t13/t13_figures_paper2.py` from the formulas",
                     "{{paper:Generated by `classification/t13/t13_figures_paper2.py`}}{{thesis:Generated by "
                     "`classification/t15/make_figs_thesis.py` (text-element edits of `t13/t13_figures_paper2.py` and `t8_figures.py`, "
                     "plus `t15/make_fig_B2.py`)}} from the formulas")
            t = edit(t, "sequential single-hue Blues for Figure 6.", "sequential single-hue Blues for {{fig:power-family}}.")
            t = re.sub(r"## fig(\d\d)_\w+\n\n!\[fig\d\d_\w+\]\(\.\./figs_paper2/fig\d\d_\w+\.png\)",
                       lambda m: "## {{fig:" + OLDFIG[str(int(m.group(1)))] + "}}\n\n![{{fig:" + OLDFIG[str(int(m.group(1)))] + "}}]({{fig:" + OLDFIG[str(int(m.group(1)))]
                       + "|n}}_" + OLDFIG[str(int(m.group(1)))] + ".png)", t)
            t = edit(t, "{{thesis: Captions here use thesis numbers; the images are the files in `figs_paper2/`. The drawn labels "
                        "in fig01 (axis title) and fig06 (legend) still show the consolidated v1 numbers of [[critical-tolerance]] "
                        "and [[power-family-unimodal]].}}",
                     "{{thesis: Captions here use thesis numbers. The images are the regenerated files `B.n_<key>.png` in this folder; "
                     "they carry no result or figure numbers (Task 15). {{fig:normal-form-plane}} and {{fig:design-sweeps}} have no caption file here; "
                     "Appendix B describes every figure.}}")
        open(p, "w").write(t)
    print("sources edited")


if __name__ == "__main__":
    main()
