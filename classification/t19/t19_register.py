"""Task 19 Part A.1 register update (PREREG_t19.md). Run after t16/t16_register.py in the render chain.
Reference 26: the key sahomasugi2016 is replaced by roberts1959 (number 26 kept) in register/references.yaml, and in
register/results.yaml (result 6.13's citations). A text replacement, so the files' layout is unchanged; references.bib carries
the new entry directly. Idempotent. Usage: python3 t19_register.py"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
OLD, NEW = "sahomasugi" + "2016", "roberts1959"


def main():
    for f in ("references.yaml", "results.yaml"):
        p = os.path.join(CLS, "register", f)
        t = open(p).read()
        n = t.count(OLD)
        open(p, "w").write(t.replace(OLD, NEW))
        print(f"{f}: {n} replaced")


if __name__ == "__main__":
    main()
