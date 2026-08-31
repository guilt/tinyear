PYTHON ?= python3
.DEFAULT_GOAL := help
.PHONY: help install test tests examples fixtures clean

help: ## Show this help
	@$(PYTHON) -c "import re; f=open('Makefile').read(); [print('  {:<24s} {}'.format(*m.groups())) for m in re.finditer(r'^([a-z_-]+):.*?## (.+)', f, re.M)]"

install:
	$(PYTHON) -m pip install -e ".[dev]"

fixtures:
	$(PYTHON) examples/make_sample.py

test: tests

tests: fixtures
	$(PYTHON) -m pytest --cov-branch --cov=tinyear --cov-report=term-missing --cov-report=html tinyear/tests

examples: fixtures
	mkdir -p examples/out
	$(PYTHON) -m tinyear ingest examples/sample.wav --out examples/out --transcript "set a timer"
	$(PYTHON) -m tinyear ingest examples/sample.wav --out examples/out --stem silent
	@grep -H transcript_ok examples/out/*.ear.md

clean:
	rm -rf dist build *.egg-info .pytest_cache .coverage htmlcov examples/out examples/sample.wav
