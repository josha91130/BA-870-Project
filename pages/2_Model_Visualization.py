
import streamlit as st
from visualization import plot_predictions

st.title("Model Visualization")

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
