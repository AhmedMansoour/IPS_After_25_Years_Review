"""Fail-closed, standard-library verification for the Indoor Spatial Intelligence review.

Manifest: validates manuscript-derived expected values and Appendix index only.
Empirical: also validates presence and internal consistency of actual research records.
No mode verifies correctness of full-text scientific judgments without source inspection.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = {"demonstrated", "partial", "assumed", "not_evaluated", "not_reported"}
DIMENSIONS = [
    "grounding_status", "representation_status", "reasoning_status",
    "uncertainty_status", "provenance_status", "action_verification_status",
    "update_status",
]


def rows(path: Path, required: set[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"Missing required source file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"Required columns missing in {path}: {sorted(required)}")
        return list(reader)


def expected_data() -> tuple[dict, dict, list]:
    expected = json.loads((ROOT / "data/expected_results.json").read_text(encoding="utf-8"))
    frontier = json.loads((ROOT / "data/frontier_summary.json").read_text(encoding="utf-8"))
    index = rows(ROOT / "data/fulltext_31_index.csv",
                 {"study_id", "reference_number", "year", "source_table"})
    return expected, frontier, index


def manifest() -> tuple[dict, dict, list]:
    expected, frontier, index = expected_data()
    m = expected["metadata"]
    if m["retrieved"] - m["duplicates_removed"] != m["unique"]:
        raise ValueError("Metadata retrieval/deduplication arithmetic fails")
    if m["unique"] - m["excluded"] != m["retained"]:
        raise ValueError("Metadata retention arithmetic fails")
    eras = expected["eras"]
    if sum(e["count"] for e in eras) != m["retained"]:
        raise ValueError("Era counts do not sum to the retained corpus")
    if [(e["start"], e["end"]) for e in eras] != [
        (2000, 2008), (2009, 2014), (2015, 2019), (2020, 2025)
    ]:
        raise ValueError("Unexpected era partition")
    if sum(frontier["screening_classes"].values()) != frontier["scopus_retrieved"]:
        raise ValueError("Frontier screening counts disagree with retrieval total")
    if len(index) != frontier["fulltext_included"] or len(index) != 31:
        raise ValueError("Appendix study index does not contain 31 entries")
    for field in ("study_id", "reference_number"):
        if len({r[field] for r in index}) != len(index):
            raise ValueError(f"Duplicate {field} in Appendix study index")
    if any(r["source_table"] not in {"A.7", "A.8"} for r in index):
        raise ValueError("Invalid appendix table designation")
    if any(not 2000 <= int(r["year"]) <= 2025 for r in index):
        raise ValueError("Index contains an out-of-window year")
    return expected, frontier, index


def empirical(meta_path: Path, frontier_path: Path, evidence_path: Path, flow_path: Path) -> None:
    expected, frontier, index = manifest()
    meta = rows(meta_path, {"record_id", "year"})
    if len(meta) != expected["metadata"]["retained"]:
        raise ValueError("Retained metadata row count does not match manuscript")
    if len({r["record_id"] for r in meta}) != len(meta) or any(
        not r["record_id"].strip() for r in meta
    ):
        raise ValueError("Duplicate/blank retained metadata identifiers")
    era_counts = Counter()
    for rec in meta:
        year = int(rec["year"])
        hit = [era["name"] for era in expected["eras"] if era["start"] <= year <= era["end"]]
        if len(hit) != 1:
            raise ValueError(f"Year {year} not in exactly one defined era")
        era_counts[hit[0]] += 1
    for era in expected["eras"]:
        if era_counts[era["name"]] != era["count"]:
            raise ValueError(f"Era {era['name']} count does not match manuscript")
    screen = rows(frontier_path, {"record_id", "screen_label"})
    if len(screen) != frontier["scopus_retrieved"]:
        raise ValueError("Frontier row count does not match manuscript")
    if len({r["record_id"] for r in screen}) != len(screen):
        raise ValueError("Duplicate frontier identifiers")
    actual = Counter(r["screen_label"].strip().lower() for r in screen)
    if dict(actual) != frontier["screening_classes"]:
        raise ValueError(f"Frontier strata mismatch: {actual}")
    evidence = rows(evidence_path, {"study_id", "reference_number", "source_locator", "verified_by", *DIMENSIONS})
    if len(evidence) != len(index):
        raise ValueError("Full-text evidence rows missing or duplicated")
    index_keys = {(r["study_id"], r["reference_number"]) for r in index}
    actual_keys = {(r["study_id"], r["reference_number"]) for r in evidence}
    if index_keys != actual_keys:
        raise ValueError("31-study evidence does not match Appendix reference index")
    if any(
        not r["source_locator"].strip() or not r["verified_by"].strip()
        or any(r[field].strip() not in STATUS for field in DIMENSIONS)
        for r in evidence
    ):
        raise ValueError("Evidence matrix contains unverified/missing fields or invalid statuses")
    if not flow_path.is_file():
        raise ValueError(f"Source flow file missing: {flow_path}")
    flow = json.loads(flow_path.read_text(encoding="utf-8"))
    for name, value in expected["metadata"].items():
        if flow.get(name) != value:
            raise ValueError(f"Source flow mismatch in {name}")
    print("PASS: supplied source records are internally consistent with manuscript targets.")
    print("NOTE: This is not an independent validation of bibliographic provenance or study interpretations.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["manifest", "empirical"], required=True)
    for arg in ("metadata", "frontier", "evidence", "flow"):
        parser.add_argument(f"--{arg}", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest()
        print("PASS: manuscript-derived totals and 31-reference index are internally consistent.")
        if args.mode == "empirical":
            if any(getattr(args, x) is None for x in ("metadata", "frontier", "evidence", "flow")):
                raise ValueError("Empirical verification requires --metadata, --frontier, --evidence and --flow")
            empirical(args.metadata, args.frontier, args.evidence, args.flow)
        else:
            print("SCOPE: manuscript consistency only; actual source record reproduction NOT established.")
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
