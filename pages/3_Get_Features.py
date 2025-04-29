import streamlit as st
import pandas as pd
from features import get_features_for_date  # ⭐️ 這是重點

# --- 頁面設定 ---
st.set_page_config(page_title="Get Features", layout="wide")
st.title("🛠️ Get Features for a Specific Date")

# --- Sidebar (如果要的話可以這邊加) ---
with st.sidebar:
    st.header("🧩 Dashboard Navigation")
    st.page_link("pages/0_Intro_to_App.py", label="Intro to App")
    st.page_link("pages/1_Info.py", label="Data Dictionary")
    st.page_link("pages/2_Model_Visualization.py", label="Model Visualization")
    st.page_link("pages/4_Predict_Volume.py", label="Predict Volume")

# --- Date Selection ---
target_date = st.date_input(
    "Select a date to get features",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

# --- 按鈕 ---
if st.button("Get Features"):
    with st.spinner('🔍 Retrieving features...'):
        target_date = pd.to_datetime(target_date)  # ⭐️⭐️⭐️
        features = get_features_for_date(target_date.strftime("%Y-%m-%d"))

    st.subheader("Features for Selected Date:")
    st.dataframe(features, use_container_width=True)
