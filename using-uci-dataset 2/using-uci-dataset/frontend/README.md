# 🏥 CKD Clinical System - Frontend

User-friendly Streamlit interface for clinicians to manage patients and run AI predictions.

## 🚀 Getting Started

### 1. Prerequisites
Ensure the backend is running on `http://localhost:8000`.

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the App
```powershell
streamlit run streamlit_app/app.py
```

## 📱 Features

- **🔐 Login/Signup**: Secure clinician authentication
- **👥 Patient Management**: Add, view, and edit patient profiles
- **🔮 AI Dashboard**:
  - Real-time CKD probability
  - **SHAP** Waterfall & Force plots
  - **LIME** Local interpretability
  - **eGFR** & **Staging** automatically calculated
