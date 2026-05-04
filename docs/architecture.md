# Architecture

## Component diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                           data/raw/                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│   │  scopus/     │  │   wos/       │  │   ieee/      │              │
│   │  *.csv       │  │  *.xls{,x}   │  │   *.csv      │              │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└──────────┼─────────────────┼─────────────────┼─────────────────────┘
           │                 │                 │
           ▼                 ▼                 ▼
       io/scopus.py      io/wos.py        io/ieee.py
           │                 │                 │
           └────────┬────────┴────────┬────────┘
                    │                 │
                    ▼                 │
            harmonize.py  ←───  config/source_mapping.yaml
                    │
                    ▼
           data/interim/harmonized.csv
                    │
                    ▼
              dedup.py  (union-find on title + DOI)
                    │
                    ▼
           data/interim/unique_corpus.csv
                    │
                    ▼
              screen.py  ←───  config/coding_dictionary.v1.0.yaml
                    │           ↑
                    │           │ (LLM-drafted, human-finalized)
                    ▼
        data/processed/corpus_screened.csv
                    │
                    ├──────────────────────┐
                    ▼                      ▼
              classify.py             sampling.py ──► validation/sample_v1.0.csv
                    │                                          │
                    ▼                                          │ (humans code)
        data/processed/section_mapping.csv                    ▼
                    │                              validation/sample_v1.0.consensus.csv
                    ▼                                          │
              figures/*.py                                     ▼
                    │                                    validate.py
                    ▼                                          │
        outputs/figures, outputs/tables                        ▼
                                              outputs/reports/validation_v1.0.md
```

## Layer responsibilities

| Layer | Files | Responsibility | Determinism |
|---|---|---|---|
| **IO** | `io/*.py` | Read raw exports as DataFrames; tag with `Source`. No schema interpretation. | Deterministic |
| **Schema** | `harmonize.py` + `source_mapping.yaml` | Map source-specific columns to a unified schema. | Deterministic |
| **Identity** | `dedup.py` | Decide which records refer to the same paper. | Deterministic |
| **Semantics** | `screen.py`, `classify.py` + `coding_dictionary.v1.0.yaml` | Assign labels via regex on Title+Abstract+Keywords. | Deterministic |
| **Quality** | `sampling.py`, `validate.py` | Estimate agreement between rules and human judgment. | Seed-deterministic |
| **Presentation** | `figures/*.py` | Render numbers as PDF / LaTeX. | Deterministic |
| **Provenance** | `utils/provenance.py` | Stamp every output with version + hash + timestamp. | — |

## Key design choices

- **Coding dictionary as data, not code.** Reviewers can audit, diff, and
  propose changes to the dictionary without reading Python.
- **Single text field for screening.** All semantic labels operate on the
  same `lower(Title || Abstract || Keywords)` string. There is no
  hidden field-specific logic.
- **Safeguard pattern.** Every out-of-scope category has a paired
  safeguard regex that prevents false exclusion of IPS papers sharing
  vocabulary with the out-of-scope domain. This is the single most
  important defense against under-recall in the rule-based screener.
- **Multi-label section mapping.** A paper that uses both Wi-Fi and BLE
  appears under both modalities. There is no forced single-label assignment.
- **Provenance headers.** Every output CSV starts with `#` lines listing
  the dictionary version, code git SHA, and SHA-256 of every input file
  used. Drop a CSV into a question and you can always recover its origin.
- **No LLM at inference time.** LLMs were used only for dictionary
  drafting and (separately) full-text panel note organization. The
  corpus pipeline contains no API calls.

## Extension points

| Want to... | Edit |
|---|---|
| Add a new source (e.g., DBLP) | Add `io/dblp.py`, add a section to `source_mapping.yaml`, add the loader to `harmonize.py` |
| Add a new sensing modality | Add an entry under `sensing_sources:` in the dictionary YAML; bump version |
| Tighten an exclusion safeguard | Edit the relevant `safeguard:` regex; bump version; re-run validation |
| Add a new section axis | Add a top-level dict under the dictionary YAML; add a loop in `classify.py` |
| Validate against a new human-coded sample | Drop the CSV under `data/validation/` and run `make validate` |
