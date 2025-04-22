import streamlit as st
import pandas as pd
import yfinance as yf

st.title("Find Abnormal Accruals for a Stock")
st.header("Modified Jones Model App")
st.subheader("What, How, Why?")

st.markdown(''' :red[What?]''')
st.write("This App trains a version of the <Modified Jones Model> using data from Compustat to determine the")
st.write("regular association between operations and accruals. Abnormal accruals are the residuals (e)")
st.write("from the model below:")


st.markdown(''' :red[Why?]''')
st.write("The <Modified Jones Model> of accruals can be used to forecast normal accruals for a stock.")
st.write("If a stock has actual accruals that are different than forecasted, then")
st.write("these accruals are likely manipulated!")

st.markdown(''' :red[How?]''')
st.write("Using the following code on GitHub, we can find manipulated accruals for a stock ...")

url = "https://github.com/wysocki-bu/earnings-manipulation/"
st.write("Link to GitHub respository for StreamLit App is here:")

st.divider()

st.subheader("Streamlit Python Code for this page:")
with open('pages/main.py', 'r') as file:
    code = file.read()
    st.code(code, language='python')
