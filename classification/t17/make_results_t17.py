"""Build classification/RESULTS_t17.md from the recorded Task 17 outputs. Usage: python3 make_results_t17.py RESULTS_COMMIT"""
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
R = os.path.join(HERE, "results")


def V(ok):
    return "**PASS**" if ok else "**FAIL**"


def main():
    rc = sys.argv[1] if len(sys.argv) > 1 else "(results commit)"
    C = json.load(open(os.path.join(R, "t17_checks.json")))
    G = json.load(open(os.path.join(R, "t17_diag.json")))
    A2 = yaml.safe_load(open(os.path.join(R, "a2_classification.yaml")))
    e5 = open(os.path.join(R, "e5_judgements.md")).read()
    e1 = C["E1"]
    items = {k: v["holds"] for k, v in e1.items() if isinstance(v, dict) and "holds" in v}
    item6 = "**Verdict: holds.**" in open(os.path.join(R, "e1_item6_review.md")).read()
    items["6 Cor 7.4"] = item6
    e1_pass = all(items.values())
    kinds = [d["kind"] for d in A2["differences"]]
    e2_pass = not any(k == "d" for k in kinds) and not any(k == "c" for k in kinds)   # every (c) would need a proof; none occur
    e3, e4, e6, e7 = C["E3"], C["E4"], C["E6"], C["E7"]
    n_claims_more = len(re.findall(r"\| \*\*claims more\*\* \|", e5))
    n_undet = len(re.findall(r"\| \*\*undetermined\*\* \|", e5))
    n_sup = len(re.findall(r"\| \*\*supported\*\*", e5))
    e5_pass = n_claims_more == 0
    t = ["# Results — Task 17: chapters 6–7 and the new §2.5 statements against the repository; repository sync items", "",
         "- Pre-registration: `classification/PREREG_t17.md`, commit **d23797b**.",
         f"- Artifacts checked: commit **{C['commit']}**. E1–E4, E6 and E7 ran once on it (6 s; `t17/results/t17_checks.log`, "
         "`.time`); E5's evidence was gathered after that run with the session's web search.",
         f"- Results: raw outputs **ddbceb6**; manual readings and post-hoc diagnosis **{rc}**; this report follows.", "",
         "## Checks", "", "| Check | Verdict | Details | Runtime (s) |", "|---|---|---|---|"]
    t.append(f"| E1 New proof steps (A1) | {V(e1_pass)} | {sum(items.values())} of 9 items hold; item 3 not shown in the recorded run "
             "(50-digit precision; holds exactly and at adequate precision post hoc); item 6: Corollary 7.4's proof as written does not "
             f"cover two clauses | {e1['seconds']} |")
    t.append(f"| E2 Statements (A2) | {V(e2_pass)} | 48 results: {len(A2['no_difference'])} without a difference, "
             f"{len(kinds)} with a wording-level difference (all kind a); no kind (b), (c) or (d) | {C['E2']['seconds']} |")
    t.append(f"| E3 Numbers (A3) | {V(e3['pass'])} | {e3['n_match']} of {e3['n']} values match; mismatch: "
             + "; ".join(f"{m['what']} (printed {m['printed']}, source {m['value']})" for m in e3["mismatches"]) + f" | {e3['seconds']} |")
    t.append(f"| E4 Cross-references (A4) | {V(e4['pass'])} | {e4['citation_groups']} citation groups, 0 unresolved; first citation "
             f"in order for [1]–[53]; {e4['typed_refs']} typed references, {len(e4['typed_bad'])} wrong type ("
             + "; ".join(f"{b['ref']}: {b['number']} {b['problem']}" for b in e4["typed_bad"]) + f"); {e4['untyped_refs']} table labels "
             f"exist; {e4['figure_refs']} figure references, 0 unknown | {e4['seconds']} |")
    t.append(f"| E5 Prior-work sentences (A4) | {V(e5_pass)} | 13 sentences: {n_sup} supported, {n_claims_more} claims more (§7.3, "
             f"[47]), {n_undet} undetermined (titles and search summaries only; abstracts unreachable) | — |")
    t.append(f"| E6 Escaped citations (B.1) | {V(e6['pass'])} | 0 escaped groups in any render; {e6['now_total']} citations = baseline "
             f"{e6['baseline_total']} + {sum(e6['added_by_imports'].values())} from the new thesis-only texts | {e6['seconds']} |")
    t.append(f"| E7 Legacy labels (B.3) | {V(e7['pass'])} | 0 flagged; {e7['exempt']['figure label']} figure labels exempt, Appendix E "
             f"included; {e7['paper1']} 'Paper 1' (Appendix D's quotation, reported) | {e7['seconds']} |")
    fails = [k for k, ok in (("E1", e1_pass), ("E2", e2_pass), ("E3", e3["pass"]), ("E4", e4["pass"]), ("E5", e5_pass),
                             ("E6", e6["pass"]), ("E7", e7["pass"])) if not ok]
    t += ["", f"**Pre-registered checks that FAIL:** {', '.join(fails)}. Each stays a failure; diagnoses below.", "",
          "## Diagnoses", "",
          "- **E1 item 3 (attribution: code).** The numeric test of \"the optimal prior M < F\" ran at 50 digits. Where "
          "e^(−2λΔt) < 10⁻⁵⁰ (large λΔt in the log-uniform draw) F − M = O(F·e^(−2λΔt)) is below working precision and M = F "
          f"numerically: {e1['3 Prop 6.13']['Lstar_numeric']['counterexamples']} of 1,000 sets, every printed example with M = F to "
          "all printed digits. Exactly, the steady prior is the positive root of an upward parabola f with f(0) < 0 and "
          "f(F) = F²a² > 0, so M < F; and the same "
          f"test with the precision raised above 2λΔt/ln 10 digits (seed 17003, the spare) gives "
          f"{G['E1_item3_adaptive_precision']['counterexamples']} of 1,000. Every symbolic part of item 3 reduced to 0 in the recorded run.",
          "- **E1 item 6 (attribution: document).** Corollary 7.4 is true, but its proof (\"Corollary 7.3, and Proposition 7.7(a)\") "
          "does not cover the exclusion of All along precision, which needs σ⋆² → 0 (Proposition 3.5), nor the last clause, which "
          "is Theorem 5.1 (named in the statement). See `t17/results/e1_item6_review.md`.",
          "- **E3 (attribution: document).** \"Theorem 7.8: T11.3 over 37 values of β\": Task 11 ran 129 values (β = k/20, k = −40…80, "
          "plus {0, 2} ± {10⁻⁶, 10⁻³}, as its pre-registration says). The \"37\" is in the repository's own label of Theorem 7.8 "
          "(`source/Stages_0_4_Source.md`) and was carried into the draft. This was seen while locating the sources, after the "
          "pre-registration commit (PREREG_t17 disclosure 8).",
          "- **E4 (attribution: document).** §6.7's summary table cites \"Prop. 6.10–6.12\"; 6.11 is a Counterexample. The "
          "pre-registered rule requires every member of a typed range to have the type.",
          "- **E5 (attribution: document).** §7.3 says coloured measurement noise is a standard setting \"for analysing mis-specified "
          "time correlation [47]\"; [47] studies time-correlated **model error** in Kalman smoothers. §6.2's wording "
          "(\"time-correlated errors\") is supported. Two further sentences are undetermined because no abstract could be reached "
          "(doi.org and Crossref are refused by the session's network policy).", "",
          "## Disclosure", "",
          "- Before the recorded run each check was run once with its output discarded (only to see that it ran), and the E3 source "
          "anchors and the E2 extraction were checked for completeness (all found). No code error appeared; nothing was changed.",
          "- While locating the E3 sources (after the pre-registration commit) the \"37 vs 129\" discrepancy was seen; the check was not "
          "changed.",
          "- E1 item 6, E2's classification and E5 are manual readings after the recorded run (`t17/results/`).", "",
          "## Files changed", "",
          "- `register/render.py` (thesis-only overrides, thesis render only); new `register/thesis_overrides.yaml`.",
          "- New `source/thesis_only/`: `stationary-variance.md` (3.1), `optimal-envelope.md` (3.5, 3.6 and their proof), "
          "`plateaus.md`, `equal-height-maxima.md`, `degenerate-points.md`, `pair-birth.md` (2.4–2.7), `discrete-excess.md` (6.13); "
          "`normal-form.md` and `tau-optimal-normal-form.md` with citations unescaped. `source/Stages_0_4_Source.md` unchanged.",
          "- Renders: `Stages_0_4_Thesis.md`, `Appendix_D_Verification.md` (draft layout; Tasks 15–17 entries), "
          "`Appendix_E_Reproduction.md` (T17 row and chain step).",
          "- `t15/make_appendix_de.py` (Appendix D layout, Task 15–17 failures, chain).",
          "- New: `t17/make_thesis_only_t17.py`, `t17/t17_checks.py`, `t17/t17_diag.py`, `t17/make_results_t17.py`, `t17/input/`, "
          "`t17/results/`.", "",
          "## For the author", "", "### 1. A1: the new proof steps", "", "| Item | Verdict | Evidence |", "|---|---|---|"]
    ev = {"1 Cor 6.5": "Πb = 2λ(1 + νt) and Π²D = 4λ²((1 + νt)² + ν(1 − t)²) reduce to 0; with Π√D = 2λ√(…) (both positive) "
                       "P/F reduces to the stated form; t = 0 gives 2/(1 + √(1 + ν)).",
          "2 Lemma 6.1 normal form": "σ²/F − 𝒱_τ reduces to 0; σ² − F = (G/a)(G/(2Π(1 + aτ)) − F), so σ² > F iff q > 2(1 + aτ); 0 "
                                     "counterexamples in 1,000.",
          "3 Prop 6.13": "P⁻ from P⁻ = a²P⁺ + q, P⁺ = (1 − L)²P⁻ + L²r; the numerator a²L(Lr − F(2 − L)); P⁺ − F = (P⁻ − F)/a²; "
                         "L⋆/(2 − L⋆) = P⁻/(P⁻ + 2r): all reduce to 0; P⁻ > F iff L/(2 − L) > φ: 0 counterexamples. The optimal "
                         "prior's M < F was not shown at 50 digits for 102 sets with e^(−2λΔt) < 10⁻⁵⁰; it holds exactly (f(F) = F²a² "
                         "> 0) and at adequate precision (diagnosis).",
          "4 Lemma 6.14": "the identity and the definition of P̄ as the time average of e^(−2λt)P⁺ + F(1 − e^(−2λt)) reduce to 0.",
          "5 Lemma 6.23": "σ²/F = (1 + g²/u)/(1 + g) reduces to 0; (Σ, Π) pairs with equal u give equal σ²/F to 10⁻⁴⁰ (1,000 "
                          "sets); u is a bijection of Σ and of Π, so the relative failure sets coincide.",
          "6 Cor 7.4": "fails as written: the proof does not cover the exclusion of All (needs σ⋆² → 0) or the last clause "
                       "(Theorem 5.1); the corollary itself is true.",
          "7 Prop 2.7": "roots ±√(bδ); ∫ a(x² − bδ) between them = −(4/3)a(bδ)^(3/2): residual 0.",
          "8 Thm 7.8 bound": "B > 0 gives B + √(B² + 4AC) > 2√(AC), so P < √(C/A); 0 counterexamples; C/A = 2ΣKτ^β/(1 − λτ)² "
                             "reduces to 0.",
          "9 Prop 7.10": "A(1/(λ²τ)) = A(τ) and v_(2−β, Kλ^(2−2β))(1/(λ²τ)) = v_(β,K)(τ) reduce to 0; P equal to 10⁻³⁵ in 1,000 "
                         "sets with β ∈ (−3, 5)."}
    for k, txt in ev.items():
        ok = items.get(k)
        verdict = "holds" if ok else ("holds post hoc; not shown in the recorded run (code)" if k.startswith("3") else "fails as written")
        t.append(f"| {k} | {verdict} | {txt} |")
    t += ["", "### 2. A2: statements", "", f"No difference beyond typography in: {', '.join(A2['no_difference'])}.", "",
          "No difference of kind (b), (c) or (d). The wording-level differences (all kind a):", ""]
    for d in A2["differences"]:
        t += [f"**{d['result']}, kind ({d['kind']}).** {d['what']}", "", f"- Draft: {d['draft']}", f"- Repository: {d['repo']}", ""]
    p = A2["proofs_added_in_draft"]
    t += [f"**Proofs.** {p['note']} Results: {', '.join(p['results'])}.", "",
          "**Edits named in the prompt.** 6.13 in the M-P notation: equivalent (above). 6.9 and 7.4 carry proofs in the draft: 7.4's "
          "is incomplete as written (A1 item 6); 6.9's matches the repository's. 7.6's title: wording only.", "",
          "### 3. A3: numbers", "", "| # | Value | Printed | Computed or stored | Source | Match |", "|---|---|---|---|---|---|"]
    for r in e3["rows"]:
        val = r["value"] if not isinstance(r["value"], bool) else ("yes" if r["value"] else "no")
        t.append(f"| {r['row']} | {r['what']} | {r['printed']} | {val} | {r['source']} | {'yes' if r['match'] else '**no**'} |")
    t += ["", "### 4. A4: references and prior-work judgements", "",
          f"Mechanical: {e4['citation_groups']} citation groups resolve; first citations of [1]–[53] are in order; one typed reference "
          "spans a wrong type (\"Prop. 6.10–6.12\" includes Counterexample 6.11); all figure references exist. Excluded as non-citations: "
          + "; ".join(f"`{x['text']}`" for x in e4["excluded_brackets"][:4]) + f" and {len(e4['excluded_brackets']) - 4} more bracketed "
          "formulas.", "", "Prior-work judgements (evidence in `t17/results/e5_sources.md`):", ""]
    tab = e5.split("\n")
    i = next(k for k, l in enumerate(tab) if l.startswith("| # |"))
    j = next(k for k in range(i, len(tab)) if not tab[k].startswith("|"))
    t += tab[i:j] + ["", "### 5. Other disagreements in chapters 1–7 (listed, not resolved)", "",
                     "1. **\"37 values of β\"** (§7.6 verification of Theorem 7.8) and the repository's own label: Task 11 ran 129.",
                     "2. **\"Prop. 6.10–6.12\"** (§6.7 table) spans Counterexample 6.11.",
                     "3. **Theorem 2.2's parts** are numbered (1)–(4) in the draft and (a)–(d) in the repository. After this task's "
                     "imports the thesis render carries the draft's 2.4 and 2.5, which cite \"Theorem 2.2(1)–(2)\" and \"2.2(3)–(4)\", "
                     "next to the repository's Theorem 2.2 with parts (a)–(d).",
                     "4. **Proposition 2.7's proof:** the draft gives the value change as (4/3)|a|(bδ)^(3/2); the repository's proof "
                     "writes (4/3)a(bδ)^(3/2) without the absolute value (A1 item 7 confirms the draft).",
                     "5. **[26]** (§6.3) is cited for the variance factor α/(2 − α) of an exponentially weighted average; the search "
                     "summaries of [26] (α–β–γ trackers with acceleration measurements) do not show it.",
                     "6. **[21]** (§7.1) is cited for monotonicity under garbling in stochastic control; its abstract concerns "
                     "optimisation and continuity of observation channels. [22, 23] carry the comparison of information structures.",
                     "7. **Bryson and Henrikson [28]** is dated 1968 in the bib (the journal version); the search found the 1967 Harvard "
                     "report of the same work.",
                     "8. **Corollary 7.4's proof** (A1 item 6).", ""]
    open(os.path.join(CLS, "RESULTS_t17.md"), "w").write("\n".join(t))
    print("written")


if __name__ == "__main__":
    main()
