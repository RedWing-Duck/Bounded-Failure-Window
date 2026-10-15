"""Task 20 register update (PREREG_t20.md, changes 1-3). Run after t19/t19_register.py in the render chain.
- results.yaml: titles of 2.1, 2.8, 5.1, 6.17, 6.19; 8.1 = narrow-windows and 8.2 = blind-searches (thesis_no and file order,
  so Appendix A stays in number order); Lemma 7.6a whole-path-garbling inserted after 7.6 (status to-verify, verified_by empty);
  6.13 discrete-excess also cites sahomasugi2016 (after roberts1959).
- references.yaml: [54]-[60] appended (frozen numbering: a new reference takes the next free number). [54]-[59] are attached to
  no result (cited only in the thesis's chapter 1, which has no source here); [60] is attached to 6.13.
- crosswalk.md regenerated from results.yaml (same layout as t16/t16_register.py).
Idempotent. Usage: python3 t20_register.py"""
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REG = os.path.join(CLS, "register")

TITLES = {"topological-realizability": "Topological realisability",
          "reparameterisation": "Reparameterisation (orientation swaps ℓ and h)",
          "realizability": "Gain realisability",
          "d3-excess": "D3 excess set; onset ρ > 2 + ν",
          "dt-optimal-mp": "Optimal M-P along Δt: posterior ↓; prior ↑; averaged ↑"}
NUMBERS = {"narrow-windows": "8.1", "blind-searches": "8.2"}
LEMMA = {"key": "whole-path-garbling", "thesis_no": "7.6a", "type": "Lemma",
         "title": "Whole-path garbling (step (iv) ⇒ (ii) of Theorem 7.6)", "chapter": 7, "cons_v1": None, "legacy": [],
         "verified_by": [], "status": "to-verify", "citations": []}
FIRST = "draft §1.6 Contributions and relation to prior work"
NEW_REFS = [(54, "sinopoli2004"), (55, "wu2018"), (56, "jiang2026"), (57, "bosov2026"), (58, "gotovos2013"), (59, "tenne2002"),
            (60, "sahomasugi2016")]
ATTACH = {"discrete-excess": ["sahomasugi2016"]}


def dump(path, data):
    head = "".join(l for l in open(path) if l.startswith("#"))
    with open(path, "w") as fh:
        fh.write(head)
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False, width=200, default_flow_style=None)


def results():
    p = os.path.join(REG, "results.yaml")
    res = yaml.safe_load(open(p))
    for e in res:
        if e["key"] in TITLES:
            e["title"] = TITLES[e["key"]]
        if e["key"] in NUMBERS:
            e["thesis_no"] = NUMBERS[e["key"]]
        for c in ATTACH.get(e["key"], []):
            if c not in e["citations"]:
                e["citations"].append(c)
    # file order of the two swapped entries follows their numbers
    i, j = (next(k for k, e in enumerate(res) if e["key"] == key) for key in ("narrow-windows", "blind-searches"))
    if i > j:
        res[i], res[j] = res[j], res[i]
    if not any(e["key"] == LEMMA["key"] for e in res):
        k = next(k for k, e in enumerate(res) if e["key"] == "gaussian-orderings-coincide")
        res.insert(k + 1, dict(LEMMA))
    dump(p, res)
    return res


def references():
    p = os.path.join(REG, "references.yaml")
    refs = yaml.safe_load(open(p))
    have = {r["key"] for r in refs}
    for n, k in NEW_REFS:
        if k not in have:
            refs.append({"number": n, "key": k, "first_cited": FIRST, "status": "cited"})
    nums = [r["number"] for r in refs]
    assert nums == list(range(1, len(refs) + 1)), "frozen numbering broken"
    assert len({r["key"] for r in refs}) == len(refs), "duplicate reference key"
    head = "".join(l for l in open(p) if l.startswith("#"))
    with open(p, "w") as fh:
        fh.write(head)
        yaml.safe_dump(refs, fh, allow_unicode=True, sort_keys=False, width=200)
    return refs


def crosswalk(res):
    cw = ["# Crosswalk: thesis numbers, keys, consolidated v1 numbers and legacy labels", "",
          "Legacy labels live only here (and, for the paper render of v1's change log, in `crosswalk_v1.yaml`). Thesis-facing "
          "documents use thesis numbers rendered from `results.yaml`. Every legacy label carries the prefix \"legacy\" (Task 16), "
          "so it cannot be read as a figure label B.n.", "", "| No. | Key | Cons. v1 | Legacy |", "|---|---|---|---|"]
    for e in res:
        cw.append(f"| {e['thesis_no']} | `{e['key']}` | {e['cons_v1'] or '—'} | {'; '.join(e['legacy'])} |")
    open(os.path.join(REG, "crosswalk.md"), "w").write("\n".join(cw) + "\n")


def main():
    res = results()
    refs = references()
    crosswalk(res)
    print(f"results.yaml: {len(res)} entries; references.yaml: {len(refs)} entries; crosswalk.md regenerated")


if __name__ == "__main__":
    main()
