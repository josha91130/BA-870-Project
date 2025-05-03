# BA-870-Project
# 📘 Predicting Trading Volumes with Market Sentiment and Macroeconomic Indicators

**Contributors:** Zhe Yu Lin, Pei Chi Chu, Ming Hua Tsai
**Website Link:** https://ba-870-project-jerry.streamlit.app/Intro_to_App
---

Trading volume is a key reflection of market participation and liquidity—both of which are essential for efficient pricing and investment decision-making.

In this project, we explore how market sentiment and macroeconomic signals jointly influence trading activity, focusing specifically on predicting the trading volume of **SPY**, the world’s largest S&P 500 ETF.

---

## 📈 Importance of Predicting Trading Volume

Understanding and predicting trading volume is critical for both investors and market makers:

- High volume periods are typically associated with higher liquidity, lower transaction costs, and more efficient price discovery.
- Sudden shifts in volume often signal changes in market sentiment and can foreshadow increased volatility or directional market moves.

---

## 🛠️ Indicators Incorporated in the Model

Our approach incorporates multiple types of indicators:

### Market Sentiment Measures
- **VIX** (Volatility Index)
- Trading activity of leveraged ETFs:
  - **SSO** (2× S&P 500)
  - **UPRO** (3× S&P 500)

### Macroeconomic Variables
- Nonfarm Payrolls (NFP)
- ISM Manufacturing PMI
- Consumer Price Index (CPI)
- Housing Starts
- Jobless Claims
- Industrial Production

---

## 🧠 Modeling Approach

By developing models that can anticipate volume changes, we contribute to:

- Better risk management
- Improved trading strategies
- More informed portfolio decisions

We employ a combination of **time-series modeling techniques**, leveraging both market sentiment and macroeconomic indicators to capture the dynamics influencing SPY’s trading volume.

Additionally, by including the trading activity of leveraged ETFs (SSO and UPRO), we examine whether 2× and 3× leveraged products exhibit greater sensitivity to trading volume changes. This allows us to assess whether leveraged market behavior provides earlier or stronger signals of shifts in overall market participation.
