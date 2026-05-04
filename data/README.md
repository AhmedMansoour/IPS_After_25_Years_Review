# `data/` — corpus storage layout

This directory stores the corpus at every pipeline stage. **The
contents are mostly gitignored / LFS-tracked**; running the pipeline
will populate it.

## Subdirectories

| Path | Contents | Tracked in git? |
|---|---|---|
| `raw/scopus/` | Raw Scopus CSV exports | **No** (license: Elsevier) |
| `raw/wos/` | Raw Web of Science XLS/XLSX exports | **No** (license: Clarivate) |
| `raw/ieee/` | Raw IEEE *Xplore* CSV exports | **No** (license: IEEE) |
| `interim/` | `harmonized.csv`, `unique_corpus.csv` | LFS (regenerable) |
| `processed/` | `corpus_screened.csv`, `section_mapping.csv` | LFS (regenerable) |
| `validation/` | Stratified samples + human-coded outputs | LFS or plain (small files) |

## How to obtain the raw exports

We do **not** redistribute the raw bibliographic exports because the
licenses of Scopus, Web of Science, and IEEE *Xplore* prohibit
redistribution.

Two options:

1. **Re-run the published queries** in [`docs/search_strategy.md`](../docs/search_strategy.md)
   on each database. Drop the resulting files into the appropriate
   `raw/<database>/` directory. Re-running queries today will produce a
   slightly larger corpus than the snapshot used in the paper because
   new publications appear continuously.

2. **Download our archived snapshot** from Zenodo
   (DOI: 10.5281/zenodo.XXXXXXX). The snapshot is the exact set of files
   used in the published paper, with SHA-256 checksums recorded in
   `config/expected_hashes.txt`. Note: access to the Zenodo snapshot may
   be restricted to verified researchers depending on database licenses.

After dropping files into `raw/`, run:

```bash
make all
```

## File size expectations

- `raw/scopus/`: ~50–80 MB
- `raw/wos/`:    ~30–50 MB
- `raw/ieee/`:   ~40–60 MB
- `interim/harmonized.csv`: ~150 MB
- `interim/unique_corpus.csv`: ~110 MB (~27,720 rows)
- `processed/corpus_screened.csv`: ~115 MB (adds 3 columns)
- `processed/section_mapping.csv`: ~125 MB (adds ~25 boolean columns)

If you need to commit the processed CSVs, use Git LFS (see
`.gitattributes`).
