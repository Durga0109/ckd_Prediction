"""
Authentication API endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Clinician
from ..schemas import ClinicianCreate, ClinicianResponse, ClinicianLogin, Token
from ..services.auth_service import (
    get_password_hash,
    authenticate_clinician,
    create_access_token,
    get_clinician_by_email,
    get_current_clinician
)
from ..config import get_settings

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=ClinicianResponse, status_code=status.HTTP_201_CREATED)
def signup(clinician: ClinicianCreate, db: Session = Depends(get_db)):
    """
    Register a new clinician
    """
    # Check if email already exists
    existing_clinician = get_clinician_by_email(db, clinician.email)
    if existing_clinician:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new clinician
    hashed_password = get_password_hash(clinician.password)
    db_clinician = Clinician(
        email=clinician.email,
        password_hash=hashed_password,
        full_name=clinician.full_name,
        specialization=clinician.specialization
    )
    
    db.add(db_clinician)
    db.commit()
    db.refresh(db_clinician)
    
    return db_clinician


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get JWT access token
    """
    clinician = authenticate_clinician(db, form_data.username, form_data.password)
    if not clinician:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": clinician.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=ClinicianResponse)
async def get_current_user(
    current_clinician: Clinician = Depends(get_current_clinician)
):
    """
    Get current authenticated clinician
    """
    return current_clinician
