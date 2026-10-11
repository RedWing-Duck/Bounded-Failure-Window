"""Format references.bib entries for Appendix C (Task 15): one line per entry,
`[n] Last, I. & Last, I. (year). Title. Journal vol(no), pages. doi:…`.
Rules (from the thesis draft's Appendix C):
- two authors "A & B"; three "A, B & C"; four or more, or an "and others" list, "First et al.";
- hyphenated initials printed spaced (J.-H. -> J. H.);
- LaTeX accents, braces and $...$ Greek converted to Unicode;
- article: "Journal vol(no), pages"; book: "Publisher" (no series, volume, address, ISBN or note);
- inproceedings/incollection: "booktitle[ volume], pages" (no publisher);
- misc with an arXiv eprint and no venue: "arXiv:id";
- "doi:…" appended when present (no final period after it)."""
import re

ACC = [('{\\"u}', "ü"), ('{\\"a}', "ä"), ('{\\"o}', "ö"), ("{\\c{s}}", "ş"), ("{\\'\\i}", "í"), ("{\\'e}", "é"),
       ("\\&", "&")]
GREEK = {r"\alpha": "α", r"\beta": "β", r"\gamma": "γ"}


def parse(path):
    txt = open(path).read()
    out = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),\n(.*?)\n\}", txt, re.S):
        f = {}
        for fm in re.finditer(r"^\s*(\w+) = \{(.*)\},?\s*$", m.group(3), re.M):
            f[fm.group(1)] = fm.group(2)
        f["_type"] = m.group(1)
        out[m.group(2).strip()] = f
    return out


def tex(s):
    for a, b in ACC:
        s = s.replace(a, b)
    s = re.sub(r"\$([^$]*)\$", lambda m: "".join(GREEK.get(t, t) for t in re.split(r"(\\[a-z]+)", m.group(1))), s)
    return s.replace("{", "").replace("}", "").replace("--", "–")


def names(a):
    ps = [p.strip() for p in tex(a).split(" and ")]
    ps = [re.sub(r"([A-Z])\.-([A-Z])\.", r"\1. \2.", p) for p in ps]
    if "others" in ps or len(ps) >= 4:
        return ps[0] + " et al."
    if len(ps) == 1:
        return ps[0]
    return ", ".join(ps[:-1]) + " & " + ps[-1]


def fmt(n, f):
    t = f["_type"]
    title = tex(f["title"])
    s = f"[{n}] {names(f['author'])} ({f['year']}). {title}{'' if title.endswith(('?', '!')) else '.'} "
    pages = tex(f.get("pages", ""))
    if t == "article":
        v = tex(f["journal"])
        if f.get("volume"):
            v += f" {f['volume']}" + (f"({f['number']})" if f.get("number") else "")
        s += v + (f", {pages}" if pages else "") + "."
    elif t in ("inproceedings", "incollection"):
        v = tex(f["booktitle"]) + (f" {f['volume']}" if f.get("volume") else "")
        s += v + (f", {pages}" if pages else "") + "."
    elif t == "book":
        s += tex(f["publisher"]) + "."
    else:   # misc
        s += f"arXiv:{f['eprint']}." if f.get("eprint") else ""
    if f.get("doi"):
        s += f" doi:{f['doi']}"
    return s.rstrip()
