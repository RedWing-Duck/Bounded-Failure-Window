"""Build classification/RESULTS_t16.md from the recorded Task 16 outputs (t16/results/). Usage: python3 make_results_t16.py RESULTS_COMMIT"""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
R = os.path.join(HERE, "results")


def V(ok):
    return "**PASS**" if ok else "**FAIL**"


def main():
    rc = sys.argv[1] if len(sys.argv) > 1 else "(results commit)"
    C = json.load(open(os.path.join(R, "t16_checks.json")))
    G = json.load(open(os.path.join(R, "t16_diag.json")))
    A2 = yaml.safe_load(open(os.path.join(R, "a2_classification.yaml")))
    d1 = C["D1"]
    item_ok = {k: v.get("holds", v.get("numeric_holds")) for k, v in d1.items() if isinstance(v, dict)}
    review_holds = "**Verdict: holds.**" in open(os.path.join(R, "d1_item4_review.md")).read()
    k4 = "4 Prop 2.9 remark (numeric part)"
    item_ok[k4] = item_ok[k4] and review_holds
    d1_pass = all(item_ok.values())
    kinds = [d["kind"] for d in A2["differences"]]
    d2_pass = not any(k in ("c", "d") for k in kinds)
    d3 = C["D3"]
    T = [f"# Results — Task 16: the thesis draft (chapters 1–5) against the repository; small repository fixes", "",
         "- Pre-registration: `classification/PREREG_t16.md`, commit **19c6ffe**.",
         f"- Artifacts checked: commit **{C['commit']}**. D1–D8 ran once on it (35 s in all; `t16/results/t16_checks.log`, `.time`).",
         f"- Results: commit **{rc}** (recorded outputs, the A2 classification, the item 4 review and the post-hoc diagnosis); this "
         "report follows it.", "",
         "## Checks", "", "| Check | Verdict | Details | Runtime (s) |", "|---|---|---|---|"]
    n_hold = sum(bool(v) for v in item_ok.values())
    T.append(f"| D1 New proof steps (A1) | {V(d1_pass)} | {n_hold} of 9 items hold in the recorded run; items 2 and 9 did not reduce "
             f"in the pre-registered SymPy routes (code; both hold post hoc) | {d1['seconds']} |")
    T.append(f"| D2 Statements (A2) | {V(d2_pass)} | {len(A2['differences'])} differences in 36 results: "
             f"{kinds.count('a')} (a), {kinds.count('b')} (b), {kinds.count('c')} (c), {kinds.count('d')} (d); kind (c) at "
             + ", ".join(d["result"] for d in A2["differences"] if d["kind"] == "c") + f" | {C['D2']['seconds']} |")
    T.append(f"| D3 Numbers (A3) | {V(d3['pass'])} | {d3['n_match']} of {d3['n']} values match their sources to the digits "
             f"printed | {d3['seconds']} |")
    d4 = C["D4"]
    T.append(f"| D4 Cross-references (A4) | {V(d4['pass'])} | {d4['citation_groups']} citation groups, 0 unresolved; first-citation "
             f"order 1–45 holds; {d4['typed_refs']} typed and {d4['untyped_refs']} untyped result references, 0 broken; "
             f"{d4['figure_refs']} figure references, 0 unknown | {d4['seconds']} |")
    d5 = C["D5"]
    T.append(f"| D5 Figure B.4 (Part B) | {V(d5['pass'])} | root Π_c = {float(d5['root']):.6g}; description, Appendix B and the "
             f"B.4 caption print 56.20 | {d5['seconds']} |")
    d6 = C["D6"]
    T.append(f"| D6 Legacy labels (C.1) | {V(d6['pass'])} | crosswalk: 0 unprefixed; renders: {len(d6['bare_legacy_labels'])} "
             f"flagged (2 figure labels outside the exemption window, Appendix E), 0 false hits on Figure B.n, "
             f"{d6['paper1']} 'Paper 1' (a quotation in Appendix D) | {d6['seconds']} |")
    d7 = C["D7"]
    T.append(f"| D7 Citation check (C.2) | {V(d7['pass'])} | {d7['now_total']} citations detected = baseline {d7['baseline_total']} "
             f"(per file equal); intervals not flagged ({len(d7['non_citations'])} listed as non-citations); no other hit | "
             f"{d7['seconds']} |")
    T.append(f"| D8 Register wording (C.3) | {V(C['D8']['pass'])} | 0 consolidated-v1 numbers in `verified_by` | {C['D8']['seconds']} |")
    fails = [k for k, ok in (("D1", d1_pass), ("D2", d2_pass), ("D3", d3["pass"]), ("D4", d4["pass"]), ("D5", d5["pass"]),
                             ("D6", d6["pass"]), ("D7", d7["pass"]), ("D8", C["D8"]["pass"])) if not ok]
    T += ["", f"**Pre-registered checks that FAIL:** {', '.join(fails)}. Each stays a failure; diagnoses below.", "",
          "## Diagnoses", "",
          "- **D1 (attribution: code).** Item 2(b) asked SymPy's assumption system whether −λ + √(λ² + 2ΣΠ) is positive; it "
          "returns None (undecided), so the check recorded the claim as not shown. The radicand minus λ² is 2ΣΠ > 0, the other "
          "root is negative, and 1,000 random sets (seed 16003, the pre-registered spare) give no counterexample. Item 9's "
          "residual contains √(R⁴ + 4d(R² + d)) = R² + 2d (with Σ = λ(R² + d)), a square root of a square that none of the three pre-registered "
          "routes denests (the cause of the Task 10 and Task 13 route failures too); after substituting the denested root the "
          "residual is 0, and the recorded numeric residual was 1.4 × 10⁻⁴⁸. Both claims hold (`t16_diag.json`). Every other "
          "sub-check of items 2 and 9 passed in the recorded run.",
          "- **D2 (attribution: document, and criterion).** Four differences are of kind (c). For 3.1 and 3.5 the draft's statement "
          "includes conclusions that the repository states in other results (Theorem 3.4, Lemma 3.6, Corollary 5.5): the draft is "
          "stronger than the repository's statement of *that* result, not than the repository; D1 items 1 and 2 verify the added "
          "conclusions. For 2.5 and 2.7 the draft has no statement, only a row of the §2.5 event table that leaves out the "
          "result's hypotheses; read as a statement it claims more than the repository. The criterion counts a correct, proved "
          "strengthening the same as an unproved one.",
          "- **D6 (attribution: criterion, and document).** None of the three hits is a legacy label. Appendix E's chain comment "
          "added in this task (\"… B.4 Pi_c\") and its line \"figures B.1, B.3–B.12 (text-only edits) and B.2\" name figure "
          "labels more than 40 characters after a \"figure\" word, outside the pre-registered exemption window; Appendix D's T15 "
          "failure line quotes the phrase \"0 'Paper 1'\". Bare legacy labels in the thesis renders: 0; false hits on Figure B.n: 0.",
          "", "## Disclosure", "",
          "- Before the recorded run each check was run once with its output discarded (standard output to /dev/null, JSON to the "
          "scratchpad), only to see that it ran. One code error was fixed: D3's maximiser of φₙ (a Newton start that strayed into "
          "complex values), replaced by golden-section search with a Newton polish; because the polish limits precision, the "
          "tolerance for t\\*² = 2√3 − 3 was set to 10⁻³⁰ at the same time, before any value was seen. The D2 extraction was checked for completeness; it reported 2.4–2.7 missing from the draft, which "
          "reading the draft had already shown (they appear only in the §2.5 table).",
          "- D2's classification and D1 item 4's logical review are manual readings made after the recorded run "
          "(`t16/results/a2_classification.yaml`, `d1_item4_review.md`).", "",
          "## Files changed", "",
          "- `register/results.yaml` (legacy labels prefixed; 5.6 `verified_by` \"T8.1 (Corollary 3.3, excess identity)\"); "
          "`register/crosswalk.md` (regenerated); `register/crosswalk_v1.yaml` (\"legacy §A.3\"); `register/figures.yaml` (B.4 "
          "Π_c = 56.20).",
          "- `source/figs/fig02_realizability.txt`, `source/figs/README.md` (Π_c = 56.20); `source/thesis_only/structural-stability.md` "
          "(the \"Direction in condition 2\" remark), `source/thesis_only/normal-form.md` (heading \"Theorem 3.2 (normal form)\").",
          "- Renders: `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (one change-log line: \"legacy §A.3\"), `Appendix_A_Register.md`, "
          "`Appendix_B_Figures.md`, `Appendix_E_Reproduction.md`, `figs_thesis/B.4_realizability.txt`, `figs_thesis/README.md`.",
          "- `t15/make_appendix_de.py` (Appendix E: the T16 row and the `t16/t16_register.py` step).",
          "- New: `t16/t16_register.py`, `t16/t16_checks.py`, `t16/t16_diag.py`, `t16/make_results_t16.py`, `t16/input/`, "
          "`t16/results/`.", "",
          "## For the author", "", "### 1. A1: the new proof steps", "",
          "| Item | Verdict | Evidence |", "|---|---|---|"]
    ev = {
        "1 Prop 3.1": "D/(2a) = (Σ + G²/(2Π))/(λ + G) reduces to 0; the Lyapunov equation gives P = D/(2a); both limits by "
                      "substitution into a continuous expression; F − H = ΣG∞/(λ(λ + G∞)) > 0.",
        "2 Prop 3.5 / Lemma 3.6": "Riccati root, G⋆ = pΠ, σ⋆² = p = σ²(G⋆), ∂σ²/∂G, both forms of q⋆: residual 0. dσ⋆²/dΠ < 0, "
                                  "σ⋆² → F, σ⋆² < F: 0 counterexamples in 1,000. The recorded run did not establish \"G⋆ is the "
                                  "only positive zero\" (SymPy could not decide the sign); it holds (diagnosis D1).",
        "3 Lemma 3.7": "total derivative minus G·N/(2Π²(λ + G)²): residual 0; ∂σ²/∂Π = −G²/(2Π²(λ + G)): residual 0.",
        k4: "logical review: complete as written (`d1_item4_review.md`); numeric: 1,000 (curve, Nᵢ) pairs, 0 counterexamples.",
        "5 Thm 5.1": "positive root of Πv² + 2λv − 2Σ minus σ⋆²: residual 0.",
        "6 Prop 5.8": "ε = 1 − G/c and the eliminated N: residual 0; root in (0, c) iff λc > 2ΣΠ₀ iff κ > 2: symbolic, and 0 "
                      "counterexamples in 1,000; turning point a maximum: N changes sign + → − in 1,000 of 1,000 sets with κ > 2.",
        "7 Prop 5.9": "inverse Π(G), ε and N = G·p(G)/(2(G + λ′)): residual 0; p′ < 0 and p(0) > 0 iff F′ > 2F: 0 counterexamples.",
        "8 Prop 5.14": "derivative identity, σ² − F factorisation, gap identity (RHS − LHS = ΠG′(2ΣΠ − λG)) and the Bayesian-stage "
                       "identity: residual 0; the bound: 0 counterexamples in 1,000.",
        "9 Cor 5.2": "the recorded run left the residual R²(R² + 2d − √(R⁴ + 4d(R² + d)))/(R² + √(…)) (numeric 1.4 × 10⁻⁴⁸); the "
                     "radicand is (R² + 2d)², so it is 0 and the identity holds (diagnosis D1).",
    }
    for k in ev:
        verdict = "holds" if item_ok[k] else "holds post hoc; recorded as not shown (code)"
        T.append(f"| {k} | {verdict} | {ev[k]} |")
    T += ["", "No item fails mathematically and none is ambiguous. One sub-claim outside the nine items was also checked post "
          "hoc: §3.3's 𝒱 − 1 = νq(q − 2)/(4 + 2νq) (residual 0).", "",
          "### 2. A2: statements", "",
          f"No difference beyond wording in: {', '.join(A2['no_difference'])}.", ""]
    for d in A2["differences"]:
        T += [f"**{d['result']}, kind ({d['kind']}).** {d['what']}", "", f"- Draft: {d['draft']}", f"- Repository: {d['repo']}"]
        if d.get("note"):
            T.append(f"- Note: {d['note']}")
        T.append("")
    T += ["**The two edits named in the prompt.** \"G⋆ < FΠ for Π > 0\" (3.5): the non-strict ≤ is the manuscript's (Paper 1, "
          "Proposition 3, p. 4), not the repository's, whose Lemma 3.6 already states σ⋆² = G⋆/Π < F; the strict form holds "
          "(D1 item 2). Corollary 5.4's title differs; the statement does not.", "",
          "**Should the thesis render carry the draft's wording of 3.1, 3.5, 3.6 and 3.7?** 3.7 is already identical. 3.1 and 3.5 "
          "have no labelled statement in the repository (only §1's model paragraph and a bullet), and the draft's statements are "
          "verified (D1 items 1–2), so importing them as thesis-only texts would give both a statement. 3.6 should move with 3.5: "
          "the draft moves the minimum value into 3.5 and \"σ² ≤ F iff G ≤ 2FΠ\" into 3.3, so taking the draft's 3.6 alone would "
          "drop content the repository states. Not changed (Part C.4).", "",
          "### 3. A3: numbers", "", "| # | Value | Printed | Computed or stored | Source | Match |", "|---|---|---|---|---|---|"]
    for r in d3["rows"]:
        val = r["value"] if not isinstance(r["value"], bool) else ("yes" if r["value"] else "no")
        T.append(f"| {r['row']} | {r['what']} | {r['printed']} | {val} | {r['source']} | {'yes' if r['match'] else '**no**'} |")
    T += ["", "### 4. A4: references", "",
          f"No broken reference. {d4['citation_groups']} citation groups resolve; numbers 1–45 first appear in order; "
          f"{d4['typed_refs']} typed references (Theorem, Prop., Cor., …, ranges expanded) name a result of that type; "
          f"{d4['untyped_refs']} table labels exist; Figure B.1–B.6 references ({d4['figure_refs']}) exist. Excluded as intervals: "
          + "; ".join(f"`{e['text']}`" for e in d4["excluded_brackets"]) + ".", "",
          "### 5. Part B: Π_c", "",
          f"The B.4 script (`t13/t13_figures_paper2.py`) uses λ = 1, Σ = 0.01, c = 1, κ = 1.5, Π₀ = c/(κF) = 66.67, the parameters "
          f"the description states. It takes Π_c as the first point of its 1,500-point log grid where cΠ/(Π + Π₀) < G⋆, and prints "
          f"it to three figures: {d5['script_grid_value']}. The root of cΠ/(Π + Π₀) = −λ + √(λ² + 2ΣΠ) is {float(d5['root']):.6f}, "
          "the value Task 10 also recorded; the description's 56.7 is the grid value, not a computation error in the formula. The "
          "description now gives Π_c = 56.20 (figures.yaml, Appendix B, the B.4 caption and the figs_thesis README). The image shows no "
          "Π_c and is unchanged, as is the curve (the bumps are still placed relative to the grid value). The Task 13 paper outputs "
          "(`figs_paper2/fig02_realizability.txt`, `figs_paper2/README.md`) keep 56.7, and re-running the T13 script prints 56.7 "
          "again.", "",
          "### 6. Other disagreements in chapters 1–5 (listed, not resolved)", "",
          "1. **\"961 random sets\" (§5.6, Theorem 5.12(b)).** Task 10's exact root-count check ran on all 2,000 sets with n = 2 "
          "(`t10/t10_census.py`), of which 961 had the pair and 1,039 none; 0 disagreements. The repository's own label also says "
          "\"961 random sets\". The count of sets checked is 2,000.",
          "2. **§1.5 \"Every class is then available to some gain (Corollary 5.3)\".** Corollary 5.3 restricts R² < F to classes "
          "with ℓ = 1; the sentence is right for R² ≥ F, or for \"some tolerance\".",
          "3. **Proposition 4.5 uses c_R** (\"Upper ray (c_R, ∞)\") without defining it.",
          "4. **§2.5 table rows for 2.4–2.7** are the draft's only statements of those results; rows for 2.5 and 2.7 leave out "
          "hypotheses (see A2).",
          "5. **Citations written \\[n\\] in the renders** are not seen by Task 15's bracket pattern, which D7 keeps: "
          f"{sum(G['D7_coverage']['escaped_citation_groups'].values())} such groups in the thesis renders "
          f"({', '.join(G['D7_coverage']['escaped_citation_groups'])}). Neither check tests them.",
          "6. **Appendix D's T15 entry** quotes the phrase \"Paper 1\", and Appendix E names figure labels without \"Figure\"; both "
          "trip D6's pre-registered pattern (above).", ""]
    open(os.path.join(CLS, "RESULTS_t16.md"), "w").write("\n".join(T))
    print("written")


if __name__ == "__main__":
    main()
