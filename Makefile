.PHONY: help install install-dev test lint format clean all harmonize dedup screen classify validate figures sample provenance check-reproducibility

help:
	@echo "IPS Review Reproducibility — Makefile targets"
	@echo ""
	@echo "  make install        Install runtime dependencies"
	@echo "  make install-dev    Install runtime + dev dependencies"
	@echo "  make all            Run full pipeline: harmonize -> dedup -> screen -> classify"
	@echo "  make harmonize      Stage 1: load + harmonize Scopus/WoS/IEEE"
	@echo "  make dedup          Stage 2: cross-database deduplication"
	@echo "  make screen         Stage 3: rule-based three-tier screening"
	@echo "  make classify       Stage 4: section-level multi-label mapping"
	@echo "  make validate       Compute Cohen's kappa against human-coded sample"
	@echo "  make sample         Draw a stratified validation sample"
	@echo "  make figures        Regenerate all paper figures"
	@echo "  make provenance     Print provenance metadata for all output CSVs"
	@echo "  make test           Run pytest suite"
	@echo "  make lint           Run ruff linter"
	@echo "  make format         Auto-format with ruff"
	@echo "  make clean          Remove generated artifacts"
	@echo "  make check-reproducibility  Verify outputs match expected SHA-256 hashes"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,figures]"
	pre-commit install || true

all: harmonize dedup screen classify
	@echo ""
	@echo "Pipeline complete. Outputs in data/processed/"

harmonize:
	ips-review harmonize \
		--scopus-dir data/raw/scopus \
		--wos-dir    data/raw/wos \
		--ieee-dir   data/raw/ieee \
		--output     data/interim/harmonized.csv

dedup: data/interim/harmonized.csv
	ips-review dedup \
		--input  data/interim/harmonized.csv \
		--output data/interim/unique_corpus.csv

screen: data/interim/unique_corpus.csv
	ips-review screen \
		--input      data/interim/unique_corpus.csv \
		--dictionary config/coding_dictionary.v1.0.yaml \
		--output     data/processed/corpus_screened.csv

classify: data/processed/corpus_screened.csv
	ips-review classify \
		--input      data/processed/corpus_screened.csv \
		--dictionary config/coding_dictionary.v1.0.yaml \
		--output     data/processed/section_mapping.csv

validate:
	ips-review validate \
		--rule-based  data/processed/corpus_screened.csv \
		--human-coded data/validation/sample_v1.0.csv \
		--report      outputs/reports/validation_report.md

sample:
	ips-review sample \
		--input      data/processed/corpus_screened.csv \
		--n          400 \
		--strata     Screen_Label,Sec_III_Era \
		--seed       20260505 \
		--output     data/validation/sample_template.csv

figures:
	python -m ips_review.figures.era_evolution
	python -m ips_review.figures.sensing_modality
	python -m ips_review.figures.deployment_matrix

provenance:
	ips-review provenance --dir data/processed

test:
	pytest -v --cov=ips_review --cov-report=term-missing

lint:
	ruff check src tests

format:
	ruff format src tests
	ruff check --fix src tests

clean:
	rm -rf data/interim/*.csv data/processed/*.csv outputs/figures/* outputs/tables/* outputs/reports/*
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

check-reproducibility:
	@echo "Verifying output hashes against config/expected_hashes.txt ..."
	@python scripts/verify_hashes.py
