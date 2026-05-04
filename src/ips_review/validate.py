"""Validation: rule-based labels vs. human-coded labels.

Computes Cohen's kappa, percent agreement, and a per-label confusion
breakdown. The output is written as a Markdown report for direct inclusion
in supplementary material.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix

log = logging.getLogger(__name__)

DEFAULT_LABELS = ["I-Core", "I-Context", "E-Exclude"]


@dataclass
class ValidationReport:
    n: int
    cohen_kappa: float
    percent_agreement: float
    per_label_recall: dict[str, float]
    per_label_precision: dict[str, float]
    confusion: pd.DataFrame
    disagreements: pd.DataFrame

    def to_markdown(
        self,
        *,
        dictionary_version: str | None = None,
        rule_based_path: str | None = None,
        human_coded_path: str | None = None,
    ) -> str:
        lines = [
            "# Validation Report",
            "",
            "Comparison of rule-based metadata labels against human-coded labels.",
            "",
            "## Summary",
            "",
            f"- Sample size: **{self.n}**",
            f"- Cohen's kappa: **{self.cohen_kappa:.3f}**",
            f"- Percent agreement: **{self.percent_agreement:.1%}**",
        ]
        if dictionary_version:
            lines.append(f"- Dictionary version: `{dictionary_version}`")
        if rule_based_path:
            lines.append(f"- Rule-based source: `{rule_based_path}`")
        if human_coded_path:
            lines.append(f"- Human-coded source: `{human_coded_path}`")

        lines += [
            "",
            "## Per-label agreement",
            "",
            "| Label | Recall (rule vs. human) | Precision (rule vs. human) |",
            "|---|---:|---:|",
        ]
        for lab in DEFAULT_LABELS:
            r = self.per_label_recall.get(lab, float("nan"))
            p = self.per_label_precision.get(lab, float("nan"))
            lines.append(f"| {lab} | {r:.1%} | {p:.1%} |")

        lines += [
            "",
            "## Confusion matrix",
            "",
            "Rows = human (truth); columns = rule-based label.",
            "",
            self.confusion.to_markdown(),
            "",
            "## Disagreements",
            "",
            f"{len(self.disagreements)} disagreements out of {self.n} records "
            f"({len(self.disagreements) / max(self.n, 1):.1%}).",
            "",
            "Disagreements are listed in the supplementary "
            "`outputs/reports/validation_disagreements.csv`.",
        ]
        return "\n".join(lines)


def validate(
    rule_based: pd.DataFrame,
    human_coded: pd.DataFrame,
    *,
    join_on: str = "DOI",
    rule_label_col: str = "Screen_Label",
    human_label_col: str = "Human_Label",
    labels: list[str] | None = None,
) -> ValidationReport:
    """Compare two labeled DataFrames on `join_on` and report agreement."""
    labels = labels or DEFAULT_LABELS
    rb = rule_based[[join_on, rule_label_col]].rename(columns={rule_label_col: "_rb"})
    hc = human_coded[[join_on, human_label_col]].rename(columns={human_label_col: "_hc"})
    merged = rb.merge(hc, on=join_on, how="inner").dropna(subset=["_rb", "_hc"])

    if merged.empty:
        raise ValueError(
            f"No overlapping rows between rule-based and human-coded sets on '{join_on}'."
        )

    y_rb = merged["_rb"].astype(str).values
    y_hc = merged["_hc"].astype(str).values
    kappa = float(cohen_kappa_score(y_hc, y_rb, labels=labels))
    pct = float((y_rb == y_hc).mean())

    cm = confusion_matrix(y_hc, y_rb, labels=labels)
    confusion = pd.DataFrame(cm, index=labels, columns=labels)

    per_recall = {
        lab: (cm[i, i] / cm[i, :].sum()) if cm[i, :].sum() else float("nan")
        for i, lab in enumerate(labels)
    }
    per_precision = {
        lab: (cm[i, i] / cm[:, i].sum()) if cm[:, i].sum() else float("nan")
        for i, lab in enumerate(labels)
    }

    disagree = merged[merged["_rb"] != merged["_hc"]].copy()
    disagree.rename(columns={"_rb": "rule_label", "_hc": "human_label"}, inplace=True)

    log.info(
        "Validation: n=%d  kappa=%.3f  pct_agreement=%.3f", len(merged), kappa, pct
    )
    return ValidationReport(
        n=len(merged),
        cohen_kappa=kappa,
        percent_agreement=pct,
        per_label_recall=per_recall,
        per_label_precision=per_precision,
        confusion=confusion,
        disagreements=disagree,
    )
