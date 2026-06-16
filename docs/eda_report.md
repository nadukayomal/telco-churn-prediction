# Telco Customer Churn — Univariate Analysis Report

**Dataset:** Telco Customer Churn
**Records:** 7,043 | **Features:** 21 (20 predictors + 1 target)
**Analysis stage:** Univariate (single-feature distribution analysis, pre-modeling)

---

## 1. Dataset Overview

| Category | Features |
| :--- | :--- |
| **Numerical** | `tenure`, `MonthlyCharges`, `SeniorCitizen` (binary 0/1 flag, numeric-coded) |
| **Categorical** | `customerID`, `gender`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `TotalCharges`* |
| **Target** | `Churn` — No: ~75% · Yes: ~25% (**imbalanced**) |

*`TotalCharges` is listed as categorical only because of a data-type defect — see Section 5.

**Target imbalance implication:** a 75/25 split means accuracy is not a reliable evaluation metric. Plan for precision, recall, F1, and ROC-AUC, and consider stratified train/test splitting, class weighting, or resampling (e.g. SMOTE) at the modeling stage.

**Note on scope:** the univariate work completed so far covers the categorical features via frequency distributions (`value_counts(normalize=True)`). `tenure` and `MonthlyCharges` still require separate numeric univariate treatment (`.describe()`, histogram, boxplot, skew/kurtosis) and are flagged as **pending** in Section 7.

---

## 2. Demographic Features

| Feature | Distribution | Predictive Value | Key Consideration | Action |
| :--- | :--- | :--- | :--- | :--- |
| **gender** | ~50% / 50% | Very low | Balanced classes give no separating signal on their own. | Exclude, or retain only to test interaction effects. |
| **Partner** | ~50% / 50% (slight ~3–4 pt edge) | Low alone, moderate combined | Correlates with tenure, Dependents, and service bundling. | Binary encode (0/1); retain for interaction/bivariate testing. |
| **Dependents** | ~70% / 30% | Moderate–high | Skew suggests two distinct customer profiles (younger/independent vs. family households); class imbalance risk if used as a sole splitter. | Binary encode; cross-tab against `Churn`; monitor for bias from the 70/30 skew. |
| **SeniorCitizen** | Numeric 0/1 flag | Pending | Already binary-coded; treat as categorical despite numeric dtype. | Cross-tab against `Churn` before deciding to keep/drop. |

---

## 3. Phone Service Features

| Feature | Distribution | Predictive Value | Key Consideration | Action |
| :--- | :--- | :--- | :--- | :--- |
| **PhoneService** | Yes 90.3% · No 9.7% | Low | Near-constant distribution → near-zero-variance feature; the model has almost no contrast to learn from. | Encode binary (0/1) for now; flag for removal if importance stays negligible after modeling. |
| **MultipleLines** | No 48.1% · Yes 42.2% · No phone service 9.7% | Moderate | Captures usage intensity (possible proxy for household size/engagement). **Redundancy:** "No phone service" (9.7%) is identical to `PhoneService = No` — same 9.7% customers counted twice. | Keep `MultipleLines`, **drop `PhoneService`**. Encode one-hot (or ordinal: 0 = No phone service, 1 = No, 2 = Yes). |

**Structural insight:** `PhoneService` is fully recoverable from `MultipleLines` (its "No phone service" category), so carrying both into modeling adds no information and only introduces multicollinearity risk for linear models.

---

## 4. Internet Service Features

| Feature | Distribution | Key Consideration |
| :--- | :--- | :--- |
| **InternetService** | Fiber optic 44.0% · DSL 34.4% · No 21.7% | Baseline segmentation driving every add-on column below. |
| **OnlineSecurity** | No 49.7% · Yes 28.7% · No internet service 21.7% | "No internet service" matches `InternetService = No` exactly. |
| **OnlineBackup** | No 43.8% · Yes 34.5% · No internet service 21.7% | Same structural overlap. |
| **DeviceProtection** | No 43.9% · Yes 34.4% · No internet service 21.7% | Same structural overlap. |
| **TechSupport** | No 49.3% · Yes 29.0% · No internet service 21.7% | Same structural overlap. |
| **StreamingTV** | No 39.9% · Yes 38.4% · No internet service 21.7% | Near-even Yes/No split among internet users — more variance than the security/support group. |
| **StreamingMovies** | No 39.5% · Yes 38.8% · No internet service 21.7% | Same as StreamingTV — more balanced, likely more discriminative. |

**Predictive value:** Moderate for the security/protection/support group (skewed adoption, may separate "low-engagement" customers); moderate-to-higher for the streaming pair (closer to balanced, generally retains more signal).

**Structural insight (the critical finding):** the value **21.7%** recurs identically across all six add-on features and matches `InternetService = No`. This is not six independent populations — it is the *same* customer segment (no internet → cannot subscribe to any internet-dependent add-on) appearing seven times. Left unaddressed, one-hot encoding all seven columns creates near-perfect collinearity between `InternetService_No` and every `*_No internet service` dummy.

