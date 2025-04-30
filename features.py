
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import timedelta

# Load Historical Data
cpi_yoy_final = pd.read_csv('historical/cpi_yoy_final.csv')
nonfarm_final = pd.read_csv('historical/nonfarm_final.csv')
ism_final = pd.read_csv('historical/ism_final.csv')
jobless_claims_final = pd.read_csv('historical/jobless_claims_final.csv')
housing_starts_final = pd.read_csv('historical/housing_starts_final.csv')
final_data = pd.read_csv('historical/final_data_spy.csv')
final_data_sso = pd.read_csv('historical/final_data_sso.csv')
final_data_upro = pd.read_csv('historical/final_data_upro.csv')
# ── (A) MACRO SCRAPER ──
urls = {
    "CPI": 'https://www.investing.com/economic-calendar/cpi-733',
    "NFP": 'https://www.investing.com/economic-calendar/nonfarm-payrolls-227',
    "ISM": 'https://www.investing.com/economic-calendar/ism-manufacturing-pmi-173',
    "Jobless_Claims": 'https://www.investing.com/economic-calendar/initial-jobless-claims-294',
    "Housing_Starts": 'https://www.investing.com/economic-calendar/housing-starts-298'
}

def get_actual_forecast_bs4(url):
    """
    Scrape the summary box on the calendar page for:
      - release_date (string),
      - actual (string),
      - forecast (string).
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers); resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # 1) release date
    date_span = (
        soup.select_one("p.eventDetails span.date")
        or soup.select_one("div.eventHeader span.date")
        or soup.find("span", class_="date")
    )
    release_date = date_span.get_text(strip=True) if date_span else None

    # 2) forecast
    fc = soup.select_one("div.arial_14.noBold")
    forecast = fc.get_text(strip=True) if fc else None

    # 3) actual (greenFont or redFont)
    ac = soup.select_one("div.arial_14.greenFont, div.arial_14.redFont")
    actual = ac.get_text(strip=True) if ac else None

    return release_date, actual, forecast

# Build a summary DataFrame of the *latest* release for each variable
records = []
for var, url in urls.items():
    rd, ac, fc = get_actual_forecast_bs4(url)
    records.append({
        "variable": var,
        "release_date": rd,
        "actual": ac,
        "forecast": fc
    })
df_summary = pd.DataFrame(records)
df_summary['release_date'] = pd.to_datetime(df_summary['release_date'], errors="coerce").dt.date


# ── (B) MARKET FEATURES ──
def get_market_features(target_date, ticker, recent_days=10):
    import pandas as pd
    import numpy as np
    import yfinance as yf
    from datetime import timedelta

    # 1) 計算時間範圍
    dt = pd.to_datetime(target_date)
    start = dt - timedelta(days=recent_days)
    end   = dt + timedelta(days=1)

    # 2) 下載行情
    df = yf.download([ticker, "^VIX"], start=start, end=end, progress=False)
    df.index = pd.to_datetime(df.index)

    # 3) 處理成交量
    vol = df[("Volume", ticker)].dropna()
    logv = np.log(vol + 1)

    # —— 以下 3 行是重點修改 —— 
    # lag_vol：取倒數第2筆（前一交易日）
    lag_vol        = logv.iloc[-2]
    # rolling_std_5d：取倒數第6到倒數第2筆的 std（過去 5 天）
    rolling_std_5d = logv.iloc[-6:-1].std()
    # lag_vix：VIX 收盤價倒數第2筆
    lag_vix        = df[("Close", "^VIX")].dropna().iloc[-2]

    # 4) 星期 dummy
    wd = dt.weekday()

    # 5) 輸出 DataFrame
    return pd.DataFrame([{
        "lag_vol":        lag_vol,
        "rolling_std_5d": rolling_std_5d,
        "lag_vix":        lag_vix,
        "monday_dummy":      int(wd == 0),
        "wednesday_dummy":   int(wd == 2),
        "friday_dummy":      int(wd == 4)
    }])







# def get_market_features(target_date, ticker, recent_days=10):
#     """
#     Download {ticker} & VIX up through target_date, then compute:
#       - lag_vol         : yesterday’s log(volume+1)
#       - rolling_std_5d  : 5-day rolling std of log(volume+1)
#       - lag_vix         : yesterday’s VIX close
#       - monday_dummy, wednesday_dummy, friday_dummy
#     """

#     dt = pd.to_datetime(target_date)
#     start = (dt - timedelta(days=recent_days)).strftime("%Y-%m-%d")
#     end   = (dt + timedelta(days=1)).strftime("%Y-%m-%d")

#     df = yf.download([ticker, "^VIX"], start=start, end=end, progress=False)

#     # 安全地存取 ticker 的 volume 和 VIX 的 close
#     try:
#         vol = df["Volume"][ticker].loc[:dt.strftime("%Y-%m-%d")]
#         logv = np.log(vol + 1)
#         lag_vol = logv.shift(1).iloc[-1]
#         rolling_std_5d = logv.rolling(5).std().iloc[-1]
#     except Exception as e:
#         raise ValueError(f"{ticker}: volume data processing error – {e}")

#     try:
#         vix_series = df["Close"]["^VIX"].loc[:dt.strftime("%Y-%m-%d")]
#         lag_vix = vix_series.shift(1).iloc[-1]
#     except Exception as e:
#         raise ValueError(f"VIX: close data processing error – {e}")

#     wd = dt.weekday()

#     return pd.DataFrame([{
#         "lag_vol": lag_vol,
#         "rolling_std_5d":  rolling_std_5d,
#         "lag_vix": lag_vix,
#         "monday_dummy": int(wd == 0),
#         "wednesday_dummy": int(wd == 2),
#         "friday_dummy": int(wd == 4)
#     }])



# ── (C) SURPRISE Z CALC ──
def clean_macro_value(x):
    """ '228K'->228.0 (thousands), '2.3%'->2.3, else float(x). """
    if x is None: return None
    s = x.replace(",", "").strip()
    try:
        if s.endswith("K"):
            return float(s[:-1])
        return float(s.rstrip("%"))
    except ValueError:
        return None

def compute_surprise_z(actual, forecast, mean, std):
    """
    z = ((actual - forecast) - mean) / std
    return None if any value missing.
    """
    a = clean_macro_value(actual)
    f = clean_macro_value(forecast)
    if None in (a,f,mean,std):
        return None
    return ((a - f) - mean) / std

# assume you have precomputed:
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

# ── (D) FINAL GET_FEATURES FUNCTION ──
def get_features_for_date(target_date, ticker):
    # 1) market
    feat = get_market_features(target_date, ticker)

    # 2) macro surprise_z (同一組)
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
