# INFFUS-D-26-05291: study-specific reproducibility and evidence

**Paper:** From Indoor Positioning to Indoor Spatial Intelligence: A Field-Evolution Review  
**Search window:** 2000–2025  
**Current verification level:** manuscript-derived reference targets and table index only.

## Package contents

- `data/expected_results.json`: exactly the longitudinal record-flow totals and four era counts stated in the submitted manuscript.
- `data/frontier_summary.json`: reported counts of the dedicated 176-record Scopus query.
- `data/fulltext_31_index.csv`: **all 31 study reference IDs and years** transcribed from Appendix Tables A.7 and A.8. This is not a historical screening decision log.
- `data/evidence_template.csv`: unfilled columns for source-verified coding; **no original-study findings are invented**.
- `scripts/verify.py`: validation routines with separate manifest and empirical modes.
- `docs/PROVENANCE.md`: provenance, required data schemas and unresolved source items.
- `docs/VALIDITY_CODING.md`: transparent instructions for grounded-system evidence coding.
- `docs/LICENSING_AUDIT.md`: redistribution/archival safety issues.

## Run the available tests

Python 3.10+ is sufficient; no third-party Python packages are needed.

```bash
python studies/inffus_2026/scripts/verify.py --mode manifest
python -m unittest discover -s studies/inffus_2026/tests -v
```

Manifest mode checks manuscript-specified arithmetic and the 31-item index. It does not authenticate study claims.

## Run strict source verification

After the actual original records have been recovered and validated against the submission:

```bash
python studies/inffus_2026/scripts/verify.py --mode empirical \
  --metadata PATH/retained_metadata.csv \
  --frontier PATH/frontier_screening.csv \
  --evidence PATH/validated_evidence.csv \
  --flow PATH/source_flow.json
```

It intentionally **fails** when any required input is absent or unreconciled. Do not populate the required files with synthetic records to make this step pass.

## Release gate

The package is **not** currently a complete independently reproducible paper artifact. Unresolved items: original dated database exports, historical deduplication and screening decisions, the detailed 176-record frontier register, origin and full-text verification of the 31 studies, exact figure-generation inputs, the executed query date, and documentation of rights to distribute any original records. See [PROVENANCE.md](docs/PROVENANCE.md).
