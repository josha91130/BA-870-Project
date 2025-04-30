
import streamlit as st
import pandas as pd
from features import get_features_for_date

st.set_page_config(page_title="Get Features", layout="wide")
st.title("Get Features for a Specific Date")

target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

if st.button("Get Features"):
    with st.spinner("Fetching features..."):
        spy_feat = get_features_for_date(target_date.strftime("%Y-%m-%d"), asset="SPY")
        sso_feat = get_features_for_date(target_date.strftime("%Y-%m-%d"), asset="SSO")
        upro_feat = get_features_for_date(target_date.strftime("%Y-%m-%d"), asset="UPRO")

    tab1, tab2, tab3 = st.tabs(["SPY", "SSO", "UPRO"])

    with tab1:
        st.subheader("SPY Features")
        st.dataframe(spy_feat)

    with tab2:
        st.subheader("SSO Features")
        st.dataframe(sso_feat)

    with tab3:
        st.subheader("UPRO Features")
        st.dataframe(upro_feat)
