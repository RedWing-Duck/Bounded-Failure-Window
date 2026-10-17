"""Task 21 checks K1-K4 (PREREG_t21.md). Run once, on the artifacts commit, from a clean working tree:
    python3 t21/t21_checks.py [--work DIR]
Pre = 8ea738d, post = HEAD (artifacts commit). Both are fresh local clones under --work; the render chain runs in each and the
capture pickles are read from the clones. Only t21/results/ is written in the repository."""
import json
import os
import pickle
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.path.join(HERE, "results")
PRE = "8ea738d"
PY = sys.executable
EXPECTED = {  # (kind, old text) -> (kind, new text), per figure, with multiplicity
    "B.8_optimal-sampling": [(("legend", "post (just after a sample)"), ("legend", "posterior (just after a sample)"))],
    "B.9_sampled-relay": [(("legend", "post"), ("legend", "posterior")),
                          (("title", "D1, post: a window"), ("title", "D1, posterior: a window")),
                          (("legend", "avg$/F - 1$"), ("legend", "averaged$/F - 1$")),
                          (("ylabel", "avg$/F - 1$"), ("ylabel", "averaged$/F - 1$"))],
    "B.10_process-noise": [(("xlabel", r"$u = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)"),
                            ("xlabel", r"$\nu = 2\Sigma\Pi/\lambda^2$ ($\lambda = \Pi = 1$)"))] * 2,
}
CHANGED_PNGS = {"classification/figs_thesis/B.8_optimal-sampling.png", "classification/figs_thesis/B.9_sampled-relay.png",
                "classification/figs_thesis/B.10_process-noise.png"}
BYPRODUCTS = {"classification/t15/results/cap_new_t13.pkl", "classification/t15/results/cap_new_t8.pkl",
              "classification/t15/results/cap_B2.pkl", "classification/register/tasks.yaml"}


def sh(cmd, cwd=REPO):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True)
    if r.returncode:
        raise RuntimeError(f"{cmd}: {r.stderr.decode()}")
    return r.stdout


def clone(work, name, commit):
    d = os.path.join(work, name)
    sh(["git", "clone", "-q", "--no-hardlinks", REPO, d])
    sh(["git", "checkout", "-q", "--detach", commit], cwd=d)
    return d


def chain(d, tag):
    c = os.path.join(d, "classification")
    t = open(os.path.join(c, "Appendix_E_Reproduction.md")).read()
    block = re.split(r"^## .*render chain$", t, flags=re.M)[1].split("```")[1]
    os.makedirs(os.path.join(RES, "logs"), exist_ok=True)
    runs = []
    for i, ln in enumerate(block.split("\n")):
        ln = ln.split("#")[0].strip()
        if not ln.startswith("python3 ") or "t15_checks" in ln:
            continue
        log = os.path.join(RES, "logs", f"{tag}_chain_{len(runs):02d}.log")
        with open(log, "w") as fh:
            r = subprocess.run([PY] + ln.split()[1:], cwd=c, stdout=fh, stderr=subprocess.STDOUT)
        runs.append({"cmd": ln, "rc": r.returncode, "last_line": open(log).read().strip().split("\n")[-1][:200]})
    return runs


def strip_pdf_date(b):
    return re.sub(rb"/CreationDate \(D:\d+Z?\)", b"", b)


def load_caps(d):
    out = {}
    for f in ("cap_new_t13.pkl", "cap_new_t8.pkl"):
        out.update(pickle.load(open(os.path.join(d, "classification", "t15", "results", f), "rb")))
    return out


def K1(pre, post):
    bad = []
    for name in sorted(set(pre) | set(post)):
        a, b = pre.get(name, {}).get("arrays"), post.get(name, {}).get("arrays")
        if a is None or b is None or len(a) != len(b) or any(x[0] != y[0] or not np.array_equal(x[1], y[1]) for x, y in zip(a, b)):
            bad.append(name)
    return {"figures_pre": sorted(pre), "figures_post": sorted(post), "figures_with_array_differences": bad,
            "pass": sorted(pre) == sorted(post) and not bad}


def K2(pre, post):
    found, ok = {}, True
    for name in sorted(set(pre) | set(post)):
        a, b = [tuple(x) for x in pre[name]["texts"]], [tuple(x) for x in post[name]["texts"]]
        if a == b:
            continue
        diffs = [(x, y) for x, y in zip(a, b) if x != y] if len(a) == len(b) else [("length", (len(a), len(b)))]
        found[name] = diffs
    for name in set(found) | set(EXPECTED):
        if Counter(found.get(name, [])) != Counter(EXPECTED.get(name, [])):
            ok = False
    return {"differences": found, "pass": ok}


def K3(art):
    names = sh(["git", "diff", "--name-only", PRE, art, "--", "classification/figs_thesis"]).decode().split()
    return {"changed_files": names, "pngs_changed": sorted(CHANGED_PNGS & set(names)),
            "other_changed": sorted(set(names) - CHANGED_PNGS),
            "pass": CHANGED_PNGS <= set(names) and not (set(names) - CHANGED_PNGS)}


def K4(d, runs):
    st = sh(["git", "status", "--porcelain", "--untracked-files=no"], cwd=d).decode().split("\n")
    unexpected = []
    for p in [l[3:] for l in st if l.strip()]:
        if p in BYPRODUCTS:
            continue
        if p.endswith(".pdf") and "/figs_thesis/" in p:
            old = subprocess.run(["git", "show", f"HEAD:{p}"], cwd=d, capture_output=True, check=True).stdout
            if strip_pdf_date(open(os.path.join(d, p), "rb").read()) == strip_pdf_date(old):
                continue
        unexpected.append(p)
    ok = all(r["rc"] == 0 for r in runs) and all("0 errors" in r["last_line"] for r in runs if "render.py" in r["cmd"])
    return {"steps": runs, "steps_ok": ok, "unexpected_changes": unexpected, "pass": ok and not unexpected}


def main():
    assert not sh(["git", "status", "--porcelain", "--untracked-files=no"]).strip(), "working tree not clean"
    art = sh(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    work = sys.argv[sys.argv.index("--work") + 1] if "--work" in sys.argv else tempfile.mkdtemp(prefix="t21_")
    os.makedirs(RES, exist_ok=True)
    t0 = time.time()
    dpre, dpost = clone(work, "pre", PRE), clone(work, "post", art)
    rpre, rpost = chain(dpre, "pre"), chain(dpost, "post")
    cpre, cpost = load_caps(dpre), load_caps(dpost)
    R = {"artifacts_commit": art, "pre": PRE, "python": sys.version.split()[0],
         "pre_chain_ok": all(r["rc"] == 0 for r in rpre),
         "K1": K1(cpre, cpost), "K2": K2(cpre, cpost), "K3": K3(art), "K4": K4(dpost, rpost),
         "seconds": round(time.time() - t0, 1)}
    json.dump(R, open(os.path.join(RES, "t21_checks.json"), "w"), indent=1, ensure_ascii=False, default=str)
    for k in ("K1", "K2", "K3", "K4"):
        print(k, R[k]["pass"])


if __name__ == "__main__":
    main()
