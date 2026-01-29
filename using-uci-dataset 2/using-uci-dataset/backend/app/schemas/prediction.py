"""
Pydantic schemas for Prediction API
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


class PredictionRequest(BaseModel):
    """Schema for prediction request"""
    patient_id: int
    visit_date: Optional[datetime] = None
    # Optional: Override patient's stored data with new values for this visit
    clinical_data: Optional[Dict[str, float | str | int]] = None


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    id: int
    patient_id: int
    
    # Prediction Results
    ckd_prediction: str
    ckd_probability: float
    no_ckd_probability: float
    confidence_level: Optional[str] = None
    risk_level: Optional[str] = None
    
    # Clinical Calculations
    egfr: Optional[float] = None
    ckd_stage: Optional[int] = None
    stage_description: Optional[str] = None
    
    # Interpretability
    shap_values: Optional[Dict] = None
    lime_values: Optional[Dict] = None
    top_features: Optional[List[Dict]] = None
    
    # Snapshot
    input_data: Optional[Dict] = None
    visit_date: Optional[datetime] = None
    
    created_at: datetime
    
    class Config:
        from_attributes = True
