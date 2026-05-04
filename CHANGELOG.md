# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-05-05

### Added
- Initial public release accompanying the COMST submission of
  "Twenty-Five Years of Indoor Positioning Systems: A Systematic Review (2000–2026)".
- Coding dictionary `config/coding_dictionary.v1.0.yaml`:
  - 7 out-of-scope safeguard categories
  - 11 I-Core regex patterns
  - 16 I-Context regex patterns
  - 11 sensing-source labels
  - 6 paradigm labels
  - 5 deployment-readiness labels
  - 4 era definitions
- Pipeline stages: `harmonize`, `dedup`, `screen`, `classify`, `validate`,
  `sample`, `provenance`, `run-all`.
- Stratified sampling utility (`ips_review.sampling`).
- Cohen's κ + per-label confusion matrix validation reporter
  (`ips_review.validate`).
- Provenance-stamped output CSVs.
- 20-paper golden fixture for screening regression tests.
- 6-row dedup fixture for deduplication contract tests.
- GitHub Actions CI: tests on Linux/macOS/Windows × Python 3.10/3.11/3.12,
  ruff lint, dictionary YAML compile check, monthly synthetic-corpus
  end-to-end smoke test.
- Documentation: methodology, coding-dictionary walkthrough, data
  dictionary, reproducibility guide, validation protocol, AI disclosure,
  architecture diagram, search strategy.
