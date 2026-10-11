"""Shared paths and helpers for Task 14."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.path.dirname(HERE)
REPO = os.path.dirname(CLS)
RES = os.path.join(HERE, "results")
PREREG = "e5edebf"
LEGACY = re.compile(r"\b(Prop\.|Proposition|Thm|Theorem|Lemma|Cor\.|Corollary|Conj\.|Conjecture|Num\.|Numerical result|"
                    r"Counterexample|Def\.|Definition)\s*\d+(\.\d+)?[a-z′']?\b")
AE = re.compile(r"\b[A-E]\.\d+\b")


def save_json(obj, name):
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, name), "w") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False, default=str)
