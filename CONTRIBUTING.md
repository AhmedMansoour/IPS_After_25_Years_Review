# Contributing

Thanks for considering a contribution. This project is the
reproducibility artifact of a published systematic review, so changes
that affect reported numbers go through extra scrutiny.

## Three kinds of changes

### 1. Bug fixes (loaders, dedup, validation utilities)

Standard PR workflow:

```bash
git checkout -b fix/<short-description>
# edit
pytest -v
ruff check src tests
git commit -m "fix: <short message>"
gh pr create
```

CI must pass before merge.

### 2. Coding-dictionary changes

Dictionary edits are the most consequential changes because they alter
the labels of every record in the corpus. Required workflow:

1. Open an issue using the `dictionary_change.md` template **first**.
   Discuss the rationale before opening a PR.
2. In the PR:
   - Edit `config/coding_dictionary.vX.Y.yaml` (do **not** rename in place).
   - **Bump the `version:` field** to the next minor (e.g., `1.0` → `1.1`).
   - Save the new version under a new filename:
     `config/coding_dictionary.v1.1.yaml`.
   - Add an entry to `CHANGELOG.md` describing the change, the
     rationale, and the impact on I-Core / I-Context / E-Exclude counts.
   - Update `tests/fixtures/golden_papers.csv` with any new test cases
     that justify the change.
   - Re-run `make all` against the production corpus and update
     `config/expected_hashes.txt` if the outputs change.
   - Re-run validation and update the κ in `outputs/reports/`.
3. Two-author review required for dictionary changes.

### 3. New features (figures, validation utilities, loaders)

Standard PR workflow. New dependencies need strong justification.

## Local development setup

```bash
git clone https://github.com/AhmedMansoour/IPS_After_25_Years_Review.git
cd IPS_After_25_Years_Review
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,figures]"
pre-commit install
pytest -v
```

## Style

- Code is formatted with `ruff format`.
- Lints are enforced by `ruff check`.
- Public functions have one-line docstrings; modules have a paragraph
  describing their stage in the pipeline.
- No new dependency without a one-paragraph rationale in the PR body.

## Reporting validation findings

If you ran the validation protocol against a new sample and want to
share the result, open an issue with:

- Sample size, stratification scheme, seed.
- Number of human reviewers, adjudication rule.
- Cohen's κ overall and per label.
- Confusion matrix.
- Top 3 disagreement patterns (anonymized titles allowed).

We will consider including notable validation results in the next
release of the repository.
