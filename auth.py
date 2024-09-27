import bcrypt
import streamlit as st
from db_manager import get_user, add_user
from utils import hash_password, check_password

def authentication():
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = True

    if st.session_state['show_login']:
        login()
        if st.button("Go to Register"):
            st.session_state['show_login'] = False
            st.experimental_rerun()
    else:
        register()
        if st.button("Go to Login"):
            st.session_state['show_login'] = True
            st.experimental_rerun()

def login():
    st.title("Welcome to the Mach33 Secondary Market")

    # Add a space-themed image
    st.video("space_video.mp4")

    # Add explanatory text
    st.markdown("""
    ### A Secondary Market for Mach33 Portfolio Companies
    Explore investment opportunities and manage your liquidity with ease!
    """)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user(username)
        if user and check_password(password, user['password']):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['user_type'] = user['user_type']
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.title("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    user_type = st.selectbox("User Type", ["User"])  # Only allow "User" type
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        if get_user(username):
            st.error("Username already exists")
        else:
            hashed_password = hash_password(password)
            add_user(username, hashed_password, user_type)
            st.success("Registration successful! Please log in.")
            # Switch to login screen
            st.session_state['show_login'] = True
            st.experimental_rerun()
