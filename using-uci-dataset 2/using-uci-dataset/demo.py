"""
Quick Demo of CKD Prediction System

Runs predictions on 3 example patients and generates visualizations
"""

import joblib
import numpy as np
from ckd_prediction_system import complete_prediction_pipeline
import os

def load_trained_models():
    """Load all trained models and preprocessors"""
    print("\n" + "="*80)
    print("📂 Loading trained models and preprocessors...")
    print("="*80)
    
    try:
        model = joblib.load('ckd_best_model.pkl')
        print("   ✅ Model loaded")
        
        scaler = joblib.load('ckd_scaler.pkl')
        print("   ✅ Scaler loaded")
        
        feature_names = joblib.load('ckd_feature_names.pkl')
        print("   ✅ Feature names loaded")
        
        label_encoders = joblib.load('ckd_label_encoders.pkl')
        print("   ✅ Label encoders loaded")
        
        print("\n✅ All models loaded successfully!")
        
        return model, scaler, feature_names, label_encoders
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n⚠️  Please run 'python train_model.py' first!")
        return None, None, None, None


def example_patient_1():
    """High-risk CKD patient"""
    return {
        'age': 48, 'bp': 80, 'sg': 1.020, 'al': 1, 'su': 0,
        'bgr': 121, 'bu': 36, 'sc': 1.2, 'sod': 137, 'pot': 4.5,
        'hemo': 15.4, 'pcv': 44, 'wbcc': 7800, 'rbcc': 5.2,
        'rbc': 'normal', 'pc': 'normal', 'pcc': 'notpresent',
        'ba': 'notpresent', 'htn': 'yes', 'dm': 'yes', 'cad': 'no',
        'appet': 'good', 'pe': 'no', 'ane': 'no',
        'sex': 'male'
    }


def example_patient_2():
    """Severe CKD patient"""
    return {
        'age': 62, 'bp': 90, 'sg': 1.010, 'al': 4, 'su': 3,
        'bgr': 180, 'bu': 87, 'sc': 5.2, 'sod': 128, 'pot': 5.8,
        'hemo': 9.8, 'pcv': 28, 'wbcc': 12000, 'rbcc': 3.2,
        'rbc': 'abnormal', 'pc': 'abnormal', 'pcc': 'present',
        'ba': 'present', 'htn': 'yes', 'dm': 'yes', 'cad': 'yes',
        'appet': 'poor', 'pe': 'yes', 'ane': 'yes',
        'sex': 'female'
    }


def example_patient_3():
    """Healthy patient (low risk)"""
    return {
        'age': 35, 'bp': 70, 'sg': 1.020, 'al': 0, 'su': 0,
        'bgr': 95, 'bu': 18, 'sc': 0.9, 'sod': 140, 'pot': 4.0,
        'hemo': 14.5, 'pcv': 42, 'wbcc': 7000, 'rbcc': 5.0,
        'rbc': 'normal', 'pc': 'normal', 'pcc': 'notpresent',
        'ba': 'notpresent', 'htn': 'no', 'dm': 'no', 'cad': 'no',
        'appet': 'good', 'pe': 'no', 'ane': 'no',
        'sex': 'female'
    }


def main():
    """Main demo function"""
    
    print("\n" + "="*80)
    print("         🏥 CKD PREDICTION SYSTEM - QUICK DEMO")
    print("="*80)
    
    # Load models
    model, scaler, feature_names, label_encoders = load_trained_models()
    
    if model is None:
        return
    
    # Example patients
    examples = [
        ("Patient 1: High Risk CKD", example_patient_1()),
        ("Patient 2: Severe CKD", example_patient_2()),
        ("Patient 3: Healthy (Low Risk)", example_patient_3())
    ]
    
    # Process each example
    for i, (description, patient_data) in enumerate(examples, 1):
        print("\n\n" + "="*80)
        print(f"         EXAMPLE {i}: {description}")
        print("="*80)
        
        # Run complete pipeline
        results, shap_explanation = complete_prediction_pipeline(
            patient_data, 
            model, 
            scaler, 
            feature_names, 
            label_encoders
        )
        
        # Rename visualization for this example
        if os.path.exists('patient_shap_report.png'):
            target_file = f'patient_{i}_shap_report.png'
            # Remove old file if it exists
            if os.path.exists(target_file):
                os.remove(target_file)
            os.rename('patient_shap_report.png', target_file)
            print(f"   📊 Visualization saved as: {target_file}")
    
    print("\n\n" + "="*80)
    print("✅ ALL EXAMPLES COMPLETED!")
    print("="*80)
    
    print("\n📁 Generated Files:")
    print("   - patient_1_shap_report.png (High Risk CKD)")
    print("   - patient_2_shap_report.png (Severe CKD)")
    print("   - patient_3_shap_report.png (Healthy)")
    
    print("\n🎓 Summary:")
    print("   The system successfully predicted CKD status for all patients")
    print("   with detailed SHAP explanations and clinical recommendations.")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

