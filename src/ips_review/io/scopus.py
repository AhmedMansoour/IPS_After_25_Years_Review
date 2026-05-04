"""Scopus CSV loader."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def load_scopus(directory: str | Path, glob: str = "scopus_*.csv") -> pd.DataFrame:
    directory = Path(directory)
    files = sorted(directory.glob(glob))
    if not files:
        raise FileNotFoundError(f"No Scopus files matching {glob} under {directory}")
    log.info("Loading %d Scopus file(s) from %s", len(files), directory)
    parts = [pd.read_csv(f, dtype=str) for f in files]
    df = pd.concat(parts, ignore_index=True)
    if "EID" in df.columns:
        df = df.drop_duplicates(subset="EID", keep="first").reset_index(drop=True)
    if "Source" in df.columns:
        df = df.rename(columns={"Source": "Scopus_Source_Col"})
    df["Source"] = "Scopus"
    log.info("  Scopus loaded: %d records (post EID dedup)", len(df))
    return df
