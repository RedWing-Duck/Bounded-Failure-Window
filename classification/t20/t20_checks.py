"""Task 20 checks C1-C6 (PREREG_t20.md). Run once, on the artifacts commit, from a clean working tree:
    python3 t20/t20_checks.py [--work DIR]          # recorded run: writes t20/results/t20_checks.json, logs/, c5_diffs.md
    python3 t20/t20_checks.py --verdict             # C5 verdict from t20/results/c5_attribution.yaml (manual reading, no re-run)
Base for every "committed" comparison: 7855e45. C2(f), C3 and C5 work in fresh local clones under --work (outside the
repository); nothing is written to the repository except t20/results/."""
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.path.join(HERE, "results")
BASE = "7855e45"
ART = "HEAD"   # set to the artifacts commit hash in main()
PY = sys.executable
sys.path.insert(0, os.path.join(CLS, "register"))
import bibfmt  # noqa: E402

PROMPT_REFS = {  # the Task 20 prompt's entries, verbatim (t20/input/Task20_prompt.md)
    54: ("sinopoli2004", "Sinopoli, B., Schenato, L., Franceschetti, M., Poolla, K., Jordan, M. I. & Sastry, S. S. (2004). Kalman filtering with intermittent observations. IEEE Transactions on Automatic Control 49(9), 1453–1464. doi:10.1109/TAC.2004.834121"),
    55: ("wu2018", "Wu, J., Shi, G., Anderson, B. D. O. & Johansson, K. H. (2018). Kalman filtering over Gilbert–Elliott channels: stability conditions and critical curve. IEEE Transactions on Automatic Control 63(4), 1003–1017. doi:10.1109/TAC.2017.2732821"),
    56: ("jiang2026", "Jiang, S., Shi, J. & Moura, S. (2026). Mitigating overconfidence in nonlinear Kalman filters via covariance recalibration. Automatica, accepted for publication; volume, pages and DOI not yet assigned. arXiv:2407.05717"),
    57: ("bosov2026", "Bosov, A., Bosov, S. & Uryupin, I. (2026). Beyond divergence: failure modes of the classical extended Kalman filter in a unified nonlinear tracking model. Mathematics 14(17), 3071. doi:10.3390/math14173071"),
    58: ("gotovos2013", "Gotovos, A., Casati, N., Hitz, G. & Krause, A. (2013). Active learning for level set estimation. Proceedings of the 23rd International Joint Conference on Artificial Intelligence (IJCAI 2013), 1344–1350. AAAI Press. https://dl.acm.org/doi/10.5555/2540128.2540322 (no DOI)"),
    59: ("tenne2002", "Tenne, D. & Singh, T. (2002). Characterizing performance of α-β-γ filters. IEEE Transactions on Aerospace and Electronic Systems 38(3), 1072–1087. doi:10.1109/TAES.2002.1039425"),
    60: ("sahomasugi2016", "Saho, K. & Masugi, M. (2016). α–β–γ tracking filters using acceleration measurements. SpringerPlus 5, 309. doi:10.1186/s40064-016-1960-8"),
}
DOIS = {54: "10.1109/TAC.2004.834121", 55: "10.1109/TAC.2017.2732821", 56: None, 57: "10.3390/math14173071", 58: None,
        59: "10.1109/TAES.2002.1039425", 60: "10.1186/s40064-016-1960-8"}
