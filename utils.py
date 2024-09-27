import bcrypt
import re
import sendgrid
from sendgrid.helpers.mail import Mail
import streamlit as st

def send_email(to_email, subject, content):
    sendgrid_api_key = st.secrets["sendgrid"]["api_key"]
    from_email = st.secrets["sendgrid"]["from_email"]

    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    try:
        response = sg.send(message)
        if response.status_code == 202:
            return True
        else:
            st.error(f"Failed to send email. Status code: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"An error occurred while sending email: {e}")
        return False


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    # Simple regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None