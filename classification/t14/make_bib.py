"""Task 14 §6: write classification/references.bib. SUPERSEDED after Task 14 by the author-verified file; running this overwrites it.
Sources of each field: (P) the Task 14 prompt; (M) the starting-study manuscript's reference list
(reference/phase1/Holder_2026_Bounded_Failure_Window_Final.pdf, p. 16-17); (S) a web-search result whose link title/URL or a
fetched publisher page shows the field (evidence in t14/bib_check.md). Fields flagged VERIFY in the prompt and not confirmed by
(M) or (S) are omitted and named in a VERIFY note. doi.org is unreachable from this session, so every DOI also carries
"VERIFY: DOI not resolved at doi.org".
Usage: python3 make_bib.py"""
import os

from t14_common import CLS

NODOI = "DOI not resolved at doi.org (unreachable from this session)"
E = []


def add(key, typ, verify=(), **f):
    E.append((key, typ, f, list(verify)))


# --- background already cited by the starting study (fields as in its reference list, M = P)
add("heffes1966", "article", ["DOI not captured"], author="Heffes, H.", title="The effect of erroneous models on the Kalman filter response",
    journal="IEEE Transactions on Automatic Control", volume="11", number="3", pages="541--543", year="1966")
add("friedland1967", "article", author="Friedland, B.", title="On the effect of incorrect gain in {K}alman filter",
    journal="IEEE Transactions on Automatic Control", volume="12", number="5", pages="610", year="1967")
add("nishimura1967", "article", author="Nishimura, T.", title="Error bounds of continuous {K}alman filters and the application to orbit determination problems",
    journal="IEEE Transactions on Automatic Control", volume="12", number="3", pages="268--275", year="1967")
add("griffin1968", "article", author="Griffin, R. E. and Sage, A. P.", title="Large and small scale sensitivity analysis of optimum estimation algorithms",
    journal="IEEE Transactions on Automatic Control", volume="13", number="4", pages="320--329", year="1968")
add("sangsukiam1990", "article", author="Sangsuk-Iam, S. and Bullock, T. E.", title="Analysis of discrete-time {K}alman filtering under incorrect noise covariances",
    journal="IEEE Transactions on Automatic Control", volume="35", number="12", pages="1304--1309", year="1990")
add("ge2016", "article", author="Ge, Q. and Shao, T. and Duan, Z. and Wen, C.", title="Performance analysis of the {K}alman filter with mismatched noise covariances",
    journal="IEEE Transactions on Automatic Control", volume="61", number="12", pages="4014--4019", year="2016")
add("teunissen2021", "article", author="Teunissen, P. J. G. and Khodabandeh, A. and Psychas, D.",
    title="A generalized {K}alman filter with its precision in recursive form when the stochastic model is misspecified",
    journal="Journal of Geodesy", volume="95", pages="108", year="2021")
add("crouse2023", "inproceedings", author="Crouse, D. F.", title="Mismatched filter design applied to {1D} and {2D} sinusoidal models",
    booktitle="Proceedings of the 26th International Conference on Information Fusion (FUSION 2023)", publisher="IEEE", year="2023")
add("ren2021", "article", author="Ren, H. and Amezcua, J. and van Leeuwen, P. J.", title="Effects of misspecified time-correlated model error in the (ensemble) {K}alman smoother",
    journal="Quarterly Journal of the Royal Meteorological Society", volume="147", number="734", pages="573--588", year="2021")
add("kalmanbucy1961", "article", author="Kalman, R. E. and Bucy, R. S.", title="New results in linear filtering and prediction theory",
    journal="Journal of Basic Engineering", volume="83", number="1", pages="95--108", year="1961")
add("singh2009", "article", author="Singh, A. and Hespanha, J. P.", title="Optimal feedback strength for noise suppression in autoregulatory gene networks",
    journal="Biophysical Journal", volume="96", number="10", pages="4013--4023", year="2009")
add("boominathan2022", "inproceedings", author="Boominathan, L. and Pitkow, X.", title="Phase transitions in when feedback is useful",
    booktitle="Advances in Neural Information Processing Systems", volume="35", year="2022", eprint="2110.07873", archiveprefix="arXiv")
add("friston2010", "article", author="Friston, K.", title="The free-energy principle: a unified brain theory?",
    journal="Nature Reviews Neuroscience", volume="11", number="2", pages="127--138", year="2010")
# --- novelty search, first set (P)
add("deyst1968", "article", author="Deyst, J. J., Jr. and Price, C. F.", title="Conditions for asymptotic stability of the discrete minimum-variance linear estimator",
    journal="IEEE Transactions on Automatic Control", volume="13", number="6", pages="702--705", year="1968")
