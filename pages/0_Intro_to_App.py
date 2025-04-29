# Project Introduction - pages/0_Intro_to_App.py
import streamlit as st

st.set_page_config(page_title="Intro to the App", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("## 📚 Start Here")
    st.page_link("pages/0_Intro_to_App.py", label="Intro to the App")
    st.page_link("pages/1_Info.py", label="Info")

    st.markdown("## 📈 Dashboard Options")
    st.page_link("pages/2_Model_Visualization.py", label="Model Visualization")
    st.page_link("pages/3_Get_Features.py", label="Get Features")
    st.page_link("pages/4_Predict_Volume.py", label="Predict Volume")

# --- Main Page Content ---
st.title("📘 Predicting Trading Volumes with Market Sentiment and Macroeconomic Indicators")

# --- Project Overview ---
st.write("""
Trading volume is a key reflection of market participation and liquidity, both of which are essential for efficient pricing and investment decision-making.

In this project, we explore how market sentiment and macroeconomic signals jointly influence trading activity, focusing specifically on predicting the trading volume of SPY, the world's largest S&P 500 ETF.
""")

st.markdown("---")

# --- Importance ---
st.subheader("📈 Importance of Predicting Trading Volume")
st.write("""
Understanding and predicting trading volume is critical for both investors and market makers:
- High volume periods are typically associated with higher liquidity, lower transaction costs, and more efficient price discovery.
- Sudden shifts in volume often signal changes in market sentiment and can foreshadow increased volatility or directional market moves.
""")

st.markdown("---")

# --- Indicators ---
st.subheader("🛠️ Indicators Incorporated in the Model")
st.write("""
Our approach incorporates multiple types of indicators:
- **Market Sentiment Measures** such as the VIX (volatility index).
- **Macroeconomic Variables** such as Nonfarm Payrolls, ISM Manufacturing PMI, CPI, Housing Starts, Jobless Claims, and Industrial Production.
""")

st.markdown("---")

# --- Modeling Approach ---
st.subheader("🧠 Modeling Approach")
st.write("""
By developing models that can anticipate these volume changes, we contribute to better risk management, improved trading strategies, and more informed portfolio decisions.

We employ a combination of time-series modeling techniques, leveraging the data provided in the attached analysis, to capture the dynamics between sentiment, macroeconomic conditions, and market trading behavior.

We specifically include the trading activity of leveraged ETFs (SSO and UPRO) to examine whether 2x and 3x leveraged products exhibit greater sensitivity to trading volume changes.
This approach allows us to assess whether leveraged market behavior provides earlier or stronger signals of shifts in overall market participation.
""")

