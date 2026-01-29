import streamlit as st
import pandas as pd
from utils.auth import require_auth, init_auth
from utils.api import get_patients

st.set_page_config(page_title="Patients - CKD System", page_icon="👥", layout="wide")
init_auth()
require_auth()

st.title("👥 Patient Management")

# Fetch patients
patients = get_patients()

if not patients:
    st.info("No patients found. Add your first patient!")
    if st.button("➕ Add New Patient"):
        st.switch_page("pages/3_👤_Patient_Profile.py")
else:
    # Key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", len(patients))
    
    # Display patients table
    df = pd.DataFrame(patients)
    
    # Select columns to display
    display_cols = ["id", "full_name", "age", "sex", "contact_number", "created_at"]
    
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "created_at": st.column_config.DatetimeColumn("Registered On", format="D MMM YYYY"),
            "full_name": "Patient Name"
        }
    )
    
    # Action buttons
    st.subheader("Actions")
    
    selected_patient_id = st.selectbox(
        "Select Patient for Details/Prediction",
        options=[p["id"] for p in patients],
        format_func=lambda x: next((p["full_name"] for p in patients if p["id"] == x), f"ID: {x}")
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Edit Profile", use_container_width=True):
            st.session_state.edit_patient_id = selected_patient_id
            st.switch_page("pages/3_👤_Patient_Profile.py")
            
    with col2:
        if st.button("🔮 Run Prediction", use_container_width=True):
            st.session_state.predict_patient_id = selected_patient_id
            st.switch_page("pages/4_🔮_Prediction.py")
