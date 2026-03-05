import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.auth import require_auth, init_auth
from utils.api import get_patients, make_prediction, get_patient_history
from utils.pdf_gen import generate_patient_pdf

st.set_page_config(page_title="Prediction Dashboard", page_icon="🔮", layout="wide")
init_auth()
require_auth()

st.title("🔮 Clinical Visit & Prediction Dashboard")

# 1. Patient Selection
patients = get_patients()
if not patients:
    st.warning("No patients found. Please register a patient in 'Patient Profile' first.")
    st.stop()

# Use session state to remember selected patient (helpful for redirects)
default_idx = 0
if "selected_pid" in st.session_state:
    for i, p in enumerate(patients):
        if p["id"] == st.session_state.selected_pid:
            default_idx = i
            break

selected_patient_id = st.selectbox(
    "Select Patient",
    options=[p["id"] for p in patients],
    index=default_idx,
    format_func=lambda x: next((p["full_name"] for p in patients if p["id"] == x), f"ID: {x}")
)

# Fetch data for selected patient
patient = next((p for p in patients if p["id"] == selected_patient_id), None)
history = get_patient_history(selected_patient_id)

if patient:
    st.sidebar.markdown(f"### 📋 Patient: {patient['full_name']}")
    st.sidebar.write(f"Age: {patient['age']} | Sex: {patient['sex']}")

# SMART PRE-FILLING: Use latest prediction data if available, otherwise use base profile
latest_data = patient.copy()
if history:
    latest_data = history[0].get('input_data', patient.copy())

# 2. Visit Entry Form
st.markdown("### 🧪 Step 2: Enter Medical Test Report")
st.caption("Update the parameters below from the laboratory report. Reference ranges are provided for guidance.")

# Date for the visit
visit_date = st.date_input("Visit Date", value=datetime.now(), key="v_date_box")

