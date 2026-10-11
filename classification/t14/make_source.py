"""Task 14 §3 and §5: convert archive/Stages_0_4_Consolidated_v1.md into the key-token source
source/Stages_0_4_Source.md, write register/matrix.csv (single source of the synthesis matrix) and
register/crosswalk_v1.yaml (verbatim legacy strings of v1's change log, used only by the paper render).
Conversion is mechanical (regexes below) plus the explicit edits in EDITS, each asserted to apply exactly once.
Usage: python3 make_source.py"""
import csv
import io
import os
import re

import yaml

from t14_common import CLS

V1 = os.path.join(CLS, "archive", "Stages_0_4_Consolidated_v1.md")
REG = os.path.join(CLS, "register")
TYPES = "Proposition|Theorem|Lemma|Corollary|Numerical result|Conjecture|Counterexample|Definition"
PLUR = {"Propositions": "Proposition", "Theorems": "Theorem", "Lemmas": "Lemma", "Corollaries": "Corollary",
        "Numerical results": "Numerical result"}
ABBR = {"Thm": "Theorem", "Prop.": "Proposition", "Cor.": "Corollary", "Num.": "Numerical result"}


def load_register():
    reg = yaml.safe_load(open(os.path.join(REG, "results.yaml")))
    by_v1 = {}
    for e in reg:
        cv = e["cons_v1"] or ""
        m = re.match(r"^(\d+)(?: \(main part\))?$", cv)
        if m:
            by_v1[int(m.group(1))] = e["key"]
    return reg, by_v1


class Conv:
    def __init__(self, by_v1, v1_types):
        self.by_v1, self.v1_types, self.warn = by_v1, v1_types, []

    def key(self, n, typ, ctx):
        if n not in self.by_v1:
            self.warn.append(f"no key for {typ} {n}: {ctx[:80]}")
            return None
        if typ and self.v1_types.get(n) != typ:
            self.warn.append(f"type mismatch {typ} {n} (v1 {self.v1_types.get(n)}): {ctx[:80]}")
        return self.by_v1[n]

    def refs(self, s):
        """v1 result references -> tokens; dotted (legacy) numbers are left alone (lookahead)."""
        num = r"\d+(?!\.\d|\d|′)"

        def plural(m):
            typ = PLUR[m.group(1)]
            body = re.sub(r"\d+", lambda k: f"[[{self.key(int(k.group(0)), typ, m.group(0)) or k.group(0)}|n]]", m.group(2))
            return m.group(1) + " " + body
        s = re.sub(r"\b(Propositions|Theorems|Lemmas|Corollaries|Numerical results)\s+(" + num + r"(?:\([a-z0-9]+\))?"
                   r"(?:(?:,\s*|\s+and\s+|\s+or\s+|\s*[–-]\s*)" + num + r"(?:\([a-z0-9]+\))?)*)", plural, s)

        def single(m):
            k = self.key(int(m.group(2)), m.group(1), m.group(0))
            return f"[[{k}]]" if k else m.group(0)
        s = re.sub(r"\b(" + TYPES + r")\s+(" + num + ")", single, s)

        def abbr(m):
            k = self.key(int(m.group(2)), ABBR[m.group(1)], m.group(0))
            out = f"[[{k}|a]]"
            if m.group(4):
                out += m.group(3) + f"[[{self.key(int(m.group(4)), ABBR[m.group(1)], m.group(0))}|n]]"
            return out
        s = re.sub(r"(Thm|Prop\.|Cor\.|Num\.)\s+(" + num + r")(?:(\s*[–-]\s*)(" + num + "))?", abbr, s)
        return s.replace("Paper 1", "{{phase1}}")


LEGACY_SUB = re.compile(r"(?:Props?\.?|Thm|Lemma|Cor\.|Conj\.|Num\.|Def\.|Theorem|Corollary|Proposition|Conjecture|Numerical result)"
                        r"\s?\d+\.\d+[a-z′]?(?:\([a-z]\))?(?:(?:\s/\s|,\s|–)\d+\.\d+[a-z′]?(?:\([a-z]\))?)*")


