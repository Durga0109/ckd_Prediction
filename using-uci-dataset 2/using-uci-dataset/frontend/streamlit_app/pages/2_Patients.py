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
        
        tab_profile, tab_history, tab_trends, tab_maintenance = st.tabs(["Identity Profile", "Diagnostic History", "Clinical Progression", "System Maintenance"])
        
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
                import plotly.graph_objects as go
                
                for idx, h in enumerate(history):
                    visit_date = h.get("visit_date", h["created_at"])[:10]
                    badge = "🔴" if h['ckd_prediction'] == "CKD" else "🟢"
                    
                    with st.expander(f"{badge} Visit: {visit_date} | Result: {h['ckd_prediction']} | Stage: {h.get('ckd_stage', 'N/A')}", expanded=(idx == 0)):
                        
                        # --- Metric Row ---
                        m1, m2, m3, m4 = st.columns(4)
                        with m1:
                            st.metric("Diagnosis", h['ckd_prediction'])
                        with m2:
                            prob = max(h.get('ckd_probability', 0), h.get('no_ckd_probability', 0))
                            st.metric("Confidence", f"{prob*100:.1f}%")
                        with m3:
                            st.metric("eGFR", f"{h.get('egfr', 'N/A')} mL/min")
                        with m4:
                            st.metric("CKD Stage", h.get('ckd_stage', 'N/A'))
                        
                        # --- XAI Sub-tabs ---
                        sub_reasoning, sub_shap, sub_lime = st.tabs(["Clinical Reasoning", "SHAP Analysis", "LIME Analysis"])
                        
                        with sub_reasoning:
                            narrative = h.get('xai_narrative', {})
                            if narrative:
                                st.info(narrative.get('summary', ''))
                                drivers = narrative.get('risk_drivers', [])
                                for di, driver in enumerate(drivers):
                                    icon = "🔴" if driver['direction'] == 'Risk Factor' else "🟢"
                                    st.markdown(f"**{icon} {driver['biomarker']}** — {driver['value']} ({driver['direction']})")
                                    st.caption(driver['clinical_context'])
                                
                                agreement = narrative.get('agreement', {})
                                if agreement:
                                    overlap = agreement.get('overlap_pct', 0)
                                    if overlap >= 66:
                                        st.success(agreement.get('text', ''))
                                    elif overlap >= 33:
                                        st.warning(agreement.get('text', ''))
                                    else:
                                        st.error(agreement.get('text', ''))
                            else:
                                st.caption("Clinical reasoning not available for this visit.")
                        
                        with sub_shap:
                            shap_feats = h.get('top_features', [])
                            if shap_feats:
                                s_df = pd.DataFrame(shap_feats)
                                s_df['abs_shap'] = s_df['shap_value'].abs()
                                s_df = s_df.sort_values('abs_shap', ascending=True)
                                colors = ['#e63946' if v > 0 else '#457b9d' for v in s_df['shap_value']]
                                fig_s = go.Figure(go.Bar(
                                    x=s_df['shap_value'].tolist(),
                                    y=s_df['feature'].tolist(),
                                    orientation='h', marker_color=colors
                                ))
                                fig_s.update_layout(
                                    title="SHAP Feature Weighting",
                                    xaxis_title="Impact Score", yaxis_title="Biomarker",
                                    height=350, margin=dict(l=10, r=10, t=35, b=10)
                                )
                                st.plotly_chart(fig_s, use_container_width=True, key=f"shap_{idx}")
                            else:
                                st.caption("SHAP data not available for this visit.")
                        
                        with sub_lime:
                            lime_data = h.get('lime_values', {}).get('top_features', [])
                            if lime_data:
                                l_df = pd.DataFrame(lime_data)
                                l_df['abs_w'] = l_df['lime_weight'].abs()
                                l_df = l_df.sort_values('abs_w', ascending=True)
                                lcolors = ['#2d6a4f' if v > 0 else '#7b2cbf' for v in l_df['lime_weight']]
                                fig_l = go.Figure(go.Bar(
                                    x=l_df['lime_weight'].tolist(),
                                    y=l_df['feature'].tolist(),
                                    orientation='h', marker_color=lcolors
                                ))
                                fig_l.update_layout(
                                    title="LIME Local Perturbation",
                                    xaxis_title="Local Weight", yaxis_title="Biomarker",
                                    height=350, margin=dict(l=10, r=10, t=35, b=10)
                                )
                                st.plotly_chart(fig_l, use_container_width=True, key=f"lime_{idx}")
                                
                                lime_r2 = h.get('lime_values', {}).get('lime_score', 0)
                                st.metric("Local Fidelity (R²)", f"{lime_r2:.2f}")
                            else:
                                st.caption("LIME data not available for this visit.")
                        
                        # --- PDF Download ---
                        st.divider()
                        pdf_bytes = generate_patient_pdf(patient['full_name'], h)
                        st.download_button(
                            label="Download Full Report (PDF)",
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

        with tab_maintenance:
            st.warning("### Danger Zone")
            st.write("Deleting this record will permanently remove the patient profile and all associated diagnostic history. This action cannot be undone.")
            
            confirm_text = st.text_input(f"Type '{patient['full_name']}' to confirm deletion", placeholder=patient['full_name'])
            
            if st.button(f"Permanently Delete {patient['full_name']}", type="primary", use_container_width=True, disabled=(confirm_text != patient['full_name'])):
                from utils.api import delete_patient
                if delete_patient(selected_patient_id):
                    st.success("Record successfully purged from clinical database.")
                    st.rerun()
                else:
                    st.error("Deletion failed. Ensure you have administrative privileges.")