"""Render key-token sources with numbers from register/results.yaml (Task 14, freeze v1).

Tokens: [[key]] type + number; [[key|n]] number; [[key|t]] type; [[key|a]] abbreviated type + number;
{{phase1}} ("the starting study (Tasks 1–7)" / "Paper 1"; {{phase1}}'s -> "the starting study's" in the thesis render);
{{thesis:...}} / {{paper:...}} and <!--thesis-->...<!--/thesis--> / <!--paper-->...<!--/paper--> keep content in one mode;
{{legacy:id}} (paper only) renders a verbatim string from register/crosswalk_v1.yaml; {{matrix}} renders register/matrix.csv.

Numbering: thesis = the register's thesis_no; paper = 1, 2, 3, ... over headed results (a line starting "**[[key]] ") in
order of appearance in source/Stages_0_4_Source.md. Mode v1check (used by Task 14 check C4) prints each key's consolidated v1
number instead ("6+" for the result split from v1's Theorem 6).

Usage:
  python3 render.py --numbering thesis    # Stages_0_4_Thesis.md, Roadmap_v3.md, figs_thesis/, Appendix_A_Register.md, ../reference/phase1/
  python3 render.py --numbering paper     # Stages_0_4_Paper2.md
  python3 render.py --numbering v1check --out FILE
Exit status 1 if any token fails to resolve."""
import argparse
import csv
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CLS = os.path.dirname(HERE)
SRC = os.path.join(CLS, "source")
ABBR = {"Theorem": "Thm", "Proposition": "Prop.", "Corollary": "Cor.", "Numerical result": "Num.", "Lemma": "Lemma",
        "Definition": "Def.", "Conjecture": "Conj.", "Counterexample": "Counterex."}
HEADED = re.compile(r"^\*\*\[\[([a-z0-9-]+)\]\] ", re.M)


def load():
    reg = yaml.safe_load(open(os.path.join(HERE, "results.yaml")))
    leg = {e["id"]: e["text"] for e in yaml.safe_load(open(os.path.join(HERE, "crosswalk_v1.yaml")))}
    return {e["key"]: e for e in reg}, leg


def numbering(mode, reg):
    if mode == "thesis":
        return {k: e["thesis_no"] for k, e in reg.items()}
    heads = HEADED.findall(strip_cond(open(os.path.join(SRC, "Stages_0_4_Source.md")).read(), "paper"))   # paper-visible text only
    if mode == "paper":
        return {k: str(i + 1) for i, k in enumerate(heads)}
    out = {}
    for k in heads:
        m = re.match(r"^(\d+)(?: \(main part\))?$", reg[k]["cons_v1"] or "")
        out[k] = m.group(1) if m else "6+"
    return out


def strip_cond(text, mode):
    """Remove the other mode's block and inline conditionals (balanced {{ }} scan); keep this mode's content."""
    other = "paper" if mode == "thesis" else "thesis"
    keep = "thesis" if mode == "thesis" else "paper"
    text = re.sub(r"<!--" + other + r"-->\n.*?<!--/" + other + r"-->\n", "", text, flags=re.S)
    text = re.sub(r"<!--/?" + keep + r"-->\n", "", text)
    out, i = [], 0
    while True:
        j = min([p for p in (text.find("{{thesis:", i), text.find("{{paper:", i)) if p >= 0], default=-1)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        tag = "thesis" if text.startswith("{{thesis:", j) else "paper"
        k, depth = j + len(tag) + 3, 1
        while depth:
            if text.startswith("{{", k):
                depth, k = depth + 1, k + 2
            elif text.startswith("}}", k):
                depth, k = depth - 1, k + 2
            else:
                k += 1
        inner = text[j + len(tag) + 3:k - 2]
        if tag == keep:
            out.append(strip_cond(inner, mode))
        i = k
    return "".join(out)


