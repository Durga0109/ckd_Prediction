"""
Authentication state management
"""
import streamlit as st

def init_auth():
    """Initialize authentication state"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_info" not in st.session_state:
        st.session_state.user_info = None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    if "token" not in st.session_state:
        return False
    return st.session_state.token is not None

def logout():
    """Logout user"""
    st.session_state.token = None
    st.session_state.user_email = None
    st.session_state.user_info = None
    st.rerun()

def require_auth():
    """Redirect to login if not authenticated"""
    if not is_authenticated():
        st.warning("Please login to access this page")
        st.stop()
