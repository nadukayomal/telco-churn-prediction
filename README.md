# 📡 Telco Customer Churn Prediction

> End-to-end ML system for predicting telecom customer churn — built to industrial standards with modular pipelines, experiment tracking, explainability, and a REST API serving layer.

[CI](https://github.com/your-org/telco-churn-prediction/actions)
[Python 3.10+](https://www.python.org/)
[Code style: ruff](https://github.com/astral-sh/ruff)
[MLflow](https://mlflow.org/)
[License: MIT](LICENSE)

---

## Table of contents

- [Business context](#business-context)
- [Dataset](#dataset)
- [Project architecture](#project-architecture)
- [Project structure](#project-structure)
- [Pipelines](#pipelines)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Experiment tracking](#experiment-tracking)
- [API serving](#api-serving)
- [Development workflow](#development-workflow)
- [Results](#results)
- [Roadmap](#roadmap)

---

## Business context

Customer acquisition in telecoms costs **5–10× more** than retention. A model that flags at-risk subscribers before they cancel — even with a 10% save rate — recovers significant annual revenue.

This project builds a production-grade churn prediction system that:

- Assigns a churn-risk probability score to each customer
- Explains *why* a customer is flagged (SHAP feature attribution)
- Exposes predictions through a REST API consumable by CRM systems
- Tracks every experiment reproducibly via MLflow

---

## Dataset

**Source:** [IBM Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/data)


| Property    | Value                                                               |
| ----------- | ------------------------------------------------------------------- |
| Records     | 7,043 customers                                                     |
| Features    | 21 (demographics, services, billing)                                |
| Target      | `Churn` — Yes / No                                                  |
| Churn rate  | ~26.5% (class imbalance present)                                    |
| Known issue | `TotalCharges` stored as string with blank values for new customers |


Feature groups:

- **Demographics** — `gender`, `SeniorCitizen`, `Partner`, `Dependents`
- **Services** — `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
- **Account** — `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`

---

## Project architecture

```
                 ┌─────────────────────────────────────────┐
                 │            Raw CSV / Kaggle API          │
                 └──────────────────┬──────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │       Pipeline 1: EDA         │
                    │  • data quality audit         │
                    │  • distribution analysis      │
                    │  • correlation & target study │
                    │  → reports/figures/           │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │    Pipeline 2: Base Model     │
                    │  • preprocessing pipeline     │
                    │  • SMOTE / class weights      │
                    │  • LR / RF / XGBoost / LGBM  │
                    │  • CV + threshold tuning      │
                    │  → MLflow experiment run      │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │  Pipeline 3: Architecture     │
                    │  • best model selection       │
                    │  • SHAP explainability        │
                    │  • model registration         │
                    │  • artefact serialisation     │
                    │  → models/artifacts/          │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │      FastAPI Serving Layer     │
                    │  POST /predict                 │
                    │  GET  /health                  │
                    │  GET  /model/info              │
                    └────────────────────────────────┘
```

---

## Project structure

```
telco-churn-prediction/
│
├── architecture_pipeline/           # Pipeline 3: Model selection & serving
│   └── [architecture code]
│
├── data/                            # Data storage & versioning
│   ├── raw/                         # Original Telco Customer Churn CSV (never modified)
│   ├── processed_eda/               # Processed data from EDA pipeline
│   └── processed_base_model/        # Processed data from base model pipeline
│
├── notebooks/                       # Jupyter notebooks for experimentation
│   ├── eda/                         # Exploratory Data Analysis notebooks
│   └── base_model/                  # Base model development & prototyping
│
├── model/                           # Trained model artifacts
│   └── [serialized models]
│
├── artifacts/                       # Pipeline outputs & artifacts
│   └── [figures, reports, metrics]
│
├── config/                          # Configuration files
│   ├── config.yaml                  # Paths, splits, evaluation settings
│   ├── model_params.yaml            # Hyperparameter search grids
│   └── logging.yaml                 # Logging configuration
│
├── src/                             # Production-grade Python package
│   ├── data/
│   │   ├── ingest.py                # Load & validate raw data
│   │   ├── validate.py              # Data quality checks
│   │   └── preprocess.py            # Transform & prepare data
│   ├── features/
│   │   ├── build_features.py        # Feature engineering orchestrator
│   │   ├── encoders.py              # Custom transformers
│   │   └── scalers.py               # Scaler selection logic
│   ├── models/
│   │   ├── train.py                 # Model training & cross-validation
│   │   ├── predict.py               # Batch & single inference
│   │   └── registry.py              # MLflow model helpers
│   ├── evaluation/
│   │   ├── metrics.py               # Performance metrics & threshold tuning
│   │   └── explainability.py        # SHAP explanations & visualization
│   ├── utils/
│   │   ├── logger.py                # Logging setup
│   │   └── io.py                    # File I/O helpers (YAML, Parquet, Joblib)
│   └── visualization/
│       └── plots.py                 # Reusable matplotlib / seaborn figures
│
├── Makefile                         # Developer commands
├── pyproject.toml                   # Project metadata & dependencies
├── README.md                        # This file
└── .gitignore                       # Git ignore patterns
```

---

## Pipelines

### Pipeline 1 — EDA

**Entry point:** `make pipeline-eda` or `python -m pipelines.eda.run_eda`

What it does:

1. Loads raw CSV and runs schema validation
2. Audits missing values, dtypes, and the `TotalCharges` string bug
3. Generates distribution plots for all features
4. Produces churn-rate breakdown by feature group
5. Saves a correlation heatmap and target-vs-feature summaries
6. Outputs all figures to `reports/figures/eda/`

### Pipeline 2 — Base Model

**Entry point:** `make pipeline-base` or `python -m pipelines.base_model.run_base_model`

What it does:

1. Loads processed data splits
2. Builds a full sklearn `Pipeline` (imputer → encoder → scaler)
3. Handles class imbalance via SMOTE + `class_weight='balanced'`
4. Runs 5-fold stratified CV for each model: Logistic Regression, Random Forest, XGBoost, LightGBM
5. Logs all metrics and parameters to MLflow
6. Saves a CV comparison table to `reports/metrics/`

### Pipeline 3 — Architecture

**Entry point:** `make pipeline-arch` or `python -m pipelines.architecture.run_architecture`

What it does:

1. Selects the best model from Pipeline 2 (by AUC-ROC on held-out val set)
2. Runs final `GridSearchCV` hyperparameter optimisation
3. Tunes classification threshold using Precision-Recall curve
4. Generates SHAP beeswarm and waterfall plots
5. Serialises the fitted pipeline to `models/artifacts/`
6. Registers the model version in the MLflow model registry

---

## Quick start

### Prerequisites

- Python 3.10+
- [Kaggle API credentials](https://www.kaggle.com/docs/api) (for data download)
- `make` (comes with macOS/Linux; install via `choco install make` on Windows)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-org/telco-churn-prediction.git
cd telco-churn-prediction

# 2. Create venv and install all dependencies
make install-dev

# 3. Copy and fill environment variables
cp .env.example .env

# 4. Download data
make download-data

# 5. Run all three pipelines in order
make pipeline-all
```

### Run individual pipelines

```bash
make pipeline-eda      # EDA only
make pipeline-base     # Base model training
make pipeline-arch     # Architecture + best model selection
```

### Launch MLflow UI

```bash
make mlflow-ui
# → open http://localhost:5000
```

### Start the inference API

```bash
make serve
# → open http://localhost:8000/docs
```

---

## Configuration

All settings live in `configs/`. The main file is `configs/config.yaml`.

```yaml
# Example: change the train/test split
data:
  test_size: 0.20   # change to 0.15 for more training data
  val_size:  0.10

# Example: add a feature to the drop list
preprocessing:
  drop_cols:
    - customerID
    - gender      # remove if you want to test fairness impact
```

Model hyperparameter grids are in `configs/model_params.yaml`. Expand them to widen the search:

```yaml
xgboost:
  learning_rate: [0.01, 0.05, 0.1, 0.2]   # added 0.2
  max_depth:     [3, 5, 7, 9]              # added 9
```

---

## Experiment tracking

Every training run is logged to MLflow automatically.

```
models/registry/          ← local tracking store (gitignored)
  mlruns/
    <experiment-id>/
      <run-id>/
        params/           ← all hyperparameters
        metrics/          ← AUC, F1, precision, recall per fold
        artifacts/        ← fitted pipeline, SHAP plots, confusion matrix
```

Launch the UI with `make mlflow-ui` and compare runs side-by-side.

To promote a run to the model registry:

```python
from telco_churn.models.registry import promote_model
promote_model(run_id="abc123", stage="Staging")
```

---

## API serving

The FastAPI app loads the registered model at startup.

**Endpoints:**


| Method | Path             | Description                          |
| ------ | ---------------- | ------------------------------------ |
| `GET`  | `/health`        | Liveness check                       |
| `GET`  | `/model/info`    | Loaded model version and metadata    |
| `POST` | `/predict`       | Single-customer churn prediction     |
| `POST` | `/predict/batch` | Batch prediction (list of customers) |


**Example request:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 12,
    "MonthlyCharges": 79.85,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
    "TechSupport": "No",
    "OnlineSecurity": "No",
    "PaymentMethod": "Electronic check"
  }'
```

**Response:**

```json
{
  "customer_id": null,
  "churn_probability": 0.83,
  "churn_prediction": true,
  "risk_tier": "HIGH",
  "top_drivers": [
    { "feature": "Contract_Month-to-month", "shap_value": 0.42 },
    { "feature": "tenure",                  "shap_value": -0.31 },
    { "feature": "TechSupport_No",          "shap_value": 0.27 }
  ]
}
```

---

## Development workflow

```bash
# Daily dev loop
make format        # auto-format with ruff
make lint          # lint check
make type-check    # mypy static analysis
make test          # full test suite with coverage

# Before opening a PR
make lint format type-check test
```

**Branch convention:**

```
main          ← stable, CI-protected
develop       ← integration branch
feature/*     ← new work
fix/*         ← bug fixes
experiment/*  ← throwaway model experiments
```

**Adding a new model:**

1. Add hyperparameter grid to `configs/model_params.yaml`
2. Register the estimator in `src/telco_churn/models/train.py`
3. Re-run `make pipeline-base` — MLflow logs it automatically

---

## Results

*Populated after running the full pipeline.*


| Model                          | AUC-ROC | F1  | Precision | Recall |
| ------------------------------ | ------- | --- | --------- | ------ |
| Logistic Regression (baseline) | —       | —   | —         | —      |
| Random Forest                  | —       | —   | —         | —      |
| XGBoost                        | —       | —   | —         | —      |
| LightGBM                       | —       | —   | —         | —      |
| **Best model**                 | —       | —   | —         | —      |


Key SHAP findings *(populated after Pipeline 3)*:

- Feature 1 — description
- Feature 2 — description

---

## Roadmap

- [ ] Pipeline 1: EDA — data quality + visualisations
- [ ] Pipeline 2: Base model — CV training + MLflow logging
- [ ] Pipeline 3: Architecture — best model + SHAP + registry
- [ ] FastAPI serving layer
- [ ] Dockerise the API (`docker-compose up`)
- [ ] Add data validation with `pandera`
- [ ] Fairness audit (gender / senior citizen subgroup analysis)
- [ ] Drift monitoring with `evidently`
- [ ] GitHub Actions: auto-retrain on data update

---

## License

MIT — see [LICENSE](LICENSE) for details.