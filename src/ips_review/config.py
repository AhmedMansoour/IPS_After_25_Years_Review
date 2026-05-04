"""Configuration loading: coding dictionary + source mapping + pipeline config."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class SafeguardCategory:
    name: str
    rationale: str
    exclude: re.Pattern
    safeguard: re.Pattern


@dataclass
class Era:
    name: str
    label: str
    year_min: int | None
    year_max: int | None
    theme_pattern: re.Pattern


@dataclass
class Dictionary:
    """In-memory representation of the YAML coding dictionary."""

    version: str
    released: str
    case_sensitive: bool
    non_scholarly_document_types: set[str]
    safeguard_categories: list[SafeguardCategory]
    i_core: re.Pattern
    i_context: re.Pattern
    sensing_sources: dict[str, re.Pattern]
    paradigms: dict[str, re.Pattern]
    deployment_indicators: dict[str, re.Pattern]
    eras: list[Era]
    priority_tiers: dict[str, Any]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


def _compile(pattern: str, case_sensitive: bool) -> re.Pattern:
    flags = 0 if case_sensitive else re.IGNORECASE
    # Multiline patterns in YAML may contain newlines; collapse them.
    cleaned = re.sub(r"\s*\n\s*", "", pattern)
    return re.compile(cleaned, flags)


def load_dictionary(path: str | Path) -> Dictionary:
    """Load and compile the YAML coding dictionary."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    cs = bool(raw.get("case_sensitive", False))

    safeguards = [
        SafeguardCategory(
            name=k,
            rationale=v.get("rationale", ""),
            exclude=_compile(v["exclude"], cs),
            safeguard=_compile(v["safeguard"], cs),
        )
        for k, v in raw.get("safeguard_categories", {}).items()
    ]

    i_core_alt = "|".join(f"(?:{p})" for p in raw["i_core_patterns"])
    i_context_alt = "|".join(f"(?:{p})" for p in raw["i_context_patterns"])

    eras = [
        Era(
            name=k,
            label=v.get("label", k),
            year_min=v.get("year_min"),
            year_max=v.get("year_max"),
            theme_pattern=_compile(v["theme_pattern"], cs),
        )
        for k, v in raw.get("eras", {}).items()
    ]

    return Dictionary(
        version=str(raw["version"]),
        released=str(raw.get("released", "")),
        case_sensitive=cs,
        non_scholarly_document_types=set(raw.get("non_scholarly_document_types", [])),
        safeguard_categories=safeguards,
        i_core=_compile(i_core_alt, cs),
        i_context=_compile(i_context_alt, cs),
        sensing_sources={k: _compile(v, cs) for k, v in raw.get("sensing_sources", {}).items()},
        paradigms={k: _compile(v, cs) for k, v in raw.get("paradigms", {}).items()},
        deployment_indicators={
            k: _compile(v, cs) for k, v in raw.get("deployment_indicators", {}).items()
        },
        eras=eras,
        priority_tiers=raw.get("priority_tiers", {}),
        raw=raw,
    )


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Generic YAML loader for source_mapping.yaml and pipeline.yaml."""
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
