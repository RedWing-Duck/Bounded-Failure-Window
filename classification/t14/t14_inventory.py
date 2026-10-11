"""Task 14 §1 inventory (read-only), taken from the pre-registration commit with git, before any file was changed.
Usage: python3 t14_inventory.py"""
import subprocess

from t14_common import AE, LEGACY, PREREG, REPO, save_json


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True).stdout


def main():
    files = git("ls-tree", "-r", "--name-only", PREREG).split("\n")
    files = [f for f in files if f]
    top = {}
    for f in files:
        d = f.split("/")[0] if "/" in f else "(root)"
        sub = "/".join(f.split("/")[:2]) if f.count("/") >= 2 else d
        top.setdefault(d, {}).setdefault(sub, 0)
        top[d][sub] += 1
    all_hist = set(git("log", "--all", "--name-only", "--pretty=format:").split("\n"))
    manus = sorted(f for f in all_hist if f.lower().endswith((".pdf", ".tex", ".docx")) and not f.startswith("classification/"))
    ver = sorted(f for f in files if f.startswith("verification/") and (f.endswith(".md") or f.split("/")[-1].startswith(("t1_", "t2_", "t3_", "t4", "t6_", "t7_"))))
    commits = [l for l in git("log", "--all", "--oneline", "--reverse").split("\n") if l][:16]
    counts = {}
    for f in files:
        if not f.startswith("classification/") or not f.endswith((".md", ".txt", ".py", ".csv", ".sh")):
            continue
        txt = git("show", f"{PREREG}:{f}")
        c = {"legacy_regex": sum(1 for _ in LEGACY.finditer(txt)), "A-E_labels": len(AE.findall(txt)), "Paper 1": txt.count("Paper 1")}
        if any(c.values()):
            counts[f] = c
    R = {"commit": PREREG, "n_files": len(files), "layout": top, "manuscript_candidates_in_history": manus,
         "verification_suite": ver, "first_commits": commits, "legacy_counts": counts,
         "totals": {k: sum(v[k] for v in counts.values()) for k in ("legacy_regex", "A-E_labels", "Paper 1")}}
    print("files", len(files), "| manuscript files in history:", manus or "none")
    for f, c in sorted(counts.items()):
        print(f"  {f}: {c}")
    print("totals", R["totals"])
    save_json(R, "t14_inventory.json")


if __name__ == "__main__":
    main()
