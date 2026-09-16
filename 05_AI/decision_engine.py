import json
import os


# ============================================================
# AI-POWERED BUSINESS DECISION ENGINE
# ============================================================

INPUT_FILE = "05_AI/ai_insights_output.json"
OUTPUT_FILE = "05_AI/ai_decision_report.json"


# ============================================================
# 1. LOAD EXTRACTED BUSINESS DATA
# ============================================================

try:
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

except FileNotFoundError:
    print(f"ERROR: Input file not found: {INPUT_FILE}")
    raise SystemExit(1)

except json.JSONDecodeError as error:
    print(f"ERROR: Invalid JSON in {INPUT_FILE}")
    print(f"Details: {error}")
    raise SystemExit(1)


overall = data.get("overall", {})
categories = data.get("category_performance", [])
customers = data.get("top_customers", [])
products = data.get("top_products", [])
regions = data.get("regional_performance", [])


# ============================================================
# 2. VALIDATE REQUIRED DATA
# ============================================================

required_overall_fields = [
    "total_sales",
    "total_profit",
    "profit_margin",
    "total_orders"
]

missing_fields = [
    field
    for field in required_overall_fields
    if field not in overall
]

if missing_fields:
    print(
        "ERROR: Missing required business metrics: "
        + ", ".join(missing_fields)
    )
    raise SystemExit(1)


# ============================================================
# 3. INITIALIZE DECISION INSIGHTS
# ============================================================

risks = []
opportunities = []


# ============================================================
# 4. CATEGORY ANALYSIS
# ============================================================

if categories:

    lowest_margin_category = min(
        categories,
        key=lambda x: x.get("profit_margin", 0)
    )

    highest_margin_category = max(
        categories,
        key=lambda x: x.get("profit_margin", 0)
    )

    lowest_category_margin = lowest_margin_category.get(
        "profit_margin",
        0
    )

    highest_category_margin = highest_margin_category.get(
        "profit_margin",
        0
    )

    # --------------------------------------------------------
    # Margin Risk
    # --------------------------------------------------------

    if lowest_category_margin < 25:

        risks.append({
            "topic": "Margin Risk",
            "finding": (
                f"{lowest_margin_category['Category']} has the "
                f"lowest profit margin at "
                f"{lowest_category_margin}%."
            ),
            "recommendation": (
                "Review pricing, discounts, supplier costs "
                "and product-level profitability."
            )
        })

    # --------------------------------------------------------
    # High Margin Opportunity
    # --------------------------------------------------------

    opportunities.append({
        "topic": "High-Margin Opportunity",
        "finding": (
            f"{highest_margin_category['Category']} has the "
            f"highest profit margin at "
            f"{highest_category_margin}%."
        ),
        "recommendation": (
            "Prioritize high-margin products and expand "
            "profitable offerings."
        )
    })


# ============================================================
# 5. PRODUCT ANALYSIS
# ============================================================

if products:

    top_product = products[0]

    highest_product_margin = max(
        products,
        key=lambda x: x.get("profit_margin", 0)
    )

    top_product_sales = top_product.get(
        "sales",
        0
    )

    highest_product_margin_value = highest_product_margin.get(
        "profit_margin",
        0
    )

    # --------------------------------------------------------
    # Top Product
    # --------------------------------------------------------

    opportunities.append({
        "topic": "Top Product",
        "finding": (
            f"{top_product['Product_Name']} generates the "
            f"highest sales among the top products at "
            f"${top_product_sales:,.2f}."
        ),
        "recommendation": (
            "Maintain availability and prioritize this "
            "product in sales and retention strategies."
        )
    })

    # --------------------------------------------------------
    # Product Profitability
    # --------------------------------------------------------

    opportunities.append({
        "topic": "Product Profitability",
        "finding": (
            f"{highest_product_margin['Product_Name']} has "
            f"a {highest_product_margin_value}% "
            f"profit margin."
        ),
        "recommendation": (
            "Evaluate high-margin products for stronger "
            "promotion and portfolio expansion."
        )
    })


# ============================================================
# 6. CUSTOMER ANALYSIS
# ============================================================

if customers:

    top_customer = customers[0]

    top_customer_sales = top_customer.get(
        "sales",
        0
    )

    opportunities.append({
        "topic": "High-Value Customer",
        "finding": (
            f"{top_customer['Customer_Name']} generated "
            f"${top_customer_sales:,.2f} in sales."
        ),
        "recommendation": (
            "Prioritize retention, repeat purchases "
            "and targeted offers for high-value customers."
        )
    })


