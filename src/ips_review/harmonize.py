"""Stage 1: harmonize Scopus / WoS / IEEE into a unified schema.

The mapping is driven by config/source_mapping.yaml so that schema changes
upstream (e.g., Scopus renaming a column) require no code edits.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from .config import load_yaml
from .io import load_ieee, load_scopus, load_wos

log = logging.getLogger(__name__)


def _safe_get(df: pd.DataFrame, col: str | None) -> pd.Series:
    if col and col in df.columns:
        return df[col].fillna("").astype(str)
    return pd.Series([""] * len(df), index=df.index, dtype=str)


def _harmonize_one(df: pd.DataFrame, mapping: dict[str, Any], source: str) -> pd.DataFrame:
    cols = mapping["columns"]
    out = pd.DataFrame()
    out["Source"] = df["Source"]
    out["Title"] = _safe_get(df, cols.get("Title"))
    out["Authors"] = _safe_get(df, cols.get("Authors"))
    out["Year"] = _safe_get(df, cols.get("Year"))
    out["DOI"] = _safe_get(df, cols.get("DOI"))
    out["Abstract"] = _safe_get(df, cols.get("Abstract"))
    out["Document_Type"] = _safe_get(df, cols.get("Document_Type"))
    out["Source_Title"] = _safe_get(df, cols.get("Source_Title"))

    ak = _safe_get(df, cols.get("Author_Keywords"))
    fb = cols.get("Author_Keywords_fallback")
    if fb:
        ak = ak.where(ak != "", _safe_get(df, fb))
    out["Author_Keywords"] = ak

    out["Cited_By"] = _safe_get(df, cols.get("Cited_By"))
    out["EID"] = _safe_get(df, cols.get("EID"))
    out["Affiliations"] = _safe_get(df, cols.get("Affiliations"))

    link_col = cols.get("Link")
    if link_col is None and source == "wos":
        # Construct from DOI for WoS
        doi = _safe_get(df, cols.get("DOI"))
        out["Link"] = doi.apply(lambda d: f"https://doi.org/{d}" if d else "")
    else:
        out["Link"] = _safe_get(df, link_col)
    return out


def harmonize(
    *,
    scopus_dir: str | Path | None = None,
    wos_dir: str | Path | None = None,
    ieee_dir: str | Path | None = None,
    mapping_path: str | Path = "config/source_mapping.yaml",
) -> pd.DataFrame:
    """Load all three sources, harmonize, concatenate.

    Any source directory can be ``None`` to skip that source.
    """
    mapping = load_yaml(mapping_path)
    frames: list[pd.DataFrame] = []

    if scopus_dir is not None:
        s = load_scopus(scopus_dir, glob=mapping["scopus"]["glob"])
        frames.append(_harmonize_one(s, mapping["scopus"], "scopus"))

    if wos_dir is not None:
        w = load_wos(wos_dir, glob=mapping["wos"]["glob"])
        frames.append(_harmonize_one(w, mapping["wos"], "wos"))

    if ieee_dir is not None:
        i = load_ieee(ieee_dir, glob=mapping["ieee"]["glob"])
        frames.append(_harmonize_one(i, mapping["ieee"], "ieee"))

    if not frames:
        raise ValueError("At least one of scopus_dir / wos_dir / ieee_dir must be provided")

    out = pd.concat(frames, ignore_index=True).fillna("")
    log.info("Harmonized: %d records (Scopus+WoS+IEEE concatenated)", len(out))
    return out
