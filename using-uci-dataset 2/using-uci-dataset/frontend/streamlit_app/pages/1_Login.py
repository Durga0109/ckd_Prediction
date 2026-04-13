import streamlit as st
from utils.api import login, signup
from utils.auth import init_auth, is_authenticated

st.set_page_config(page_title="Login - CKD System", page_icon="🏥")

init_auth()

if is_authenticated():
    st.switch_page("app.py")

st.header("Authorized Personnel Access")

tab1, tab2 = st.tabs(["Clinician Login", "New Clinician Registration"])

with tab1:
    st.subheader("Sign In")
    with st.form("login_form"):
        email = st.text_input("Institutional Email", placeholder="doctor@hospital.com")
        password = st.text_input("Secure Password", type="password")
        submit = st.form_submit_button("Authenticate", use_container_width=True, type="primary")
        
        if submit:
            if login(email, password):
                st.success("Authentication successful.")
                st.rerun()
            else:
                st.error("Invalid credentials. Please verify your email and password.")

with tab2:
    st.subheader("Credential Registration")
    with st.form("signup_form"):
        new_email = st.text_input("Institutional Email")
        new_password = st.text_input("Secure Password (Min. 8 characters)", type="password")
        full_name = st.text_input("Medical Professional Full Name")
        specialization = st.selectbox("Department / Specialization", [
            "Nephrology", "General Practice", "Internal Medicine", "Cardiology", "System Administrator", "Other"
        ])
        
        create = st.form_submit_button("Register Credentials", use_container_width=True)
        
        if create:
            if not new_email or not new_password or not full_name:
                st.warning("All fields are mandatory for clinical credentialing.")
            elif signup(new_email, new_password, full_name, specialization):
                st.success("Credentials registered successfully. You may now log in.")
            else:
                st.error("Registration failed. This email may already be registered in our system.")
