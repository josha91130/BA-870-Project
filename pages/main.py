import streamlit as st
import pandas as pd
import yfinance as yf

st.title("Predicting S&P 500 ETF Volume using VIX and macro data")
st.header("Modified Jones")
st.subheader("What, How, Why?")

st.markdown(''' :red[What?]''')
st.write("This App trains a version of the <Modified Jones Model> using data from Compustat to determine the")
st.write("regular association between operations and accruals. Abnormal accruals are the residuals (e)")
st.write("from the model below:")


st.markdown(''' :red[How?]''')
st.write("Using the following code on GitHub, we can find manipulated accruals for a stock ...")


st.divider()

st.subheader("Streamlit Python Code for this page:")
# with open('pages/main.py', 'r') as file:
#     code = file.read()
#     st.code(code, language='python')
if os.path.exists('pages/main.py'):
    with open('pages/main.py', 'r') as file:
        code = file.read()
        st.code(code, language='python')
else:
    st.warning('pages/main.py not found yet.')
