# src/authentication.py

import streamlit as st

# Dummy user database
USER_DATABASE = {
    "student1": {"password": "studentpass", "role": "student"},
    "alumni1": {"password": "alumnipass", "role": "alumni"},
}

def login(username: str, password: str, role: str) -> bool:
    user = USER_DATABASE.get(username)
    if user and user["password"] == password and user["role"] == role:
        return True
    return False

def show_login():
    st.title("CareerMate AI")
    st.subheader("Smart Career Assistant 🚀")

    # No white box or empty widget inserted here ✅

    st.markdown("## 🔐 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["student", "alumni"])

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
        else:
            st.error("Please fill out all fields!")
