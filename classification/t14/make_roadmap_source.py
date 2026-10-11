"""Task 14 §3.5 and §6: key-token sources for Roadmap v3 and the figure captions.
Roadmap_v3.md and figs_paper2/*.txt, README.md are read as committed at the pre-registration commit (e5edebf), converted with
make_source.Conv, and edited by the explicit EDITS below (each asserted to apply exactly once):
- the matrix of §3 becomes {{matrix}} (register/matrix.csv), which also fixes rows 25-26;
- result ranges that are not contiguous in thesis numbering are written as explicit lists;
- the novelty paragraph of §7 and the query rows for the second search set (clusters 11-17).
Usage: python3 make_roadmap_source.py"""
import os
import re
import subprocess

from make_source import Conv, load_register, TYPES
from t14_common import CLS, PREREG, REPO

SRC = os.path.join(CLS, "source")


def at_prereg(rel):
    return subprocess.run(["git", "-C", REPO, "show", f"{PREREG}:classification/{rel}"], capture_output=True, text=True,
                          check=True).stdout


def ranges_ok(text, reg):
    """Every [[a|n]]–[[b|n]] range must be contiguous in thesis numbering (same chapter, b = a + 1 ... in order)."""
    bad = []
    for m in re.finditer(r"\[\[([a-z0-9-]+)\|n\]\]\s*[–-]\s*\[\[([a-z0-9-]+)\|n\]\]", text):
        a, b = reg[m.group(1)]["thesis_no"].split("."), reg[m.group(2)]["thesis_no"].split(".")
        if a[0] != b[0] or int(b[1]) <= int(a[1]):
            bad.append(m.group(0))
    return bad


ROADMAP_EDITS = [
    ("Revised\nOctober 2026 (Task 13)", "Revised\nOctober 2026 (Task 13); result numbers rendered from `register/results.yaml` (thesis numbering, Task 14)"),
    ("consolidated in `Stages_0_4_Consolidated.md` (the \"consolidated document\" below, cited by section and\nresult number)",
     "consolidated in `Stages_0_4_Thesis.md` (the \"consolidated document\" below, cited by section and\nthesis result number; "
     "source `source/Stages_0_4_Source.md`, consolidated v1 frozen in `archive/Stages_0_4_Consolidated_v1.md`)"),
    ("| § | Section | Results (consolidated numbering) | Figures (`figs_paper2/`) |",
     "| § | Section | Results (thesis numbering) | Figures (`figs_paper2/`; thesis captions in `figs_thesis/`) |"),
    ("Lemmas 50–52, Propositions 53–55, Theorem 56, Proposition 57, Numerical result 58",
     "Lemmas 50, 51, 52, Propositions 53–55, Theorem 56, Proposition 57, @@SPLIT@@, Numerical result 58"),
    ("Lemma 13 – Proposition 26", "Lemma 13, Propositions 14, 15, 16, Theorem 17, Propositions 18, 19, 20, 21, Counterexample 22, "
     "Proposition 23, Theorems 24, 25, Proposition 26"),
    ("Lemma 27 – Conjecture 38", "Lemma 27, Propositions 28, 29, 30, 31, Theorem 32, Proposition 33, Corollary 34, Theorem 35, "
     "Proposition 36, Numerical result 37, Conjecture 38"),
    ("Lemma 39 – Proposition 44", "Lemma 39, Propositions 40, 41, 42, 43, 44"),
    ("Definition 64 – Proposition 73", "Definition 64, Theorem 65, Corollaries 66, 67, Proposition 68, Theorem 69, Propositions 70, 71, "
     "Counterexample 72, Proposition 73"),
    ("Numerical results 62–63", "Numerical results 62, 63"),
    ("filtering (methods), and Blackwell comparison of linear normal experiments (static). No source on a causal Blackwell\nordering in "
     "filtering was found. This",
     "filtering (methods), and Blackwell comparison of linear normal experiments (static).\n\n"
     "Garbling-order monotonicity of optimal performance is established for sequential experiments [greenshtein1996] and for "
     "stochastic control and teams [yuksellinder2012], [yukselbasar2013], [yukselbasar2024]. @@CAUSAL@@ is presented as the "
     "filtering instance of that principle: a causal garbling of observation processes and its consequence for filtering error. "
     "@@GAUSS@@ extends the static result for linear normal experiments [hansentorgersen1974] to stationary Gaussian processes.\n\n"
     "This"),
    ("| 10 | measurement delay optimal filtering error increases latency Kalman Bucy Ornstein Uhlenbeck |",
     "@@ROWS11_17@@| 10 | measurement delay optimal filtering error increases latency Kalman Bucy Ornstein Uhlenbeck |"),
]
# Second search set (clusters 11-17). The query strings of that search were not supplied to Task 14; the topic of each cluster
# and its sources are taken from the Task 14 bibliography list, grouped by topic here.
ROWS = [
    ("11", "comparison of statistical and sequential experiments", "[greenshtein1996], [lecam1964], [torgersen1991], [hansentorgersen1974], [blackwell1951], [blackwell1953]",
     "R (garbling order and monotone optimal performance; static and sequential, not filtering): cited for [[causal-monotonicity]], [[spectral-dominance]], [[gaussian-orderings-coincide]]"),
    ("12", "information structures in stochastic control and teams", "[yuksellinder2012], [yukselbasar2013], [yukselbasar2024], [hogeboomburr2021]",
     "R (Blackwell ordering of information structures in control): cited for [[causal-monotonicity]], [[gaussian-orderings-coincide]]"),
    ("13", "covariance control and state covariance assignment", "[hotzskelton1985], [hotzskelton1987], [collinsskelton1987], [xuskelton1992], [yasuda1993], [skeltonikeda1989]",
     "P (which covariances a gain can assign): related to [[realizability]]"),
    ("14", "optimal sampling rate for state estimation", "[martinezrey2017]", "P (sampling interval and estimation error): related to [[dt-optimal-mp]], [[mp-not-ordered]]"),
    ("15", "state estimation with coloured measurement noise", "[shmaliy2020]", "P (methods for coloured noise): related to [[matched-variance-optimal]], [[power-family-sharpness]]"),
    ("16", "divisive normalization", "[heeger1992], [carandiniheeger2012]", "P (Hill-type gain shapes in neural computation): related to [[hill-turning-points]], [[hill-classification]]"),
    ("17", "persistence, contour trees and Morse theory", "[cohensteiner2007], [edelsbrunnerharer2010], [edelsbrunner2002], [carr2003], [oudot2015], [milnor1963]",
     "P (topology of sublevel and superlevel sets of a function): related to [[critical-tolerance]], [[structural-stability]]"),
]


