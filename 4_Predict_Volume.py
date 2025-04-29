# pages/6_Predict_Volume.py
# Predict Volume for a Specific Date

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import yfinance as yf
from features import get_features_for_date

st.set_page_config(page_title="Predict Volume", layout="wide")

st.title("🔮 Predict Trading Volume")

# --- Load trained models ---
with open('models/best_model_spy.pkl', 'rb') as f:
    model_spy = pickle.load(f)
with open('models/best_model_sso.pkl', 'rb') as f:
    model_sso = pickle.load(f)
with open('models/best_model_upro.pkl', 'rb') as f:
    model_upro = pickle.load(f)

# --- Select prediction date ---
target_date = st.date_input("Select a date to predict:", value=pd.to_datetime("2025-04-25"))

if st.button("Predict Volume"):
    with st.spinner("Predicting..."):
        features = get_features_for_date(target_date.strftime("%Y-%m-%d")).astype(float)

        def get_lag_return(ticker, dt):
            prices = yf.download(ticker, start=dt - pd.Timedelta(days=1), end=dt + pd.Timedelta(days=1), progress=False)["Close"]
            return np.log(prices).diff().dropna().iloc[-1]

        lag_returns = {ticker: get_lag_return(ticker, pd.to_datetime(target_date)) for ticker in ["SPY", "SSO", "UPRO"]}

        ml_features = [
            'lag_vol', 'lag_return', 'rolling_std_5d', 'lag_vix',
            'NFP_surprise_z', 'ISM_surprise_z', 'CPI_surprise_z',
            'Housing_Starts_surprise_z', 'Jobless_Claims_surprise_z',
            'monday_dummy', 'wednesday_dummy', 'friday_dummy'
        ]

        for name, model in zip(["SPY", "SSO", "UPRO"], [model_spy, model_sso, model_upro]):
            feat = features.copy()
            feat["lag_return"] = lag_returns[name]
            pred_log = model.predict(feat[ml_features])[0]
            pred_vol = np.exp(pred_log) - 1
            st.metric(f"{name} Predicted Volume", value=f"{pred_vol:,.0f}")
