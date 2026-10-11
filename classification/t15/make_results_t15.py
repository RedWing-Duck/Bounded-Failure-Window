"""Build classification/RESULTS_t15.md from t15/results/*.json. Usage: python3 make_results_t15.py RESULTS_COMMIT"""
import json
import os
import subprocess
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
PREREG, ARTIFACTS = "aa0b914", "41d5e43"


def L(n):
    p = os.path.join(HERE, "results", n)
    return json.load(open(p)) if os.path.exists(p) else {}


def V(ok):
    return "**PASS**" if ok else "**FAIL**"


def main():
    commit = sys.argv[1] if len(sys.argv) > 1 else "(this commit)"
    C, G, D = L("t15_checks.json"), L("t15_partG.json"), L("t15_diag.json")
    figs = yaml.safe_load(open(os.path.join(CLS, "register", "figures.yaml")))
    g11, g12, ill, gx = G.get("C11", {}), G.get("C12", {}), G.get("ILL", {}), G.get("C11X", {})
    T = ["# Task 15: sync the repository with the thesis draft (results)", "",
         f"- Pre-registration: `classification/PREREG_t15.md`, commit **{PREREG}**.",
         f"- Artifacts checked: commit **{ARTIFACTS}**. Checks C1–C10 and C13 and Part G (C11, C12) ran once on it.",
         f"- Results and diagnoses: commit **{commit}**.",
         "- The planned post-run register change (status of 2.8 and 2.9) and the re-render of Appendices A and D are in the "
         "commit after the results.", "",
         "## Check table", "", "| Check | Verdict | Details | Runtime (s) |", "|---|---|---|---|"]
    c = C
    rows = [
        ("C1 Bibliography", c["C1"]["pass"], f"{c['C1']['entries']} entries, {c['C1']['doi']} DOI, {c['C1']['verify']} VERIFY; dangling {c['C1']['dangling']}, unused {c['C1']['unused']}; jazwinski1970 → {c['C1']['attachments']['jazwinski1970']}, simon2006 → {c['C1']['attachments']['simon2006']}", c["C1"]["seconds"]),
        ("C2 Reference register", c["C2"]["pass"], "numbers 1–53 unique and contiguous; bijection with the bib; equal to the frozen table; 46–53 planned", c["C2"]["seconds"]),
        ("C3 Appendix C render", c["C3"]["pass"], f"{c['C3']['lines_render']} lines against the draft's {c['C3']['lines_draft']}; {len(c['C3']['differences'])} differences", c["C3"]["seconds"]),
        ("C4 [n] rendering", c["C4"]["pass"], f"{c['C4']['files']} thesis renders; hits: " + "; ".join(f"{k}: {v}" for k, v in c["C4"]["hits"].items()) if c["C4"]["hits"] else "0 raw keys, 0 author–year, 0 tokens, all numbers resolve", c["C4"]["seconds"]),
        ("C5 Figures carry no numbers", c["C5"]["pass"], f"{c['C5']['n']} figures, {c['C5']['text_elements']} text elements inspected; {len(c['C5']['hits'])} with a match", c["C5"]["seconds"]),
        ("C6 Figure B.2", c["C6"]["pass"], f"touch at (ν_R, r) = ({c['C6']['touch']['0.5']['nu_R']}, 0.5) exact; r = 1 boundary {{0}} ∪ {{2}}: {c['C6']['r1']}; ordering violations {c['C6']['ordering_violations']} at 10⁴ ν; negative q drawn {c['C6']['negative_q_drawn']}", c["C6"]["seconds"]),
        ("C7 Figure data unchanged", c["C7"]["pass"], "all plotted arrays of B.1 and B.3–B.12 equal the original scripts' (11 figures)", c["C7"]["seconds"]),
        ("C8 Roadmap §7", c["C8"]["pass"], "rows 11–17 equal the Part D table; the line follows it; no 'query text not supplied'; rows 6–10 unchanged", c["C8"]["seconds"]),
        ("C9 Appendix letters", c["C9"]["pass"], f"{len(c['C9']['old_sense'])} old-sense uses; {c['C9']['files_present']}/5 appendix files", c["C9"]["seconds"]),
        ("C10 Thesis phrase check", c["C10"]["pass"], f"0 'Paper 1' in {c['C10']['files']} renders; A–E pattern matches: {D.get('C10', {}).get('matches', '?')}, all the new figure labels B.1–B.12", c["C10"]["seconds"]),
        ("C11 Corollary 2.8", g11.get("pass"), f"{g11.get('curves')} curves ({g11.get('by_kind')}), {g11.get('tolerances')} tolerances, {g11.get('classifications')} classifications; class mismatches {g11.get('class_mismatches')}, signature mismatches {g11.get('signature_mismatches')}, route disagreements {g11.get('route_disagreements')}; turning points per curve {g11.get('turning_points_hist')}", g11.get("seconds")),
        ("C12 Proposition 2.9", g12.get("pass"), f"{g12.get('cases_run')} cases on {g12.get('curves')} curves ({g12.get('by_kind')}); mismatches {g12.get('mismatches')}; skipped {len(g12.get('skipped', []))}; crossings {g12.get('crossings_hist')}", g12.get("seconds")),
        ("C13 Reproduction unaffected", c["C13"]["pass"], f"{c['C13']['checked']} paths; {len(c['C13']['unresolved'])} unresolved", c["C13"]["seconds"]),
    ]
    for n, ok, txt, s in rows:
        T.append(f"| {n} | {V(ok)} | {txt} | {s} |")
    fails = [r[0] for r in rows if not r[1]]
    T += ["", f"**Pre-registered checks that FAIL:** {'; '.join(fails) or 'none'}. Each is diagnosed below.", "",
          "## Diagnoses", ""]
    if not c["C4"]["pass"]:
        T.append(f"- **C4 (attribution: criterion/code).** {D['C4']['text']} Item: `{D['C4']['items'][0]['context']}`.")
    if not c["C10"]["pass"]:
        T.append(f"- **C10 (attribution: criterion).** {D['C10']['text']} No other A–E label and no 'Paper 1' remains "
                 "anywhere, newlines included, so the Part H.1 miss is fixed.")
    for k, r in (("C11", g11), ("C12", g12)):
        if r and not r.get("pass"):
            T.append(f"- **{k}:** see the examples in `t15/results/t15_partG.json`.")
    T += ["- **Task 14 C9** (unused entries, unresolvable DOIs) is resolved by this task's input: the verified bib and the Part A "
          "attachments (C1 passes). `RESULTS_t14.md` is unchanged.",
          "- **Development disclosure.** Before the recorded run, the Appendix C formatter was compared with the draft's list during "
          "development, as with T14's converter. The Part G code was smoke-tested on 8 curves (C11) and 6 curves (C12); those "
          "results are kept in `t15/results/t15_partG_smoke*.json`. The smoke test showed that the pre-registered monomial "
          "polynomials give mostly 1–2 turning points. The design was not changed. A separate, exploratory run on Chebyshev "
          "series is reported below and is not a pass criterion.", ""]
    T += ["## Part G detail", "",
          f"- **C11** used {g11.get('curves')} pre-registered curves with {g11.get('min_tolerances_per_curve')} or more tolerances "
          "each, every critical value included.",
          f"- **Exploratory C11X** (not pre-registered): Chebyshev series of degree 9–12 with seeds 15301/15302 gave "
          f"{gx.get('curves')} curves with turning points {gx.get('turning_points_hist')}. Class mismatches "
          f"{gx.get('class_mismatches')}, signature mismatches {gx.get('signature_mismatches')}, route disagreements "
          f"{gx.get('route_disagreements')}.",
          f"- **C12:** {g12.get('cases_run')} cases. Two kinds of perturbation: (a) constant on each Nᵢ; (b) a smooth sum accepted only "
          "if strictly monotone on every Nᵢ. The class was unchanged in all cases with sup |δ| < η.",
          f"- **Illustration (not a criterion):** a wiggle of amplitude 0.9η inside N₁, violating only condition 2, changes the class "
          f"from {ill.get('class_before')} to {ill.get('class_after')} (route ii agrees: {ill.get('class_after_route_ii')}); "
          f"R² = {ill.get('R2')}, η = {ill.get('eta')}.",
          "- **Ambiguity in Proposition 2.9, not blocking.** Condition 2 asks for σ̃² strictly monotone on each Nᵢ without naming the "
          "direction. Under condition 1 the ends of Nᵢ have opposite signs of σ̃² − R², which forces the direction of σ². Reading "
          "used: any strictly monotone σ̃² on Nᵢ. Generator (b) accepts either direction; only the forced one can occur.", ""]
    T += ["## Files moved or created", "",
          "- **Register:** `register/references.yaml`, `register/figures.yaml`, `register/bibfmt.py`; `register/render.py` extended "
          "(citation, figure and include tokens; paper numbering on paper-visible text); `register/results.yaml` (citations; "
          "status of 3.2 and 6.5; after the run, 2.8 and 2.9); `register/tasks.yaml` (wording only).",
          "- **Sources:** `source/thesis_only/{signature, reparameterisation, structural-stability, normal-form, "
          "tau-optimal-normal-form}.md` (verbatim imports); edits to `source/Stages_0_4_Source.md`, `source/Roadmap_v3_Source.md`, "
          "`source/figs/*`, `source/phase1/ERRATA.md` (17 pages).",
          "- **Renders:** `Stages_0_4_Thesis.md`, `Stages_0_4_Paper2.md` (one line break moved), `Roadmap_v3.md`, "
          "`Appendix_A_Register.md`, new `Appendix_B_Figures.md`, `Appendix_C_References.md`, `Appendix_D_Verification.md`, "
          "`Appendix_E_Reproduction.md`, and `reference/phase1/`.",
          "- **Figures:** `figs_thesis/B.n_<key>.png` (B.1–B.12) and `.pdf` (all except B.3, whose script writes PNG only); the "
          "captions `figs_thesis/B.n_<key>.txt` replace `figs_thesis/fig*.txt`. `figs_paper2/` is untouched.",
          "- **Code:** `t15/` with `t15_register.py`, `make_sources_t15.py`, `fig_harness.py`, `make_figs_thesis.py` (writes "
          "`gen/gen_figs_t13.py` and `gen/gen_figs_t8.py`), `make_fig_B2.py`, `make_appendix_de.py`, `t15_checks.py`, "
          "`t15_partG.py`, `t15_diag.py`, `make_results_t15.py`, `bib_check.md`, `input/` (the draft and the prompt) and "
          "`results/`.", "",
          "## Regenerate everything", "", "From `classification/`:", "", "```",
          "python3 t15/t15_register.py",
          "python3 t15/make_figs_thesis.py",
          "python3 register/render.py --numbering thesis && python3 register/render.py --numbering paper",
          "python3 t15/make_appendix_de.py --with-t15",
          "python3 t15/t15_checks.py && python3 t15/t15_partG.py C11 C12 ILL",
          "```", "", "Appendix E gives the full chain, Tasks 1–15.", ""]
    # For the author
    h2 = c["H2"]
    T += ["## For the author", "",
          "### 1. Part H.2: the manuscript PDF", "",
          f"`reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf`: `pdfinfo` reports **{h2['pages']} pages**, producer "
          f"{h2['producer']}, {h2['bytes']:,} bytes, sha256 `{h2['sha256']}`. This is the **same file** as yours.",
          "",
          "- ERRATA's \"18 pages\" was my error: splitting `pdftotext` output on form feeds gives an empty 18th element. It is "
          "corrected to 17.",
          "- Each cited page holds its quote (`pdftotext -f n -l n`): "
          + ", ".join(f"{k} p. {v['page']} {'yes' if v['found_on_page'] else 'NO'}" for k, v in h2["errata"].items()) + ".", "",
          "### 2. Part C.4: what each figure plots", ""]
    T += [f"- **Figure {e['label']}** (`{e['key']}`; script `{e['script']}`). {e['description']}" for e in figs]
    T += ["", "### 3. Part C.2: text elements changed", ""]
    ch = {k: v["text_changes"] for k, v in c["C7"]["figures"].items()}
    for e in figs:
        if e["label"] == "B.2":
            T.append("- **B.2:** new figure; its labels use words and symbols only.")
        else:
            d = ch.get(e["label"], [])
            T.append(f"- **{e['label']}:** " + ("; ".join(f"`{a[1]}` → `{b[1]}`" for a, b in d) if d else "no text element changed (none carried a number)."))
    T += ["", "### 4. Part F.3: statements of 3.1, 3.5 and 6.13 in the manuscript", "",
          "**3.1 = Proposition 1 (p. 3).** \"The stationary variance of (1) is σ²(Π) = (Σ + ½G²/Π)/(λ + G). (2) If G → 0 and G²/Π → 0 "
          "as Π → 0, then σ² tends to the floor F = Σ/λ. If G → G∞ ∈ (0, ∞) as Π → ∞, it tends to the high-precision limit "
          "H = Σ/(λ + G∞) < F.\" Proof: x is an Ornstein–Uhlenbeck process with rate a = λ + G and noise intensity "
          "D = G²/Π + 2Σ, so its stationary variance is D/(2a).", "",
          "**3.5 = Proposition 3 (p. 4), \"steady-state Kalman–Bucy filter [9]\".** \"For this plant, the steady-state Riccati equation "
          "0 = 2Σ − 2λp − Πp² gives G⋆(Π) = pΠ = −λ + √(λ² + 2ΣΠ), σ⋆²(Π) = p = 2Σ/(λ + √(λ² + 2ΣΠ)). (4) G⋆ also minimizes (2) over "
          "constant gains, so σ²(Π) ≥ σ⋆²(Π) for every gain.\" It continues: \"This is standard. The remark used below is that σ⋆² "
          "decreases strictly from F, so G⋆ = σ⋆²Π ≤ FΠ.\"", "",
          "**6.13 = Proposition 6 (p. 7).** \"M_L = (ϕ²L²r + q)/(1 − ϕ²(1 − L)²), S_L = (1 − L)²M_L + L²r, S_L − F = (M_L − F)/ϕ², and "
          "M_L > F ⟺ S_L > F ⟺ L/(2 − L) > FΠ_d. (10) The steady-state Kalman gain L⋆ satisfies L⋆/(2 − L⋆) < ½FΠ_d for every "
          "Π_d > 0.\" Proof: see the manuscript's Appendix A (p. 14).", "",
          "### 5. Part G outcomes", "",
          f"- **C11 (Corollary 2.8):** {V(g11.get('pass'))}, with class mismatches {g11.get('class_mismatches')} and signature "
          f"mismatches {g11.get('signature_mismatches')}. The exploratory run with more turning points gave "
          f"{gx.get('class_mismatches')} and {gx.get('signature_mismatches')}.",
          f"- **C12 (Proposition 2.9):** {V(g12.get('pass'))}, {g12.get('mismatches')} mismatches.",
          f"- **Illustration:** violating only condition 2 changes the class ({ill.get('class_before')} → {ill.get('class_after')}).",
          "- **Ambiguity:** see Part G detail above. It is not blocking.", "",
          "### 6. Where references 46–53 belong", "",
          "From the register's citation table: the result, the line of its heading in `classification/source/Stages_0_4_Source.md`, "
          "and the reference number.", "", "| Ref. | Key | Result (thesis no., key) | Source line |", "|---|---|---|---|"]
    reg = yaml.safe_load(open(os.path.join(CLS, "register", "results.yaml")))
    refs = {r["key"]: r["number"] for r in yaml.safe_load(open(os.path.join(CLS, "register", "references.yaml")))}
    src = open(os.path.join(CLS, "source", "Stages_0_4_Source.md")).read().split("\n")
    for k, n in sorted(refs.items(), key=lambda kv: kv[1]):
        if n < 46:
            continue
        for e in reg:
            if k in e["citations"]:
                ln = next((i + 1 for i, l in enumerate(src) if l.startswith("**[[" + e["key"] + "]]")), None)
                T.append(f"| [{n}] | {k} | {e['thesis_no']} `{e['key']}` | {ln} |")
    T += ["", "### 7. Disagreements with the attached draft (listed, not resolved)", "",
          "1. **Figure B.1 caption.** The draft calls it \"the variance curve of the starting relay with its critical-tolerance "
          "diagram\", and §2.4 says \"the variance curve\". The image (fig01) is a schematic curve, a sum of three Gaussian bumps "
          "and a logistic step with no filtering parameters, not the relay's variance.",
          "2. **Task 13 audit of the design sweeps (§4.1, §4.4 Verification).** The draft says the Task 13 audit repeated the "
          "design-sweep check \"with no class outside the stated sets\". That is true, but row 12 of the Task 13 class audit (the Π₀ "
          "sweep of tanh, exp and Hill gains) **failed** its pre-registered rule: 122 persisting route disagreements, attributed to "
          "code (`t13/RESULTS_t13.md`, diagnosis 7). §4.4 should say so if it cites the audit.",
          "3. **Planned references.** The draft's Appendix C says [46]–[53] are cited in chapters 5–9; the Task 15 prompt says "
          "chapters 6–7. The register's attachments put them on results 6.10, 6.19, 7.1, 7.2, 7.5, 7.6, 7.8, 7.11, 7.12 and 7.16 "
          "(table above), so chapters 6–7.",
          "4. **Figure B.2 axis.** The draft and prompt ask for q from 0 to about 4. The R²_rel = 2 boundary approaches q = 4 from "
          "above (q₊ → 2R²_rel), so the figure uses 0–5 to show it.",
          "5. **Label collision.** The figure labels B.1–B.12 have the same form as, and for B.1–B.12 the same text as, the legacy "
          "labels B.1–B.12 kept in `register/crosswalk.md` (B.1 = 2.1 topological realizability, …). Thesis-facing text uses only "
          "figure labels, but a reader of the crosswalk could confuse the two. This is why C10 fails.",
          "6. **Theorem 3.2 labelling.** The draft states \"Theorem 3.2(a) (normal form)\" with the partial derivatives as unlabelled "
          "text; the register has 3.2 as one theorem. The thesis-only import keeps the draft's text verbatim.", "",
          "## Provenance", "",
          f"- Pre-registration {PREREG}; artifacts {ARTIFACTS}; results {commit}.",
          f"- Runtimes: checks {sum(v.get('seconds', 0) for v in C.values()):.0f} s (C7 reruns the original figure scripts); "
          f"Part G C11 {g11.get('seconds')} s, C12 {g12.get('seconds')} s, exploratory C11X {gx.get('seconds')} s.",
          "- Seeds: 15001/15002 (C11), 15101/15102 (C12), 15201 (illustration), 15301/15302 (exploratory)."]
    open(os.path.join(CLS, "RESULTS_t15.md"), "w").write("\n".join(T) + "\n")
    print("written")


if __name__ == "__main__":
    main()
