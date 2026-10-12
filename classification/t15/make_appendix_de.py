"""Task 15 Part E.3-E.4: Appendix D (verification record, Tasks 1-14; T15 added after its run) and Appendix E (reproduction).
Appendix D copies outcomes from the RESULTS files: pass/fail counts are parsed from each report's check table, and every failure
is listed with the attribution its report gives (FAILURES below, one line each, quoted or condensed from the report's diagnosis).
Nothing is re-judged. Usage: python3 make_appendix_de.py [--with-t15]"""
import importlib.metadata as md
import os
import platform
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)

TASKS = [  # task, prereg, results file, how to select its check rows
    ("T1", "verification/PREREG.md", "verification/REPORT.md", r"^\| T1\."),
    ("T2", "verification/PREREG.md", "verification/REPORT.md", r"^\| T2\."),
    ("T3", "verification/PREREG.md", "verification/REPORT.md", r"^\| T3\."),
    ("T4", "verification/PREREG.md", "verification/REPORT.md", None),
    ("T5", "verification/PREREG.md", "verification/REPORT.md", None),
    ("T6", "verification/PREREG_t6.md", "verification/REPORT.md", "T6"),
    ("T7", "verification/PREREG_t7.md", "verification/REPORT.md", r"^\| T7\."),
    ("T8", "classification/PREREG_t8.md", "classification/REPORT.md", "first"),
    ("T9", "classification/PREREG_t9.md", "classification/t9/RESULTS_t9.md", "first"),
    ("T10", "classification/PREREG_t10.md", "classification/t10/RESULTS_t10.md", "first"),
    ("T11", "classification/PREREG_t11.md", "classification/t11/RESULTS_t11.md", "first"),
    ("T12", "classification/PREREG_t12.md", "classification/t12/RESULTS_t12.md", "first"),
    ("T13", "classification/PREREG_t13.md", "classification/t13/RESULTS_t13.md", "first"),
    ("T14", "classification/PREREG_t14.md", "classification/t14/RESULTS_t14.md", "first"),
]
NOTE = {"T4": "Exploratory by pre-registration (outcomes reported either way; no pass/fail criteria).",
        "T5": "The report itself (`verification/REPORT.md`); no pass/fail criteria."}
FAILURES = {
    "T6": ["C5 (peak locations to 3 s.f. against Task 4b): criterion — Task 4b located peaks on a grid of about 0.4 % steps; "
           "heights all match, three locations differ in the third figure."],
    "T9": ["T9.2 ARE route: criterion — the regularised ARE converges as √ε with a large prefactor; mp ARE and the closed-form "
           "Wiener filter match the document.",
           "T9.5 monotonicity and ordering: criterion — float64 resolution; 0 of 285 and 0 of 13 flags are real at higher precision."],
    "T10": ["T10.1 symbolic (2 items): criterion / route — no √(square) handling in the pre-registered SymPy route; identities hold.",
            "T10.2 A1.3 as specified: plan's construction (criterion as pre-registered); the supplementary construction passes.",
            "T10.5 pair birth: criterion.", "T10.6 matched-variance τ (zero-limit shape check): criterion."],
    "T11": ["T11.3 classes: criterion — the pre-registered limits/brackets at β ≥ 2."],
    "T12": ["Symbolic A5 (D2 post at Δt → ∞): code — the SymPy check route (`sympy.limit`); the series route confirms.",
            "A7 minimum below F and two rays: criterion — the zero tolerance is too coarse for the prior dip.",
            "A8 qualitative regression: prediction — the prompt's quick-check numbers."],
    "T13": ["Part A symbolic (2 of 68 items): criterion / route — identities verified by a post-hoc rewrite route.",
            "A2 numerical (auxiliary cross-check, 277 sets): code — precision loss; all agree at higher precision.",
            "C1 numbers, first run: document (4, a truncated worked value) and code (2, parser); passes after the fixes.",
            "C2 classes, row 8: document — the stated class (1,0,1) cannot occur (proved; class set corrected).",
            "C2 classes, row 12: code — route (ii) sample point below its equality tolerance at an exact limit.",
            "D reproduction, Task 10: code — `run_t10.sh` omits `t10_realize_diag.py`; Task 12: criterion — masking of the provenance runtime list."],
    "T14": ["C4 paper render reproduces v1: criterion — the register types the excess identity as a Corollary (accepted in Task 15).",
            "C9 bibliography: input / criterion — two entries unattached and DOIs unresolvable from the session; resolved by the "
            "Task 15 input (verified bib, attachments).",
            "C10 reproduction: code — the dry-run resolver; all 9 flagged paths resolve as their scripts build them."],
}


def rows(path, sel):
    L = open(os.path.join(REPO, path)).read().split("\n")
    if sel == "first":
        i = next(i for i, l in enumerate(L) if l.startswith("|") and ("Verdict" in l or "verdict" in l or "Result" in l))
        out = []
        for l in L[i + 2:]:
            if not l.startswith("|"):
                break
            out.append(l)
        return out
    if sel == "T6":
        s = "\n".join(L).split("## Task 6")[1].split("## Task 7")[0].split("\n")
        return [l for l in s if re.match(r"^\| C\d", l)]
    return [l for l in L if re.match(sel, l)]


def verdict(l):
    return "FAIL" if re.search(r"\bFAIL\b", l) else ("PASS" if re.search(r"\bPASS\b", l) else None)