# ============================================================
# 7. REGIONAL ANALYSIS
# ============================================================

valid_regions = [
    region
    for region in regions
    if region.get("Region") not in (
        "Unknown",
        None,
        ""
    )
]


if valid_regions:

    lowest_region_margin = min(
        valid_regions,
        key=lambda x: x.get("profit_margin", 0)
    )

    highest_region_margin = max(
        valid_regions,
        key=lambda x: x.get("profit_margin", 0)
    )

    lowest_region_margin_value = lowest_region_margin.get(
        "profit_margin",
        0
    )

    highest_region_margin_value = highest_region_margin.get(
        "profit_margin",
        0
    )

    # --------------------------------------------------------
    # Regional Margin Risk
    # --------------------------------------------------------

    if lowest_region_margin_value < 30:

        risks.append({
            "topic": "Regional Margin Risk",
            "finding": (
                f"{lowest_region_margin['Region']} has the "
                f"lowest regional profit margin at "
                f"{lowest_region_margin_value}%."
            ),
            "recommendation": (
                "Investigate regional pricing, costs, "
                "discounts and sales mix."
            )
        })

    # --------------------------------------------------------
    # Regional Opportunity
    # --------------------------------------------------------

    opportunities.append({
        "topic": "Regional Opportunity",
        "finding": (
            f"{highest_region_margin['Region']} has the "
            f"highest valid regional margin at "
            f"{highest_region_margin_value}%."
        ),
        "recommendation": (
            "Study the regional sales mix and replicate "
            "successful practices where appropriate."
        )
    })


# ============================================================
# 8. OVERALL BUSINESS HEALTH
# ============================================================

profit_margin = overall["profit_margin"]

if profit_margin >= 30:

    overall_status = "Healthy"

else:

    overall_status = "Needs Attention"


# ============================================================
# 9. CREATE RECOMMENDATION LIST
# ============================================================

recommendations = [
    item["recommendation"]
    for item in risks + opportunities
]


# ============================================================
# 10. CREATE DECISION REPORT
# ============================================================

decision_report = {

    "business_health": {

        "status": overall_status,

        "total_sales": overall["total_sales"],

        "total_profit": overall["total_profit"],

        "profit_margin": overall["profit_margin"],

        "total_orders": overall["total_orders"]

    },

    "risks": risks,

    "opportunities": opportunities,

    "recommendations": recommendations

}


# ============================================================
# 11. SAVE DECISION REPORT
# ============================================================

try:

    output_directory = os.path.dirname(OUTPUT_FILE)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            decision_report,
            file,
            indent=4,
            ensure_ascii=False
        )

except OSError as error:

    print("ERROR: Could not save decision report.")
    print(f"Details: {error}")

    raise SystemExit(1)


# ============================================================
# 12. DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("AI-POWERED DECISION ENGINE")
print("=" * 60)

print()
print(f"Business Health : {overall_status}")
print(f"Sales           : ${overall['total_sales']:,.2f}")
print(f"Profit          : ${overall['total_profit']:,.2f}")
print(f"Profit Margin   : {overall['profit_margin']}%")
print(f"Total Orders    : {overall['total_orders']:,}")


# ============================================================
# 13. DISPLAY BUSINESS RISKS
# ============================================================

print()
print("BUSINESS RISKS")
print("-" * 60)

if risks:

    for risk in risks:

        print()
        print(f"- {risk['topic']}")
        print(f"  Finding        : {risk['finding']}")
        print(
            f"  Recommendation : "
            f"{risk['recommendation']}"
        )

else:

    print("No major risks detected.")


# ============================================================
# 14. DISPLAY BUSINESS OPPORTUNITIES
# ============================================================

print()
print("BUSINESS OPPORTUNITIES")
print("-" * 60)

if opportunities:

    for opportunity in opportunities:

        print()
        print(f"- {opportunity['topic']}")
        print(
            f"  Finding        : "
            f"{opportunity['finding']}"
        )
        print(
            f"  Recommendation : "
            f"{opportunity['recommendation']}"
        )

else:

    print("No major opportunities detected.")


# ============================================================
# 15. COMPLETION MESSAGE
# ============================================================

print()
print("=" * 60)
print("Decision report saved successfully.")
print(f"File: {OUTPUT_FILE}")
print("=" * 60)

print()
print("DECISION ENGINE COMPLETED SUCCESSFULLY")