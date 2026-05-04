---
name: Coding-dictionary change proposal
about: Propose an edit to config/coding_dictionary.*.yaml
title: "[dict] "
labels: ["dictionary", "needs-review"]
---

## What pattern do you want to change?

> Quote the exact regex (or category) from the YAML and the line number.

## What is the defect?

> Explain why the current pattern misclassifies (false positive or false negative).
> Give 2–3 example titles + abstracts that the change would correctly classify.

## What is the proposed replacement?

> Quote the exact replacement regex.

## Expected impact

- [ ] Counts: I-Core ___ → ___ ; I-Context ___ → ___ ; E-Exclude ___ → ___
- [ ] Validation κ: ___ → ___ (if you have a re-run number)
- [ ] Risk of unintended exclusions: low / medium / high

## Have you run the test suite?

- [ ] `pytest -v` passes locally with the new regex
- [ ] `tests/fixtures/golden_papers.csv` updated if needed (with rationale)

## Version bump

By accepting this change, the dictionary version will move from `vX.Y` to
`vX.(Y+1)` and a CHANGELOG entry will be added.
