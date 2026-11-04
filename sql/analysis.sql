-- Load outputs/clean_sales.csv into a table named sales.
-- Suggested types: InvoiceNo VARCHAR, StockCode VARCHAR, Description VARCHAR,
-- Quantity INTEGER, InvoiceDate TIMESTAMP, UnitPrice DECIMAL(12,2),
-- CustomerID VARCHAR, Country VARCHAR, Revenue DECIMAL(14,2).

-- 1. Overall KPIs
SELECT COUNT(DISTINCT InvoiceNo) AS orders,
       SUM(Quantity) AS units_sold,
       ROUND(SUM(Revenue), 2) AS revenue_gbp,
       ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS average_order_value
FROM sales;

-- 2. Monthly sales trend
SELECT DATE_TRUNC('month', InvoiceDate) AS order_month,
       ROUND(SUM(Revenue), 2) AS revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY 1
ORDER BY 1;

-- 3. Revenue by country
SELECT Country,
       ROUND(SUM(Revenue), 2) AS revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY Country
ORDER BY revenue_gbp DESC;

-- 4. Top products by revenue
SELECT StockCode, MAX(Description) AS product,
       SUM(Quantity) AS units,
       ROUND(SUM(Revenue), 2) AS revenue_gbp
FROM sales
GROUP BY StockCode
ORDER BY revenue_gbp DESC
LIMIT 20;

-- 5. Customer revenue concentration
WITH customer_sales AS (
    SELECT CustomerID, SUM(Revenue) AS revenue
    FROM sales
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT CustomerID, revenue,
       SUM(revenue) OVER (ORDER BY revenue DESC) /
       SUM(revenue) OVER () AS cumulative_revenue_share
FROM customer_sales
ORDER BY revenue DESC;
