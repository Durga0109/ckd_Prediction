"""
SIMPLE EXAMPLE - How to Input Patient Data and Get Predictions

This shows the EASIEST way to use the CKD Prediction System
"""

import joblib
from ckd_prediction_system import complete_prediction_pipeline

# ============================================================================
# STEP 1: Load the trained models (do this once)
# ============================================================================

print("Loading trained models...")
model = joblib.load('ckd_best_model.pkl')
scaler = joblib.load('ckd_scaler.pkl')
feature_names = joblib.load('ckd_feature_names.pkl')
label_encoders = joblib.load('ckd_label_encoders.pkl')
print("✅ Models loaded!\n")

# ============================================================================
# STEP 2: Prepare your patient data
# ============================================================================

# Example Patient 1: High-risk CKD
patient_data = {
    # Numerical features (14 total)
    'age': 48,        # Patient age in years
    'bp': 80,         # Blood Pressure in mm/Hg
    'sg': 1.020,      # Specific Gravity
    'al': 1,          # Albumin in urine (0-5)
    'su': 0,          # Sugar in urine (0-5)
    'bgr': 121,       # Blood Glucose Random (mg/dL)
    'bu': 36,         # Blood Urea (mg/dL)
    'sc': 1.2,        # Serum Creatinine (mg/dL) ⚠️ CRITICAL!
    'sod': 137,       # Sodium (mEq/L)
    'pot': 4.5,       # Potassium (mEq/L)
    'hemo': 15.4,     # Hemoglobin (gms/dL)
    'pcv': 44,        # Packed Cell Volume (%)
    'wbcc': 7800,     # White Blood Cell Count
    'rbcc': 5.2,      # Red Blood Cell Count
    
    # Categorical features (10 total)
    'rbc': 'normal',       # Red Blood Cells: 'normal' or 'abnormal'
    'pc': 'normal',        # Pus Cell: 'normal' or 'abnormal'
    'pcc': 'notpresent',   # Pus Cell Clumps: 'present' or 'notpresent'
    'ba': 'notpresent',    # Bacteria: 'present' or 'notpresent'
    'htn': 'yes',          # Hypertension: 'yes' or 'no'
    'dm': 'yes',           # Diabetes Mellitus: 'yes' or 'no'
    'cad': 'no',           # Coronary Artery Disease: 'yes' or 'no'
    'appet': 'good',       # Appetite: 'good' or 'poor'
    'pe': 'no',            # Pedal Edema: 'yes' or 'no'
    'ane': 'no',           # Anemia: 'yes' or 'no'
    
    # Additional required
    'sex': 'male'  # ⚠️ REQUIRED for eGFR calculation: 'male' or 'female'
}

# ============================================================================
# STEP 3: Get prediction
# ============================================================================

results, shap_explanation = complete_prediction_pipeline(
    patient_data, model, scaler, feature_names, label_encoders
)

# ============================================================================
# STEP 4: Access results programmatically
# ============================================================================

print("\n" + "="*80)
print("ACCESSING RESULTS PROGRAMMATICALLY:")
print("="*80)

print(f"\n📊 PREDICTION:")
print(f"   Status: {results['prediction']}")
print(f"   CKD Probability: {results['ckd_probability']:.2f}%")
print(f"   Confidence: {results['confidence']}")
print(f"   Risk Level: {results['risk_level']}")

print(f"\n🔬 KIDNEY FUNCTION:")
print(f"   eGFR: {results['egfr']} mL/min/1.73m²")
print(f"   CKD Stage: {results['ckd_stage']}")
print(f"   Description: {results['stage_description']}")

print(f"\n💡 TOP 5 RISK FACTORS:")
top_features = shap_explanation['top_features']
for i, (idx, row) in enumerate(top_features.head(5).iterrows(), 1):
    print(f"   {i}. {row['feature']} - {row['impact_direction']} risk (Impact: {abs(row['shap_value']):.3f})")

print(f"\n🎯 RECOMMENDATIONS:")
for i, rec in enumerate(results['recommendations'][:3], 1):
    print(f"   {i}. {rec}")

print(f"\n📊 VISUALIZATION SAVED:")
print(f"   File: patient_shap_report.png")
print("="*80)

