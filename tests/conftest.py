"""Shared pytest fixtures."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from ips_review.config import load_dictionary


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def dictionary():
    return load_dictionary(REPO_ROOT / "config" / "coding_dictionary.v1.0.yaml")


@pytest.fixture
def golden_papers() -> pd.DataFrame:
    return pd.read_csv(FIXTURES / "golden_papers.csv", dtype=str).fillna("")


@pytest.fixture
def dedup_cases() -> pd.DataFrame:
    return pd.read_csv(FIXTURES / "dedup_cases.csv", dtype=str).fillna("")
