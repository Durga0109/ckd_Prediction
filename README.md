# 🏥 Chronic Kidney Disease (CKD) Clinical Decision Support System

> **AI-Powered Clinical Decision Support System for Prediction and Management of Chronic Kidney Disease with Explainable AI (SHAP & LIME)**

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen.svg)](https://github.com/Durga0109/ckd_Prediction)
[![Model Accuracy](https://img.shields.io/badge/Model%20Accuracy-98.75%25-blue.svg)](#ml-performance)
[![ROC-AUC](https://img.shields.io/badge/ROC--AUC-1.00-gold.svg)](#ml-performance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Project Overview

This project is a **full-stack, clinical-grade medical AI application** designed to help clinicians predict, stage, and explain Chronic Kidney Disease (CKD). It transforms a "black-box" machine learning model into a transparent clinical tool by integrating **Explainable AI (XAI)**, standard medical formulas, and automated recommendation engines.

**Core Capabilities:**
- **Automated Prediction**: Analyzes 24 clinical parameters to predict CKD with clinical-grade accuracy.
* **CKD Staging**: Automatically calculates **eGFR** (CKD-EPI 2021) and determines **CKD Stage** (KDIGO 2024).
- **Explainability**: Explains every diagnosis using dual-XAI techniques (**SHAP** and **LIME**).
- **Personalized Care**: Generates patient-specific clinical recommendations based on abnormal lab values.
- **Longitudinal Tracking**: Monitors disease progression via eGFR trendlines across multiple visits.
- **Professional Reporting**: Generates downloadable PDF clinical reports for medical records.

---

## 🏗️ System Architecture

The system follows a scalable **three-tier architecture** with secure data isolation.

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Streamlit)                        │
│  ┌──────────┐ ┌───────────┐ ┌──────────────┐ ┌───────────────┐  │
│  │  Login   │ │ Patient   │ │  Patient     │ │  Prediction   │  │
│  │  Page    │ │ List Page │ │  Profile     │ │  Dashboard    │  │
│  │ (Auth)   │ │ (CRUD)    │ │  (Register)  │ │  (AI+XAI)     │  │
│  └──────────┘ └───────────┘ └──────────────┘ └───────────────┘  │
│                         │ HTTP/REST (JSON)                        │
├─────────────────────────┼───────────────────────────────────────┤
│                      BACKEND (FastAPI)                            │
│  ┌──────────┐ ┌───────────┐ ┌───────────────────────────────┐   │
│  │  Auth    │ │ Patient   │ │  Prediction Engine            │   │
│  │  Service │ │ Service   │ │  (Calls ML Service)           │   │
│  └──────────┘ └───────────┘ └───────────────────────────────┘   │
│       │             │                      │                      │
│  ┌──────────┐ ┌───────────┐ ┌───────────────────────────────┐   │
│  │  JWT     │ │ SQLAlchemy│ │  ML Service (SHAP+LIME)       │   │
│  │  Auth    │ │   ORM     │ │  (Model, Scaler, Encoders)    │   │
│  └──────────┘ └───────────┘ └───────────────────────────────┘   │
├─────────────────────────┼───────────────────────────────────────┤
│                      DATA LAYER                                   │
│  ┌──────────────────────┐  ┌────────────────────────────────┐   │
│  │  SQLite Database     │  │  Trained ML Artifacts          │   │
│  │  (Clinicians,        │  │  (.pkl: Model, Scaler,         │   │
│  │   Patients, History) │  │   Imputer, Encoders)           │   │
│  └──────────────────────┘  └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```bash
ckd_Prediction/
└── using-uci-dataset 2/
    └── using-uci-dataset/
        ├── backend/                # FastAPI service (Logic, DB, API)
        │   ├── app/
        │   │   ├── models/         # SQLAlchemy DB models
        │   │   ├── routers/        # API Endpoints
        │   │   ├── schemas/        # Pydantic validation
        │   │   └── services/       # ML Inference & XAI Logic
        │   └── ckd_clinical.db     # Local SQLite database
        │
        ├── frontend/               # Streamlit application
        │   ├── streamlit_app/ 
        │   │   ├── Home.py         # Entry point
        │   │   ├── pages/          # Login, Patients, Diagnostics
        │   │   └── utils/          # API & PDF generation
        │
        ├── ml_pipeline/            # Core ML Engine & Training
        │   ├── __init__.py
        │   ├── ckd_prediction_system.py
        │   ├── train_model.py
        │   ├── train_xgboost.py
        │   └── train_model_selector.py
        │
        ├── scripts/                # Evaluation & Utility tools
        │   ├── __init__.py
        │   ├── demo.py
        │   └── predict.py
        │
        ├── docs/         # Specialized ML documentation
        │   ├── Model_switching.md
        │   ├── Use_xgboost.md
        │   └── ...
        │
        ├── trained_models/         # Serialized ML artifacts (Untracked)
        ├── deployment/             # Docker & Kubernetes manifests
        ├── requirements.txt        # Unified ML dependencies
        └── chronic_kidney_disease_dataset.csv
```

---

## 🎯 Clinical Methodology

The system is built on internationally recognized medical standards:

### 1. eGFR Calculation (CKD-EPI 2021 Equation)
Replaces old race-based calculations with the latest race-free formula (NEJM 2021).
```
eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^(-1.200) × 0.9938^age × [1.012 if female]
```

### 2. CKD Staging (KDIGO 2024 Guidelines)
Automatically assigns G-stages (G1–G5) based on eGFR:
- **Stage 1 (G1)**: eGFR ≥ 90 (Normal)
- **Stage 2 (G2)**: eGFR 60-89 (Mildly decreased)
- **Stage 3 (G3a/b)**: eGFR 30-59 (Moderate)
- **Stage 4 (G4)**: eGFR 15-29 (Severe)
- **Stage 5 (G5)**: eGFR < 15 (Kidney Failure)

---

## 🤖 Machine Learning Performance

Our model was trained on the UCI repository (400 records) with advanced preprocessing:
- **Imputation**: KNN Imputer (k=5) for sophisticated handling of clinical "NaN" values.
- **Balancing**: SMOTE technique to ensure high sensitivity to minority CKD cases.
- **Scaling**: RobustScaler to handle clinical outliers without bias.

| Metric | Accuracy | Precision | Recall | ROC-AUC |
|--------|----------|-----------|--------|---------|
| **Primary Model (RF)** | 98.75% | 100% | 96.67% | **1.00** |

### 🔍 Explainable AI Suite
We provide dual explanations for every prediction to ensure clinical trust:
- **SHAP (Game Theory based)**: Provides mathematically exact global impact of each biomarker.
- **LIME (Model Agnostic)**: Provides local, intuitive explanations around the specific patient case.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- [Homebrew](https://brew.sh/) (Mac users, for `libomp`)

### 2. Clone and Environment
```bash
git clone https://github.com/Durga0109/ckd_Prediction.git
cd ckd_Prediction/"using-uci-dataset 2/using-uci-dataset"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Mac users: Required for XGBoost
brew install libomp

# Install Python requirements
pip install -r requirements.txt
```

### 4. Generate Machine Learning Models
New clones do not include binary models. You must train them locally first:
```bash
python3 ml_pipeline/train_model.py
```

### 5. Launch the Application
You will need two terminal windows:

**Terminal 1 (Backend):**
```bash
cd ckd_Prediction/"using-uci-dataset 2/using-uci-dataset"
source venv/bin/activate
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd ckd_Prediction/"using-uci-dataset 2/using-uci-dataset"
source venv/bin/activate
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app/Home.py
```

---

## 🩺 Clinical Workflow

1. **Clinician Onboarding**: Securely sign up and log in via the `Login` page.
2. **Patient Registration**: Add a patient profile with demographics in the `Registration` page.
3. **Clinical Diagnosis**:
    - Enter blood and urine lab values in the `Diagnostics` dashboard.
    - View the instant AI prediction and probability.
    - Analyze the **SHAP Importance** chart to see which biomarkers are driving the risk.
4. **Actionable Insights**:
    - Review stage-specific recommendations (e.g., "Monitor BP," "Nephrologist Referral").
    - Generate and download the **Clinical PDF Report**.
5. **Progression Tracking**: Check the `History` tab for eGFR trendlines across multiple visits.

---

## 🛠️ Tech Stack

- **ML Core**: Scikit-Learn, XGBoost, SHAP, LIME, Imbalanced-Learn (SMOTE).
- **Backend**: FastAPI (Python), SQLAlchemy ORM, Pydantic, JWT Auth, Bcrypt.
- **Frontend**: Streamlit, Plotly (Charts), Pandnas/NumPy.
- **Documentation**: fpdf2 (PDF Generation).
- **Infrastucture**: Docker, Kubernetes, AWS ECR scripts.

---

## 📜 Medical Disclaimer

**IMPORTANT: This application is for clinical decision support, NOT automated diagnosis.**
- The system is intended for use by licensed clinicians as an auxiliary tool.
- Final clinical decisions must be based on a clinician's professional judgment and local institutional standards.
- eGFR screening is a mathematical estimate and should be validated via laboratory standards.

---

## 📞 Support & License

For issues or clinical validation questions, please open an issue in the repository.
Licensed under the **MIT License**.

© 2025 CKD Prediction Project Team
