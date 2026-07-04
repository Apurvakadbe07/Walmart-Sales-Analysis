import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Python Analysis",
    page_icon="🐍",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("dataset/walmart_preprocessed_data.csv")

# ---------------- TITLE ----------------
st.title("🐍 Python Exploratory Data Analysis")

st.markdown("""
After preparing the dataset, I explored it using Python and Pandas to understand
sales performance, customer purchasing behaviour, product categories, and profit trends.
The analysis helped identify patterns that were later used in SQL queries and Power BI dashboards.
""")

st.divider()

# ---------------- KPI ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"₹ {df['Sales'].sum():,.2f}")

with col2:
    st.metric("Total Profit", f"₹ {df['Profit'].sum():,.2f}")

with col3:
    st.metric("Total Quantity Sold", int(df["Quantity"].sum()))

st.divider()

# ---------------- CATEGORY ----------------
st.subheader("Sales by Category")

category = (
    df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)

st.dataframe(category, use_container_width=True)

st.divider()

# ---------------- STATE ----------------
st.subheader("Top 10 States by Sales")

state_sales = (
    df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(state_sales, use_container_width=True)

st.divider()

# ---------------- PRODUCTS ----------------
st.subheader("Top 10 Products by Sales")

product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(product_sales, use_container_width=True)

st.divider()

# ---------------- YEAR ----------------
st.subheader("Year-wise Sales")

year_sales = (
    df.groupby("Order Year")["Sales"]
    .sum()
)

st.dataframe(year_sales, use_container_width=True)

st.divider()

# ---------------- MONTH ----------------
st.subheader("Monthly Sales")

month_sales = (
    df.groupby("Order Month")["Sales"]
    .sum()
)

st.dataframe(month_sales, use_container_width=True)

st.divider()

# ---------------- PYTHON LIBRARIES ----------------
st.subheader("Python Libraries Used")

st.code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns        
""", language="python")

st.divider()

# ---------------- CONCLUSION ----------------
st.subheader("Key Findings")

st.markdown("""
- Sales performance varies across product categories.
- A small number of products contribute significantly to overall revenue.
- Sales distribution differs across states.
- Monthly and yearly trends help identify seasonal business patterns.
- These observations were further explored using PostgreSQL and Power BI.
""")