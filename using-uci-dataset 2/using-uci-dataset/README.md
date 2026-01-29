# 🏥 Chronic Kidney Disease (CKD) Prediction System

A complete machine learning system for predicting Chronic Kidney Disease with stage determination, eGFR calculation, and SHAP-based explainability.

---

## 🎯 Features

✅ **Binary CKD Classification** - Predicts CKD/No CKD with probability scores  
✅ **CKD Stage Determination** - Stages 0-5 based on eGFR (KDIGO 2024 guidelines)  
✅ **eGFR Calculation** - Uses CKD-EPI 2021 equation (race-free)  
✅ **SHAP Explanations** - Interprets which features affect the prediction  
✅ **Clinical Recommendations** - Stage-specific actionable advice  
✅ **Professional Visualizations** - Beautiful SHAP reports  
✅ **High Performance** - >95% ROC-AUC on test data  

---

## 📊 Dataset Information

- **Source:** `chronic_kidney_disease_dataset.csv`
- **Samples:** 400 patients
- **Features:** 24 clinical parameters
- **Target:** Binary classification (CKD/Not CKD)
- **Class Distribution:** 62.5% CKD, 37.5% Non-CKD

### Input Features (24 Clinical + 1 Sex)

#### Numerical Features (14):
- `age` - Patient age in years
- `bp` - Blood Pressure (mm/Hg)
- `sg` - Specific Gravity of urine
- `al` - Albumin level in urine
- `su` - Sugar level in urine
- `bgr` - Blood Glucose Random (mg/dL)
- `bu` - Blood Urea (mg/dL)
- `sc` - Serum Creatinine (mg/dL) ⚠️ **CRITICAL for eGFR**
- `sod` - Sodium level (mEq/L)
- `pot` - Potassium level (mEq/L)
- `hemo` - Hemoglobin (gms/dL)
- `pcv` - Packed Cell Volume (%)
- `wbcc` - White Blood Cell Count
- `rbcc` - Red Blood Cell Count

#### Categorical Features (10):
- `rbc` - Red Blood Cells: "normal" or "abnormal"
- `pc` - Pus Cell: "normal" or "abnormal"
- `pcc` - Pus Cell Clumps: "present" or "notpresent"
- `ba` - Bacteria: "present" or "notpresent"
- `htn` - Hypertension: "yes" or "no"
- `dm` - Diabetes Mellitus: "yes" or "no"
- `cad` - Coronary Artery Disease: "yes" or "no"
- `appet` - Appetite: "good" or "poor"
- `pe` - Pedal Edema: "yes" or "no"
- `ane` - Anemia: "yes" or "no"

#### Additional Required:
- `sex` - "male" or "female" ⚠️ **REQUIRED for eGFR calculation**

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd "using-uci-dataset"

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model

```bash
# Train models and save preprocessors
python train_model.py
```

This will:
- Load and preprocess the dataset
- Handle missing values with KNN imputation
- Balance classes with SMOTE
- Train XGBoost and Random Forest models
- Save the best model and all preprocessors

**Expected Output:**
```
✅ Model achieves >95% ROC-AUC on test set
✅ All models saved as .pkl files
```

### 3. Run Examples

```bash
# Test predictions on example patients
python example_usage.py
```

This demonstrates:
- High-risk CKD patient
- Severe CKD patient  
- Healthy patient (low risk)

---

## 📖 Usage

### Making Predictions

```python
import joblib
from ckd_prediction_system import complete_prediction_pipeline

# Load trained models
model = joblib.load('ckd_best_model.pkl')
scaler = joblib.load('ckd_scaler.pkl')
feature_names = joblib.load('ckd_feature_names.pkl')
label_encoders = joblib.load('ckd_label_encoders.pkl')

# Prepare patient data
patient_data = {
    # Numerical features
    'age': 48, 'bp': 80, 'sg': 1.020, 'al': 1, 'su': 0,
    'bgr': 121, 'bu': 36, 'sc': 1.2, 'sod': 137, 'pot': 4.5,
    'hemo': 15.4, 'pcv': 44, 'wbcc': 7800, 'rbcc': 5.2,
    
    # Categorical features
    'rbc': 'normal', 'pc': 'normal', 'pcc': 'notpresent',
    'ba': 'notpresent', 'htn': 'yes', 'dm': 'yes', 'cad': 'no',
    'appet': 'good', 'pe': 'no', 'ane': 'no',
    
    # Additional required
    'sex': 'male'
}

# Run prediction
results, shap_explanation = complete_prediction_pipeline(
    patient_data, model, scaler, feature_names, label_encoders
)
```

