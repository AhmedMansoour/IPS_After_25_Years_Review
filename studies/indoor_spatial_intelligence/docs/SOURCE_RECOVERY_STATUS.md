# Recovery inventory for the indoor spatial intelligence review

This note records a search of the researcher's existing ChatGPT Library project folder **Indoor Spatial Intelligence**, compared against the submitted paper's Appendix Tables A.7–A.8. It documents research material that may support the public reproducibility package; **source existence does not establish that any study has been independently verified or coded**.

## Located source material

| Library file | Content observed | Next action |
| --- | --- | --- |
| `indoor_spatial_intelligence_frontier_24.csv` | 24 curated studies with citation keys, titles, publication years and methodological roles | Cross-link to the 31 Appendix references |
| `indoor_spatial_intelligence_frontier_24.bib` | Bibliography for the 24-study register | Check DOI/title consistency against final manuscript |
| `INDOOR~1(1).JSO` | Structured source-text extraction; JSON reports 22 papers with paragraph-level extraction | Locally audit full-text fidelity, don't redistribute full text |
| `INDOOR~1(1).BIB` | Companion bibliography for the structured extraction | Reconcile 22 extraction records |
| `A_Survey_on_Robot_Semantic_Navigation_Systems_for_(1).pdf` | Primary PDF for Alqobali et al. (2024), ref. [20] | Inspect locally and derive source-based coding |
| `Goal-Oriented_Visual_Semantic_Navigation_Using_Semantic_Knowledge_Graph_and_Transformer(1).pdf` | Primary PDF for Wang and Tian (2025), ref. [49] | Inspect locally and derive source-based coding |
| `ref_with_indoor_spatial_intelligence_frontier_24.bib` | Broader bibliography | Audit bibliographic identifiers and unique keys |
| `Figure_IPS_Research_Landscape.png` | Existing Figure 2-type visual | Locate the underlying quantitative plotting inputs |
| `new-main-ips_spatial-intelligence-figure.tex` | LaTeX/TikZ conceptual figure source | Compare with final figure and preserve if applicable |
| `Pasted text(...).txt` | Earlier methodology, introduction and section drafts | Version-match; never treat drafts as executed search logs |

## Verified bibliographic overlap

All 24 citations in the early CSV correspond to references in the final 31-study synthesis. In early register order, the final-paper numeric references are:

```
33, 5, 65, 45, 6, 9, 37, 39, 7, 47, 42, 46,
48, 43, 38, 54, 55, 8, 41, 19, 20, 49, 58, 40
```

The JSON contains **22 distinct structured paper extraction records**. The two early-register papers absent from JSON are:

- Alqobali et al. (2024), semantic navigation survey, manuscript [20] — PDF found separately.
- Wang and Tian (2025), goal-oriented visual semantic navigation, manuscript [49] — PDF found separately.

Thus, material corresponding to all 24 *early-list* studies was located (22 structured text extractions and two PDFs), subject to scientific validation.

## Seven later full-text studies not in the early 24-study register

These are present in the submitted 31-study appendix but not in the early 24-study CSV:

1. **[52]** Tao et al. (2024), *3D Active Metric-Semantic SLAM*, DOI 10.1109/LRA.2024.3363542.
2. **[34]** Mehan et al. (2024), *QueSTMaps: Queryable Semantic Topological Maps for 3D Scene Understanding*, DOI 10.1109/IROS58592.2024.10801814.
3. **[4]** Rosinol et al. (2020), *3D Dynamic Scene Graphs: Actionable Spatial Perception with Places, Objects, and Humans*, DOI 10.15607/RSS.2020.XVI.079.
4. **[50]** Lang et al. (2025), *SELM: From Efficient Autonomous Exploration to Long-Term Monitoring in Semantic Level*, DOI 10.1109/TCDS.2025.3531367.
5. **[51]** Cornejo et al. (2025), *Concept-Guided Exploration: Building Persistent, Actionable Scene Graphs*, DOI 10.3390/app152011084.
6. **[44]** Li et al. (2025), *Queryable 3D Scene Representation: A Multi-Modal Framework for Semantic Reasoning and Robotic Task Planning*, DOI 10.1145/3746027.3758177.
7. **[53]** Bajpai et al. (2025), *Uncertainty-Informed Active Perception for Open Vocabulary Object Goal Navigation*, DOI 10.1109/ECMR65884.2025.11162987.

Complete original full-text files for these seven were **not identified in the dedicated Library project folder**; the final paper's bibliography and Appendix describe them. Recover or verify the source publications before authoring their empirical evidence assessments.

## Missing original evidence artifacts

- Exact export/snapshot used for the 25,135-study retained metadata set, with permitted redistributable representation.
- Original **source-record-level** 48,955 -> 27,720 -> 25,135 deduplication/screening decisions.
- Original 176-record frontier screening IDs/decisions and numeric provenance of supplementary discoveries.
- Final 31-study human-authored evidence coding and source/page-level evidence anchors.
- Underlying data tables and scripts regenerating manuscript Figure 2 and other data-derived figures.
- Search log establishing the precise date of the frontier query and original query syntax.

A different repository workflow happens to report some of the same aggregate counts, but that is not sufficient to establish identical source queries or screening rules.

## Safe implementation order

1. Assemble a local, non-public source index from the 24-study CSV and JSON/PDF material; map all 31 sources by DOI and final reference number.
2. Locate/obtain and inspect the seven additional primary studies.
3. Complete a **source-verified** evidence matrix with page references and actual evaluator decisions. Never auto-fill missing observations as demonstrated.
4. Recover dated raw exports and decision logs; reconstruct the 176 and 25,135 sets from original records, or explicitly document limits.
5. Independently regenerate numerical figures/tables, compare exact values, and retain mismatch reports.
6. Publish only bibliographic metadata and human-authored derived tables for which sharing rights are confirmed. Avoid copying 22 source papers' paragraph text or third-party PDFs into public GitHub.
7. Archive a vetted release only after data rights, consistency, and CI checks pass.

All statuses here reflect **discovery**, not final verification or publication approval.