with st.form("visit_form"):
    tab1, tab2, tab3 = st.tabs(["🩸 Blood Tests & Vitals", "🧬 Kidney Markers", "🩺 Lifestyle & Urinalysis"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        bp = c1.number_input("Blood Pressure (Normal: 80 mm/Hg)", value=float(latest_data.get("bp", 80)))
        hemo = c2.number_input("Hemoglobin (Normal: 12-17 gms/dL)", value=float(latest_data.get("hemo", 15.0)))
        bgr = c3.number_input("Blood Glucose (Normal: 70-140 mg/dL)", value=float(latest_data.get("bgr", 120)))
        
        c4, c5, c6 = st.columns(3)
        pcv = c4.number_input("Packed Cell Volume (Normal: 35-50%)", value=float(latest_data.get("pcv", 44)))
        rbcc = c5.number_input("Red Blood Cell (Normal: 4.5-6.0)", value=float(latest_data.get("rbcc", 5.2)))
        wbcc = c6.number_input("White Blood Cell (Normal: 4500-11000)", value=float(latest_data.get("wbcc", 7800)))

    with tab2:
        c1, c2 = st.columns(2)
        sc = c1.number_input("Serum Creatinine (Normal: 0.6-1.2 mg/dL)", value=float(latest_data.get("sc", 1.2)), format="%.2f")
        bu = c2.number_input("Blood Urea (Normal: 10-40 mg/dL)", value=float(latest_data.get("bu", 36)))
        
        c3, c4 = st.columns(2)
        sod = c3.number_input("Sodium (Normal: 135-145 mEq/L)", value=float(latest_data.get("sod", 137)))
        pot = c4.number_input("Potassium (Normal: 3.5-5.0 mEq/L)", value=float(latest_data.get("pot", 4.5)))
        
        c5, c6, c7 = st.columns(3)
        sg = c5.selectbox("Specific Gravity (Normal: 1.005-1.025)", [1.005, 1.010, 1.015, 1.020, 1.025], index=3)
        al = c6.selectbox("Albumin (Normal: 0)", [0, 1, 2, 3, 4, 5], index=int(latest_data.get("al", 0)))
        su = c7.selectbox("Sugar (Normal: 0)", [0, 1, 2, 3, 4, 5], index=int(latest_data.get("su", 0)))

    with tab3:
        c1, c2, c3 = st.columns(3)
        rbc = c1.selectbox("Red Blood Cells", ["normal", "abnormal"], index=0 if latest_data.get("rbc") == "normal" else 1)
        pc = c2.selectbox("Pus Cell", ["normal", "abnormal"], index=0 if latest_data.get("pc") == "normal" else 1)
        pcc = c3.selectbox("Pus Cell Clumps", ["notpresent", "present"], index=0 if latest_data.get("pcc") == "notpresent" else 1)
        
        c4, c5, c6 = st.columns(3)
        ba = c4.selectbox("Bacteria", ["notpresent", "present"], index=0 if latest_data.get("ba") == "notpresent" else 1)
        htn = c5.selectbox("Hypertension", ["no", "yes"], index=0 if latest_data.get("htn") == "no" else 1)
        dm = c6.selectbox("Diabetes", ["no", "yes"], index=0 if latest_data.get("dm") == "no" else 1)
        
        c7, c8, c9 = st.columns(3)
        cad = c7.selectbox("CAD", ["no", "yes"], index=0 if latest_data.get("cad") == "no" else 1)
        appet = c8.selectbox("Appetite", ["good", "poor"], index=0 if latest_data.get("appet") == "good" else 1)
        pe = c9.selectbox("Pedal Edema", ["no", "yes"], index=0 if latest_data.get("pe") == "no" else 1)
        
        ane = st.selectbox("Anemia", ["no", "yes"], index=0 if latest_data.get("ane") == "no" else 1)

    run_btn = st.form_submit_button("🚀 Generate Prediction & Clinical Summary", type="primary", use_container_width=True)

if run_btn:
    current_visit_data = {
        "age": patient.get("age", 40), "sex": patient.get("sex", "male"), "sc": sc, "hemo": hemo, "bp": bp, "bgr": bgr, "bu": bu,
        "sod": sod, "pot": pot, "pcv": pcv, "wbcc": wbcc, "rbcc": rbcc, "sg": sg,
        "al": al, "su": su, "rbc": rbc, "pc": pc, "pcc": pcc, "ba": ba, "htn": htn,
        "dm": dm, "cad": cad, "appet": appet, "pe": pe, "ane": ane
    }
    
    with st.spinner("Analyzing laboratory values..."):
        date_str = visit_date.isoformat() if visit_date else None
        result = make_prediction(selected_patient_id, current_visit_data, visit_date=date_str)
        
        if result:
            st.success("✅ Visit Saved Successfully!")
            st.session_state.current_res = result
            st.session_state.prev_res = history[0] if history else None
            # Clear flash pid
            if "selected_pid" in st.session_state: del st.session_state.selected_pid
            st.rerun()

# 3. ANALYSIS DASHBOARD
if "current_res" in st.session_state:
    res = st.session_state.current_res
    prev = st.session_state.prev_res
    
    st.divider()
    
    col_title, col_pdf = st.columns([3, 1])
    with col_title:
        st.header("⚖️ AI Clinical Diagnosis")
    with col_pdf:
        # Generate PDF
        pdf_bytes = generate_patient_pdf(patient['full_name'], res)
        st.download_button(
            label="📄 Save as PDF",
            data=pdf_bytes,
            file_name=f"CKD_Report_{patient['full_name']}_{res.get('visit_date', '')[:10]}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.subheader(f"Test Date: {res.get('visit_date', '')[:10]}")
    
    # METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        color = "red" if res['ckd_prediction'] == "CKD" else "green"
        st.markdown(f"**Diagnosis**")
        st.markdown(f":{color}[## {res['ckd_prediction']}]")
    with m2:
        prob = res['ckd_probability'] if res['ckd_prediction'] == "CKD" else res['no_ckd_probability']
        st.metric("Model Confidence", f"{prob*100:.1f}%")
    with m3:
        e_delta = (res['egfr'] - prev['egfr']) if prev else None
        st.metric("eGFR", f"{res['egfr']} mL/min", delta=f"{e_delta:.1f}" if e_delta is not None else None, help="Estimated Glomerular Filtration Rate")
    with m4:
        st.metric("CKD Stage", f"Stage {res['ckd_stage']}")

    # RECOMMENDATIONS SECTION
    st.markdown("---")
    st.subheader("💡 Targeted Clinical Recommendations")
    st.markdown("These suggestions are generated based on the specific test values entered above.")
    recs = res.get('recommendations', [])
    if recs:
        for rec in recs:
            st.info(rec)
    
    st.warning(f"🚩 **CKD Progression Note:** {res['stage_description']}")

    # XAI EXPLANATION
    st.markdown("---")
    st.subheader("🧬 Explainable AI Analysis (XAI)")
    st.write("Below is a breakdown of which biomarkers influenced the model's decision the most for this patient.")
    
    tab_shap, tab_lime, tab_hist = st.tabs(["🎯 SHAP Risk Factors", "🧬 LIME Analysis", "📈 Progression History"])
    
    with tab_shap:
        shap_data = res.get('top_features', [])
        if shap_data:
            feat_df = pd.DataFrame(shap_data)
            fig = px.bar(feat_df, x='shap_value', y='feature', orientation='h', 
                         color='shap_value', color_continuous_scale='RdBu_r',
                         labels={"shap_value": "Impact Score", "feature": "Biomarker"},
                         title="SHAP Risk Breakdown (Red = Increases Risk, Blue = Protective)")
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **How to read this chart (SHAP):**
            *   **Red Bars:** These parameters are outside the normal range and are pushing the patient toward a CKD diagnosis.
            *   **Blue Bars:** These parameters are in a healthy state and are protecting the patient from CKD.
            *   **Interpretation:** SHAP provides a mathematically consistent breakdown based on all possible feature combinations.
            """)

    with tab_lime:
        lime_data = res.get('lime_values', {}).get('top_features', [])
        if lime_data:
            lime_df = pd.DataFrame(lime_data)
            fig_lime = px.bar(lime_df, x='lime_weight', y='feature', orientation='h', 
                             color='lime_weight', color_continuous_scale='curl',
                             labels={"lime_weight": "Weight Impact", "feature": "Biomarker"},
                             title="LIME Local Explanation (Decision Local Logic)")
            fig_lime.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
            st.plotly_chart(fig_lime, use_container_width=True)
            
            st.markdown("""
            **How to read this chart (LIME):**
            *   **Local Importance:** LIME explains why the model made *this specific* decision by perturbing the data locally.
            *   **Consistency Check:** If SHAP and LIME both highlight the same top biomarkers (e.g., Hemoglobin or SC), the diagnosis is highly reliable.
            *   **Novelty:** Providing two XAI perspectives is a significant enhancement for clinical validation.
            """)
        else:
            st.info("LIME analysis is not available for this record.")

    with tab_hist:
        if history:
            h_list = []
            for h in history:
                h_list.append({
                    "Date": h.get("visit_date", h["created_at"])[:10],
                    "Diagnosis": h["ckd_prediction"],
                    "eGFR": h["egfr"],
                    "Stage": h["ckd_stage"]
                })
            h_df = pd.DataFrame(h_list).sort_values("Date")
            
            if len(h_df) > 1:
                fig_trend = px.line(h_df, x='Date', y='eGFR', markers=True, title="eGFR Trendline")
                st.plotly_chart(fig_trend, use_container_width=True)
            
            st.dataframe(h_df, use_container_width=True, hide_index=True)
        else:
            st.info("Additional visits are required to generate trend data.")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)