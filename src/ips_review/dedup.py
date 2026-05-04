"""Stage 2: cross-database deduplication via union-find on title and DOI."""
from __future__ import annotations

import logging
from collections import defaultdict

import pandas as pd

from .utils.text import normalize_doi, normalize_title

log = logging.getLogger(__name__)

SOURCE_PRIORITY = {"Scopus": 0, "WoS": 1, "IEEE": 2}


class _UnionFind:
    __slots__ = ("parent",)

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        p = self.parent
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def deduplicate(records: pd.DataFrame) -> pd.DataFrame:
    """Collapse duplicate records across Scopus / WoS / IEEE.

    Two records are considered duplicates if they share a normalized title
    or a normalized DOI. Representative selection prefers Scopus > WoS > IEEE.
    Adds two columns to the output:
        Also_In         — semicolon-separated list of other sources containing the record
        Duplicate_Count — number of distinct sources in the cluster
    """
    df = records.copy().reset_index(drop=True)
    df["_ntitle"] = df["Title"].apply(normalize_title)
    df["_ndoi"] = df["DOI"].apply(normalize_doi)

    uf = _UnionFind(len(df))

    title_idx: dict[str, list[int]] = {}
    for i, t in enumerate(df["_ntitle"]):
        if t:
            title_idx.setdefault(t, []).append(i)
    for members in title_idx.values():
        for j in members[1:]:
            uf.union(members[0], j)

    doi_idx: dict[str, list[int]] = {}
    for i, d in enumerate(df["_ndoi"]):
        if d:
            doi_idx.setdefault(d, []).append(i)
    for members in doi_idx.values():
        for j in members[1:]:
            uf.union(members[0], j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(df)):
        groups[uf.find(i)].append(i)

    rows = []
    for members in groups.values():
        members.sort(key=lambda i: SOURCE_PRIORITY.get(df.at[i, "Source"], 9))
        rep = members[0]
        sources = {df.at[m, "Source"] for m in members}
        rep_source = df.at[rep, "Source"]
        row = df.iloc[rep].copy()
        row["Also_In"] = ";".join(sorted(sources - {rep_source}))
        row["Duplicate_Count"] = len(sources)
        rows.append(row)

    out = pd.DataFrame(rows).drop(columns=["_ntitle", "_ndoi"]).reset_index(drop=True)
    log.info(
        "Deduplicated %d harmonized records -> %d unique records",
        len(df),
        len(out),
    )
    return out