# every element of each prompt entry, as the BibTeX field (after bibfmt.tex) that must hold it
BIBFIELDS = {
    "sinopoli2004": {"author": "Sinopoli, B. and Schenato, L. and Franceschetti, M. and Poolla, K. and Jordan, M. I. and Sastry, S. S.",
                     "year": "2004", "title": "Kalman filtering with intermittent observations",
                     "journal": "IEEE Transactions on Automatic Control", "volume": "49", "number": "9", "pages": "1453–1464",
                     "doi": "10.1109/TAC.2004.834121"},
    "wu2018": {"author": "Wu, J. and Shi, G. and Anderson, B. D. O. and Johansson, K. H.", "year": "2018",
               "title": "Kalman filtering over Gilbert–Elliott channels: stability conditions and critical curve",
               "journal": "IEEE Transactions on Automatic Control", "volume": "63", "number": "4", "pages": "1003–1017",
               "doi": "10.1109/TAC.2017.2732821"},
    "jiang2026": {"author": "Jiang, S. and Shi, J. and Moura, S.", "year": "2026",
                  "title": "Mitigating overconfidence in nonlinear Kalman filters via covariance recalibration", "journal": "Automatica",
                  "note": "accepted for publication; volume, pages and DOI not yet assigned", "eprint": "2407.05717"},
    "bosov2026": {"author": "Bosov, A. and Bosov, S. and Uryupin, I.", "year": "2026",
                  "title": "Beyond divergence: failure modes of the classical extended Kalman filter in a unified nonlinear tracking model",
                  "journal": "Mathematics", "volume": "14", "number": "17", "pages": "3071", "doi": "10.3390/math14173071"},
    "gotovos2013": {"author": "Gotovos, A. and Casati, N. and Hitz, G. and Krause, A.", "year": "2013",
                    "title": "Active learning for level set estimation",
                    "booktitle": "Proceedings of the 23rd International Joint Conference on Artificial Intelligence (IJCAI 2013)",
                    "pages": "1344–1350", "publisher": "AAAI Press", "url": "https://dl.acm.org/doi/10.5555/2540128.2540322"},
    "tenne2002": {"author": "Tenne, D. and Singh, T.", "year": "2002", "title": "Characterizing performance of α-β-γ filters",
                  "journal": "IEEE Transactions on Aerospace and Electronic Systems", "volume": "38", "number": "3",
                  "pages": "1072–1087", "doi": "10.1109/TAES.2002.1039425"},
    "sahomasugi2016": {"author": "Saho, K. and Masugi, M.", "year": "2016", "title": "α–β–γ tracking filters using acceleration measurements",
                       "journal": "SpringerPlus", "volume": "5", "pages": "309", "doi": "10.1186/s40064-016-1960-8"},
}
NEW_TITLES = {"2.1": "Topological realisability", "2.8": "Reparameterisation (orientation swaps ℓ and h)",
              "5.1": "Gain realisability", "6.17": "D3 excess set; onset ρ > 2 + ν",
              "6.19": "Optimal M-P along Δt: posterior ↓; prior ↑; averaged ↑"}
LEMMA_ROW = "| 7.6a | Lemma | Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6) | `whole-path-garbling` | — | to-verify |"
RECORDED_T13 = ("- Recorded — A3 (Theorem 7.15): the pre-registered resultant route, completed post hoc in exact arithmetic "
                "(`t13/t13_A3_proof.py`, 22 of 22 checks; the pre-registered attempt `t13_A3_attempt.py` reported 'unresolved'): the "
                "resultant of the cleared quadratic and its x-derivative is 4u²x²(u + 1)²(E − 1)⁴(E² + 2xE − 1)², and E² + 2xE − 1 = "
                "−2e^(−x)(sinh x − x) < 0 on E = e^(−x), so dp/dx never vanishes.")
CHECK_SCRIPTS = ["t15/t15_checks.py", "t15/t15_partG.py", "t16/t16_checks.py", "t17/t17_checks.py", "t18/t18_checks.py",
                 "t19/t19_checks.py"]
CHECK_JSON = {"t15/t15_checks.py": "t15/results/t15_checks.json", "t15/t15_partG.py": "t15/results/t15_partG.json",
              "t16/t16_checks.py": "t16/results/t16_checks.json", "t17/t17_checks.py": "t17/results/t17_checks.json",
              "t18/t18_checks.py": "t18/results/t18_checks.json", "t19/t19_checks.py": "t19/results/t19_checks.json"}
BYPRODUCTS = {"classification/t15/results/cap_new_t13.pkl", "classification/t15/results/cap_new_t8.pkl",
              "classification/t15/results/cap_B2.pkl", "classification/register/tasks.yaml"}


def sh(cmd, cwd=REPO, check=True, **kw):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)
    if check and r.returncode:
        raise RuntimeError(f"{cmd}: {r.stderr}")
    return r


