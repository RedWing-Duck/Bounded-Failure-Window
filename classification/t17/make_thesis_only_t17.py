"""Task 17 Part B.1-B.2: thesis-only imports from the draft (t17/input/Thesis_Draft_ch1-7.md) and unescaped citations.
Each import is verbatim from the draft lines named, except that escaped citation groups \\[n\\] become [n] (Part B.1).
Existing thesis-only texts get the same unescaping. register/thesis_overrides.yaml says where render.py places each import
(thesis render only; source/Stages_0_4_Source.md is not changed). Idempotent. Usage: python3 make_thesis_only_t17.py"""
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
TO = os.path.join(CLS, "source", "thesis_only")
DRAFT = os.path.join(HERE, "input", "Thesis_Draft_ch1-7.md")
CIT = re.compile(r"\\\[(\d+(?:–\d+)?(?:, \d+(?:–\d+)?)*)\\\]")

IMPORTS = [  # file, section, draft line ranges (inclusive)
    ("plateaus.md", "§2.5", [(211, 213)]),
    ("equal-height-maxima.md", "§2.5", [(215, 217)]),
    ("degenerate-points.md", "§2.5", [(221, 223)]),
    ("pair-birth.md", "§2.5", [(225, 227)]),
    ("stationary-variance.md", "§3.1", [(306, 316)]),
    ("optimal-envelope.md", "§3.4", [(382, 394)]),
    ("discrete-excess.md", "§6.3", [(1014, 1024)]),
]


def unescape(t):
    return CIT.sub(r"[\1]", t)


def main():
    L = open(DRAFT).read().split("\n")
    for f, sec, ranges in IMPORTS:
        lines = ", ".join(f"{a}–{b}" for a, b in ranges)
        body = "\n\n".join("\n".join(L[a - 1:b]) for a, b in ranges)
        head = (f"*Thesis-only text, imported verbatim from the thesis draft (`t17/input/Thesis_Draft_ch1-7.md`, {sec}, lines {lines}; "
                "citations written [n]). Task 17.*")
        open(os.path.join(TO, f), "w").write(head + "\n\n" + unescape(body) + "\n")
    n = 0
    for p in sorted(glob.glob(os.path.join(TO, "*.md"))):
        t = open(p).read()
        u = unescape(t)
        if u != t:
            open(p, "w").write(u)
            n += 1
    print(f"{len(IMPORTS)} imports written; {n} existing texts unescaped")


if __name__ == "__main__":
    main()
