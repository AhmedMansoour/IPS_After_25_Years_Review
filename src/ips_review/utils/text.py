"""Lowercased text normalization shared across screen / classify / validate."""
from __future__ import annotations

import string
import re
import pandas as pd

_PUNCT = str.maketrans("", "", string.punctuation)


def build_search_text(df: pd.DataFrame) -> pd.Series:
    """Concatenate Title + Abstract + Author_Keywords, lowercased.

    All regex screening operates on this single field.
    """
    return (
        df["Title"].fillna("").astype(str).str.lower()
        + " "
        + df["Abstract"].fillna("").astype(str).str.lower()
        + " "
        + df["Author_Keywords"].fillna("").astype(str).str.lower()
    )


def normalize_title(t: str) -> str:
    if not isinstance(t, str) or not t.strip():
        return ""
    s = t.lower().strip().translate(_PUNCT)
    return re.sub(r"\s+", " ", s).strip()


def normalize_doi(d: str) -> str:
    if not isinstance(d, str) or not d.strip():
        return ""
    s = re.sub(r"^https?://doi\.org/", "", d.lower().strip())
    return s.strip()
