import json
import os
from dotenv import load_dotenv
from google import genai
load_dotenv("05_AI/.env")
# ============================================================
# GOOGLE GEMINI API CONFIGURATION
# ============================================================

# Paste your Google Gemini API key here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Gemini model
MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# LOAD BUSINESS DECISION DATA
# ============================================================

input_file = "05_AI/ai_decision_report.json"

try:
    with open(input_file, "r", encoding="utf-8") as file:
        decision_data = json.load(file)

except FileNotFoundError:
    print(f"❌ File not found: {input_file}")
    print("Please run decision_engine.py first.")
    exit()


# ============================================================
# BUSINESS ANALYSIS PROMPT
# ============================================================

prompt = f"""
You are a senior Business Intelligence and Decision Support Analyst.

Analyze the following business intelligence decision report.

BUSINESS DATA:
{json.dumps(decision_data, indent=2, ensure_ascii=False)}

Your task is to produce a professional executive-level business analysis.

Identify:

1. Overall business performance
2. Major business risks
3. Major growth opportunities
4. Product profitability insights
5. Customer insights
6. Regional performance insights
7. Specific actionable recommendations

IMPORTANT RULES:

- Use ONLY the provided business data.
- Do not invent numbers.
- Mention important percentages and values.
- Clearly distinguish facts from recommendations.
- Focus on business impact.
- Keep recommendations practical and actionable.
- Write in professional business English.
- Keep the response concise but useful for an executive dashboard.

Structure your response using these sections:

EXECUTIVE SUMMARY

KEY BUSINESS RISKS

GROWTH OPPORTUNITIES

PRODUCT & PROFITABILITY INSIGHTS

CUSTOMER INSIGHTS

REGIONAL INSIGHTS

ACTIONABLE RECOMMENDATIONS
"""


# ============================================================
# SEND DATA TO GEMINI
# ============================================================

print("\n🤖 Sending business data to Gemini...")
print("=" * 60)

try:

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    ai_analysis = response.text

except Exception as error:

    print("\n❌ Gemini API Error")
    print("-" * 60)
    print(error)
    exit()


# ============================================================
# SAVE AI GENERATED INSIGHTS
# ============================================================

output = {
    "source": "AI Business Intelligence Decision System",
    "model": MODEL_NAME,
    "analysis": ai_analysis
}

output_file = "05_AI/ai_generated_insights.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        output,
        file,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n🧠 AI EXECUTIVE ANALYSIS")
print("=" * 60)

print(ai_analysis)

print("\n" + "=" * 60)
print("📁 AI insights saved successfully!")
print(f"📄 File: {output_file}")
print("=" * 60)

print("\n✅ GEMINI AI ANALYSIS COMPLETED!")