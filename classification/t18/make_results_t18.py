"""Build classification/RESULTS_t18.md from the recorded Task 18 outputs. Usage: python3 make_results_t18.py RESULTS_COMMIT"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
R = os.path.join(HERE, "results")


def V(ok):
    return "**PASS**" if ok else "**FAIL**"


def rd(f):
    return open(os.path.join(R, f)).read()


def main():
    rc = sys.argv[1] if len(sys.argv) > 1 else "(results commit)"
    C = json.load(open(os.path.join(R, "t18_checks.json")))
    G = json.load(open(os.path.join(R, "t18_diag.json")))
    sha = hashlib.sha256(open(os.path.join(REPO, "thesis", "Thesis_Draft_full.md"), "rb").read()).hexdigest()
    f1, f2, f5, f6, f7 = C["F1"], C["F2"], C["F5"], C["F6"], C["F7"]
    fixes = {k: v["resolved"] for k, v in f1.items() if isinstance(v, dict) and "resolved" in v}
    names = {"cor_7_4": "Corollary 7.4's proof", "beta": "β count", "s67_label": "§6.7 label", "s47": "[47] sentences",
             "s21": "[21] sentence", "p613": "Proposition 6.13's P⁻ < F"}
    f2_pass, f3_pass, f4_pass = False, False, True     # from f2_examples.md, f3_claims.md, f4_claims.md (manual readings)
    t = ["# Results — Task 18: final collection (chapters 8–9, the Task 17 fixes, last open items, archive)", "",
         "- Pre-registration: `classification/PREREG_t18.md`, commit **97e1889**.",
         f"- Artifacts checked: commit **{C['commit']}**. F1–F7 ran once on it (8 s; `t18/results/t18_checks.log`, `.time`).",
         f"- Results: raw outputs **1beb7d6**; manual readings, diagnosis and `OPEN_ITEMS.md` **{rc}**; this report follows.",
         f"- Archived thesis: `thesis/Thesis_Draft_full.md`, sha256 **{sha}** (byte-identical to the input).", "",
         "## Checks", "", "| Check | Verdict | Details | Runtime (s) |", "|---|---|---|---|",
         f"| F1 Task 17 fixes (A1) | {V(f1['pass'])} | {sum(fixes.values())} of 6 resolved in the recorded run: "
         + ", ".join(f"{names[k]} {'resolved' if v else '**not resolved**'}" for k, v in fixes.items())
         + f"; f(F) − F²a² reduces to 0 | {f1['seconds']} |",
         f"| F2 Chapter 8 counts (A2) | {V(f2_pass)} | recorded recount {f2['total']} checks, {f2['failed']} failed, no criteria "
         f"{f2['no_criteria']}; 144 when Task 2's 'PASS (info)' row is read as the rule says (code); every §8.4 example a real failure of "
         f"the named task; every Appendix D failure maps | {f2['seconds']} |",
         f"| F3 Chapter 8 claims (A2) | {V(f3_pass)} | §8.2 matches (one persistent disagreement: Task 13 audit row 12, route (ii)); "
         f"§8.5 does not (Task 13 C4's referee read the whole document) | {C['F3']['seconds']} |",
         f"| F4 Chapter 9 claims (A3) | {V(f4_pass)} | 25 claims, each sourced and matching; notes on the Hill gain and on open problems "
         f"5–6 (not in the repository's §11) | {C['F4']['seconds']} |",
         f"| F5 Mechanical (A4) | {V(f5['pass'])} | {f5['citation_groups']} citation groups, 0 unresolved, order [1]–[53] holds; "
         f"{f5['typed_refs']} typed references, 0 wrong; {f5['figure_refs']} figure references; {f5['task_refs']} task and "
         f"{f5['check_refs']} check references, 0 nonexistent | {f5['seconds']} |",
         f"| F6 Appendices (B.5) | {V(f6['pass'])} | records A {f6['A']['draft_records']}/{f6['A']['render_records']} "
         f"({len(f6['A']['differences'])} difference), C {f6['C']['draft_records']}/{f6['C']['render_records']} "
         f"({len(f6['C']['differences'])}), D {f6['D']['draft_records']}/{f6['D']['render_records']} ({len(f6['D']['differences'])}) "
         f"| {f6['seconds']} |",
         f"| F7 Thesis render consistency (B.3) | {V(f7['pass'])} | 0 lettered references to Theorem 2.2 | {f7['seconds']} |", "",
         "**Pre-registered checks that FAIL:** F1, F2, F3, F6. Each stays a failure; diagnoses below.", "",
         "## Diagnoses", "",
         "- **F1 (attribution: code and document).** [47]: the recorded search for sentences citing [47] ran over the whole draft and "
         "picked up Appendix D's quotation of the Task 17 finding; restricted to chapters 1–9, both sentences (§6.2, §7.3) say "
         "\"time-correlated model error\" (`t18_diag.json`; code). [21]: §7.1 now cites [21] for observation channels as design "
         "variables, but §1.6 (line 85) still says monotonicity under garbling \"extends to sequential experiments [20] and "
         "stochastic control and teams [21–23]\" (document; not resolved). The other four fixes are resolved, and f(F) = F²a² "
         "reduces to 0 by `simplify`, with 0 of 1,000 counterexamples to M < F at up to 39,399 digits (seed 18001).",
         "- **F2 (attribution: code).** The recount parser required a verdict cell equal to \"PASS\" and skipped Task 2's T2.1c "
         "(\"PASS (info)\"), giving 143. The pre-registered rule counts cells that say PASS or FAIL; so read, the total is 144, with "
         "28 failed and Tasks 4 and 5 without criteria, as the draft says. The §8.4 mapping holds (`f2_examples.md`).",
         "- **F3 (attribution: document).** §8.5 says the only referee pass was on Theorem 7.6 (Task 13). The record is an "
         "independent referee pass (a separate agent, inside the project) over the whole consolidated Stages 0–4 document, 14 "
         "points, all valid and fixed (`t13/referee_report.md`, RESULTS_t13 C4); Theorem 7.6 was among the results read. This was "
         "known from the inventory and disclosed in the pre-registration (disclosure 3).",
         "- **F6 (attribution: code and document).** Appendix A: one row differs only by math delimiters (\"$n = 2$\" vs \"n = 2\"), "
         "formatting the normaliser did not strip (code). Appendix D: the draft rewrote three Task 17 failure lines after the fixes "
         "(\"omits\" → \"omitted … (the corollary holds; the proof was completed)\", \"M < F\" → \"P⁻ < F\", \"spans\" → \"spanned\", "
         "\"makes\" → \"made\"); the repository's lines are the record as written at Task 17 (document). Appendix C: all 53 entries match.",
         "", "## Disclosure", "",
         "- Before the recorded run each check was run once with its output discarded, to see that it ran, and F6's parsers and F4's "
         "extractions were checked to find records on both sides. No code was changed after that.",
         "- The Task 13 referee record (F3) was read while taking stock, before the pre-registration (disclosure 3).",
         "- While building Part B.3, `register/render.py`'s block rule was widened so that a multi-paragraph statement (Theorem 2.2's) "
         "is replaced through its proof; the Task 17 overrides render unchanged.",
         "- F2's §8.4 mapping, F3, F4 and A5 are manual readings after the recorded run (`t18/results/`).", "",
         "## Files changed", "",
         "- `source/Stages_0_4_Source.md`: Theorem 7.8's label, \"37 values of β\" → \"129 values of β (β = k/20, k = −40, …, 80, plus "
         "{0, 2} ± {10⁻⁶, 10⁻³})\" (record correction); Proposition 2.7's proof, (4/3)a(bδ)^(3/2) → (4/3)|a|(bδ)^(3/2) "
         "(documentation fix).",
         "- New `source/thesis_only/critical-tolerance.md` (the draft's Theorem 2.2, parts (1)–(4)); `register/thesis_overrides.yaml` "
         "(replace critical-tolerance); `register/render.py` (block rule through the proof).",
         "- New `thesis/Thesis_Draft_full.md` (archive, not rendered).",
         "- Renders: `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (the β label and |a|), `Appendix_A_Register.md`, "
         "`Appendix_C_References.md` (unchanged by this task), `Appendix_D_Verification.md` (Tasks 1–18), `Appendix_E_Reproduction.md` "
         "(T18 row, chain step).",
         "- `t15/make_appendix_de.py` (T18 entry, chain); new `t18/` scripts, inputs and results; `OPEN_ITEMS.md`.", "",
         "## For the author", "", "### 1. A1: the Task 17 fixes", "", "| Fix | Verdict | Evidence |", "|---|---|---|",
         "| Corollary 7.4's proof | resolved | cites σ⋆² = 2Σ/(λ + √(λ² + 2ΣΠ)) → 0 (Proposition 3.5) to exclude All, and Theorem 5.1 for the last clause; SymPy limit 0 |",
         "| β count | resolved | the draft says 129; `t11_3.json` has 129 distinct β. The repository's label is corrected in Part B.1 |",
         "| §6.7 label | resolved | \"Prop. 6.10, Cex. 6.11, Prop. 6.12\": types match the register |",
         "| [47] sentences | resolved (post hoc) | §6.2 and §7.3 both say \"mis-specified time-correlated model error\"; the recorded sub-check failed on scope (code) |",
         "| [21] sentence | **not resolved** | §7.1 is fixed (\"where observation channels are also treated as design variables [21]\"); §1.6 still cites [21–23] for monotonicity under garbling |",
         "| Proposition 6.13's P⁻ < F | resolved | the proof now states f(F) = F²a² > 0; f(F) − F²a² reduces to 0; f is monic with f(0) = −sFr < 0; numerical: 0 of 1,000 |",
         "", "### 2. A2: chapter 8 counts", "", "| Task | Checks with a verdict | Failed |", "|---|---|---|"]
    per = G["F2_qualified_verdicts"]["per_task"]
    for n in range(1, 18):
        fails = f2["per_task"][str(n)]["fail"]
        t.append(f"| {n} | {per[str(n)]} | {fails} |")
    t += [f"| **Total** | **{sum(per.values())}** (143 if T2.1c's \"PASS (info)\" is excluded) | **{f2['failed']}** |", "",
          "Tasks 4 and 5 have no pass criteria. Corrections chapter 8 may need:",
          "- §8.4, \"Code\" row: T10's and T13's SymPy failures and T9.5's double-precision flags are attributed to the criterion "
          "(\"criterion / route\", \"criterion\") in their reports, not to code.",
          "- §8.4, \"four truncated worked values (T13)\": Task 13 records four occurrences of one truncated value (0.0099504 for 0.0099505).",
          "- §8.5: the Task 13 referee pass covered the whole consolidated document (14 points), not only Theorem 7.6.",
          "- §8.2 is correct.", "", "### 3. A3: chapter 9", ""]
    f4 = rd("f4_claims.md")
    i = f4.index("| # |")
    t += [f4[i:].strip(), "", "### 4. A4: references", "",
          f"No broken reference: {f5['citation_groups']} citation groups resolve and [1]–[53] first appear in order; "
          f"{f5['typed_refs']} typed references (with \"Cex.\") have the right type; {f5['figure_refs']} figure references exist; "
          f"{f5['task_refs']} \"Task n\" and {f5['check_refs']} \"Tn.m\"/\"Tn X\" references name existing tasks and checks.", "",
          "### 5. A5: [26] and [29]", ""]
    a5 = rd("a5_sources.md")
    t += [a5[a5.index("**Access.**"):].strip(), "", "### 6. Part B: what changed in the repository", "",
          "- Theorem 7.8's label now says 129 values of β, with the composition of `PREREG_t11.md`.",
          "- Proposition 2.7's proof (repository source, paper render) now has (4/3)|a|(bδ)^(3/2), matching the thesis text.",
          "- The thesis render's Theorem 2.2 is the draft's, with parts (1)–(4); no lettered reference to it remains (F7). Note: the "
          "draft's proof of Theorem 2.2 does not include the closing sentences the Task 13 referee (point 10) added to the "
          "repository's proof (the rule at a tolerance equal to an interior turning-point value; approach directions determined by "
          "the sequence). The thesis render now shows the draft's proof; the paper render keeps the repository's.",
          f"- `thesis/Thesis_Draft_full.md` archived (sha256 {sha}).",
          "- Appendices A, C, D (Tasks 1–18) and E (Task 18 row and chain step) re-rendered. Their introductions differ from the "
          "draft's, which is not a record difference; one is stale: the render's Appendix C introduction still says references "
          "[46]–[53] \"are cited in chapters 5–9, still to be drafted\" (Task 15 wording), while the draft says \"first cited in chapters 6–7\".",
          "", "### 7. The closing inventory (`OPEN_ITEMS.md`)", "", open(os.path.join(CLS, "OPEN_ITEMS.md")).read().split("\n", 2)[2].strip(), ""]
    open(os.path.join(CLS, "RESULTS_t18.md"), "w").write("\n".join(t))
    print("written")


if __name__ == "__main__":
    main()
