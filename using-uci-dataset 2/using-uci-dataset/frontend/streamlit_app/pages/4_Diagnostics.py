import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.auth import require_auth, init_auth
from utils.api import get_patients, make_prediction, get_patient_history
from utils.pdf_gen import generate_patient_pdf

st.set_page_config(page_title="Diagnostic Analysis", page_icon="🏥", layout="wide")
init_auth()
require_auth()

st.header("Clinical Consultation & Diagnostic Assessment")

# 1. Patient Selection
patients = get_patients()
if not patients:
    st.warning("No clinical records identified. Please enroll a patient in the Registry module first.")
    st.stop()

# Session state management for patient continuity
default_idx = 0
if "selected_pid" in st.session_state:
    for i, p in enumerate(patients):
        if p["id"] == st.session_state.selected_pid:
            default_idx = i
            break

selected_patient_id = st.selectbox(
    "Active Patient Record",
    options=[p["id"] for p in patients],
    index=default_idx,
    format_func=lambda x: next((p["full_name"] for p in patients if p["id"] == x), f"ID: {x}")
)

# Patient Data Retrieval
patient = next((p for p in patients if p["id"] == selected_patient_id), None)
history = get_patient_history(selected_patient_id)

if patient:
    st.sidebar.markdown(f"**Patient Information**")
    st.sidebar.write(f"Name: {patient['full_name']}")
    st.sidebar.write(f"Age: {patient['age']} | Biological Sex: {patient['sex']}")

# Longitudinal Data pre-filling
latest_data = patient.copy()
if history:
    latest_data = history[0].get('input_data', patient.copy())

# 2. Laboratory Data Entry
st.markdown("### Section II: Laboratory Results Entry")
st.caption("Update relevant biomarkers from the latest laboratory report. Standard reference ranges are provided for clinical guidance.")

# Consultation mapping
visit_date = st.date_input("Consultation Date", value=datetime.now(), key="v_date_box")

