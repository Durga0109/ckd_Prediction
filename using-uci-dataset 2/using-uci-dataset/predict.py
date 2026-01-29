"""
Simple CKD Prediction Script

Enter your patient data and get predictions with explanations!

Usage: python3 predict.py
"""

import joblib
from ckd_prediction_system import complete_prediction_pipeline

def get_patient_input():
    """
    Get patient data from user with helpful prompts
    """
    print("\n" + "="*80)
    print("            🏥 CKD PREDICTION - PATIENT DATA INPUT")
    print("="*80)
    print("\nPlease provide the following patient information:")
    print("(Press Enter to use default values shown in brackets)")
    
    patient = {}
    
    # Numerical features
    print("\n📊 NUMERICAL FEATURES:")
    print("-" * 80)
    
    patient['age'] = float(input("\n1. Age (years) [48]: ") or "48")
    patient['bp'] = float(input("2. Blood Pressure (mm/Hg) [80]: ") or "80")
    patient['sg'] = float(input("3. Specific Gravity [1.020]: ") or "1.020")
    patient['al'] = float(input("4. Albumin in urine (0-5) [1]: ") or "1")
    patient['su'] = float(input("5. Sugar in urine (0-5) [0]: ") or "0")
    patient['bgr'] = float(input("6. Blood Glucose Random (mg/dL) [121]: ") or "121")
    patient['bu'] = float(input("7. Blood Urea (mg/dL) [36]: ") or "36")
    patient['sc'] = float(input("8. Serum Creatinine (mg/dL) ⚠️ Important [1.2]: ") or "1.2")
    patient['sod'] = float(input("9. Sodium (mEq/L) [137]: ") or "137")
    patient['pot'] = float(input("10. Potassium (mEq/L) [4.5]: ") or "4.5")
    patient['hemo'] = float(input("11. Hemoglobin (gms/dL) [15.4]: ") or "15.4")
    patient['pcv'] = float(input("12. Packed Cell Volume (%) [44]: ") or "44")
    patient['wbcc'] = float(input("13. White Blood Cell Count [7800]: ") or "7800")
    patient['rbcc'] = float(input("14. Red Blood Cell Count [5.2]: ") or "5.2")
    
    # Categorical features
    print("\n🏥 CATEGORICAL FEATURES:")
    print("-" * 80)
    print("Use: yes/no, normal/abnormal, present/notpresent, good/poor")
    
    patient['rbc'] = input("\n15. Red Blood Cells (normal/abnormal) [normal]: ") or "normal"
    patient['pc'] = input("16. Pus Cell (normal/abnormal) [normal]: ") or "normal"
    patient['pcc'] = input("17. Pus Cell Clumps (present/notpresent) [notpresent]: ") or "notpresent"
    patient['ba'] = input("18. Bacteria (present/notpresent) [notpresent]: ") or "notpresent"
    patient['htn'] = input("19. Hypertension (yes/no) [yes]: ") or "yes"
    patient['dm'] = input("20. Diabetes Mellitus (yes/no) [yes]: ") or "yes"
    patient['cad'] = input("21. Coronary Artery Disease (yes/no) [no]: ") or "no"
    patient['appet'] = input("22. Appetite (good/poor) [good]: ") or "good"
    patient['pe'] = input("23. Pedal Edema (yes/no) [no]: ") or "no"
    patient['ane'] = input("24. Anemia (yes/no) [no]: ") or "no"
    
    # Required for eGFR
    patient['sex'] = input("\n⚠️  25. Sex (male/female) ⚠️ REQUIRED for eGFR [male]: ") or "male"
    
    return patient


