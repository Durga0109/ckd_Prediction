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
with st.sidebar:
    st.title("CKD Clinical System")
    
    if is_authenticated():
        st.success(f"Authenticated: {st.session_state.user_email}")
        if st.button("Sign Out", use_container_width=True):
            from utils.auth import logout
            logout()
    else:
        st.info("Authentication Required")

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
    
    **Please authenticate via the sidebar to access clinical modules.**
    """)
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Patient Records", use_container_width=True):
            st.switch_page("pages/2_Patients.py")
            
    with col2:
        if st.button("Register New Patient", use_container_width=True):
            st.switch_page("pages/3_Registration.py")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        height: 3em;
        border-radius: 5px;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)
