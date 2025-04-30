import streamlit as st
import pandas as pd
from features import get_features_for_date

#st.title("Get Features for a Specific Date")

#target_date = st.date_input(
    #"Select a date to get features",
    #value=pd.to_datetime("2025-04-25"),
    #min_value=pd.to_datetime("2010-01-01"),
    #max_value=pd.to_datetime("2025-12-31")
#)

#if st.button("Get Features"):
    #with st.spinner('Getting features...'):
        #features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
    #st.subheader("Features for selected date:")
    #st.dataframe(features)

st.title("Get Features for a Specific Date")

target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

if st.button("Get Features"):
    with st.spinner('Getting features...'):
        features_spy = get_features_for_date(target_date.strftime("%Y-%m-%d"), "SPY")
        features_sso = get_features_for_date(target_date.strftime("%Y-%m-%d"), "SSO")
        features_upro = get_features_for_date(target_date.strftime("%Y-%m-%d"), "UPRO")

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
