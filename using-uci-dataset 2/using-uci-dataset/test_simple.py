"""
Simple CKD Prediction Test Script

This script:
1. Loads the trained model from pickle files
2. Uses default values or command line arguments
3. Makes predictions and displays results

Usage: 
- Basic: python3 test_simple.py
- With args: python3 test_simple.py --age 55 --sc 1.5 --sex female
"""

import joblib
import argparse
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

def get_default_patient():
    """Return default patient data"""
    return {
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

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Test CKD Prediction Model')
    
    # Numerical features
    parser.add_argument('--age', type=float, help='Age in years')
    parser.add_argument('--bp', type=float, help='Blood Pressure in mm/Hg')
    parser.add_argument('--sg', type=float, help='Specific Gravity')
    parser.add_argument('--al', type=float, help='Albumin level (0-5)')
    parser.add_argument('--su', type=float, help='Sugar level (0-5)')
    parser.add_argument('--bgr', type=float, help='Blood Glucose Random in mg/dL')
    parser.add_argument('--bu', type=float, help='Blood Urea in mg/dL')
    parser.add_argument('--sc', type=float, help='Serum Creatinine in mg/dL')
    parser.add_argument('--sod', type=float, help='Sodium in mEq/L')
    parser.add_argument('--pot', type=float, help='Potassium in mEq/L')
    parser.add_argument('--hemo', type=float, help='Hemoglobin in gms/dL')
    parser.add_argument('--pcv', type=float, help='Packed Cell Volume in %')
    parser.add_argument('--wbcc', type=float, help='White Blood Cell Count')
    parser.add_argument('--rbcc', type=float, help='Red Blood Cell Count')
    
    # Categorical features
    parser.add_argument('--rbc', choices=['normal', 'abnormal'], help='Red Blood Cells')
    parser.add_argument('--pc', choices=['normal', 'abnormal'], help='Pus Cell')
    parser.add_argument('--pcc', choices=['present', 'notpresent'], help='Pus Cell Clumps')
    parser.add_argument('--ba', choices=['present', 'notpresent'], help='Bacteria')
    parser.add_argument('--htn', choices=['yes', 'no'], help='Hypertension')
    parser.add_argument('--dm', choices=['yes', 'no'], help='Diabetes Mellitus')
    parser.add_argument('--cad', choices=['yes', 'no'], help='Coronary Artery Disease')
    parser.add_argument('--appet', choices=['good', 'poor'], help='Appetite')
    parser.add_argument('--pe', choices=['yes', 'no'], help='Pedal Edema')
    parser.add_argument('--ane', choices=['yes', 'no'], help='Anemia')
    
    # Additional required
    parser.add_argument('--sex', choices=['male', 'female'], help='Sex (required for eGFR)')
    
    # Output options
    parser.add_argument('--save', action='store_true', help='Save results to file')
    parser.add_argument('--output', default='test_results.txt', help='Output file name')
    
    return parser.parse_args()

def get_patient_data_from_args(args):
    """Get patient data from command line arguments"""
    patient = get_default_patient()
    
    # Update patient data with provided arguments
    for key, value in vars(args).items():
        if key in patient and value is not None:
            patient[key] = value
    
    return patient

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

def print_patient_summary(patient_data):
    """Print a summary of patient data"""
    print("\n" + "="*80)
    print("                   PATIENT DATA SUMMARY")
    print("="*80)
    
    print("\n📊 KEY VALUES:")
    print(f"   Age: {patient_data['age']} years")
    print(f"   Sex: {patient_data['sex']}")
    print(f"   Serum Creatinine: {patient_data['sc']} mg/dL")
    print(f"   Hypertension: {patient_data['htn']}")
    print(f"   Diabetes: {patient_data['dm']}")
    print(f"   Hemoglobin: {patient_data['hemo']} gms/dL")
    
    print("\n⚠️  NOTE: Using default values for parameters not specified.")
    print("   To change any value, use command line arguments.")
    print("   Example: --age 55 --sc 1.5 --sex female")
    print("="*80)

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
    
    # Parse arguments
    args = parse_arguments()
    
    # Get patient data
    patient_data = get_patient_data_from_args(args)
    
    # Print patient summary
    print_patient_summary(patient_data)
    
    # Make prediction
    print("\n🔮 Making prediction...")
    results, shap_explanation = complete_prediction_pipeline(
        patient_data, model, scaler, feature_names, label_encoders
    )
    
    # Save results to file if requested
    if args.save:
        save_results_to_file(patient_data, results, args.output)
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE!")
    print("="*80)
    print("\n📊 Results:")
    print(f"   - Visualization: patient_shap_report.png")
    if args.save:
        print(f"   - Text report: {args.output}")
    print("\n🔍 Next steps:")
    print("   - Check the SHAP visualization")
    print("   - Run again with different patient data")
    print("   - Example: python3 test_simple.py --age 62 --sc 5.2 --sex female --save")
    print("="*80)

if __name__ == "__main__":
    main()
