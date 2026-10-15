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
    ("T15", "classification/PREREG_t15.md", "classification/RESULTS_t15.md", "first"),
    ("T16", "classification/PREREG_t16.md", "classification/RESULTS_t16.md", "first"),
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
    "T15": ["C4 [n] rendering: criterion / code — the pre-registered bracket pattern flags the interval '[0, 10]' in the "
            "Appendix B description of Figure B.1; it is not a citation, and no unresolved citation remains.",
            "C10 thesis phrase check: criterion — all 81 A–E matches are Task 15's figure labels B.1–B.12, which coincide in form with "
            "the legacy labels the pattern targets; 0 'Paper 1', no legacy label remains."],
    # Task 16: the wording of the thesis draft's Appendix D (t17/input/Thesis_Draft_ch1-7.md), attributions as RESULTS_t16.md
    "T16": ["D1 new proof steps of the thesis draft (2 of 9 items): code — SymPy could not decide a sign and could not denest a "
            "square root of a square; both items hold (post-hoc diagnosis).",
            "D2 statements against the repository: document / criterion — four statements differ in content: 3.1 and 3.5 gather "
            "conclusions the repository states in other results (verified in D1), and the §2.5 table rows for 2.5 and 2.7 left out "
            "hypotheses (full statements were then added to the thesis).",
            "D6 legacy labels: criterion / document — three hits, none a legacy label: two figure labels in Appendix E outside the "
            "exemption window, and a quotation in Appendix D."],
}


