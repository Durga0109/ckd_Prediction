# Chronic Kidney Disease (CKD) Prediction System — Complete Project Documentation

> **Project Title:** AI-Powered Clinical Decision Support System for Chronic Kidney Disease Prediction with Explainable AI  
> **Domain:** Healthcare / Medical AI / Machine Learning  
> **Dataset:** UCI Chronic Kidney Disease Dataset (400 samples, 25 attributes)  
> **Tech Stack:** Python · XGBoost · Random Forest · SHAP · LIME · FastAPI · Streamlit · SQLite · SQLAlchemy · JWT · Docker · Kubernetes  
> **Model Accuracy:** ~98.75% (ROC-AUC)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Dataset & Clinical Parameters](#3-dataset--clinical-parameters)
4. [Data Preprocessing Pipeline](#4-data-preprocessing-pipeline)
5. [Machine Learning Model Training](#5-machine-learning-model-training)
6. [Prediction Pipeline (Inference)](#6-prediction-pipeline-inference)
7. [eGFR Calculation & CKD Staging](#7-egfr-calculation--ckd-staging)
8. [Explainable AI (XAI) — SHAP & LIME](#8-explainable-ai-xai--shap--lime)
9. [Automated Clinical Recommendations Engine](#9-automated-clinical-recommendations-engine)
10. [Backend — FastAPI REST API](#10-backend--fastapi-rest-api)
11. [Frontend — Streamlit Clinical Dashboard](#11-frontend--streamlit-clinical-dashboard)
12. [Authentication & Role-Based Access Control](#12-authentication--role-based-access-control)
13. [Patient Management System (CRUD)](#13-patient-management-system-crud)
14. [Prediction Result Storage & History Tracking](#14-prediction-result-storage--history-tracking)
15. [PDF Report Generation](#15-pdf-report-generation)
16. [Disease Progression Monitoring (eGFR Trendline)](#16-disease-progression-monitoring-egfr-trendline)
17. [Deployment Infrastructure — Docker & Kubernetes](#17-deployment-infrastructure--docker--kubernetes)
18. [Complete End-to-End Workflow](#18-complete-end-to-end-workflow)
19. [Technology Summary](#19-technology-summary)
20. [Key Innovations & Differentiators](#20-key-innovations--differentiators)

---

## 1. Project Overview

This project is a **full-stack, AI-powered Clinical Decision Support System (CDSS)** for predicting Chronic Kidney Disease (CKD). It is designed for use by clinicians (doctors, nephrologists) in a hospital or clinical setting.

**What the system does:**
- Takes 24 clinical lab parameters from a patient's blood and urine tests
- Uses a trained ML model (XGBoost or Random Forest) to predict whether the patient has CKD or not
- Provides a CKD probability score, a confidence level, and a risk level
- Calculates the patient's **eGFR** (Estimated Glomerular Filtration Rate) using the CKD-EPI 2021 equation
- Determines the **CKD Stage** (1-5) based on the KDIGO 2024 clinical guidelines
- Explains **why** the model made its prediction using two Explainable AI techniques: **SHAP** (SHapley Additive exPlanations) and **LIME** (Local Interpretable Model-agnostic Explanations)
- Generates **personalized clinical recommendations** based on the patient's specific abnormal lab values
- Stores all patient records and prediction history in a database
- Allows clinicians to track **disease progression** over time via eGFR trendlines
- Generates **downloadable PDF clinical reports** for medical records
- Provides a secure login system with JWT-based authentication

---

## 2. System Architecture

The system follows a **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Streamlit)                        │
│  ┌──────────┐ ┌───────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │  Login   │ │ Patient   │ │  Patient     │ │  Prediction   │  │
│  │  Page    │ │ List Page │ │  Profile     │ │  Dashboard    │  │
│  │ (Auth)   │ │ (CRUD)    │ │  (Register)  │ │  (AI+XAI)     │  │
│  └──────────┘ └───────────┘ └──────────────┘ └───────────────┘  │
│                         │ HTTP/REST                               │
├─────────────────────────┼───────────────────────────────────────┤
│                      BACKEND (FastAPI)                            │
│  ┌──────────┐ ┌───────────┐ ┌───────────────────────────────┐   │
│  │  Auth    │ │ Patient   │ │  Prediction   Router          │   │
│  │  Router  │ │ Router    │ │  (calls ML Service)           │   │
│  └──────────┘ └───────────┘ └───────────────────────────────┘   │
│       │             │                      │                      │
│  ┌──────────┐ ┌───────────┐ ┌───────────────────────────────┐   │
│  │  Auth    │ │ SQLAlchemy│ │  ML Service (SHAP+LIME)       │   │
│  │  Service │ │   ORM     │ │  (Model, Scaler, Encoders)    │   │
│  │  (JWT)   │ │           │ │                               │   │
│  └──────────┘ └───────────┘ └───────────────────────────────┘   │
│                         │                                         │
├─────────────────────────┼───────────────────────────────────────┤
│                      DATA LAYER                                   │
│  ┌──────────────────────┐  ┌────────────────────────────────┐   │
│  │  SQLite Database     │  │  Serialized ML Artifacts       │   │
│  │  (Clinician, Patient,│  │  (.pkl files: model, scaler,   │   │
│  │   Prediction tables) │  │   encoders, feature names,     │   │
│  └──────────────────────┘  │   KNN imputer, metrics)        │   │
│                            └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Communication:**
- Frontend (Streamlit) communicates with Backend (FastAPI) via REST API calls (HTTP POST/GET/PUT/DELETE)
- Backend interacts with the SQLite database via SQLAlchemy ORM
- Backend loads pre-trained ML models from serialized `.pkl` files on startup
- JWT tokens are used for authentication between frontend and backend

---

## 3. Dataset & Clinical Parameters

**Source:** UCI Machine Learning Repository — Chronic Kidney Disease Dataset  
**Samples:** 400 patients (250 CKD, 150 Not CKD)  
**Total Attributes:** 25 (24 clinical features + 1 target class)

### 3.1 Numerical Features (14)

| # | Feature | Full Name | Normal Range | Unit |
|---|---------|-----------|--------------|------|
| 1 | `age` | Patient Age | — | years |
| 2 | `bp` | Blood Pressure | ~80 | mm/Hg |
| 3 | `sg` | Specific Gravity | 1.005–1.025 | — |
| 4 | `al` | Albumin in Urine | 0 | 0–5 scale |
| 5 | `su` | Sugar in Urine | 0 | 0–5 scale |
| 6 | `bgr` | Blood Glucose Random | 70–140 | mg/dL |
| 7 | `bu` | Blood Urea | 10–40 | mg/dL |
| 8 | `sc` | Serum Creatinine | 0.6–1.2 | mg/dL |
| 9 | `sod` | Sodium | 135–145 | mEq/L |
| 10 | `pot` | Potassium | 3.5–5.0 | mEq/L |
| 11 | `hemo` | Hemoglobin | 12–17 | gms/dL |
| 12 | `pcv` | Packed Cell Volume | 35–50 | % |
| 13 | `wbcc` | White Blood Cell Count | 4500–11000 | cells/cmm |
| 14 | `rbcc` | Red Blood Cell Count | 4.5–6.0 | millions/cmm |

### 3.2 Categorical Features (10)

| # | Feature | Full Name | Possible Values |
|---|---------|-----------|-----------------|
| 1 | `rbc` | Red Blood Cells (in urine) | normal / abnormal |
| 2 | `pc` | Pus Cell | normal / abnormal |
| 3 | `pcc` | Pus Cell Clumps | present / notpresent |
| 4 | `ba` | Bacteria | present / notpresent |
| 5 | `htn` | Hypertension | yes / no |
| 6 | `dm` | Diabetes Mellitus | yes / no |
| 7 | `cad` | Coronary Artery Disease | yes / no |
| 8 | `appet` | Appetite | good / poor |
| 9 | `pe` | Pedal Edema | yes / no |
| 10 | `ane` | Anemia | yes / no |

### 3.3 Additional Input (Not in Dataset)

| Feature | Full Name | Purpose |
|---------|-----------|---------|
| `sex` | Sex of patient | Required for eGFR calculation (male/female) |

### 3.4 Target Variable

| Feature | Values | Encoding |
|---------|--------|----------|
| `class` | `ckd` (CKD) / `notckd` (Not CKD) | ckd=0, notckd=1 (via LabelEncoder) |

---

## 4. Data Preprocessing Pipeline

The preprocessing pipeline is implemented in `ckd_prediction_system.py → load_and_preprocess_data()` and performs the following 10 steps:

### Step 1: Dataset Loading
- Reads the UCI CSV file `chronic_kidney_disease_dataset.csv`
- Cleans column names by stripping quote characters

### Step 2: Missing Value Handling
- Replaces all `'?'` values with `NaN` (the UCI dataset uses `?` for missing values)
- Reports missing value counts per feature

### Step 3: Target Variable Cleaning
- Strips whitespace from the `class` column
- Standardizes labels: `'no'` → `'notckd'`, `'ckd\t'` → `'ckd'`

### Step 4: Data Type Conversion
- Converts all 14 numerical features to `float` type using `pd.to_numeric(errors='coerce')`

### Step 5: Missing Value Imputation
- **Numerical features:** Uses **KNN Imputer** (k=5) — finds the 5 nearest neighbors and uses their average to fill missing values. This is more sophisticated than simple mean/median imputation.
- **Categorical features:** Uses **mode imputation** — fills missing values with the most frequent category

### Step 6: Categorical Feature Encoding
- Uses **LabelEncoder** for each of the 10 categorical features
- Each encoder is saved for later use during inference (so new predictions are encoded consistently)

### Step 7: Target Variable Encoding
- Uses a separate **LabelEncoder** for the target: `ckd → 0`, `notckd → 1`

### Step 8: Train/Validation/Test Split
- **60% Training, 20% Validation, 20% Test** split
- Uses **stratified splitting** to maintain CKD/Non-CKD class ratios in all subsets

### Step 9: Feature Scaling
- Uses **RobustScaler** (robust to outliers, uses median and IQR instead of mean and std)
- Fitted on training data only; applied to validation and test data (to prevent data leakage)

### Step 10: Class Imbalance Handling (SMOTE)
- Applies **SMOTE** (Synthetic Minority Over-Sampling Technique) only to the training set
- SMOTE generates synthetic samples of the minority class by interpolating between existing minority samples
- This balances the CKD vs. Non-CKD classes to prevent bias toward the majority class

### Saved Artifacts (Serialized with Joblib)

| Artifact File | Contents | Purpose |
|---|---|---|
| `ckd_best_model.pkl` | Trained best model (XGBoost or RF) | Making predictions |
| `ckd_scaler.pkl` | Fitted RobustScaler | Scaling new patient data |
| `ckd_feature_names.pkl` | Ordered list of 24 feature names | Ensuring correct feature ordering |
| `ckd_label_encoders.pkl` | Dict of 10 LabelEncoders | Encoding categorical inputs |
| `ckd_target_encoder.pkl` | Target LabelEncoder | Decoding prediction output |
| `ckd_knn_imputer.pkl` | Fitted KNN Imputer | Handling missing values |
| `ckd_test_metrics.pkl` | Test set evaluation metrics | Performance reference |

---

## 5. Machine Learning Model Training

### 5.1 Models Implemented

Two machine learning models are trained and compared:

#### Model 1: XGBoost (Extreme Gradient Boosting)
- **Algorithm:** Ensemble of boosted decision trees trained sequentially, where each new tree corrects errors of the previous ones
- **Hyperparameter Search Space:**
  - `n_estimators`: [100, 200, 300] — number of boosting rounds
  - `max_depth`: [3, 4, 5, 6] — maximum tree depth
  - `learning_rate`: [0.01, 0.1, 0.2] — shrinkage rate per tree
  - `subsample`: [0.8, 0.9, 1.0] — fraction of samples per tree
- **Configuration:** `eval_metric='logloss'`, `use_label_encoder=False`, `random_state=42`

#### Model 2: Random Forest
- **Algorithm:** Ensemble of independently trained decision trees that vote on the final prediction
- **Hyperparameter Search Space:**
  - `n_estimators`: [100, 200, 300]
  - `max_depth`: [10, 15, 20, None]
  - `min_samples_split`: [2, 5, 10]
  - `min_samples_leaf`: [1, 2, 4]
- **Configuration:** `random_state=42`, `n_jobs=-1`

### 5.2 Hyperparameter Optimization
- **Method:** `GridSearchCV` — exhaustive search over the parameter grid
- **Cross-Validation:** 5-fold stratified CV
- **Scoring Metric:** ROC-AUC (Area Under the Receiver Operating Characteristic curve)
- **Parallelization:** `n_jobs=-1` (uses all available CPU cores)

### 5.3 Model Selection
- Both models are evaluated on the **validation set** using ROC-AUC
- The model with the **highest validation ROC-AUC** is selected as the best model
- The user can also force a specific model using: `python train_model_selector.py --model [xgboost/randomforest/both]`

### 5.4 Model Evaluation Metrics
The best model is evaluated on the held-out test set with:
- **Accuracy** — overall correctness
- **Precision** — of predicted CKD cases, how many are true CKD
- **Recall (Sensitivity)** — of all actual CKD cases, how many were correctly identified
- **F1-Score** — harmonic mean of precision and recall
- **ROC-AUC** — probability that the model ranks a random positive example higher than a random negative one
- **Confusion Matrix** — true positives, false positives, true negatives, false negatives
- **Classification Report** — per-class precision, recall, F1

**Reported Performance:** ~98.75% accuracy, ~0.99 ROC-AUC

---

## 6. Prediction Pipeline (Inference)

When a new patient's data is submitted for prediction, the system follows this pipeline (implemented in `predict_ckd_with_stage()` and `MLService.predict()`):

### Step 1: Input Validation
- Checks that all 24 clinical features + `sex` are present
- Reports any missing features

### Step 2: Categorical Feature Encoding
- Encodes the 10 categorical features using the **same LabelEncoders** saved during training
- Converts values to lowercase before encoding
- Falls back to 0 if an unseen value is encountered

### Step 3: Feature Ordering & Scaling
- Extracts features in the **exact same order** as used during training (from `ckd_feature_names.pkl`)
- Scales the features using the **same RobustScaler** saved during training

### Step 4: Model Prediction
- Calls `model.predict_proba()` to get class probabilities
- Calls `model.predict()` to get the binary prediction
- Class 0 = CKD, Class 1 = Not CKD (as encoded during training)
- Extracts:
  - `ckd_probability` — probability of CKD (class 0)
  - `no_ckd_probability` — probability of Not CKD (class 1)

### Step 5: Confidence Level Calculation
- `confidence_score = abs(ckd_probability - 0.5) * 2`
- **High** confidence: score ≥ 0.4 (probability ≥ 70% or ≤ 30%)
- **Medium** confidence: score ≥ 0.2 (probability ≥ 60% or ≤ 40%)
- **Low** confidence: score < 0.2 (probability near 50%)

### Step 6: Risk Level Assessment
- **High risk:** CKD probability ≥ 70%
- **Medium risk:** CKD probability ≥ 50%
- **Low risk:** CKD probability < 50%

### Step 7: eGFR Calculation (see Section 7)
### Step 8: CKD Stage Determination (see Section 7)
### Step 9: SHAP Explanation Generation (see Section 8)
### Step 10: LIME Explanation Generation (see Section 8)
### Step 11: Clinical Recommendations (see Section 9)

---

## 7. eGFR Calculation & CKD Staging

### 7.1 eGFR Calculation (CKD-EPI 2021 Equation — Race-Free)

The system calculates the **Estimated Glomerular Filtration Rate (eGFR)** — the gold-standard clinical marker of kidney function. eGFR estimates how many mL of blood the kidneys can filter per minute.

**Formula used:** CKD-EPI 2021 (the latest race-free equation, replacing the 2009 version):

```
eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^(-1.200) × 0.9938^age × [1.012 if female]
```

**Where:**
- `Scr` = Serum Creatinine (from patient's lab test, in mg/dL)
- `κ` = 0.7 (female) or 0.9 (male)
- `α` = -0.241 (female) or -0.302 (male)
- `age` = Patient age in years
- Female factor = 1.012 (applied only for female patients)

**Output:** eGFR in mL/min/1.73m²

### 7.2 CKD Stage Determination (KDIGO 2024 Guidelines)

Based on the calculated eGFR, the system maps to CKD stage using KDIGO (Kidney Disease: Improving Global Outcomes) clinical guidelines:

| eGFR Range (mL/min/1.73m²) | Stage | Description |
|---|---|---|
| ≥ 90 | Stage 1 (G1) | Normal or high kidney function |
| 60–89 | Stage 2 (G2) | Mildly decreased kidney function |
| 45–59 | Stage 3a (G3a) | Mild to moderately decreased kidney function |
| 30–44 | Stage 3b (G3b) | Moderately to severely decreased kidney function |
| 15–29 | Stage 4 (G4) | Severely decreased kidney function |
| < 15 | Stage 5 (G5) | Kidney failure (end-stage) |

**If the model predicts "No CKD":** Stage is set to 0 with description "No CKD - Normal kidney function"

---

## 8. Explainable AI (XAI) — SHAP & LIME

This is one of the most important differentiators of this project. Rather than providing a "black box" prediction, the system explains **why** it arrived at its prediction using two complementary XAI techniques.

### 8.1 SHAP (SHapley Additive exPlanations)

**What it is:** SHAP values come from game theory (Shapley values). They assign each feature a value representing its contribution to pushing the prediction from the base value (average prediction) toward the actual prediction.

**Implementation:**
- Uses `shap.TreeExplainer` for tree-based models (XGBoost, Random Forest) — this is an exact, fast algorithm
- Falls back to `shap.KernelExplainer` for other model types
- Extracts SHAP values for **Class 0 (CKD)** — the class of clinical interest
- Handles multi-dimensional SHAP value arrays (2D, 3D) with proper extraction logic

**Output for each patient prediction:**
- **Feature importance ranking** — all 24 features ranked by absolute SHAP value
- **Top 10 features** with:
  - Feature name (e.g., `hemo`, `sc`, `al`)
  - SHAP value (positive = increases CKD risk, negative = decreases CKD risk)
  - Absolute SHAP value (magnitude of impact)
  - Original feature value (what the patient's actual value was)
  - Impact direction: "↑ INCREASES" or "↓ DECREASES" CKD risk
- **Base value** — the model's average prediction across all training data

**Visualization:**
- Creates a professional 2-panel SHAP report:
  - **Left Panel:** Horizontal bar chart of top 10 features (red = increases risk, teal = decreases risk)
  - **Right Panel:** Text summary with prediction, probabilities, eGFR, stage, top risk factors, and recommendations
- Interactive Plotly bar chart in the Streamlit frontend

### 8.2 LIME (Local Interpretable Model-agnostic Explanations)

**What it is:** LIME creates a simplified, interpretable model (linear model) around the specific prediction by perturbing the input data and observing how the prediction changes.

**Implementation:**
- Uses `lime.lime_tabular.LimeTabularExplainer`
- Configured with feature names and class names `['CKD', 'No CKD']`
- Generates explanations for the **top 10 features**

**Output:**
- **Feature importance** with LIME weights (similar to SHAP but computed differently)
- **LIME score** — confidence of the local explanation

**Why two XAI methods?**
- If SHAP and LIME both highlight the same top biomarkers, the diagnosis is **more reliable**
- They provide different perspectives: SHAP gives a global, consistent mathematically rooted breakdown; LIME provides a local, intuitive explanation
- Having dual verification boosters confidence in clinical settings

---

## 9. Automated Clinical Recommendations Engine

The system generates **personalized, actionable clinical recommendations** based on the patient's specific lab values. This is implemented in `MLService._generate_feature_recommendations()`.

### Recommendations are triggered by these conditions:

| Condition | Threshold | Recommendation |
|---|---|---|
| **High Blood Pressure** | BP > 140 mmHg | Target BP < 130/80, discuss ACEi/ARB therapy |
| **Anemia** | Hemo < 12 (Female) or < 13 (Male) | Evaluate iron, B12/Folate, erythropoietin agents |
| **High Serum Creatinine** | SC > 1.5 mg/dL | Avoid nephrotoxic drugs (NSAIDs, IV contrast) |
| **Proteinuria (Albumin)** | Albumin ≥ 1 | Indicates kidney damage; strict BP control |
| **Poor Glycemic Control** | BGr > 180 mg/dL | Tighten diabetes management (HbA1c < 7%) |
| **Hyperkalemia** | Potassium > 5.5 | URGENT: Low-K diet, review meds (spironolactone) |
| **Hypokalemia** | Potassium < 3.5 | Dietary supplementation |
| **Hyponatremia** | Sodium < 135 | Evaluate fluid intake, possible restriction |
| **Possible Infection** | WBC > 11000 | Screen for UTI (Urinary Tract Infection) |

### Additional stage-based recommendations (from `ckd_prediction_system.py`):

| CKD Stage | Recommendations |
|---|---|
| **Stage 4-5** or probability ≥ 95% | URGENT nephrology consultation, hospital admission, strict renal diet, weekly monitoring |
| **Probability ≥ 90%** | Urgent nephrology referral (1-2 weeks), monitor BP 2-3x daily, no NSAIDs |
| **Stage 3** | Consult nephrologist (1 month), kidney-friendly diet, 3-month monitoring |
| **Stage 1-2** | Regular check-ups, 6-12 month monitoring, healthy lifestyle |
| **No CKD** | Continue healthy lifestyle, manage risk factors, stay hydrated |
| **Diabetes comorbidity** | HbA1c target < 7% |
| **Hypertension comorbidity** | Strict BP control < 130/80 mmHg |

---

## 10. Backend — FastAPI REST API

The backend is a **FastAPI** REST API server (file: `backend/app/main.py`).

### 10.1 API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/auth/signup` | Register a new clinician | No |
| `POST` | `/auth/login` | Login, receive JWT token | No |
| `GET` | `/auth/me` | Get current user info | Yes |
| `POST` | `/patients/` | Create a new patient profile | Yes |
| `GET` | `/patients/` | List all patients for current clinician | Yes |
| `GET` | `/patients/{id}` | Get specific patient | Yes |
| `PUT` | `/patients/{id}` | Update patient info | Yes |
| `DELETE` | `/patients/{id}` | Delete a patient | Yes |
| `POST` | `/predictions/` | Make a CKD prediction | Yes |
| `GET` | `/predictions/patient/{id}` | Get all predictions for a patient | Yes |
| `GET` | `/predictions/{id}` | Get specific prediction | Yes |
| `GET` | `/` | Root endpoint (API info) | No |
| `GET` | `/health` | Health check | No |

### 10.2 Key Backend Features
- **CORS Middleware** enabled for cross-origin requests (frontend on different port)
- **Auto-docs** at `/docs` (Swagger UI powered by FastAPI)
- **Database auto-initialization** on startup
- **ML models loaded once** at startup (singleton pattern via `ml_service = MLService()`)

---

## 11. Frontend — Streamlit Clinical Dashboard

The frontend is built with **Streamlit** — a Python framework for data-centric web applications.

### 11.1 Pages

| # | Page | Icon | Purpose |
|---|---|---|---|
| 1 | **Home** (`app.py`) | 🏥 | Landing page with system overview and quick actions |
| 2 | **Login** (`1_🔑_Login.py`) | 🔑 | Clinician login and registration |
| 3 | **Patients** (`2_👥_Patients.py`) | 👥 | Patient list with table view, search, and actions |
| 4 | **Patient Profile** (`3_👤_Patient_Profile.py`) | 👤 | Register new patient or edit existing profile |
| 5 | **Prediction Dashboard** (`4_🔮_Prediction.py`) | 🔮 | Main prediction + analysis page |

### 11.2 Prediction Dashboard Features (Page 4 — The Core Page)

This is the most feature-rich page with:

1. **Patient Selector** — Dropdown to select a registered patient
2. **Medical Test Report Entry Form** — Organized into 3 tabs:
   - **🩸 Blood Tests & Vitals:** BP, Hemoglobin, Blood Glucose, PCV, RBC count, WBC count
   - **🧬 Kidney Markers:** Serum Creatinine, Blood Urea, Sodium, Potassium, Specific Gravity, Albumin, Sugar
   - **🩺 Lifestyle & Urinalysis:** RBC (urine), Pus Cell, Bacteria, Hypertension, Diabetes, CAD, Appetite, Pedal Edema, Anemia
3. **Reference Ranges** displayed inline for every input (e.g., "Blood Pressure (Normal: 80 mm/Hg)")
4. **Smart Pre-filling** — If the patient has previous visits, the latest lab values are auto-populated
5. **Visit Date selector** — Allows backdating visits
6. **AI Clinical Diagnosis Panel** with:
   - **Metrics Row:** Diagnosis (CKD/No CKD), Model Confidence %, eGFR value (with delta from previous visit), CKD Stage
   - **Targeted Clinical Recommendations** section
   - **CKD Progression Note** with stage description
7. **Explainable AI Analysis (XAI)** — Three tabs:
   - **🎯 SHAP Risk Factors:** Interactive Plotly bar chart showing feature impact
   - **🧬 LIME Analysis:** Second XAI perspective using LIME weights
   - **📈 Progression History:** eGFR trendline chart + history table

---

## 12. Authentication & Role-Based Access Control

### 12.1 Authentication Flow

1. **Registration (`/auth/signup`):**
   - Clinician provides: email, password, full name, specialization (Nephrology, General Practice, Internal Medicine, etc.)
   - Password is hashed using **bcrypt** (via `passlib`) before storage
   - Email uniqueness is enforced

2. **Login (`/auth/login`):**
   - Clinician provides email and password
   - Server verifies credentials against bcrypt hash
   - On success, returns a **JWT (JSON Web Token)** with:
     - `sub` (subject) = clinician email
     - `exp` (expiration) = current time + 30 minutes
   - Token is signed using **HS256** algorithm with a secret key

3. **Authenticated Requests:**
   - Frontend stores the JWT token in Streamlit session state
   - Every API call includes `Authorization: Bearer <token>` header
   - Backend validates the token, extracts the email, and loads the clinician record
   - All patient/prediction endpoints are protected with the `get_current_clinician` dependency

### 12.2 Data Isolation
- Each clinician can only see and manage **their own patients**
- All patient queries filter by `clinician_id`
- Prediction access is verified through patient ownership

---

## 13. Patient Management System (CRUD)

### Database Model: `Patient`

| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Auto-incrementing unique identifier |
| `clinician_id` | Integer (FK) | References the clinician who created this patient |
| `full_name` | String | Patient full name |
| `age` | Integer | Patient age |
| `sex` | String | male / female |
| `contact_number` | String | Optional phone number |
| `bp`, `sg`, `al`, ... (24 fields) | Float/String | All clinical parameters |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on modification |

### CRUD Operations:
- **Create:** Register a new patient with demographics + sensible default clinical values
- **Read:** List all patients (paginated), get individual patient by ID
- **Update:** Modify patient demographics or clinical values
- **Delete:** Remove patient and cascade-delete all predictions

### Clinical Workflow:
1. Register patient with **demographics only** (Step 1 — Patient Profile page)
2. Clinical values are entered during the **first visit** on the Prediction Dashboard (Step 2)
3. On subsequent visits, the **latest values are pre-filled** for convenience

---

## 14. Prediction Result Storage & History Tracking

### Database Model: `Prediction`

| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Unique prediction ID |
| `patient_id` | Integer (FK) | References the patient |
| `ckd_prediction` | String | "CKD" or "No CKD" |
| `ckd_probability` | Float | Probability of CKD (0-1) |
| `no_ckd_probability` | Float | Probability of Not CKD (0-1) |
| `confidence_level` | String | "High" / "Medium" / "Low" |
| `risk_level` | String | "High" / "Medium" / "Low" |
| `egfr` | Float | Calculated eGFR value |
| `ckd_stage` | Integer | CKD stage (0-5) |
| `stage_description` | String | Human-readable stage description |
| `shap_values` | JSON | Complete SHAP analysis results |
| `lime_values` | JSON | Complete LIME analysis results |
| `top_features` | JSON | Top 10 contributing features |
| `input_data` | JSON | Snapshot of all input values used for this prediction |
| `visit_date` | DateTime | Date of the clinical visit |
| `created_at` | DateTime | Auto-set creation timestamp |

### Key Design Decisions:
- **Input data snapshot:** Every prediction stores a complete copy of the input values. This means even if the patient's profile is updated later, historical predictions retain their original context.
- **Full XAI storage:** SHAP and LIME explanations are stored as JSON, enabling retrospective review.
- **Visit date support:** Allows backdating clinical visits for delayed data entry.

---

## 15. PDF Report Generation

The system can generate **downloadable PDF clinical reports** for each prediction.

**Implementation:** Uses `fpdf2` library (file: `frontend/streamlit_app/utils/pdf_gen.py`).

### PDF Report Contents:
1. **Header:** "Chronic Kidney Disease (CKD) Clinical Report"
2. **Patient Information:** Name, visit date
3. **Summary of Results Table:**
   - CKD Prediction
   - Probability (%)
   - eGFR Value (mL/min)
   - CKD Stage
4. **Clinical Recommendations:** All personalized recommendations
5. **Top 5 AI Risk Factors:** Table with feature name, impact direction (Increases/Decreases), and SHAP value
6. **Footer:** Page number, generation timestamp

**Usage:** The "📄 Save as PDF" button appears on the prediction dashboard after an analysis is run.

---

## 16. Disease Progression Monitoring (eGFR Trendline)

When a patient has **multiple visits**, the system generates:

1. **eGFR Trendline Chart** — An interactive Plotly line chart showing how the eGFR has changed over time:
   - X-axis: Visit dates
   - Y-axis: eGFR values
   - Markers on each data point
2. **History Table** — Shows all past visits with:
   - Date
   - Diagnosis (CKD / No CKD)
   - eGFR value
   - CKD Stage
3. **Delta Metrics** — The current eGFR is shown with a delta indicator (↑ or ↓) compared to the previous visit

This allows clinicians to visually track whether a patient's kidney function is **improving, stable, or deteriorating**.

---

## 17. Deployment Infrastructure — Docker & Kubernetes

### 17.1 Docker
- **Dockerfile** is provided for containerization
- Base image: `python:3.10-slim`
- Installs all dependencies from `requirements.txt`
- Exposes port 8501 (Streamlit default)
- Includes health check endpoint
- Environment variables: `PYTHONUNBUFFERED=1`, `STREAMLIT_SERVER_HEADLESS=true`

### 17.2 Kubernetes
- Full Kubernetes manifests are provided in `deployment/kubernetes/`:
  - **`deployment.yaml`** — Defines the pod spec, resource limits, and replica count
  - **`service.yaml`** — Exposes the deployment as a ClusterIP service
  - **`ingress.yaml`** — Configures external HTTP access

### 17.3 AWS ECR
- Scripts and guides for pushing Docker images to **AWS Elastic Container Registry (ECR)**
- AMD64-specific build support for cloud compatibility

---

## 18. Complete End-to-End Workflow

Here is the full user journey from start to finish:

```
┌──────────────────────────────────────────────────────────────────┐
│  1. CLINICIAN REGISTRATION                                       │
│  → Clinician signs up with email, password, name, specialization │
│  → Password hashed with bcrypt, stored in SQLite                 │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  2. LOGIN                                                        │
│  → Clinician enters credentials                                  │
│  → JWT token generated and stored in session                     │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  3. PATIENT REGISTRATION (Patient Profile Page)                  │
│  → Enter demographics: name, age, sex, contact                   │
│  → Default clinical values assigned                              │
│  → Patient saved to database → Auto-redirects to Prediction page │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  4. CLINICAL VISIT (Prediction Dashboard)                        │
│  → Patient selected from dropdown                                │
│  → Clinician enters lab test results in organized form:          │
│    ├── Blood Tests & Vitals (6 parameters)                       │
│    ├── Kidney Markers (7 parameters)                             │
│    └── Lifestyle & Urinalysis (11 parameters)                    │
│  → Reference ranges shown for guidance                           │
│  → Visit date selected                                           │
│  → Click "Generate Prediction & Clinical Summary"                │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  5. BACKEND PROCESSING                                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ a) Encode categorical features (LabelEncoders)              │ │
│  │ b) Order features identically to training                   │ │
│  │ c) Scale features (RobustScaler)                            │ │
│  │ d) Model prediction → CKD probability, binary result       │ │
│  │ e) Calculate Confidence Level & Risk Level                  │ │
│  │ f) Calculate eGFR using CKD-EPI 2021 equation               │ │
│  │ g) Determine CKD Stage (KDIGO 2024 guidelines)              │ │
│  │ h) Generate SHAP explanation (TreeExplainer)                │ │
│  │ i) Generate LIME explanation (LimeTabularExplainer)         │ │
│  │ j) Generate personalized clinical recommendations           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│  → Save prediction + all results + input snapshot to database    │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  6. RESULTS DISPLAY (Prediction Dashboard)                       │
│  ├── Diagnosis: CKD / No CKD (color-coded)                      │
│  ├── Confidence: e.g., 97.3%                                    │
│  ├── eGFR: e.g., 42.5 mL/min (with ↓ delta from last visit)    │
│  ├── CKD Stage: e.g., Stage 3b                                  │
│  ├── Clinical Recommendations (targeted to this patient)         │
│  ├── SHAP Analysis (interactive bar chart)                       │
│  ├── LIME Analysis (second XAI perspective)                      │
│  └── Progression History (eGFR trendline if multiple visits)     │
└──────────────┬───────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────┐
│  7. REPORT EXPORT                                                │
│  → Click "Save as PDF" → Download clinical report                │
│  → Contains: diagnosis, probabilities, eGFR, stage,             │
│    recommendations, top 5 SHAP risk factors                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 19. Technology Summary

| Layer | Technology | Purpose |
|---|---|---|
| **ML Framework** | scikit-learn, XGBoost | Model training, evaluation, preprocessing |
| **XAI** | SHAP, LIME | Model interpretability/explainability |
| **Imbalanced Data** | imbalanced-learn (SMOTE) | Oversampling minority class |
| **Backend API** | FastAPI | REST API with auto-generated docs |
| **ORM** | SQLAlchemy | Object-Relational Mapping for DB access |
| **Database** | SQLite | Lightweight relational database |
| **Authentication** | python-jose (JWT), passlib (bcrypt) | Token-based auth with password hashing |
| **Frontend** | Streamlit | Interactive clinical dashboard |
| **Charts** | Plotly, Matplotlib, Seaborn | Interactive and static visualizations |
| **PDF Generation** | fpdf2 | Clinical report export |
| **Model Serialization** | Joblib | Saving/loading trained models |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Scalable cloud deployment |
| **Cloud** | AWS ECR | Container image registry |
| **Data Processing** | Pandas, NumPy | Data manipulation and computation |
| **Feature Scaling** | RobustScaler | Outlier-resistant normalization |
| **Imputation** | KNNImputer | Intelligent missing value handling |

---

## 20. Key Innovations & Differentiators

1. **Dual XAI (SHAP + LIME):** Provides two complementary explanations for every prediction — a rare feature in medical AI systems. This significantly boosts clinical trust and validation.

2. **Clinical Integration:** Not just a model — this is a complete clinical workflow system with patient management, visit tracking, and report generation.

3. **Real Clinical Formulas:** Uses the actual CKD-EPI 2021 equation (race-free, latest version) and KDIGO 2024 staging guidelines — the same tools nephrologists use.

4. **Automated Clinical Recommendations:** Dynamically generates actionable, parameter-specific medical advice instead of generic warnings.

5. **Disease Progression Tracking:** eGFR trendline visualization over multiple visits allows monitoring of kidney function over time.

6. **PDF Export:** Generates professional clinical reports suitable for medical records.

7. **Full-Stack Architecture:** Separation of concerns with FastAPI backend + Streamlit frontend, connected via REST API.

8. **Secure by Design:** JWT authentication, bcrypt password hashing, data isolation per clinician.

9. **Production-Ready Deployment:** Docker + Kubernetes + AWS ECR manifests provided.

10. **Smart Form Pre-filling:** Previous visit data is automatically loaded for convenience during follow-up visits.

11. **KNN Imputation + SMOTE:** Advanced data preprocessing that handles missing values intelligently and addresses class imbalance.

12. **Model Selection Pipeline:** Automated comparison of XGBoost vs. Random Forest with hyperparameter search, selecting the best-performing model.

---

*This documentation covers all features, technologies, algorithms, and workflows implemented in the CKD Prediction System project. It is intended to provide comprehensive context for generating a brief, accurate project summary.*
