# --- pages/2_Data_Dictionary.py ---
# 📚 Feature Dictionary
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Dictionary", layout="wide")

st.title("📚 Data Dictionary")

df = pd.DataFrame({
    "Feature": [
        "lag_vol", "rolling_std_5d", "lag_vix", "CPI_surprise_z",
        "NFP_surprise_z", "ISM_surprise_z", "Jobless_Claims_surprise_z", "Housing_Starts_surprise_z"
    ],
    "Description": [
        "Yesterday’s log(volume+1)", "5-day rolling std of log(volume)",
        "Lagged VIX close", "CPI macro surprise z-score",
        "NFP macro surprise z-score", "ISM PMI macro surprise",
        "Jobless Claims surprise z-score", "Housing Starts surprise z-score"
    ]
})

st.dataframe(df)
