# app.py
import streamlit as st
import sys
from auth import login
from admin import admin_interface
from user import user_interface
from db_manager import initialize_db


def main():
    st.set_page_config(page_title="Secondary Market App")

    # Initialize the database
    initialize_db()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login()
    else:
        if st.session_state['user_type'] == 'Admin':
            admin_interface()
        else:
            user_interface()

if __name__ == '__main__':
    main()
