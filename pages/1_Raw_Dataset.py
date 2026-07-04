import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Raw Dataset",
    page_icon="📂",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("dataset/walmart_data.csv")

# ---------------- PAGE TITLE ----------------
st.title("📂 Raw Walmart Sales Dataset")

st.markdown("""
The raw dataset represents the original Walmart sales records before any preprocessing.
I first explored the data to understand its structure, identify missing values,
and evaluate its overall quality. This initial assessment guided the data cleaning
and feature engineering process used throughout the project.
""")

st.divider()

# ---------------- DATASET PREVIEW ----------------
st.subheader("Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ---------------- KPI CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

st.divider()

# ---------------- COLUMN INFORMATION ----------------
st.subheader("Column Information")

column_info = pd.DataFrame({
    "Column Name": df.columns,
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(column_info, use_container_width=True)

st.divider()

# ---------------- MISSING VALUES ----------------
st.subheader("Missing Values")

missing = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values
})

st.dataframe(missing, use_container_width=True)

st.divider()

# ---------------- SUMMARY STATISTICS ----------------
st.subheader("Summary Statistics")

st.dataframe(df.describe(), use_container_width=True)

st.divider()

# ---------------- DATA QUALITY ----------------
st.subheader("Initial Data Assessment")

st.markdown(f"""
- **Total Records:** {df.shape[0]}
- **Total Features:** {df.shape[1]}
- **Missing Values:** {int(df.isnull().sum().sum())}
- **Duplicate Records:** {df.duplicated().sum()}

The dataset was reviewed before preprocessing to identify potential data quality
issues and prepare it for further analysis.
""")