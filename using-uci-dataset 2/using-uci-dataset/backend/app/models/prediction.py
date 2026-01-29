"""
Prediction database model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Prediction(Base):
    """Prediction model to store ML prediction results"""
    
    __tablename__ = "predictions"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    # Prediction Results
    ckd_prediction = Column(String(20), nullable=False)  # 'CKD' or 'No CKD'
    ckd_probability = Column(Float, nullable=False)
    no_ckd_probability = Column(Float, nullable=False)
    confidence_level = Column(String(20), nullable=True)  # 'High', 'Medium', 'Low'
    risk_level = Column(String(20), nullable=True)
    
    # Clinical Calculations
    egfr = Column(Float, nullable=True)  # Estimated GFR
    ckd_stage = Column(Integer, nullable=True)  # 0-5
    stage_description = Column(String(255), nullable=True)
    
    # Interpretability (stored as JSON)
    shap_values = Column(JSON, nullable=True)  # SHAP feature importance
    lime_values = Column(JSON, nullable=True)  # LIME explanation
    top_features = Column(JSON, nullable=True)  # Top contributing features
    
    # Input Data Snapshot
    input_data = Column(JSON, nullable=True)  # Store the values used for this prediction
    visit_date = Column(DateTime, nullable=True) # Date of the clinical visit
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    patient = relationship("Patient", back_populates="predictions")
