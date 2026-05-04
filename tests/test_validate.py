"""Test the Cohen's kappa validation utility."""
from __future__ import annotations

import pandas as pd

from ips_review.validate import validate


def test_perfect_agreement():
    rb = pd.DataFrame({"DOI": ["a", "b", "c"], "Screen_Label": ["I-Core", "I-Context", "E-Exclude"]})
    hc = pd.DataFrame({"DOI": ["a", "b", "c"], "Human_Label": ["I-Core", "I-Context", "E-Exclude"]})
    rep = validate(rb, hc)
    assert rep.cohen_kappa == 1.0
    assert rep.percent_agreement == 1.0
    assert rep.disagreements.empty


def test_partial_agreement():
    rb = pd.DataFrame({
        "DOI":          ["a", "b", "c", "d"],
        "Screen_Label": ["I-Core", "I-Context", "E-Exclude", "I-Core"],
    })
    hc = pd.DataFrame({
        "DOI":         ["a", "b", "c", "d"],
        "Human_Label": ["I-Core", "I-Context", "E-Exclude", "I-Context"],
    })
    rep = validate(rb, hc)
    assert rep.n == 4
    assert rep.percent_agreement == 0.75
    assert len(rep.disagreements) == 1


def test_kappa_is_zero_for_random():
    rb = pd.DataFrame({"DOI": list("abcd"), "Screen_Label": ["I-Core"] * 4})
    hc = pd.DataFrame({"DOI": list("abcd"), "Human_Label": ["I-Core"] * 4})
    rep = validate(rb, hc)
    # Constant predictions vs constant truth gives nan kappa per sklearn convention,
    # but percent_agreement should be 1.0
    assert rep.percent_agreement == 1.0
