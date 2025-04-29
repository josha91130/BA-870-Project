# --- pages/2_Model_Visualization.py ---
# Prediction vs Actual Visualization
import streamlit as st
from visualization import plot_predictions

st.set_page_config(page_title="Model Visualization", layout="wide")

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
st.title("📈 Model Visualization")

tab1, tab2, tab3 = st.tabs(["SPY", "SSO", "UPRO"])

with tab1:
    st.header("SPY Prediction vs Actual")
    plot_predictions("SPY")

with tab2:
    st.header("SSO Prediction vs Actual")
    plot_predictions("SSO")

with tab3:
    st.header("UPRO Prediction vs Actual")
    plot_predictions("UPRO")
