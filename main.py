import streamlit as st

st.set_page_config(page_title="Trading Volume Prediction App", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.markdown("### Start Here:")
st.sidebar.page_link("pages/0_Intro_to_App.py", label="Intro to the App")
st.sidebar.page_link("pages/0_Data_Dictionary.py", label="Data Dictionary")

st.sidebar.markdown("### Dashboard Options:")
st.sidebar.page_link("pages/1_Model_Training.py", label="1) Model Training Code")
st.sidebar.page_link("pages/2_Model_Parameters.py", label="2) Parameters of Trained Model")
st.sidebar.page_link("pages/3_Forecast_Analyze.py", label="3) Forecast & Analyze Accruals")
st.sidebar.page_link("pages/4_List_Model_Code.py", label="4) List Model Training Code")
st.sidebar.page_link("pages/5_List_Streamlit_App_Code.py", label="5) List Streamlit App Code")

st.write("# 📈 Welcome!")  # 也可以只放個歡迎字或圖
st.write("Please select a section from the sidebar to begin.")
