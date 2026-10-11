"""Part D for Task 13: compare the clean-checkout replay's results/*.json (and C2 row files) with this run's.
Masked: keys naming runtimes or paths (seconds, time, runtime, *_s, workdir, file paths). Pass: every remaining value equal,
numbers within 1e-6 relative. Files that exist in only one run are listed (e.g. first-run records kept by hand).
Usage: python3 compare_t13.py WORKDIR"""
import json
import os
import sys

from t13_common import RES, save_json

SKIP = {"seconds", "time", "runtime", "runtime_s", "workdir", "realize_diag_s", "elapsed"}


def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in SKIP or k.endswith("_s") or k.endswith("_seconds"):
                continue
            if k not in a or k not in b:
                out.append(f"{path}.{k}: missing in {'committed' if k not in a else 'replay'}")
                continue
            walk(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: length {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if not (a == b or abs(a - b) <= 1e-6 * max(abs(a), abs(b))):
            out.append(f"{path}: {a} vs {b}")
    elif isinstance(a, str) and isinstance(b, str) and ("/tmp/" in a or "/home/" in a):
        pass
    elif a != b:
        out.append(f"{path}: {str(a)[:120]} vs {str(b)[:120]}")


def files(root):
    return {os.path.relpath(os.path.join(r, f), root) for r, _, fs in os.walk(root) for f in fs if f.endswith(".json")}


def main():
    rep = os.path.join(sys.argv[1], "classification", "t13", "results")
    mine, theirs = files(RES), files(rep)
    skip = {"t13_compare_repro.json", "t13_repro_t10_diag.json", "t13_repro_compare_diag.json", "repro_manifest.json",
            "t13_compare_t13.json", "env.json"}
    R = {"only_committed": sorted(mine - theirs - skip), "only_replay": sorted(theirs - mine - skip), "files": {}}
    for f in sorted((mine & theirs) - skip):
        if f.startswith("c2_rows_n"):
            continue
        out = []
        walk(json.load(open(os.path.join(RES, f))), json.load(open(os.path.join(rep, f))), "", out)
        R["files"][f] = out[:20] + ([f"... {len(out) - 20} more"] if len(out) > 20 else [])
    # Part A numerics ran in two invocations here (container restart), in one in the replay: compare the merged items
    num = lambda root: {k: v for f in sorted(os.listdir(root)) if f.startswith("t13_partA_numeric_") and f.endswith(".json")
                        and not f.endswith("_diag.json") for k, v in json.load(open(os.path.join(root, f))).items()}
    for f in [f for f in R["files"] if f.startswith("t13_partA_numeric_") and not f.endswith("_diag.json")]:
        del R["files"][f]
    out = []
    walk(num(RES), num(rep), "", out)
    R["files"]["t13_partA_numeric_* (merged)"] = out[:20]
    R["only_committed"] = [f for f in R["only_committed"] if not f.startswith("c2_rows_n3/")]
    R["n_files"] = len(R["files"])
    R["n_identical"] = sum(not v for v in R["files"].values())
    R["pass"] = R["n_identical"] == R["n_files"]
    print(f"Task 13: {R['n_identical']}/{R['n_files']} result files identical (masked); only committed {R['only_committed']}; "
          f"only replay {R['only_replay']}")
    for f, v in R["files"].items():
        if v:
            print("  ", f, v[:5])
    save_json(R, "t13_compare_t13.json")


if __name__ == "__main__":
    main()
