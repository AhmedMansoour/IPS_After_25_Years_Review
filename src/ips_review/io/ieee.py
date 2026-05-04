"""IEEE Xplore CSV loader.

Document type is inferred from filename prefix: files starting with `conf`
are tagged as Conference; everything else is Non-Conference (journal /
early-access / magazine).
"""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def load_ieee(
    directory: str | Path,
    glob: str = "*.csv",
    conf_prefix: str = "conf",
) -> pd.DataFrame:
    directory = Path(directory)
    files = sorted(directory.glob(glob))
    if not files:
        raise FileNotFoundError(f"No IEEE files matching {glob} under {directory}")
    log.info("Loading %d IEEE file(s) from %s", len(files), directory)
    frames = []
    for f in files:
        df = pd.read_csv(f, dtype=str)
        df["_IEEE_DocType"] = "Conference" if f.stem.startswith(conf_prefix) else "Non-Conference"
        log.debug("  %s: %d rows", f.name, len(df))
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["Source"] = "IEEE"
    log.info("  IEEE total: %d records", len(df))
    return df
