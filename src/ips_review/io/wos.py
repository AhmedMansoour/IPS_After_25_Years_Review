"""Web of Science loader.

WoS exports are typically legacy `.xls` (BIFF) files; we read them with
xlrd. Newer `.xlsx` exports are also supported via openpyxl.
"""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import xlrd

log = logging.getLogger(__name__)


def _read_xls(path: Path) -> pd.DataFrame:
    wb = xlrd.open_workbook(str(path))
    ws = wb.sheet_by_index(0)
    headers = [ws.cell_value(0, c) for c in range(ws.ncols)]
    rows = []
    for r in range(1, ws.nrows):
        row = []
        for c in range(ws.ncols):
            cell = ws.cell(r, c)
            if cell.ctype == xlrd.XL_CELL_NUMBER:
                v = int(cell.value) if cell.value == int(cell.value) else cell.value
                row.append(str(v))
            elif cell.ctype == xlrd.XL_CELL_EMPTY:
                row.append("")
            else:
                row.append(str(cell.value))
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)


def load_wos(directory: str | Path, glob: str = "savedrecs*.xls") -> pd.DataFrame:
    directory = Path(directory)
    files = sorted(directory.glob(glob)) + sorted(directory.glob("savedrecs*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No WoS files matching {glob} under {directory}")
    log.info("Loading %d WoS file(s) from %s", len(files), directory)
    frames = []
    for f in files:
        if f.suffix.lower() == ".xls":
            df = _read_xls(f)
        else:
            df = pd.read_excel(f, dtype=str, engine="openpyxl")
        log.debug("  %s: %d rows", f.name, len(df))
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["Source"] = "WoS"
    log.info("  WoS total: %d records", len(df))
    return df
