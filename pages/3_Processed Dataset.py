import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Processed Dataset",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(
    "dataset/walmart_preprocessed_data.csv",
    parse_dates=["Order Date", "Ship Date"]
)

# ---------------- TITLE ----------------
st.title("📊 Processed Dataset")

st.markdown("""

This processed dataset is the final output of the data preprocessing stage.
Missing values were handled, data types were standardized, and additional business-oriented features were created to support Python analysis, SQL reporting, and interactive Power BI dashboards.

""")

st.divider()

# ---------------- DATASET PREVIEW ----------------
st.subheader("Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ---------------- KPI ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

st.divider()

# ---------------- COLUMN DETAILS ----------------
st.subheader("Column Details")

column_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(column_info, use_container_width=True)

st.divider()

# ---------------- NEW FEATURES ----------------
st.subheader("New Features Created")

feature_df = pd.DataFrame({
    "Feature": [
        "Shipping Days",
        "Order Year",
        "Order Month",
        "Order Day of Week"
    ],
    "Description": [
        "Number of days taken for delivery",
        "Year extracted from Order Date",
        "Month extracted from Order Date",
        "Weekday extracted from Order Date"
    ]
})

st.dataframe(feature_df, use_container_width=True)

st.divider()

# ---------------- SUMMARY ----------------
st.subheader("Statistical Summary")

st.dataframe(df.describe(), use_container_width=True)

st.divider()

# ---------------- DOWNLOAD ----------------
st.subheader("Download Processed Dataset")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="walmart_preprocessed_data.csv",
    mime="text/csv"
)

st.divider()

# ---------------- FINAL NOTE ----------------

st.info("""
This processed dataset was used for Python analysis, SQL queries, and Power BI dashboard development.
It provides a clean and consistent foundation for generating business insights.
""")