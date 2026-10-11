"""C3 (PREREG_t13): references and labels in Stages_0_4_Consolidated.md.
(a) every result reference (full or abbreviated kind + number, ranges included) resolves to a defined result of that kind;
(b) every defined result appears exactly once in the verification appendix with the same kind;
(c) no result header carries two kinds and every label line agrees with its header;
(d) every 'Section N' reference resolves to a top-level heading.
The change log (Section 13) cites old stage numbers and is excluded from (a)."""
import os
import re

from t13_common import CLS, save_json

DOC = os.path.join(CLS, "Stages_0_4_Consolidated.md")
KINDS = ["Theorem", "Proposition", "Lemma", "Corollary", "Numerical result", "Conjecture", "Counterexample", "Definition"]
ABBR = {"Thm": "Theorem", "Thms": "Theorem", "Theorems": "Theorem", "Prop.": "Proposition", "Props": "Proposition",
        "Props.": "Proposition", "Propositions": "Proposition", "Lemmas": "Lemma", "Cor.": "Corollary",
        "Corollaries": "Corollary", "Num.": "Numerical result", "Conj.": "Conjecture", "Def.": "Definition"}
HDR = re.compile(r"^\*\*(" + "|".join(KINDS) + r") (\d+)(?: \([^*]*\))?\.\*\*")
LABEL = re.compile(r"^\*\*Label:\*\* ([A-Za-z ]+?)(?: \(|\.|$)")
REFWORDS = sorted(KINDS + list(ABBR), key=len, reverse=True)
REF = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(w) for w in REFWORDS) + r")\s+(\d+)(?:\s*[–-]\s*(\d+))?(?![.\d]\d)"
                 r"((?:\s*(?:,|and)\s*\d+(?![.\d]\d))*)")


def main():
    doc = open(DOC).read()
    main_part, _, rest = doc.partition("\n## 12. Verification appendix")
    appendix, _, changelog = rest.partition("\n## 13. Change log")
    lines = doc.split("\n")
    errs = {"a": [], "b": [], "c": [], "d": []}
    defined = {}
    order = []
    for i, ln in enumerate(lines):
        m = HDR.match(ln)
        if m:
            kind, num = m.group(1), int(m.group(2))
            if num in defined:
                errs["c"].append(f"line {i+1}: number {num} defined twice")
            defined[num] = kind
            order.append(num)
            if "+" in ln.split("**")[1]:
                errs["c"].append(f"line {i+1}: header with two kinds")
            for j in range(i + 1, min(i + 80, len(lines))):
                lm = LABEL.match(lines[j])
                if lm:
                    lab = lm.group(1).strip()
                    if lab != kind:
                        errs["c"].append(f"line {j+1}: label '{lab}' for {kind} {num}")
                    if "+" in lines[j].split("(")[0]:
                        errs["c"].append(f"line {j+1}: label line with two kinds")
                    break
                if HDR.match(lines[j]):
                    errs["c"].append(f"{kind} {num}: no label line before the next result")
                    break
    seq_ok = sorted(defined) == list(range(1, max(defined) + 1)) and order == sorted(order)
    if not seq_ok:
        errs["c"].append(f"numbering not one increasing sequence 1..{max(defined)}: {order}")
    # (a) references outside the change log
    body = main_part + appendix
    n_refs = 0
    for i, ln in enumerate(body.split("\n")):
        if HDR.match(ln) or ln.startswith("|") and ln.count("|") >= 5 and re.match(r"^\| \d+ \| (" + "|".join(KINDS) + r") \|", ln):
            continue
        for m in REF.finditer(ln):
            word, a, b, more = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            kind = ABBR.get(word, word)
            nums = list(range(a, int(b) + 1)) if b else [a]
            nums += [int(x) for x in re.findall(r"\d+", more or "")]
            for n in nums:
                n_refs += 1
                if defined.get(n) != kind:
                    errs["a"].append(f"line {i+1}: '{m.group(0).strip()}' -> {kind} {n} is {defined.get(n)}")
    # (b) appendix table
    app = {}
    for ln in appendix.split("\n"):
        m = re.match(r"^\| (\d+) \| (" + "|".join(KINDS) + r") \|", ln)
        if m:
            n, k = int(m.group(1)), m.group(2)
            if n in app:
                errs["b"].append(f"appendix lists {n} twice")
            app[n] = k
    for n, k in defined.items():
        if app.get(n) != k:
            errs["b"].append(f"{k} {n}: appendix says {app.get(n)}")
    for n in app:
        if n not in defined:
            errs["b"].append(f"appendix row {n} has no result")
    # (d) section references
    heads = {int(m.group(1)) for m in re.finditer(r"^## (\d+)\.", doc, re.M)}
    subheads = {m.group(1) for m in re.finditer(r"^### (\d+\.\d+)", doc, re.M)}
    for m in re.finditer(r"Sections? (\d+(?:\.\d+)?)(?:[–-](\d+))?", main_part + appendix):
        for s_ in ([m.group(1)] + ([m.group(2)] if m.group(2) else [])):
            ok = (int(s_) in heads) if "." not in s_ else (s_ in subheads)
            ctx = (main_part + appendix)[max(0, m.start() - 40):m.end() + 10]
            if not ok and "Roadmap" not in ctx and "Section 12 label" not in ctx:
                errs["d"].append(f"'Section {s_}' does not resolve: ...{ctx}...")
    res = {"n_results": len(defined), "n_refs_checked": n_refs, "errors": errs, "n_errors": sum(len(v) for v in errs.values()),
           "kinds": {k: sum(v == k for v in defined.values()) for k in KINDS}}
    res["pass"] = res["n_errors"] == 0
    for k, v in errs.items():
        for e in v:
            print(k, e)
    print(f"C3: {'PASS' if res['pass'] else 'FAIL'}; results {len(defined)}, references {n_refs}, errors {res['n_errors']}; {res['kinds']}")
    save_json(res, "t13_audit_refs.json")


if __name__ == "__main__":
    main()