class Renderer:
    def __init__(self, mode):
        self.mode = mode
        self.reg, self.leg = load()
        self.num = numbering(mode, self.reg)
        self.errors = []
        self.refs = {e["key"]: e["number"] for e in yaml.safe_load(open(os.path.join(HERE, "references.yaml")))}
        self.figs = {e["key"]: e["label"] for e in yaml.safe_load(open(os.path.join(HERE, "figures.yaml")))}

    def cite(self, m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        nums = []
        for k in keys:
            if k not in self.refs:
                self.errors.append(f"unknown citation key {k}")
                return m.group(0)
            nums.append(self.refs[k])
        return "[" + compress(nums) + "]"

    def fig(self, m):
        key, form = m.group(1), m.group(2) or ""
        if key not in self.figs:
            self.errors.append(f"unknown figure key {key}")
            return m.group(0)
        return self.figs[key] if form == "|n" else f"Figure {self.figs[key]}"

    def ref(self, m):
        key, form = m.group(1), m.group(2) or ""
        if key not in self.reg:
            self.errors.append(f"unresolved key {key}")
            return f"??{key}??"
        typ = self.reg[key]["type"]
        if form == "|t":
            return typ
        if key not in self.num:
            self.errors.append(f"no number for {key} in {self.mode} render (not headed)")
            return f"??{key}??"
        n = self.num[key]
        return {"": f"{typ} {n}", "|n": n, "|a": f"{ABBR[typ]} {n}"}[form]

    def inline(self, text):
        text = strip_cond(text, "thesis" if self.mode == "thesis" else "paper")
        if self.mode == "thesis" and "{{legacy:" in text:
            self.errors.append("legacy token outside paper-only content")
        text = re.sub(r"\{\{legacy:(L\d+)\}\}", lambda m: self.leg[m.group(1)], text)
        if self.mode == "thesis":   # sentence-initial occurrences are capitalised
            text = re.sub(r"([.!?]\)?\s+|[.!?]\*\*\s+)\{\{phase1\}\}", lambda m: m.group(1) + "{{Phase1}}", text)
            text = text.replace("{{Phase1}}'s", "The starting study's").replace("{{Phase1}}", "The starting study (Tasks 1–7)")
            text = text.replace("{{phase1}}'s", "the starting study's").replace("{{phase1}}", "the starting study (Tasks 1–7)")
        else:
            text = text.replace("{{phase1}}", "Paper 1")
        text = re.sub(r"\[\[([a-z0-9-]+)(\|[nta])?\]\]", self.ref, text)
        text = re.sub(r"\[(@[a-z][a-z0-9-]*(?:;\s*@[a-z][a-z0-9-]*)*)\]", self.cite, text)
        text = re.sub(r"\{\{fig:([a-z0-9-]+)(\|n)?\}\}", self.fig, text)
        left = re.findall(r"\{\{[^}]*\}\}|\[\[[^\]]*\]\]", text)
        if left:
            self.errors.append(f"unrendered tokens {left[:5]}")
        return text

    def matrix(self):
        rows = list(csv.reader(open(os.path.join(HERE, "matrix.csv"))))
        lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * len(rows[0])]
        lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(lines)

    def render(self, text):
        text = re.sub(r"\{\{include:([\w./-]+)\}\}", lambda m: open(os.path.join(SRC, m.group(1))).read().rstrip("\n"), text)
        return self.inline(text.replace("{{matrix}}", self.matrix()))


def block_span(L, key):
    """Lines of result `key` in the source: its **[[key]] line through the end of its proof (a line ending in $\\square$ or ∎);
    if no proof comes before the next **Label:** line, result label, heading or rule, through the last statement line before it.
    (Task 18: statements of several paragraphs, such as Theorem 2.2's, are covered.)"""
    i = next(j for j, l in enumerate(L) if l.startswith(f"**[[{key}]]"))
    k = i + 1
    while k < len(L) and not (L[k].startswith("*Proof") or L[k].startswith("**Label:") or L[k].startswith("**[[")
                              or L[k].startswith("#") or L[k].startswith("---")):
        k += 1
    if k < len(L) and L[k].startswith("*Proof"):
        e = k
        while not (L[e].rstrip().endswith("$\\square$") or L[e].rstrip().endswith("∎")):
            e += 1
        return i, e
    e = k - 1
    while e > i and not L[e].strip():
        e -= 1
    return i, e


def apply_overrides(doc):
    """Task 17: thesis-only replacements and insertions (register/thesis_overrides.yaml), thesis render only."""
    L = doc.split("\n")
    for o in yaml.safe_load(open(os.path.join(HERE, "thesis_overrides.yaml"))):
        txt = open(os.path.join(SRC, o["file"])).read().rstrip("\n").split("\n")
        if "replace" in o:
            i, j = block_span(L, o["replace"])
            L[i:j + 1] = txt
        else:
            i = (L.index(o["insert_before"]) if "insert_before" in o else
                 next(j for j, l in enumerate(L) if l.startswith(f"**[[{o['insert_before_key']}]]")))
            L[i:i] = txt + [""]
    return "\n".join(L)


