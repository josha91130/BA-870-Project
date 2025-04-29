import streamlit as st

# --- 網頁設定 ---
st.set_page_config(page_title="Trading Volume App", layout="wide")

# --- Sidebar 自訂義導航 ---
with st.sidebar:
    st.header("📚 Start Here")
    st.page_link("pages/0_Intro_to_App.py", label="Intro to the App")
    st.page_link("pages/1_Info.py", label="Info")

    st.markdown("---")
    st.header("📊 Dashboard Options")
    st.page_link("pages/2_Model_Visualization.py", label="1) Model Visualization")
    st.page_link("pages/3_Get_Features.py", label="2) Get Features")
    st.page_link("pages/4_Predict_Volume.py", label="3) Predict Volume")

# --- Main Page 正式內容 ---
st.title("📚 Welcome to Trading Volume Prediction App")

st.write("""
Welcome!
This dashboard predicts SPY trading volumes based on market sentiment and macroeconomic indicators.

**Contributor:** Zhe Yu Lin, Pei Chi Chu, Ming Hua Tsai

👉 Please start by selecting **Intro to the App** on the sidebar.
""")

