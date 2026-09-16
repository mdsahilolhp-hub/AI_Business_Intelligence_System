import json
import os
import requests
from dotenv import load_dotenv


# ============================================================
# AI BUSINESS INSIGHTS GENERATOR
# ============================================================

ENV_FILE = "05_AI/.env"
INPUT_FILE = "05_AI/ai_decision_report.json"
OUTPUT_FILE = "05_AI/ai_generated_insights.json"

MODEL_NAME = "gemini-3.6-flash"

load_dotenv(ENV_FILE)


# ============================================================
# 1. LOAD GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in 05_AI/.env")
    raise SystemExit(1)

GEMINI_API_KEY = GEMINI_API_KEY.strip()

if len(GEMINI_API_KEY) < 20:
    print("ERROR: GEMINI_API_KEY appears to be invalid or incomplete.")
    raise SystemExit(1)


# ============================================================
# 2. LOAD BUSINESS DECISION DATA
# ============================================================

try:

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        decision_data = json.load(file)

except FileNotFoundError:

    print(f"ERROR: File not found: {INPUT_FILE}")
    print("Please run decision_engine.py first.")
    raise SystemExit(1)

except json.JSONDecodeError as error:

    print(f"ERROR: Invalid JSON in {INPUT_FILE}")
    print(f"Details: {error}")
    raise SystemExit(1)


# ============================================================
# 3. BUSINESS ANALYSIS PROMPT
# ============================================================

business_data = json.dumps(
    decision_data,
    indent=2,
    ensure_ascii=False
)


prompt = f"""
You are a senior Business Intelligence and Decision Support Analyst.

Analyze the following business intelligence decision report.

BUSINESS DATA:
{business_data}

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
# 4. GEMINI API REQUEST
# ============================================================

print()
print("Sending business data to Gemini...")
print("=" * 60)

API_URL = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL_NAME}:generateContent"
)

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": GEMINI_API_KEY
}

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}


try:

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

except requests.RequestException as error:

    print()
    print("ERROR: Could not connect to Gemini API.")
    print("-" * 60)
    print(f"Details: {error}")
    raise SystemExit(1)


# ============================================================
# 5. HANDLE GEMINI API RESPONSE
# ============================================================

if response.status_code != 200:

    print()
    print("ERROR: Gemini API request failed.")
    print("-" * 60)
    print(f"HTTP Status: {response.status_code}")

    try:

        error_data = response.json()

        error_message = (
            error_data
            .get("error", {})
            .get("message", "Unknown API error")
        )

        print(f"Message: {error_message}")

    except ValueError:

        print("Response:")
        print(response.text[:1000])

    if response.status_code == 401:

        print()
        print(
            "Authentication failed. "
            "Check GEMINI_API_KEY in 05_AI/.env."
        )

    elif response.status_code == 403:

        print()
        print(
            "Access denied. Check API key permissions "
            "and Gemini API availability."
        )

    elif response.status_code == 404:

        print()
        print(
            f"Model '{MODEL_NAME}' was not found or is not "
            "available for this API key."
        )

    raise SystemExit(1)


# ============================================================
# 6. EXTRACT GENERATED TEXT
# ============================================================

try:

    response_data = response.json()

    candidates = response_data.get(
        "candidates",
        []
    )

    if not candidates:

        print()
        print("ERROR: Gemini returned no candidates.")
        print(response_data)
        raise SystemExit(1)

    parts = (
        candidates[0]
        .get("content", {})
        .get("parts", [])
    )

    text_parts = [
        part.get("text", "")
        for part in parts
        if part.get("text")
    ]

    ai_analysis = "\n".join(text_parts).strip()

    if not ai_analysis:

        print()
        print("ERROR: Gemini returned an empty response.")
        raise SystemExit(1)

except (ValueError, TypeError, KeyError) as error:

    print()
    print("ERROR: Could not parse Gemini response.")
    print(f"Details: {error}")
    raise SystemExit(1)


# ============================================================
# 7. SAVE AI GENERATED INSIGHTS
# ============================================================

output = {
    "source": "AI Business Intelligence Decision System",
    "model": MODEL_NAME,
    "analysis": ai_analysis
}


try:

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

except OSError as error:

    print()
    print("ERROR: Could not save AI insights.")
    print(f"Details: {error}")
    raise SystemExit(1)


# ============================================================
# 8. DISPLAY RESULT
# ============================================================

print()
print("AI EXECUTIVE ANALYSIS")
print("=" * 60)

print(ai_analysis)

print()
print("=" * 60)
print("AI insights saved successfully.")
print(f"File: {OUTPUT_FILE}")
print("=" * 60)

print()
print("GEMINI AI ANALYSIS COMPLETED SUCCESSFULLY")