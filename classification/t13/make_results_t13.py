"""Builds RESULTS_t13.md from results/*.json. Usage: python3 make_results_t13.py [code_commit_hash]"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
PREREG = "296a797"
CODE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "(not yet committed)"


def L(n):
    p = os.path.join(RES, n)
    return json.load(open(p)) if os.path.exists(p) else None


V = lambda ok: "**PASS**" if ok else "**FAIL**"
g = lambda x, f=".3g": format(float(x), f) if x is not None and not isinstance(x, str) else str(x)
sym, symd, reg = L("t13_partA_symbolic.json"), L("t13_partA_symbolic_diag.json"), L("t13_regression_symbolic.json")
num = {}
for fn in sorted(glob.glob(os.path.join(RES, "t13_partA_numeric_*.json"))):
    if fn.endswith("_diag.json"):
        continue
    num.update(json.load(open(fn)))
numd = L("t13_partA_numeric_diag.json")
a3att, a3pr, a3cl = L("t13_A3_attempt.json"), L("t13_A3_proof.json"), L("t13_A3_closed.json")
c1, c1r1, c3 = L("t13_audit_numbers.json"), L("t13_audit_numbers_run1.json"), L("t13_audit_refs.json")
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(RES, "c2_rows", "row_*.json")))]
cmp_ = L("t13_compare_repro.json")
man = L("repro_manifest.json")
env = L("env.json") or {}
rt = {}
for fn in ("runtime.tsv",):
    p = os.path.join(RES, fn)
    if os.path.exists(p):
        rt.update({a: float(b) for a, b in (l.split("\t") for l in open(p).read().splitlines() if l.strip())})
for p in glob.glob(os.path.join(RES, "*.time")):
    k = os.path.basename(p)[:-5]
    for l in open(p):
        if l.startswith("real"):
            m_, sec = l.split()[1].rstrip("s").split("m")
            rt.setdefault(k, 60 * float(m_) + float(sec))


def items_ok(d, key):
    return all(it["pass"] for it in d.get(key, []))


def n_items(d, key):
    v = d.get(key, [])
    return f"{sum(it['pass'] for it in v)}/{len(v)}"


A = num
c2_pass = bool(rows) and len(rows) == 42 and all(r["pass"] for r in rows)
rowsT = [
    ("Part A symbolic (A1, A2, A4, A5, A7, A8)", V(sym["pass"]), f"{sum(it['pass'] for k, v in sym.items() if isinstance(v, list) and k != 'lines' for it in v if isinstance(it, dict) and 'pass' in it)}/{sym['n']} items; "
     "failing: " + "; ".join(it["desc"] for k, v in sym.items() if isinstance(v, list) and k != "lines" for it in v if isinstance(it, dict) and not it.get("pass", True))
     + f". Diagnosis: both identities verified by a rewrite route ({'yes' if symd and symd['pass'] else 'no'})", rt.get("t13_partA_symbolic")),
    ("A-reg: Tasks 8–12 symbolic regression", V(reg["pass"]), f"{reg['n_pass']}/{reg['n']} items; " + ", ".join(f"T{k[1:]} {v['n_pass']}/{v['n']}" for k, v in reg["by_task"].items())
     + f"; documented fallbacks used {len(reg['fallbacks'])}", rt.get("t13_regression_symbolic")),
    ("A1 numerical (10,000 sets, 100 digits)", V(A["A1"]["pass"]), f"failures {A['A1']['fail_counts'] or 0}; min dM/dx {g(A['A1']['min_dM'])}", None),
    ("A2 numerical (same sets)", V(A["A2"]["pass"]), f"failures {A['A2']['fail_counts']} (auxiliary cross-check only; diagnosis: "
     f"{numd['n_still_failing'] if numd else '?'} remain at higher precision, pre-registered links 0 failures)", None),
    ("A3 numerical (10,000 sets, 100 digits)", V(A["A3"]["pass"]), f"violations {A['A3']['n_violations']}; min dP_a/dx {g(A['A3']['min_dPa'])}, min dP_b/dx {g(A['A3']['min_dPb'])}", None),
    ("A3 symbolic attempt (pre-registered script)", "unresolved", "automated verdict 'unresolved' (float leak; coefficient-sign rule only)", None),
    ("A3 exact completion of the resultant route", V(a3pr["pass"]), f"{sum(it['pass'] for v in a3pr.values() if isinstance(v, list) for it in v if isinstance(it, dict) and 'pass' in it)} checks", None),
    ("A3 closed form (referee point 5)", V(a3cl["pass"]), "a0 = -a1; p = 2/(1 + sqrt(1 + 2u/k)), k = (1+u) x coth(x/2) - 2u increasing", None),
    ("A4 numerical (10,000 curves, 0 < β < 2)", V(A["A4"]["pass"]), f"turning points {A['A4']['kinds_hist']}; max Φ_τ residual {g(A['A4']['max_Phi_tau_rel'])}; "
     f"Φ_ττ closed vs direct {g(A['A4']['max_closed_vs_direct_rel'])}", A["A4"]["seconds"]),
]
if "A5" in A:
    rowsT.append(("A5 regression + 5,000 Hill sets (real n)", V(A["A5"]["pass"]), "Π0_pair: " + ", ".join(f"n = {r['n']}: {g(r['closed_form'], '.12g')} (rel {g(r['rel'])})" for r in A["A5"]["regression"])
                  + f"; mismatches {A['A5']['n_fail']} of {A['A5']['n']} (pair predicted in {A['A5']['n_pair_pred']})", A["A5"]["seconds"]))
if "A7" in A:
    rowsT.append(("A7 numerical (10,000 sets, 60 digits)", V(A["A7"]["pass"]), f"failures {A['A7']['n_fail']}; min (V − P)/P {g(A['A7']['min_rel_gap'])}", A["A7"]["seconds"]))
rowsT += [
    ("C1 numbers, first run", V(c1r1["pass"]) if c1r1 else "—", f"failing entries {c1r1['n_fail_entries']} (4 document: 0.0099504 truncated; 2 code: parser)" if c1r1 else "", None),
    ("C1 numbers, after the fixes", V(c1["pass"]), f"{c1['n_literals']} literals; {len(c1['entries'])} registry entries ({c1['n_formula']} formulas); {len(c1['ids'])} identifiers; unmatched {len(c1['unmatched'])}", None),
    ("C2 classes (42 rows × 1,000 sets × 100 tolerances)", V(c2_pass) if len(rows) == 42 else f"{len(rows)}/42 rows done",
     f"rows passing {sum(r['pass'] for r in rows)}/{len(rows)}; classifications {sum(r['classifications'] for r in rows):,}; flagged {sum(r['flagged'] for r in rows)}; "
     f"persisting {sum(r['persisting'] for r in rows)}", sum(r["seconds"] for r in rows) if rows else None),
    ("C3 references and labels", V(c3["pass"]), f"{c3['n_results']} results, {c3['n_refs_checked']} references, {c3['n_errors']} errors", None),
    ("C4 independent referee", "record", "14 points, all valid, all fixed (dispositions below)", None),
]
if cmp_:
    done = {k: v for k, v in cmp_["reports"].items() if "pass" in v}
    rowsT.append(("D reproduction (Tasks 8–12 reports)", V(cmp_["pass"]), "; ".join(f"T{k}: {'identical' if v['pass'] else str(v['n_issues']) + ' issues'}" for k, v in done.items())
                  + ("" if len(done) == 5 else f"; not reproduced: {sorted(set(cmp_['reports']) - set(done))}"), None))

T = ["# Task 13 — finalize Stages 0–4: results", "",
     f"Pre-registration `classification/PREREG_t13.md`, commit **{PREREG}**; code and results commit **{CODE}**. Python "
     f"{env.get('python', '?')}, mpmath {env.get('mpmath', '?')}, SymPy {env.get('sympy', '?')}, {env.get('cpus', '?')} CPUs.", "",
     "| Check | Verdict | Counts / worst errors | Runtime (s) |", "|---|---|---|---|"]
for n, v, m, t in rowsT:
    T.append(f"| {n} | {v} | {m} | {'' if t is None else f'{t:.0f}'} |")
fails = [n for n, v, _, _ in rowsT if v == V(False)]
T += ["", "**Pre-registered checks that FAIL:** " + ("; ".join(fails) if fails else "none") + ". Each is diagnosed below.", ""]

T += ["## Part A outcomes", "", "| Item | Outcome | New label (consolidated document) |", "|---|---|---|",
      "| A1 Prop. 2.6(b), optimal M-P prior increasing | **proved** (verified: every step symbolic, 10,000 sets with 0 failures) | Theorem 32(b) |",
      "| A2 Num. 2.6c, optimal M-P time average increasing | **proved** (new route via $P^+ = F/(1+\\mu)$; final bound $\\sinh 2x \\ge 2x$) | Theorem 32(c) |",
      "| A3 Num. 2.8 / 4.10a, integrate-and-dump monotone | **proved** (exact resultant route completed post hoc; closed form $p = 2/(1 + \\sqrt{1 + 2u/k(x)})$ found in response to the referee) | Theorem 35 |",
      "| A4 Num. 4.6a, power family unimodal for $0 < \\beta < 2$ | **proved** (every critical point is a strict maximum: $\\Phi_{\\tau\\tau} = P^2(\\beta + (2-\\beta)\\lambda^2\\tau^2)/\\tau^3$) | Theorem 25 |",
      "| A5 Conj. 3.10, Hill gain every $n > 1$ | **proved** for every real $n > 1$ (Descartes on a cubic with signs $+, ?, -, -$) | Theorem 56 |",
      "| A6 Conj. 2.11, sampled relays at most two turning points | **unresolved** (no route; evidence below) | Conjecture 38 |",
      "| A7 Num. 3.5 (Stage 2), strict gap $P < V$ | **proved** (orthogonality fails through the $e^{-u/\\tau}$ term; compactness) | Proposition 20 |",
      "| A8 Conj. 4.11, non-linear causal garblings | **proved** for additive stationary Gaussian noise (fixed-lag limit + frequency localization; referee found no gap) | Theorem 69 |", ""]
a6 = [r for r in rows if 24 <= r["row"] <= 32]
if a6:
    T += [f"A6 evidence (C2 rows 24–32, 9,000 new curves): maximum number of turning points per row "
          + ", ".join(f"{r['name']}: {r['max_turning_points']}" for r in a6) + "; Task 12: 6,000 sets × 3 metrics, never more than two.", ""]

T += ["## Plain statements", "",
      "- **Did any result in Stages 0–4 change?** No theorem, proposition or class was overturned. Labels changed where Part A "
      "proved something (six items became theorems or propositions; A1 verified). The audit and the referee found document "
      "errors that are now corrected and logged: a truncated worked value (0.0099504 → 0.0099505), D2's unstated requirement "
      "$c < 2$ (with $c = 3$ the excess set is all of $(0,\\infty)$, not a lower ray), the condition column of rows 25–26 "
      "(\"two rays iff $G > 2F\\Pi$\" is only \"if\"), missing equality rows (optimal prior/avg at $R^2 = \\sigma_\\star^2$; capped "
      "gain at $g = 2F$), and several missing hypotheses (C2 in Proposition 36, continuity in Corollary 66, windows in "
      "Corollary 59). One class list changed: the C2 audit of row 8 (two-stage Bayesian) never observed the stated $(1,0,1)$, and the post-hoc diagnosis proved it impossible (Theorem 6 addendum: for increasing $G$ with $G/\\Pi$ strictly decreasing, every interior minimum exceeds $F$); row 8's set is corrected (change log row 45). The pre-registered C2 verdict for row 8 stays FAIL.",
      "- **Did any class outside the stated sets appear?** " + (
          ("No: the class audit found 0 persisting out-of-set classes and 0 persisting route disagreements in "
           f"{sum(r['classifications'] for r in rows):,} classifications." if c2_pass else
           "See the C2 section: " + "; ".join(f"row {r['row']} ({r['name']}): out of set {r['out_of_set']}, missing {r['missing_stated']}, persisting {r['persisting']}" for r in rows if not r["pass"]))
          if len(rows) == 42 else "C2 incomplete."),
      "- **What remains open?** Conjecture 38 (sampled relays have at most two turning points), Numerical result 58 (two-stage "
      "gains), a necessary condition for monotone optimal error beyond the power family, and Stage 6 (α–β, multivariate). "
      "Consolidated Section 11 states each with its evidence.", ""]

T += ["## Diagnoses and fixes", "",
      "1. **Part A symbolic, two route failures (attribution: criterion/route).** The sign of $-sFr$ (A1 item 2) is not decided by "
      "SymPy's assumptions because $1 - e^{-2x}$ is not known positive; the A2 identity with $\\sinh$ is not reduced by the "
      "pre-registered routes. Both reduce to 0 after `rewrite(exp)` / an explicit positive series (`t13_partA_symbolic_diag.py`).",
      "2. **Code bug (fixed before the recorded run of the symbolic script).** A2 item 4 had a sign typo ($-E\\cdot G$ for "
      "$+E\\cdot G$) contradicting the pre-registered identity; fixed, then the script was re-run (66/68).",
      f"3. **A2 numerical (attribution: code).** The auxiliary cross-check $\\bar P(\\mu) = \\bar P(M)$ to 1e-80 (not a "
      f"pre-registered link) failed in {A['A2']['fail_counts'].get('Pbar(mu) = Pbar(M)', 0)} sets, all at $\\lambda\\Delta t \\ge 26.6$, "
      "because $F - M$ cancels about $2x/\\ln 10$ digits. With $100 + 2x/\\ln 10 + 30$ digits all agree to "
      f"{g(numd['max_rel']) if numd else '?'} (`t13_partA_numeric_diag.py`). Every pre-registered A2 link had 0 failures.",
      "4. **A3 (attribution: code; outcome completed post hoc).** The pre-registered attempt script leaked floats (Python integer "
      "division) and its automatic verdict only checked coefficient signs of polynomials in $(x, E, u)$, so it reported "
      "'unresolved'. Completing the same resultant route in exact arithmetic (`t13_A3_proof.py`) shows the resultant is "
      "$4u^2x^2(u+1)^2(E-1)^4(E^2 + 2xE - 1)^2$ and $E^2 + 2xE - 1 = -2e^{-x}(\\sinh x - x) < 0$ on $E = e^{-x}$, so the derivative "
      "never vanishes. The referee's request to print the quadratic then exposed $a_0 = -a_1$ and a closed form "
      "(`t13_A3_closed.py`, 11/11), which proves monotonicity and both limits directly. `t13_A3_limits.py` (a series attempt at the "
      "limits) is superseded: SymPy's limit route failed at $x \\to \\infty$, which the closed form settles.",
      "5. **C1 first run (attribution: document 4, code 2).** $G^\\star = \\sigma_\\star^2$ at $\\Pi = 1$ is 0.00995049…, stated as 0.0099504 "
      "(truncated; T8.2 checked 4 s.f.); corrected to 0.0099505 everywhere (change log row 29). The parser mis-read plain "
      "`10^{12}` (code); fixed. After the referee fixes the registry was extended to the new literals (three entries) and the "
      "run repeated: PASS.",
      "6. **compare_repro.py (code, before any recorded comparison).** A `|z|` inside a table cell shifted the runtime column, and "
      "reports not yet regenerated in the worktree were compared with themselves; fixed (last-cell masking; only tasks in the "
      "replay's runtime logs are compared).",
      "7. **C2 row 12, Pi0 monotone (attribution: code).** 122 persisting disagreements in 23 sets, all at $R^2$ exactly $L_-$ on "
      "increasing curves whose approach to $L_-$ is exponentially flat ($\\tanh$, $\\exp$ shapes). With no split point, route (ii) "
      "tests one point ($P_0 = 1$), where $f - R^2$ is below its 1e-40 relative equality tolerance, so it reads Empty; at "
      "$P_0 = 10\\Pi$ the gap is positive in every case, and the failure set is All, as route (i) says. No document change.",
      "8. **C2 row 8, two-stage Bayesian (attribution: document).** $(1,0,1)$ was never observed (0 in 1,000 sets, 0 in 400,000 "
      "further screened draws). Proved impossible post hoc (Theorem 6 addendum, "
      "`t13_audit_classes_diag2.py`); row 8's stated set corrected (change log row 45). The pre-registered verdict stays FAIL.", ""]
bad_rows = [r for r in rows if not r["pass"]]
if rows:
    T += ["## C2 class audit", "", "| # | Row | Stated | Observed classes | Turning points | Flagged | Persisting | Verdict |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        T.append(f"| {r['row']} | {r['name']} | {', '.join(r['stated'])} | {r['classes']} | {r['kinds_hist']} | {r['flagged']} | "
                 f"{r['persisting']} | {V(r['pass'])} |")
    T.append("")
    if bad_rows:
        T += ["Failing rows: " + "; ".join(f"row {r['row']}: missing {r['missing_stated']}, out of set {r['out_of_set']}, persisting "
              f"{r['persisting']}" for r in bad_rows) + ". Diagnosis in `t13_audit_classes_diag.json` if present and below.", ""]
    for fn in ("t13_audit_classes_diag.json", "t13_audit_classes_diag2.json"):
        dg = L(fn)
        if dg:
            T += [f"`{fn}`: " + dg.get("text", ""), ""]

ref = open(os.path.join(HERE, "referee_report.md")).read().split("\n", 1)[1]
T += ["## Independent referee (C4): report and dispositions", "", ref.strip(), ""]

T += ["## Reproducibility (Part D)", ""]
if man:
    tot = sum(man["runtime_s"].values())
    T += ["Clean checkout: `git worktree` of the repository, replayed with `reproduce_all.sh` in four invocations: Task 8; "
          "Tasks 9–12 (restarted after a container restart interrupted the first run during Task 9; it stopped at Task 10, "
          "below); Tasks 11–12; Task 13 on the final commit. Task 10's runtime is the sum of its scripts' logged runtimes.",
          "", "| Task | Runtime (s) |", "|---|---|"] + [f"| {k} | {v:.0f} |" for k, v in man["runtime_s"].items()] + [
          "", f"Total measured wall time {tot:.0f} s ({tot / 3600:.1f} h) on {man.get('cpus', '?')} CPUs, sharing them with the Task 13 "
          f"audits; manifest with SHA-256 of {len(man.get('sha256', {}))} output files in `results/repro_manifest.json`. A "
          "reviewer with 4 CPUs and nothing else running should expect the original runtimes (Task 8 161 s, Task 9 631 s, Task "
          "10 5861 s, Task 11 4394 s, Task 12 8935 s, Task 13 as in the table above), about 5.6 h for Tasks 8–12.", ""]
t10d = L("t13_repro_t10_diag.json")
if t10d:
    T += ["**Task 10: FAIL as pre-registered** (the replay stopped with an error, so no report was regenerated). Diagnosis "
          "(`repro_t10_diag.py`): " + t10d["text"], ""]
if cmp_:
    T += ["Pre-registered comparison (`compare_repro.py`): " + "; ".join(
        f"Task {k} " + (v["status"] if "status" in v else ("PASS" if v["pass"] else f"FAIL ({v['n_issues']} issues, verdicts identical {v['verdicts_identical']})"))
        for k, v in cmp_["reports"].items()) + ".", ""]
    for k, v in cmp_["reports"].items():
        if v.get("issues"):
            T += [f"Task {k} differences: " + "; ".join(json.dumps(i, ensure_ascii=False)[:300] for i in v["issues"][:10]), ""]

T += ["## Deliverables", "",
      "- `classification/Stages_0_4_Consolidated.md`: the single source document (73 results, change log of 45 corrections).",
      "- `classification/Roadmap_v3.md`: status, open problems, final matrix, Stages 5–6, Paper 2 outline, novelty check.",
      "- `classification/figs_paper2/`: ten figures (PNG + PDF + caption each; `README.md` lists them).",
      "- `classification/reproduce_all.sh`, `t13/compare_repro.py`, `t13/run_t13.sh`.",
      "- `t13/literature_check.md` (queries and sources), `t13/referee_report.md`.", "",
      "## Provenance", "", "Runtime per script (s): " + ", ".join(f"{k} {v:.0f}" for k, v in sorted(rt.items())) + "."]
open(os.path.join(HERE, "RESULTS_t13.md"), "w").write("\n".join(T) + "\n")
print("\n".join(T[:24]))
