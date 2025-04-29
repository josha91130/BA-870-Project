# --- pages/1_Info.py ---
# Feature Dictionary
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Dictionary", layout="wide")

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
st.title("📚 Data Dictionary")

# --- Cleaned Data Dictionary ---
data = {
    "Variable": [
        "Lag_Volume(SPY)", "Lag_Volume(SSO)", "Lag_Volume(UPRO)", "Lag_VIX",
        "Non-Farm Payrolls surprise Z score",
        "ISM Manufacturing Index surprise Z score",
        "Consumer Price Index surprise Z score",
        "Housing Starts surprise Z score",
        "Jobless Claims surprise Z score",
        "Lag ETF Return", "Lag Rolling Std",
        "Monday Dummy", "Wednesday Dummy", "Friday Dummy"
    ],
    "Description": [
        "Lag Daily trading volume for SPY (largest S&P 500 ETF)",
        "Lag Daily trading volume for SSO (2x S&P 500 leveraged ETF)",
        "Lag Daily trading volume for UPRO (3x S&P 500 leveraged ETF)",
        "CBOE Volatility Index (fear index), measures expected 30-day volatility",
        "Z-score for Nonfarm Payrolls surprise, reflects labor market surprises",
        "Z-score for ISM Manufacturing PMI surprise, reflects manufacturing sector activity",
        "Z-score for Consumer Price Index (CPI) inflation surprise",
        "Z-score for Housing Starts data surprise, new home construction indicator",
        "Z-score for Initial Jobless Claims surprise, labor market health indicator",
        "Previous day's return (SPY/SSO/UPRO)",
        "Rolling standard deviation of recent returns (SPY/SSO/UPRO)",
        "Dummy variable: 1 if Monday, else 0",
        "Dummy variable: 1 if Wednesday, else 0",
        "Dummy variable: 1 if Friday, else 0"
    ],
    "Frequency": [
        "Daily", "Daily", "Daily", "Daily",
        "Monthly", "Monthly", "Monthly",
        "Monthly", "Weekly", "Daily", "Daily",
        "-", "-", "-"
    ],
    "Source": [
        "CRSP", "CRSP", "CRSP", "CBOE Index Data",
        "Bloomberg", "Bloomberg", "Bloomberg",
        "Bloomberg", "Bloomberg",
        "CRSP", "CRSP",
        "-", "-", "-"
    ]
}

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)
