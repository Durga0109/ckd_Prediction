# CKD Clinical Decision Support System

This project is a web-based Clinical Decision Support System (CDSS) for Chronic Kidney Disease (CKD) prediction and management. It uses machine learning to predict CKD risk from patient data and provides clinical decision support to healthcare providers.

## Features

- **Patient Management**: Add, view, and manage patient records
- **CKD Prediction**: Machine learning-based prediction of CKD risk
- **Explainable AI**: SHAP and LIME visualizations to explain predictions
- **Clinician Authentication**: Secure login and signup for healthcare providers
- **Role-Based Access**: Different access levels for clinicians
- **Data Visualization**: Interactive charts and graphs for patient data
- **Audit Trail**: Track all predictions and patient data modifications

## Tech Stack

### Frontend
- **Streamlit**: Web application framework
- **Python**: Core programming language

### Backend
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database
- **Alembic**: Database migrations
- **PyJWT**: Authentication
- **Bcrypt**: Password hashing

### Machine Learning
- **Scikit-learn**: ML models and preprocessing
- **XGBoost**: Gradient boosting for prediction
- **SHAP**: Explainable AI
- **LIME**: Local interpretable model-agnostic explanations

### Database
- **SQLite**: Development database
- **PostgreSQL**: Production database (optional)

## Project Structure

```
ckd_Prediction/
└── using-uci-dataset 2/
    └── using-uci-dataset/
        │
        ├── backend/                          # FastAPI backend service
        │   ├── app/
        │   │   ├── __init__.py
        │   │   ├── main.py                   # FastAPI app entry point
        │   │   ├── config.py                 # App configuration / settings
        │   │   ├── database.py               # SQLAlchemy engine & session
        │   │   ├── models/                   # Database ORM models
        │   │   │   ├── clinician.py
        │   │   │   ├── patient.py
        │   │   │   └── prediction.py
        │   │   ├── routers/                  # API route handlers
        │   │   │   ├── auth.py               # Authentication endpoints
        │   │   │   ├── patients.py            # Patient CRUD endpoints
        │   │   │   └── predictions.py         # Prediction endpoints
        │   │   ├── schemas/                  # Pydantic request/response schemas
        │   │   │   ├── clinician.py
        │   │   │   ├── patient.py
        │   │   │   └── prediction.py
        │   │   └── services/                 # Business logic
        │   │       ├── auth_service.py        # JWT & password helpers
        │   │       └── ml_service.py          # ML inference & XAI
        │   ├── ckd_clinical.db               # SQLite database
        │   ├── inspect_db.py                 # DB inspection utility
        │   ├── requirements.txt
        │   ├── .env.example
        │   └── README.md
        │
        ├── frontend/                         # Streamlit frontend
        │   ├── streamlit_app/
        │   │   ├── Home.py                    # Streamlit entry point
        │   │   ├── pages/
        │   │   │   ├── 1_Login.py
        │   │   │   ├── 2_Patients.py
        │   │   │   ├── 3_Registration.py
        │   │   │   └── 4_Diagnostics.py
        │   │   └── utils/
        │   │       ├── api.py                # Backend API client
        │   │       ├── auth.py               # Session / auth helpers
        │   │       └── pdf_gen.py            # PDF report generation
        │   ├── requirements.txt
        │   └── README.md
        │
        ├── deployment/                       # Docker & Kubernetes configs
        │   ├── kubernetes/
        │   │   ├── deployment.yaml
        │   │   ├── service.yaml
        │   │   └── ingress.yaml
        │   ├── scripts/
        │   │   ├── build_and_push.sh
        │   │   └── deploy_to_kubernetes.sh
        │   ├── PUSH_TO_ECR.sh
        │   └── *.md                          # Deployment guides
        │
        ├── ── ML Artifacts ──
        │   ├── ckd_best_model.pkl             # Trained model
        │   ├── ckd_feature_names.pkl
        │   ├── ckd_knn_imputer.pkl
        │   ├── ckd_label_encoders.pkl
        │   ├── ckd_scaler.pkl
        │   ├── ckd_target_encoder.pkl
        │   └── ckd_test_metrics.pkl
        │
        ├── ── Training & Utility Scripts ──
        │   ├── train_model.py                # Main model training
        │   ├── train_xgboost.py              # XGBoost-specific training
        │   ├── train_model_selector.py       # Model comparison / selection
        │   ├── predict.py                    # CLI prediction helper
        │   ├── ckd_prediction_system.py       # Core prediction pipeline
        │   ├── demo.py / example_usage.py / simple_example.py
        │   └── test_simple.py
        │
        ├── chronic_kidney_disease_dataset.csv # UCI CKD dataset
        ├── Dockerfile
        ├── requirements.txt                  # Root-level dependencies
        ├── app.py / main.py                  # Legacy entry points
        └── *.md                              # Documentation files
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone the repository
```bash
git clone <repository-url>
cd ckd_Prediction
```
### 2. Common commands
```bash
cd "using-uci-dataset 2/using-uci-dataset"
python3 -m venv venv
source venv/bin/activate
```

### 3. Backend Setup (continue from common commands in new terminal)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup (continue from common commands in new terminal)
```bash
cd frontend
pip install -r requirements.txt
python -m streamlit run streamlit_app/Home.py
```

## Usage

### Accessing the Application
Once the frontend is running, open your browser and navigate to:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

### Authentication
1. **Sign Up**: Create a new clinician account
2. **Login**: Use your email and password to log in
3. **Dashboard**: Access patient management and prediction features

### Patient Management
- Add new patients with demographic and clinical data
- View existing patient records
- Edit patient information
- Delete patient records (with confirmation)

### CKD Prediction
1. Select a patient
2. Click "Predict CKD Risk"
3. View prediction results with:
   - CKD probability
   - Risk level (Low, Medium, High)
   - Key risk factors
   - SHAP and LIME explanations

## Machine Learning Models

The system uses multiple ML models for comprehensive prediction:

### Primary Models
- **Random Forest**: High accuracy, good interpretability
- **XGBoost**: Gradient boosting for optimal performance
- **Decision Tree**: Visual decision paths

### Explainable AI
- **SHAP**: Global and local explanations
- **LIME**: Local interpretable explanations

## Database

The application uses SQLite for development and can be configured for PostgreSQL.

### Database Schema
- **users**: Clinician accounts
- **patients**: Patient records
- **predictions**: Prediction history
- **audit_logs**: Activity tracking

## Development

### Adding New Features
1. Update backend API endpoints
2. Add new database models if needed
3. Create frontend pages/components
4. Update requirements.txt
5. Run database migrations

### Testing
```bash
# Run backend tests
cd backend
pytest

# Run frontend tests (if available)
cd frontend
pytest
```

## Deployment

### Docker Deployment
```bash
# Build backend image
docker build -t ckd-backend ./backend

# Build frontend image
docker build -t ckd-frontend ./frontend

# Run containers
docker run -d -p 8000:8000 --name backend ckd-backend
docker run -d -p 8501:8501 --name frontend ckd-frontend
```

### Production Deployment
For production, consider using:
- PostgreSQL database
- Nginx reverse proxy
- Docker Compose for multi-container deployment
- Environment variables for configuration

## Configuration

Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=sqlite:///./ckd_clinical.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue in the repository.
