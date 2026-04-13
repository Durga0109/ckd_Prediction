import streamlit as st
from utils.auth import init_auth, is_authenticated

# Page config
st.set_page_config(
    page_title="CKD Clinical Decision Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize auth
init_auth()

# Sidebar
from utils.auth import render_sidebar
render_sidebar()

# Main content
st.header("Chronic Kidney Disease (CKD) Clinical Decision Support System")

if not is_authenticated():
    st.markdown("""
    ### Clinician Portal
    
    This system provides advanced diagnostic tools for Chronic Kidney Disease identification and management, leveraging validated machine learning models.
    
    #### System Capabilities:
    *   **Patient Record Management**: Centralized storage for clinical and demographic data.
    *   **Predictive Diagnostics**: High-accuracy (98.75%) algorithmic CKD risk assessment.
    *   **Interpretability Analysis**: Comprehensive model interpretability through **SHAP** and **LIME** analytics.
    *   **Renal Function Monitoring**: Automated **eGFR** calculation and standardized **CKD Staging**.
    """)
    
    if st.button("Enter Secure Clinician Portal", type="primary", use_container_width=True):
        st.switch_page("pages/1_Login.py")
    
    st.info("Authentication is required to access patient data and diagnostic modules.")
else:
    st.markdown("""
    ### Dashboard Overview
    
    Select a clinical module from the navigation menu or use the quick actions below to begin.
    
    *   **Patient Records**: View and audit existing patient longitudinal data.
    *   **New Registration**: Enroll patients and initialize clinical profiles.
    *   **Diagnostic Analysis**: Perform algorithmic assessments on laboratory results.
    
    ---
    
    #### Quick Actions
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View Patient Records", use_container_width=True):
            st.switch_page("pages/2_Patients.py")
            
    with col2:
        if st.button("Register New Patient", use_container_width=True):
            st.switch_page("pages/3_Registration.py")

    with col3:
        if st.button("View Patient Diagnostics", use_container_width=True):
            st.switch_page("pages/4_Diagnostics.py")