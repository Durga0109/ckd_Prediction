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
    """Redirect to login if not authenticated with professional UI"""
    if not is_authenticated():
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.error("Authentication Required")
            st.info("You must be logged in to access this clinical module. Please authenticate your credentials to continue.")
            if st.button("Proceed to Clinician Login", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Login.py")
        st.stop()
