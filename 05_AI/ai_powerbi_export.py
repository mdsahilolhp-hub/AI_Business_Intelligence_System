import json
import csv
import re

# ============================================================
# LOAD GEMINI AI OUTPUT
# ============================================================

input_file = "05_AI/ai_generated_insights.json"
output_file = "05_AI/ai_powerbi_insights.csv"

try:
    with open(input_file, "r", encoding="utf-8") as file:
        ai_data = json.load(file)

except FileNotFoundError:
    print(f"❌ File not found: {input_file}")
    print("Please run ai_insights_generator.py first.")
    exit()


analysis = ai_data.get("analysis", "")


# ============================================================
# EXTRACT AI SECTIONS
# ============================================================

sections = [
    "EXECUTIVE SUMMARY",
    "KEY BUSINESS RISKS",
    "GROWTH OPPORTUNITIES",
    "PRODUCT & PROFITABILITY INSIGHTS",
    "CUSTOMER INSIGHTS",
    "REGIONAL INSIGHTS",
    "ACTIONABLE RECOMMENDATIONS"
]

rows = []

for i, section in enumerate(sections):

    start_marker = f"### {section}"

    if start_marker in analysis:

        start = analysis.index(start_marker) + len(start_marker)

        if i + 1 < len(sections):
            next_marker = f"### {sections[i + 1]}"

            if next_marker in analysis:
                end = analysis.index(next_marker)
                content = analysis[start:end]
            else:
                content = analysis[start:]
        else:
            content = analysis[start:]

        # Clean markdown formatting
        content = re.sub(r"\*\*", "", content)
        content = content.replace("---", "")
        content = content.strip()

        rows.append({
            "Section": section,
            "AI_Insight": content
        })


# ============================================================
# EXPORT FOR POWER BI
# ============================================================

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["Section", "AI_Insight"]
    )

    writer.writeheader()
    writer.writerows(rows)


# ============================================================
# RESULT
# ============================================================

print("\n🤖 AI POWER BI EXPORT")
print("=" * 60)

print(f"✅ Sections exported: {len(rows)}")
print(f"📁 File created: {output_file}")

for row in rows:
    print(f"   • {row['Section']}")

print("=" * 60)
print("✅ POWER BI AI INSIGHTS EXPORT COMPLETED!")