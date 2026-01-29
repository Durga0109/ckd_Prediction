"""
API Utility functions for communicating with the FastAPI backend
"""
import requests
import streamlit as st
from typing import Dict, Optional, Any
import os

# Backend URL configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

def get_auth_headers() -> Dict[str, str]:
    """Get authorization headers with JWT token"""
    if "token" not in st.session_state:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}

# --- Authentication ---

def login(email: str, password: str) -> bool:
    """Login to the system"""
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.user_email = email
            return True
        return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

def signup(email: str, password: str, full_name: str, specialization: str) -> bool:
    """Register a new clinician"""
    try:
        response = requests.post(
            f"{API_URL}/auth/signup",
            json={
                "email": email,
                "password": password,
                "full_name": full_name,
                "specialization": specialization
            }
        )
        if response.status_code == 201:
            return True
        else:
            st.error(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        st.error(f"Connection error: {e}")
        return False

def get_current_user() -> Optional[Dict]:
    """Get current user details"""
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# --- Patients ---

def get_patients() -> list:
    """Get list of patients"""
    try:
        response = requests.get(
            f"{API_URL}/patients/",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_patient(patient_data: Dict) -> bool:
    """Create a new patient"""
    try:
        response = requests.post(
            f"{API_URL}/patients/",
            headers=get_auth_headers(),
            json=patient_data
        )
        return response.status_code == 201
    except:
        return False

def update_patient(patient_id: int, patient_data: Dict) -> bool:
    """Update patient details"""
    try:
        response = requests.put(
            f"{API_URL}/patients/{patient_id}",
            headers=get_auth_headers(),
            json=patient_data
        )
        return response.status_code == 200
    except:
        return False

def delete_patient(patient_id: int) -> bool:
    """Delete a patient"""
    try:
        response = requests.delete(
            f"{API_URL}/patients/{patient_id}",
            headers=get_auth_headers()
        )
        return response.status_code == 204
    except:
        return False

# --- Predictions ---

def make_prediction(patient_id: int, clinical_data: Optional[Dict] = None, visit_date: Optional[str] = None) -> Optional[Dict]:
    """Make a CKD prediction"""
    try:
        payload = {"patient_id": patient_id}
        if clinical_data:
            payload["clinical_data"] = clinical_data
        if visit_date:
            payload["visit_date"] = visit_date
            
        response = requests.post(
            f"{API_URL}/predictions/",
            headers=get_auth_headers(),
            json=payload
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Prediction failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_patient_history(patient_id: int) -> list:
    """Get prediction history"""
    try:
        response = requests.get(
            f"{API_URL}/predictions/patient/{patient_id}",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []
