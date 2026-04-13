import streamlit as st
import pandas as pd
from utils.auth import require_auth, init_auth
from utils.api import get_patients

st.set_page_config(page_title="Patient Records - CKD System", page_icon="🏥", layout="wide")
init_auth()
require_auth()

st.header("Clinical Patient Record Management")

# Fetch patients
patients = get_patients()

if not patients:
    st.info("No patient records identified in the system. Please register a new patient.")
    if st.button("Register New Patient", type="primary"):
        st.switch_page("pages/3_Registration.py")
else:
    # Key clinical metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Enrolled Patients", len(patients))
    
    # Display patients table
    df = pd.DataFrame(patients)
    
    # Select and rename columns for professional display
    display_mapping = {
        "id": "Patient Identifier",
        "full_name": "Full Legal Name",
        "age": "Age",
        "sex": "Gender",
        "contact_number": "Primary Contact",
        "created_at": "Registration Date"
    }
    
    st.markdown("### Patient Registry")
    st.dataframe(
        df[list(display_mapping.keys())].rename(columns=display_mapping),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Registration Date": st.column_config.DatetimeColumn("Date of Registration", format="D MMM YYYY"),
        }
    )
    
    st.divider()
    
    # Action interface
    st.subheader("Clinical Actions")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        selected_patient_id = st.selectbox(
            "Select Patient for Review or Analysis",
            options=[p["id"] for p in patients],
            format_func=lambda x: next((p["full_name"] for p in patients if p["id"] == x), f"ID: {x}")
        )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Modify Clinical Profile", use_container_width=True):
            st.session_state.edit_patient_id = selected_patient_id
            st.switch_page("pages/3_Registration.py")
            
    with col2:
        if st.button("Execute Diagnostic Analysis", use_container_width=True, type="primary"):
            st.session_state.predict_patient_id = selected_patient_id
            st.switch_page("pages/4_Diagnostics.py")
