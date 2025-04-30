
import streamlit as st
import pandas as pd
from features import get_features_for_date

# ── Title ──
st.title("Get Market and Macro Features for a Specific Date")

# ── Date Input ──
target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

# ── Button + Feature Extraction ──
if st.button("Get Features"):
    with st.spinner('Getting features...'):
        date_str = target_date.strftime("%Y-%m-%d")
        features_spy = get_features_for_date(date_str, ticker="SPY")
        features_sso = get_features_for_date(date_str, ticker="SSO")
        features_upro = get_features_for_date(date_str, ticker="UPRO")

    # ── Display Tabs ──
    tab1, tab2, tab3 = st.tabs(["SPY Features", "SSO Features", "UPRO Features"])

    with tab1:
        st.subheader("SPY Features")
        st.dataframe(features_spy)

    with tab2:
        st.subheader("SSO Features")
        st.dataframe(features_sso)

    with tab3:
        st.subheader("UPRO Features")
        st.dataframe(features_upro)