def appendix(r):
    out = ["# Appendix A. Register of results", "",
           "Rendered from `register/results.yaml` (freeze v1, Task 14). Numbers are thesis numbers: one counter per chapter, shared "
           "by all result types. Verification task identifiers are listed in `register/tasks.yaml`; earlier labels are in "
           "`register/crosswalk.md`.", "", "| No. | Type | Result | Key | Verified by | Status |", "|---|---|---|---|---|---|"]
    for k, e in r.reg.items():
        vb = ", ".join(e["verified_by"]) or "—"
        out.append(f"| {e['thesis_no']} | {e['type']} | {e['title']} | `{k}` | {vb} | {e['status']} |")
    return "\n".join(out) + "\n"


def appendix_c():
    import bibfmt
    bib = bibfmt.parse(os.path.join(CLS, "references.bib"))
    R = yaml.safe_load(open(os.path.join(HERE, "references.yaml")))
    out = ["# Appendix C. References", "",
           "Numbered in order of first citation; a number, once assigned, does not change. References [46]–[53] are first cited "
           "in chapters 6–7. Rendered from `register/references.yaml` and `references.bib` (Task 19 wording).", ""]
    for r in R:
        out += [bibfmt.fmt(r["number"], bib[r["key"]]), ""]
    return "\n".join(out)


def appendix_b(r):
    F = yaml.safe_load(open(os.path.join(HERE, "figures.yaml")))
    out = ["# Appendix B. Figures", "",
           "The images carry no result or figure numbers; the text cites each one as Figure B.n. Rendered from "
           "`register/figures.yaml`. Images are in `figs_thesis/`.", ""]
    for e in F:
        out += [f"**Figure {e['label']}.** " + r.inline(e.get("description", "")), "",
                f"![Figure {e['label']}](figs_thesis/{e['label']}_{e['key']}.png)", ""]
    return "\n".join(out)


def compress(nums):
    """Sorted citation numbers; runs of three or more consecutive numbers as n–m."""
    ns, out, i = sorted(set(nums)), [], 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out += [f"{ns[i]}–{ns[j]}"] if j - i >= 2 else [str(x) for x in ns[i:j + 1]]
        i = j + 1
    return ", ".join(out)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--numbering", choices=["thesis", "paper", "v1check"], required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    r = Renderer(a.numbering)
    doc = open(os.path.join(SRC, "Stages_0_4_Source.md")).read()
    if a.numbering == "thesis":
        write(os.path.join(CLS, "Stages_0_4_Thesis.md"), r.render(apply_overrides(doc)))
        write(os.path.join(CLS, "Roadmap_v3.md"), r.render(open(os.path.join(SRC, "Roadmap_v3_Source.md")).read()))
        figmap = {os.path.basename(e["caption_source"]): f"{e['label']}_{e['key']}.txt"
                  for e in yaml.safe_load(open(os.path.join(HERE, "figures.yaml"))) if e.get("caption_source")}
        for f in sorted(os.listdir(os.path.join(SRC, "figs"))):
            write(os.path.join(CLS, "figs_thesis", figmap.get(f, f)), r.render(open(os.path.join(SRC, "figs", f)).read()))
        write(os.path.join(CLS, "Appendix_A_Register.md"), appendix(r))
        write(os.path.join(CLS, "Appendix_B_Figures.md"), appendix_b(r))
        write(os.path.join(CLS, "Appendix_C_References.md"), appendix_c())
        for f in sorted(os.listdir(os.path.join(SRC, "phase1"))):
            write(os.path.join(os.path.dirname(CLS), "reference", "phase1", f), r.render(open(os.path.join(SRC, "phase1", f)).read()))
    elif a.numbering == "paper":
        write(os.path.join(CLS, "Stages_0_4_Paper2.md"), r.render(doc))
    else:
        write(a.out, r.render(doc))
    for e in r.errors:
        print("ERROR", e, file=sys.stderr)
    print(f"{a.numbering}: {len(r.errors)} errors")
    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