def main():
    reg_list, by_v1 = load_register()
    reg = {e["key"]: e for e in reg_list}
    v1 = open(os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")).read()
    v1_types = {int(m.group(2)): m.group(1) for m in re.finditer(r"^\*\*(" + TYPES + r") (\d+) ", v1, re.M)}
    C = Conv(by_v1, v1_types)
    rm = at_prereg("Roadmap_v3.md")
    lines = rm.split("\n")
    i0 = next(i for i, l in enumerate(lines) if l.startswith("| # | Sweep |"))
    i1 = i0
    while lines[i1].startswith("|"):
        i1 += 1
    rm = "\n".join(lines[:i0] + ["{{matrix}}"] + lines[i1:])
    for a, b in ROADMAP_EDITS:
        assert rm.count(a) == 1, (rm.count(a), a[:80])
        rm = rm.replace(a, b)
    rm = C.refs(rm)
    rows = "".join(f"| {n} | (second search set, cluster {n}: {topic}; query text not supplied to Task 14) | {src} | {rel} |\n"
                   for n, topic, src, rel in ROWS)
    rm = (rm.replace("@@SPLIT@@", "[[no-mixed-decreasing-ratio]]").replace("@@CAUSAL@@", "[[causal-monotonicity]]")
          .replace("@@GAUSS@@", "[[gaussian-orderings-coincide]]"))
    # second-set rows go after the first set's last row (10)
    rm = rm.replace("@@ROWS11_17@@", "")
    k = rm.index("| 10 | measurement delay optimal filtering error")
    k = rm.index("\n", k) + 1
    rm = rm[:k] + rows + rm[k:]
    rm = rm.replace("**Finding (novelty, targeted).** None of the ten searches",
                    "**Finding (novelty, targeted).** None of the ten searches of the first set")
    os.makedirs(os.path.join(SRC, "figs"), exist_ok=True)
    open(os.path.join(SRC, "Roadmap_v3_Source.md"), "w").write(rm)
    bad = ranges_ok(rm, reg)
    # figure captions
    names = [l for l in subprocess.run(["git", "-C", REPO, "ls-tree", "--name-only", PREREG, "classification/figs_paper2/"],
                                         capture_output=True, text=True).stdout.split() if l.endswith((".txt", ".md"))]
    for n in names:
        t = at_prereg(n.split("classification/", 1)[1])
        base = os.path.basename(n)
        if base == "README.md":
            for a, b in [("# Paper 2 figure set", "# {{thesis:Thesis figure set (captions in thesis numbering)}}{{paper:Paper 2 figure set}}"),
                         ("from the formulas of `Stages_0_4_Consolidated.md`.",
                          "from the formulas of the consolidated document (v1, now `archive/Stages_0_4_Consolidated_v1.md`)."
                          "{{thesis: Captions here use thesis numbers; the images are the files in `figs_paper2/`. The drawn labels "
                          "in fig01 (axis title) and fig06 (legend) still show the consolidated v1 numbers of [[critical-tolerance]] "
                          "and [[power-family-unimodal]].}}")]:
                assert t.count(a) == 1, a
                t = t.replace(a, b)
            t = re.sub(r"!\[(fig\d+_\w+)\]\((fig\d+_\w+\.png)\)", r"![\1](../figs_paper2/\2)", t)
        t = C.refs(t)
        bad += ranges_ok(t, reg)
        open(os.path.join(SRC, "figs", base), "w").write(t)
    print("roadmap + captions written; non-contiguous ranges:", bad, "| warnings", C.warn)


if __name__ == "__main__":
    main()
