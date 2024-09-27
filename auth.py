import bcrypt
import streamlit as st
from db_manager import get_user, add_user
from utils import hash_password, check_password, validate_email

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
    st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGk5dDBhdzBsMXdhaTkxcWFkZWFoNDBia3ZrbnB4bzF5OHBzZ2cxdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cEYFeE4wJ6jdDVBiiIM/giphy.webp", use_column_width=True)

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
    email = st.text_input("Enter Your Email")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    user_type = "User"  # Fixed user type for registration

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        if not validate_email(email):
            st.error("Invalid email address")
            return
        if get_user(username):
            st.error("Username already exists")
        else:
            hashed_password = hash_password(password)
            add_user(username, hashed_password, email, user_type)
            st.success("Registration successful! Please log in.")
            # Switch to login screen
            st.session_state['show_login'] = True
            st.experimental_rerun()
