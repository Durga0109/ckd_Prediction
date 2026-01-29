"""
CKD Prediction System - Test Script

This script:
1. Loads the trained model from pickle files
2. Takes user input for patient data
3. Makes predictions and displays results

Usage: python3 test.py
"""

import joblib
import numpy as np
import pandas as pd
import os
from ckd_prediction_system import complete_prediction_pipeline

def check_models_exist():
    """Check if all required model files exist"""
    required_files = [
        'ckd_best_model.pkl',
        'ckd_scaler.pkl',
        'ckd_feature_names.pkl',
        'ckd_label_encoders.pkl'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("\n❌ ERROR: The following required files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n⚠️  Please run 'python3 train_model.py' first to train the model!")
        return False
    
    return True

def load_models():
    """Load all required models from pickle files"""
    print("\n📂 Loading trained models...")
    
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
    
    except Exception as e:
        print(f"\n❌ ERROR: Failed to load models: {e}")
        return None, None, None, None

def get_numerical_input(prompt, default=None, min_val=None, max_val=None):
    """Get numerical input with validation"""
    default_str = f" [{default}]" if default is not None else ""
    
    while True:
        try:
            value_str = input(f"{prompt}{default_str}: ")
            
            if value_str == "" and default is not None:
                return default
            
            value = float(value_str)
            
            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}. Please try again.")
                continue
                
            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}. Please try again.")
                continue
                
            return value
            
        except ValueError:
            print("❌ Please enter a valid number.")

def get_categorical_input(prompt, options, default=None):
    """Get categorical input with validation"""
    options_lower = [opt.lower() for opt in options]
    default_str = f" [{default}]" if default is not None else ""
    options_str = "/".join(options)
    
    while True:
        value = input(f"{prompt} ({options_str}){default_str}: ")
        
        if value == "" and default is not None:
            return default
        
        if value.lower() in options_lower:
            # Return with the original case from options
            index = options_lower.index(value.lower())
            return options[index]
        
        print(f"❌ Invalid choice. Please enter one of: {options_str}")

def get_patient_data():
    """Get all patient data from user input"""
    print("\n" + "="*80)
    print("                🏥 PATIENT DATA INPUT")
    print("="*80)
    print("\nPlease provide the following patient information.")
    print("Press Enter to use default values shown in brackets.")
    
    patient_data = {}
    
    # Numerical features
    print("\n📊 NUMERICAL FEATURES:")
    print("-" * 60)
    
    patient_data['age'] = get_numerical_input("Age (years)", 48, 1, 120)
    patient_data['bp'] = get_numerical_input("Blood Pressure (mm/Hg)", 80, 40, 250)
    patient_data['sg'] = get_numerical_input("Specific Gravity", 1.020, 1.000, 1.050)
    patient_data['al'] = get_numerical_input("Albumin level (0-5)", 1, 0, 5)
    patient_data['su'] = get_numerical_input("Sugar level (0-5)", 0, 0, 5)
    patient_data['bgr'] = get_numerical_input("Blood Glucose Random (mg/dL)", 121, 10, 1000)
    patient_data['bu'] = get_numerical_input("Blood Urea (mg/dL)", 36, 1, 500)
    patient_data['sc'] = get_numerical_input("Serum Creatinine (mg/dL) ⚠️", 1.2, 0.1, 20)
    patient_data['sod'] = get_numerical_input("Sodium (mEq/L)", 137, 100, 180)
    patient_data['pot'] = get_numerical_input("Potassium (mEq/L)", 4.5, 2, 10)
    patient_data['hemo'] = get_numerical_input("Hemoglobin (gms/dL)", 15.4, 3, 25)
    patient_data['pcv'] = get_numerical_input("Packed Cell Volume (%)", 44, 10, 70)
    patient_data['wbcc'] = get_numerical_input("White Blood Cell Count", 7800, 1000, 50000)
    patient_data['rbcc'] = get_numerical_input("Red Blood Cell Count", 5.2, 1, 10)
    
    # Categorical features
    print("\n🏥 CATEGORICAL FEATURES:")
    print("-" * 60)
    
    patient_data['rbc'] = get_categorical_input("Red Blood Cells", ["normal", "abnormal"], "normal")
    patient_data['pc'] = get_categorical_input("Pus Cell", ["normal", "abnormal"], "normal")
    patient_data['pcc'] = get_categorical_input("Pus Cell Clumps", ["present", "notpresent"], "notpresent")
    patient_data['ba'] = get_categorical_input("Bacteria", ["present", "notpresent"], "notpresent")
    patient_data['htn'] = get_categorical_input("Hypertension", ["yes", "no"], "yes")
    patient_data['dm'] = get_categorical_input("Diabetes Mellitus", ["yes", "no"], "yes")
    patient_data['cad'] = get_categorical_input("Coronary Artery Disease", ["yes", "no"], "no")
    patient_data['appet'] = get_categorical_input("Appetite", ["good", "poor"], "good")
    patient_data['pe'] = get_categorical_input("Pedal Edema", ["yes", "no"], "no")
    patient_data['ane'] = get_categorical_input("Anemia", ["yes", "no"], "no")
    
    # Additional required
    print("\n⚠️  REQUIRED FOR eGFR CALCULATION:")
    print("-" * 60)
    
    patient_data['sex'] = get_categorical_input("Sex (required for eGFR)", ["male", "female"], "male")
    
    return patient_data

