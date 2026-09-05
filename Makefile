PYTHON ?= python3
TINYHOWL ?= ../tinyhowl
export TINYHOWL_ROOT := $(TINYHOWL)
.DEFAULT_GOAL := help
.PHONY: help install test tests unit-tests coverage examples fixtures corpus pipe clean format lint

help: ## Show this help
	@$(PYTHON) -c "import re; f=open('Makefile').read(); [print('  {:<24s} {}'.format(*m.groups())) for m in re.finditer(r'^([a-z_-]+):.*?## (.+)', f, re.M)]"

install: ## Editable install with dev extras
	$(PYTHON) -m pip install -e ".[dev]"

fixtures: ## Write examples/sample.wav
	PYTHONPATH=. $(PYTHON) examples/make_sample.py

corpus: ## Offline 6-vowel + silence corpus
	PYTHONPATH=. $(PYTHON) examples/make_corpus.py

test: tests

tests: fixtures ## Pytest with branch coverage (Howl is a test dep)
	PYTHONPATH=$(TINYHOWL):. TINYHOWL_ROOT=$(TINYHOWL) $(PYTHON) -m pytest --cov-branch --cov=tinyear --cov-report=term-missing --cov-report=html tinyear/tests

unit-tests: tests ## Alias

coverage: tests ## Alias

examples: fixtures corpus ## Ingest sample + corpus
	mkdir -p examples/out
	PYTHONPATH=. $(PYTHON) -m tinyear ingest examples/sample.wav --out examples/out --transcript "set a timer"
	PYTHONPATH=. $(PYTHON) -m tinyear ingest examples/sample.wav --out examples/out --stem silent
	@grep -H transcript_ok examples/out/*.ear.md examples/out/corpus/*.ear.md || true

pipe: ## Howl stdout → Ear stdin (needs sibling ../tinyhowl)
	PYTHONPATH=$(TINYHOWL):. TINYHOWL_ROOT=$(TINYHOWL) $(PYTHON) examples/howl_pipe.py

format: ## Ruff format
	-$(PYTHON) -m ruff format tinyear examples

lint: format
	-$(PYTHON) -m ruff check tinyear

clean: ## Remove artifacts
	rm -rf dist build *.egg-info .pytest_cache .coverage htmlcov examples/out examples/sample.wav