add("kurt2025", "misc", ["arXiv identifier 2511.22034"], author="Kurt, B. and Orguner, U.", title="Performance of the {K}alman filter and smoother for benchmark studies", year="2025")
add("kalman1960", "article", ["all fields"], author="Kalman, R. E.", title="A new approach to linear filtering and prediction problems",
    journal="Journal of Basic Engineering", volume="82", number="1", pages="35--45", year="1960")
add("jazwinski1970", "book", ["edition and publisher"], author="Jazwinski, A. H.", title="Stochastic Processes and Filtering Theory", year="1970")
add("andersonmoore1979", "book", ["edition and publisher"], author="Anderson, B. D. O. and Moore, J. B.", title="Optimal Filtering", year="1979")
add("simon2006", "book", ["edition and publisher"], author="Simon, D.", title="Optimal State Estimation", year="2006")
add("blackwell1951", "inproceedings", ["pages (93--102 or 99--102)"], author="Blackwell, D.", title="Comparison of experiments",
    booktitle="Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability", year="1951")
add("blackwell1953", "article", author="Blackwell, D.", title="Equivalent comparisons of experiments", journal="Annals of Mathematical Statistics",
    volume="24", number="2", year="1953", doi="10.1214/aoms/1177729032")
add("brysonjohansen1965", "article", ["title and venue"], author="Bryson, A. E. and Johansen, D. E.", year="1965", doi="10.1109/TAC.1965.1098063")
add("brysonhenrikson1968", "article", ["title"], author="Bryson, A. E. and Henrikson, L. J.", year="1968", doi="10.2514/3.29327")
add("chang2014", "article", ["title"], author="Chang, G.", year="2014", doi="10.1007/s00190-014-0751-7")
add("kalata1984", "article", ["title and DOI"], author="Kalata, P. R.", journal="IEEE Transactions on Aerospace and Electronic Systems", year="1984",
    doi="10.1109/TAES.1984.310438")
add("sahomasugi2016", "article", ["title, volume, DOI"], author="Saho, K. and Masugi, M.", journal="SpringerPlus", year="2016")
add("ernstbanks2002", "article", author="Ernst, M. O. and Banks, M. S.", journal="Nature", volume="415", pages="429--433", year="2002")
add("barshalom2002", "article", ["title and DOI"], author="Bar-Shalom, Y.", journal="IEEE Transactions on Aerospace and Electronic Systems",
    volume="38", number="3", pages="769--778", year="2002")
add("yoder2018", "article", ["authors and DOI"], author="Yoder, others", journal="Sensors", volume="18", number="6", pages="1947", year="2018")
# --- novelty search, second set (P)
add("greenshtein1996", "article", author="Greenshtein, E.", title="Comparison of sequential experiments", journal="Annals of Statistics",
    volume="24", number="1", pages="436--448", year="1996", doi="10.1214/aos/1033066220")
add("yuksellinder2012", "article", ["DOI"], author="Y{\\\"u}ksel, S. and Linder, T.", title="Optimization and convergence of observation channels in stochastic control",
    journal="SIAM Journal on Control and Optimization", volume="50", pages="864--887", year="2012")
add("yukselbasar2013", "book", author="Y{\\\"u}ksel, S. and Ba{\\c{s}}ar, T.", title="Stochastic Networked Control Systems", publisher="Springer",
    year="2013", isbn="978-1-4614-7084-7")
add("yukselbasar2024", "incollection", author="Y{\\\"u}ksel, S. and Ba{\\c{s}}ar, T.", title="Comparison of information structures and their {B}lackwell ordering",
    booktitle="Stochastic Teams, Games, and Control under Information Constraints", publisher="Birkh{\\\"a}user", year="2024",
    doi="10.1007/978-3-031-54071-4_7")
add("hogeboomburr2021", "article", ["title"], author="Hogeboom-Burr, I. and Y{\\\"u}ksel, S.", journal="SIAM Journal on Control and Optimization",
    volume="59", number="3", pages="1781--1803", year="2021", eprint="2005.06673", archiveprefix="arXiv")
add("torgersen1991", "book", author="Torgersen, E. N.", title="Comparison of Statistical Experiments", publisher="Cambridge University Press", year="1991")
add("lecam1964", "article", ["DOI"], author="Le Cam, L.", title="Sufficiency and approximate sufficiency", journal="Annals of Mathematical Statistics",
    volume="35", pages="1419--1455", year="1964")
add("hansentorgersen1974", "article", ["title and DOI"], author="Hansen, O. H. and Torgersen, E. N.", journal="Annals of Statistics", volume="2",
    pages="367--373", year="1974")
add("hotzskelton1987", "article", author="Hotz, A. and Skelton, R. E.", title="Covariance control theory", journal="International Journal of Control",
    volume="46", number="1", pages="13--32", year="1987", doi="10.1080/00207178708933880")
