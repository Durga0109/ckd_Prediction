from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Clinician, Patient, Prediction
from ..schemas import PredictionRequest, PredictionResponse
from ..services.auth_service import get_current_clinician
from ..services.ml_service import ml_service

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Make a CKD prediction for a patient
    """
    # Get patient
    patient = db.query(Patient).filter(
        Patient.id == request.patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Prepare patient data for ML model
    # Start with stored patient data
    base_data = {
        'age': patient.age,
        'sex': patient.sex,
        'bp': patient.bp,
        'sg': patient.sg,
        'al': patient.al,
        'su': patient.su,
        'bgr': patient.bgr,
        'bu': patient.bu,
        'sc': patient.sc,
        'sod': patient.sod,
        'pot': patient.pot,
        'hemo': patient.hemo,
        'pcv': patient.pcv,
        'wbcc': patient.wbcc,
        'rbcc': patient.rbcc,
        'rbc': patient.rbc,
        'pc': patient.pc,
        'pcc': patient.pcc,
        'ba': patient.ba,
        'htn': patient.htn,
        'dm': patient.dm,
        'cad': patient.cad,
        'appet': patient.appet,
        'pe': patient.pe,
        'ane': patient.ane
    }
    
    # Override with any new values provided in the request
    patient_data = base_data.copy()
    if request.clinical_data:
        # Convert types if necessary and update
        for key, value in request.clinical_data.items():
            if key in patient_data:
                patient_data[key] = value
    
    # Make prediction
    try:
        prediction_result = ml_service.predict(patient_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
    
    # Save prediction to database
    db_prediction = Prediction(
        patient_id=patient.id,
        ckd_prediction=prediction_result['ckd_prediction'],
        ckd_probability=prediction_result['ckd_probability'],
        no_ckd_probability=prediction_result['no_ckd_probability'],
        confidence_level=prediction_result['confidence_level'],
        risk_level=prediction_result['risk_level'],
        egfr=prediction_result['egfr'],
        ckd_stage=prediction_result['ckd_stage'],
        stage_description=prediction_result['stage_description'],
        shap_values=prediction_result['shap_values'],
        lime_values=prediction_result['lime_values'],
        top_features=prediction_result['top_features'],
        input_data=patient_data,  # Save snapshot
        visit_date=request.visit_date or datetime.now()  # Use current date if not provided
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction


@router.get("/patient/{patient_id}", response_model=List[PredictionResponse])
def get_patient_predictions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Get all predictions for a specific patient
    """
    # Verify patient belongs to clinician
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    predictions = db.query(Prediction).filter(
        Prediction.patient_id == patient_id
    ).order_by(Prediction.visit_date.desc(), Prediction.created_at.desc()).all()
    
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Get a specific prediction by ID
    """
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id
    ).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )
    
    # Verify prediction belongs to clinician's patient
    patient = db.query(Patient).filter(
        Patient.id == prediction.patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return prediction