# Task 20: non-failure lines, emitted after a task's failure bullets as "- Recorded — …" (not counted as checks or failures)
NOTES = {
    "T13": ["A3 (Theorem 7.15): the pre-registered resultant route, completed post hoc in exact arithmetic (`t13/t13_A3_proof.py`, 22 of 22 checks; the pre-registered attempt `t13_A3_attempt.py` reported 'unresolved'): the resultant of the cleared quadratic and its x-derivative is 4u²x²(u + 1)²(E − 1)⁴(E² + 2xE − 1)², and E² + 2xE − 1 = −2e^(−x)(sinh x − x) < 0 on E = e^(−x), so dp/dx never vanishes."],
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


def appendix_d(with_t17=False):
    """Appendix D in the thesis draft's layout (Task 17, Part B.4): one paragraph per task, failures as bullets."""
    tasks = list(TASKS)
    if with_t17:
        tasks.append(("T17", "classification/PREREG_t17.md", "classification/RESULTS_t17.md", "first"))
    if with_t17 in ("t18", "t19"):
        tasks.append(("T18", "classification/PREREG_t18.md", "classification/RESULTS_t18.md", "first"))
    if with_t17 == "t19":
        tasks.append(("T19", "classification/PREREG_t19.md", "classification/RESULTS_t19.md", "first"))
    last = tasks[-1][0][1:]
    out = [f"# Appendix D. Verification record, Tasks 1–{last}", "",
           "For each task: the pre-registration and results files, the pre-registered checks that passed and failed, and every "
           "failure with the attribution its report gives (criterion, input, code, document or prediction). Outcomes are copied "
           "from the reports, not re-judged, and every failure stays recorded.", ""]
    for t, pre, res, sel in tasks:
        head = f"**Task {t[1:]}.** {pre} · {res}."
        if sel is None:
            out += [f"{head} {NOTE[t]}", ""]
            continue
        v = [verdict(l) for l in rows(res, sel)]
        v = [x for x in v if x]
        n_p, n_f = v.count("PASS"), v.count("FAIL")
        out += [f"{head} {n_p + n_f} checks with a verdict; {n_p} pass, {n_f} fail.", ""]
        fl = {"T17": FAILURES_T17, "T18": FAILURES_T18, "T19": FAILURES_T19}.get(t, FAILURES.get(t, []))
        nl = NOTES.get(t, [])
        if fl or nl:
            out += [f"- Failure — {x}" for x in fl] + [f"- Recorded — {x}" for x in nl] + [""]
    return "\n".join(out)


FAILURES_T19 = [  # from RESULTS_t19.md (recorded run on 8cb8777); planned post-run entry (PREREG_t19.md)
    "G1 citations: input — Roberts (1959) unreachable from the session; that it states r/(2 − r) cannot be determined from its text "
    "(secondary sources agree); the §6.3 identity, [29], [40] and both [21] sentences hold.",
    "G3 chapter 8: code / document — the coverage parser missed two Appendix D lines (both covered); §8.2 interchanges the route "
    "descriptions; §8.4 lists Task 13 under √(x²) handling, which Task 13's report does not support. Recount 151 / 32 and §8.5 match.",
    "G4 chapter 9: document — §9.2's c/(FΠ₀) > 4 for the Hill gain holds for n = 2 only.",
    "G7 sync: criterion / code — the old key remains in ten recorded files of Tasks 14, 15 and 17 (not editable) and in Task 19's "
    "register script's docstring; 0 in live files; the other three clauses hold.",
    "H-13.C2-12 C2 row 12 re-check: criterion — 45 persisting cases; the 10⁻³⁰⁰ tolerance is finer than the stored limit's precision "
    "(about 10⁻²⁵), so the routes compare below what the critical value carries."]
FAILURES_T18 = [  # from RESULTS_t18.md (recorded run on f77ab8f)
    "F1 Task 17 fixes (2 of 6): code / document — the [47] search included Appendix D's quotation of the old finding (both chapter "
    "sentences now say model error); §1.6 still cites [21–23] for monotonicity under garbling (fixed in §7.1 only).",
    "F2 chapter 8 counts: code — the recount parser skipped Task 2's 'PASS (info)' row (143); read as pre-registered the total is "
    "144, with 28 failed and Tasks 4 and 5 without criteria.",
    "F3 chapter 8 claims: document — §8.5 names a referee pass on Theorem 7.6 only; Task 13 C4's independent referee read the whole "
    "consolidated document (14 points, all fixed).",
    "F6 appendices: code / document — Appendix A differs only in math delimiters; the draft's Appendix D rewords three Task 17 "
    "failure lines (tense, P⁻ for M, 'the proof was completed')."]
FAILURES_T17 = [  # from RESULTS_t17.md (recorded run on 81e977c)
    "E1 new proof steps of the thesis draft (2 of 9 items): code / document — the 50-digit test of the optimal prior M < F "
    "(Proposition 6.13) cannot resolve it when e^(−2λΔt) < 10⁻⁵⁰ (it holds exactly, f(F) = F²a² > 0); Corollary 7.4's proof as "
    "written omits σ⋆² → 0 and Theorem 5.1 (the corollary holds).",
    "E3 numbers (1 of 88): document — \"37 values of β\" for Theorem 7.8, in the repository's label and the draft; Task 11 ran 129.",
    "E4 cross-references: document — \"Prop. 6.10–6.12\" spans Counterexample 6.11.",
    "E5 prior-work sentences: document — §7.3 makes [47] an analysis of coloured measurement noise; it studies time-correlated "
    "model error (2 sentences undetermined: no abstracts reachable from the session)."]


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
           "| T16 | register fixes, renders, checks D1–D8 | render chain below, then `python3 t16/t16_checks.py` |",
           "| T17 | thesis-only imports, renders, checks E1–E7 | render chain below, then `python3 t17/t17_checks.py` |",
           "| T18 | record corrections, Theorem 2.2 import, archived thesis, checks F1–F7 | render chain below, then "
           "`python3 t18/t18_checks.py` |",
           "| T19 | reference 26, Theorem 2.2 import, open problems 5–6, archived thesis, checks G1–G7 and re-checks H-* | render "
           "chain below, then `python3 t19/t19_checks.py`, `python3 t19/t19_routes.py` and `python3 t19/h13d_replay.py` |",
           "| T20 | register sync with the thesis (titles, 8.1/8.2, Lemma 7.6a, references 54–60, Appendix D note, figures B.5/B.6), "
           "checks C1–C6 | render chain below, then `python3 t20/t20_checks.py` |", "",
           "## The T14–T19 render chain", "", "From `classification/`:", "", "```",
           "python3 t14/build_register.py          # register from the T14 table (T14; overwrites T15 metadata, re-apply next line)",
           "python3 t15/t15_register.py            # T15 citations/status, references.yaml, figures.yaml",
           "python3 t16/t16_register.py            # T16 legacy-label prefixes, crosswalk, result 5.6 wording, B.4 Pi_c",
           "python3 t19/t19_register.py            # T19 reference 26: key roberts1959 in references.yaml and results.yaml",
           "python3 t20/t20_register.py            # T20 titles, 8.1/8.2, Lemma 7.6a, references 54-60, crosswalk",
           "python3 t17/make_thesis_only_t17.py    # T17 thesis-only imports (placed by register/thesis_overrides.yaml)",
           "python3 t18/make_thesis_only_t18.py    # T18 thesis-only Theorem 2.2 (parts (1)-(4))",
           "python3 t19/make_thesis_only_t19.py    # T19 Theorem 2.2 with the proof's closing sentences (replaces T18's file)",
           "python3 t15/make_figs_thesis.py        # figures B.1, B.3-B.12 (text-only edits) and B.2",
           "python3 register/render.py --numbering thesis   # Stages_0_4_Thesis.md, Roadmap_v3.md, figs_thesis/*.txt, Appendices A-C, reference/phase1/",
           "python3 register/render.py --numbering paper    # Stages_0_4_Paper2.md",
           "python3 t15/make_appendix_de.py --with-t19   # Appendices D (Tasks 1-19) and E",
           "python3 t15/t15_checks.py && python3 t15/t15_partG.py   # Task 15 checks",
           "```", "",
           "The sources were derived once from the Task 14 versions by `t14/make_source.py`, `t14/make_roadmap_source.py` and "
           "`t15/make_sources_t15.py`; they are now edited directly and are not regenerated by this chain.", ""]
    return "\n".join(out)


def main():
    flag = "t19" if "--with-t19" in sys.argv else ("t18" if "--with-t18" in sys.argv else ("--with-t17" in sys.argv))
    open(os.path.join(CLS, "Appendix_D_Verification.md"), "w").write(appendix_d(flag))
    open(os.path.join(CLS, "Appendix_E_Reproduction.md"), "w").write(appendix_e())
    print("appendices D and E written")


if __name__ == "__main__":
    main()
