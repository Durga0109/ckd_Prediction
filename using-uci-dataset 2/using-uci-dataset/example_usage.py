"""
Example Usage of CKD Prediction System

This script demonstrates how to:
1. Load trained models
2. Make predictions for new patients
3. Generate SHAP explanations
4. Create visualizations

Run this after training the model with train_model.py
"""

import joblib
import numpy as np
from ckd_prediction_system import complete_prediction_pipeline

def load_trained_models():
    """
    Load all trained models and preprocessors
    """
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
        
        target_encoder = joblib.load('ckd_target_encoder.pkl')
        print("   ✅ Target encoder loaded")
        
        print("\n✅ All models loaded successfully!")
        
        return model, scaler, feature_names, label_encoders, target_encoder
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n⚠️  Please run 'python train_model.py' first to train and save the models!")
        return None, None, None, None, None


def example_patient_1():
    """
    Example 1: High-risk CKD patient
    
    Patient Profile:
    - 48-year-old male
    - Has hypertension and diabetes
    - Elevated serum creatinine (1.2)
    - Elevated blood urea (36)
    """
    
    patient_data = {
        # Numerical features
        'age': 48,
        'bp': 80,
        'sg': 1.020,
        'al': 1,
        'su': 0,
        'bgr': 121,
        'bu': 36,
        'sc': 1.2,
        'sod': 137,
        'pot': 4.5,
        'hemo': 15.4,
        'pcv': 44,
        'wbcc': 7800,
        'rbcc': 5.2,
        
        # Categorical features
        'rbc': 'normal',
        'pc': 'normal',
        'pcc': 'notpresent',
        'ba': 'notpresent',
        'htn': 'yes',
        'dm': 'yes',
        'cad': 'no',
        'appet': 'good',
        'pe': 'no',
        'ane': 'no',
        
        # Additional required
        'sex': 'male'
    }
    
    return patient_data


def example_patient_2():
    """
    Example 2: Severe CKD patient
    
    Patient Profile:
    - 62-year-old female
    - Very high serum creatinine (5.2)
    - High blood urea (87)
    - Anemia present
    - Poor appetite
    """
    
    patient_data = {
        # Numerical features
        'age': 62,
        'bp': 90,
        'sg': 1.010,
        'al': 4,
        'su': 3,
        'bgr': 180,
        'bu': 87,
        'sc': 5.2,
        'sod': 128,
        'pot': 5.8,
        'hemo': 9.8,
        'pcv': 28,
        'wbcc': 12000,
        'rbcc': 3.2,
        
        # Categorical features
        'rbc': 'abnormal',
        'pc': 'abnormal',
        'pcc': 'present',
        'ba': 'present',
        'htn': 'yes',
        'dm': 'yes',
        'cad': 'yes',
        'appet': 'poor',
        'pe': 'yes',
        'ane': 'yes',
        
        # Additional required
        'sex': 'female'
    }
    
    return patient_data


def example_patient_3():
    """
    Example 3: Healthy patient (low risk)
    
    Patient Profile:
    - 35-year-old female
    - No comorbidities
    - Normal lab values
    """
    
    patient_data = {
        # Numerical features
        'age': 35,
        'bp': 70,
        'sg': 1.020,
        'al': 0,
        'su': 0,
        'bgr': 95,
        'bu': 18,
        'sc': 0.9,
        'sod': 140,
        'pot': 4.0,
        'hemo': 14.5,
        'pcv': 42,
        'wbcc': 7000,
        'rbcc': 5.0,
        
        # Categorical features
        'rbc': 'normal',
        'pc': 'normal',
        'pcc': 'notpresent',
        'ba': 'notpresent',
        'htn': 'no',
        'dm': 'no',
        'cad': 'no',
        'appet': 'good',
        'pe': 'no',
        'ane': 'no',
        
        # Additional required
        'sex': 'female'
    }
    
    return patient_data


def main():
    """
    Main demo function
    """
    
    print("\n" + "="*80)
    print("         🏥 CKD PREDICTION SYSTEM - DEMONSTRATION")
    print("="*80)
    
    # Load models
    model, scaler, feature_names, label_encoders, target_encoder = load_trained_models()
    
    if model is None:
        return
    
    # Example patients
    examples = [
        ("Patient 1 - High Risk CKD", example_patient_1()),
        ("Patient 2 - Severe CKD", example_patient_2()),
        ("Patient 3 - Healthy (Low Risk)", example_patient_3())
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
        import os
        if os.path.exists('patient_shap_report.png'):
            os.rename('patient_shap_report.png', f'patient_{i}_shap_report.png')
            print(f"   📊 Visualization saved as: patient_{i}_shap_report.png")
        
        # Wait for user input before next example (optional)
        if i < len(examples):
            input("\n⏸️  Press Enter to continue to next example...")
    
    print("\n\n" + "="*80)
    print("✅ ALL EXAMPLES COMPLETED!")
    print("="*80)
    
    print("\n📁 Generated Files:")
    print("   - patient_1_shap_report.png (High Risk CKD)")
    print("   - patient_2_shap_report.png (Severe CKD)")
    print("   - patient_3_shap_report.png (Healthy)")
    
    print("\n🎓 Next Steps:")
    print("   1. Review the generated SHAP visualizations")
    print("   2. Modify patient data to test different scenarios")
    print("   3. Integrate the system into your application")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

