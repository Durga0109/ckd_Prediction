"""
Pydantic schemas for Clinician API
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ClinicianBase(BaseModel):
    """Base clinician schema"""
    email: EmailStr
    full_name: str
    specialization: Optional[str] = None


class ClinicianCreate(ClinicianBase):
    """Schema for creating a new clinician"""
    password: str


class ClinicianLogin(BaseModel):
    """Schema for login"""
    email: EmailStr
    password: str


class ClinicianResponse(ClinicianBase):
    """Schema for clinician response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload"""
    email: Optional[str] = None
