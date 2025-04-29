# --- pages/3_Model_Training.py ---
# Model Training
import streamlit as st

st.set_page_config(page_title="Model Training", layout="wide")

st.title("🧠 Model Training Process")

st.write("""
Here we describe how the models were trained:
- Features: lag_vol, lag_return, rolling_std_5d, etc.
- Model types: XGBoost, Linear Regression
- Validation: Train/Test Split
- Metrics: RMSE
""")
