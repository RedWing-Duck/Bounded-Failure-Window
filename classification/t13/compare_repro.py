"""Part D (PREREG_t13): compare the reports regenerated in the clean checkout with the committed ones.
Masked: runtimes (any line mentioning runtime, and the last 'Runtime (s)' column of check tables), commit hashes, dates.
Pass per report: every verdict token identical, every other number identical or within 1e-6 relative.
Usage: python3 compare_repro.py WORKDIR"""
import json
import os
import re
import sys

from t13_common import CLS, save_json

REPORTS = {"8": "REPORT.md", "9": "t9/RESULTS_t9.md", "10": "t10/RESULTS_t10.md", "11": "t11/RESULTS_t11.md",
           "12": "t12/RESULTS_t12.md"}
VERD = re.compile(r"\*\*(PASS|FAIL)\*\*|\[(PASS|FAIL|DONE)\]|\b(PASS|FAIL)\b")
NUM = re.compile(r"[-+]?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?")
HASH = re.compile(r"\b[0-9a-f]{7,40}\b")


def mask(text):
    out, rt_col = [], None
    for ln in text.split("\n"):
        if ln.startswith("|") and "Runtime (s)" in ln:
            hdr = [c.strip() for c in ln.strip("|").split("|")]
            rt_col = "last" if hdr[-1] == "Runtime (s)" else hdr.index("Runtime (s)")
        elif not ln.startswith("|"):
            rt_col = None
        if re.search(r"runtime|Runtime|seconds|wall time|\b\d+(\.\d+)? ?s\b(?! *\|)", ln) and not ln.startswith("|"):
            ln = NUM.sub("#", ln)
        if rt_col is not None and ln.startswith("|") and "---" not in ln and "Runtime (s)" not in ln:
            cells = ln.strip("|").split("|")
            if rt_col == "last":
                cells[-1] = " # "
            elif len(cells) > rt_col:
                cells[rt_col] = " # "
            ln = "|" + "|".join(cells) + "|"
        ln = HASH.sub("<hash>", ln)
        ln = re.sub(r"\d{4}-\d{2}-\d{2}", "<date>", ln)
        out.append(ln)
    return out


def nums(s):
    return [float(x.replace(",", "")) for x in NUM.findall(s) if re.search(r"\d", x)]


def compare(a, b):
    A, B = mask(a), mask(b)
    issues = []
    va = [m.group(0) for ln in A for m in VERD.finditer(ln)]
    vb = [m.group(0) for ln in B for m in VERD.finditer(ln)]
    if va != vb:
        issues.append({"kind": "verdicts", "committed": va, "reproduced": vb})
    if len(A) != len(B):
        issues.append({"kind": "line count", "committed": len(A), "reproduced": len(B)})
    for i, (x, y) in enumerate(zip(A, B)):
        if x == y:
            continue
        tx, ty = NUM.sub("#", x), NUM.sub("#", y)
        nx, ny = nums(x), nums(y)
        if tx != ty or len(nx) != len(ny):
            issues.append({"kind": "text", "line": i + 1, "committed": x[:300], "reproduced": y[:300]})
            continue
        bad = [(p, q) for p, q in zip(nx, ny) if not (p == q or abs(p - q) <= 1e-6 * max(abs(p), abs(q)))]
        if bad:
            issues.append({"kind": "number", "line": i + 1, "pairs": bad[:5], "committed": x[:300], "reproduced": y[:300]})
    return issues


def main():
    work = sys.argv[1]
    R = {"workdir": work, "reports": {}}
    done_tasks = set()
    for fn in os.listdir(work):
        if fn.startswith("runtime_") and fn.endswith(".tsv"):
            done_tasks |= {l.split("\t")[0] for l in open(os.path.join(work, fn)).read().splitlines() if l.strip()}
    R["completed_tasks"] = sorted(done_tasks, key=int)
    for t, rel in REPORTS.items():
        rp = os.path.join(work, "classification", rel)
        if t not in done_tasks or not os.path.exists(rp):
            R["reports"][t] = {"status": "not reproduced"}
            continue
        iss = compare(open(os.path.join(CLS, rel)).read(), open(rp).read())
        verd_ok = not any(i["kind"] == "verdicts" for i in iss)
        R["reports"][t] = {"file": rel, "n_issues": len(iss), "verdicts_identical": verd_ok, "issues": iss[:40],
                           "pass": verd_ok and not iss}
        print(f"Task {t}: {'PASS' if R['reports'][t]['pass'] else 'FAIL'} ({len(iss)} issues; verdicts identical {verd_ok})")
        for i in iss[:8]:
            print("   ", json.dumps(i, ensure_ascii=False)[:400])
    done = [v for v in R["reports"].values() if "pass" in v]
    R["pass"] = len(done) == len(REPORTS) and all(v["pass"] for v in done)
    save_json(R, "t13_compare_repro.json")


if __name__ == "__main__":
    main()
