# Indoor Spatial Intelligence Review — Reproducibility Repository

**Manuscript:** *From Indoor Positioning to Indoor Spatial Intelligence: A Field-Evolution Review*  

[Open the dedicated reproducibility package](studies/indoor_spatial_intelligence/README.md) · [Source provenance](studies/indoor_spatial_intelligence/docs/PROVENANCE.md) · [Validity coding](studies/indoor_spatial_intelligence/docs/VALIDITY_CODING.md) · [Licensing and data audit](studies/indoor_spatial_intelligence/docs/LICENSING_AUDIT.md)

## What the study reports

The submitted manuscript uses a two-part evidence design: metadata analysis of indoor positioning research published in 2000–2025, and a purposive 31-study full-text synthesis of physical grounding, structured indoor world representations, spatial reasoning, planning, action, and updating.

| Manuscript-reported stage | Number |
| --- | ---: |
| Initial database retrieval | 48,955 |
| Removed duplicate/overlapping records | 21,235 |
| Unique records | 27,720 |
| Excluded from longitudinal analysis | 2,585 |
| Retained for longitudinal analysis | 25,135 |
| Dedicated frontier query records | 176 |
| Selected full-text studies (including supplementary discovery) | 31 |

**Integrity notice:** Figures above are *transcribed from the submitted manuscript*. The public repository must not be represented as fully reproducing those findings until the original source snapshots, screening decisions, coding records, and scripts have been independently reconciled. Read the [verification status](studies/indoor_spatial_intelligence/README.md).

## Screening-rule versions

The default metadata pipeline uses the frozen `coding_dictionary.v1.0.yaml`. A separately versioned `coding_dictionary.v1.1.yaml` is available for validation of manually labeled examples. Its full-corpus impact has not been established; it must **not** be substituted for the original screening rules when reproducing reported manuscript counts. See the [screening audit](studies/indoor_spatial_intelligence/docs/SCREENING_RULE_AUDIT.md).

## How to examine the currently available evidence scaffold

```bash
git clone https://github.com/AhmedMansoour/IPS_After_25_Years_Review.git
cd IPS_After_25_Years_Review
python studies/indoor_spatial_intelligence/scripts/verify.py --mode manifest
python -m unittest discover -s studies/indoor_spatial_intelligence/tests -v
```

These checks validate manuscript-to-repository consistency only; they do **not** prove empirical reproduction of 25,135 records.

## Software and data transparency

The root-level `src/ips_review/` package is existing, potentially reusable code, and must be checked against the actual research search boundaries and coding dictionary before its outputs are treated as results of this manuscript. Previous configuration choices are **not** automatically valid for this study.

Raw vendor database exports are already present in historical repository commits and some in the currently tracked tree; their redistribution rights have **not** yet been cleared. They must not be included in a new archive or release until the rights audit is complete. See [LICENSING_AUDIT.md](studies/indoor_spatial_intelligence/docs/LICENSING_AUDIT.md). Do not publish restricted inputs without a completed rights review.

## Citation

Cite the accompanying review by its title and author list; no publication DOI is implied. A permanent software archive identifier should be added only once one has actually been issued.
