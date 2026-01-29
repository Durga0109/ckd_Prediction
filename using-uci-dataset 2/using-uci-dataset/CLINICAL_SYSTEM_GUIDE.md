# 🏥 CKD Clinical System - Operational Guide

## 🎉 Congratulations! Your System is Ready!

You have successfully upgraded your project to a **Full-Stack Clinical Application** with:
- **Backend:** FastAPI, SQLite, Authentication, ML Integration
- **Frontend:** Streamlit, Patient Dashboard, SHAP/LIME Visualization
- **AI:** XGBoost/Random Forest Model with Explainable AI

---

## 🚀 How to Run the System

You need to run **two separate terminals**: one for the backend (API) and one for the frontend (UI).

### 1️⃣ Terminal 1: Start the Backend (API)

```powershell
# Navigate to backend folder
cd "d:\Final year Project\ckd_prediction\using-uci-dataset 2\using-uci-dataset\backend"

# Start the server
python -m uvicorn app.main:app --reload --port 8000
```
✅ **Success:** You should see `Uvicorn running on http://127.0.0.1:8000`

---

### 2️⃣ Terminal 2: Start the Frontend (Dahboard)

```powershell
# Navigate to frontend folder
cd "d:\Final year Project\ckd_prediction\using-uci-dataset 2\using-uci-dataset\frontend"

# Run the app
streamlit run streamlit_app/app.py
```
✅ **Success:** A browser window will open automatically at `http://localhost:8501`

---

## 👨‍⚕️ User Workflow

### Step 1: Sign Up / Login
1. On the login page, go to the **"Sign Up"** tab.
2. Enter your details (e.g., `doctor@hospital.com`, `password123`, `Dr. Smith`).
3. Click **Sign Up**, then switch to **Login** and sign in.

### Step 2: Manage Patients
1. Go to **"Add New Patient"** in the sidebar.
2. Enter patient demographics and clinical values (e.g., Age: 45, Creatinine: 1.2).
   - *Note: Default values are pre-filled for testing.*
3. Click **Save Patient Profile**.

### Step 3: Run Prediction
1. Go to **"Predictions"** in the sidebar.
2. Select your newly created patient.
3. Click **🚀 Run Analysis**.

### Step 4: Analyze Results
1. **Diagnosis:** See if the patient has CKD and the confidence level.
2. **Features:** Check the **SHAP** graph to see *why* the model made that decision.
3. **Recommendations:** Read the AI-generated clinical advice and stage info.

---

## 📂 Project Structure

```
using-uci-dataset/
├── backend/                # FastAPI Server
│   ├── app/
│   │   ├── main.py        # Entry point
│   │   ├── models/        # Database tables
│   │   ├── routers/       # API endpoints (Auth, Patients, Preds)
│   │   └── services/      # ML Logic (SHAP, LIME)
│   └── ckd_clinical.db    # SQLite Database (Auto-created)
│
├── frontend/               # Streamlit App
│   ├── streamlit_app/
│   │   ├── app.py         # Main UI
│   │   ├── pages/         # Login, Patients, Predictions pages
│   │   └── utils/         # API connection logic
│
└── ml_models/              # Your pre-trained .pkl files
```

## 🛠 Troubleshooting

- **"Connection Error":** Ensure the Backend terminal is running!
- **"Module not found":** Run `pip install -r requirements.txt` in both backend and frontend folders.
- **"Database Locked":** Close any programs that might have the `.db` file open (like DB Browser).

---

**Ready to demo!** Good luck with your project! 🚀
