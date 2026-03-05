# Run this script from the project root to start the Streamlit frontend
# Usage: .\run_frontend.ps1

Write-Host "Starting CKD Prediction Frontend..." -ForegroundColor Green
python -m streamlit run frontend/streamlit_app/app.py
