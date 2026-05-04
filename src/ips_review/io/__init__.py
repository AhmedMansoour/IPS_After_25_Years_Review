"""Database loaders. Each returns a DataFrame with a `Source` column added.

Loaders are intentionally simple: they only READ files. All column
harmonization is delegated to ips_review.harmonize.
"""
from .scopus import load_scopus
from .wos import load_wos
from .ieee import load_ieee

__all__ = ["load_scopus", "load_wos", "load_ieee"]