add("hotzskelton1985", "inproceedings", ["DOI"], author="Hotz, A. and Skelton, R. E.", title="A covariance control theory",
    booktitle="Proceedings of the IEEE Conference on Decision and Control", pages="552--557", year="1985")
add("collinsskelton1987", "article", ["DOI"], author="Collins, E. G. and Skelton, R. E.", title="A theory of state covariance assignment for discrete systems",
    journal="IEEE Transactions on Automatic Control", volume="32", number="1", pages="35--41", year="1987")
add("xuskelton1992", "article", author="Xu, J.-H. and Skelton, R. E.", title="An improved covariance assignment theory for discrete systems",
    journal="IEEE Transactions on Automatic Control", volume="37", number="10", pages="1588--1591", year="1992", doi="10.1109/9.256389")
add("yasuda1993", "article", ["title and DOI"], author="Yasuda, K. and Skelton, R. E. and Grigoriadis, K. M.", journal="Automatica", volume="29",
    number="3", pages="785--788", year="1993")
add("skeltonikeda1989", "article", ["title and DOI"], author="Skelton, R. E. and Ikeda, M.", journal="International Journal of Control", volume="49",
    number="5", pages="1773--1785", year="1989")
add("martinezrey2017", "article", author="Mart{\\'\\i}nez-Rey, M. and Espinosa, F. and Gardel, A.",
    title="Analysis of the optimal sampling rate for state estimation in sensor networks with delays", journal="ISA Transactions", volume="68",
    pages="293--301", year="2017", doi="10.1016/j.isatra.2017.03.007")
add("shmaliy2020", "article", ["full author list"], author="Shmaliy, Y. S. and others",
    title="Kalman and {UFIR} state estimation with coloured measurement noise using backward {E}uler method", journal="IET Signal Processing",
    year="2020", doi="10.1049/iet-spr.2019.0166")
add("heeger1992", "article", author="Heeger, D. J.", title="Normalization of cell responses in cat striate cortex", journal="Visual Neuroscience",
    volume="9", number="2", pages="181--197", year="1992", doi="10.1017/S0952523800009640")
add("carandiniheeger2012", "article", author="Carandini, M. and Heeger, D. J.", title="Normalization as a canonical neural computation",
    journal="Nature Reviews Neuroscience", volume="13", number="1", pages="51--62", year="2012", doi="10.1038/nrn3136")
add("cohensteiner2007", "article", author="Cohen-Steiner, D. and Edelsbrunner, H. and Harer, J.", title="Stability of persistence diagrams",
    journal="Discrete and Computational Geometry", volume="37", number="1", pages="103--120", year="2007", doi="10.1007/s00454-006-1276-5")
add("edelsbrunnerharer2010", "book", author="Edelsbrunner, H. and Harer, J.", title="Computational Topology: An Introduction",
    publisher="American Mathematical Society", year="2010", isbn="978-0-8218-4925-5")
add("edelsbrunner2002", "article", author="Edelsbrunner, H. and Letscher, D. and Zomorodian, A.", title="Topological persistence and simplification",
    journal="Discrete and Computational Geometry", volume="28", number="4", pages="511--533", year="2002", doi="10.1007/s00454-002-2885-2")
add("carr2003", "article", author="Carr, H. and Snoeyink, J. and Axen, U.", title="Computing contour trees in all dimensions",
    journal="Computational Geometry", volume="24", number="2", pages="75--94", year="2003", doi="10.1016/S0925-7721(02)00093-7")
add("oudot2015", "book", author="Oudot, S. Y.", title="Persistence Theory: From Quiver Representations to Data Analysis",
    series="Mathematical Surveys and Monographs", volume="209", publisher="American Mathematical Society", year="2015")
add("milnor1963", "book", author="Milnor, J.", title="Morse Theory", series="Annals of Mathematics Studies", volume="51",
    publisher="Princeton University Press", year="1963")