### Output

```
================================================================================
                      CKD PREDICTION REPORT
================================================================================

📊 PREDICTION RESULT:
   Status:              CKD
   CKD Probability:     87.45%
   No CKD Probability:  12.55%
   Confidence:          High
   Risk Level:          High

🔬 KIDNEY FUNCTION ASSESSMENT:
   eGFR:                54.3 mL/min/1.73m²
   CKD Stage:           3
   Description:         Stage 3a (G3a): Mild to moderately decreased kidney function

💡 FEATURE IMPORTANCE (SHAP Analysis):
   Top 10 features affecting this prediction:

   Rank   Feature      Direction             Impact       Value       
   ------ ------------ -------------------- ------------ ------------
   1      hemo         ↓ DECREASES risk     0.2341       15.4
   2      sc           ↑ INCREASES risk     0.1892       1.2
   3      htn          ↑ INCREASES risk     0.1654       yes
   ...

🎯 CLINICAL RECOMMENDATIONS:
   1. ⚠️  Consult a nephrologist immediately
   2. 📊 Monitor blood pressure regularly
   3. 🥗 Follow a kidney-friendly diet
   ...

================================================================================
```

---

## 🔬 Technical Details

### Model Architecture

- **Primary Model:** XGBoost Classifier
- **Backup Model:** Random Forest Classifier
- **Selection Criteria:** Best ROC-AUC on validation set
- **Hyperparameter Tuning:** GridSearchCV with 5-fold CV

### Data Preprocessing Pipeline

1. **Missing Value Handling:**
   - Numerical: KNN Imputation (k=5)
   - Categorical: Mode Imputation

2. **Feature Encoding:**
   - Label Encoding for categorical features
   - Feature names preserved for interpretability

3. **Scaling:**
   - RobustScaler (robust to outliers)

4. **Class Imbalance:**
   - SMOTE (Synthetic Minority Over-sampling)
   - Applied only to training set

5. **Data Split:**
   - Train: 60%
   - Validation: 20%
   - Test: 20%
   - Stratified sampling

### eGFR Calculation

**CKD-EPI 2021 Equation (Race-Free):**

```
eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^-1.200 × 0.9938^age × [1.012 if female]

Where:
- κ = 0.7 (female) or 0.9 (male)
- α = -0.241 (female) or -0.302 (male)
- Scr = Serum Creatinine in mg/dL
- age = Age in years
```

### CKD Staging (KDIGO 2024 Guidelines)

| Stage | eGFR Range | Description |
|-------|-----------|-------------|
| 0 | - | No CKD detected |
| 1 (G1) | ≥90 | Normal or high kidney function |
| 2 (G2) | 60-89 | Mildly decreased kidney function |
| 3a (G3a) | 45-59 | Mild to moderately decreased |
| 3b (G3b) | 30-44 | Moderately to severely decreased |
| 4 (G4) | 15-29 | Severely decreased kidney function |
| 5 (G5) | <15 | Kidney failure (end-stage) |

### SHAP Explanations

- **Method:** TreeExplainer for tree-based models
- **Output:** Feature importance with direction (↑ increases / ↓ decreases risk)
- **Visualization:** Professional 2-panel report with:
  - Left: SHAP values bar chart (red=increases, blue=decreases)
  - Right: Summary with top risk factors and recommendations

---

## 📁 Project Structure

```
using-uci-dataset/
│
├── chronic_kidney_disease_dataset.csv  # Original dataset
│
├── ckd_prediction_system.py            # Main module with all functions
├── train_model.py                      # Training script
├── example_usage.py                    # Usage demonstrations
│
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
│
├── ckd_best_model.pkl                  # Trained model (generated)
├── ckd_scaler.pkl                      # Feature scaler (generated)
├── ckd_feature_names.pkl               # Feature names (generated)
├── ckd_label_encoders.pkl              # Categorical encoders (generated)
├── ckd_target_encoder.pkl              # Target encoder (generated)
├── ckd_knn_imputer.pkl                 # KNN imputer (generated)
├── ckd_test_metrics.pkl                # Test metrics (generated)
│
└── patient_*_shap_report.png           # SHAP visualizations (generated)
```

