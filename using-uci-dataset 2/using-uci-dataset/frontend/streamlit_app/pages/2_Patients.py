import streamlit as st
import pandas as pd
from utils.auth import require_auth, init_auth, render_sidebar
from utils.api import get_patients

st.set_page_config(page_title="Patient Records - CKD System", page_icon="🏥", layout="wide")
init_auth()
require_auth()
render_sidebar()

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
        "full_name": "Name",
        "age": "Age",
        "sex": "Gender",
        "contact_number": "Contact Number",
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