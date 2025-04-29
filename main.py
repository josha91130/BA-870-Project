import streamlit as st

# --- Page config ---
st.set_page_config(page_title="Trading Volume Dashboard", layout="wide")

# --- Main page content ---
st.title("📊 Welcome to the Trading Volume Prediction App")

st.write("""
Use the sidebar to navigate between sections.  
This dashboard explores how **market sentiment** and **macroeconomic indicators** affect trading volume in SPY, the largest S&P 500 ETF.
""")

st.markdown("---")
st.write("🔍 Start by reviewing the project introduction or data dictionary under **Start Here**.")

# --- Sidebar navigation ---
st.sidebar.markdown("### Start Here:")
st.sidebar.page_link("0_Intro_to_App.py", label="📘 Intro to the App")
st.sidebar.page_link("0_Data_Dictionary.py", label="📚 Data Dictionary")

st.sidebar.markdown("### Dashboard Options:")
st.sidebar.page_link("1_Model_Training.py", label="1️⃣ Model Training Code")
st.sidebar.page_link("2_Model_Parameters.py", label="2️⃣ Parameters of Trained Model")
st.sidebar.page_link("3_Forecast_Analyze.py", label="3️⃣ Forecast & Analyze Accruals")
st.sidebar.page_link("4_List_Model_Code.py", label="4️⃣ List Model Training Code")
st.sidebar.page_link("5_List_Streamlit_App_Code.py", label="5️⃣ List Streamlit App Code")

