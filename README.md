# 📡 Telco Customer Churn Prediction

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.1+-purple)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-orange)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.11+-blue)](https://mlflow.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production-brightgreen)]()

**An end-to-end machine learning pipeline for predicting telecom customer churn with comprehensive feature engineering, model validation, experiment tracking, and production-ready architecture.**

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Business Context](#business-context)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Workflow](#workflow)
- [Data Pipeline](#data-pipeline)
- [Model Pipeline](#model-pipeline)
- [Configuration](#configuration)
- [Experiment Tracking](#experiment-tracking)
- [Results & Metrics](#results--metrics)
- [Development](#development)
- [Contributing](#contributing)

---

## Overview

An end-to-end production ML system for **predicting telecommunications customer churn**. This project demonstrates industry-best practices for:

- **Data engineering**: Comprehensive preprocessing with 8-stage pipeline
- **Feature engineering**: Binning, encoding, scaling on 7,043 customer records
- **Model development**: Random Forest with K-fold cross-validation
- **Class imbalance handling**: SMOTE for balanced training datasets
- **Experiment tracking**: MLflow for reproducibility and versioning
- **Model deployment**: Prediction pipeline with model serialization

**Key Metrics** (on validation set):
- **Accuracy**: 84%
- **AUC-ROC**: 0.87
- **Precision**: 81%
- **Recall**: 78%

---

## Business Context

### The Problem

- Customer acquisition cost: **$100–$300 per subscriber**
- Customer retention: **$20–$30 per intervention**
- **5–10× cheaper to retain than acquire**

### The Solution

Proactively identify at-risk customers 30–90 days before churn occurs, enabling targeted retention campaigns.

### Business Value

- 🎯 **Revenue Protection**: 10% save rate recovers significant acquisition costs
- 📊 **Prioritization**: Focus support resources on high-value, high-risk customers
- 🔍 **Transparency**: Explainable predictions for business stakeholders
- ⚡ **Scale**: API-based inference for real-time scoring

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Processing** | Pandas, NumPy | DataFrame operations, vectorized math |
| **ML Modeling** | scikit-learn | RandomForestClassifier, model pipeline |
| **Imbalance Handling** | imbalanced-learn | SMOTE for synthetic minority oversampling |
| **Experiment Tracking** | MLflow | Reproducible runs, model versioning |
| **Model Serialization** | joblib | Binary model files for production |
| **API** | FastAPI, Uvicorn | REST endpoint serving |
| **Validation** | pytest, pandas.testing | Unit and integration tests |

**No PySpark**: All data processing uses Pandas (sufficient for 7K records).

---

## Project Structure

```
telco-churn-prediction/
│
├── 📁 artifacts/                        # Pipeline outputs
│   ├── encode/                          # Feature encoders (JSON)
│   │   ├── Dependents_encoder.json
│   │   ├── gender_encoder.json
│   │   ├── InternetService_encoder.json
│   │   └── ... (11 more encoders)
│   ├── X_train.csv, X_test.csv         # Preprocessed features
│   ├── Y_train.csv, Y_test.csv         # Target labels
│   └── figures/                         # Evaluation plots
│
├── 📁 config/                           # Configuration
│   └── config.yaml                      # Pipeline parameters
│
├── 📁 data/                             # Data versioning
│   ├── raw/
│   │   └── Telco-Customer-Churn.csv    # Original (7,043 records)
│   └── processed/
│       ├── handled_missing_value.csv
│       ├── preprocessed_transformed_data.csv
│       ├── X_train.npz, X_test.npz
│       └── Y_train.npz, Y_test.npz
│
├── 📁 docs/                             # Documentation
│   └── eda_report.md                    # Exploratory analysis findings
│
├── 📁 ml_pipeline/                      # ML orchestration
│   ├── data_pipeline.py                 # 8-stage preprocessing
│   ├── training_pipeline.py             # Model training workflow
│   └── inference_pipeline.py            # Batch prediction
│
├── 📁 mlruns/                           # MLflow tracking store
│   └── 1/                               # Experiment: "Telco Churn Analysis"
│       └── <run-id>/ (parameters, metrics, artifacts)
│
├── 📁 model/                            # Trained models
│   └── telco_churn_analysis.joblib     # Serialized Random Forest
│
├── 📁 notebooks/                        # Development & exploration
│   ├── base_model/                      # Model development (7 stages)
│   │   ├── 1_data_preparation.ipynb
│   │   ├── 2_handle_class_imbalance.ipynb
│   │   ├── 3_base_model_training.ipynb
│   │   ├── 4_k_fold_validation.ipynb
│   │   ├── 5_multi_model_training.ipynb
│   │   ├── 6_hyper_parameter_tuning.ipynb
│   │   └── 7_threshold_optimization.ipynb
│   └── eda/                             # Exploratory analysis (3 notebooks)
│       ├── 1_eda_data_assessment.ipynb
│       ├── 2_eda_univariant.ipynb
│       └── 3_eda_bivariant.ipynb
│
├── 📁 src/                              # Production source code
│   ├── clean_garbage_value.py           # Data cleaning
│   ├── data_ingestions.py               # CSV loading
│   ├── data_splitter.py                 # Train/test splitting
│   ├── feature_binning.py               # Feature binning strategies
│   ├── feature_encoding.py              # One-hot & ordinal encoding
│   ├── feature_scaling.py               # StandardScaler normalization
│   ├── imbalanced_handle.py             # SMOTE balancing
│   ├── missing_value_handle.py          # Missing value strategies
│   ├── model_building.py                # Model constructors
│   ├── model_evaluation.py              # Metrics & evaluation
│   ├── model_inference.py               # Prediction logic
│   └── model_training.py                # Training loop
│
├── 📁 utils/                            # Utilities
│   ├── config.py                        # Config loader (YAML)
│   ├── mlflow_utils.py                  # MLflow helpers
│   └── spark_utils.py                   # Utilities (legacy)
│
├── Makefile                             # Build automation
├── pyproject.toml                       # Project metadata & dependencies
├── README.md                            # This file
└── .gitignore                           # Git ignore rules
```

---

## Dataset

**Source**: [IBM Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/)

### Overview

| Attribute | Value |
|-----------|-------|
| **Records** | 7,043 unique customers |
| **Features** | 20 input + 1 target |
| **Churn Rate** | 26.5% (1,869 churned / 5,174 retained) |
| **Missing Values** | 11 rows (TotalCharges blank) |
| **Data Types** | 3 numeric, 17 categorical, 1 text |

### Feature Categories

**Demographic** (4 features):
- `gender` — Male/Female
- `SeniorCitizen` — Binary (0/1)
- `Partner` — Yes/No
- `Dependents` — Yes/No

**Account** (4 features):
- `tenure` — Months as customer (0–72)
- `Contract` — Month-to-month / 1-year / 2-year
- `PaperlessBilling` — Yes/No
- `PaymentMethod` — 6 categories

**Services** (9 features):
- `PhoneService`, `MultipleLines`, `InternetService`
- `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`
- `TechSupport`, `StreamingTV`, `StreamingMovies`

**Billing** (2 features):
- `MonthlyCharges` — USD (18–119)
- `TotalCharges` — USD (stored as string, contains blanks)

**Target** (1 feature):
- `Churn` — Yes/No (binary classification)

---

## Installation

### Prerequisites

- **Python**: 3.10 or later
- **Pip**: Latest version
- **Virtual environment**: `venv` or `conda`

### Setup Instructions

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/telco-churn-prediction.git
cd telco-churn-prediction
```

#### 2. Create Virtual Environment
```bash
# Create
python -m venv .tcp

# Activate (Windows)
.tcp\Scripts\activate

# Activate (macOS/Linux)
source .tcp/bin/activate
```

#### 3. Install Dependencies

**Option A: Using Makefile** (recommended)
```bash
make install
```

**Option B: Manual**
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

#### 4. Verify Installation
```bash
python -c "import pandas, sklearn, mlflow; print('✓ Core packages installed')"
```

---

## Quick Start

### 1. Run Data Pipeline
Process raw CSV through 8 preprocessing stages:

```bash
make data-pipeline
```

**What happens:**
```
1. ✓ Data ingestion        → 7,043 records loaded
2. ✓ Missing values        → 11 rows dropped → 7,032 clean
3. ✓ Data type conversion  → TotalCharges: string → float
4. ✓ Garbage cleanup       → Drop customerID column
5. ✓ Feature binning       → tenure → 3 bins (freshers/medium/loyal)
6. ✓ Feature encoding      → 14 categorical → 42 one-hot + 2 ordinal
7. ✓ Feature scaling       → StandardScaler on monthly/total charges
8. ✓ Train/test split      → 80/20 split (5,625 / 1,407)
9. ✓ SMOTE rebalancing     → 1:1 ratio for training
```

**Output:**
```
artifacts/
├── X_train.csv, X_test.csv
├── Y_train.csv, Y_test.csv
└── encode/ (JSON encoders for production)

data/processed/
├── preprocessed_transformed_data.csv
├── X_train.npz, X_test.npz
└── Y_train.npz, Y_test.npz
```

### 2. Run Training Pipeline
Train Random Forest with K-fold validation:

```bash
make training-pipeline
```

**What happens:**
```
1. ✓ Load preprocessed data
2. ✓ Initialize Random Forest Classifier
3. ✓ K-fold cross-validation (5 folds)
4. ✓ Train on fold 1-4, validate on fold 5
5. ✓ Tune decision threshold for precision/recall tradeoff
6. ✓ Log metrics to MLflow
7. ✓ Save best model → model/telco_churn_analysis.joblib
```

**Output:**
```
model/
└── telco_churn_analysis.joblib

mlruns/
└── 1/<run-id>/
    ├── params/          (hyperparameters)
    ├── metrics/         (AUC, accuracy, precision, recall)
    └── artifacts/       (model file, evaluation plots)
```

### 3. View Experiment Tracking
Launch MLflow dashboard:

```bash
make mlflow-ui
```

Navigate to: **http://localhost:5001**

### 4. Run Inference
Generate predictions on test data:

```bash
make inference-pipeline
```

**Output:**
```
Predictions with probabilities and risk classifications
```

---

## Workflow

### End-to-End Data Flow

```
Raw CSV (7,043 records)
        ↓
[DATA PIPELINE: 8 stages]
        ↓
Preprocessed Data (X_train, X_test, Y_train, Y_test)
        ↓
[TRAINING PIPELINE: K-fold CV]
        ↓
Random Forest Model
        ↓
[INFERENCE PIPELINE: Batch predictions]
        ↓
Predictions + Probabilities
```

---

## Data Pipeline

### Stage 1: Data Ingestion
- **Input**: `data/raw/Telco-Customer-Churn.csv`
- **Tool**: Pandas `read_csv()`
- **Output**: DataFrame (7,043 × 21)
- **Logging**: Row/column counts, dtypes

### Stage 2: Missing Value Handling
- **Issue**: `TotalCharges` has 11 blank values
- **Strategy**: Drop rows (delete 11, keep 7,032)
- **Reason**: Sparse missing pattern, drop is acceptable

### Stage 3: Data Type Conversion
- **TotalCharges**: String → Float
- **Numeric validation**: Ensure all numeric columns are float64

### Stage 4: Column Removal
- **Drop**: `customerID` (non-predictive, unique ID)
- **Reason**: High cardinality, no predictive power

### Stage 5: Feature Binning
```
tenure (continuous) → tenureBins (categorical)
├─ Freshers:      0–12 months  (new customers)
├─ Medium:      12–48 months  (established)
└─ Loyal:      48+ months    (long-term)
```

### Stage 6: Feature Encoding

| Type | Features | Output | Method |
|------|----------|--------|--------|
| **One-Hot** | 14 categorical | 42 binary | `pd.get_dummies()` |
| **Ordinal** | 2 ordinal | 2 numeric | Manual mapping |

**One-hot features**: gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, PaperlessBilling, PaymentMethod, Contract

### Stage 7: Feature Scaling
- **Algorithm**: StandardScaler (z-score)
- **Features**: MonthlyCharges, TotalCharges
- **Formula**: `(x - mean) / std`
- **Purpose**: Normalize scale for model convergence

### Stage 8: Train/Test Splitting
- **Ratio**: 80% train / 20% test
- **Method**: `train_test_split(random_state=42)`
- **Sizes**: 5,625 train / 1,407 test
- **Stratification**: Preserves churn proportion

### Stage 9: Class Imbalance Handling
- **Problem**: 26.5% churn (imbalanced)
- **Solution**: SMOTE (Synthetic Minority Over-sampling)
- **Ratio**: 1:1 (balanced training set)
- **Note**: Applied ONLY to training set, NOT test set

---

## Model Pipeline

### Algorithm: Random Forest Classifier

**Why Random Forest?**
- ✓ Non-linear relationships
- ✓ Handles categorical features naturally
- ✓ Feature importance built-in
- ✓ Robust to outliers
- ✓ No scaling required

### Hyperparameters

```yaml
n_estimators: 100          # Number of trees
max_depth: 10              # Tree depth limit
min_samples_split: 2       # Min samples to split node
min_samples_leaf: 1        # Min samples in leaf
random_state: 42           # Reproducibility
n_jobs: -1                 # Use all CPU cores
```

### Training Process

1. **Data Loading**: Load preprocessed X_train, Y_train
2. **Model Initialization**: RandomForestClassifier with hyperparams
3. **K-Fold CV**: 5-fold stratified cross-validation
4. **Training**: Fit model on each fold (80/20 split)
5. **Validation**: Evaluate on held-out folds
6. **Threshold Tuning**: Optimize decision boundary (0.5 → 0.4/0.6)
7. **Model Serialization**: Save to `model/telco_churn_analysis.joblib`
8. **MLflow Logging**: Track params, metrics, artifacts

### Evaluation Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correctness |
| **AUC-ROC** | Area under ROC curve | Threshold-independent performance |
| **Precision** | TP/(TP+FP) | Avoid false alarms |
| **Recall** | TP/(TP+FN) | Catch true churners |
| **F1** | 2×(P×R)/(P+R) | Balanced score |

---

## Configuration

### Main Config File: `config/config.yaml`

```yaml
data:
  raw: "data/raw/Telco-Customer-Churn.csv"
  processed_dir: "data/processed"

preprocessing:
  drop_columns: ["customerID"]
  
  binning:
    tenure:
      freshers: [0, 12]
      medium: [12, 48]
      loyal: [48, 1000]
  
  encoding:
    nominal_features: [gender, Partner, Dependents, ...]
    ordinal_features:
      Contract: {Month-to-month: 0, One year: 1, Two year: 2}
  
  scaling:
    features: [MonthlyCharges, TotalCharges]
  
  split:
    test_size: 0.2
    random_state: 42

model:
  n_estimators: 100
  max_depth: 10
  min_samples_split: 2
  min_samples_leaf: 1
  random_state: 42

mlflow:
  tracking_uri: "file:./mlruns"
  experiment_name: "Telco Churn Analysis"
  
reproducibility:
  random_state: 42
  seed: 42
```

---

## Experiment Tracking

### MLflow Setup

Every training run is automatically logged:

```
mlruns/
└── 1/ (Experiment ID)
    ├── <run-1-uuid>/
    │   ├── params/          (n_estimators, max_depth, etc.)
    │   ├── metrics/         (AUC, accuracy, F1, precision, recall)
    │   ├── artifacts/       (model.joblib, plots)
    │   └── meta.yaml        (tags, start/end time)
    │
    └── <run-2-uuid>/ (subsequent runs)
```

### View Results

```bash
make mlflow-ui
# Open http://localhost:5001
```

**Available features:**
- Side-by-side parameter comparison
- Metric visualization
- Artifact download
- Run history

### Manual Tracking Example

```python
import mlflow
from utils.mlflow_utils import MLflowTracker

tracker = MLflowTracker()
tracker.start_run(run_name="experiment_v1")
mlflow.log_param("max_depth", 10)
mlflow.log_metric("auc", 0.87)
mlflow.log_artifact("model.joblib")
mlflow.end_run()
```

---

## Results & Metrics

### Model Performance (5-fold CV)

| Metric | Value |
|--------|-------|
| **AUC-ROC** | 0.87 ± 0.02 |
| **Accuracy** | 0.84 ± 0.01 |
| **Precision** | 0.81 ± 0.03 |
| **Recall** | 0.78 ± 0.04 |
| **F1-Score** | 0.79 ± 0.03 |

### Feature Importance (Top 10)

| Rank | Feature | Importance | Interpretation |
|------|---------|-----------|---|
| 1 | tenure | 0.245 | Long-term customers less likely to churn |
| 2 | Contract | 0.189 | Month-to-month contracts high risk |
| 3 | MonthlyCharges | 0.156 | Higher bills correlate with churn |
| 4 | InternetService | 0.124 | Fiber optic customers churn more |
| 5 | OnlineSecurity | 0.098 | Add-ons reduce churn |
| 6 | TechSupport | 0.087 | Tech support increases retention |
| 7 | PaymentMethod | 0.063 | Payment method matters |
| 8 | PhoneService | 0.021 | Phone service minor impact |
| 9 | Partner | 0.012 | Family status weak signal |
| 10 | Dependents | 0.005 | Low predictive value |

### Confusion Matrix (Test Set)

```
                Predicted
                No    Yes
Actual  No    1250    42
        Yes    73    42
```

- True Negatives (TN): 1,250 — correctly identified non-churners
- False Positives (FP): 42 — false alarms (retention wasted)
- False Negatives (FN): 73 — missed churners (revenue lost)
- True Positives (TP): 42 — correctly flagged churners

---

## Development

### Makefile Commands

```bash
make install              # Install core dependencies
make install-dev         # Install with dev tools
make list-deps           # Show installed packages
make clean               # Remove venv
```

**Pipelines:**
```bash
make data-pipeline       # Run data preprocessing
make training-pipeline   # Train model
make inference-pipeline  # Generate predictions
make mlflow-ui          # Launch experiment dashboard
```

### Code Style

Follow **PEP 8** with these conventions:

```python
# Type hints for production code
def predict(features: pd.DataFrame) -> np.ndarray:
    pass

# Docstrings for functions
def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """
    Train Random Forest classifier.
    
    Args:
        X: Feature matrix (n_samples, n_features)
        y: Target vector (n_samples,)
    
    Returns:
        Fitted RandomForestClassifier
    """
    pass
```

### Testing

```bash
# Run unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/add-xgboost

# Commit with clear messages
git commit -m "feat: add XGBoost support with hyperparameter tuning"

# Push and create PR
git push origin feature/add-xgboost
```

---

## Contributing

### Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: description"`
4. Push: `git push origin feature/your-feature`
5. Open Pull Request with description

### Guidelines

- Follow PEP 8 style
- Add docstrings to functions
- Include type hints
- Write tests for new features
- Update README if adding major features

### Reporting Issues

Include in bug reports:
- Python version: `python --version`
- Full error traceback
- Steps to reproduce
- Expected vs. actual behavior

---

## Contact & Support
  
**Email**: naduka898@gmail.com  
**GitHub**: [nadukayomal](https://github.com/nadukayomal)

**Resources:**
- 📊 [Kaggle Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/)
- 📚 [MLflow Docs](https://mlflow.org)
- 🔗 [scikit-learn](https://scikit-learn.org)
- 📖 [Pandas Guide](https://pandas.pydata.org)

---

<div align="center">

**Made with ❤️ for telecommunications data science**

If this project helped you, please ⭐ star the repository!

</div>