def quick_predict(age=48, bp=80, sg=1.020, al=1, su=0, 
                  bgr=121, bu=36, sc=1.2, sod=137, pot=4.5,
                  hemo=15.4, pcv=44, wbcc=7800, rbcc=5.2,
                  rbc='normal', pc='normal', pcc='notpresent',
                  ba='notpresent', htn='yes', dm='yes', cad='no',
                  appet='good', pe='no', ane='no',
                  sex='male'):
    """
    Quick prediction with default values
    
    Modify the values in the function call to test different patients!
    """
    
    # Patient data dictionary
    patient = {
        'age': age, 'bp': bp, 'sg': sg, 'al': al, 'su': su,
        'bgr': bgr, 'bu': bu, 'sc': sc, 'sod': sod, 'pot': pot,
        'hemo': hemo, 'pcv': pcv, 'wbcc': wbcc, 'rbcc': rbcc,
        'rbc': rbc, 'pc': pc, 'pcc': pcc,
        'ba': ba, 'htn': htn, 'dm': dm, 'cad': cad,
        'appet': appet, 'pe': pe, 'ane': ane,
        'sex': sex
    }
    
    # Load models
    print("\n" + "="*80)
    print("📂 Loading trained models...")
    print("="*80)
    
    model = joblib.load('ckd_best_model.pkl')
    scaler = joblib.load('ckd_scaler.pkl')
    feature_names = joblib.load('ckd_feature_names.pkl')
    label_encoders = joblib.load('ckd_label_encoders.pkl')
    
    print("✅ Models loaded successfully!")
    
    # Make prediction
    results, shap_explanation = complete_prediction_pipeline(
        patient, model, scaler, feature_names, label_encoders
    )
    
    return results, shap_explanation


def show_examples():
    """
    Show pre-defined example patients
    """
    print("\n" + "="*80)
    print("         📋 EXAMPLE PATIENTS - QUICK ACCESS")
    print("="*80)
    
    print("\n🔬 EXAMPLE 1: High-Risk CKD Patient")
    print("   Profile: 48M, Diabetes+HTN+, Cr=1.2")
    print("   Command:")
    print("   >>> from predict import quick_predict")
    print("   >>> quick_predict(age=48, sc=1.2, htn='yes', dm='yes', sex='male')")
    
    print("\n🔬 EXAMPLE 2: Severe CKD Patient")
    print("   Profile: 62F, Multiple comorbidities, Cr=5.2")
    print("   Command:")
    print("   >>> quick_predict(age=62, sc=5.2, htn='yes', dm='yes', hemo=9.8,")
    print("                     pcv=28, appet='poor', pe='yes', ane='yes', sex='female')")
    
    print("\n🔬 EXAMPLE 3: Healthy Patient")
    print("   Profile: 35F, No comorbidities, Cr=0.9")
    print("   Command:")
    print("   >>> quick_predict(age=35, sc=0.9, htn='no', dm='no', hemo=14.5,")
    print("                     pcv=42, sex='female')")
    
    print("\n" + "="*80)


def main():
    """
    Main function - Choose between interactive or quick prediction
    """
    print("\n" + "="*80)
    print("         🏥 CKD PREDICTION SYSTEM")
    print("="*80)
    
    print("\n📋 Choose an option:")
    print("\n1. Quick Prediction (use defaults)")
    print("2. Interactive Input (enter your own data)")
    print("3. Show Examples")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        # Quick prediction with default values
        print("\n" + "="*80)
        print("Using default patient data (48M with diabetes and hypertension)")
        print("="*80)
        
        results, shap_explanation = quick_predict()
        print(f"\n✅ Prediction complete! Check 'patient_shap_report.png'")
        
    elif choice == "2":
        # Interactive input
        patient = get_patient_input()
        
        print("\n" + "="*80)
        print("📂 Loading trained models...")
        print("="*80)
        
        model = joblib.load('ckd_best_model.pkl')
        scaler = joblib.load('ckd_scaler.pkl')
        feature_names = joblib.load('ckd_feature_names.pkl')
        label_encoders = joblib.load('ckd_label_encoders.pkl')
        
        print("✅ Models loaded!")
        
        results, shap_explanation = complete_prediction_pipeline(
            patient, model, scaler, feature_names, label_encoders
        )
        
        print(f"\n✅ Prediction complete! Check 'patient_shap_report.png'")
        
    elif choice == "3":
        show_examples()
        main()  # Show menu again
        
    elif choice == "4":
        print("\n👋 Thank you for using CKD Prediction System!")
        return
        
    else:
        print("\n❌ Invalid choice. Please try again.")
        main()


if __name__ == "__main__":
    main()

