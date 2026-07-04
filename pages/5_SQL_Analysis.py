import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SQL Analysis",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SQL Analysis using PostgreSQL")

st.markdown("""
After preparing the dataset in Python, I imported it into PostgreSQL to answer
business-related questions. The following queries were written to explore sales
performance, profitability, regional trends, and customer insights.
""")

st.divider()

# ----------------------------------------------------
st.subheader("Query 1 : Total Records and Unique Orders")

st.markdown("**Business Question:** How many records and unique orders are available in the dataset?")

st.code("""
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT "Order ID") AS unique_orders
FROM sales_data;
""", language="sql")

st.success("Purpose : Understand the size of the dataset and verify the number of unique orders.")

st.divider()

# ----------------------------------------------------
st.subheader("Query 2 : Sales and Profit by Category")

st.markdown("**Business Question:** Which product category generates the highest sales and profit?")

st.code("""
SELECT
    "Category",
    ROUND(SUM("Sales")::numeric,2) AS total_sales,
    ROUND(SUM("Profit")::numeric,2) AS total_profit
FROM sales_data
GROUP BY "Category"
ORDER BY total_profit DESC;
""", language="sql")

st.success("Purpose : Compare category-wise performance and identify the most profitable category.")

st.divider()

# ----------------------------------------------------
st.subheader("Query 3 : Year-on-Year Sales Trend")

st.markdown("**Business Question:** How have sales changed over different years?")

st.code("""
SELECT
    EXTRACT(YEAR FROM "Order Date"::date) AS order_year,
    ROUND(SUM("Sales")::numeric,2) AS yearly_sales
FROM sales_data
GROUP BY EXTRACT(YEAR FROM "Order Date"::date)
ORDER BY order_year;
""", language="sql")

st.success("Purpose : Analyze yearly sales growth and overall business performance.")

st.divider()

# ----------------------------------------------------
st.subheader("Query 4 : Monthly Sales Seasonality")

st.markdown("**Business Question:** Which months generate higher sales?")

st.code("""
SELECT
    EXTRACT(MONTH FROM "Order Date"::date) AS order_month,
    ROUND(SUM("Sales")::numeric,2) AS monthly_sales
FROM sales_data
GROUP BY EXTRACT(MONTH FROM "Order Date"::date)
ORDER BY order_month;
""", language="sql")

st.success("Purpose : Identify monthly sales trends and seasonal demand patterns.")

st.divider()

# ----------------------------------------------------
st.subheader("Query 5 : Top 5 Most Profitable States")

st.markdown("**Business Question:** Which states contribute the highest profit?")

st.code("""
SELECT
    "State",
    ROUND(SUM("Profit")::numeric,2) AS total_profit
FROM sales_data
GROUP BY "State"
ORDER BY total_profit DESC
LIMIT 5;
""", language="sql")

st.success("Purpose : Identify the top-performing states based on total profit.")

st.divider()

# =========================
# 📊 ADVANCED SQL ANALYSIS 
# =========================

st.header("📊 Advanced Business SQL Analysis")

# ----------------------------------------------------
st.container()
st.subheader("Query 6 : Top 5 Loss-Making Cities")

st.markdown("**Business Question:** Which cities generated the highest losses?")

st.code("""
SELECT
    "City",
    ROUND(SUM("Profit")::numeric,2) AS total_profit
FROM sales_data
GROUP BY "City"
HAVING SUM("Profit") < 0
ORDER BY total_profit ASC
LIMIT 5;
""", language="sql")

st.success("Insight: These cities are consistently generating losses and need cost optimization strategies.")

st.divider()

# ----------------------------------------------------
st.container()
st.subheader("Query 7 : Sales and Profit by Category")

st.markdown("**Business Question:** How does each product category perform in terms of sales and profit?")

st.code("""
SELECT
    "Category",
    ROUND(SUM("Sales")::numeric,2) AS total_sales,
    ROUND(SUM("Profit")::numeric,2) AS total_profit
FROM sales_data
GROUP BY "Category"
ORDER BY total_profit DESC;
""", language="sql")

st.success("Insight: Helps compare which categories are driving revenue vs profitability.")

st.divider()

# ----------------------------------------------------
st.container()
st.subheader("Query 8 : Top 5 Most Profitable Products")

st.markdown("**Business Question:** Which products contribute the highest profit?")

st.code("""
SELECT *
FROM (
    SELECT
        "Product Name",
        ROUND(SUM("Profit")::numeric,2) AS total_profit,
        RANK() OVER (ORDER BY SUM("Profit") DESC) AS profit_rank
    FROM sales_data
    GROUP BY "Product Name"
) ranked_products
WHERE profit_rank <= 5
ORDER BY profit_rank;
""", language="sql")

st.success("Insight: These products are the key revenue drivers of the business.")

st.divider()

# ----------------------------------------------------
st.container()
st.subheader("Query 9 : Average Delivery Days by Category")

st.markdown("**Business Question:** Which product categories take longer to deliver?")

st.code("""
SELECT
    "Category",
    ROUND(AVG("Ship Date"::date - "Order Date"::date)::numeric,2) AS avg_delivery_days
FROM sales_data
GROUP BY "Category"
ORDER BY avg_delivery_days DESC;
""", language="sql")

st.success("Insight: Longer delivery time may impact customer satisfaction.")

st.divider()

# ----------------------------------------------------
st.container()
st.subheader("Query 10 : High-Value Orders Analysis")

st.markdown("**Business Question:** How many high-value orders (Sales > 1000) are present?")

st.code("""
SELECT
    COUNT("Order ID") AS high_value_orders_count,
    ROUND(SUM("Sales")::numeric,2) AS high_value_sales
FROM sales_data
WHERE "Sales" > 1000;
""", language="sql")

st.success("Insight: High-value orders contribute significantly to total revenue.")

st.divider()

# ----------------------------------------------------
st.container()
st.subheader("Bonus Query : Profitability Segmentation")

st.markdown("**Business Question:** How can orders be grouped based on profit?")

st.code("""
SELECT
    "Order ID",
    "Sales",
    "Profit",
    CASE
        WHEN "Profit" < 0 THEN 'Loss Making'
        WHEN "Profit" <= 50 THEN 'Low Profit'
        ELSE 'High Profit'
    END AS profit_bucket
FROM sales_data
LIMIT 10;
""", language="sql")

st.success("Insight: Helps in categorizing orders for better business decisions.")

st.divider()

# =========================
# 📌 SKILLS SECTION
# =========================

st.header("🧠 SQL Skills Demonstrated")

st.markdown("""
✔ Data Retrieval using SELECT  
✔ Filtering using WHERE & HAVING  
✔ Aggregation using SUM(), COUNT(), AVG()  
✔ Grouping using GROUP BY  
✔ Sorting using ORDER BY  
✔ Window Functions (RANK)  
✔ Conditional Logic (CASE WHEN)  
✔ Business Reporting using SQL  
""")

st.info("""
This analysis focuses on real-world business problems like sales, profit, delivery time, and product performance.
It is directly aligned with Data Analyst job roles.
""")