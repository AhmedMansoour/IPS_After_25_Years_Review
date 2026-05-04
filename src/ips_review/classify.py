"""Stage 5: section-level multi-label mapping.

Each retained record (I-Core or I-Context) is assigned:
    Sec_III_Era                 — Era1 / Era2 / Era3 / Era4 (year-based)
    Sec_IV_Sensing_<modality>   — boolean per modality
    Sec_IV_Paradigm_<paradigm>  — boolean per paradigm
    Sec_VI_Deploy_<indicator>   — boolean per deployment indicator

A record can carry multiple sensing / paradigm / deployment labels.
"""
from __future__ import annotations

import logging

import pandas as pd

from .config import Dictionary
from .utils.text import build_search_text

log = logging.getLogger(__name__)


def classify(records: pd.DataFrame, dictionary: Dictionary) -> pd.DataFrame:
    df = records.copy().reset_index(drop=True)
    df["_text"] = build_search_text(df)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    retained = df["Screen_Label"].isin(["I-Core", "I-Context"])

    # ── Section III: Era (year-based, on retained only) ──────────────────────
    df["Sec_III_Era"] = ""
    for era in dictionary.eras:
        mask = retained & df["Year"].notna()
        if era.year_min is not None:
            mask &= df["Year"] > era.year_min
        if era.year_max is not None:
            mask &= df["Year"] <= era.year_max
        df.loc[mask, "Sec_III_Era"] = era.name
        log.info("Era %s (%s): %d", era.name, era.label, int(mask.sum()))

    # ── Section IV.1: sensing source (multi-label) ───────────────────────────
    for label, pattern in dictionary.sensing_sources.items():
        col = f"Sec_IV_Sensing_{label}"
        df[col] = retained & df["_text"].apply(lambda x, p=pattern: bool(p.search(x)))

    # ── Section IV.2: paradigm (multi-label) ─────────────────────────────────
    for label, pattern in dictionary.paradigms.items():
        col = f"Sec_IV_Paradigm_{label}"
        df[col] = retained & df["_text"].apply(lambda x, p=pattern: bool(p.search(x)))

    # ── Section VI.x: deployment indicators (multi-label) ────────────────────
    for label, pattern in dictionary.deployment_indicators.items():
        col = f"Sec_VI_Deploy_{label}"
        df[col] = retained & df["_text"].apply(lambda x, p=pattern: bool(p.search(x)))

    return df.drop(columns=["_text"])
