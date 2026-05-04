# IPS Review Reproducibility Package

> **Reproducibility artifact for**
> *"Indoor Positioning Systems After 25 Years: A Survey of Wireless, Mobile, and Networked Localization from Accuracy to Deployment Readiness"*
> by **Ahmed Mansour**.
> Submitted to *IEEE Communications Surveys & Tutorials* (COMST).

[![CI](https://github.com/AhmedMansoour/IPS_After_25_Years_Review/actions/workflows/ci.yml/badge.svg)](https://github.com/AhmedMansoour/IPS_After_25_Years_Review/actions)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Coding dictionary v1.0](https://img.shields.io/badge/dictionary-v1.0-brightgreen.svg)](config/coding_dictionary.v1.0.yaml)

---

## What this is

This repository contains **everything needed to reproduce, audit, and extend** the
corpus statistics, screening labels, section mappings, validation results, and
figures in the survey above.

It is *not* a generic IPS toolkit. It is the exact pipeline that produced the
**27,720-record corpus**, the **I-Core / I-Context / E-Exclude** screening
labels, the **four-era taxonomy**, and the **525-paper full-text validation
panel** described in Section II of the manuscript.

## Why this exists

Systematic reviews live or die by reproducibility. Anyone — reviewer, reader,
or future researcher — should be able to:

1. Take the same raw Scopus / Web of Science / IEEE *Xplore* exports.
2. Run a single command.
3. Get bit-identical screening labels, section mappings, and figure data.
4. Inspect the **coding dictionary as data** (YAML), not buried in code.
5. Re-run the **κ validation** against their own human-coded sample.
6. Diff our coding dictionary against an alternative and quantify the
   sensitivity of our reported numbers.

That is what this package delivers.

## Five-second mental model

```
raw exports ──► harmonize ──► dedup ──► screen ──► classify ──► figures
  (Scopus,      (unified      (union-   (regex     (multi-      (PDFs,
   WoS, IEEE)    schema)       find on   over       label per    LaTeX
                               title +   T+A+K)     section)     tables)
                               DOI)
                                   │
                                   ▼
                         coding_dictionary.yaml
                       (LLM-drafted, human-finalized)
                                   │
                                   ▼
                       stratified human validation
                          (Cohen's κ, % agreement)
```

**No record-level LLM inference is performed at any stage of the corpus
pipeline.** The full disclosure of where AI was and was not used is in
[`docs/ai_disclosure.md`](docs/ai_disclosure.md).

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/AhmedMansoour/IPS_After_25_Years_Review.git
cd IPS_After_25_Years_Review
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# 2. Drop your raw exports into:
#    data/raw/scopus/ ─ scopus_*.csv
#    data/raw/wos/    ─ savedrecs*.xls
#    data/raw/ieee/   ─ *.csv
#    (or download our archived snapshot from Zenodo: see data/README.md)

# 3. Run the entire pipeline
make all

# 4. Run validation against the bundled human-coded sample
make validate

# 5. Regenerate paper figures and tables
make figures
```

That's it. Outputs land in `data/processed/` and `outputs/`.

## Repository layout

```
ips-review-reproducibility/
├── README.md                     ← you are here
├── LICENSE / LICENSE-DATA        ← MIT (code) + CC-BY-4.0 (derived data)
├── CITATION.cff                  ← cite this software via GitHub button
├── pyproject.toml                ← package metadata + deps
├── Makefile                      ← one-command pipeline
├── .github/                      ← CI, issue templates, release automation
├── config/                       ← ★ coding dictionary as YAML (versioned)
│   ├── coding_dictionary.v1.0.yaml
│   ├── era_taxonomy.yaml
│   ├── source_mapping.yaml
│   └── pipeline.yaml
├── src/ips_review/               ← installable Python package
│   ├── io/                       ← Scopus / WoS / IEEE loaders
│   ├── harmonize.py              ← unified schema
│   ├── dedup.py                  ← union-find dedup
│   ├── screen.py                 ← three-tier rule-based screening
│   ├── classify.py               ← section-level multi-label mapping
│   ├── validate.py               ← Cohen's κ + % agreement
│   ├── sampling.py               ← stratified validation sampling
│   ├── figures/                  ← paper figures
│   └── cli.py                    ← `ips-review` command
├── tests/                        ← pytest, golden cases, regex fixtures
├── data/
│   ├── raw/                      ← drop your exports here (gitignored / LFS)
│   ├── interim/                  ← deduplicated unified corpus
│   ├── processed/                ← screened + section-mapped corpus
│   └── validation/               ← human-coded sample + κ reports
├── outputs/figures, tables, reports
├── notebooks/                    ← exploratory + audit notebooks
├── scripts/                      ← convenience scripts (compute_kappa, etc.)
└── docs/                         ← methodology, dictionary, AI disclosure,
                                    validation protocol, architecture
```

## What makes this package unusual

- **Coding dictionary as data, not code.** Every regex, every safeguard, every
  era boundary lives in [`config/coding_dictionary.v1.0.yaml`](config/coding_dictionary.v1.0.yaml).
  Reviewers can read it, diff it, and propose changes via PR without touching
  Python.
- **Versioned dictionary.** Dictionary changes bump the version
  (`v1.0` → `v1.1`); the pipeline records which version produced each output
  CSV in its provenance header.
- **Built-in validation.** `ips-review validate --sample data/validation/sample.csv`
  computes Cohen's κ and per-label agreement against any human-coded sample
  you provide. The protocol for drawing a stratified sample is in
  [`docs/validation_protocol.md`](docs/validation_protocol.md).
- **Sensitivity analysis.** `notebooks/03_sensitivity_analysis.ipynb` swaps in
  alternative dictionary versions and reports how the I-Core / I-Context /
  E-Exclude counts shift. Lets reviewers test "what if you used a stricter
  I-Core definition?" in two minutes.
- **Honest AI disclosure.** [`docs/ai_disclosure.md`](docs/ai_disclosure.md)
  states exactly where Claude and ChatGPT were and were not used, model
  versions, access dates, and a per-stage table.
- **Full provenance.** Every output CSV carries a header comment:
  dictionary version, code git SHA, input file SHA-256s, run timestamp.
- **CI-checked.** Every commit runs the regex fixtures and a smoke test on
  a 50-paper synthetic corpus to catch dictionary regressions.

## Citing this work

If you use this package, please cite **both** the paper and the software:

**Paper (BibTeX):**
```bibtex
@article{mansour2026ips,
  title   = {Indoor Positioning Systems After 25 Years: A Survey of Wireless, Mobile, and Networked Localization from Accuracy to Deployment Readiness},
  author  = {Mansour, Ahmed},
  journal = {IEEE Communications Surveys \& Tutorials},
  year    = {2026},
  note    = {Under review}
}
```

**Software (BibTeX):**
```bibtex
@software{mansour2026ipssoftware,
  title   = {IPS Review Reproducibility Package},
  author  = {Mansour, Ahmed},
  year    = {2026},
  doi     = {10.5281/zenodo.XXXXXXX},
  url     = {https://github.com/AhmedMansoour/IPS_After_25_Years_Review},
  version = {1.0.0}
}
```

A machine-readable [`CITATION.cff`](CITATION.cff) is provided so GitHub's
"Cite this repository" button works out of the box.

## Documentation index

| Document | What it covers |
|---|---|
| [`docs/methodology.md`](docs/methodology.md) | Mirrors Section II of the paper. Authoritative description of the pipeline. |
| [`docs/coding_dictionary.md`](docs/coding_dictionary.md) | Human-readable walkthrough of every regex group with rationale. |
| [`docs/data_dictionary.md`](docs/data_dictionary.md) | Schema of every CSV column, every label value. |
| [`docs/reproducibility.md`](docs/reproducibility.md) | Step-by-step: install → run → verify against expected hashes. |
| [`docs/validation_protocol.md`](docs/validation_protocol.md) | How to draw a stratified sample and compute κ against it. |
| [`docs/ai_disclosure.md`](docs/ai_disclosure.md) | Per-stage AI-use disclosure (model, version, role). |
| [`docs/architecture.md`](docs/architecture.md) | Component diagram + data flow. |

## Contributing

Bug reports, dictionary refinements, and new validation samples are welcome.
See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the workflow. Dictionary changes
follow a stricter review process documented there.

## Licensing

- **Code** (everything in `src/`, `tests/`, `scripts/`, configs): MIT — see [`LICENSE`](LICENSE).
- **Derived data** (everything in `data/processed/`, `data/validation/`,
  `outputs/`): Creative Commons Attribution 4.0 — see [`LICENSE-DATA`](LICENSE-DATA).
- **Raw bibliographic exports** in `data/raw/` are bundled in this repository
  for transparency and reproducibility. They are subject to the terms of
  Scopus (Elsevier), Web of Science (Clarivate), and IEEE *Xplore* respectively;
  redistribution may be restricted by those licenses. See [`data/README.md`](data/README.md).

## Acknowledgments

The coding dictionary in this repository was drafted with assistance from
Anthropic Claude and OpenAI ChatGPT, and was finalized and approved by the
authors. See [`docs/ai_disclosure.md`](docs/ai_disclosure.md) for the full
disclosure.
