import streamlit as st
import pandas as pd
from PIL import Image


def load_css():
    with open(".streamlit/styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Walmart Sales Analysis",
    page_icon="📊",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📁 Dataset",
        "🐍 Python Analysis"
    ]
)


# ---------------- HOME PAGE ----------------
if page == "🏠 Home":

    st.title("📊 Walmart Sales Analysis Project")
    st.markdown("---")

    # Image + Introduction
    col1, col2 = st.columns([1, 2])

    from PIL import Image

    with col1:
       img = Image.open("images3/walmart.jpeg")
       img = img.resize((450, 450))  # (width, height)
       st.image(img)

    with col2:

       st.markdown("""
       <h2>About Walmart</h2>

       <p style="
          text-align: justify;
          font-size:18px;
          line-height:1.8;
       ">
       Walmart is one of the world's largest multinational retail corporations, operating thousands of hypermarkets, discount stores, and e-commerce platforms across multiple countries. The company serves millions of customers every day and relies heavily on data-driven strategies to improve operational efficiency and customer experience.
       <br><br>
       This project presents an end-to-end sales analysis of Walmart using <b>Python</b>, <b>PostgreSQL</b>, <b>Power BI</b>, and <b>Streamlit</b>. The objective is to transform raw sales data into meaningful business insights by analyzing sales performance, profitability, customer behavior, regional trends, and operational efficiency.
       </p>
       """, unsafe_allow_html=True)
    st.markdown("---")

    # Technology Stack
    st.subheader("🛠 Technology Stack")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("""
### 🐍 Python
- Data Cleaning
- Data Analysis
- Pandas
""")

    with col2:
        st.info("""
### 🗄 PostgreSQL
- SQL Queries
- Aggregations
- Window Functions
""")

    with col3:
        st.info("""
### 📊 Power BI
- KPI Dashboard
- Interactive Reports
- Business Insights
""")

    with col4:
        st.info("""
### 🌐 Streamlit
- Interactive Web App
- Portfolio Deployment
- Data Presentation
""")

    st.markdown("---")

    st.subheader("📋 Project Workflow")

    st.success("""
1️⃣ Data Collection

2️⃣ Data Cleaning using Python

3️⃣ Exploratory Data Analysis (EDA)

4️⃣ SQL Business Analysis

5️⃣ Interactive Dashboard Development in Power BI

6️⃣ Business Insights & Reporting using Streamlit
""")

    st.markdown("---")

    st.subheader("🎯 Project Objectives")

    st.write("""
- Analyze Walmart sales performance across different states and cities.
- Identify profitable and loss-making categories.
- Evaluate customer purchasing behavior.
- Monitor delivery performance and operational efficiency.
- Support data-driven business decision-making through interactive dashboards.
""")

# ---------------- DATASET PAGE ----------------
# ---------------- DATASET PAGE ----------------
elif page == "📁 Dataset":

    st.title("📁 Walmart Sales Dataset")

    # Load Dataset
    df = pd.read_csv("dataset/walmart_data.csv")

    st.markdown("### Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")

    # Basic Information
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    st.markdown("---")

    st.subheader("Column Information")
    column_info = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(column_info, use_container_width=True)

    st.markdown("---")

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    st.markdown("---")

    st.subheader("Missing Values")
    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing, use_container_width=True)



    # ---------------- PYTHON ANALYSIS PAGE ----------------
elif page == "🐍 Python Analysis":

    st.title("🐍 Python Data Analysis")

    # Load Dataset
    df = pd.read_csv("dataset/walmart_data.csv")

    st.markdown("### Basic Data Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Sales", f"{df['Sales'].sum():,.2f}")

    with col2:
        st.metric("Total Profit", f"{df['Profit'].sum():,.2f}")

    st.markdown("---")

    st.subheader("Sales by Category")

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
    )

    st.dataframe(category_sales, use_container_width=True)

    st.markdown("---")

    st.subheader("Top 10 Customers by Sales")

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(10)
    )

    st.dataframe(top_customers, use_container_width=True)

    st.markdown("---")

    st.subheader("Python Code Used")

    st.code("""
# Total Sales
df['Sales'].sum()

# Total Profit
df['Profit'].sum()

# Sales by Category
df.groupby('Category')['Sales'].sum()

# Top Customers
df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
""", language="python")