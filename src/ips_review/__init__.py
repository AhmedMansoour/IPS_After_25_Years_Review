"""
ips_review
==========

Reproducibility package for the 25-Years IPS Systematic Review.

The pipeline is deterministic: every label produced for the corpus is the
output of regular expressions defined in the YAML coding dictionary applied
to (Title + Abstract + Author_Keywords). No record-level LLM inference
is performed.

Public API:
    load_dictionary(path)   -> Dictionary
    harmonize(...)          -> pd.DataFrame
    deduplicate(df)         -> pd.DataFrame
    screen(df, dictionary)  -> pd.DataFrame
    classify(df, dictionary)-> pd.DataFrame
    validate(rb, hc)        -> ValidationReport
    stratified_sample(df,...) -> pd.DataFrame
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ips-review")
except PackageNotFoundError:  # editable install w/o metadata
    __version__ = "1.0.0"

from .config import Dictionary, load_dictionary
from .dedup import deduplicate
from .harmonize import harmonize
from .screen import screen
from .classify import classify
from .sampling import stratified_sample
from .validate import ValidationReport, validate

__all__ = [
    "__version__",
    "Dictionary",
    "load_dictionary",
    "harmonize",
    "deduplicate",
    "screen",
    "classify",
    "stratified_sample",
    "validate",
    "ValidationReport",
]
