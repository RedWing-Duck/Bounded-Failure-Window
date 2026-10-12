"""Task 18 Part B.3: the draft's Theorem 2.2 (statement and proof, parts numbered (1)-(4)) as a thesis-only text, placed by
register/thesis_overrides.yaml (replace critical-tolerance; thesis render only). Verbatim from the draft except \\[n\\] -> [n].
Idempotent. Usage: python3 make_thesis_only_t18.py"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_full.md")
CIT = re.compile(r"\\\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\\\]")


def main():
    L = open(DRAFT).read().split("\n")
    body = "\n".join(L[157:165])
    head = ("*Thesis-only text, imported verbatim from the thesis draft (`t18/input/Thesis_Draft_full.md`, §2.3, lines 158–165; "
            "citations written [n]). Task 18.*")
    open(os.path.join(CLS, "source", "thesis_only", "critical-tolerance.md"), "w").write(head + "\n\n" + CIT.sub(r"[\1]", body) + "\n")
    print("critical-tolerance.md written")


if __name__ == "__main__":
    main()
