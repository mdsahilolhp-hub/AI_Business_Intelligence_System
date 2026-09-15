import mysql.connector
import json
import getpass


# ==========================================
# 1. CONNECT TO MYSQL
# ==========================================

print("🔄 Connecting to MySQL...")

mysql_password = getpass.getpass("Enter MySQL password: ")

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="powerbi_user",
    password=mysql_password,
    database="ai_business_intelligence"
)

cursor = conn.cursor(dictionary=True)

print("✅ MySQL connection successful!")


# ==========================================
# 2. OVERALL BUSINESS METRICS
# ==========================================

cursor.execute("""
    SELECT
        ROUND(SUM(Sales), 2) AS total_sales,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(
            (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
            2
        ) AS profit_margin,
        SUM(Quantity) AS total_quantity,
        COUNT(DISTINCT Order_ID) AS total_orders
    FROM sales
""")

overall = cursor.fetchone()


# ==========================================
# 3. CATEGORY PERFORMANCE
# ==========================================

cursor.execute("""
    SELECT
        Category,
        ROUND(SUM(Sales), 2) AS sales,
        ROUND(SUM(Profit), 2) AS profit,
        ROUND(
            (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
            2
        ) AS profit_margin
    FROM sales
    GROUP BY Category
    ORDER BY profit_margin DESC
""")

category_performance = cursor.fetchall()


# ==========================================
# 4. TOP 10 CUSTOMERS
# ==========================================

cursor.execute("""
    SELECT
        Customer_Name,
        ROUND(SUM(Sales), 2) AS sales,
        ROUND(SUM(Profit), 2) AS profit
    FROM sales
    GROUP BY Customer_Name
    ORDER BY sales DESC
    LIMIT 10
""")

top_customers = cursor.fetchall()


# ==========================================
# 5. TOP 10 PRODUCTS
# ==========================================

cursor.execute("""
    SELECT
        Product_Name,
        ROUND(SUM(Sales), 2) AS sales,
        ROUND(SUM(Profit), 2) AS profit,
        ROUND(
            (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
            2
        ) AS profit_margin
    FROM sales
    GROUP BY Product_Name
    ORDER BY sales DESC
    LIMIT 10
""")

top_products = cursor.fetchall()


# ==========================================
# 6. REGIONAL PERFORMANCE
# ==========================================

cursor.execute("""
    SELECT
        Region,
        ROUND(SUM(Sales), 2) AS sales,
        ROUND(SUM(Profit), 2) AS profit,
        ROUND(
            (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
            2
        ) AS profit_margin
    FROM sales
    GROUP BY Region
    ORDER BY profit_margin DESC
""")

regional_performance = cursor.fetchall()


# ==========================================
# 7. SALES CHANNEL PERFORMANCE
# ==========================================

cursor.execute("""
    SELECT
        Sales_Channel,
        ROUND(SUM(Sales), 2) AS sales,
        ROUND(SUM(Profit), 2) AS profit,
        ROUND(
            (SUM(Profit) / NULLIF(SUM(Sales), 0)) * 100,
            2
        ) AS profit_margin
    FROM sales
    GROUP BY Sales_Channel
    ORDER BY sales DESC
""")

channel_performance = cursor.fetchall()


# ==========================================
# 8. PREPARE AI ANALYSIS DATA
# ==========================================

analysis_data = {
    "overall": overall,
    "category_performance": category_performance,
    "top_customers": top_customers,
    "top_products": top_products,
    "regional_performance": regional_performance,
    "channel_performance": channel_performance
}


# ==========================================
# 9. SAVE JSON OUTPUT
# ==========================================

with open(
    "05_AI/ai_insights_output.json",
    "w",
    encoding="utf-8"
) as file:

   json.dump(
    analysis_data,
    file,
    indent=4,
    ensure_ascii=False,
    default=float
)


# ==========================================
# 10. DISPLAY BUSINESS SUMMARY
# ==========================================

print("\n" + "=" * 55)
print("📊 BUSINESS DATA EXTRACTED")
print("=" * 55)

print(f"Total Sales    : ₹{overall['total_sales']:,.2f}")
print(f"Total Profit   : ₹{overall['total_profit']:,.2f}")
print(f"Profit Margin  : {overall['profit_margin']}%")
print(f"Total Quantity : {overall['total_quantity']:,}")
print(f"Total Orders   : {overall['total_orders']:,}")


# ==========================================
# 11. TOP CUSTOMER
# ==========================================

print("\n🏆 TOP CUSTOMER")
print("-" * 55)

if top_customers:
    print(
        f"{top_customers[0]['Customer_Name']} "
        f"→ ₹{top_customers[0]['sales']:,.2f} Sales"
    )


# ==========================================
# 12. TOP PRODUCT
# ==========================================

print("\n🏆 TOP PRODUCT")
print("-" * 55)

if top_products:
    print(
        f"{top_products[0]['Product_Name']} "
        f"→ ₹{top_products[0]['sales']:,.2f} Sales"
    )


# ==========================================
# 13. BEST MARGIN CATEGORY
# ==========================================

print("\n📈 BEST MARGIN CATEGORY")
print("-" * 55)

if category_performance:
    print(
        f"{category_performance[0]['Category']} "
        f"→ {category_performance[0]['profit_margin']}% Margin"
    )


# ==========================================
# 14. BEST REGIONAL MARGIN
# ==========================================

print("\n🌍 BEST REGIONAL MARGIN")
print("-" * 55)

if regional_performance:
    print(
        f"{regional_performance[0]['Region']} "
        f"→ {regional_performance[0]['profit_margin']}% Margin"
    )


# ==========================================
# 15. OUTPUT FILE
# ==========================================

print("\n📁 JSON output saved successfully!")
print("📄 File: 05_AI/ai_insights_output.json")


# ==========================================
# 16. CLOSE CONNECTION
# ==========================================

cursor.close()
conn.close()

print("\n" + "=" * 55)
print("✅ AI BUSINESS DATA EXTRACTION COMPLETED!")
print("=" * 55)