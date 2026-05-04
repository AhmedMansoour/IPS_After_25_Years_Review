"""Provenance metadata: stamped onto every output CSV header."""
from __future__ import annotations

import datetime as _dt
import hashlib
import platform
import subprocess
from pathlib import Path

from .. import __version__


def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def provenance_header(
    *,
    stage: str,
    dictionary_version: str | None = None,
    inputs: dict[str, str | Path] | None = None,
) -> str:
    """Return a multi-line `#`-prefixed header for prepending to CSV outputs."""
    lines = [
        f"# ips_review pipeline output",
        f"# stage: {stage}",
        f"# package_version: {__version__}",
        f"# git_sha: {git_sha()}",
        f"# python: {platform.python_version()}  platform: {platform.platform()}",
        f"# generated_utc: {_dt.datetime.utcnow().isoformat(timespec='seconds')}Z",
    ]
    if dictionary_version:
        lines.append(f"# dictionary_version: {dictionary_version}")
    if inputs:
        for label, p in inputs.items():
            try:
                sha = file_sha256(p)[:16]
            except OSError:
                sha = "missing"
            lines.append(f"# input.{label}: {p}  sha256={sha}")
    return "\n".join(lines) + "\n"
