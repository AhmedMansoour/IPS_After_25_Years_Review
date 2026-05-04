# Validation Protocol

This document specifies how to draw a stratified sample from the screened
corpus, have it independently coded by humans, and quantify agreement
against the rule-based labels.

## Why this exists

A rule-based screener is only as trustworthy as the dictionary that
drives it. Validation against independent human coding is what converts
"the rules look reasonable" into "the rules agree with expert judgment at
κ = X.XX, and disagreements concentrate in [these specific patterns]."

## Step 1 — Draw the stratified sample

```bash
ips-review sample \
    --input   data/processed/corpus_screened.csv \
    --n       400 \
    --strata  Screen_Label,Sec_III_Era \
    --seed    20260505 \
    --output  data/validation/sample_v1.0.csv
```

This draws ≈400 records balanced across the cross-product of
{I-Core, I-Context, E-Exclude} × {Era1, Era2, Era3, Era4}. Each stratum
gets at least 5 records. The output has an empty `Human_Label` column for
reviewers to fill.

**Sample-size guidance.** For κ confidence intervals of approximately
±0.05 with three label classes at expected agreement ≈0.85, a sample of
~400 records is adequate. If you have only one human coder, draw a
smaller sample (200) but interpret κ confidence intervals accordingly.

## Step 2 — Blind the sample for coders

```bash
python scripts/blind_sample.py \
    --input  data/validation/sample_v1.0.csv \
    --output data/validation/sample_v1.0.blinded.csv
```

This drops the `Screen_Label` column and shuffles the rows so coders
cannot anchor to the rule-based label. (Implement `blind_sample.py`
according to your project's blinding requirements.)

## Step 3 — Independent human coding

Each reviewer assigns one of {I-Core, I-Context, E-Exclude} to every row,
using **only** Title + Abstract + Author_Keywords (the same fields the
rule-based classifier sees) and the published coding dictionary as a
reference.

Output: `data/validation/sample_v1.0.coded_by_<reviewer>.csv`.

If multiple reviewers code the sample, compute pairwise inter-rater
agreement first; resolve disagreements by adjudication; then compute
agreement between the consensus human label and the rule-based label.

## Step 4 — Compute agreement

```bash
ips-review validate \
    --rule-based  data/processed/corpus_screened.csv \
    --human-coded data/validation/sample_v1.0.consensus.csv \
    --rule-col    Screen_Label \
    --human-col   Human_Label \
    --report      outputs/reports/validation_v1.0.md
```

Outputs:

- `outputs/reports/validation_v1.0.md` — Markdown report with κ, percent
  agreement, per-label recall/precision, confusion matrix.
- `outputs/reports/validation_v1.0_disagreements.csv` — every disagreement
  with both labels for diagnostic review.

## Step 5 — Reporting in the paper

Report at minimum:

- Sample size N.
- Stratification scheme.
- Number of human reviewers and adjudication rule.
- Cohen's κ overall and per label.
- Percent agreement overall and per label.
- Top 3 disagreement patterns (e.g., "I-Context papers labeled E-Exclude
  by humans tended to involve [specific pattern]").

## Step 6 — Use disagreements to refine the dictionary (optional)

If a systematic disagreement reveals a dictionary defect, propose the
edit via PR. **The dictionary version MUST be bumped** (`v1.0` → `v1.1`)
and the previous validation results re-run on the new version. Never
silently edit a dictionary that has already produced reported numbers.

## What NOT to do

- ❌ Never use the rule-based label as input to human coders. Blinding is mandatory.
- ❌ Never compute κ on a non-stratified sample then report it as if it were stratified.
- ❌ Never accept κ ≥ 0.8 as proof the dictionary is correct. κ measures
  consistency, not validity. A wrong-but-consistent rule still has high κ.
- ❌ Never report κ on the full corpus without specifying which version
  of the dictionary produced the rule-based labels.
