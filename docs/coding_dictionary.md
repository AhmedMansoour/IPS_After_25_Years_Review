# Coding Dictionary — Human-Readable Walkthrough

The authoritative dictionary file is
[`config/coding_dictionary.v1.0.yaml`](../config/coding_dictionary.v1.0.yaml).
This document is a plain-language companion that explains what each
section of the dictionary does and why each pattern is there. Anyone
proposing a change should read this first.

## Versioning rule

Any edit to a regex, a category, or an era boundary **MUST** bump
the `version:` field in the YAML and add an entry in
[`CHANGELOG.md`](../CHANGELOG.md) with:

1. The exact diff.
2. The rationale (what defect / opportunity motivated the change).
3. The impact on the I-Core / I-Context / E-Exclude counts.

Never edit the dictionary in place without bumping the version. Outputs
generated under different dictionary versions are **not comparable**.

## Section 1 — `non_scholarly_document_types`

Set of `Document_Type` strings that are excluded immediately. These are
non-research artifacts: erratum, retracted paper, editorial, letter,
short survey, note. Conference papers and journal articles are NOT in
this list.

## Section 2 — `safeguard_categories`

Seven categories that overlap technically with IPS but are NOT IPS unless
the paper explicitly targets indoor positioning. Each category has:

- `exclude` — pattern that flags the record as out-of-scope.
- `safeguard` — pattern that *rescues* the record back into screening
  if it also mentions IPS-relevant terminology.

A record is excluded **only if** `exclude` matches AND `safeguard` does
NOT match.

| Category | Why it overlaps with IPS | Why we still need to exclude it |
|---|---|---|
| `robotics_slam` | Many SLAM papers use indoor sensors | Most are pure robotics, not pedestrian/asset positioning |
| `outdoor_gnss` | GNSS is positioning, but outdoor | Out of scope unless seamless indoor-outdoor |
| `channel_propagation` | Channel models inform fingerprinting | Pure PHY-layer work doesn't produce a position |
| `place_scene_recognition` | Image retrieval can be a localization aid | Most place-recognition papers don't output coordinates |
| `activity_recognition` | Activity sensors often coincide with positioning | Activity ≠ position |
| `networking_comms` | Throughput / handover work involves WiFi too | These are network-engineering papers, not IPS |
| `outdoor_tracking` | Vehicle tracking shares vocabulary with asset tracking | Out of scope unless indoor parking / underground |

## Section 3 — `i_core_patterns`

Eleven patterns that are **strong, direct evidence** the paper is
explicitly an IPS paper:

- Explicit phrases: "indoor positioning", "indoor localization", "indoor
  locating", "indoor location system".
- Indoor + navigation/tracking with position/localization within 30 chars.
- The acronym IPS combined with indoor/position/localization context.
- Fingerprinting combined with indoor/positioning/WiFi/RSSI/CSI/BLE.
- Radio map / site survey.
- Floor / building detection / classification / identification.
- Seamless indoor-outdoor.
- UWB / Ultra-wideband within 30 chars of position/localization/ranging.
- RSSI / RSS / CSI within 30 chars of position/localization/fingerprint.

A match here lets the paper bypass the I-Context check.

## Section 4 — `i_context_patterns`

Sixteen broader patterns covering papers that are **IPS-enabling**
without necessarily being IPS-as-stated-aim:

- Sensing technology (WiFi/BLE/UWB/...) within 80 chars of
  position/localization/navigation/tracking/ranging.
- The same in reverse direction.
- IMU / PDR / inertial / step detection + positioning / navigation / indoor.
- SLAM combined with indoor / positioning / localization.
- Any fingerprinting mention.
- Radio map / site survey / map matching / floor plan.
- Crowdsourcing combined with positioning.
- Benchmark / dataset combined with positioning / indoor.
- Privacy / security combined with positioning.
- Fusion / multimodal combined with positioning.
- Deployment / calibration / maintenance combined with positioning.
- Semantic / context-aware combined with positioning.
- Machine / deep learning combined with positioning / fingerprint / indoor.
- Indoor combined with positioning / localization / navigation / tracking
  / mapping / sensing / monitoring.
- Trilateration / triangulation / ranging combined with positioning.
- Path loss / channel / propagation combined with positioning (these
  passed the Step-2 safeguard precisely because they mention positioning).

## Section 5 — `priority_tiers`

Tiering is applied **only to retained records** (I-Core or I-Context):

- **T1** if the document is a Review (but not "Conference review"), OR
  has ≥100 citations, OR matches a high-impact keyword
  (survey/review/benchmark/dataset/data paper/evaluation framework/competition).
- **T2** if it has ≥20 citations OR Document_Type ∈ {Article, J,
  Non-Conference}.
- **T3** otherwise.

T1 records are treated as anchor papers for the close-synthesis subset.

## Section 6 — `sensing_sources`, `paradigms`, `deployment_indicators`

These are multi-label assignments. A single paper can carry multiple
labels (e.g., a Wi-Fi+BLE fusion paper gets both `Wi-Fi` and `BLE`).
The label patterns are intentionally narrower than the I-Context
patterns to reduce false positives in section-level statistics.

## Section 7 — `eras`

Year-bin definitions for Section III:

- Era1 (Foundations): year ≤ 2008.
- Era2 (Smartphone Fingerprinting): 2009–2014.
- Era3 (Multimodal Fusion): 2015–2019.
- Era4 (Deep Learning & Deployment): year ≥ 2020.

The `theme_pattern` for each era is **diagnostic only** — it does not
gate the era assignment, which is purely year-based. The theme pattern
is used in the optional `Sec_III_ThemeMatch` column for sanity checks.

## How AI helped, and how it did not

Each regex above was first **drafted** with assistance from Anthropic
Claude and OpenAI ChatGPT — typically by asking the LLM to propose
keyword variants for a given concept, then editing the proposal down.
Every regex was then **tested**, **edited**, and **approved** by the
authors against representative examples drawn from the corpus.

The dictionary, as a whole, is a human-authored artifact. The pipeline
that uses it does NOT call any LLM at runtime.
