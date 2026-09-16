import json
import csv
import re
import os


# ============================================================
# AI POWER BI INSIGHTS EXPORT
# ============================================================

INPUT_FILE = "05_AI/ai_generated_insights.json"
OUTPUT_FILE = "05_AI/ai_powerbi_insights.csv"


# ============================================================
# 1. LOAD GEMINI AI OUTPUT
# ============================================================

try:

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ai_data = json.load(file)

except FileNotFoundError:

    print(f"ERROR: File not found: {INPUT_FILE}")
    print("Please run ai_insights_generator.py first.")
    raise SystemExit(1)

except json.JSONDecodeError as error:

    print(f"ERROR: Invalid JSON file: {INPUT_FILE}")
    print(f"Details: {error}")
    raise SystemExit(1)


analysis = ai_data.get("analysis", "")


if not isinstance(analysis, str) or not analysis.strip():

    print("ERROR: AI analysis is empty.")
    raise SystemExit(1)


# ============================================================
# 2. DEFINE EXPECTED AI SECTIONS
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


# ============================================================
# 3. EXTRACT AI SECTIONS
# ============================================================

rows = []


for i, section in enumerate(sections):

    start_marker = f"### {section}"

    if start_marker not in analysis:
        continue

    start = (
        analysis.index(start_marker)
        + len(start_marker)
    )

    if i + 1 < len(sections):

        next_marker = f"### {sections[i + 1]}"

        if next_marker in analysis:

            end = analysis.index(next_marker)

            content = analysis[start:end]

        else:

            content = analysis[start:]

    else:

        content = analysis[start:]


    # --------------------------------------------------------
    # Clean Markdown formatting
    # --------------------------------------------------------

    content = re.sub(
        r"\*\*",
        "",
        content
    )

    content = re.sub(
        r"^\s*---+\s*$",
        "",
        content,
        flags=re.MULTILINE
    )

    content = content.strip()


    if content:

        rows.append({
            "Section": section,
            "AI_Insight": content
        })


# ============================================================
# 4. VALIDATE EXTRACTED SECTIONS
# ============================================================

if not rows:

    print("ERROR: No AI sections were extracted.")
    print("Please check the structure of ai_generated_insights.json.")
    raise SystemExit(1)


# ============================================================
# 5. CREATE OUTPUT DIRECTORY
# ============================================================

output_directory = os.path.dirname(OUTPUT_FILE)

if output_directory:

    os.makedirs(
        output_directory,
        exist_ok=True
    )


# ============================================================
# 6. EXPORT FOR POWER BI
# ============================================================

try:

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Section",
                "AI_Insight"
            ]
        )

        writer.writeheader()

        writer.writerows(rows)

except OSError as error:

    print("ERROR: Could not create Power BI CSV.")
    print(f"Details: {error}")
    raise SystemExit(1)


# ============================================================
# 7. DISPLAY EXPORT RESULT
# ============================================================

print()
print("=" * 60)
print("AI POWER BI EXPORT")
print("=" * 60)

print()
print(f"Sections exported: {len(rows)}")
print(f"File created: {OUTPUT_FILE}")

print()

for row in rows:

    print(f"- {row['Section']}")


print()
print("=" * 60)
print("POWER BI AI INSIGHTS EXPORT COMPLETED SUCCESSFULLY")
print("=" * 60)