# # --- pages/5_Get_Features.py ---
# # 📂 Get Features for a Specific Date
# import streamlit as st
# import pandas as pd
# from features import get_features_for_date

# st.set_page_config(page_title="Get Features", layout="wide")

# st.title("📂 Get Features for a Specific Date")

# target_date = st.date_input("Select a date:", value=pd.to_datetime("2025-04-25"))

# if st.button("Get Features"):
#     with st.spinner("Loading features..."):
#         features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
#     st.dataframe(features)
# --- pages/3_Get_Features.py ---
# 📂 Get Features for a Specific Date

import streamlit as st
import pandas as pd
from features import get_features_for_date

# --- Page Settings ---
st.set_page_config(page_title="Get Features", layout="wide")

# --- Title ---
st.title("📂 Get Features for a Specific Date")

# --- Date Selection ---
target_date = st.date_input(
    "Select a date to retrieve features:", 
    value=pd.to_datetime("2025-04-25"), 
    min_value=pd.to_datetime("2010-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

# --- Button to trigger feature retrieval ---
if st.button("Get Features"):
    with st.spinner("Loading features..."):
        features = get_features_for_date(target_date.strftime("%Y-%m-%d"))
    st.success("Features loaded successfully!")
    st.dataframe(features, use_container_width=True)

