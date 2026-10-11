"""Build t14/RESULTS_t14.md from results/*.json. Usage: python3 make_results_t14.py RESULTS_COMMIT"""
import json
import os
import sys

from t14_common import HERE, PREREG, RES

ARTIFACTS = "45b0058"


def L(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


def V(ok):
    return "**PASS**" if ok else "**FAIL**"


def main():
    commit = sys.argv[1] if len(sys.argv) > 1 else "(this commit)"
    C, G, inv, d10 = L("t14_checks.json"), L("t14_partG.json"), L("t14_inventory.json"), L("t14_c10_diag.json")
    c4 = C["C4"]
    T = ["# Task 14: thesis numbering, Phase 1 roll-in, matrix fix and bibliography (results)", "",
         f"- Pre-registration: `classification/PREREG_t14.md`, commit **{PREREG}**.",
         f"- Artifacts as checked: commit **{ARTIFACTS}**. The single recorded run of C1–C10 ran on this commit.",
         f"- Results and diagnoses: commit **{commit}**.",
         "- Python 3, PyYAML, SymPy, mpmath.", "",
         "## Check table", "", "| Check | Verdict | Counts / details | Runtime (s) |", "|---|---|---|---|"]
    rows = [
        ("C1 Register integrity", C["C1"]["pass"], f"{C['C1']['n_entries']} entries; keys unique and well-formed; thesis numbers unique and contiguous in chapters 2–8; v1 numbers 1–73 all mapped; {C['C1']['legacy_labels_in_table']} legacy A–E labels, 0 unmapped"),
        ("C2 Reference resolution", C["C2"]["pass"], f"{C['C2']['tokens']} tokens, {C['C2']['keys_referenced']} keys referenced; 0 unresolved, 0 unreferenced (thesis-only exempt). Tokens without a heading: paper render {len(C['C2']['headless_in_paper_render'])}; thesis render {len(C['C2']['headless_in_thesis_render (cited by thesis number)'])} ({', '.join(C['C2']['headless_in_thesis_render (cited by thesis number)'])}), all cited by thesis number only"),
        ("C3 No hand-typed numbers", C["C3"]["pass"], f"{C['C3']['matches_in_sources']} matches in the sources (phase1 sources, reported only: {C['C3']['phase1_sources_matches']})"),
        ("C4 Paper render reproduces v1", c4["pass"], f"numbering shift exact (0 mismatches); {c4['hunks']} differing hunks: {c4['by_category']['b (split)']} split, {c4['by_category']['c (rows 25-26)']} rows 25–26, {c4['by_category']['other']} other, all the pre-disclosed type change of the excess identity"),
        ("C5 Thesis render", C["C5"]["pass"], f"{C['C5']['files']} files; 0 'Paper 1', 0 A–E labels"),
        ("C6 Matrix identity", C["C6"]["pass"], f"thesis and Roadmap tables byte-identical ({C['C6']['n_lines']} lines); rows 25–26 exact"),
        ("C7 Errata value", C["C7"]["pass"], f"m = {C['C7']['m_8sf']} (8 s.f.) at Π = {C['C7']['Pi_at_min']}; 5 s.f. {C['C7']['m_5sf']}"),
        ("C8 Phase 1 records", C["C8"]["pass"], "all six Task 1–7 hashes exist: " + ", ".join(C["C8"]["hashes"])),
        ("C9 Bibliography", C["C9"]["pass"], f"{C['C9']['entries']} entries; 0 dangling; unused {C['C9']['unused']}; {C['C9']['doi_entries']} DOI entries, {C['C9']['doi_resolved']} resolved (doi.org blocked), all marked VERIFY"),
        ("C10 Reproduction unaffected", C["C10"]["pass"], f"{C['C10']['checked']} paths checked; {len(C['C10']['missing'])} flagged; diagnosis: {d10['text'] if d10 else ''}"),
        ("Part G (3.2 and 6.5)", G["pass"], f"G1–G6 all reduce to 0; G6 at 20 rational points max abs. difference {G['G6 numeric 20 rational points (max |diff|)']}"),
    ]
    for (name, ok, txt), key in zip(rows, ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", None]):
        T.append(f"| {name} | {V(ok)} | {txt} | {C[key]['seconds'] if key else ''} |")
    fails = [r[0] for r in rows if not r[1]]
    T += ["", f"**Pre-registered checks that FAIL:** {'; '.join(fails)}. Each is diagnosed below; no criterion was changed and no "
          "artifact was changed after the recorded run.", ""]
    T += ["## Plain statements", "",
          "- **Did any mathematical content change?** No. The paper render differs from the consolidated v1 only as follows:",
          "  - numbers shift by one for v1 numbers 7 and above;",
          "  - the window theorem's addendum is split out (same text; the lead-in becomes \"In the setting of …\", and \"Proof of "
          "the addendum\" becomes \"Proof\");",
          "  - matrix rows 25–26 use the prescribed wording, which has the same content as v1;",
          "  - the excess identity is printed as a Corollary instead of a Proposition, as the register types it.",
          "  The thesis render differs from the paper render only in numbers, the `{{phase1}}` phrase, and the conditional "
          "passages listed in the source. No mathematical error was found.",
          "- **What still needs a human decision?**",
          "  1. The excess identity is typed Corollary in the register and was Proposition in v1. This is why C4 fails as worded. "
          "Accept the type change for the Paper 2 render, or give the register a separate paper type.",
          "  2. `jazwinski1970` and `simon2006` are in the prompt's entry list but not in its attachment table, so C9 fails on "
          "them. Attach them to a result, or drop them.",
          "  3. Roadmap §7, query rows for clusters 11–17: the second search set's query text and its clustering were not supplied. "
          "The rows give a topic and the bib keys grouped under it, marked \"query text not supplied\". Confirm or replace "
          "them.",
          "  4. The images of fig01 (axis title) and fig06 (legend) carry v1 numbers (Theorem 2, Theorem 25). `figs_paper2/` was "
          "left untouched. The thesis captions in `figs_thesis/` link these images and say so. Regenerating the images needs a "
          "decision on how their labels are numbered.",
          "  5. 34 bibliography entries carry `VERIFY` notes (listed below). No DOI could be resolved, because doi.org is blocked "
          "from this session.",
          "  6. The starting-study manuscript was supplied mid-task as a PDF only, with no LaTeX source. It was added unchanged; "
          "since it was never in the repository, no history could be kept.",
          "  7. The thesis-only results (2.3, 2.8, 2.9, 3.2, 6.5) have no text in the repository. Part G checked 3.2 and 6.5 in the "
          "reading ν = 2ΣΠ/λ², q = G/(FΠ), t = λτ, and both hold in that reading. Results 3.1, 3.5 and 6.13 have no heading in the "
          "consolidated document; the thesis render cites them by number, and their statements are in the manuscript.",
          "  8. The prompt's CSV row for 3.2 had an unquoted comma in its title (`V(ν,q)`). The input copy "
          "(`t14/input/register_table.csv`) quotes it; nothing else was changed.", ""]
    T += ["## Diagnoses", "",
          "1. **C4 (attribution: criterion).** All 7 \"other\" hunks are the excess identity's type, printed from the register: "
          "its heading, its label line, the §12 row, the v1 number-map row, and three references (\"Proposition 4\" → "
          "\"Corollary 4\"). The pre-registration predicted this (disclosure item 4). The numbering check passed: every key's "
          "paper number is its v1 number, +1 for 7 and above, and the split result is 7. There is no other difference.",
          "2. **C9 (attribution: input/criterion).** `jazwinski1970` and `simon2006` are not attached to any result in the "
          "prompt's citation table, and no source cites them. Every DOI entry is marked VERIFY because doi.org is unreachable "
          "(proxy CONNECT 403, every DOI).",
          "3. **C10 (attribution: code).** The pre-registered dry run resolved string literals only against `classification/`, "
          "the script's directory and the repository root.",
          "   - It flagged 9 literals. In `t14_c10_diag.py` each was resolved the way its script builds the path:",
          "     - the two Task 13 audit scripts' `DOC`, evaluated by import, is the archived v1, which exists;",
          "     - `README.md` in `t13_figures_paper2.py` is written by the script, not read;",
          "     - the six `t*_symbolic*.py` names in `t13_regression_symbolic.py` are copied from `classification/t9`…`t12`, and all "
          "exist.",
          "   - No file is missing. The only change Task 14 made for reproduction is the path fallback in `t13_audit_numbers.py` "
          "and `t13_audit_refs.py` (disclosure item 6).",
          "4. **Development note (disclosure).** The converter (`make_source.py`) was developed by rendering in v1-number mode and "
          "diffing against v1, which is C4's method (ii). It was therefore known before the recorded run that the only "
          "remaining differences were the predicted ones.",
          "5. **Deviation from the pre-registration's output list.** The pre-registration planned a `MANUSCRIPT_LOCATION.md` stub "
          "because the manuscript was absent. The author then supplied it, so it is now in `reference/phase1/` and the stub was "
          "not kept. The errata quotes were checked against its text, all verbatim (pp. 5, 5, 8, 12). The value m = 0.0099852 "
          "is not in the manuscript; C7 confirms it.", ""]
    T += ["## C4 diff summary", "",
          f"Raw diff, actual paper render against v1: {c4['raw_paper_vs_v1_changed_lines']} changed lines. Almost all are numbers "
          "≥ 7 shifted by one. In the v1-number render (method (ii)) there are {} hunks:".format(c4["hunks"]), "",
          "| v1 lines | Category | v1 | render |", "|---|---|---|---|"]
    for h in c4["all_hunks"]:
        o = " / ".join(h["old"])[:110].replace("|", "\\|")
        n = " / ".join(h["new"])[:110].replace("|", "\\|")
        T.append(f"| {h['v1_lines']} | {h['category']} | {o} | {n} |")
    T += ["", "## Inventory (§1, state at the pre-registration commit)", "",
          f"Repository: {inv['n_files']} tracked files. Top level: `classification/` (Tasks 8–14), `verification/` (the starting "
          "study's suite: `PREREG.md`, `PREREG_t6.md`, `PREREG_t7.md`, `REPORT.md`, scripts `t1_symbolic.py`, `t2_em.py`, "
          "`t3_paired.py`, `t4a`–`t4e`, `t6_colored_symbolic.py`, `t7_*.py`, `run_all.sh`).",
          "",
          "- **Starting-study manuscript:** no PDF, TeX or Word file in any commit or branch. It was supplied by the author during "
          "Task 14.",
          "- **Task 1–7 commits:** d21f193 (pre-registration), 50f1b38…6457bad (T1–T4), 70ebb55 (results), 637d542 (report), "
          "824ca06/0944b81 (T6), a0d2be2/2f9da71/183cb8f (T7).", "",
          "Legacy-reference counts per file in `classification/`:",
          "- legacy regex: Prop./Thm/… followed by a number;",
          "- A–E labels;",
          "- 'Paper 1'.", "",
          "| File | Legacy regex | A–E | Paper 1 |", "|---|---|---|---|"]
    for f, c in sorted(inv["legacy_counts"].items()):
        T.append(f"| {f} | {c['legacy_regex']} | {c['A-E_labels']} | {c['Paper 1']} |")
    t = inv["totals"]
    T.append(f"| **total** | {t['legacy_regex']} | {t['A-E_labels']} | {t['Paper 1']} |")
    T += ["", "## Files moved or created", "",
          "- **Moved (`git mv`, unchanged):** `classification/Stages_0_4_Consolidated.md` → `classification/archive/Stages_0_4_Consolidated_v1.md`.",
          "- **Added unchanged:** `reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf` (the author's upload).",
          "- **Register:** `classification/register/` with `results.yaml`, `tasks.yaml`, `matrix.csv`, `crosswalk.md`, "
          "`crosswalk_v1.yaml` and `render.py`.",
          "- **Sources:** `classification/source/` with `Stages_0_4_Source.md`, `Roadmap_v3_Source.md`, `figs/*.txt`, "
          "`figs/README.md`, `phase1/README.md` and `phase1/ERRATA.md`.",
          "- **Renders (thesis):** `classification/Stages_0_4_Thesis.md`, `classification/Roadmap_v3.md` (overwritten; the "
          "earlier version is in git history), `classification/figs_thesis/` (10 captions and `README.md`), "
          "`classification/Appendix_A_Register.md`, `reference/phase1/README.md` and `reference/phase1/ERRATA.md`.",
          "- **Render (paper):** `classification/Stages_0_4_Paper2.md`.",
          "- **Bibliography:** `classification/references.bib` and `classification/t14/bib_check.md`.",
          "- **Task 14 code:** `classification/t14/` with `t14_common.py`, `t14_inventory.py`, `build_register.py`, "
          "`make_source.py`, `make_roadmap_source.py`, `make_bib.py`, `make_bib_check.py`, `t14_checks.py`, "
          "`t14_c10_diag.py`, `t14_partG.py`, `make_results_t14.py`, `input/register_table.csv`, and `results/`.",
          "- **Changed:** `classification/t13/t13_audit_numbers.py` and `t13_audit_refs.py`, which got a path fallback to the "
          "archived v1 (organisation only).", "",
          "Regenerate everything with:",
          "`python3 t14/build_register.py && python3 t14/make_source.py && python3 t14/make_roadmap_source.py && "
          "python3 register/render.py --numbering thesis && python3 register/render.py --numbering paper && python3 t14/make_bib.py`.",
          "",
          "## VERIFY flags left in the bibliography", "", "See `t14/bib_check.md` for the evidence behind each confirmed field.", ""]
    T += [l for l in open(os.path.join(HERE, "bib_check.md")).read().split("## VERIFY flags left in references.bib", 1)[1].split("\n") if l.startswith("|")]
    T += ["", "## Provenance", "",
          f"- Pre-registration: {PREREG}. Artifacts checked: {ARTIFACTS}. Results: {commit}.",
          f"- Runtimes: C1–C10 total {sum(C[k]['seconds'] for k in C):.1f} s; Part G about 1 s; the inventory and every build "
          "script under 2 s each.",
          "- Web: the bibliography search was run by a subagent of this session (37 searches) with an evidence rule. Only link "
          "titles and URLs count; generated summaries do not. doi.org and api.crossref.org were blocked."]
    add = os.path.join(HERE, "addendum_bib.md")
    tail = open(add).read() if os.path.exists(add) else ""
    open(os.path.join(HERE, "RESULTS_t14.md"), "w").write("\n".join(T) + "\n" + tail)
    print("written")


if __name__ == "__main__":
    main()
