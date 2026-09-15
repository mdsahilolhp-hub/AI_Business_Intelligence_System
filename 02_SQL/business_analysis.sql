-- =========================================================
-- AI-Powered Business Intelligence & Decision System
-- SQL Business Analysis
-- =========================================================

USE ai_business_intelligence;


-- =========================================================
-- 1. Overall Business KPIs
-- =========================================================

SELECT
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Percent
FROM sales;


-- =========================================================
-- 2. Regional Performance
-- =========================================================

SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Percent
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;


-- =========================================================
-- 3. Category Performance
-- =========================================================

SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Percent,
    SUM(Quantity) AS Units_Sold
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;


-- =========================================================
-- 4. Monthly Sales and Profit Trend
-- =========================================================

SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS Month,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
ORDER BY Month;


-- =========================================================
-- 5. Top 10 Products by Sales
-- =========================================================

SELECT
    Product_ID,
    Product_Name,
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Units_Sold
FROM sales
GROUP BY
    Product_ID,
    Product_Name,
    Category
ORDER BY Total_Sales DESC
LIMIT 10;


-- =========================================================
-- 6. Top 10 Customers by Sales
-- =========================================================

SELECT
    Customer_ID,
    Customer_Name,
    Customer_Segment,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Units_Purchased,
    COUNT(DISTINCT Order_ID) AS Number_of_Orders
FROM sales
GROUP BY
    Customer_ID,
    Customer_Name,
    Customer_Segment
ORDER BY Total_Sales DESC
LIMIT 10;


-- =========================================================
-- 7. Sales Channel Performance
-- =========================================================

SELECT
    Sales_Channel,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Percent,
    COUNT(DISTINCT Order_ID) AS Number_of_Orders
FROM sales
GROUP BY Sales_Channel
ORDER BY Total_Sales DESC;


-- =========================================================
-- 8. Customer Segment Performance
-- =========================================================

SELECT
    Customer_Segment,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Percent,
    COUNT(DISTINCT Customer_ID) AS Unique_Customers,
    COUNT(DISTINCT Order_ID) AS Number_of_Orders
FROM sales
GROUP BY Customer_Segment
ORDER BY Total_Sales DESC;