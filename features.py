
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# ── (A) Load Historical Data ──
cpi_yoy_final = pd.read_csv('historical/cpi_yoy_final.csv')
nonfarm_final = pd.read_csv('historical/nonfarm_final.csv')
ism_final = pd.read_csv('historical/ism_final.csv')
jobless_claims_final = pd.read_csv('historical/jobless_claims_final.csv')
housing_starts_final = pd.read_csv('historical/housing_starts_final.csv')
final_data = pd.read_csv('historical/final_data_spy.csv')
final_data_sso = pd.read_csv('historical/final_data_sso.csv')
final_data_upro = pd.read_csv('historical/final_data_upro.csv')

urls = {
    "CPI": 'https://www.investing.com/economic-calendar/cpi-733',
    "NFP": 'https://www.investing.com/economic-calendar/nonfarm-payrolls-227',
    "ISM": 'https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173',
    "Jobless_Claims": 'https://www.investing.com/economic-calendar/initial-jobless-claims-294',
    "Housing_Starts": 'https://www.investing.com/economic-calendar/housing-starts-298'
}

def get_actual_forecast_bs4(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers); resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    release_date = (
        soup.select_one("p.eventDetails span.date")
        or soup.select_one("div.eventHeader span.date")
        or soup.find("span", class_="date")
    )
    release_date = release_date.get_text(strip=True) if release_date else None

    forecast = soup.select_one("div.arial_14.noBold")
    actual = soup.select_one("div.arial_14.greenFont, div.arial_14.redFont")

    return (
        release_date,
        actual.get_text(strip=True) if actual else None,
        forecast.get_text(strip=True) if forecast else None,
    )

# Latest macroeconomic release summary
records = []
for var, url in urls.items():
    rd, ac, fc = get_actual_forecast_bs4(url)
    records.append({"variable": var, "release_date": rd, "actual": ac, "forecast": fc})
df_summary = pd.DataFrame(records)
df_summary['release_date'] = pd.to_datetime(df_summary['release_date'], errors="coerce").dt.date

# ── (B) Market Features ──
def get_market_features(target_date, ticker, recent_days=10):
    """
    Downloads market data and computes:
      - lag_vol (log(volume+1), lagged)
      - rolling_std_5d
      - lag_vix (previous day close)
      - weekday dummies
    """
    dt = pd.to_datetime(target_date)
    start = (dt - timedelta(days=recent_days)).strftime("%Y-%m-%d")
    end = (dt + timedelta(days=1)).strftime("%Y-%m-%d")

    df = yf.download([ticker, "^VIX"], start=start, end=end, progress=False)

    if df.empty:
        raise IndexError(f"No market data for {ticker} between {start} and {end}.")

    # --- Extract volume ---
    try:
        vol = df["Volume"][ticker].loc[:dt.strftime("%Y-%m-%d")]
    except KeyError:
        raise IndexError(f"Volume data for {ticker} not found.")

    if vol.isna().all() or len(vol.dropna()) < 5:
        raise IndexError(f"Not enough {ticker} volume data before {target_date}")

    logv = np.log(vol + 1)

    # Compute lag_vol safely
    lag_vol_series = logv.shift(1).dropna()
    if lag_vol_series.empty:
        raise IndexError(f"lag_vol is NaN for {ticker} on {target_date}")
    lag_vol = lag_vol_series.iloc[-1]

    # Compute rolling std safely
    rolling_std_series = logv.rolling(5).std().dropna()
    if rolling_std_series.empty:
        raise IndexError(f"rolling_std_5d cannot be computed for {ticker} on {target_date}")
    rolling_std_5d = rolling_std_series.iloc[-1]

    # --- Extract lagged VIX close ---
    try:
        vix_series = df["Close"]["^VIX"].loc[:dt.strftime("%Y-%m-%d")]
    except KeyError:
        raise IndexError("VIX data not found.")
    lag_vix_series = vix_series.shift(1).dropna()
    if lag_vix_series.empty:
        raise IndexError(f"lag_vix is NaN for {target_date}")
    lag_vix = lag_vix_series.iloc[-1]

    # --- Weekday dummies ---
    wd = dt.weekday()
    return pd.DataFrame([{
        "lag_vol": lag_vol,
        "rolling_std_5d": rolling_std_5d,
        "lag_vix": lag_vix,
        "monday_dummy": int(wd == 0),
        "wednesday_dummy": int(wd == 2),
        "friday_dummy": int(wd == 4),
    }])

# ── (C) Macro Surprise Z ──
def clean_macro_value(x):
    if x is None: return None
    s = x.replace(",", "").strip()
    try:
        if s.endswith("K"):
            return float(s[:-1])
        return float(s.rstrip("%"))
    except ValueError:
        return None

def compute_surprise_z(actual, forecast, mean, std):
    a = clean_macro_value(actual)
    f = clean_macro_value(forecast)
    if None in (a, f, mean, std):
        return None
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

# ── (D) Final Feature Generator ──
def get_features_for_date(target_date, ticker):
    feat = get_market_features(target_date, ticker)

    for var in urls:
        sel = df_summary[
            (df_summary['variable'] == var) &
            (df_summary['release_date'] == pd.to_datetime(target_date).date())
        ]
        if not sel.empty:
            actual = sel.iloc[0]['actual']
            forecast = sel.iloc[0]['forecast']
            z = compute_surprise_z(actual, forecast, mean_dict[var], std_dict[var])
            feat.loc[0, f"{var}_surprise_z"] = 0.0 if z is None else z
        else:
            feat.loc[0, f"{var}_surprise_z"] = 0.0

    return feat
