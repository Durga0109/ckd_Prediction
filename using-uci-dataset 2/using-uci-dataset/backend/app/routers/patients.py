"""
Patient CRUD API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Clinician, Patient
from ..schemas import PatientCreate, PatientUpdate, PatientResponse
from ..services.auth_service import get_current_clinician

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Create a new patient profile
    """
    db_patient = Patient(
        **patient.dict(),
        clinician_id=current_clinician.id
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.get("/", response_model=List[PatientResponse])
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Get all patients for the current clinician
    """
    patients = db.query(Patient).filter(
        Patient.clinician_id == current_clinician.id
    ).offset(skip).limit(limit).all()
    
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Get a specific patient by ID
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Update a patient's information
    """
    db_patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Update only provided fields
    update_data = patient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Delete a patient
    """
    db_patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.clinician_id == current_clinician.id
    ).first()
    
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    db.delete(db_patient)
    db.commit()
    
    return None
