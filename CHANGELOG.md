# Changelog

## Pending: INFFUS evidence and reproducibility alignment

- Refocused public documentation and citation metadata on the Indoor Spatial Intelligence review.
- Added a source-traceability scaffold, manuscript-count manifest, and a 31-study Appendix reference index.
- Added explicit, fail-closed empirical source verification and CI checks for manuscript-derived data.
- Replaced misleading output hash-verification behavior with explicit failure on a missing expected-hashes manifest.
- Documented unresolved public raw export rights and frozen-source recovery requirements.
- Did **not** claim complete empirical reproduction, publish a DOI, invent coded evidence, or alter published numerical findings.

## Screening-rule audit candidate v1.1

- Added an **opt-in** `config/coding_dictionary.v1.1.yaml` for independently testing five hand-labeled screening examples: indoor PDR, BLE asset positioning, VLC positioning, activity-aware indoor location estimation, and standalone fall detection.
- Preserved `config/coding_dictionary.v1.0.yaml` and `config/pipeline.yaml` unchanged as the historical/default pipeline. The v1.1 definitions are **not** the verified basis for the manuscript's 25,135 retained studies.
- Added regression tests documenting exactly five original v1.0 manual-label disagreements, alongside positive and negative cases for the v1.1 candidate.
- No empirical corpus counts, original decisions, figure results, or manuscript claims were modified. Adopting candidate criteria requires a full-record-level impact audit and scientific adjudication.
