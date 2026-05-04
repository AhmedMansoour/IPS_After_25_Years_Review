"""Compute Cohen's kappa between two human coders' label CSVs.

Use this for inter-rater reliability BEFORE comparing against the
rule-based labels.
"""
from __future__ import annotations

import argparse

import pandas as pd
from sklearn.metrics import cohen_kappa_score


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--coder-a", required=True, help="CSV with columns DOI, Human_Label")
    p.add_argument("--coder-b", required=True)
    p.add_argument("--label-col", default="Human_Label")
    p.add_argument("--join-on", default="DOI")
    args = p.parse_args()

    a = pd.read_csv(args.coder_a, comment="#")[[args.join_on, args.label_col]].rename(columns={args.label_col: "_a"})
    b = pd.read_csv(args.coder_b, comment="#")[[args.join_on, args.label_col]].rename(columns={args.label_col: "_b"})
    m = a.merge(b, on=args.join_on, how="inner").dropna(subset=["_a", "_b"])
    if m.empty:
        raise SystemExit("No overlap between coders.")

    labels = ["I-Core", "I-Context", "E-Exclude"]
    k = cohen_kappa_score(m["_a"], m["_b"], labels=labels)
    pct = (m["_a"] == m["_b"]).mean()
    print(f"n = {len(m)}")
    print(f"Cohen's kappa = {k:.3f}")
    print(f"Percent agreement = {pct:.1%}")
    disagree = m[m["_a"] != m["_b"]]
    if not disagree.empty:
        print(f"\n{len(disagree)} disagreements:")
        print(disagree.to_string(index=False))


if __name__ == "__main__":
    main()
