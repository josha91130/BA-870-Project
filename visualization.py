
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_predictions(etf_name):
    try:
        # 讀對應資產的 validation 預測資料
        file_path = f"validation_preds/{etf_name}_validation_preds.csv"
        df = pd.read_csv(file_path)

        # 讀取日期、實際值、預測值
        dates = pd.to_datetime(df['date'])
        actual = df['Actual']
        predicted = df['Predicted']

        # 畫線圖
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(dates, actual, label='Actual', linewidth=2)
        ax.plot(dates, predicted, label='Predicted', linewidth=2)
        ax.set_xlabel("Date")
        ax.set_ylabel("log(volume)")
        ax.set_title(f"{etf_name} - Predicted vs Actual (Validation)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error loading or plotting {etf_name}: {e}")
