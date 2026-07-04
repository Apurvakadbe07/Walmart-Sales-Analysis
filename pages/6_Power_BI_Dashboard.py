import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(page_title="Dashboard | Walmart Sales Analysis", layout="wide")

st.title("📊 Walmart Sales Dashboard")

st.write("""
This page presents the Power BI dashboard created as part of the Walmart Sales Analysis project.
It helps visualize key business insights such as sales performance, profit trends, and category-wise analysis.
""")

st.divider()

# -------------------------
# Sales & Profit Overview
# -------------------------

st.subheader("Walmart Executive Sales Analysis")

st.write("""
This dashboard shows the analysis of sales performance, seasonal trends, and year-over-year growth.

• It shows clear seasonal variation in monthly sales, with demand fluctuating across the year.

• The highest sales are observed in December (116K), indicating strong holiday season impact.

• The lowest sales are observed in February (16K), showing reduced off-season demand.

• Year-over-Year analysis shows an increase in sales from 0.15M (2011) to 0.25M (2014), indicating steady growth.

• Q4 (October–December) consistently shows higher sales compared to other quarters.

• The analysis indicates that sales performance is highly influenced by seasonal patterns rather than uniform demand.
""")



img1 = Image.open("images/Dashboard 1.png")
st.image(img1, use_container_width=True)

st.divider()


#2nd

st.subheader("Profit and Performance Analysis")

st.write("""
This dashboard shows state-wise profit and loss distribution along with category-wise sales and profitability analysis.

• It shows a clear imbalance in profitability across states, with performance concentrated in a few regions.

• California is the most profitable state with 76K profit, while Colorado records the highest loss at -7K.

• The analysis indicates that overall profit is heavily dependent on a limited number of high-performing states.

• Copiers (19.3K) and Accessories (16.4K) are the top profit-generating product categories.

• Machines and Bookcases are consistently loss-making categories and require cost or pricing optimization.

• The data highlights regional and category-level inefficiencies that impact overall profitability.


""")

img2 = Image.open("images/Dashboard 2.png")
st.image(img2, use_container_width=True)

st.divider()

# 3rd
st.subheader("logistics & product Insights")

st.write("""
This dashboard shows order-level metrics, customer segmentation, delivery performance, and product-level profitability.

• It shows total orders along with key operational and customer performance indicators.

• VIP customers contribute 41.4% of total revenue, making them a significant revenue-driving segment.

• Average shipping time is 3.93 days, which meets the 4-day delivery target, indicating efficient logistics performance.

• On-time delivery rate is 81.3%, but a declining trend across months suggests inconsistency in delivery performance.

• Delivery performance varies over time, indicating operational fluctuations that may require process monitoring.

• Canon imageCLASS 2200 is the highest profit-generating product with 6.72K profit.


""")

img3 = Image.open("images/Dashboard 3.png")
st.image(img3, use_container_width=True)

st.divider()


# -------------------------
# Final Insight
# -------------------------

st.success("""

This dashboard provides a complete analysis of Walmart sales performance, profitability, customer segmentation, and delivery operations. The sales data shows clear seasonal patterns, with peak performance in December and lower sales in February, along with steady year-over-year growth. Profitability analysis highlights a strong regional imbalance, where California is the most profitable state (76K) while Colorado records the highest loss (-7K), and category performance shows Copiers and Accessories as top profit contributors, whereas Machines and Bookcases are loss-making. From an operational perspective, VIP customers contribute 41.4% of total revenue, making them a key segment, while the average shipping time of 3.93 days meets the delivery target of 4 days. However, the on-time delivery rate of 81.3% shows a declining trend across months, indicating inconsistency in delivery performance. Overall, Walmart demonstrates strong revenue generation but requires improvements in regional profitability balance, loss-making categories, and delivery consistency.

""")