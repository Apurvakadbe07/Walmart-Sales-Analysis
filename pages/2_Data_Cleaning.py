import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Cleaning",
    page_icon="🧹",
    layout="wide"
)

raw_df = pd.read_csv("dataset/walmart_data.csv")
clean_df = pd.read_csv("dataset/walmart_preprocessed_data.csv")

st.title("🧹 Data Cleaning & Preprocessing")

st.markdown("""
Before performing any analysis, I cleaned and transformed the raw dataset to improve its quality and make it suitable for business analysis.
""")

st.divider()

st.subheader("Cleaning Steps Performed")

st.markdown("""
✅ Checked missing values

✅ Checked duplicate records

✅ Converted date columns into datetime format

✅ Created **Shipping Days**

✅ Extracted **Order Year**

✅ Extracted **Order Month**

✅ Extracted **Order Day of Week**

✅ Saved the cleaned dataset for analysis
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Dataset")
    st.metric("Rows", raw_df.shape[0])
    st.metric("Columns", raw_df.shape[1])

with col2:
    st.subheader("Processed Dataset")
    st.metric("Rows", clean_df.shape[0])
    st.metric("Columns", clean_df.shape[1])

st.divider()

st.subheader("New Features Added")

feature_df = pd.DataFrame({
    "Feature": [
        "Shipping Days",
        "Order Year",
        "Order Month",
        "Order Day of Week"
    ],
    "Purpose": [
        "Delivery Time Analysis",
        "Year-wise Analysis",
        "Monthly Sales Trend",
        "Weekday Sales Analysis"
    ]
})

st.dataframe(feature_df, use_container_width=True)

st.divider()

st.success("The cleaned dataset is now ready for exploratory analysis, SQL queries, and dashboard creation.")