with st.form("visit_form"):
    tab1, tab2, tab3 = st.tabs(["Hematology & Vitals", "Renal Indicators", "Clinical & Lifestyle Markers"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        bp = c1.number_input("Systolic BP (Normal: 80 mm/Hg)", value=float(latest_data.get("bp", 80)))
        hemo = c2.number_input("Hemoglobin (Normal: 12-17 gms/dL)", value=float(latest_data.get("hemo", 15.0)))
        bgr = c3.number_input("Random Blood Glucose (Ref: <140 mg/dL)", value=float(latest_data.get("bgr", 120)))
        
        c4, c5, c6 = st.columns(3)
        pcv = c4.number_input("Packed Cell Volume (Normal: 35-50%)", value=float(latest_data.get("pcv", 44)))
        rbcc = c5.number_input("Erythrocyte Count (Normal: 4.5-6.0)", value=float(latest_data.get("rbcc", 5.2)))
        wbcc = c6.number_input("Leukocyte Count (Normal: 4.5-11.0 k/uL)", value=float(latest_data.get("wbcc", 7800)))

    with tab2:
        c1, c2 = st.columns(2)
        sc = c1.number_input("Serum Creatinine (Ref: 0.6-1.2 mg/dL)", value=float(latest_data.get("sc", 1.2)), format="%.2f")
        bu = c2.number_input("Blood Urea (Ref: 10-40 mg/dL)", value=float(latest_data.get("bu", 36)))
        
        c3, c4 = st.columns(2)
        sod = c3.number_input("Sodium (Ref: 135-145 mEq/L)", value=float(latest_data.get("sod", 137)))
        pot = c4.number_input("Potassium (Ref: 3.5-5.0 mEq/L)", value=float(latest_data.get("pot", 4.5)))
        
        c5, c6, c7 = st.columns(3)
        sg = c5.selectbox("Specific Gravity (Normal: 1.005-1.025)", [1.005, 1.010, 1.015, 1.020, 1.025], index=3)
        al = c6.selectbox("Albuminuria (Grade 0-5)", [0, 1, 2, 3, 4, 5], index=int(latest_data.get("al", 0)))
        su = c7.selectbox("Glycosuria (Grade 0-5)", [0, 1, 2, 3, 4, 5], index=int(latest_data.get("su", 0)))

    with tab3:
        c1, c2, c3 = st.columns(3)
        rbc = c1.selectbox("Red Blood Cell Morphology", ["normal", "abnormal"], index=0 if latest_data.get("rbc") == "normal" else 1)
        pc = c2.selectbox("Pus Cell Presence", ["normal", "abnormal"], index=0 if latest_data.get("pc") == "normal" else 1)
        pcc = c3.selectbox("Pus Cell Clumps", ["notpresent", "present"], index=0 if latest_data.get("pcc") == "notpresent" else 1)
        
        c4, c5, c6 = st.columns(3)
        ba = c4.selectbox("Bacteriuria", ["notpresent", "present"], index=0 if latest_data.get("ba") == "notpresent" else 1)
        htn = c5.selectbox("Hypertensive Status", ["no", "yes"], index=0 if latest_data.get("htn") == "no" else 1)
        dm = c6.selectbox("Diabetic History", ["no", "yes"], index=0 if latest_data.get("dm") == "no" else 1)
        
        c7, c8, c9 = st.columns(3)
        cad = c7.selectbox("CAD / Cardiovascular Disease", ["no", "yes"], index=0 if latest_data.get("cad") == "no" else 1)
        appet = c8.selectbox("Appetite Assessment", ["good", "poor"], index=0 if latest_data.get("appet") == "good" else 1)
        pe = c9.selectbox("Peripheral Edema", ["no", "yes"], index=0 if latest_data.get("pe") == "no" else 1)
        
        ane = st.selectbox("Anemia Indicators", ["no", "yes"], index=0 if latest_data.get("ane") == "no" else 1)

    run_btn = st.form_submit_button("Initiate Algorithmic Assessment", type="primary", use_container_width=True)

if run_btn:
    current_visit_data = {
        "age": patient.get("age", 40), "sex": patient.get("sex", "male"), "sc": sc, "hemo": hemo, "bp": bp, "bgr": bgr, "bu": bu,
        "sod": sod, "pot": pot, "pcv": pcv, "wbcc": wbcc, "rbcc": rbcc, "sg": sg,
        "al": al, "su": su, "rbc": rbc, "pc": pc, "pcc": pcc, "ba": ba, "htn": htn,
        "dm": dm, "cad": cad, "appet": appet, "pe": pe, "ane": ane
    }
    
    with st.spinner("Analyzing laboratory biomarkers..."):
        date_str = visit_date.isoformat() if visit_date else None
        result = make_prediction(selected_patient_id, current_visit_data, visit_date=date_str)
        
        if result:
            st.success("Consultation record and analysis successfully saved.")
            st.session_state.current_res = result
            st.session_state.prev_res = history[0] if history else None
            # Clear selection state
            if "selected_pid" in st.session_state: del st.session_state.selected_pid
            st.rerun()

# 3. CLINICAL ANALYSIS DASHBOARD
if "current_res" in st.session_state:
    res = st.session_state.current_res
    prev = st.session_state.prev_res
    
    st.divider()
    
    col_title, col_pdf = st.columns([3, 1])
    with col_title:
        st.subheader("Algorithmic Diagnostic Summary")
    with col_pdf:
        # Generate PDF
        pdf_bytes = generate_patient_pdf(patient['full_name'], res)
        st.download_button(
            label="Generate Clinical Report (PDF)",
            data=pdf_bytes,
            file_name=f"CKD_Assessment_{patient['full_name']}_{res.get('visit_date', '')[:10]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown(f"**Assessment Date:** {res.get('visit_date', '')[:10]}")
    
    # METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        color = "#e63946" if res['ckd_prediction'] == "CKD" else "#2a9d8f"
        st.markdown(f"**Diagnostic Output**")
        st.markdown(f"<h2 style='color: {color}; margin-top: 0;'>{res['ckd_prediction']}</h2>", unsafe_allow_html=True)
    with m2:
        prob = res['ckd_probability'] if res['ckd_prediction'] == "CKD" else res['no_ckd_probability']
        st.metric("Statistical Probability", f"{prob*100:.1f}%")
    with m3:
        e_delta = (res['egfr'] - prev['egfr']) if prev else None
        st.metric("eGFR", f"{res['egfr']} mL/min", delta=f"{e_delta:.1f}" if e_delta is not None else None, help="Estimated Glomerular Filtration Rate")
    with m4:
        st.metric("Standardized CKD Stage", f"Stage {res['ckd_stage']}")

    # CLINICAL INSIGHTS SECTION
    st.markdown("---")
    st.subheader("Automated Management Insights")
    st.markdown("The following suggestions are generated based on identified biometric deviations.")
    recs = res.get('recommendations', [])
    if recs:
        for rec in recs:
            st.info(rec)
    
    st.warning(f"**Clinical Pathway Note:** {res['stage_description']}")

    # INTERPRETABILITY COMPONENT
    st.markdown("---")
    st.subheader("Interpretability Analysis (XAI)")
    st.write("Quantitative breakdown of biomarkers influencing the algorithmic decision.")
    
    tab_shap, tab_lime, tab_hist = st.tabs(["SHAP Influence Scores", "LIME Local Explanation", "Longitudinal Progression"])
    
    with tab_shap:
        shap_data = res.get('top_features', [])
        if shap_data:
            feat_df = pd.DataFrame(shap_data)
            fig = px.bar(feat_df, x='shap_value', y='feature', orientation='h', 
                         color='shap_value', color_continuous_scale='RdBu_r',
                         labels={"shap_value": "Impact Score", "feature": "Biomarker"},
                         title="SHAP Feature Weighting (Red = Increased Risk, Blue = Protective)")
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
            fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **SHAP Methodology Overview:**
            *   **Positive Impact (Red):** Markers exceeding clinical thresholds that statistically correlate with CKD progression.
            *   **Protective Impact (Blue):** Biomarkers within standard reference ranges that mitigate the probability of a CKD diagnosis.
            """)

    with tab_lime:
        lime_data = res.get('lime_values', {}).get('top_features', [])
        if lime_data:
            lime_df = pd.DataFrame(lime_data)
            fig_lime = px.bar(lime_df, x='lime_weight', y='feature', orientation='h', 
                             color='lime_weight', color_continuous_scale='curl',
                             labels={"lime_weight": "Local Weight", "feature": "Biomarker"},
                             title="LIME Local Perturbation Analysis")
            fig_lime.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
            st.plotly_chart(fig_lime, use_container_width=True)
            
            st.markdown("""
            **LIME Local Insights:**
            *   Explains the model's logic for *this specific* instance by analyzing local data perturbations.
            *   High alignment between SHAP and LIME rankings increases clinical confidence in the diagnostic output.
            """)
        else:
            st.info("Local LIME analysis not available for this session.")

    with tab_hist:
        if history and len(history) > 1:
            h_list = []
            for h in history:
                h_list.append({
                    "Consultation Date": h.get("visit_date", h["created_at"])[:10],
                    "Diagnosis": h["ckd_prediction"],
                    "eGFR": h["egfr"],
                    "Stage": h["ckd_stage"]
                })
            h_df = pd.DataFrame(h_list).sort_values("Consultation Date")
            
            fig_trend = px.line(h_df, x='Consultation Date', y='eGFR', markers=True, title="eGFR Longitudinal Trendline")
            st.plotly_chart(fig_trend, use_container_width=True)
            st.dataframe(h_df, use_container_width=True, hide_index=True)
        else:
            st.info("Additional clinical sessions are required to generate longitudinal trend data.")

# Professional Styling
st.markdown("""
<style>
    .stButton>button {
        height: 3em;
        border-radius: 4px;
    }
    .stMetric {
        border: 1px solid #e9ecef;
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)
t: 3em;
    }
</style>
""", unsafe_allow_html=True)