"""Test the rule-based screening against the golden-papers fixture."""
from __future__ import annotations

import pandas as pd

from ips_review.screen import screen


def test_dictionary_loads(dictionary):
    assert dictionary.version == "1.0"
    assert dictionary.i_core is not None
    assert dictionary.i_context is not None
    assert len(dictionary.safeguard_categories) == 7
    assert len(dictionary.eras) == 4


def test_golden_papers_label(dictionary, golden_papers):
    """Every hand-labeled paper should be classified correctly by the rules."""
    out = screen(golden_papers, dictionary)
    mismatches = []
    for _, r in golden_papers.iterrows():
        actual = out.loc[out["DOI"] == r["DOI"], "Screen_Label"].iloc[0]
        if actual != r["expected_label"]:
            mismatches.append(
                (r["DOI"], r["Title"][:40], r["expected_label"], actual, r["note"])
            )
    if mismatches:
        msg = "\n".join(
            f"  {d}: '{t}' expected={e} got={a}  ({n})"
            for d, t, e, a, n in mismatches
        )
        raise AssertionError(f"{len(mismatches)} golden papers misclassified:\n{msg}")


def test_safeguard_rescues_indoor_uwb(dictionary):
    df = pd.DataFrame(
        [
            {
                "Title": "UWB ranging in robotics SLAM",
                "Abstract": "We use UWB ranging for indoor positioning.",
                "Author_Keywords": "uwb;slam;indoor",
                "Document_Type": "Article",
                "Year": "2022",
                "Cited_By": "5",
                "DOI": "10.x/1",
            }
        ]
    )
    out = screen(df, dictionary)
    assert out.iloc[0]["Screen_Label"] == "I-Core"


def test_non_scholarly_excluded(dictionary):
    df = pd.DataFrame(
        [
            {
                "Title": "WiFi indoor positioning",
                "Abstract": "...",
                "Author_Keywords": "indoor positioning",
                "Document_Type": "Editorial",
                "Year": "2021",
                "Cited_By": "0",
                "DOI": "10.x/2",
            }
        ]
    )
    out = screen(df, dictionary)
    assert out.iloc[0]["Screen_Label"] == "E-Exclude"
    assert out.iloc[0]["Exclude_Reason"] == "non-scholarly"


def test_priority_tier_review_paper(dictionary):
    df = pd.DataFrame(
        [
            {
                "Title": "A survey of indoor positioning",
                "Abstract": "Comprehensive survey.",
                "Author_Keywords": "indoor positioning;survey",
                "Document_Type": "Review",
                "Year": "2020",
                "Cited_By": "150",
                "DOI": "10.x/3",
            }
        ]
    )
    out = screen(df, dictionary)
    assert out.iloc[0]["Priority_Tier"] == "T1"


def test_screening_is_deterministic(dictionary, golden_papers):
    """Running screen twice on the same input yields identical labels."""
    a = screen(golden_papers, dictionary)
    b = screen(golden_papers, dictionary)
    pd.testing.assert_series_equal(a["Screen_Label"], b["Screen_Label"])
    pd.testing.assert_series_equal(a["Priority_Tier"], b["Priority_Tier"])
