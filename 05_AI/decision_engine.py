import json


# ==========================================
# 1. LOAD EXTRACTED BUSINESS DATA
# ==========================================

with open(
    "05_AI/ai_insights_output.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)


overall = data["overall"]
categories = data["category_performance"]
customers = data["top_customers"]
products = data["top_products"]
regions = data["regional_performance"]


# ==========================================
# 2. INITIALIZE DECISION INSIGHTS
# ==========================================

risks = []
opportunities = []
recommendations = []


# ==========================================
# 3. CATEGORY ANALYSIS
# ==========================================

lowest_margin_category = min(
    categories,
    key=lambda x: x["profit_margin"]
)

highest_margin_category = max(
    categories,
    key=lambda x: x["profit_margin"]
)


if lowest_margin_category["profit_margin"] < 25:
    risks.append({
        "topic": "Margin Risk",
        "finding": (
            f"{lowest_margin_category['Category']} has the "
            f"lowest profit margin at "
            f"{lowest_margin_category['profit_margin']}%."
        ),
        "recommendation": (
            "Review pricing, discounts, supplier costs "
            "and product-level profitability."
        )
    })


opportunities.append({
    "topic": "High-Margin Opportunity",
    "finding": (
        f"{highest_margin_category['Category']} has the "
        f"highest profit margin at "
        f"{highest_margin_category['profit_margin']}%."
    ),
    "recommendation": (
        "Prioritize high-margin products and expand "
        "profitable offerings."
    )
})


# ==========================================
# 4. PRODUCT ANALYSIS
# ==========================================

if products:

    top_product = products[0]

    highest_product_margin = max(
        products,
        key=lambda x: x["profit_margin"]
    )

    opportunities.append({
        "topic": "Top Product",
        "finding": (
            f"{top_product['Product_Name']} generates the "
            f"highest sales among the top products at "
            f"₹{top_product['sales']:,.2f}."
        ),
        "recommendation": (
            "Maintain availability and prioritize this "
            "product in sales and retention strategies."
        )
    })

    opportunities.append({
        "topic": "Product Profitability",
        "finding": (
            f"{highest_product_margin['Product_Name']} has "
            f"a {highest_product_margin['profit_margin']}% "
            f"profit margin."
        ),
        "recommendation": (
            "Evaluate high-margin products for stronger "
            "promotion and portfolio expansion."
        )
    })


# ==========================================
# 5. CUSTOMER ANALYSIS
# ==========================================

if customers:

    top_customer = customers[0]

    opportunities.append({
        "topic": "High-Value Customer",
        "finding": (
            f"{top_customer['Customer_Name']} generated "
            f"₹{top_customer['sales']:,.2f} in sales."
        ),
        "recommendation": (
            "Prioritize retention, repeat purchases "
            "and targeted offers for high-value customers."
        )
    })


# ==========================================
# 6. REGIONAL ANALYSIS
# ==========================================

valid_regions = [
    region for region in regions
    if region["Region"] not in ("Unknown", None, "")
]

if valid_regions:

    lowest_region_margin = min(
        valid_regions,
        key=lambda x: x["profit_margin"]
    )

    highest_region_margin = max(
        valid_regions,
        key=lambda x: x["profit_margin"]
    )

    if lowest_region_margin["profit_margin"] < 30:

        risks.append({
            "topic": "Regional Margin Risk",
            "finding": (
                f"{lowest_region_margin['Region']} has the "
                f"lowest regional profit margin at "
                f"{lowest_region_margin['profit_margin']}%."
            ),
            "recommendation": (
                "Investigate regional pricing, costs, "
                "discounts and sales mix."
            )
        })

    opportunities.append({
        "topic": "Regional Opportunity",
        "finding": (
            f"{highest_region_margin['Region']} has the "
            f"highest valid regional margin at "
            f"{highest_region_margin['profit_margin']}%."
        ),
        "recommendation": (
            "Study the regional sales mix and replicate "
            "successful practices where appropriate."
        )
    })


# ==========================================
# 7. OVERALL BUSINESS HEALTH
# ==========================================

if overall["profit_margin"] >= 30:

    overall_status = "Healthy"

else:

    overall_status = "Needs Attention"


# ==========================================
# 8. CREATE DECISION REPORT
# ==========================================

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

    "recommendations": [
        item["recommendation"]
        for item in risks + opportunities
    ]
}


# ==========================================
# 9. SAVE DECISION REPORT
# ==========================================

with open(
    "05_AI/ai_decision_report.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        decision_report,
        file,
        indent=4,
        ensure_ascii=False
    )


# ==========================================
# 10. DISPLAY RESULTS
# ==========================================

print("\n" + "=" * 60)
print("🤖 AI-POWERED DECISION ENGINE")
print("=" * 60)

print(
    f"\nBusiness Health: {overall_status}"
)

print(
    f"Sales: ₹{overall['total_sales']:,.2f}"
)

print(
    f"Profit: ₹{overall['total_profit']:,.2f}"
)

print(
    f"Margin: {overall['profit_margin']}%"
)


print("\n🔴 BUSINESS RISKS")
print("-" * 60)

if risks:

    for risk in risks:

        print(f"\n• {risk['topic']}")
        print(f"  Finding: {risk['finding']}")
        print(f"  Recommendation: {risk['recommendation']}")

else:

    print("No major risks detected.")


print("\n🟢 BUSINESS OPPORTUNITIES")
print("-" * 60)

for opportunity in opportunities:

    print(f"\n• {opportunity['topic']}")
    print(f"  Finding: {opportunity['finding']}")
    print(
        f"  Recommendation: "
        f"{opportunity['recommendation']}"
    )


print("\n" + "=" * 60)
print("📁 Decision report saved:")
print("05_AI/ai_decision_report.json")
print("=" * 60)

print("\n✅ DECISION ENGINE COMPLETED!")