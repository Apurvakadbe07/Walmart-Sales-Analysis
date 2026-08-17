import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SQL Analysis",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🧠 SQL Analysis using PostgreSQL")

st.markdown(
    """
    The dataset is analysed using PostgreSQL to answer business questions
    related to sales, profitability, regional performance, delivery and
    order value.
    """
)

st.divider()


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"]
    )


# ============================================================
# RUN QUERY
# ============================================================

def run_query(query, params=None):

    conn = get_connection()

    return pd.read_sql_query(
        query,
        conn,
        params=params
    )


# ============================================================
# CONNECTION CHECK
# ============================================================

try:

    conn = get_connection()

    st.success("Connected to PostgreSQL successfully.")

except Exception as e:

    st.error("Unable to connect to PostgreSQL.")
    st.error(f"Connection error: {e}")
    st.stop()


# ============================================================
# GET ACTUAL PUBLIC TABLES
# ============================================================

tables_query = """
SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
"""

try:

    tables = run_query(tables_query)

except Exception as e:

    st.error("Unable to read PostgreSQL tables.")
    st.error(f"Database error: {e}")
    st.stop()


if tables.empty:

    st.warning(
        "No tables are currently available in the PostgreSQL database."
    )

    st.info(
        "Load the Walmart dataset into PostgreSQL before running the SQL analysis."
    )

    st.stop()


# ============================================================
# TABLE SELECTION
# ============================================================

table_names = tables["table_name"].tolist()

selected_table = st.selectbox(
    "Select table",
    table_names
)


# ============================================================
# GET ACTUAL COLUMNS
# ============================================================

columns_query = """
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = %s
ORDER BY ordinal_position;
"""

try:

    columns = run_query(
        columns_query,
        params=(selected_table,)
    )

except Exception as e:

    st.error("Unable to read table columns.")
    st.error(f"Database error: {e}")
    st.stop()


if columns.empty:

    st.warning(
        "No columns were found for the selected table."
    )

    st.stop()


column_names = columns["column_name"].tolist()


# ============================================================
# OPTIONAL SCHEMA INFORMATION
# ============================================================

