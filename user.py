import streamlit as st
from db_manager import get_companies, place_bid

def user_interface():
    st.title("Available Companies")
    companies = get_companies()
    for company in companies:
        st.subheader(company['name'])
        st.write(f"Number of Shares: {company['shares']}")
        st.write(f"Market Price: ${company['market_price']}")
        st.write(f"Ask Price: ${company['buy_price']}")
        with st.form(f"bid_form_{company['company_id']}"):
            num_shares_bid = st.number_input("Number of Shares to Buy", min_value=0, max_value=company['shares'], key=f"shares_{company['company_id']}")
            bid_price = st.number_input("Your Bid Price per Share", min_value=0.0, key=f"price_{company['company_id']}")
            submitted = st.form_submit_button("Place Bid")
            if submitted:
                place_bid(st.session_state['username'], company['company_id'], num_shares_bid, bid_price)
                st.success(f"Bid placed for {company['name']}")
                
    company_name = st.selectbox("Select Company", get_company_list())
    bid_amount = st.number_input("Enter your bid amount", min_value=0.0, format="%.2f")

    if st.button("Submit Bid"):
        # Save bid to database
        add_bid(
            username=st.session_state['username'],
            company_name=company_name,
            bid_amount=bid_amount
        )

        # Get user email
        user = get_user_by_username(st.session_state['username'])
        user_email = user['email']

        # Send email to user
        user_subject = "Your Bid Has Been Received"
        user_content = f"""
        <p>Dear {st.session_state['username']},</p>
        <p>Your bid of ${bid_amount:.2f} for {company_name} has been received.</p>
        <p>Thank you for your interest.</p>
        """
        send_email(user_email, user_subject, user_content)

        # Send email to admin
        admin_email = st.secrets["admin"]["email"]
        admin_subject = f"New Bid Received from {st.session_state['username']}"
        admin_content = f"""
        <p>A new bid has been placed by {st.session_state['username']}.</p>
        <p>Company: {company_name}</p>
        <p>Bid Amount: ${bid_amount:.2f}</p>
        """
        send_email(admin_email, admin_subject, admin_content)

        st.success("Bid submitted successfully. A confirmation email has been sent.")