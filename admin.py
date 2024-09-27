import streamlit as st
import pandas as pd
from db_manager import add_company

def admin_interface():
    st.title("Admin Dashboard")
    option = st.selectbox("Choose an action", ["Add Company", "Upload Companies CSV"])

    if option == "Add Company":
        with st.form("add_company_form"):
            company_name = st.text_input("Company Name")
            num_shares = st.number_input("Number of Shares", min_value=0)
            market_price = st.number_input("Market Price", min_value=0.0)
            buy_price = st.number_input("Buy Price (Below Market)", min_value=0.0)
            submitted = st.form_submit_button("Add Company")
            if submitted:
                add_company(company_name, num_shares, market_price, buy_price)
                st.success("Company added successfully!")
    elif option == "Upload Companies CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            for index, row in df.iterrows():
                add_company(row['name'], row['shares'], row['market_price'], row['buy_price'])
            st.success("Companies uploaded successfully!")