def show(path, commit=BASE):
    return sh(["git", "show", f"{commit}:{path}"]).stdout


def show_bytes(path, commit=BASE):
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=REPO, capture_output=True, check=True).stdout


def cur(path):
    return open(os.path.join(REPO, path), encoding="utf-8").read()


def clone(work, name, commit):
    d = os.path.join(work, name)
    sh(["git", "clone", "-q", "--no-hardlinks", REPO, d])
    sh(["git", "checkout", "-q", "--detach", commit], cwd=d)
    return d


def chain_steps(clsdir):
    """Render-chain commands from that commit's Appendix E (the code block of the render chain), without the Task 15 checks line."""
    t = open(os.path.join(clsdir, "Appendix_E_Reproduction.md")).read()
    block = t.split("render chain")[1].split("```")[1]
    cmds = []
    for ln in block.split("\n"):
        ln = ln.split("#")[0].strip()
        if ln.startswith("python3 ") and "t15_checks" not in ln:
            cmds.append(ln.split()[1:])
    return cmds


def run_logged(args, cwd, log, timeout=7200):
    t0 = time.time()
    with open(log, "w") as fh:
        r = subprocess.run([PY] + args, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout)
    return {"cmd": " ".join(["python3"] + args), "rc": r.returncode, "seconds": round(time.time() - t0, 1),
            "last_line": (open(log).read().strip().split("\n") or [""])[-1][:300]}