**Impact:**
- Tree-based models (Random Forest, XGBoost) tolerate this redundancy reasonably well.
- Linear/distance-based models (Logistic Regression, KNN) suffer inflated coefficient variance, unstable weights, and distorted feature-importance/interpretability.
- Analysts risk double-counting the same 21.7% segment as if it were independent evidence across seven features.

**Recommended treatment:**
1. Drop the redundant "No internet service" dummy from each of the six add-on encodings — `InternetService` alone already carries that information.
2. Optionally engineer a single derived feature, e.g. `TotalServicesSubscribed` (count of "Yes" across the six add-ons), to compress correlated columns into one informative numeric feature.
3. If using a linear model, check VIF (Variance Inflation Factor) post-encoding to confirm the fix.

---

## 5. Account & Billing Features

| Feature | Distribution | Predictive Value | Action |
| :--- | :--- | :--- | :--- |
| **Contract** | Month-to-month 55.0% · Two year 24.1% · One year 20.9% | High — well-documented strong churn predictor | One-hot or ordinal encode; prioritize in bivariate analysis against `Churn`. |
| **PaperlessBilling** | Yes 59.2% · No 40.8% | Low–moderate | Binary encode; check interaction with `PaymentMethod`. |
| **PaymentMethod** | Electronic check 33.6% · Mailed check 22.9% · Bank transfer (auto) 21.9% · Credit card (auto) 21.6% | High — Electronic check is a well-documented strong churn predictor | One-hot encode; flag "Electronic check" for early bivariate review. |

### TotalCharges — Data Quality Flag

`TotalCharges` should be a continuous numeric variable but is currently stored as an **object/string** dtype. Running `value_counts(normalize=True)` on it produced ~6,531 near-unique "categories" — a clear symptom of treating continuous data as categorical, and a sign no real numeric summary (mean, median, std, skew) has been computed yet.

A closer look reveals a **blank string `" "`** appearing 11 times in place of a numeric value. In this dataset these 11 rows consistently correspond to customers with `tenure = 0` (new sign-ups not yet billed).

| Issue | Risk if ignored | Resolution |
| :--- | :--- | :--- |
| Stored as string, not float | Arithmetic/model errors; no real distribution insight | `pd.to_numeric(df['TotalCharges'], errors='coerce')` |
| 11 blank-string rows → become NaN | Careless mean-imputation invents spending that never happened; careless zero-fill can bias tenure-based features | Cross-check against `tenure`; if all 11 are `tenure = 0`, set `TotalCharges = 0` (consistent with "not yet billed") |
| Right-skew (typical for this column, correlated with tenure × MonthlyCharges) | Can destabilize linear models | Re-run proper univariate analysis (`.describe()`, histogram/boxplot); consider log transform if used in a linear model |

---

## 6. Cross-Cutting Findings Summary

| Finding | Affected Features | Severity | Recommended Fix |
| :--- | :--- | :--- | :--- |
| Structural redundancy (same segment, multiple columns) | `PhoneService` ↔ `MultipleLines`; `InternetService` ↔ 6 add-ons | Medium–High (multicollinearity for linear models) | Drop one side of each redundant pair / collapse redundant dummy categories |
| Near-zero-variance feature | `PhoneService` | Low–Medium | Cross-tab with churn before keeping |
| Data type defect | `TotalCharges` | High (blocks numeric analysis entirely) | Convert to numeric, resolve 11 blank values |
| Class imbalance | `Churn` (target), `Dependents` (70/30) | Medium | Stratified split, class weighting/resampling for target; monitor bias risk for `Dependents` |
| Pending numeric univariate analysis | `tenure`, `MonthlyCharges` | N/A — not yet analyzed | Run `.describe()`, histograms, skew/outlier checks |

---

## 7. Recommended Next Steps (Priority Order)

1. **Fix `TotalCharges` dtype** and resolve the 11 missing/blank entries before any further numeric work.
2. **Complete numeric univariate analysis** for `tenure` and `MonthlyCharges` (currently pending).
3. **Resolve structural redundancies**: drop `PhoneService` in favor of `MultipleLines`; drop duplicated "No internet service" dummies across the six internet add-ons (or replace with a single `TotalServicesSubscribed` count feature).
4. **Encode remaining categoricals** — binary encode two-level features; one-hot or ordinal encode multi-level features depending on the downstream model.
5. **Address target imbalance** at the train/test split and modeling stage (stratification, class weights, or resampling).
6. **Move to bivariate analysis**: cross-tab every feature above against `Churn`, prioritizing the features already flagged as historically strong predictors — `Contract` (Month-to-month) and `PaymentMethod` (Electronic check) — to confirm signal strength before finalizing the feature set.