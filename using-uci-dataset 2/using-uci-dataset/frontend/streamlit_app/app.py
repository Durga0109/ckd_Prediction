import streamlit as st
from utils.auth import init_auth, is_authenticated

# Page config
st.set_page_config(
    page_title="CKD Clinical System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize auth
init_auth()

# Sidebar
with st.sidebar:
    st.title("🏥 CKD Clinical System")
    
    if is_authenticated():
        st.success(f"Logged in as: {st.session_state.user_email}")
        if st.button("Logout"):
            from utils.auth import logout
            logout()
    else:
        st.info("Please login to continue")

# Main content
st.write("# Welcome to CKD Clinical Prediction System")

if not is_authenticated():
    st.markdown("""
    ### 👨‍⚕️ For Clinicians
    
    This system provides advanced AI-powered tools for Chronic Kidney Disease diagnosis and management.
    
    #### Key Features:
    - **Patient Management**: Securely store and manage patient profiles
    - **AI Prediction**: 98.75% accurate CKD prediction
    - **Explainable AI**: Understand predictions with **SHAP** and **LIME** analysis
    - **Clinical Tools**: Automated **eGFR** calculation and **CKD Staging**
    
    👈 **Please login using the sidebar menu to access the system.**
    """)
else:
    st.markdown("""
    ### 👋 Welcome back!
    
    Select a module from the sidebar to begin:
    
    - **👥 Patient List**: View and manage your patients
    - **👤 Add Patient**: Create new patient profiles
    - **🔮 Predictions**: Run AI analysis on patient data
    
    ---
    
    #### 🚀 Quick Actions
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 View All Patients", use_container_width=True):
            st.switch_page("pages/2_👥_Patients.py")
            
    with col2:
        if st.button("➕ Add New Patient", use_container_width=True):
            st.switch_page("pages/3_👤_Patient_Profile.py")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)
