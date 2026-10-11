"""Write t14/bib_check.md: DOI resolution outcomes (from check C9 in results/t14_checks.json), the evidence for every field
confirmed by web search, the entries confirmed by the starting-study manuscript's reference list, and every VERIFY flag left in
references.bib. Usage: python3 make_bib_check.py"""
import json
import os
import re

from t14_common import CLS, HERE, RES

EVID = [  # (key, field(s), value, evidence URL) -- link title or URL only; search summaries did not count
    ("heffes1966", "title", "The effect of erroneous models on the Kalman filter response", "https://www.semanticscholar.org/paper/The-effect-of-erroneous-models-on-the-Kalman-filter-Heffes/6d05ab2b09a41735c211fc9257e2ede0bd7d6ae3"),
    ("kurt2025", "arXiv id, title", "2511.22034; Performance of the Kalman Filter and Smoother for Benchmark Studies", "https://arxiv.org/html/2511.22034v1"),
    ("kalman1960", "title, DOI", "A New Approach to Linear Filtering and Prediction Problems; 10.1115/1.3662552", "https://www.citedrive.com/en/discovery/a-new-approach-to-linear-filtering-and-prediction-problems"),
    ("jazwinski1970", "ISBN", "978-0-12-381550-7 (Elsevier listing)", "https://shop.elsevier.com/books/stochastic-processes-and-filtering-theory/jazwinski/978-0-12-381550-7"),
    ("simon2006", "publisher, ISBN", "Wiley; 978-0-471-70858-2", "https://wiley-vch.de/en/areas-interest/engineering/optimal-state-estimation-978-0-471-70858-2"),
    ("chang2014", "title, DOI", "On Kalman filter for linear system with colored measurement noise; 10.1007/s00190-014-0751-7", "https://link.springer.com/article/10.1007/s00190-014-0751-7"),
    ("kalata1984", "title", "The Tracking Index: A Generalized Parameter for α-β and α-β-γ Target Trackers", "https://www.semanticscholar.org/paper/The-Tracking-Index:-A-Generalized-Parameter-for-%CE%B1-%CE%B2-Kalata/37dc628deaa03dcdd8a3ecfac219e562d2e771d6"),
    ("kalata1984", "volume", "20 (first page 174)", "https://ui.adsabs.harvard.edu/abs/1984ITAES..20..174K/abstract"),
    ("sahomasugi2016", "title, DOI", "α–β–γ tracking filters using acceleration measurements; 10.1186/s40064-016-1960-8", "https://springerplus.springeropen.com/articles/10.1186/s40064-016-1960-8"),
    ("barshalom2002", "title", "Update with out-of-sequence measurements in tracking: exact solution", "https://www.researchgate.net/publication/3003506_Update_with_out-of-sequence_measurements_in_tracking_exact_solution"),
    ("yoder2018", "title, DOI", "Exploring the Exponentially Decaying Merit of an Out-of-Sequence Observation; 10.3390/s18061947", "https://www.mdpi.com/1424-8220/18/6/1947"),
    ("yuksellinder2012", "title, DOI", "Optimization and Convergence of Observation Channels in Stochastic Control; 10.1137/100808976", "https://epubs.siam.org/doi/10.1137/100808976"),
    ("lecam1964", "title, issue, DOI", "Sufficiency and Approximate Sufficiency; 35(4); 10.1214/aoms/1177700372", "https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-4/Sufficiency-and-Approximate-Sufficiency/10.1214/aoms/1177700372.full"),
    ("hansentorgersen1974", "title, issue, DOI", "Comparison of Linear Normal Experiments; 2(2); 10.1214/aos/1176342672", "https://projecteuclid.org/journals/annals-of-statistics/volume-2/issue-2/Comparison-of-Linear-Normal-Experiments/10.1214/aos/1176342672.full"),
    ("hotzskelton1985", "title", "A covariance control theory", "https://www.semanticscholar.org/paper/A-covariance-control-theory-Hotz-Skelton/c519b536f3de8e6e70c43600255a63df65dddccf"),
    ("collinsskelton1987", "title", "A theory of state covariance assignment for discrete systems", "https://ieeexplore.ieee.org/document/1104443/"),
    ("yasuda1993", "title", "Covariance controllers: a new parametrization of the class of all stabilizing controllers", "https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/1685965"),
    ("shmaliy2020", "title, first author, year, DOI", "as in the bib; 10.1049/iet-spr.2019.0166", "https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-spr.2019.0166"),
    ("greenshtein1996", "title, volume, issue, DOI", "Comparison of sequential experiments; 24(1); 10.1214/aos/1033066220", "https://projecteuclid.org/journals/annals-of-statistics/volume-24/issue-1/Comparison-of-sequential-experiments/10.1214/aos/1033066220.pdf"),
    ("yukselbasar2024", "title, DOI", "Comparison of Information Structures and Their Blackwell Ordering; 10.1007/978-3-031-54071-4_7", "https://link.springer.com/chapter/10.1007/978-3-031-54071-4_7"),
    ("blackwell1953", "title, volume, issue, DOI", "Equivalent Comparisons of Experiments; 24(2); 10.1214/aoms/1177729032", "https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-24/issue-2/Equivalent-Comparisons-of-Experiments/10.1214/aoms/1177729032.short"),
]
MANUSCRIPT = ["boominathan2022", "crouse2023", "friedland1967", "friston2010", "ge2016", "griffin1968", "heffes1966", "kalmanbucy1961",
              "nishimura1967", "ren2021", "sangsukiam1990", "singh2009", "teunissen2021"]