# ------------------------------------------------------------------------------------------------------------------ C1
def C1():
    base = show("classification/Appendix_A_Register.md").split("\n")
    exp = []
    for ln in base:
        cells = ln.split(" | ")
        if ln.startswith("| ") and len(cells) >= 6:
            no = cells[0][2:]
            if no in NEW_TITLES:
                cells[2] = NEW_TITLES[no]
                ln = " | ".join(cells)
        exp.append(ln)
    i81 = next(i for i, l in enumerate(exp) if l.startswith("| 8.1 |"))
    i82 = next(i for i, l in enumerate(exp) if l.startswith("| 8.2 |"))
    r81, r82 = exp[i81], exp[i82]                                           # base: 8.1 blind-searches, 8.2 narrow-windows
    exp[i81], exp[i82] = "| 8.1 |" + r82[len("| 8.2 |"):], "| 8.2 |" + r81[len("| 8.1 |"):]
    i76 = next(i for i, l in enumerate(exp) if l.startswith("| 7.6 |"))
    exp.insert(i76 + 1, LEMMA_ROW)
    now = cur("classification/Appendix_A_Register.md").split("\n")
    diff = [l for l in difflib.unified_diff(exp, now, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
    reg = yaml.safe_load(cur("classification/register/results.yaml"))
    keys, nos = [e["key"] for e in reg], [e["thesis_no"] for e in reg]
    out = {"expected_equals_rendered": not diff, "unexpected_differences": diff[:20], "entries": len(reg),
           "keys_unique": len(set(keys)) == len(keys), "thesis_no_unique": len(set(nos)) == len(nos),
           "row_8.1": now[next(i for i, l in enumerate(now) if l.startswith("| 8.1 |"))],
           "row_8.2": now[next(i for i, l in enumerate(now) if l.startswith("| 8.2 |"))],
           "row_after_7.6": now[next(i for i, l in enumerate(now) if l.startswith("| 7.6 |")) + 1]}
    out["pass"] = bool(not diff and len(reg) == 83 and out["keys_unique"] and out["thesis_no_unique"])
    return out


# ------------------------------------------------------------------------------------------------------------------ C2
def C2(work):
    base = show("classification/Appendix_C_References.md").split("\n")
    now = cur("classification/Appendix_C_References.md").split("\n")
    k53 = next(i for i, l in enumerate(base) if l.startswith("[53] "))
    prefix_same = now[:k53 + 2] == base[:k53 + 2]
    tail = [l for l in now[k53 + 2:] if l.strip()]
    refs = yaml.safe_load(cur("classification/register/references.yaml"))
    bykey = {r["key"]: r for r in refs}
    bib = bibfmt.parse(os.path.join(CLS, "references.bib"))
    order = [PROMPT_REFS[n][0] for n in range(54, 61)]
    fmt_ok, fmt_err = {}, {}
    for n in range(54, 61):
        k = PROMPT_REFS[n][0]
        try:
            fmt_ok[k] = bibfmt.fmt(n, bib[k])
        except Exception as e:   # noqa: BLE001
            fmt_err[k] = repr(e)
    tail_ok = (len(tail) == 7 and all(tail[i] == fmt_ok.get(order[i]) for i in range(7))
               and all(tail[i].startswith(f"[{54 + i}] ") for i in range(7)))
    reg_ok = ([r["number"] for r in refs] == list(range(1, 61)) and len(bykey) == 60
              and bykey["roberts1959"]["number"] == 26 and bykey["sahomasugi2016"]["number"] == 60
              and all(bykey[k]["number"] == n and bykey[k]["status"] == "cited"
                      and bykey[k]["first_cited"] == "draft §1.6 Contributions and relation to prior work"
                      for n, (k, _) in PROMPT_REFS.items()))
    doi = {n: bib[PROMPT_REFS[n][0]].get("doi") for n in range(54, 61)}
    doi_ok = all(doi[n] == DOIS[n] for n in DOIS)
    res = yaml.safe_load(cur("classification/register/results.yaml"))
    de = next(e for e in res if e["key"] == "discrete-excess")
    cited_by = {k: [e["key"] for e in res if k in e["citations"]] for k in order}
    attach_ok = (de["citations"] == ["roberts1959", "sahomasugi2016"]
                 and all(not cited_by[k] for k in order[:6]) and cited_by["sahomasugi2016"] == ["discrete-excess"]
                 and set(bykey) == set(bib))
    # (f) collision test in a scratch clone
    d = clone(work, "c2_collision", ART)
    c = os.path.join(d, "classification")
    steps = [["t14/build_register.py"], ["t15/t15_register.py"], ["t16/t16_register.py"], ["t19/t19_register.py"],
             ["t20/t20_register.py"]]
    snap = []
    for p in range(2):
        for s in steps:
            r = subprocess.run([PY] + s, cwd=c, capture_output=True, text=True)
            assert r.returncode == 0, (s, r.stderr)
        snap.append({f: open(os.path.join(c, "register", f)).read() for f in ("results.yaml", "references.yaml")})
    r = subprocess.run([PY, "t19/t19_register.py"], cwd=c, capture_output=True, text=True)
    snap.append({f: open(os.path.join(c, "register", f)).read() for f in ("results.yaml", "references.yaml")})
    committed = {f: cur(f"classification/register/{f}") for f in ("results.yaml", "references.yaml")}
    collision = {"pass1_equals_committed": snap[0] == committed, "pass2_equals_pass1": snap[1] == snap[0],
                 "t19_alone_after_changes_nothing": snap[2] == snap[1], "t19_alone_output": r.stdout.strip()}
    out = {"a_lines_1_53_byte_identical": prefix_same, "b_entries_54_60": tail, "b_tail_matches_bibfmt": tail_ok,
           "b_register_numbers_keys": reg_ok, "c_bibfmt_errors": fmt_err, "d_doi": doi, "d_doi_ok": doi_ok,
           "e_6.13_citations": de["citations"], "e_cited_by": cited_by, "e_ok": attach_ok, "f_collision": collision}
    out["pass"] = bool(prefix_same and tail_ok and reg_ok and not fmt_err and doi_ok and attach_ok
                       and all(v for k, v in collision.items() if k != "t19_alone_output"))
    return out


# ------------------------------------------------------------------------------------------------------------------ C3
def totals(text):
    cs = [tuple(map(int, m)) for m in re.findall(r"(\d+) checks with a verdict; (\d+) pass, (\d+) fail", text)]
    return {"checks": sum(c[0] for c in cs), "pass": sum(c[1] for c in cs), "fail": sum(c[2] for c in cs),
            "failure_lines": len(re.findall(r"^- Failure — ", text, re.M)), "recorded_lines": len(re.findall(r"^- Recorded — ", text, re.M))}


def C3(art_clone):
    base = show("classification/Appendix_D_Verification.md")
    regen = open(os.path.join(art_clone, "classification", "Appendix_D_Verification.md")).read()
    committed = cur("classification/Appendix_D_Verification.md")
    B, N = base.split("\n"), regen.split("\n")
    ops = [op for op in difflib.SequenceMatcher(None, B, N, autojunk=False).get_opcodes() if op[0] != "equal"]
    i13 = next(i for i, l in enumerate(B) if l.startswith("**Task 13.**"))
    i14 = next(i for i, l in enumerate(B) if l.startswith("**Task 14.**"))
    last_fail_13 = max(i for i in range(i13, i14) if B[i].startswith("- Failure — "))
    only_insert = (len(ops) == 1 and ops[0][0] == "insert" and ops[0][1] == ops[0][2] == last_fail_13 + 1
                   and N[ops[0][3]:ops[0][4]] == [RECORDED_T13])
    t = totals(regen)
    out = {"differences": [(op, B[i1:i2], N[j1:j2]) for op, i1, i2, j1, j2 in ops], "only_the_recorded_line": only_insert,
           "regenerated_equals_committed": regen == committed, "totals": t, "totals_base": totals(base)}
    out["pass"] = bool(only_insert and t["checks"] == 182 and t["fail"] == 37 and t["failure_lines"] == 38)
    return out


# ------------------------------------------------------------------------------------------------------------------ C4
def C4():
    F = yaml.safe_load(cur("classification/register/figures.yaml"))
    lab = {e["label"]: e["key"] for e in F}
    order = [e["label"] for e in F]
    a = lab.get("B.5") == "peak-heights" and lab.get("B.6") == "hill-phase" and order.index("B.5") < order.index("B.6")
    ab = cur("classification/Appendix_B_Figures.md")
    i5, i6 = ab.find("**Figure B.5.** Peak variance M/F"), ab.find("**Figure B.6.** Hill gain")
    b = (0 <= i5 < ab.find("figs_thesis/B.5_peak-heights.png") < i6 < ab.find("figs_thesis/B.6_hill-phase.png"))
    rd = cur("classification/figs_thesis/README.md")
    j5, j6 = rd.find("## Figure B.5"), rd.find("## Figure B.6")
    c1 = 0 <= j5 < rd.find("(B.5_peak-heights.png)") < j6 < rd.find("(B.6_hill-phase.png)")
    rm = cur("classification/Roadmap_v3.md")
    c2 = "Figures B.5, B.6" in rm and "Figures {{fig:peak-heights|n}}, {{fig:hill-phase|n}}" in cur("classification/source/Roadmap_v3_Source.md")
    fd = os.path.join(CLS, "figs_thesis")
    stale = sorted(f for f in os.listdir(fd) if f.startswith(("B.5_hill-phase.", "B.6_peak-heights.")))
    png5 = open(os.path.join(fd, "B.5_peak-heights.png"), "rb").read() == show_bytes("classification/figs_thesis/B.6_peak-heights.png")
    png6 = open(os.path.join(fd, "B.6_hill-phase.png"), "rb").read() == show_bytes("classification/figs_thesis/B.5_hill-phase.png")
    caps = all(os.path.exists(os.path.join(fd, f)) for f in ("B.5_peak-heights.txt", "B.6_hill-phase.txt"))
    out = {"a_figures_yaml": a, "b_appendix_B": b, "c_readme": c1, "c_roadmap": c2, "d_stale_files": stale,
           "e_png_B5_eq_old_B6": png5, "e_png_B6_eq_old_B5": png6, "e_captions_exist": caps}
    out["pass"] = bool(a and b and c1 and c2 and not stale and png5 and png6 and caps)
    return out


# ------------------------------------------------------------------------------------------------------------------ C5
def strip_pdf_date(b):
    return re.sub(rb"/CreationDate \(D:\d+Z?\)", b"", b)


def C5_chain(d, tag):
    c = os.path.join(d, "classification")
    os.makedirs(os.path.join(RES, "logs"), exist_ok=True)
    runs = []
    for i, args in enumerate(chain_steps(c)):
        runs.append(run_logged(args, c, os.path.join(RES, "logs", f"{tag}_chain_{i:02d}.log")))
    st = sh(["git", "status", "--porcelain", "--untracked-files=no"], cwd=d).stdout.split("\n")
    changed = [l[3:] for l in st if l.strip()]
    unexpected = []
    for p in changed:
        if p in BYPRODUCTS:
            continue
        if p.endswith(".pdf") and "/figs_thesis/" in p:
            new = open(os.path.join(d, p), "rb").read()
            old = subprocess.run(["git", "show", f"HEAD:{p}"], cwd=d, capture_output=True, check=True).stdout
            if strip_pdf_date(new) == strip_pdf_date(old):
                continue
        unexpected.append(p)
    return {"steps": runs, "all_rc0": all(r["rc"] == 0 for r in runs),
            "render_0_errors": all("0 errors" in r["last_line"] for r in runs if "render.py" in r["cmd"]),
            "changed_tracked": changed, "unexpected_changes": unexpected}


def norm_out(v):
    if isinstance(v, dict):
        return {k: norm_out(x) for k, x in v.items() if k not in ("seconds", "wall_seconds", "commit", "time", "timestamp")}
    if isinstance(v, list):
        return [norm_out(x) for x in v]
    return v


def verdicts(d):
    out = {}
    for s, j in CHECK_JSON.items():
        p = os.path.join(d, "classification", j)
        J = json.load(open(p)) if os.path.exists(p) else {}
        for k, v in J.items():
            if isinstance(v, dict):
                out[f"{s.split('/')[0].upper()} {k}"] = {"pass": v.get("pass"), "out": norm_out(v)}
    return out


def C5(work):
    base_d, art_d = clone(work, "c5_base", BASE), clone(work, "c5_art", ART)
    with ThreadPoolExecutor(2) as ex:
        fb, fa = ex.submit(C5_chain, base_d, "base"), ex.submit(C5_chain, art_d, "art")
        chain_base, chain_art = fb.result(), fa.result()
    jobs = [(tag, d, s) for tag, d in (("base", base_d), ("art", art_d)) for s in CHECK_SCRIPTS]
    with ThreadPoolExecutor(6) as ex:
        rr = list(ex.map(lambda j: (j[0], j[2], run_logged([j[2]], os.path.join(j[1], "classification"),
                                                             os.path.join(RES, "logs", f"{j[0]}_{os.path.basename(j[2])}.log"))), jobs))
    scripts = {f"{t} {s}": r for t, s, r in rr}
    vb, va = verdicts(base_d), verdicts(art_d)
    changed = sorted(k for k in set(vb) | set(va) if (vb.get(k) or {}).get("pass") != (va.get(k) or {}).get("pass"))
    out_changed = sorted(k for k in set(vb) & set(va) if k not in changed and vb[k]["out"] != va[k]["out"])
    md = ["# Task 20 C5: checks whose verdict changed between 7855e45 and the artifacts commit", "",
          "Each check's own output at both commits (timing fields removed). Attribution: `c5_attribution.yaml` (manual reading).", ""]
    for k in changed:
        md += [f"## {k}: {(vb.get(k) or {}).get('pass')} → {(va.get(k) or {}).get('pass')}", "", "Baseline:", "", "```",
               json.dumps((vb.get(k) or {}).get("out"), ensure_ascii=False, indent=1, default=str)[:6000], "```", "", "Artifacts:", "",
               "```", json.dumps((va.get(k) or {}).get("out"), ensure_ascii=False, indent=1, default=str)[:6000], "```", ""]
    open(os.path.join(RES, "c5_diffs.md"), "w").write("\n".join(md))
    out = {"a_chain_base": chain_base, "a_chain_art": chain_art, "b_scripts": scripts,
           "b_all_rc0": all(r["rc"] == 0 for r in scripts.values()),
           "verdicts_base": {k: v["pass"] for k, v in vb.items()}, "verdicts_art": {k: v["pass"] for k, v in va.items()},
           "verdict_changes": changed, "output_changed_same_verdict": out_changed}
    out["a_ok"] = bool(chain_art["all_rc0"] and chain_art["render_0_errors"] and not chain_art["unexpected_changes"])
    out["pass"] = None   # set by --verdict from c5_attribution.yaml
    return out, art_d


# ------------------------------------------------------------------------------------------------------------------ C6
def C6():
    D = cur("classification/Appendix_D_Verification.md")
    e13 = D.split("**Task 13.**")[1].split("**Task 14.**")[0]
    a3 = json.load(open(os.path.join(CLS, "t13", "results", "t13_A3_proof.json")))["A3"]
    items = [x for x in a3 if isinstance(x, dict) and "pass" in x]
    a = "22 of 22 checks" in e13 and len(items) == 22 and all(x["pass"] for x in items)
    t = totals(D)
    b = t["checks"] == 182 and t["fail"] == 37
    lines = {int(m.group(1)): m.group(0) for m in re.finditer(r"^\[(\d+)\] .*$", cur("classification/Appendix_C_References.md"), re.M)}
    nf = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731
    render = {n: {"rendered": lines.get(n), "prompt": f"[{n}] {txt}", "equal": nf(lines.get(n) or "") == nf(f"[{n}] {txt}")}
              for n, (k, txt) in PROMPT_REFS.items()}
    bib = bibfmt.parse(os.path.join(CLS, "references.bib"))
    fields = {}
    for k, want in BIBFIELDS.items():
        have = {f: bibfmt.tex(v) if f not in ("url", "doi", "eprint") else v for f, v in bib[k].items()}
        fields[k] = {f: have.get(f) == w for f, w in want.items()}
    c_render = all(v["equal"] for v in render.values())
    c_fields = all(all(v.values()) for v in fields.values())
    out = {"a_22_of_22": a, "b_totals": t, "b_ok": b, "c_render": render, "c_render_ok": c_render, "c_bib_fields": fields,
           "c_bib_fields_ok": c_fields}
    out["pass"] = bool(a and b and c_render and c_fields)
    return out


def main():
    if "--verdict" in sys.argv:
        p = os.path.join(RES, "t20_checks.json")
        R = json.load(open(p))
        att = yaml.safe_load(open(os.path.join(RES, "c5_attribution.yaml")))
        causes = {"i", "ii", "iii", "iv", "v"}
        un = [k for k in R["C5"]["verdict_changes"] if not (att.get(k) or {}).get("cause") in causes]
        R["C5"]["unattributed"] = un
        R["C5"]["pass"] = bool(R["C5"]["a_ok"] and R["C5"]["b_all_rc0"] and not un)
        json.dump(R, open(p, "w"), indent=1, ensure_ascii=False, default=str)
        print("C5", R["C5"]["pass"], "unattributed", un)
        return
    assert not sh(["git", "status", "--porcelain", "--untracked-files=no"]).stdout.strip(), "working tree not clean"
    global ART
    art = ART = sh(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
    work = sys.argv[sys.argv.index("--work") + 1] if "--work" in sys.argv else tempfile.mkdtemp(prefix="t20_")
    os.makedirs(RES, exist_ok=True)
    R = {"artifacts_commit": art, "base": BASE, "python": sys.version.split()[0], "work": work}
    for name, fn in (("C1", C1), ("C4", C4), ("C6", C6)):
        t0 = time.time()
        R[name] = fn()
        R[name]["seconds"] = round(time.time() - t0, 1)
        print(name, R[name]["pass"], flush=True)
    t0 = time.time()
    R["C2"] = C2(work)
    R["C2"]["seconds"] = round(time.time() - t0, 1)
    print("C2", R["C2"]["pass"], flush=True)
    t0 = time.time()
    R["C5"], art_d = C5(work)
    R["C5"]["seconds"] = round(time.time() - t0, 1)
    print("C5 chain/scripts", R["C5"]["a_ok"], R["C5"]["b_all_rc0"], "changes", R["C5"]["verdict_changes"], flush=True)
    t0 = time.time()
    R["C3"] = C3(art_d)
    R["C3"]["seconds"] = round(time.time() - t0, 1)
    print("C3", R["C3"]["pass"], flush=True)
    json.dump(R, open(os.path.join(RES, "t20_checks.json"), "w"), indent=1, ensure_ascii=False, default=str)


if __name__ == "__main__":
    main()