def save_results_to_file(patient_data, results, filename="test_results.txt"):
    """Save test results to a file"""
    with open(filename, "w") as f:
        f.write("="*80 + "\n")
        f.write("                  CKD PREDICTION TEST RESULTS\n")
        f.write("="*80 + "\n\n")
        
        f.write("PATIENT DATA:\n")
        f.write("-"*80 + "\n")
        
        # Numerical features
        f.write("Numerical Features:\n")
        numerical = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 
                    'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc']
        for feature in numerical:
            f.write(f"   {feature}: {patient_data.get(feature, 'N/A')}\n")
        
        # Categorical features
        f.write("\nCategorical Features:\n")
        categorical = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 
                      'appet', 'pe', 'ane', 'sex']
        for feature in categorical:
            f.write(f"   {feature}: {patient_data.get(feature, 'N/A')}\n")
        
        # Results
        f.write("\n" + "="*80 + "\n")
        f.write("PREDICTION RESULTS:\n")
        f.write("-"*80 + "\n")
        
        f.write(f"Prediction: {results['prediction']}\n")
        f.write(f"CKD Probability: {results['ckd_probability']:.2f}%\n")
        f.write(f"No CKD Probability: {results['no_ckd_probability']:.2f}%\n")
        f.write(f"Confidence: {results['confidence']}\n")
        f.write(f"Risk Level: {results['risk_level']}\n\n")
        
        f.write(f"eGFR: {results['egfr']} mL/min/1.73m²\n")
        f.write(f"CKD Stage: {results['ckd_stage']}\n")
        f.write(f"Stage Description: {results['stage_description']}\n\n")
        
        f.write("Clinical Recommendations:\n")
        for i, rec in enumerate(results['recommendations'], 1):
            f.write(f"{i}. {rec}\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write(f"Results saved: {filename}\n")
        f.write(f"Visualization saved: patient_shap_report.png\n")
        f.write("="*80 + "\n")
    
    print(f"\n✅ Results saved to {filename}")

def main():
    """Main function"""
    print("\n" + "="*80)
    print("           🏥 CKD PREDICTION SYSTEM - TEST SCRIPT")
    print("="*80)
    
    # Check if models exist
    if not check_models_exist():
        return
    
    # Load models
    model, scaler, feature_names, label_encoders = load_models()
    if model is None:
        return
    
    # Get patient data
    patient_data = get_patient_data()
    
    # Make prediction
    print("\n🔮 Making prediction...")
    results, shap_explanation = complete_prediction_pipeline(
        patient_data, model, scaler, feature_names, label_encoders
    )
    
    # Save results to file
    save_results_to_file(patient_data, results)
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE!")
    print("="*80)
    print("\n📊 Results:")
    print(f"   - Text report: test_results.txt")
    print(f"   - Visualization: patient_shap_report.png")
    print("\n🔍 Next steps:")
    print("   - Review the results file")
    print("   - Check the SHAP visualization")
    print("   - Run again with different patient data")
    print("="*80)

if __name__ == "__main__":
    main()
