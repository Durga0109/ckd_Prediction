"""
Pydantic schemas for Patient API
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PatientBase(BaseModel):
    """Base patient schema with all clinical parameters"""
    # Demographics
    full_name: str
    age: int
    sex: str  # 'male' or 'female'
    contact_number: Optional[str] = None
    
    # Clinical Parameters (24 features)
    bp: Optional[float] = None
    sg: Optional[float] = None
    al: Optional[float] = None
    su: Optional[float] = None
    bgr: Optional[float] = None
    bu: Optional[float] = None
    sc: Optional[float] = None  # Serum Creatinine (CRITICAL)
    sod: Optional[float] = None
    pot: Optional[float] = None
    hemo: Optional[float] = None
    pcv: Optional[float] = None
    wbcc: Optional[float] = None
    rbcc: Optional[float] = None
    rbc: Optional[str] = None
    pc: Optional[str] = None
    pcc: Optional[str] = None
    ba: Optional[str] = None
    htn: Optional[str] = None
    dm: Optional[str] = None
    cad: Optional[str] = None
    appet: Optional[str] = None
    pe: Optional[str] = None
    ane: Optional[str] = None


class PatientCreate(PatientBase):
    """Schema for creating a new patient"""
    pass


class PatientUpdate(PatientBase):
    """Schema for updating a patient (all fields optional)"""
    full_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None


class PatientResponse(PatientBase):
    """Schema for patient response"""
    id: int
    clinician_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