def main():
    reg, by_v1 = load_register()
    v1 = open(V1).read()
    v1_types = {int(m.group(2)): m.group(1) for m in re.finditer(r"^\*\*(" + TYPES + r") (\d+) ", v1, re.M)}
    C = Conv(by_v1, v1_types)
    legacy = []

    def leg(text, ctx):
        lid = f"L{len(legacy) + 1:03d}"
        legacy.append({"id": lid, "text": text, "context": ctx})
        return "{{legacy:" + lid + "}}"

    head, rest = v1.split("\n## 10. Final synthesis matrix\n")
    mat_part, tail = rest.split("\n\nRows 1–20 and 35–42", 1)
    body, chlog = tail.split("\n## 13. Change log\n")
    mat_lines = [l for l in mat_part.split("\n") if l.startswith("|")]
    mat_intro = "\n".join(l for l in mat_part.split("\n") if not l.startswith("|")).rstrip("\n")

    # --- matrix.csv (single source): v1 rows, references as keys; rows 25-26 per Task 14 §5; row 8 points to the split
    hdr = [c.strip() for c in mat_lines[0].strip("|").split("|")]
    rows = []
    for l in mat_lines[2:]:
        cells = [c.strip() for c in l.strip().strip("|").split(" | ")]
        assert len(cells) == len(hdr), l
        r = dict(zip(hdr, cells))
        r["Label"] = C.refs(r["Label"])
        r["Verified by"] = C.refs(r["Verified by"])
        r["Conditions"] = C.refs(r["Conditions"])
        rows.append(r)
    by_no = {r["#"]: r for r in rows}
    by_no["25"]["Conditions"] = "2R if $G > 2F\\Pi$ ([[dt-two-rays]])"
    by_no["26"]["Conditions"] = "2R if $G > 2F\\Pi$ ([[dt-two-rays]]); also seen for $G \\le 2F\\Pi$ ([[dt-relay-census]])"
    assert by_no["8"]["Label"] == "[[two-stage-gains|a]], [[window-theorem|a]]", by_no["8"]["Label"]
    by_no["8"]["Label"] = "[[two-stage-gains|a]], [[no-mixed-decreasing-ratio|a]]"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=hdr, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    open(os.path.join(REG, "matrix.csv"), "w").write(buf.getvalue())

    # --- main text
    src = head + "\n## 10. Final synthesis matrix\n" + mat_intro + "\n\n{{matrix}}\n\nRows 1–20 and 35–42" + body
    # label lines: type comes from the register via the preceding heading's key
    out, cur = [], None
    for ln in src.split("\n"):
        m = re.match(r"^\*\*(" + TYPES + r") (\d+) ", ln)
        if m:
            cur = by_v1[int(m.group(2))]
        lm = re.match(r"^\*\*Label:\*\* (" + TYPES + r") ", ln)
        if lm:
            ln = f"**Label:** [[{cur}|t]] " + ln[lm.end():]
        out.append(ln)
    src = "\n".join(out)
    # section 12 table: number and kind columns
    src = re.sub(r"^\| (\d+) \| (" + TYPES + r") \| ", lambda m: f"| [[{by_v1[int(m.group(1))]}|n]] | [[{by_v1[int(m.group(1))]}|t]] | ",
                 src, flags=re.M)
    # legacy remarks in the body (paper render only)
    for old in ["It was Numerical result 2.8 / 4.10a.", "It was Conjecture 4.11 in Stage 4."]:
        assert src.count(" " + old) == 1, old
        txt = old[len("It was "):].rstrip(".")
        lt = leg(txt.replace(" in Stage 4", ""), "body remark")
        rep = "{{paper: It was " + lt + (" in Stage 4" if "Stage 4" in old else "") + ".}}"
        src = src.replace(" " + old, rep)
    src = C.refs(src)

    # --- change log: paper render keeps v1's (legacy strings via the crosswalk); thesis render points to the crosswalk
    cl = []
    sec = None
    for ln in chlog.split("\n"):
        if ln.startswith("### 13.1"):
            sec = 1
        elif ln.startswith("### 13.2"):
            sec = 2
        if ln.startswith("| ") and not ln.startswith("| Old") and not ln.startswith("| #") and not ln.startswith("|---"):
            cells = ln.strip().strip("|").split(" | ")
            if sec == 1:
                cells[0] = leg(cells[0].strip(), "13.1 old")
                cells[1] = C.refs(cells[1].strip())
            else:
                cells[2] = LEGACY_SUB.sub(lambda m: leg(m.group(0), f"13.2 row {cells[0].strip()}"), cells[2].strip())
                cells = [c.strip() for c in cells[:2]] + [C.refs(cells[2]), C.refs(cells[3].strip())]
            ln = "| " + " | ".join(c.strip() for c in cells) + " |"
        cl.append(ln)
    thesis_cl = ("<!--thesis-->\n\n### 13.1 Numbering\n\n"
                 "Results carry thesis numbers from `register/results.yaml` (freeze v1, Task 14): one counter per thesis chapter, shared "
                 "by all result types. Earlier numbers (stage documents, the A–E labels, the consolidated v1 numbers) appear only in "
                 "`register/crosswalk.md`. The consolidated v1 number map and its 45 corrections are kept verbatim in "
                 "`archive/Stages_0_4_Consolidated_v1.md`, Section 13.\n\n"
                 "### 13.2 Changes at freeze v1 (Task 14)\n\n"
                 "Numbering, references, file organisation and citations only; no mathematical content changed. The addendum of "
                 "[[window-theorem]] is now its own result, [[no-mixed-decreasing-ratio]], with its proof unchanged. "
                 "[[excess-identity]] carries the register's type. The synthesis matrix of Section 10 is rendered from "
                 "`register/matrix.csv`, the same file that renders Roadmap v3's matrix.\n<!--/thesis-->\n")
    src = src + "\n## 13. Change log\n" + thesis_cl + "<!--paper-->\n" + "\n".join(cl).rstrip("\n") + "\n<!--/paper-->\n"

    # --- explicit edits (each must apply exactly once)
    EDITS = [
        # intro: thesis render states its numbering
        ("**John Holder** · Source document for Paper 2 · consolidated by Task 13 · October 2026",
         "**John Holder** · {{paper:Source document for Paper 2}}{{thesis:Thesis numbering, freeze v1 (Task 14), rendered from "
         "`source/Stages_0_4_Source.md` and `register/results.yaml`}} · consolidated by Task 13 · October 2026"),
        ("one number from a single sequence and exactly one Roadmap Section 12 label",
         "{{paper:one number from a single sequence}}{{thesis:its thesis number (chapter.counter, from `register/results.yaml`)}} "
         "and exactly one Roadmap Section 12 label"),
        ("the change log in Section 13 maps every old number to its\nnew one and records every correction.",
         "{{paper:the change log in Section 13 maps every old number to its\nnew one and records every correction.}}"
         "{{thesis:Appendix A (`Appendix_A_Register.md`) lists every thesis result, and `register/crosswalk.md` maps earlier "
         "numbers to thesis numbers.}}"),
        # unheaded starting-study results: cited by thesis number in the thesis render only
        ("All variances are **actual** stationary error variances, never filter-reported ones. The stationary variance is",
         "All variances are **actual** stationary error variances, never filter-reported ones. The stationary variance"
         "{{thesis: ([[stationary-variance]])}} is"),
        ("$\\sigma_\\star^2(\\Pi) = G^\\star/\\Pi = 2\\Sigma/(\\lambda + \\sqrt{\\lambda^2 + 2\\Sigma\\Pi})$.\n",
         "$\\sigma_\\star^2(\\Pi) = G^\\star/\\Pi = 2\\Sigma/(\\lambda + \\sqrt{\\lambda^2 + 2\\Sigma\\Pi})${{thesis: ([[optimal-envelope]])}}.\n"),
        ("({{phase1}}'s discrete excess condition)", "({{phase1}}'s discrete excess condition{{thesis:, [[discrete-excess]]}})"),
        # the split: the addendum becomes its own result directly after the theorem's statement
        ("lower ray ($R^2 < F$) and Empty ($R^2 \\ge F$).\nIf moreover $G$ is increasing",
         "lower ray ($R^2 < F$) and Empty ($R^2 \\ge F$).\n\n"
         "**Label:** [[window-theorem|t]] (proved in {{phase1}} and its verification suite; optimal part re-checked T13 C2 row 1).\n\n"
         "**[[no-mixed-decreasing-ratio]] (no mixed class when $G/\\Pi$ decreases).** In the setting of [[window-theorem]], if "
         "moreover $G$ is increasing"),
        ("*Proof of the addendum.* $2\\Pi^2", "*Proof.* $2\\Pi^2"),
        ("**Label:** [[window-theorem|t]] (proved in {{phase1}} and its verification suite; optimal part re-checked T13 C2 row 1; "
         "addendum proved post hoc\nfrom the T13 C2 row-8 failure, SymPy steps in `t13_audit_classes_diag2.py`).",
         "**Label:** [[no-mixed-decreasing-ratio|t]] (proved post hoc from the T13 C2 row-8 failure, SymPy steps in "
         "`t13_audit_classes_diag2.py`)."),
        ("never join a lower ray ([[window-theorem]], addendum).", "never join a lower ray ([[no-mixed-decreasing-ratio]])."),
        ("| [[window-theorem|n]] | [[window-theorem|t]] | window theorem; optimal monotone along $\\Pi$ | {{phase1}}; T13 C2 |\n",
         "| [[window-theorem|n]] | [[window-theorem|t]] | window theorem; optimal monotone along $\\Pi$ | {{phase1}}; T13 C2 |\n"
         "| [[no-mixed-decreasing-ratio|n]] | [[no-mixed-decreasing-ratio|t]] | no mixed class when $G/\\Pi$ decreases | T13 C2 "
         "(row-8 diagnosis) |\n"),
    ]
    for a, b in EDITS:
        assert src.count(a) == 1, (src.count(a), a[:90])
        src = src.replace(a, b)
    os.makedirs(os.path.join(CLS, "source"), exist_ok=True)
    open(os.path.join(CLS, "source", "Stages_0_4_Source.md"), "w").write(src)
    with open(os.path.join(REG, "crosswalk_v1.yaml"), "w") as fh:
        fh.write("# Verbatim legacy strings of archive/Stages_0_4_Consolidated_v1.md (change log and two remarks).\n"
                 "# Part of the crosswalk: used only by the paper render ({{legacy:id}} inside paper-only content).\n")
        yaml.safe_dump(legacy, fh, allow_unicode=True, sort_keys=False, width=200)
    print("legacy strings", len(legacy), "| warnings", len(C.warn))
    for w_ in C.warn:
        print("  ", w_)


if __name__ == "__main__":
    main()
