from fpdf import FPDF
import pandas as pd
from datetime import datetime

class PatientReportPDF(FPDF):
    def header(self):
        # Logo or Title
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Chronic Kidney Disease (CKD) Clinical Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_patient_pdf(patient_name, prediction_data):
    """
    Generate a PDF bytes object for the prediction report
    """
    pdf = PatientReportPDF()
    pdf.add_page()
    
    # 1. Patient Information
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f"Patient Name: {patient_name}", 0, 1)
    pdf.cell(0, 10, f"Visit Date: {prediction_data.get('visit_date', 'N/A')[:10]}", 0, 1)
    pdf.ln(5)

    # 2. Key Metrics
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, "Summary of Results", 1, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 8, "CKD Prediction:", 1)
    pdf.cell(0, 8, f"{prediction_data['ckd_prediction']}", 1, 1)
    
    pdf.cell(50, 8, "Probability:", 1)
    prob = prediction_data['ckd_probability'] if prediction_data['ckd_prediction'] == "CKD" else prediction_data['no_ckd_probability']
    pdf.cell(0, 8, f"{prob*100:.2f}%", 1, 1)
    
    pdf.cell(50, 8, "eGFR Value:", 1)
    pdf.cell(0, 8, f"{prediction_data['egfr']} mL/min", 1, 1)
    
    pdf.cell(50, 8, "CKD Stage:", 1)
    pdf.cell(0, 8, f"Stage {prediction_data['ckd_stage']}", 1, 1)
    
    pdf.ln(5)

    # 3. Recommendations
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, "Clinical Recommendations", 1, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 10)
    recs = prediction_data.get('recommendations', [])
    for rec in recs:
        # Check if record has markdown boldness
        clean_rec = rec.replace("**", "").replace("💓 ", "").replace("🩸 ", "").replace("⚠️ ", "").replace("🛡️ ", "").replace("🍭 ", "").replace("🍌 ", "").replace("📉 ", "").replace("💧 ", "").replace("🦠 ", "").replace("✅ ", "")
        pdf.multi_cell(0, 8, f"- {clean_rec}", 1)
    
    pdf.ln(5)

    # 4. Top SHAP Features (Explanation)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, "Top 5 Artificial Intelligence Risk Factors", 1, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(80, 8, "Feature Name", 1)
    pdf.cell(40, 8, "Impact Direction", 1)
    pdf.cell(0, 8, "SHAP Value", 1, 1)

    top_features = prediction_data.get('top_features', [])[:5]
    for feat in top_features:
        pdf.cell(80, 8, f"{feat['feature']}", 1)
        pdf.cell(40, 8, f"{feat['impact'].capitalize()}", 1)
        pdf.cell(0, 8, f"{feat['shap_value']:.4f}", 1, 1)

    return bytes(pdf.output())
