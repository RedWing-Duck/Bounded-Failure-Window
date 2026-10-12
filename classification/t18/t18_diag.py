"""Post-hoc diagnosis of the T18 failures (results/t18_checks.json, recorded on f77ab8f). Not a pass criterion.
- F1 [47]: the recorded search for "[47]" sentences covered the whole draft, including Appendix D's quotation of the Task 17 finding;
  restricted to chapters 1-9.
- F1 [21]: where "[21–23]" still occurs.
- F2: rows whose verdict cell begins with PASS or FAIL but carries a qualifier (e.g. "PASS (info)"); recount with that reading,
  which is the pre-registered wording ("says PASS or FAIL").
- F2: the Appendix D failures the automatic attribution parser could not read, mapped by hand.
- F6: Appendix A difference with $...$ math delimiters removed.
Usage: python3 t18_diag.py"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import t18_checks as T18  # noqa: E402


def main():
    C = json.load(open(os.path.join(HERE, "results", "t18_checks.json")))
    R = {}
    L = T18.draft_lines()
    end = next(k for k, l in enumerate(L) if l.startswith("## Appendices"))
    body = T18.unesc("\n".join(L[:end]))
    s47 = [s for s in re.split(r"(?<=[.!?])\s+", body) if "[47]" in s]
    R["F1_s47_chapters_only"] = {"sentences": s47, "all_model_error": all("model error" in s for s in s47), "n": len(s47),
                                 "text": "Restricted to chapters 1–9, both [47] sentences say 'time-correlated model error'. The recorded "
                                         "failure came from Appendix D's quotation of the Task 17 finding. Attribution: code (scope)."}
    occ = [(k + 1, l[:300]) for k, l in enumerate(L) if "21–23" in l]
    R["F1_s21_remaining"] = {"lines": occ,
                             "text": "§1.6 still says monotonicity under garbling 'extends to sequential experiments [20] and stochastic "
                                     "control and teams [21–23]'. §7.1 was fixed; §1.6 was not. Attribution: document."}
    qual, per = [], {}
    for n in range(1, 18):
        rows = T18.task_rows(n)
        t = open(os.path.join(T18.REPO, T18.TASKFILES[n])).read()
        extra = []
        if n <= 7 and n != 6:
            for l in t.split("\n"):
                if re.match(rf"^\| T{n}\.\d", l):
                    cells = [c.strip().replace("*", "") for c in l.strip().strip("|").split("|")]
                    v = next((c for c in cells if re.match(r"^(PASS|FAIL)\b", c) and c not in ("PASS", "FAIL")), None)
                    if v and not any(c in ("PASS", "FAIL") for c in cells):   # only rows the recorded parser skipped
                        extra.append((cells[0], v))
        qual += [(n,) + e for e in extra]
        per[n] = len(rows) + len(extra)
    R["F2_qualified_verdicts"] = {"rows": qual, "recount_total": sum(per.values()), "per_task": per,
                                  "text": "Task 2's T2.1c reads 'PASS (info)'; the recorded parser required the cell to equal PASS. With "
                                          "the pre-registered reading ('says PASS'), the total is the sum above. Attribution: code."}
    R["F2_unparsed_attributions"] = {
        "T10.2 A1.3 as specified: plan's construction (criterion as pre-registered)": "criterion",
        "T10.5 pair birth: criterion.": "criterion",
        "T10.6 matched-variance τ (zero-limit shape check): criterion.": "criterion",
        "C1 numbers, first run (T13): document (4, a truncated worked value) and code (2, parser)": "document, code",
        "text": "The automatic mapper looked for an attribution between ':' and ' — '; these four lines end without ' — '. Each names a "
                "listed attribution. Attribution of the recorded gap: code."}
    a = C["F6"]["A"]["differences"]
    R["F6_A_math_delimiters"] = {"differences": a, "same_without_dollars": all(
        (d["draft"] or "").replace("$", "") == (d["render"] or "").replace("$", "") for d in a),
        "text": "The only Appendix A difference is '$n = 2$' vs 'n = 2' (math delimiters): formatting the normaliser did not remove. "
                "Attribution: code."}
    json.dump(R, open(os.path.join(HERE, "results", "t18_diag.json"), "w"), indent=1, ensure_ascii=False, default=str)
    print("s47 chapters:", R["F1_s47_chapters_only"]["n"], R["F1_s47_chapters_only"]["all_model_error"], "| [21–23] lines:",
          [x[0] for x in occ], "| qualified:", qual, "recount", R["F2_qualified_verdicts"]["recount_total"],
          "| A same w/o $:", R["F6_A_math_delimiters"]["same_without_dollars"])


if __name__ == "__main__":
    main()
