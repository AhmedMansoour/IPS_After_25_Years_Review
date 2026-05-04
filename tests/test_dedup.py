"""Test cross-database deduplication."""
from __future__ import annotations

from ips_review.dedup import deduplicate


def test_dedup_collapses_title_and_doi_matches(dedup_cases):
    out = deduplicate(dedup_cases)
    # 6 input rows -> 3 unique groups (g1, g2, g3)
    assert len(out) == 3
    counts = out["Duplicate_Count"].astype(int).sort_values().tolist()
    # group sizes: g3 has 1, g2 has 2, g1 has 3 -> Duplicate_Count = distinct sources per group
    assert counts == [1, 2, 3]


def test_dedup_prefers_scopus_representative(dedup_cases):
    out = deduplicate(dedup_cases)
    # Group g1 has Scopus, WoS, IEEE — representative must be Scopus
    g1 = out[out["DOI"] == "10.1000/abc"]
    assert len(g1) == 1
    assert g1.iloc[0]["Source"] == "Scopus"
    also_in = set(g1.iloc[0]["Also_In"].split(";"))
    assert {"WoS", "IEEE"}.issubset(also_in)


def test_dedup_handles_missing_doi(dedup_cases):
    """g2 has one row with empty DOI; title-based merge should still link them."""
    out = deduplicate(dedup_cases)
    g2 = out[out["Title"].str.lower().str.contains("ble asset tracking")]
    assert len(g2) == 1
    assert int(g2.iloc[0]["Duplicate_Count"]) == 2
