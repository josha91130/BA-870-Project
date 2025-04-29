# --- pages/6_Predict_Volume.py ---
# 🔮 Predict Volume for a Specific Date

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
    with st.spinner('Predicting...'):
        date_str = target_date.strftime("%Y-%m-%d")

        # --- 分別取得各資產的 features
        features_spy = get_features_for_date(date_str, ticker="SPY")
        features_sso = get_features_for_date(date_str, ticker="SSO")
        features_upro = get_features_for_date(date_str, ticker="UPRO")

        features_spy = features_spy.astype(float)
        features_sso = features_sso.astype(float)
        features_upro = features_upro.astype(float)

        # --- 抓每個資產的 lag_return
        # def get_lag_return(ticker, date_str):
        #     start = pd.to_datetime(date_str) - pd.Timedelta(days=1)
        #     end = pd.to_datetime(date_str) + pd.Timedelta(days=1)
        #     prices = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)["Close"]
        #     returns = np.log(prices).diff()
        #     return returns.dropna().iloc[-1]
        def get_lag_return(ticker, date_str, lookback_days=5):
          dt = pd.to_datetime(date_str)
          for delta in range(1, lookback_days+1):
            start = dt - pd.Timedelta(days=delta)
            end = dt + pd.Timedelta(days=1)
            prices = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)["Close"]

            returns = np.log(prices).diff()

            if not returns.dropna().empty:
              return returns.dropna().iloc[-1]

        raise ValueError(f"Unable to find lag return for {ticker} on {date_str} even after looking back {lookback_days} days.")

        lag_return_spy = get_lag_return("SPY", date_str)
        lag_return_sso = get_lag_return("SSO", date_str)
        lag_return_upro = get_lag_return("UPRO", date_str)

        features_spy["lag_return"] = lag_return_spy
        features_sso["lag_return"] = lag_return_sso
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

    # --- 顯示在三個Tab
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



# if st.button("Predict Volume"):
#     with st.spinner("Predicting..."):
#         features = get_features_for_date(target_date.strftime("%Y-%m-%d")).astype(float)

#         def get_lag_return(ticker, dt):
#             prices = yf.download(ticker, start=dt - pd.Timedelta(days=1), end=dt + pd.Timedelta(days=1), progress=False)["Close"]
#             return np.log(prices).diff().dropna().iloc[-1]

#         lag_returns = {ticker: get_lag_return(ticker, pd.to_datetime(target_date)) for ticker in ["SPY", "SSO", "UPRO"]}

#         ml_features = [
#             'lag_vol', 'lag_return', 'rolling_std_5d', 'lag_vix',
#             'NFP_surprise_z', 'ISM_surprise_z', 'CPI_surprise_z',
#             'Housing_Starts_surprise_z', 'Jobless_Claims_surprise_z',
#             'monday_dummy', 'wednesday_dummy', 'friday_dummy'
#         ]

#         for name, model in zip(["SPY", "SSO", "UPRO"], [model_spy, model_sso, model_upro]):
#             feat = features.copy()
#             feat["lag_return"] = lag_returns[name]
#             pred_log = model.predict(feat[ml_features])[0]
#             pred_vol = np.exp(pred_log) - 1
#             st.metric(f"{name} Predicted Volume", value=f"{pred_vol:,.0f}")
