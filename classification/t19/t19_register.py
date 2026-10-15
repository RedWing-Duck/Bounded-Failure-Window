"""Task 19 Part A.1 register update (PREREG_t19.md). Run after t16/t16_register.py in the render chain.
Reference 26: the key sahomasugi2016 is replaced by roberts1959 (number 26 kept) in register/references.yaml, and in
register/results.yaml (result 6.13's citations). A text replacement, so the files' layout is unchanged; references.bib carries
the new entry directly. Idempotent. Usage: python3 t19_register.py"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
OLD, NEW = "sahomasugi" + "2016", "roberts1959"


def swap(f, t):
    """Task 20 (PREREG_t20.md, item 4): the swap is limited to reference number 26 in references.yaml and to citations lines
    without roberts1959 in results.yaml, so that the key re-added as [60] by t20/t20_register.py is never swapped."""
    if f == "references.yaml":
        return re.subn(r"(- number: 26\n  key: )" + OLD + r"\b", r"\g<1>" + NEW, t)
    n, out = 0, []
    for ln in t.split("\n"):
        if OLD in ln and ln.lstrip().startswith("citations:") and NEW not in ln:
            ln, k = ln.replace(OLD, NEW), ln.count(OLD)
            n += k
        out.append(ln)
    return "\n".join(out), n


def main():
    for f in ("references.yaml", "results.yaml"):
        p = os.path.join(CLS, "register", f)
        t, n = swap(f, open(p).read())
        open(p, "w").write(t)
        print(f"{f}: {n} replaced")


if __name__ == "__main__":
    main()
