# Methodology

This document is the authoritative description of the corpus-construction
and screening methodology. It mirrors Section II of the manuscript, with
direct cross-references to the code and dictionary that implement each step.

## 1. Sources

| Source | Files | Loader | Internal dedup key |
|---|---|---|---|
| Scopus | `scopus_*.csv` | [`io/scopus.py`](../src/ips_review/io/scopus.py) | `EID` |
| Web of Science | `savedrecs*.xls{,x}` | [`io/wos.py`](../src/ips_review/io/wos.py) | (none) |
| IEEE *Xplore* | `*.csv` (prefix `conf` → Conference; otherwise Non-Conference) | [`io/ieee.py`](../src/ips_review/io/ieee.py) | (none) |

Search queries used to produce each export are documented in
[`docs/search_strategy.md`](search_strategy.md).

## 2. Harmonization

Each source is mapped onto a unified 13-column schema by
[`harmonize.py`](../src/ips_review/harmonize.py), driven by
[`config/source_mapping.yaml`](../config/source_mapping.yaml).

```
Source · Title · Authors · Year · DOI · Abstract · Document_Type
Source_Title · Author_Keywords · Cited_By · EID · Affiliations · Link
```

Author keyword fields in IEEE fall back to *IEEE Terms* when *Author
Keywords* is empty. WoS *Link* is constructed from *DOI*.

## 3. Cross-database deduplication

Implemented in [`dedup.py`](../src/ips_review/dedup.py) as a Union-Find on
two equivalence relations:

1. **Normalized title match.** Lowercased, punctuation-stripped, whitespace-collapsed.
2. **Normalized DOI match.** Lowercased, `https://doi.org/` prefix stripped.

Two records are merged if they share *either* a normalized title *or* a
normalized DOI. Within each connected component, the representative is
chosen by source priority: **Scopus > WoS > IEEE**. Two diagnostic columns
are added: `Also_In` (sources containing the duplicate) and
`Duplicate_Count` (number of distinct sources in the cluster).

## 4. Three-tier rule-based screening

Implemented in [`screen.py`](../src/ips_review/screen.py); all patterns
read from [`config/coding_dictionary.v1.0.yaml`](../config/coding_dictionary.v1.0.yaml).

The screening operates on a single text field built per record:

```
text(r) = lowercase( Title || ' ' || Abstract || ' ' || Author_Keywords )
```

### Step 1 — Non-scholarly exclusions
Records with `Document_Type ∈ {Erratum, Retracted, Editorial, Letter, Short
survey, Note}` are labeled `E-Exclude / non-scholarly`.

### Step 2 — Out-of-scope safeguard categories
Seven categories (`robotics-SLAM`, `outdoor-GNSS/GPS`, `channel/propagation`,
`place/scene-recognition`, `activity-recognition`, `networking/comms`,
`outdoor-tracking`) each define an `exclude` regex and a `safeguard` regex.

A record is excluded as out-of-scope **only if** it matches `exclude` AND
does NOT match `safeguard`. The safeguard rescues records that share
vocabulary with an out-of-scope domain but explicitly target indoor
positioning (e.g., a SLAM paper that does pedestrian indoor tracking).

### Step 3 — I-Core
Records still unlabeled are tested against 11 strong direct-IPS regex
patterns (e.g., `indoor positioning`, `indoor localization`, `radio map`,
`fingerprint + indoor`, `UWB + ranging/position`). A match assigns
`Screen_Label = I-Core`.

### Step 4 — I-Context
Remaining unlabeled records are tested against 16 IPS-enabling patterns
(sensing+localization combinations, IMU/PDR+navigation, SLAM+indoor,
fingerprinting, radio map, crowdsourcing+localization, benchmark+positioning,
privacy+positioning, fusion+positioning, deployment+positioning, ML+positioning,
indoor+navigation, trilateration/triangulation, propagation+positioning).
A match assigns `Screen_Label = I-Context`.

### Step 5 — Residual exclusion
All still-unlabeled records are labeled `E-Exclude / no-IPS-relevance`.

### Step 6 — Priority tiering (retained records only)
- **T1**: review/survey documents, OR ≥100 citations, OR keyword-marked
  (survey | review | benchmark | dataset | data paper | evaluation framework
  | competition).
- **T2**: ≥20 citations OR Document_Type ∈ {Article, J, Non-Conference}.
- **T3**: remaining retained records.

## 5. Section-level multi-label mapping

Implemented in [`classify.py`](../src/ips_review/classify.py). For each
retained record:

- **Section III — Era** (year-based, mutually exclusive):
  Era1 ≤ 2008; Era2 2009–2014; Era3 2015–2019; Era4 ≥ 2020.
- **Section IV.1 — Sensing source** (multi-label): 11 modalities
  (Wi-Fi, BLE, UWB, RFID, Cellular/5G, IMU/PDR, Magnetic, Vision, LiDAR, VLC, Acoustic).
- **Section IV.2 — Paradigm** (multi-label): Fingerprinting, ToA/TDoA, AoA,
  RSSI Ranging, PDR/Inertial, SLAM.
- **Section VI — Deployment indicators** (multi-label): RealWorld,
  MultiBuilding, LongTerm, Calibration, Maintenance.

Multi-label means a single paper can carry e.g. both `Sec_IV_Sensing_Wi-Fi`
and `Sec_IV_Sensing_BLE`.

## 6. AI-assisted dictionary construction

The coding dictionary used in Stages 3–5 was drafted with assistance from
Anthropic Claude and OpenAI ChatGPT. Each candidate pattern was reviewed,
edited, and approved by the human authors before inclusion. **No
record-level LLM inference is performed by the pipeline.** See
[`ai_disclosure.md`](ai_disclosure.md) for the full per-stage AI-use
breakdown.

## 7. Validation

Two independent layers:

1. **Metadata-level validation.** A stratified sample of N records is
   drawn by [`sampling.py`](../src/ips_review/sampling.py), independently
   coded by human reviewers, and compared against the rule-based labels
   using Cohen's κ ([`validate.py`](../src/ips_review/validate.py)). The
   protocol is in [`validation_protocol.md`](validation_protocol.md).
2. **Full-text panel.** A 525-paper stratified sample is independently
   coded by three human reviewers from the original PDFs. AI assistance is
   restricted to extraction-note organization and consistency-checking; no
   numerical value or final label is accepted from AI without human
   verification against the source.

## 8. Reproducibility guarantees

- Every output CSV carries a provenance header: package version, git SHA,
  dictionary version, input file SHA-256s, run timestamp.
- The full pipeline is deterministic given (raw files, dictionary version).
- Bit-identical reproduction is verified by `make check-reproducibility`
  against expected hashes in `config/expected_hashes.txt`.
