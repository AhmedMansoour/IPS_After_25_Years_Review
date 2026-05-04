"""Command-line interface: `ips-review <command> ...`.

Exposes one subcommand per pipeline stage so each can be run, tested, and
reproduced in isolation.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from . import __version__
from .classify import classify
from .config import load_dictionary, load_yaml
from .dedup import deduplicate
from .harmonize import harmonize
from .sampling import stratified_sample
from .screen import screen
from .utils.provenance import provenance_header
from .validate import validate

log = logging.getLogger("ips_review")


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-7s  %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def _write_csv(df: pd.DataFrame, path: str | Path, header: str | None) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if header:
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            f.write(header)
            df.to_csv(f, index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")
    log.info("Wrote %d rows -> %s", len(df), path)


# ────────────────────────────────────────────────────────────────────────────
# Subcommand handlers
# ────────────────────────────────────────────────────────────────────────────
def cmd_harmonize(args: argparse.Namespace) -> int:
    df = harmonize(
        scopus_dir=args.scopus_dir,
        wos_dir=args.wos_dir,
        ieee_dir=args.ieee_dir,
        mapping_path=args.mapping,
    )
    hdr = provenance_header(
        stage="harmonize",
        inputs={
            "scopus_dir": args.scopus_dir or "",
            "wos_dir": args.wos_dir or "",
            "ieee_dir": args.ieee_dir or "",
            "mapping": args.mapping,
        },
    )
    _write_csv(df, args.output, hdr)
    return 0


def cmd_dedup(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig", comment="#")
    out = deduplicate(df)
    hdr = provenance_header(stage="dedup", inputs={"input": args.input})
    _write_csv(out, args.output, hdr)
    return 0


def cmd_screen(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig", comment="#")
    dictionary = load_dictionary(args.dictionary)
    out = screen(df, dictionary)
    hdr = provenance_header(
        stage="screen",
        dictionary_version=dictionary.version,
        inputs={"input": args.input, "dictionary": args.dictionary},
    )
    _write_csv(out, args.output, hdr)
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig", comment="#")
    dictionary = load_dictionary(args.dictionary)
    out = classify(df, dictionary)
    hdr = provenance_header(
        stage="classify",
        dictionary_version=dictionary.version,
        inputs={"input": args.input, "dictionary": args.dictionary},
    )
    _write_csv(out, args.output, hdr)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    rb = pd.read_csv(args.rule_based, dtype=str, encoding="utf-8-sig", comment="#")
    hc = pd.read_csv(args.human_coded, dtype=str, encoding="utf-8-sig", comment="#")
    report = validate(
        rb,
        hc,
        join_on=args.join_on,
        rule_label_col=args.rule_col,
        human_label_col=args.human_col,
    )
    md = report.to_markdown(
        rule_based_path=args.rule_based,
        human_coded_path=args.human_coded,
    )
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(md, encoding="utf-8")
    log.info("Wrote validation report -> %s", args.report)
    if not report.disagreements.empty:
        dpath = Path(args.report).with_suffix("").as_posix() + "_disagreements.csv"
        report.disagreements.to_csv(dpath, index=False, encoding="utf-8-sig")
        log.info("Wrote %d disagreements -> %s", len(report.disagreements), dpath)
    return 0


def cmd_sample(args: argparse.Namespace) -> int:
    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig", comment="#")
    strata = [s.strip() for s in args.strata.split(",") if s.strip()]
    sample = stratified_sample(df, n=args.n, strata=strata, seed=args.seed)
    sample["Human_Label"] = ""  # to be filled by reviewers
    hdr = provenance_header(
        stage="sample",
        inputs={"input": args.input, "strata": ",".join(strata), "n": str(args.n)},
    )
    _write_csv(sample, args.output, hdr)
    return 0


def cmd_provenance(args: argparse.Namespace) -> int:
    p = Path(args.dir)
    for csv in sorted(p.glob("*.csv")):
        print(f"=== {csv} ===")
        with csv.open("r", encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                if line.startswith("#"):
                    print(line.rstrip())
                else:
                    break
        print()
    return 0


def cmd_run_all(args: argparse.Namespace) -> int:
    cfg = load_yaml(args.config)
    p = cfg["paths"]
    dictionary = cfg["dictionary"]

    log.info("=== Stage 1: harmonize ===")
    h = harmonize(
        scopus_dir=p["raw"]["scopus"],
        wos_dir=p["raw"]["wos"],
        ieee_dir=p["raw"]["ieee"],
        mapping_path=cfg["source_mapping"],
    )
    _write_csv(h, p["interim"]["harmonized"], provenance_header(stage="harmonize"))

    log.info("=== Stage 2: dedup ===")
    u = deduplicate(h)
    _write_csv(u, p["interim"]["unique"], provenance_header(stage="dedup"))

    log.info("=== Stage 3: screen ===")
    d = load_dictionary(dictionary)
    s = screen(u, d)
    _write_csv(
        s,
        p["processed"]["screened"],
        provenance_header(stage="screen", dictionary_version=d.version),
    )

    log.info("=== Stage 5: classify ===")
    c = classify(s, d)
    _write_csv(
        c,
        p["processed"]["section_mapping"],
        provenance_header(stage="classify", dictionary_version=d.version),
    )

    log.info("=== Pipeline complete ===")
    return 0


# ────────────────────────────────────────────────────────────────────────────
# Argument parser
# ────────────────────────────────────────────────────────────────────────────
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ips-review",
        description="Reproducibility CLI for the 25-Years IPS Systematic Review.",
    )
    p.add_argument("--version", action="version", version=f"ips-review {__version__}")
    p.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")

    # harmonize
    h = sub.add_parser("harmonize", help="Stage 1: load + unify Scopus/WoS/IEEE")
    h.add_argument("--scopus-dir")
    h.add_argument("--wos-dir")
    h.add_argument("--ieee-dir")
    h.add_argument("--mapping", default="config/source_mapping.yaml")
    h.add_argument("--output", required=True)
    h.set_defaults(func=cmd_harmonize)

    # dedup
    d = sub.add_parser("dedup", help="Stage 2: cross-database deduplication")
    d.add_argument("--input", required=True)
    d.add_argument("--output", required=True)
    d.set_defaults(func=cmd_dedup)

    # screen
    s = sub.add_parser("screen", help="Stage 3: rule-based three-tier screening")
    s.add_argument("--input", required=True)
    s.add_argument("--dictionary", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=cmd_screen)

    # classify
    c = sub.add_parser("classify", help="Stage 5: section-level multi-label mapping")
    c.add_argument("--input", required=True)
    c.add_argument("--dictionary", required=True)
    c.add_argument("--output", required=True)
    c.set_defaults(func=cmd_classify)

    # validate
    v = sub.add_parser("validate", help="Cohen's kappa vs. human-coded sample")
    v.add_argument("--rule-based", required=True)
    v.add_argument("--human-coded", required=True)
    v.add_argument("--report", required=True)
    v.add_argument("--join-on", default="DOI")
    v.add_argument("--rule-col", default="Screen_Label")
    v.add_argument("--human-col", default="Human_Label")
    v.set_defaults(func=cmd_validate)

    # sample
    sm = sub.add_parser("sample", help="Draw a stratified validation sample")
    sm.add_argument("--input", required=True)
    sm.add_argument("--n", type=int, default=400)
    sm.add_argument("--strata", default="Screen_Label,Sec_III_Era")
    sm.add_argument("--seed", type=int, default=20260505)
    sm.add_argument("--output", required=True)
    sm.set_defaults(func=cmd_sample)

    # provenance
    pv = sub.add_parser("provenance", help="Print provenance headers from output CSVs")
    pv.add_argument("--dir", default="data/processed")
    pv.set_defaults(func=cmd_provenance)

    # run-all
    ra = sub.add_parser("run-all", help="Run the full pipeline using pipeline.yaml")
    ra.add_argument("--config", default="config/pipeline.yaml")
    ra.set_defaults(func=cmd_run_all)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.log_level)
    try:
        return int(args.func(args) or 0)
    except FileNotFoundError as e:
        log.error("File not found: %s", e)
        return 2
    except Exception:
        log.exception("Unhandled error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