def appendix_d(with_t15=False):
    tasks = list(TASKS)
    if with_t15:
        tasks.append(("T15", "classification/PREREG_t15.md", "classification/RESULTS_t15.md", "first"))
    out = ["# Appendix D. Verification record, Tasks 1–" + ("15" if with_t15 else "14"), "",
           "One section per task: the pre-registration and results files, the number of pre-registered checks that passed and "
           "failed (read from each report's check table), and every failure with the attribution its report gives. Outcomes are "
           "copied from the reports, not re-judged. Every failure stays recorded as a failure.", ""]
    for t, pre, res, sel in tasks:
        out += [f"## {t}", "", f"- Pre-registration: `{pre}`", f"- Results: `{res}`"]
        if sel is None:
            out += [f"- Checks: {NOTE[t]}", ""]
            continue
        v = [verdict(l) for l in rows(res, sel)]
        v = [x for x in v if x]
        n_p, n_f = v.count("PASS"), v.count("FAIL")
        out.append(f"- Checks: {n_p + n_f} with a verdict; {n_p} pass, {n_f} fail.")
        fl = FAILURES.get(t, [])
        if with_t15 and t == "T15":
            fl = FAILURES_T15
        out += [f"- Failure: {x}" for x in fl] if fl else ["- Failures: none."]
        out.append("")
    return "\n".join(out)


FAILURES_T15 = [  # from RESULTS_t15.md (recorded run on 41d5e43)
    "C4 [n] rendering: criterion / code — the pre-registered bracket pattern flags the interval '[0, 10]' in the Appendix B "
    "description of Figure B.1; it is not a citation, and no unresolved citation remains.",
    "C10 thesis phrase check: criterion — all 81 A–E matches are Task 15's figure labels B.1–B.12, which coincide in form with "
    "the legacy labels the pattern targets; 0 'Paper 1', no legacy label remains."]


def appendix_e():
    pk = {}
    for p in ("numpy", "scipy", "sympy", "mpmath", "matplotlib", "PyYAML"):
        try:
            pk[p] = md.version(p)
        except md.PackageNotFoundError:
            pk[p] = "not installed"
    out = ["# Appendix E. Reproduction", "",
           "## Environment", "", f"- Python {platform.python_version()} on {platform.platform()}",
           "- Packages (from the installed environment, `importlib.metadata`; the repository has no lockfile): "
           + ", ".join(f"{k} {v}" for k, v in pk.items()) + ".",
           "- Tasks 1–7 record their own environment in `verification/results/env.json`; Tasks 8–13 in each task's "
           "`results/env.json`.", "",
           "## Commands, task by task", "",
           "All commands run from the repository root unless stated.", "",
           "| Task | What it regenerates | Command |", "|---|---|---|",
           "| T1–T7 | starting-study checks, simulations, figures, `verification/REPORT.md` | `cd verification && bash run_all.sh` |",
           "| T8 | Stage 0–1 checks, figure, `classification/REPORT.md` | `cd classification && bash run_all.sh` |",
           "| T9 | Stage 2 τ sweep, `t9/RESULTS_t9.md` | `cd classification && bash t9/run_t9.sh` |",
           "| T10 | Stage 3 checks, figures, `t10/RESULTS_t10.md` | `cd classification && bash t10/run_t10.sh` "
           "(then `python3 t10/t10_realize_diag.py`, which the run script omits; see Task 13) |",
           "| T11 | Stage 4 checks, figures, `t11/RESULTS_t11.md` | `cd classification && bash t11/run_t11.sh` |",
           "| T12 | Δt and Σ sweeps, figures, `t12/RESULTS_t12.md` | `cd classification && bash t12/run_t12.sh` |",
           "| T13 | open items, audits, Paper 2 figures, `t13/RESULTS_t13.md` | `cd classification && bash t13/run_t13.sh` |",
           "| T8–T13 at once | clean checkout, manifest | `bash classification/reproduce_all.sh WORKDIR 8 9 10 11 12 13` |",
           "| T14 | register, sources, renders, bibliography check | see the render chain below |",
           "| T15 | figures B.n, appendices, renders, checks | see the render chain below |",
           "| T16 | register fixes, renders, checks D1–D8 | render chain below, then `python3 t16/t16_checks.py` |", "",
           "## The T14–T16 render chain", "", "From `classification/`:", "", "```",
           "python3 t14/build_register.py          # register from the T14 table (T14; overwrites T15 metadata, re-apply next line)",
           "python3 t15/t15_register.py            # T15 citations/status, references.yaml, figures.yaml",
           "python3 t16/t16_register.py            # T16 legacy-label prefixes, crosswalk, result 5.6 wording, B.4 Pi_c",
           "python3 t15/make_figs_thesis.py        # figures B.1, B.3-B.12 (text-only edits) and B.2",
           "python3 register/render.py --numbering thesis   # Stages_0_4_Thesis.md, Roadmap_v3.md, figs_thesis/*.txt, Appendices A-C, reference/phase1/",
           "python3 register/render.py --numbering paper    # Stages_0_4_Paper2.md",
           "python3 t15/make_appendix_de.py        # Appendices D and E",
           "python3 t15/t15_checks.py && python3 t15/t15_partG.py   # Task 15 checks",
           "```", "",
           "The sources were derived once from the Task 14 versions by `t14/make_source.py`, `t14/make_roadmap_source.py` and "
           "`t15/make_sources_t15.py`; they are now edited directly and are not regenerated by this chain.", ""]
    return "\n".join(out)


def main():
    with_t15 = "--with-t15" in sys.argv
    open(os.path.join(CLS, "Appendix_D_Verification.md"), "w").write(appendix_d(with_t15))
    open(os.path.join(CLS, "Appendix_E_Reproduction.md"), "w").write(appendix_e())
    print("appendices D and E written")


if __name__ == "__main__":
    main()
