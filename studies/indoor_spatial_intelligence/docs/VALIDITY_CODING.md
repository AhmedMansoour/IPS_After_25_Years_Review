# Source-verifiable coding protocol

Purpose: support a critical, traceable analysis of interfaces among spatial-state estimation, indoor world representation, task-relevant reasoning, physical action verification, and updating. This is **not** an experimental validation of the proposed validity framework.

## Controlled status vocabulary

Use one of:
- `demonstrated`: explicit implemented mechanism and evaluation in the cited primary source.
- `partial`: relevant component or evidence reported, but only part of the stated capability verified.
- `assumed`: supplied by simulation, oracle, prebuilt map, accurate external pose, or other untested prerequisite.
- `not_evaluated`: mechanism asserted or implemented but no relevant evaluation found.
- `not_reported`: no sufficient primary-source basis; avoid interpreting absence of reporting as a tested failure.

For each dimension record a **direct page, section, figure, table, or stable full-text locator**, plus a short claim, supporting quotation limited to relevant text rights, and a distinct judgement of the reviewer. Do not overwrite study claims with inferred performance.

## Coding dimensions

1. `grounding_status`: physical observations, pose origin (measured/estimated/assumed), registration and frame alignment.
2. `representation_status`: persistent or ephemeral geometry, rooms, object identity, relations, topology and semantics.
3. `reasoning_status`: grounded queries, spatial inference, task-level planning, language alignment and evaluation.
4. `uncertainty_status`: confidence/probability/covariance and cross-stage uncertainty handling.
5. `provenance_status`: evidence IDs, source and timestamp attribution, map freshness and uncertainty lineage.
6. `action_verification_status`: feasibility/safety checks, action rejection/deferral and low-level execution.
7. `update_status`: change detection, map/model revision, correction, identity continuity and rollback.

Use `verified_by` to name the scientific coder(s); `source_locator` identifies the primary source DOI/URL or locally auditable citation. Disagreements must be logged and reconciled, not resolved by an automatic model label.

## Interpretation

A missing component can be a limitation of the *evidence*, not an inherent defect of a system: report this distinction. The published 31-study set is purposive and cannot be used to infer field-wide prevalence.

## Analysis to manuscript crosswalk

- Physical foundation and representations: Section 4 and Appendix A.
- Spatial validity and claim types: Section 5, Table 5 and illustrative equations.
- Interpretation, limitations and research agenda: Section 6.

The 31-source index was transcribed from the author's submitted manuscript and is NOT a verified empirical coding matrix. Do not mark it as complete until scientific coders inspect each original study.
