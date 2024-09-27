import bcrypt
import streamlit as st
from db_manager import get_user

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    user_type = st.sidebar.selectbox("Login as", ["User", "Admin"])
    if st.sidebar.button("Login"):
        user = get_user(username)
        if user and user['user_type'] == user_type and check_password(password, user['password']):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['user_type'] = user_type
            st.sidebar.success(f"Logged in as {user_type}")
        else:
            st.sidebar.error("Invalid username or password")
