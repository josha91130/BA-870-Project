
# import streamlit as st
# import pandas as pd
# import pickle
# import numpy as np
# import yfinance as yf
# from features import get_features_for_date

# st.title("Predict Trading Volume for a Specific Date")

# # Load models
# with open('models/best_model_spy.pkl', 'rb') as f:
#     model_spy = pickle.load(f)

# with open('models/best_model_sso.pkl', 'rb') as f:
#     model_sso = pickle.load(f)

# with open('models/best_model_upro.pkl', 'rb') as f:
#     model_upro = pickle.load(f)

# # 選日期
# target_date = st.date_input(
#     "Select a date to predict trading volume",
#     value=pd.to_datetime("2025-04-25"),
#     min_value=pd.to_datetime("2010-01-01"),
#     max_value=pd.to_datetime("2025-12-31")
# )

# if st.button("Predict Volume"):
#     with st.spinner('Predicting...'):
#         # --- 取得 features (lag_return 尚未補)
#         features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
#         features = features.astype(float)

#         date_str = target_date.strftime("%Y-%m-%d")

#         # --- 抓每個資產的 lag_return
#         def get_lag_return(ticker, date_str):
#             start = pd.to_datetime(date_str) - pd.Timedelta(days=1)
#             end = pd.to_datetime(date_str) + pd.Timedelta(days=1)
#             prices = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)["Close"]
#             returns = np.log(prices).diff()
#             return returns.dropna().iloc[-1]

#         lag_return_spy = get_lag_return("SPY", date_str)
#         lag_return_sso = get_lag_return("SSO", date_str)
#         lag_return_upro = get_lag_return("UPRO", date_str)

#         # --- 分別補上 lag_return
#         features_spy = features.copy()
#         features_spy["lag_return"] = lag_return_spy

#         features_sso = features.copy()
#         features_sso["lag_return"] = lag_return_sso

#         features_upro = features.copy()
#         features_upro["lag_return"] = lag_return_upro

#         # --- 分別做預測
#         ml_features_clean = [
#             'lag_vol', 'lag_return', 'rolling_std_5d', 'lag_vix',
#             'NFP_surprise_z', 'ISM_surprise_z', 'CPI_surprise_z',
#             'Housing_Starts_surprise_z', 'Jobless_Claims_surprise_z',
#             'monday_dummy', 'wednesday_dummy', 'friday_dummy'
#         ]

#         X_spy = features_spy[ml_features_clean]
#         X_sso = features_sso[ml_features_clean]
#         X_upro = features_upro[ml_features_clean]

#         pred_log_spy = model_spy.predict(X_spy)[0]
#         pred_vol_spy = np.exp(pred_log_spy) - 1

#         pred_log_sso = model_sso.predict(X_sso)[0]
#         pred_vol_sso = np.exp(pred_log_sso) - 1

#         pred_log_upro = model_upro.predict(X_upro)[0]
#         pred_vol_upro = np.exp(pred_log_upro) - 1

#     # --- 顯示在三個Tab
#     tab1, tab2, tab3 = st.tabs(["SPY", "SSO", "UPRO"])

#     with tab1:
#         st.subheader("SPY Prediction")
#         st.metric(label="Predicted log(volume+1)", value=f"{pred_log_spy:.4f}")
#         st.metric(label="Predicted volume", value=f"{pred_vol_spy:,.0f}")

#     with tab2:
#         st.subheader("SSO Prediction")
#         st.metric(label="Predicted log(volume+1)", value=f"{pred_log_sso:.4f}")
#         st.metric(label="Predicted volume", value=f"{pred_vol_sso:,.0f}")

#     with tab3:
#         st.subheader("UPRO Prediction")
#         st.metric(label="Predicted log(volume+1)", value=f"{pred_log_upro:.4f}")
#         st.metric(label="Predicted volume", value=f"{pred_vol_upro:,.0f}")
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import yfinance as yf
from features import get_features_for_date

st.title("Predict Trading Volume for a Specific Date")

# Load models
with open('models/best_model_spy.pkl', 'rb') as f:
    model_spy = pickle.load(f)

with open('models/best_model_sso.pkl', 'rb') as f:
    model_sso = pickle.load(f)

with open('models/best_model_upro.pkl', 'rb') as f:
    model_upro = pickle.load(f)

# 選日期
target_date = st.date_input(
    "Select a date to predict trading volume",
    value=pd.to_datetime("2025-04-25"),
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

if st.button("Predict Volume"):
    with st.spinner('Predicting...'):
        date_str = target_date.strftime("%Y-%m-%d")

        # --- 分別取得 SPY / SSO / UPRO 的 features
        features_spy = get_features_for_date(date_str, asset="SPY")
        features_sso = get_features_for_date(date_str, asset="SSO")
        features_upro = get_features_for_date(date_str, asset="UPRO")

        # --- 確保數據型別正確
        features_spy = features_spy.astype(float)
        features_sso = features_sso.astype(float)
        features_upro = features_upro.astype(float)

        # --- 抓每個資產的 lag_return
        def get_lag_return(ticker, date_str):
            start = pd.to_datetime(date_str) - pd.Timedelta(days=1)
            end = pd.to_datetime(date_str) + pd.Timedelta(days=1)
            prices = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), progress=False)["Close"]
            returns = np.log(prices).diff()
            return returns.dropna().iloc[-1]

        lag_return_spy = get_lag_return("SPY", date_str)
        lag_return_sso = get_lag_return("SSO", date_str)
        lag_return_upro = get_lag_return("UPRO", date_str)

        # --- 分別補上 lag_return
        features_spy["lag_return"] = lag_return_spy
        features_sso["lag_return"] = lag_return_sso
        features_upro["lag_return"] = lag_return_upro

        # --- 要的欄位
        ml_features_clean = [
            'lag_vol', 'lag_return', 'rolling_std_5d', 'lag_vix',
            'NFP_surprise_z', 'ISM_surprise_z', 'CPI_surprise_z',
            'Housing_Starts_surprise_z', 'Jobless_Claims_surprise_z',
            'monday_dummy', 'wednesday_dummy', 'friday_dummy'
        ]

        # --- 做預測
        X_spy = features_spy[ml_features_clean]
        X_sso = features_sso[ml_features_clean]
        X_upro = features_upro[ml_features_clean]

        pred_log_spy = model_spy.predict(X_spy)[0]
        pred_vol_spy = np.exp(pred_log_spy) - 1

        pred_log_sso = model_sso.predict(X_sso)[0]
        pred_vol_sso = np.exp(pred_log_sso) - 1

        pred_log_upro = model_upro.predict(X_upro)[0]
        pred_vol_upro = np.exp(pred_log_upro) - 1

    # --- 顯示結果
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
