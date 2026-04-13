import streamlit as st
from utils.auth import require_auth, init_auth, render_sidebar
from utils.api import create_patient, update_patient, get_patients

st.set_page_config(page_title="Patient Enrollment", page_icon="🏥", layout="wide")
init_auth()
require_auth()
render_sidebar()

st.header("New Patient Enrollment & Clinical Registration")
st.markdown("### Section I: Foundation Identity")

# Check if editing existing patient
is_edit = "edit_patient_id" in st.session_state
patient_data = {}

if is_edit:
    patient_id = st.session_state.edit_patient_id
    patients = get_patients()
    patient_data = next((p for p in patients if p["id"] == patient_id), {})
    st.info(f"Modifying Clinical Profile: {patient_data.get('full_name', 'Not Specified')}")
    if st.button("Cancel & Return to Records"):
        del st.session_state.edit_patient_id
        st.switch_page("pages/2_Patients.py")

with st.form("patient_form"):
    st.subheader("Demographics & Identification")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Name", value=patient_data.get("full_name", ""))
        age = st.number_input("Age", min_value=0, max_value=120, value=patient_data.get("age", 0))
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female"], index=0 if patient_data.get("sex") == "male" else 1)
        contact = st.text_input("Contact Number", value=patient_data.get("contact_number", ""))

    # HIDDEN DEFAULT VALUES for a new profile
    defaults = {
        "bp": 80.0, "sg": 1.020, "al": 0, "su": 0, "bgr": 120.0, "bu": 36.0, "sc": 1.2,
        "sod": 137.0, "pot": 4.5, "hemo": 15.0, "pcv": 44.0, "wbcc": 7800.0, "rbcc": 5.2,
        "rbc": "normal", "pc": "normal", "pcc": "notpresent", "ba": "notpresent", "htn": "no", "dm": "no", "cad": "no",
        "appet": "good", "pe": "no", "ane": "no"
    }

    submit_label = "Update Clinical Profile" if is_edit else "Complete Enrollment & Initialize Clinical Visit"
    submit = st.form_submit_button(submit_label, use_container_width=True, type="primary")
    
    if submit:
        if not full_name:
            st.error("Submission requires a valid Patient Name.")
            st.stop()
            
        # Collect data
        output_data = {
            "full_name": full_name, "age": age, "sex": sex, "contact_number": contact,
            **defaults
        }
        
        if is_edit:
            # Preservation of existing clinical data during demographic updates
            for key in defaults.keys():
                if key in patient_data:
                    output_data[key] = patient_data[key]

            if update_patient(patient_id, output_data):
                st.success("Clinical profile successfully updated.")
                del st.session_state.edit_patient_id
                st.switch_page("pages/2_Patients.py")
            else:
                st.error("Update failed. Error communicating with clinical database.")
        else:
            new_patient = create_patient(output_data)
            if new_patient:
                st.success(f"Enrollment Successful: {full_name}")
                st.session_state.selected_pid = new_patient["id"]
                st.switch_page("pages/4_Diagnostics.py")
            else:
                st.error("Enrollment failed. Error reconciling patient data.")