# Verified by web search (filled from t14/bib_check.md; each value has its evidence URL there). key -> {field: value}
SEARCH = {
    "kurt2025": {"eprint": "2511.22034", "archiveprefix": "arXiv"},
    "kalman1960": {"doi": "10.1115/1.3662552"},
    "jazwinski1970": {"isbn": "978-0-12-381550-7"},
    "simon2006": {"publisher": "Wiley", "isbn": "978-0-471-70858-2"},
    "chang2014": {"title": "On {K}alman filter for linear system with colored measurement noise"},
    "kalata1984": {"title": "The tracking index: a generalized parameter for $\\alpha$-$\\beta$ and $\\alpha$-$\\beta$-$\\gamma$ target trackers", "volume": "20"},
    "sahomasugi2016": {"title": "$\\alpha$-$\\beta$-$\\gamma$ tracking filters using acceleration measurements", "doi": "10.1186/s40064-016-1960-8"},
    "barshalom2002": {"title": "Update with out-of-sequence measurements in tracking: exact solution"},
    "yoder2018": {"title": "Exploring the exponentially decaying merit of an out-of-sequence observation", "doi": "10.3390/s18061947"},
    "yuksellinder2012": {"doi": "10.1137/100808976"},
    "lecam1964": {"doi": "10.1214/aoms/1177700372", "number": "4"},
    "hansentorgersen1974": {"title": "Comparison of linear normal experiments", "doi": "10.1214/aos/1176342672", "number": "2"},
    "yasuda1993": {"title": "Covariance controllers: a new parametrization of the class of all stabilizing controllers"},
}
# Fields removed because they could not be confirmed (the prompt flagged them, or search evidence contradicts them).
DROP = {"kalman1960": ["journal", "volume", "number", "pages"], "barshalom2002": ["pages"]}
# VERIFY items replaced after the search. key -> new list of VERIFY items (before the automatic DOI/title items)
REVERIFY = {
    "kurt2025": [],
    "kalman1960": ["journal, volume, issue and pages (J. Basic Eng. 82(1), 35-45 per the prompt; seen only in search summaries)"],
    "jazwinski1970": ["publisher (Academic Press per catalog summaries; ISBN confirmed via the Elsevier listing) and edition"],
    "simon2006": ["edition"],
    "blackwell1951": ["pages (search evidence points to 93-102, not 99-102, but only through summaries)"],
    "chang2014": ["journal, volume and pages (Journal of Geodesy 88, 1163-1170 per one catalog summary)"],
    "kalata1984": ["number and pages (174-182 in one index, 174-181 in a reference list)", "DOI (10.1109/TAES.1984.310438 given in the prompt; not confirmed)"],
    "sahomasugi2016": ["volume and article number (5, 309 per a search summary)"],
    "barshalom2002": ["pages (prompt 769-778; the IEEE record as quoted in a search summary gives 769-777)", "DOI (probably 10.1109/TAES.2002.1039398; not confirmed)"],
    "yoder2018": ["full author list"],
    "yuksellinder2012": ["issue (2, per a search summary)"],
    "lecam1964": [],
    "hansentorgersen1974": [],
    "yasuda1993": ["DOI"],
    "skeltonikeda1989": ["title and DOI (nothing confirmed by search, including the author pairing and the volume/pages)"],
    "hotzskelton1985": ["DOI (10.1109/CDC.1985.268547 per a search summary; not confirmed)"],
    "collinsskelton1987": ["DOI (not found)"],
    "heffes1966": ["DOI not captured (10.1109/TAC.1966.1098392 appears only in a search summary)"],
    "brysonjohansen1965": ["title, venue, volume and pages (a search summary gives 'Linear filtering for time-varying systems using measurements containing colored noise', IEEE TAC 10(1), 4-10; not confirmed)"],
    "brysonhenrikson1968": ["title and venue (a search summary gives 'Estimation using sampled data containing sequentially correlated noise', J. Spacecraft and Rockets 5(6), 662-665; not confirmed)"],
    "hogeboomburr2021": ["title and DOI (not confirmed by search)"],
    "shmaliy2020": ["full author list, volume and pages (Shmaliy, Zhao and Ahn, 14(2), 64-71 per a search summary)"],
}


def main():
    out = ["% Bibliography for the thesis (Task 14). Field sources and every VERIFY flag: classification/t14/bib_check.md.",
           "% Never add a DOI, page range or author that has not been verified.", ""]
    for key, typ, f, ver in E:
        f = dict(f)
        if key == "kalata1984":
            f.pop("doi", None)          # flagged in the prompt and not confirmed
        f.update(SEARCH.get(key, {}))
        for d in DROP.get(key, []):
            f.pop(d, None)
        if key in REVERIFY:
            ver = list(REVERIFY[key])
        if "title" not in f and not any("title" in v for v in ver):
            ver.insert(0, "title")
        if f.get("doi"):
            ver.append(NODOI)
        if f.get("author", "").endswith("others") and "authors" not in " ".join(ver):
            ver.append("full author list")
        if ver:
            f["note"] = "VERIFY: " + "; ".join(ver)
        out.append(f"@{typ}{{{key},")
        out += [f"  {k} = {{{v}}}," for k, v in f.items()]
        out[-1] = out[-1].rstrip(",")
        out += ["}", ""]
    open(os.path.join(CLS, "references.bib"), "w").write("\n".join(out))
    print(len(E), "entries;", sum(1 for x in out if "VERIFY" in x), "with VERIFY")


if __name__ == "__main__":
    main()
