# --- pages/3_Get_Features.py ---
import streamlit as st
import pandas as pd
from features import get_features_for_date

st.set_page_config(page_title="Get Features", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("## 📚 Start Here")
    st.page_link("pages/0_Intro_to_App.py", label="Intro to the App")
    st.page_link("pages/1_Info.py", label="Data Dictionary")

    st.markdown("## 📈 Dashboard Options")
    st.page_link("pages/2_Model_Visualization.py", label="Model Visualization")
    st.page_link("pages/3_Get_Features.py", label="Get Features")
    st.page_link("pages/4_Predict_Volume.py", label="Predict Volume")

# --- Main Page Content ---
st.title("🔎 Get Features for a Specific Date")

target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

if st.button("Get Features"):
    with st.spinner('Getting features...'):
        features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
    st.subheader("Features for selected date:")
    st.dataframe(features)
