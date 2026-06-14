# ─────────────────────────────────────────────────────────
#  Telco Churn Prediction — Makefile
# ─────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
PYTHON        := python
PIP           := pip
VENV          := .venv
VENV_BIN      := $(VENV)/bin

.PHONY: help venv install install-dev lint format type-check test \
        pipeline-eda pipeline-base pipeline-arch serve clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ── Environment ───────────────────────────────────────────
venv:  ## Create virtual environment
	$(PYTHON) -m venv $(VENV)
	@echo "✓ venv created — activate with: source $(VENV)/bin/activate"

install: venv  ## Install production dependencies
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -e .

install-dev: install  ## Install dev + production dependencies
	$(VENV_BIN)/pip install -e ".[dev]"
	$(VENV_BIN)/pre-commit install

# ── Code Quality ──────────────────────────────────────────
lint:  ## Run ruff linter
	$(VENV_BIN)/ruff check src/ pipelines/ tests/

format:  ## Auto-format with ruff
	$(VENV_BIN)/ruff format src/ pipelines/ tests/
	$(VENV_BIN)/ruff check --fix src/ pipelines/ tests/

type-check:  ## Static type checking with mypy
	$(VENV_BIN)/mypy src/telco_churn/

# ── Testing ───────────────────────────────────────────────
test:  ## Run all tests with coverage
	$(VENV_BIN)/pytest tests/ -v --cov=src/telco_churn --cov-report=html

test-unit:  ## Run unit tests only
	$(VENV_BIN)/pytest tests/unit/ -v

test-integration:  ## Run integration tests only
	$(VENV_BIN)/pytest tests/integration/ -v

# ── Pipelines ─────────────────────────────────────────────
pipeline-eda:  ## Run EDA pipeline
	$(VENV_BIN)/python -m pipelines.eda.run_eda

pipeline-base:  ## Run base model pipeline
	$(VENV_BIN)/python -m pipelines.base_model.run_base_model

pipeline-arch:  ## Run full architecture pipeline (all stages)
	$(VENV_BIN)/python -m pipelines.architecture.run_architecture

pipeline-all: pipeline-eda pipeline-base pipeline-arch  ## Run all pipelines sequentially

# ── MLflow ────────────────────────────────────────────────
mlflow-ui:  ## Launch MLflow tracking UI
	$(VENV_BIN)/mlflow ui --backend-store-uri models/registry --host 0.0.0.0 --port 5000

# ── Serving ───────────────────────────────────────────────
serve:  ## Start FastAPI inference server
	$(VENV_BIN)/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ── Data ──────────────────────────────────────────────────
download-data:  ## Download raw data from Kaggle
	$(VENV_BIN)/python scripts/download_data.py

# ── Cleanup ───────────────────────────────────────────────
clean:  ## Remove build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name ".coverage" -delete
	@echo "✓ Clean complete"

clean-all: clean  ## Remove venv and all generated files
	rm -rf $(VENV) models/artifacts/* reports/figures/* reports/metrics/*
	@echo "✓ Full clean complete"