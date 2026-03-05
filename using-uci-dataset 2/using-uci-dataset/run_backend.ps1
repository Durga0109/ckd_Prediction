# Run this script from the project root to start the FastAPI backend
# Usage: .\run_backend.ps1

Write-Host "Starting CKD Prediction Backend..." -ForegroundColor Cyan
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
