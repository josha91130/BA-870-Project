# --- pages/4_Predict_Volume.py ---
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import yfinance as yf
from features import get_features_for_date

st.set_page_config(page_title="Predict Volume", layout="wide")

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
st.title("📊 Predict SPY Trading Volume")

# Load models
with open('models/best_model_spy.pkl', 'rb') as f:
    model_spy = pickle.load(f)

with open('models/best_model_sso.pkl', 'rb') as f:
    model_sso = pickle.load(f)

with open('models/best_model_upro.pkl', 'rb') as f:
    model_upro = pickle.load(f)

target_date = st.date_input(
    "Select a date to predict trading volume",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

if st.button("Predict Volume"):
    with st.spinner('Predicting...'):
        features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
        features = features.astype(float)

        def get_lag_return(ticker, date_str):
            start = pd.to_datetime(date_str) - pd.Timedelta(days=1)
            end = pd.to_datetime(date_str) + pd.Timedelta(days=1)
            prices = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)["Close"]
            returns = np.log(prices).diff()
            return returns.dropna().iloc[-1]

        date_str = target_date.strftime("%Y-%m-%d")
        lag_return_spy = get_lag_return("SPY", date_str)
        lag_return_sso = get_lag_return("SSO", date_str)
        lag_return_upro = get_lag_return("UPRO", date_str)

        features_spy = features.copy()
        features_spy["lag_return"] = lag_return_spy

        features_sso = features.copy()
        features_sso["lag_return"] = lag_return_sso

        features_upro = features.copy()
        features_upro["lag_return"] = lag_return_upro

        ml_features_clean = [
            'lag_vol', 'lag_return', 'rolling_std_5d', 'lag_vix',
            'NFP_surprise_z', 'ISM_surprise_z', 'CPI_surprise_z',
            'Housing_Starts_surprise_z', 'Jobless_Claims_surprise_z',
            'monday_dummy', 'wednesday_dummy', 'friday_dummy'
        ]

        X_spy = features_spy[ml_features_clean]
        X_sso = features_sso[ml_features_clean]
        X_upro = features_upro[ml_features_clean]

        pred_log_spy = model_spy.predict(X_spy)[0]
        pred_vol_spy = np.exp(pred_log_spy) - 1

        pred_log_sso = model_sso.predict(X_sso)[0]
        pred_vol_sso = np.exp(pred_log_sso) - 1

        pred_log_upro = model_upro.predict(X_upro)[0]
        pred_vol_upro = np.exp(pred_log_upro) - 1

    tab1, tab2, tab3 = st.tabs(["SPY", "SSO", "UPRO"])

    with tab1:
        st.subheader("SPY Prediction")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_log_spy:.4f}")
        st.metric(label="Predicted volume", value=f"{pred_vol_spy:,.0f}")

    with tab2:
        st.subheader("SSO Prediction")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_log_sso:.4f}")
        st.metric(label="Predicted volume", value=f"{pred_vol_sso:,.0f}")

    with tab3:
        st.subheader("UPRO Prediction")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_log_upro:.4f}")
        st.metric(label="Predicted volume", value=f"{pred_vol_upro:,.0f}")