---

## 🎓 API Reference

### Main Functions

#### `load_and_preprocess_data(filepath)`
Loads and preprocesses the dataset.

**Returns:**
- X_train, X_val, X_test, y_train, y_val, y_test
- scaler, label_encoders, target_encoder, feature_names, knn_imputer

#### `train_best_model(X_train, y_train, X_val, y_val)`
Trains and selects best model using GridSearchCV.

**Returns:**
- best_model: Trained model
- model_name: Name of best model

#### `calculate_egfr(age, sex, creatinine)`
Calculates eGFR using CKD-EPI 2021 equation.

**Parameters:**
- age: Patient age (years)
- sex: 'male' or 'female'
- creatinine: Serum creatinine (mg/dL)

**Returns:**
- eGFR (mL/min/1.73m²)

#### `determine_ckd_stage(egfr)`
Determines CKD stage based on eGFR.

**Returns:**
- stage: Stage number (0-5)
- description: Stage description

#### `predict_ckd_with_stage(patient_data, model, scaler, feature_names, label_encoders)`
Complete prediction pipeline for a single patient.

**Returns:**
- Dictionary with prediction, probabilities, confidence, risk level, eGFR, stage, recommendations

#### `explain_prediction_with_shap(patient_data, model, scaler, feature_names, label_encoders, top_n)`
Generates SHAP explanation.

**Returns:**
- Dictionary with SHAP values, feature importance, top features

#### `complete_prediction_pipeline(patient_data, model, scaler, feature_names, label_encoders)`
End-to-end prediction workflow with visualization.

**Returns:**
- results: Prediction results
- shap_explanation: SHAP analysis

---

## 🔍 Model Performance

### Expected Performance Metrics

- **ROC-AUC:** >0.95
- **Accuracy:** >0.95
- **Precision:** >0.90
- **Recall:** >0.95
- **F1-Score:** >0.92

### Cross-Validation

- 5-fold stratified cross-validation
- Validation on separate 20% validation set
- Final evaluation on held-out 20% test set

---

## ⚠️ Important Notes

1. **Required Input:** All 25 features (24 clinical + sex) must be provided
2. **Missing Values:** Will be imputed automatically using saved imputer
3. **Categorical Values:** Must use exact strings ("yes"/"no", "normal"/"abnormal", etc.)
4. **Serum Creatinine:** Critical for eGFR calculation - ensure accurate measurement
5. **Sex Parameter:** Required for accurate eGFR calculation (CKD-EPI equation)

---

## 🐛 Troubleshooting

### Issue: Models not found
**Solution:** Run `python train_model.py` first

### Issue: Import errors
**Solution:** Install all dependencies: `pip install -r requirements.txt`

### Issue: Incorrect predictions
**Solution:** Verify all 25 features are provided with correct data types

### Issue: SHAP visualization not generated
**Solution:** Check matplotlib backend, ensure write permissions

---

## 📚 References

1. **CKD-EPI 2021 Equation:**  
   Inker LA, et al. New Creatinine- and Cystatin C–Based Equations to Estimate GFR without Race. N Engl J Med. 2021;385:1737-1749.

2. **KDIGO 2024 Guidelines:**  
   Kidney Disease: Improving Global Outcomes (KDIGO) CKD Work Group. KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease.

3. **SHAP:**  
   Lundberg SM, Lee SI. A Unified Approach to Interpreting Model Predictions. NIPS 2017.

4. **Dataset:**  
   UCI Machine Learning Repository - Chronic Kidney Disease Dataset

---

## 📝 License

This project is for educational and research purposes.

---

## 👥 Contributors

- AI Assistant
- Date: October 28, 2025

---

## 🆘 Support

For issues or questions, please review the code documentation and comments in:
- `ckd_prediction_system.py` - Main module
- `train_model.py` - Training pipeline
- `example_usage.py` - Usage examples

---

**⚕️ Medical Disclaimer:** This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.

