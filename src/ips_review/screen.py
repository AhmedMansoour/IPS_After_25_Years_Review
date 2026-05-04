"""Stage 3: rule-based three-tier screening.

Every record is assigned:
    Screen_Label    : I-Core | I-Context | E-Exclude
    Exclude_Reason  : non-scholarly | out-of-scope:<cat> | no-IPS-relevance | ""
    Priority_Tier   : T1 | T2 | T3 | ""

The screening is fully deterministic given (records, dictionary).
"""
from __future__ import annotations

import logging
import re

import pandas as pd

from .config import Dictionary
from .utils.text import build_search_text

log = logging.getLogger(__name__)


def _apply_priority_tiers(df: pd.DataFrame, dictionary: Dictionary) -> pd.DataFrame:
    inc = df["Screen_Label"].isin(["I-Core", "I-Context"])
    cited = pd.to_numeric(df["Cited_By"], errors="coerce").fillna(0).astype(int)

    pt = dictionary.priority_tiers
    t1_kw = re.compile(pt["t1"]["keyword_pattern"], re.IGNORECASE)
    t1_thr = int(pt["t1"]["citation_threshold"])
    t1_doc_inc = set(pt["t1"].get("document_types", []))
    t1_doc_exc = set(pt["t1"].get("document_types_exclude", []))
    t2_thr = int(pt["t2"]["citation_threshold"])
    t2_doc_inc = set(pt["t2"].get("document_types", []))

    is_review = df["Document_Type"].apply(
        lambda d: any(s in str(d) for s in t1_doc_inc)
        and not any(s in str(d) for s in t1_doc_exc)
    )
    is_t1_kw = df["_text"].apply(lambda t: bool(t1_kw.search(t)))
    t1 = inc & (is_review | (cited >= t1_thr) | is_t1_kw)

    is_t2_doc = df["Document_Type"].isin(t2_doc_inc)
    t2 = inc & ~t1 & ((cited >= t2_thr) | is_t2_doc)
    t3 = inc & ~t1 & ~t2

    df["Priority_Tier"] = ""
    df.loc[t1, "Priority_Tier"] = "T1"
    df.loc[t2, "Priority_Tier"] = "T2"
    df.loc[t3, "Priority_Tier"] = "T3"
    return df


def screen(records: pd.DataFrame, dictionary: Dictionary) -> pd.DataFrame:
    """Apply the three-tier screening pipeline.

    Steps:
      1. E-Exclude non-scholarly document types.
      2. E-Exclude 7 out-of-scope categories with safeguards.
      3. Label residue I-Core via strong direct-IPS regex.
      4. Label residue I-Context via IPS-enabling regex.
      5. E-Exclude remaining as no-IPS-relevance.
      6. Assign Priority_Tier (T1/T2/T3) over retained records.
    """
    df = records.copy().reset_index(drop=True)
    df["_text"] = build_search_text(df)
    df["Screen_Label"] = ""
    df["Exclude_Reason"] = ""

    # Step 1
    ns = df["Document_Type"].isin(dictionary.non_scholarly_document_types)
    df.loc[ns, ["Screen_Label", "Exclude_Reason"]] = ["E-Exclude", "non-scholarly"]
    log.info("Step 1 — non-scholarly excluded: %d", int(ns.sum()))

    # Step 2
    for cat in dictionary.safeguard_categories:
        pool = df.index[df["Screen_Label"] == ""]
        t = df.loc[pool, "_text"]
        excl = t.apply(lambda x, p=cat.exclude: bool(p.search(x))) & ~t.apply(
            lambda x, p=cat.safeguard: bool(p.search(x))
        )
        idx = t[excl].index
        df.loc[idx, ["Screen_Label", "Exclude_Reason"]] = [
            "E-Exclude",
            f"out-of-scope: {cat.name}",
        ]
        log.info("Step 2 — %s excluded: %d", cat.name, len(idx))

    # Step 3 — I-Core
    pool = df.index[df["Screen_Label"] == ""]
    t = df.loc[pool, "_text"]
    is_core = t.apply(lambda x: bool(dictionary.i_core.search(x)))
    df.loc[t[is_core].index, "Screen_Label"] = "I-Core"
    log.info("Step 3 — I-Core: %d", int((df["Screen_Label"] == "I-Core").sum()))

    # Step 4 — I-Context
    pool = df.index[df["Screen_Label"] == ""]
    t = df.loc[pool, "_text"]
    is_ctx = t.apply(lambda x: bool(dictionary.i_context.search(x)))
    df.loc[t[is_ctx].index, "Screen_Label"] = "I-Context"
    log.info("Step 4 — I-Context: %d", int((df["Screen_Label"] == "I-Context").sum()))

    # Step 5
    rest = df["Screen_Label"] == ""
    df.loc[rest, ["Screen_Label", "Exclude_Reason"]] = ["E-Exclude", "no-IPS-relevance"]
    log.info("Step 5 — no-IPS-relevance: %d", int(rest.sum()))

    # Step 6
    df = _apply_priority_tiers(df, dictionary)
    log.info(
        "Step 6 — tiers  T1=%d  T2=%d  T3=%d",
        int((df["Priority_Tier"] == "T1").sum()),
        int((df["Priority_Tier"] == "T2").sum()),
        int((df["Priority_Tier"] == "T3").sum()),
    )

    return df.drop(columns=["_text"])
