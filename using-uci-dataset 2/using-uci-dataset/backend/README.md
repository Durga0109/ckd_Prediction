# 🚀 Backend Quick Start Guide

## ✅ Backend Setup Complete!

The FastAPI backend for the CKD Clinical System has been created with:
- ✅ Authentication (JWT-based login/signup)
- ✅ Patient CRUD operations
- ✅ ML predictions with SHAP + LIME
- ✅ SQLite database
- ✅ Complete API documentation

---

## 📦 Installation

### Step 1: Navigate to backend directory
```powershell
cd "d:\Final year Project\ckd_prediction\using-uci-dataset 2\using-uci-dataset\backend"
```

### Step 2: Install dependencies
```powershell
pip install -r requirements.txt
```

---

## 🚀 Running the Backend

### Start the FastAPI server:
```powershell
cd "d:\Final year Project\ckd_prediction\using-uci-dataset 2\using-uci-dataset\backend"
uvicorn app.main:app --reload
```

The server will start at: **http://localhost:8000**

---

## 📚 API Documentation

Once the server is running, access:

- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔐 API Endpoints

### Authentication
- `POST /auth/signup` - Register new clinician
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Patients (Requires Authentication)
- `POST /patients/` - Create patient
- `GET /patients/` - List all patients
- `GET /patients/{id}` - Get patient by ID
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient

### Predictions (Requires Authentication)
- `POST /predictions/` - Make prediction for patient
- `GET /predictions/patient/{patient_id}` - Get all predictions for patient
- `GET /predictions/{id}` - Get specific prediction

---

## 🧪 Testing the API

### 1. Register a Clinician
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@hospital.com",
    "password": "securepassword123",
    "full_name": "Dr. John Smith",
    "specialization": "Nephrology"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=doctor@hospital.com&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Patient (use the token from login)
```bash
curl -X POST "http://localhost:8000/patients/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Doe",
    "age": 48,
    "sex": "female",
    "contact_number": "1234567890",
    "bp": 80,
    "sc": 1.2,
    "htn": "yes",
    "dm": "yes"
  }'
```

### 4. Make a Prediction
```bash
curl -X POST "http://localhost:8000/predictions/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1
  }'
```

---

## 🗄️ Database

- **Type:** SQLite (development)
- **Location:** `backend/ckd_clinical.db`
- **Tables:** clinicians, patients, predictions

The database is created automatically on first run.

---

## 🔧 Configuration

Edit `backend/.env` to customize:
- Database URL
- JWT secret key
- Token expiration time
- ML models path

---

## ✅ Next Steps

1. **Test the API** using Swagger UI at http://localhost:8000/docs
2. **Create the frontend** to connect to this backend
3. **Deploy** using Docker or cloud services

---

**Backend is ready! 🎉**
