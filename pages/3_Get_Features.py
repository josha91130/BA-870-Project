import streamlit as st
import pandas as pd
from features import get_features_for_date

st.title("Get Features for a Specific Date")

# Date input widget
target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

# Fetch and display features when button is clicked
if st.button("Get Features"):
    with st.spinner('Getting features...'):
        date_str = target_date.strftime("%Y-%m-%d")
        features = {
            "SPY": get_features_for_date(date_str, "SPY"),
            "SSO": get_features_for_date(date_str, "SSO"),
            "UPRO": get_features_for_date(date_str, "UPRO"),
        }

    # Display in tabs
    tabs = st.tabs(["SPY Features", "SSO Features", "UPRO Features"])
    for tab, name in zip(tabs, features):
        with tab:
            st.subheader(f"{name} Features")
            st.dataframe(features[name])
