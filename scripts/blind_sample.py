"""Blind a stratified sample for human coding.

Drops the rule-based label column and shuffles the rows so reviewers
cannot anchor to it.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--drop-cols", default="Screen_Label,Exclude_Reason,Priority_Tier")
    p.add_argument("--seed", type=int, default=20260505)
    args = p.parse_args()

    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig", comment="#")
    drop = [c.strip() for c in args.drop_cols.split(",") if c.strip() in df.columns]
    df = df.drop(columns=drop).sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    df["Human_Label"] = ""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"Wrote blinded sample: {args.output} ({len(df)} rows, dropped {drop})")


if __name__ == "__main__":
    main()
