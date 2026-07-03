select * from sales_data limit 5;
---total rows and orders
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT "Order ID") AS unique_orders
FROM sales_data;

SELECT "Order ID", "Order Date", "Customer Name", "Sales", "Profit" 
FROM sales_data 
LIMIT 5;

---1. Total sales and Total profit
SELECT 
    "Category",
    ROUND(SUM("Sales")::numeric, 2) AS total_sales,
    ROUND(SUM("Profit")::numeric, 2) AS total_profit
FROM sales_data
GROUP BY "Category"
ORDER BY total_profit DESC;


---2. Year-on-Year Sales Trend

SELECT 
    EXTRACT(YEAR FROM "Order Date"::date) AS order_year,
    ROUND(SUM("Sales")::numeric, 2) AS yearly_sales
FROM sales_data
GROUP BY EXTRACT(YEAR FROM "Order Date"::date)
ORDER BY order_year ASC;

---3. Monthly Sales Seasonality
SELECT 
    EXTRACT(MONTH FROM "Order Date"::date) AS order_month,
    ROUND(SUM("Sales")::numeric, 2) AS monthly_sales
FROM sales_data
GROUP BY EXTRACT(MONTH FROM "Order Date"::date)
ORDER BY order_month ASC;

---4. Top 5 Most Profitable States 
SELECT 
    "State",
    ROUND(SUM("Profit")::numeric, 2) AS total_profit
FROM sales_data
GROUP BY "State"
ORDER BY total_profit DESC
LIMIT 5;

---5. Top 5 Loss-Making Cities 
SELECT 
    "City",
    ROUND(SUM("Profit")::numeric, 2) AS total_profit
FROM sales_data
GROUP BY "City"
HAVING SUM("Profit") < 0
ORDER BY total_profit ASC
LIMIT 5

---6. Sales & Profit by Category
SELECT 
    "Category",
    ROUND(SUM("Sales")::numeric, 2) AS total_sales,
    ROUND(SUM("Profit")::numeric, 2) AS total_profit
FROM sales_data
GROUP BY "Category"
ORDER BY total_profit DESC;

---7. Top 5 Most Profitable Products 

SELECT *
FROM (
    SELECT
        "Product Name",
        ROUND(SUM("Profit")::numeric, 2) AS total_profit,
        RANK() OVER (ORDER BY SUM("Profit") DESC) AS profit_rank
    FROM sales_data
    GROUP BY "Product Name"
) ranked_products
WHERE profit_rank <= 5
ORDER BY profit_rank;

---8. Average Delivery Days by Category
SELECT 
    "Category",
    ROUND(AVG("Ship Date"::date - "Order Date"::date)::numeric, 2) AS avg_delivery_days
	FROM sales_data
GROUP BY "Category"
ORDER BY avg_delivery_days DESC;

---9. High-Value Orders Count 
SELECT 
    COUNT("Order ID") AS high_value_orders_count,
    ROUND(SUM("Sales")::numeric, 2) AS high_value_sales
FROM sales_data
WHERE "Sales" > 1000;

---10. Profitability Buckets 
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