with st.expander("View detected table structure"):

    st.dataframe(
        columns,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# COLUMN CHECK FUNCTION
# ============================================================

def required_columns_exist(required_columns):

    return all(
        column in column_names
        for column in required_columns
    )


# ============================================================
# SQL ANALYSIS
# ============================================================

st.divider()

st.header("📊 Business SQL Analysis")


# ============================================================
# QUERY 1
# ============================================================

st.subheader("1. Total Records and Unique Orders")

st.markdown(
    "**Business Question:** How many records and unique orders are available in the dataset?"
)

required = ["Order ID"]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT {order_id}) AS unique_orders
        FROM {table_name};
    """).format(
        order_id=sql.Identifier("Order ID"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Understand the size of the dataset and the number of unique orders."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because the required column is not available."
    )


st.divider()


# ============================================================
# QUERY 2
# ============================================================

st.subheader("2. Sales and Profit by Category")

st.markdown(
    "**Business Question:** Which product category generates the highest sales and profit?"
)

required = [
    "Category",
    "Sales",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {category} AS category,
            ROUND(SUM({sales})::numeric, 2) AS total_sales,
            ROUND(SUM({profit})::numeric, 2) AS total_profit
        FROM {table_name}
        GROUP BY {category}
        ORDER BY total_profit DESC;
    """).format(
        category=sql.Identifier("Category"),
        sales=sql.Identifier("Sales"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Compare category-wise sales and profitability."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 3
# ============================================================

st.subheader("3. Year-on-Year Sales Trend")

st.markdown(
    "**Business Question:** How have sales changed across different years?"
)

required = [
    "Order Date",
    "Sales"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            EXTRACT(
                YEAR FROM {order_date}::date
            ) AS order_year,

            ROUND(
                SUM({sales})::numeric,
                2
            ) AS yearly_sales

        FROM {table_name}

        GROUP BY
            EXTRACT(
                YEAR FROM {order_date}::date
            )

        ORDER BY order_year;
    """).format(
        order_date=sql.Identifier("Order Date"),
        sales=sql.Identifier("Sales"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Analyse yearly sales trends."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 4
# ============================================================

st.subheader("4. Monthly Sales Seasonality")

st.markdown(
    "**Business Question:** Which months generate higher sales?"
)

required = [
    "Order Date",
    "Sales"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            EXTRACT(
                MONTH FROM {order_date}::date
            ) AS order_month,

            ROUND(
                SUM({sales})::numeric,
                2
            ) AS monthly_sales

        FROM {table_name}

        GROUP BY
            EXTRACT(
                MONTH FROM {order_date}::date
            )

        ORDER BY order_month;
    """).format(
        order_date=sql.Identifier("Order Date"),
        sales=sql.Identifier("Sales"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Identify monthly sales patterns."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 5
# ============================================================

st.subheader("5. Top 5 Most Profitable States")

st.markdown(
    "**Business Question:** Which states contribute the highest profit?"
)

required = [
    "State",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {state} AS state,

            ROUND(
                SUM({profit})::numeric,
                2
            ) AS total_profit

        FROM {table_name}

        GROUP BY {state}

        ORDER BY total_profit DESC

        LIMIT 5;
    """).format(
        state=sql.Identifier("State"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Identify the top-performing states based on profit."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 6
# ============================================================

st.subheader("6. Top 5 Loss-Making Cities")

st.markdown(
    "**Business Question:** Which cities generated the highest losses?"
)

required = [
    "City",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {city} AS city,

            ROUND(
                SUM({profit})::numeric,
                2
            ) AS total_profit

        FROM {table_name}

        GROUP BY {city}

        HAVING SUM({profit}) < 0

        ORDER BY total_profit ASC

        LIMIT 5;
    """).format(
        city=sql.Identifier("City"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Identify cities with negative overall profitability."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 7
# ============================================================

st.subheader("7. Sales and Profit by Category")

st.markdown(
    "**Business Question:** How does each product category perform in terms of sales and profit?"
)

required = [
    "Category",
    "Sales",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {category} AS category,

            ROUND(
                SUM({sales})::numeric,
                2
            ) AS total_sales,

            ROUND(
                SUM({profit})::numeric,
                2
            ) AS total_profit

        FROM {table_name}

        GROUP BY {category}

        ORDER BY total_profit DESC;
    """).format(
        category=sql.Identifier("Category"),
        sales=sql.Identifier("Sales"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Compare sales and profitability across product categories."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 8
# ============================================================

st.subheader("8. Top 5 Most Profitable Products")

st.markdown(
    "**Business Question:** Which products contribute the highest profit?"
)

required = [
    "Product Name",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {product} AS product_name,

            ROUND(
                SUM({profit})::numeric,
                2
            ) AS total_profit

        FROM {table_name}

        GROUP BY {product}

        ORDER BY total_profit DESC

        LIMIT 5;
    """).format(
        product=sql.Identifier("Product Name"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Identify the products contributing most to profitability."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 9
# ============================================================

st.subheader("9. Average Delivery Days by Category")

st.markdown(
    "**Business Question:** Which product categories take longer to deliver?"
)

required = [
    "Category",
    "Order Date",
    "Ship Date"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT
            {category} AS category,

            ROUND(
                AVG(
                    {ship_date}::date
                    -
                    {order_date}::date
                )::numeric,
                2
            ) AS avg_delivery_days

        FROM {table_name}

        GROUP BY {category}

        ORDER BY avg_delivery_days DESC;
    """).format(
        category=sql.Identifier("Category"),
        order_date=sql.Identifier("Order Date"),
        ship_date=sql.Identifier("Ship Date"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Compare average delivery time across product categories."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 10
# ============================================================

st.subheader("10. High-Value Orders Analysis")

st.markdown(
    "**Business Question:** How many high-value orders with Sales greater than 1000 are present?"
)

required = [
    "Order ID",
    "Sales"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT

            COUNT({order_id})
            AS high_value_orders_count,

            ROUND(
                SUM({sales})::numeric,
                2
            ) AS high_value_sales

        FROM {table_name}

        WHERE {sales} > 1000;
    """).format(
        order_id=sql.Identifier("Order ID"),
        sales=sql.Identifier("Sales"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Measure the sales contribution of high-value orders."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# QUERY 11
# ============================================================

st.subheader("11. Profitability Segmentation")

st.markdown(
    "**Business Question:** How can orders be grouped based on profit?"
)

required = [
    "Order ID",
    "Sales",
    "Profit"
]

if required_columns_exist(required):

    query = sql.SQL("""
        SELECT

            {order_id} AS order_id,

            {sales} AS sales,

            {profit} AS profit,

            CASE

                WHEN {profit} < 0
                    THEN 'Loss Making'

                WHEN {profit} <= 50
                    THEN 'Low Profit'

                ELSE 'High Profit'

            END AS profit_bucket

        FROM {table_name}

        LIMIT 10;
    """).format(
        order_id=sql.Identifier("Order ID"),
        sales=sql.Identifier("Sales"),
        profit=sql.Identifier("Profit"),
        table_name=sql.Identifier(selected_table)
    )

    try:

        result = run_query(query.as_string(get_connection()))

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Purpose: Categorise orders based on profitability."
        )

    except Exception as e:

        st.error(f"Query execution failed: {e}")

else:

    st.info(
        "This analysis cannot be executed because one or more required columns are not available."
    )


st.divider()


# ============================================================
# SQL SKILLS
# ============================================================

st.header("🧠 SQL Skills Demonstrated")

st.markdown(
    """
    - SELECT and DISTINCT
    - WHERE and HAVING
    - SUM(), COUNT(), AVG()
    - GROUP BY
    - ORDER BY
    - LIMIT
    - Window Functions
    - RANK()
    - CASE WHEN
    - Business-focused SQL analysis
    """
)

st.info(
    "The results displayed above are fetched directly from PostgreSQL."
)