def main():
    c9 = json.load(open(os.path.join(RES, "t14_checks.json")))["C9"]
    bib = open(os.path.join(CLS, "references.bib")).read()
    verify = re.findall(r"@\w+\{([^,]+),.*?note = \{VERIFY: (.*?)\}\n\}", bib, re.S)
    L = ["# Bibliography check (Task 14)", "",
         "`classification/references.bib` has 53 entries, built by `t14/make_bib.py`. Every field comes from one of three "
         "sources:",
         "- the Task 14 prompt;",
         "- the starting-study manuscript's reference list (`reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf`, "
         "pp. 16–17);",
         "- a web-search result whose link title or URL shows the field (table below).", "",
         "A search engine's generated summary was never accepted as evidence. A field the prompt flagged and none of the three "
         "sources confirmed was left out and named in the entry's `VERIFY` note.", "",
         "## DOI resolution at doi.org", "",
         f"Check C9 tried `https://doi.org/<doi>` once for each of the {c9['doi_entries']} entries that carry a DOI, with "
         f"curl and a 20 s timeout. {c9['doi_resolved']} resolved. The session's network policy blocks doi.org: the proxy "
         "rejects the CONNECT, and WebFetch cannot resolve the host either. Every DOI entry therefore carries `VERIFY: DOI not "
         "resolved at doi.org`.", "", "| Key | DOI | HTTP | Outcome |", "|---|---|---|---|"]
    for k, v in sorted(c9["doi"].items()):
        L.append(f"| {k} | {v['doi']} | {v['http']} | {'resolved' if v['resolved'] else 'not resolved: ' + v['error']} |")
    L += ["", "## Fields confirmed by web search", "",
          "Search run by a subagent of this session (37 searches) and by the session itself. A field counts only through a "
          "link title or URL.", "", "| Key | Field(s) | Value | Evidence |", "|---|---|---|---|"]
    L += [f"| {k} | {f} | {v} | {u} |" for k, f, v, u in EVID]
    L += ["", "## Confirmed by the starting-study manuscript", "",
          "The details of these entries match the manuscript's reference list, p. 16–17: " + ", ".join(MANUSCRIPT) + ".", "",
          "## Discrepancies found", "",
          "- `barshalom2002`: the prompt gives pp. 769–778. The IEEE record, as quoted in a search summary, gives 769–777. The "
          "pages are left out and flagged.",
          "- `blackwell1951`: the evidence points to pp. 93–102, not 99–102, but only through summaries, so the pages are "
          "flagged.",
          "- `kalata1984`: sources disagree on the last page (174–182 and 174–181). The pages and the prompt's DOI are left out "
          "and flagged.",
          "- `skeltonikeda1989`: nothing was confirmed by search, not even the author pairing or the volume and pages.",
          "", "## VERIFY flags left in references.bib", "", "| Key | Still to verify |", "|---|---|"]
    L += [f"| {k} | {n} |" for k, n in verify]
    L += ["", f"Entries never cited (check C9): {', '.join(c9['unused']) or 'none'}."]
    open(os.path.join(HERE, "bib_check.md"), "w").write("\n".join(L) + "\n")
    print(len(verify), "VERIFY flags")


if __name__ == "__main__":
    main()
