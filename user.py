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
