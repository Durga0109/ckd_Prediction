import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import require_auth, init_auth, render_sidebar
from utils.api import get_patients, get_patient_history
from utils.pdf_gen import generate_patient_pdf

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

    st.divider()

    # --- CLINICAL CASE FILE SECTION ---
    st.subheader("In-depth Clinical Case Review")
    st.caption("Select a patient to review their full clinical history, longitudinal trends, and past diagnostic reports.")

    selected_patient_id = st.selectbox(
        "Select Patient for Review",
        options=[None] + [p["id"] for p in patients],
        format_func=lambda x: "Select a patient..." if x is None else next((p["full_name"] for p in patients if p["id"] == x), f"ID: {x}")
    )

    if selected_patient_id:
        patient = next((p for p in patients if p["id"] == selected_patient_id), None)
        history = get_patient_history(selected_patient_id)
        
        tab_profile, tab_history, tab_trends = st.tabs(["Identity Profile", "Diagnostic History", "Clinical Progression"])
        
        with tab_profile:
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.write(f"**Full Name:** {patient['full_name']}")
                st.write(f"**Age:** {patient['age']}")
                st.write(f"**Biological Sex:** {patient['sex']}")
            with col_p2:
                st.write(f"**Contact:** {patient['contact_number']}")
                st.write(f"**System ID:** {patient['id']}")
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Modify Profile Details", use_container_width=True):
                    st.session_state.edit_patient_id = selected_patient_id
                    st.switch_page("pages/3_Registration.py")
            with c2:
                if st.button("Initiate New Assessment", use_container_width=True, type="primary"):
                    st.session_state.selected_pid = selected_patient_id
                    st.switch_page("pages/4_Diagnostics.py")

        with tab_history:
            if not history:
                st.info("No diagnostic history found for this patient.")
            else:
                for idx, h in enumerate(history):
                    visit_date = h.get("visit_date", h["created_at"])[:10]
                    with st.expander(f"Visit: {visit_date} | Result: {h['ckd_prediction']} | Stage: {h['ckd_stage']}"):
                        col_h1, col_h2 = st.columns([2, 1])
                        with col_h1:
                            st.write(f"**eGFR:** {h['egfr']} mL/min")
                            st.write(f"**Probability:** {max(h.get('ckd_probability', 0), h.get('no_ckd_probability', 0))*100:.1f}%")
                        with col_h2:
                            # Generate PDF for this historical visit
                            pdf_bytes = generate_patient_pdf(patient['full_name'], h)
                            st.download_button(
                                label="Download Report",
                                data=pdf_bytes,
                                file_name=f"CKD_Report_{patient['full_name']}_{visit_date}.pdf",
                                mime="application/pdf",
                                key=f"dl_{selected_patient_id}_{idx}"
                            )

        with tab_trends:
            if len(history) < 2:
                st.info("Additional clinical sessions are required to generate longitudinal trend data.")
            else:
                h_df = pd.DataFrame([{
                    "Date": h.get("visit_date", h["created_at"])[:10],
                    "eGFR": h["egfr"]
                } for h in history]).sort_values("Date")
                
                fig = px.line(h_df, x="Date", y="eGFR", markers=True, title=f"eGFR Trendline: {patient['full_name']}")
                fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="CKD Threshold (60)")
                st.plotly_chart(fig, use_container_width=True)