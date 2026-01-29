import streamlit as st
from utils.auth import require_auth, init_auth
from utils.api import create_patient, update_patient, get_patients

st.set_page_config(page_title="Patient Profile", page_icon="👤", layout="wide")
init_auth()
require_auth()

st.title("👤 Patient Registration")
st.markdown("### Step 1: Basic Clinical Identity")
st.info("Enter the patient's demographic details here. Clinical test results will be entered in the next step (Prediction Dashboard).")

# Check if editing existing patient
is_edit = "edit_patient_id" in st.session_state
patient_data = {}

if is_edit:
    patient_id = st.session_state.edit_patient_id
    patients = get_patients()
    patient_data = next((p for p in patients if p["id"] == patient_id), {})
    st.info(f"Modifying Profile: {patient_data.get('full_name', 'Unknown')}")
    if st.button("Cancel & Go Back"):
        del st.session_state.edit_patient_id
        st.switch_page("pages/2_👥_Patients.py")

with st.form("patient_form"):
    st.subheader("Demographics")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name", value=patient_data.get("full_name", ""), placeholder="e.g. John Doe")
        age = st.number_input("Age", min_value=0, max_value=120, value=patient_data.get("age", 40))
    with col2:
        sex = st.selectbox("Sex", ["male", "female"], index=0 if patient_data.get("sex") == "male" else 1)
        contact = st.text_input("Contact Number (Optional)", value=patient_data.get("contact_number", ""), placeholder="+1 234 567 890")

    # HIDDEN DEFAULT VALUES for a new profile (will be updated during visits)
    # We provide sensible defaults so the backend doesn't crash if they are not updated immediately
    defaults = {
        "bp": 80.0, "sg": 1.020, "al": 0, "su": 0, "bgr": 120.0, "bu": 36.0, "sc": 1.2,
        "sod": 137.0, "pot": 4.5, "hemo": 15.0, "pcv": 44.0, "wbcc": 7800.0, "rbcc": 5.2,
        "rbc": "normal", "pc": "normal", "pcc": "notpresent", "ba": "notpresent", "htn": "no", "dm": "no", "cad": "no",
        "appet": "good", "pe": "no", "ane": "no"
    }

    submit_label = "Update Profile" if is_edit else "Complete Registration & Proceed to Clinical Visit"
    submit = st.form_submit_button(submit_label, use_container_width=True, type="primary")
    
    if submit:
        if not full_name:
            st.error("Please enter a name.")
            st.stop()
            
        # Collect data
        output_data = {
            "full_name": full_name, "age": age, "sex": sex, "contact_number": contact,
            **defaults
        }
        
        if is_edit:
            # When editing only basic info, we keep the old clinical values
            for key in defaults.keys():
                if key in patient_data:
                    output_data[key] = patient_data[key]

            if update_patient(patient_id, output_data):
                st.success("Profile updated!")
                del st.session_state.edit_patient_id
                st.switch_page("pages/2_👥_Patients.py")
            else:
                st.error("Failed to update profile")
        else:
            new_patient = create_patient(output_data)
            if new_patient:
                st.success(f"Registration Successful for {full_name}!")
                # Automatically select this patient for prediction
                st.session_state.selected_pid = new_patient["id"]
                st.switch_page("pages/4_🔮_Prediction.py")
            else:
                st.error("Failed to create profile")
