
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# └─ Load Historical Surprise Data
cpi_yoy_final = pd.read_csv('historical/cpi_yoy_final.csv')
nonfarm_final = pd.read_csv('historical/nonfarm_final.csv')
ism_final = pd.read_csv('historical/ism_final.csv')
jobless_claims_final = pd.read_csv('historical/jobless_claims_final.csv')
housing_starts_final = pd.read_csv('historical/housing_starts_final.csv')

# └─ Macro URLs
urls = {
    "CPI": 'https://www.investing.com/economic-calendar/cpi-733',
    "NFP": 'https://www.investing.com/economic-calendar/nonfarm-payrolls-227',
    "ISM": 'https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173',
    "Jobless_Claims": 'https://www.investing.com/economic-calendar/initial-jobless-claims-294',
    "Housing_Starts": 'https://www.investing.com/economic-calendar/housing-starts-298'
}

def get_actual_forecast_bs4(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    date_span = (
        soup.select_one("p.eventDetails span.date") or
        soup.select_one("div.eventHeader span.date") or
        soup.find("span", class_="date")
    )
    release_date = date_span.get_text(strip=True) if date_span else None
    fc = soup.select_one("div.arial_14.noBold")
    forecast = fc.get_text(strip=True) if fc else None
    ac = soup.select_one("div.arial_14.greenFont, div.arial_14.redFont")
    actual = ac.get_text(strip=True) if ac else None
    return release_date, actual, forecast

records = []
for var, url in urls.items():
    rd, ac, fc = get_actual_forecast_bs4(url)
    records.append({"variable": var, "release_date": rd, "actual": ac, "forecast": fc})

df_summary = pd.DataFrame(records)
df_summary['release_date'] = pd.to_datetime(df_summary['release_date'], errors="coerce").dt.date

# └─ Market Feature Functions Per ETF
def get_market_features(target_date, ticker, recent_days=10):
    dt = pd.to_datetime(target_date)
    start = (dt - timedelta(days=recent_days)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=1)).strftime("%Y-%m-%d")

    df = yf.download([ticker, "^VIX"], start=start, end=end, progress=False)

    # --- Detect and extract volume properly ---
    if isinstance(df.columns, pd.MultiIndex):
        vol = df["Volume"][ticker].loc[:dt.strftime("%Y-%m-%d")]
        vix_series = df["Close"]["^VIX"].loc[:dt.strftime("%Y-%m-%d")]
    else:
        vol = df[f"{ticker} Volume"].loc[:dt.strftime("%Y-%m-%d")]
        vix_series = df["^VIX Close"].loc[:dt.strftime("%Y-%m-%d")]

    logv = np.log(vol + 1)
    lag_vol = logv.shift(1).iloc[-1] if len(logv) > 1 else np.nan
    rolling_std_5d = logv.rolling(5).std().iloc[-1] if len(logv) >= 5 else np.nan

    lag_vix = vix_series.shift(1).iloc[-1] if len(vix_series) > 1 else np.nan

    wd = dt.weekday()
    return pd.DataFrame([{
        "lag_vol": lag_vol,
        "rolling_std_5d": rolling_std_5d,
        "lag_vix": lag_vix,
        "monday_dummy": int(wd == 0),
        "wednesday_dummy": int(wd == 2),
        "friday_dummy": int(wd == 4)
    }])

# └─ Macro Z-score

def clean_macro_value(x):
    if x is None: return None
    s = x.replace(",", "").strip()
    try:
        if s.endswith("K"): return float(s[:-1])
        return float(s.rstrip("%"))
    except ValueError:
        return None

def compute_surprise_z(actual, forecast, mean, std):
    a = clean_macro_value(actual)
    f = clean_macro_value(forecast)
    if None in (a, f, mean, std): return None
    return ((a - f) - mean) / std

mean_dict = {
    "CPI": cpi_yoy_final['CPI_surprise'].mean(),
    "NFP": nonfarm_final['NFP_surprise'].mean(),
    "ISM": ism_final['ISM_surprise'].mean(),
    "Jobless_Claims": jobless_claims_final['Jobless_Claims_surprise'].mean(),
    "Housing_Starts": housing_starts_final['Housing_Starts_surprise'].mean()
}
std_dict = {
    "CPI": cpi_yoy_final['CPI_surprise'].std(),
    "NFP": nonfarm_final['NFP_surprise'].std(),
    "ISM": ism_final['ISM_surprise'].std(),
    "Jobless_Claims": jobless_claims_final['Jobless_Claims_surprise'].std(),
    "Housing_Starts": housing_starts_final['Housing_Starts_surprise'].std()
}

# └─ Main Feature Function
def get_features_for_date(target_date, ticker):
    # 1) market
    feat = get_market_features(target_date, ticker)

    # 2) macro surprise_z (
    for var in urls:
        sel = df_summary[
            (df_summary['variable']==var) & 
            (df_summary['release_date']==pd.to_datetime(target_date).date())
        ]
        if not sel.empty:
            actual   = sel.iloc[0]['actual']
            forecast = sel.iloc[0]['forecast']
            z = compute_surprise_z(
                actual, forecast,
                mean_dict[var], std_dict[var]
            )
            feat.loc[0, f"{var}_surprise_z"] = 0.0 if z is None else z
        else:
            feat.loc[0, f"{var}_surprise_z"] = 0.0

    return feat
