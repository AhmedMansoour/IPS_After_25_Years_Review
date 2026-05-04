# Reproducibility Guide

This guide is for someone who downloaded the repository (or a Zenodo
snapshot) and wants to reproduce the corpus statistics in the paper.

## Prerequisites

- Python 3.10 or newer.
- ~2 GB free disk space.
- ~5 minutes runtime on a recent laptop.
- Raw bibliographic exports from Scopus, WoS, IEEE *Xplore*. We do **not**
  redistribute these; see [`data/README.md`](../data/README.md) for the
  exact search queries to reproduce them, or download our archived
  snapshot from Zenodo (DOI: 10.5281/zenodo.XXXXXXX).

## Step 1 — Install

```bash
git clone https://github.com/AhmedMansoour/IPS_After_25_Years_Review.git
cd IPS_After_25_Years_Review
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Step 2 — Drop raw exports into place

```
data/raw/scopus/
    scopus_1.csv
    scopus_2.csv
data/raw/wos/
    savedrecs.xls
    savedrecs(1).xls
    ...
data/raw/ieee/
    conf_2020_2022.csv
    journal_2018_2024.csv
    ...
```

The exact filenames don't matter; the loaders pick up files by the glob
patterns in `config/source_mapping.yaml`.

## Step 3 — Run

```bash
make all
```

Equivalent to running these four commands in sequence:

```bash
ips-review harmonize  --scopus-dir data/raw/scopus  --wos-dir data/raw/wos  --ieee-dir data/raw/ieee  --output data/interim/harmonized.csv
ips-review dedup      --input data/interim/harmonized.csv                    --output data/interim/unique_corpus.csv
ips-review screen     --input data/interim/unique_corpus.csv  --dictionary config/coding_dictionary.v1.0.yaml  --output data/processed/corpus_screened.csv
ips-review classify   --input data/processed/corpus_screened.csv  --dictionary config/coding_dictionary.v1.0.yaml  --output data/processed/section_mapping.csv
```

You should see:

```
Stage 1 — non-scholarly excluded: ~280
Stage 2 — robotics-SLAM: ~310
...
Stage 3 — I-Core: ~19,583
Stage 4 — I-Context: ~5,552
Stage 5 — no-IPS-relevance: ~2,585
```

(Exact numbers depend on the snapshot date of your raw exports.)

## Step 4 — Verify

```bash
make check-reproducibility
```

This compares SHA-256 hashes of the produced CSVs against the values in
`config/expected_hashes.txt`. If the hashes match, you have bit-identical
reproduction.

If the hashes do not match, the most likely causes are:

1. **Different raw exports.** Compare your input file SHA-256s against
   the provenance headers in our published outputs (see Zenodo).
2. **Different dictionary version.** Check that `config/coding_dictionary.v1.0.yaml`
   matches the published version.
3. **Different package version.** Run `pip install -e .` again to ensure
   you're on the version recorded in `pyproject.toml`.

## Step 5 — Run the validation

```bash
ips-review validate \
    --rule-based  data/processed/corpus_screened.csv \
    --human-coded data/validation/sample_v1.0.consensus.csv \
    --report      outputs/reports/validation_v1.0.md
```

Reproduces the κ and percent-agreement numbers in Section II of the paper.

## Step 6 — Regenerate figures

```bash
make figures
```

Outputs land in `outputs/figures/` and `outputs/tables/`.

## Common pitfalls

- **CSV encoding.** All inputs and outputs use UTF-8 with BOM
  (`utf-8-sig`). If your editor strips the BOM, pandas will still read
  correctly.
- **Comment lines.** Output CSVs have `#`-prefixed provenance headers.
  Read them with `pd.read_csv(..., comment="#")`.
- **WoS legacy XLS files.** WoS exports as old BIFF `.xls`; the loader
  uses `xlrd` for these. Newer `.xlsx` exports also work via `openpyxl`.
- **Determinism.** The pipeline is deterministic given (raw files,
  dictionary, code version). Any non-determinism is a bug — please file
  an issue.
