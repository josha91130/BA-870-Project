
import streamlit as st
import pandas as pd
import pickle
from features import get_features_for_date

st.title("Predict Trading Volume for a Specific Date")

# Load your models (需要事先把模型存成pkl檔)
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
        # 取得 features
        features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
        features = features.astype(float)  # 確保數據型別正確

        # 分別做預測
        pred_spy = model_spy.predict(features)[0]
        pred_sso = model_sso.predict(features)[0]
        pred_upro = model_upro.predict(features)[0]

    # 顯示在三個Tab
    tab1, tab2, tab3 = st.tabs(["SPY", "SSO", "UPRO"])

    with tab1:
        st.subheader("SPY Predicted Trading Volume (log scale)")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_spy:.4f}")

    with tab2:
        st.subheader("SSO Predicted Trading Volume (log scale)")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_sso:.4f}")

    with tab3:
        st.subheader("UPRO Predicted Trading Volume (log scale)")
        st.metric(label="Predicted log(volume+1)", value=f"{pred_upro:.4f}")
