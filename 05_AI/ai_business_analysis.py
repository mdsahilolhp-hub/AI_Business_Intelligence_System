import json
import os
import mysql.connector
from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv("05_AI/.env")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "ai_business_intelligence"
)


# ==========================================
# 2. VALIDATE MYSQL CONFIGURATION
# ==========================================

required_variables = {
    "MYSQL_USER": MYSQL_USER,
    "MYSQL_PASSWORD": MYSQL_PASSWORD,
    "MYSQL_DATABASE": MYSQL_DATABASE
}

missing_variables = [
    name
    for name, value in required_variables.items()
    if not value
]

if missing_variables:
    print(
        "Missing environment variables: "
        + ", ".join(missing_variables)
    )
    raise SystemExit(1)


# ==========================================
# 3. CONNECT TO MYSQL
# ==========================================

print("Connecting to MySQL...")

conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    cursor = conn.cursor(dictionary=True)

    print("MySQL connection successful!")


    # ==========================================
    # 4. OVERALL BUSINESS METRICS
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
    # 5. CATEGORY PERFORMANCE
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
    # 6. TOP 10 CUSTOMERS
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
    # 7. TOP 10 PRODUCTS
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
    # 8. REGIONAL PERFORMANCE
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
        WHERE Region IS NOT NULL
          AND TRIM(Region) <> ''
          AND LOWER(TRIM(Region)) <> 'unknown'
        GROUP BY Region
        ORDER BY profit_margin DESC
    """)

    regional_performance = cursor.fetchall()


    # ==========================================
    # 9. SALES CHANNEL PERFORMANCE
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
    # 10. PREPARE AI ANALYSIS DATA
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
    # 11. SAVE JSON OUTPUT
    # ==========================================

    output_file = "05_AI/ai_insights_output.json"

    with open(
        output_file,
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
    # 12. DISPLAY BUSINESS SUMMARY
    # ==========================================

    print()
    print("=" * 55)
    print("BUSINESS DATA EXTRACTED")
    print("=" * 55)

    print(
        f"Total Sales    : "
        f"${overall['total_sales']:,.2f}"
    )

    print(
        f"Total Profit   : "
        f"${overall['total_profit']:,.2f}"
    )

    print(
        f"Profit Margin  : "
        f"{overall['profit_margin']}%"
    )

    print(
        f"Total Quantity : "
        f"{overall['total_quantity']:,}"
    )

    print(
        f"Total Orders   : "
        f"{overall['total_orders']:,}"
    )


    # ==========================================
    # 13. TOP CUSTOMER
    # ==========================================

    print()
    print("TOP CUSTOMER")
    print("-" * 55)

    if top_customers:
        print(
            f"{top_customers[0]['Customer_Name']} "
            f"-> ${top_customers[0]['sales']:,.2f} Sales"
        )


    # ==========================================
    # 14. TOP PRODUCT
    # ==========================================

    print()
    print("TOP PRODUCT")
    print("-" * 55)

    if top_products:
        print(
            f"{top_products[0]['Product_Name']} "
            f"-> ${top_products[0]['sales']:,.2f} Sales"
        )


    # ==========================================
    # 15. BEST MARGIN CATEGORY
    # ==========================================

    print()
    print("BEST MARGIN CATEGORY")
    print("-" * 55)

    if category_performance:
        print(
            f"{category_performance[0]['Category']} "
            f"-> {category_performance[0]['profit_margin']}% Margin"
        )


    # ==========================================
    # 16. BEST REGIONAL MARGIN
    # ==========================================

    print()
    print("BEST REGIONAL MARGIN")
    print("-" * 55)

    if regional_performance:
        print(
            f"{regional_performance[0]['Region']} "
            f"-> {regional_performance[0]['profit_margin']}% Margin"
        )


    # ==========================================
    # 17. OUTPUT FILE
    # ==========================================

    print()
    print("JSON output saved successfully!")
    print(f"File: {output_file}")


except mysql.connector.Error as error:
    print()
    print("MySQL connection or query failed.")
    print(f"Error: {error}")
    raise SystemExit(1)

except (OSError, TypeError, ValueError) as error:
    print()
    print("File or data processing failed.")
    print(f"Error: {error}")
    raise SystemExit(1)

finally:
    if cursor is not None:
        cursor.close()

    if conn is not None and conn.is_connected():
        conn.close()

    print()
    print("=" * 55)
    print("AI BUSINESS DATA EXTRACTION COMPLETED")
    print("=" * 55)