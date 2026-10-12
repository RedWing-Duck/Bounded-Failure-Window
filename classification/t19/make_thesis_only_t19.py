"""Task 19 Part A.2: the draft's Theorem 2.2 (statement and proof, with the closing sentences the Task 13 referee added to the
repository's proof) as a thesis-only text, placed by register/thesis_overrides.yaml (replace critical-tolerance; thesis render
only). Verbatim from the draft (t19/input/Thesis_Draft_full.md, lines 158-165) except \\[n\\] -> [n]. Replaces the output of
t18/make_thesis_only_t18.py and runs after it in the chain. Idempotent. Usage: python3 make_thesis_only_t19.py"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_full.md")
CIT = re.compile(r"\\\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\\\]")


def main():
    L = open(DRAFT).read().split("\n")
    assert L[157].startswith("**Theorem 2.2.**") and L[164].startswith("*Proof.*"), "draft lines moved"
    body = "\n".join(L[157:165])
    head = ("*Thesis-only text, imported verbatim from the thesis draft (`t19/input/Thesis_Draft_full.md`, §2.3, lines 158–165; "
            "citations written [n]). Task 19 (Task 18's import, with the proof's closing sentences).*")
    open(os.path.join(CLS, "source", "thesis_only", "critical-tolerance.md"), "w").write(head + "\n\n" + CIT.sub(r"[\1]", body) + "\n")
    print("critical-tolerance.md written")


if __name__ == "__main__":
    main()
