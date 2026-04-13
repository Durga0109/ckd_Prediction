import streamlit as st
from utils.api import login, signup
from utils.auth import init_auth, is_authenticated

st.set_page_config(page_title="Login - CKD System", page_icon="🔑")

init_auth()

if is_authenticated():
    st.switch_page("app.py")

st.title("🔐 Clinician Access")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="doctor@hospital.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if login(email, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

with tab2:
    st.header("Register New Clinician")
    with st.form("signup_form"):
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        full_name = st.text_input("Full Name")
        specialization = st.selectbox("Specialization", [
            "Nephrology", "General Practice", "Internal Medicine", "Cardiology", "Other"
        ])
        
        create = st.form_submit_button("Sign Up", use_container_width=True)
        
        if create:
            if signup(new_email, new_password, full_name, specialization):
                st.success("Account created! Please login.")
            else:
                st.error("Registration failed. Email might be taken.")
