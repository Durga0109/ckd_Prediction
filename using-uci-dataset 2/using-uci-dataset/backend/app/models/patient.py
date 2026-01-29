"""
Patient database model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Patient(Base):
    """Patient model with all clinical parameters"""
    
    __tablename__ = "patients"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    clinician_id = Column(Integer, ForeignKey("clinicians.id"), nullable=False)
    
    # Demographics
    full_name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)  # 'male' or 'female'
    contact_number = Column(String(20), nullable=True)
    
    # Clinical Parameters (24 features)
    # Numerical features
    bp = Column(Float, nullable=True)    # Blood Pressure
    sg = Column(Float, nullable=True)    # Specific Gravity
    al = Column(Float, nullable=True)    # Albumin
    su = Column(Float, nullable=True)    # Sugar
    bgr = Column(Float, nullable=True)   # Blood Glucose Random
    bu = Column(Float, nullable=True)    # Blood Urea
    sc = Column(Float, nullable=True)    # Serum Creatinine (CRITICAL)
    sod = Column(Float, nullable=True)   # Sodium
    pot = Column(Float, nullable=True)   # Potassium
    hemo = Column(Float, nullable=True)  # Hemoglobin
    pcv = Column(Float, nullable=True)   # Packed Cell Volume
    wbcc = Column(Float, nullable=True)  # White Blood Cell Count
    rbcc = Column(Float, nullable=True)  # Red Blood Cell Count
    
    # Categorical features
    rbc = Column(String(20), nullable=True)    # Red Blood Cells
    pc = Column(String(20), nullable=True)     # Pus Cell
    pcc = Column(String(20), nullable=True)    # Pus Cell Clumps
    ba = Column(String(20), nullable=True)     # Bacteria
    htn = Column(String(10), nullable=True)    # Hypertension
    dm = Column(String(10), nullable=True)     # Diabetes Mellitus
    cad = Column(String(10), nullable=True)    # Coronary Artery Disease
    appet = Column(String(20), nullable=True)  # Appetite
    pe = Column(String(10), nullable=True)     # Pedal Edema
    ane = Column(String(10), nullable=True)    # Anemia
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    clinician = relationship("Clinician", back_populates="patients")
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")
