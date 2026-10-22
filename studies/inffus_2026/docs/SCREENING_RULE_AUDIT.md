# Screening rule validation and corpus-impact requirements

The historical `config/coding_dictionary.v1.0.yaml` is preserved unchanged, including its original rationale and screening patterns. It is still selected by `config/pipeline.yaml`. **A passed unit-test suite does not certify the retrospective 25,135-study cohort or 31-study synthesis.**

## Manually labeled fixture reconciliation

The repository includes 20 synthetic, DOI-like screening examples in `tests/fixtures/golden_papers.csv`. Five intended labels do not match v1.0's deterministic outputs:

| Synthetic example | Hand-labeled | v1.0 actual | Candidate v1.1 criterion |
| --- | --- | --- | --- |
| Indoor pedestrian dead reckoning with magnetic observations | I-Core | I-Context | Explicit PDR within direct indoor-navigation context |
| Fall detection with explicit “no positioning” | E-Exclude | I-Context | Tighten activity-recognition exception to affirmative indoor positioning/navigation |
| BLE beacon hospital asset tracking and indoor location | I-Core | I-Context | Match indoor location with BLE/beacon sensing |
| VLC-based LED positioning | I-Core | I-Context | Match direct visible-light positioning |
| Activity-aware indoor location estimation | I-Core | I-Context | Recognize direct indoor location-estimation terminology |

`v1.1` introduces patterns to match these test expectations and retains the v1.0 dictionary for full historical transparency. The fixture uses synthetic examples and cannot establish error rates in real indexed bibliographic records.

## Before claiming full methodological reproduction

1. Reconstruct the exact 27,720 deduplicated records from the original dated retrievals, with the submitted exclusion criteria.
2. Run both versions on **the same fixed records**, record label-by-label changes, compare exclusions/retentions and era totals, and investigate all sample-level disagreements.
3. Conduct author-led case adjudication and document any corrections to actual original screening decisions. A revised dictionary that reassigns even one real record may affect the manuscript figures and statistics.
4. Preserve immutable v1.0 outputs and compare both full pipeline results with the manuscript.
5. Only adopt a revised scheme when the empirical impact is verified, with matched figure/table updates or an explicit correction disclosure.

Do **not** edit reported corpus counts or automatically change historical labels to make the synthetic fixture pass. Do not report a green test suite as independent reconstruction of a licensed search export.
