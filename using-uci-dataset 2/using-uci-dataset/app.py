"""
CKD Prediction System - Streamlit Web Interface

This script creates a user-friendly web interface for the CKD prediction system
using Streamlit. Users can input patient data and get predictions with visualizations.

Usage: streamlit run streamlit_app.py
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from ckd_prediction_system import complete_prediction_pipeline

# Set page configuration
st.set_page_config(
    page_title="CKD Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0066cc;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4d4d4d;
        text-align: center;
    }
    .result-header {
        font-size: 1.8rem;
        color: #0066cc;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .danger-box {
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    """Load all required models from pickle files"""
    try:
        model = joblib.load('ckd_best_model.pkl')
        scaler = joblib.load('ckd_scaler.pkl')
        feature_names = joblib.load('ckd_feature_names.pkl')
        label_encoders = joblib.load('ckd_label_encoders.pkl')
        
        return model, scaler, feature_names, label_encoders
    
    except Exception as e:
        st.error(f"Failed to load models: {e}")
        st.warning("Please make sure you've run 'python3 train_model.py' first!")
        return None, None, None, None

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
        st.error("The following required files are missing:")
        for file in missing_files:
            st.error(f"- {file}")
        st.warning("Please run 'python3 train_model.py' first to train the model!")
        return False
    
    return True

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

def display_header():
    """Display the application header"""
    st.markdown("<h1 class='main-header'>🏥 Chronic Kidney Disease Prediction System</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Enter patient data to predict CKD status, stage, and get recommendations</h2>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ About this application"):
        st.markdown("""
        This application predicts Chronic Kidney Disease (CKD) using machine learning based on 25 clinical parameters.
        
        ### Features:
        - **CKD Prediction:** Binary classification (CKD or Not CKD) with probability
        - **CKD Stage Determination:** Stage 0-5 based on calculated eGFR
        - **Feature Explanation:** Which factors affect the prediction most (using SHAP)
        - **Clinical Recommendations:** What actions the patient should take
        
        ### Model Performance:
        - **ROC-AUC:** 100%
        - **Accuracy:** 98.75%
        - **Precision:** 100%
        - **Recall:** 96.67%
        - **F1-Score:** 98.31%
        
        ### Medical Disclaimer:
        This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.
        """)

def input_patient_data():
    """Get patient data from user input via Streamlit UI"""
    patient_data = {}
    default_patient = get_default_patient()
    
    st.sidebar.markdown("## 📋 Patient Information")
    
    # Use example data button
    use_example = st.sidebar.selectbox(
        "Choose an example patient or enter your own data:",
        ["Enter your own data", "Example 1: High-Risk CKD", "Example 2: Severe CKD", "Example 3: Healthy Patient"]
    )
    
    if use_example == "Example 1: High-Risk CKD":
        patient_data = default_patient.copy()
        st.sidebar.info("Using Example 1: 48-year-old male with diabetes and hypertension")
    
    elif use_example == "Example 2: Severe CKD":
        patient_data = {
            'age': 62, 'bp': 90, 'sg': 1.010, 'al': 4, 'su': 3,
            'bgr': 180, 'bu': 87, 'sc': 5.2, 'sod': 128, 'pot': 5.8,
            'hemo': 9.8, 'pcv': 28, 'wbcc': 12000, 'rbcc': 3.2,
            'rbc': 'abnormal', 'pc': 'abnormal', 'pcc': 'present',
            'ba': 'present', 'htn': 'yes', 'dm': 'yes', 'cad': 'yes',
            'appet': 'poor', 'pe': 'yes', 'ane': 'yes',
            'sex': 'female'
        }
        st.sidebar.info("Using Example 2: 62-year-old female with severe CKD")
    
    elif use_example == "Example 3: Healthy Patient":
        patient_data = {
            'age': 35, 'bp': 70, 'sg': 1.020, 'al': 0, 'su': 0,
            'bgr': 95, 'bu': 18, 'sc': 0.9, 'sod': 140, 'pot': 4.0,
            'hemo': 14.5, 'pcv': 42, 'wbcc': 7000, 'rbcc': 5.0,
            'rbc': 'normal', 'pc': 'normal', 'pcc': 'notpresent',
            'ba': 'notpresent', 'htn': 'no', 'dm': 'no', 'cad': 'no',
            'appet': 'good', 'pe': 'no', 'ane': 'no',
            'sex': 'female'
        }
        st.sidebar.info("Using Example 3: 35-year-old healthy female")
    
    else:
        # Patient details - Demographics
        st.sidebar.markdown("### Demographics")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            patient_data['age'] = st.number_input("Age (years)", 
                                                min_value=1, max_value=120, 
                                                value=default_patient['age'])
        with col2:
            patient_data['sex'] = st.selectbox("Sex (for eGFR calculation)", 
                                            ["male", "female"], 
                                            index=0 if default_patient['sex'] == 'male' else 1)
        
        # Patient details - Critical Values
        st.sidebar.markdown("### ⚠️ Critical Values")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            patient_data['sc'] = st.number_input("Serum Creatinine (mg/dL)", 
                                                min_value=0.1, max_value=20.0, 
                                                value=default_patient['sc'],
                                                step=0.1,
                                                help="Critical for eGFR calculation")
        with col2:
            patient_data['hemo'] = st.number_input("Hemoglobin (gms/dL)", 
                                                min_value=3.0, max_value=25.0, 
                                                value=default_patient['hemo'],
                                                step=0.1)
        
        # Patient details - Blood Tests
        st.sidebar.markdown("### Blood Tests")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            patient_data['bp'] = st.number_input("Blood Pressure (mm/Hg)", 
                                                min_value=40, max_value=250, 
                                                value=default_patient['bp'])
            patient_data['bgr'] = st.number_input("Blood Glucose (mg/dL)", 
                                                min_value=10, max_value=1000, 
                                                value=default_patient['bgr'])
            patient_data['bu'] = st.number_input("Blood Urea (mg/dL)", 
                                                min_value=1, max_value=500, 
                                                value=default_patient['bu'])
        with col2:
            patient_data['sod'] = st.number_input("Sodium (mEq/L)", 
                                                min_value=100, max_value=180, 
                                                value=default_patient['sod'])
            patient_data['pot'] = st.number_input("Potassium (mEq/L)", 
                                                min_value=2.0, max_value=10.0, 
                                                value=default_patient['pot'],
                                                step=0.1)
            patient_data['pcv'] = st.number_input("Packed Cell Volume (%)", 
                                                min_value=10, max_value=70, 
                                                value=default_patient['pcv'])
        
        # Patient details - Urine Tests
        st.sidebar.markdown("### Urine Tests")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            patient_data['sg'] = st.number_input("Specific Gravity", 
                                                min_value=1.000, max_value=1.050, 
                                                value=default_patient['sg'],
                                                step=0.001,
                                                format="%.3f")
            patient_data['al'] = st.number_input("Albumin (0-5)", 
                                                min_value=0, max_value=5, 
                                                value=default_patient['al'])
        with col2:
            patient_data['su'] = st.number_input("Sugar (0-5)", 
                                                min_value=0, max_value=5, 
                                                value=default_patient['su'])
            patient_data['rbc'] = st.selectbox("Red Blood Cells", 
                                            ["normal", "abnormal"], 
                                            index=0 if default_patient['rbc'] == 'normal' else 1)
        
        # Patient details - Other Tests
        st.sidebar.markdown("### Other Tests")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            patient_data['wbcc'] = st.number_input("White Blood Cell Count", 
                                                min_value=1000, max_value=50000, 
                                                value=default_patient['wbcc'],
                                                step=100)
            patient_data['rbcc'] = st.number_input("Red Blood Cell Count", 
                                                min_value=1.0, max_value=10.0, 
                                                value=default_patient['rbcc'],
                                                step=0.1)
            patient_data['pc'] = st.selectbox("Pus Cell", 
                                            ["normal", "abnormal"], 
                                            index=0 if default_patient['pc'] == 'normal' else 1)
            patient_data['pcc'] = st.selectbox("Pus Cell Clumps", 
                                            ["notpresent", "present"], 
                                            index=0 if default_patient['pcc'] == 'notpresent' else 1)
        with col2:
            patient_data['ba'] = st.selectbox("Bacteria", 
                                            ["notpresent", "present"], 
                                            index=0 if default_patient['ba'] == 'notpresent' else 1)
            patient_data['appet'] = st.selectbox("Appetite", 
                                                ["good", "poor"], 
                                                index=0 if default_patient['appet'] == 'good' else 1)
            patient_data['pe'] = st.selectbox("Pedal Edema", 
                                            ["no", "yes"], 
                                            index=0 if default_patient['pe'] == 'no' else 1)
            patient_data['ane'] = st.selectbox("Anemia", 
                                            ["no", "yes"], 
                                            index=0 if default_patient['ane'] == 'no' else 1)
        
        # Patient details - Medical History
        st.sidebar.markdown("### Medical History")
        col1, col2, col3 = st.sidebar.columns(3)
        with col1:
            patient_data['htn'] = st.selectbox("Hypertension", 
                                            ["no", "yes"], 
                                            index=1 if default_patient['htn'] == 'yes' else 0)
        with col2:
            patient_data['dm'] = st.selectbox("Diabetes", 
                                            ["no", "yes"], 
                                            index=1 if default_patient['dm'] == 'yes' else 0)
        with col3:
            patient_data['cad'] = st.selectbox("Coronary Artery Disease", 
                                            ["no", "yes"], 
                                            index=1 if default_patient['cad'] == 'yes' else 0)
    
    return patient_data

def display_prediction_results(results, shap_explanation):
    """Display prediction results in a user-friendly format"""
    
    # Create columns for layout
    col1, col2 = st.columns([3, 2])
    
    # Extract prediction at the beginning to use throughout the function
    prediction = results['prediction']
    
    with col1:
        # Main prediction result
        if prediction == "CKD":
            st.markdown(f"<div class='danger-box'><h2>Prediction: {prediction}</h2>"
                        f"<h3>Probability: {results['ckd_probability']:.2f}%</h3>"
                        f"<h4>Confidence: {results['confidence']} | Risk Level: {results['risk_level']}</h4></div>", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='success-box'><h2>Prediction: {prediction}</h2>"
                        f"<h3>Probability: {results['no_ckd_probability']:.2f}%</h3>"
                        f"<h4>Confidence: {results['confidence']} | Risk Level: {results['risk_level']}</h4></div>", 
                        unsafe_allow_html=True)
        
        # Kidney function assessment
        st.subheader("🔬 Kidney Function Assessment")
        
        # Create a gauge chart for eGFR
        fig, ax = plt.subplots(figsize=(8, 3))
        
        # Define eGFR ranges and colors
        egfr_ranges = [0, 15, 30, 45, 60, 90, 120]
        colors = ['#FF0000', '#FF6666', '#FFCC66', '#FFFF66', '#66FF66', '#66FF66']
        
        # Create the gauge chart
        for i in range(len(egfr_ranges)-1):
            ax.barh(0, egfr_ranges[i+1]-egfr_ranges[i], left=egfr_ranges[i], height=0.5, color=colors[i])
        
        # Add the pointer
        egfr = results['egfr']
        ax.plot([egfr, egfr], [-0.5, 0.5], 'k-', linewidth=2)
        ax.plot(egfr, 0, 'ko', markersize=10)
        
        # Add a small label showing the actual eGFR-based range (regardless of prediction)
        # This helps clarify that the pointer is showing the eGFR value
        if egfr >= 90:
            eGFR_range = "Normal eGFR range"
        elif egfr >= 60:
            eGFR_range = "Mild reduction"
        elif egfr >= 45:
            eGFR_range = "Mild-moderate reduction"
        elif egfr >= 30:
            eGFR_range = "Moderate-severe reduction"
        elif egfr >= 15:
            eGFR_range = "Severe reduction"
        else:
            eGFR_range = "Kidney failure range"
            
        # For No CKD predictions, add a note about the eGFR value without mentioning stage
        if prediction == "No CKD":
            # Don't use the word "Stage" for No CKD predictions to avoid confusion
            ax.text(egfr, -0.7, eGFR_range, ha='center', fontsize=8, 
                   color='gray', style='italic')
        
        # Determine which stage area to highlight based on eGFR value and prediction
        stage = results['ckd_stage']
        
        # Add labels - highlight the current stage
        stage_positions = [7.5, 22.5, 37.5, 52.5, 75, 105]
        stage_labels = ['Stage 5', 'Stage 4', 'Stage 3b', 'Stage 3a', 'Stage 2', 'Stage 1']
        
        # If prediction is "No CKD", don't highlight any stage on the gauge
        if prediction == "No CKD":
            # Create a more prominent Stage 0 box in the center-top of the chart
            # This makes it very clear this is Stage 0 regardless of eGFR value
            ax.text(egfr, 1, 'Stage 0', ha='center', fontweight='bold', color='green', 
                   bbox=dict(facecolor='lightgreen', alpha=0.5, pad=5, boxstyle='round,pad=0.5'),
                   fontsize=12)
            
            # Add regular stage labels without highlighting, but skip Stage 1 to avoid overlap
            for i, (pos, label) in enumerate(zip(stage_positions, stage_labels)):
                # Skip Stage 1 label to avoid overlap with Stage 0
                if i == 5:  # Stage 1 is at index 5
                    continue
                ax.text(pos, -1, label, ha='center', fontweight='normal', color='black')
        else:
            # For CKD prediction, highlight the appropriate stage
            # Get probability to adjust stage highlighting if needed
            ckd_probability = results['ckd_probability']
            
            # Determine the display stage based on probability and eGFR
            if ckd_probability >= 95:
                # For very high probability CKD (≥95%), highlight stage 5
                display_stage = 5
            elif ckd_probability >= 90 and stage < 4:
                # For high probability CKD (≥90%), highlight at least stage 4
                display_stage = 4
            elif ckd_probability >= 85 and stage < 3:
                # For moderately high probability CKD (≥85%), highlight at least stage 3
                display_stage = 3
            else:
                display_stage = stage
                
            for i, (pos, label) in enumerate(zip(stage_positions, stage_labels)):
                # Determine if this is the current stage
                is_current = False
                if display_stage == 5 and i == 0:
                    is_current = True
                elif display_stage == 4 and i == 1:
                    is_current = True
                elif display_stage == 3 and label == 'Stage 3b' and egfr < 45:
                    is_current = True
                elif display_stage == 3 and label == 'Stage 3a' and (egfr >= 45 or ckd_probability >= 85):
                    is_current = True
                elif display_stage == 2 and i == 4 and ckd_probability < 85:  # Only if not high probability
                    is_current = True
                elif display_stage == 1 and i == 5 and ckd_probability < 85:  # Only if not high probability
                    is_current = True
                
                # Set font weight and color based on current stage
                weight = 'bold' if is_current else 'normal'
                color = 'red' if is_current else 'black'
                ax.text(pos, -1, label, ha='center', fontweight=weight, color=color)
        
        # Set limits and remove axes
        ax.set_xlim(0, 120)
        ax.set_ylim(-1.5, 1.5)  # Increased upper limit to accommodate Stage 0 label
        ax.axis('off')
        
        # Add title and eGFR value
        ax.set_title(f'eGFR: {egfr} mL/min/1.73m²')
        
        st.pyplot(fig)
        
        # Display stage information based on eGFR, prediction and probability
        stage = results['ckd_stage']
        egfr = results['egfr']
        ckd_probability = results['ckd_probability']
        
        # Determine the correct stage based on prediction, probability and eGFR
        if prediction == "No CKD":
            # If prediction is No CKD, show Stage 0
            display_stage = 0
            stage_description = "No CKD - Normal kidney function"
        else:
            # For CKD prediction, adjust stage based on probability if needed
            if ckd_probability >= 95:
                # For very high probability CKD (≥95%), set to stage 5
                display_stage = 5
                stage_description = "Stage 5 (G5): Kidney failure (end-stage)"
                # Note: This is an override based on very high probability despite eGFR
            elif ckd_probability >= 90 and stage < 4:
                # For high probability CKD (≥90%), ensure stage is at least 4
                display_stage = 4
                stage_description = "Stage 4 (G4): Severely decreased kidney function"
                # Note: This is an override based on high probability despite eGFR
            elif ckd_probability >= 85 and stage < 3:
                # For moderately high probability CKD (≥85%), ensure stage is at least 3
                display_stage = 3
                stage_description = "Stage 3a (G3a): Mild to moderately decreased kidney function"
                # Note: This is an override based on high probability despite eGFR
            else:
                # Use the stage based on eGFR
                display_stage = stage
                stage_description = results['stage_description']
        
        # Display the appropriate box based on the stage
        if display_stage >= 3:
            # For high stages, show probability-based adjustment note if applicable
            probability_note = ""
            if ckd_probability >= 95 and results['ckd_stage'] < 5:
                probability_note = f"<p><em>Note: Stage adjusted to 5 due to very high CKD probability ({ckd_probability:.1f}%)</em></p>"
            elif ckd_probability >= 90 and results['ckd_stage'] < 4:
                probability_note = f"<p><em>Note: Stage adjusted to 4 due to high CKD probability ({ckd_probability:.1f}%)</em></p>"
            elif ckd_probability >= 85 and results['ckd_stage'] < 3:
                probability_note = f"<p><em>Note: Stage adjusted to 3 due to elevated CKD probability ({ckd_probability:.1f}%)</em></p>"
                
            st.markdown(f"<div class='danger-box'>"
                        f"<h3>CKD Stage: {display_stage}</h3>"
                        f"<p>{stage_description}</p>"
                        f"{probability_note}"
                        f"</div>", 
                        unsafe_allow_html=True)
        elif display_stage > 0:
            st.markdown(f"<div class='warning-box'>"
                        f"<h3>CKD Stage: {display_stage}</h3>"
                        f"<p>{stage_description}</p>"
                        f"</div>", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='success-box'>"
                        f"<h3>CKD Stage: {display_stage}</h3>"
                        f"<p>{stage_description}</p>"
                        f"</div>", 
                        unsafe_allow_html=True)
    
    with col2:
        # Clinical recommendations
        st.subheader("🎯 Clinical Recommendations")
        for i, rec in enumerate(results['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
    
    # SHAP explanation
    st.subheader("💡 Feature Importance (SHAP Analysis)")
    
    # Create two columns for feature importance
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Check if SHAP visualization exists
        if os.path.exists('patient_shap_report.png'):
            image = Image.open('patient_shap_report.png')
            st.image(image, caption='SHAP Feature Importance', width='stretch')
        else:
            st.warning("SHAP visualization not found. Please run the prediction first.")
    
    with col2:
        # Display top features table
        st.write("Top 10 Features Affecting Prediction:")
        
        # Format the top features data
        top_features = shap_explanation['top_features']
        
        # Convert all values to strings to avoid type issues with Arrow
        top_features_df = pd.DataFrame({
            'Feature': top_features['feature'],
            'Impact': top_features['impact_direction'],
            'Value': [str(val) for val in top_features['feature_value']],
            'SHAP Value': abs(top_features['shap_value'])
        })
        
        # Display the table
        st.dataframe(top_features_df.style.format({'SHAP Value': '{:.4f}'}))

def main():
    """Main function"""
    # Display header
    display_header()
    
    # Check if models exist
    if not check_models_exist():
        return
    
    # Load models
    model, scaler, feature_names, label_encoders = load_models()
    if model is None:
        return
    
    # Get patient data from sidebar
    patient_data = input_patient_data()
    
    # Main content area
    st.markdown("## Enter patient data in the sidebar and click 'Predict' to get results")
    
    # Predict button
    predict_button = st.button("🔮 Predict CKD Status", type="primary", use_container_width=True)
    
    if predict_button:
        # Show spinner while making prediction
        with st.spinner("Making prediction..."):
            # Make prediction
            results, shap_explanation = complete_prediction_pipeline(
                patient_data, model, scaler, feature_names, label_encoders
            )
            
            # Display results
            st.markdown("<h2 class='result-header'>📊 Prediction Results</h2>", unsafe_allow_html=True)
            display_prediction_results(results, shap_explanation)
    
    # Footer
    st.markdown("---")
    st.markdown("### 📚 About the Model")
    st.markdown("""
    This model was trained on the UCI Chronic Kidney Disease dataset with 400 patients.
    - **Algorithm:** Random Forest
    - **Performance:** 98.75% accuracy, 100% ROC-AUC
    - **eGFR Formula:** CKD-EPI 2021 equation (race-free)
    - **Staging Guidelines:** KDIGO 2024
    """)
    
    st.markdown("### ⚠️ Medical Disclaimer")
    st.markdown("""
    This system is for educational and research purposes only. 
    Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.
    """)

if __name__ == "__main__":
    main()
