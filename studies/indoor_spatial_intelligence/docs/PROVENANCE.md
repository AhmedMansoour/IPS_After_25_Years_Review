# Provenance and source reconciliation

This file records facts taken from the submitted manuscript and identifies what **cannot** be established from manuscript totals alone.

## Longitudinal database mapping (Section 2.1)

- Scopus, Web of Science and IEEE Xplore searches **6 April 2026** using the stable expressions "indoor positioning", "indoor localization", and "indoor localisation", with database-specific syntax.
- Initial: 48,955; duplicates: 21,235; unique: 27,720; excluded: 2,585; retained: 25,135.
- Era totals E1=801, E2=3,836, E3=8,379, E4=12,119.
- The existing generic repository search strategy is **not** automatically a faithful transcription of these specific executed queries. Recover the original search logs, full predicates, exports, and database settings.

## Frontier search (Section 2.2 and Appendix A)

- Dedicated Scopus query executed "Mid 2026"; **exact date not specified** in the submitted manuscript.
- Query returned 176: core 68, supporting 69, excluded 39.
- Supplementary discovery contributed to purposive full-text selection; the database/supplementary split is not numerically supplied by the paper.
- 31 sources in Appendix Tables A.7–A.8. `fulltext_31_index.csv` transcribes only reference numbers and years; it does not document when a study was identified or by whom it was coded.
- Retrieve original historical decisions and full text; do **not** infer counts of sources from each route.

## Empirical verification input schemas

These are deliberately minimal CSV interchange formats for the validation script. Stable identifiers must reflect real records, not generated synthetic IDs.

1. `retained_metadata.csv`: `record_id,year`, one record per retained study, with real deduplicated IDs and publication years. Exactly 25,135 distinct IDs. All four era counts must reproduce.
2. `frontier_screening.csv`: `record_id,screen_label`, one record per retrieved Scopus frontier study. Exactly 176 distinct IDs, with `core` (68), `supporting` (69), or `excluded` (39).
3. `validated_evidence.csv`: `study_id,reference_number,source_locator,verified_by,grounding_status,representation_status,reasoning_status,uncertainty_status,provenance_status,action_verification_status,update_status`, one row per original Appendix study. All statuses must be human-assessed; see [VALIDITY_CODING.md](VALIDITY_CODING.md).
4. `source_flow.json`: `retrieved,duplicates_removed,unique,excluded,retained`, derived from documented source processing. This summary is **not** a replacement for the original per-record deduplication/screening log.

The strict script checks the counts, completeness, and basic logical consistency of these files. Passing cannot itself prove that values were faithfully extracted from published studies; source audits remain necessary.

## Before reporting 'reproducible'

- Check all source files against date-stamped original exports and reproduce harmonization, deduplication and screening decisions from the documented algorithm.
- Rebuild manuscript Figure 2 panels and Table 2 using the accepted coding dictionary, count definitions and exact frozen corpus.
- Check all study source locators and validity coding against the corresponding primary publications.
- Document disagreements, adjudication, version reconciliation and changes to reported manuscript claims.
- Obtain redistribution permission before publishing vendor exports or third-party full texts.
