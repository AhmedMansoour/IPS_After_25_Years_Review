"""Stratified sampling for the validation panel."""
from __future__ import annotations

import logging
from typing import Sequence

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def stratified_sample(
    df: pd.DataFrame,
    *,
    n: int,
    strata: Sequence[str],
    seed: int = 20260505,
    min_per_stratum: int = 5,
) -> pd.DataFrame:
    """Draw a stratified random sample over the cross-product of `strata` columns.

    Returns a subset of ``df`` with ~``n`` rows. Each stratum receives a
    proportional share but no fewer than ``min_per_stratum`` rows where
    the stratum has enough records.

    The returned DataFrame is shuffled and includes a `_stratum` column for audit.
    """
    rng = np.random.default_rng(seed)
    work = df.copy()
    work["_stratum"] = work[list(strata)].astype(str).agg("|".join, axis=1)

    sizes = work.groupby("_stratum").size()
    total = sizes.sum()
    target = (sizes / total * n).round().astype(int)
    target = target.clip(lower=min_per_stratum).where(sizes >= min_per_stratum, sizes)

    parts: list[pd.DataFrame] = []
    for stratum, take in target.items():
        pool = work[work["_stratum"] == stratum]
        take = int(min(take, len(pool)))
        if take <= 0:
            continue
        idx = rng.choice(pool.index.values, size=take, replace=False)
        parts.append(pool.loc[idx])

    sample = pd.concat(parts, ignore_index=False)
    sample = sample.sample(frac=1.0, random_state=int(rng.integers(0, 2**31 - 1)))
    sample = sample.reset_index(drop=True)
    log.info(
        "Drew stratified sample: %d rows across %d strata (target %d)",
        len(sample),
        len(target),
        n,
    )
    return sample
