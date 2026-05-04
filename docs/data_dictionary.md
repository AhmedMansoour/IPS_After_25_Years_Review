# Data Dictionary

Schema reference for every CSV produced by the pipeline.

## `data/interim/harmonized.csv`

Output of Stage 1 (`harmonize`). One row per raw record, **before** dedup.

| Column | Type | Description |
|---|---|---|
| `Source` | string | One of `Scopus`, `WoS`, `IEEE`. |
| `Title` | string | Paper title. |
| `Authors` | string | Author list as exported. |
| `Year` | string | Publication year. |
| `DOI` | string | Digital Object Identifier (raw). |
| `Abstract` | string | Abstract text. |
| `Document_Type` | string | Source-reported document type. |
| `Source_Title` | string | Journal / conference title. |
| `Author_Keywords` | string | Author-provided keywords; falls back to IEEE Terms when empty (IEEE only). |
| `Cited_By` | string | Citation count as reported. |
| `EID` | string | Scopus EID (empty for non-Scopus). |
| `Affiliations` | string | Author affiliations / addresses. |
| `Link` | string | URL to source record. |

## `data/interim/unique_corpus.csv`

Output of Stage 2 (`dedup`). One row per **unique** paper (representative
chosen by source priority Scopus > WoS > IEEE).

Adds two columns to the harmonized schema:

| Column | Type | Description |
|---|---|---|
| `Also_In` | string | Semicolon-separated list of other sources containing the same paper. |
| `Duplicate_Count` | int | Number of distinct sources in the cluster. |

## `data/processed/corpus_screened.csv`

Output of Stage 3 (`screen`). Adds:

| Column | Type | Values | Description |
|---|---|---|---|
| `Screen_Label` | string | `I-Core`, `I-Context`, `E-Exclude` | Three-tier screening outcome. |
| `Exclude_Reason` | string | `non-scholarly`, `out-of-scope: <category>`, `no-IPS-relevance`, `""` | Reason for exclusion (empty for retained records). |
| `Priority_Tier` | string | `T1`, `T2`, `T3`, `""` | Assigned only for retained records. |

## `data/processed/section_mapping.csv`

Output of Stage 5 (`classify`). Adds:

| Column | Type | Values | Description |
|---|---|---|---|
| `Sec_III_Era` | string | `Era1`, `Era2`, `Era3`, `Era4`, `""` | Year-based era (retained records only). |
| `Sec_IV_Sensing_<modality>` | bool | True/False | One column per modality in dictionary `sensing_sources`. |
| `Sec_IV_Paradigm_<paradigm>` | bool | True/False | One column per paradigm. |
| `Sec_VI_Deploy_<indicator>` | bool | True/False | One column per deployment indicator. |

## `data/validation/sample_*.csv`

Output of `ips-review sample`. Stratified sample with all columns from
`corpus_screened.csv` plus:

| Column | Type | Description |
|---|---|---|
| `_stratum` | string | The stratum identifier (concatenation of strata column values). |
| `Human_Label` | string | **Empty by default**; reviewers fill with `I-Core`, `I-Context`, or `E-Exclude`. |

## Provenance headers

Every output CSV begins with `#`-prefixed comment lines, e.g.:

```
# ips_review pipeline output
# stage: screen
# package_version: 1.0.0
# git_sha: a1b2c3d
# python: 3.11.5  platform: Linux-6.5.0-x86_64
# generated_utc: 2026-05-05T10:23:14Z
# dictionary_version: 1.0
# input.input: data/interim/unique_corpus.csv  sha256=fa39b2e0c1d4c8aa
# input.dictionary: config/coding_dictionary.v1.0.yaml  sha256=4c2e8b3a1f9d6e7c
```

Pandas reads them transparently with `pd.read_csv(..., comment="#")`.
