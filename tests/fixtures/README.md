# Test fixtures

- **`golden_papers.csv`** — 20 hand-labeled papers spanning every screening
  outcome (I-Core, I-Context, E-Exclude with each exclusion reason). The
  test suite re-runs the screening on these papers on every commit; if a
  dictionary edit breaks any expected label, CI fails.
- **`dedup_cases.csv`** — 6 records covering the deduplication contract:
  same-DOI matches across sources, fuzzy-title matches with punctuation
  variants, missing-DOI title-only matches, and unrelated near-duplicates
  that must NOT be merged.

To add a new test case:

1. Append a row to the appropriate fixture with the expected outcome.
2. Run `pytest -v` locally.
3. If the test fails, decide: is the dictionary wrong (fix it and bump
   version), or is the fixture row wrong (fix the fixture)?
