import subprocess
from datetime import datetime

print("=" * 60)
print("AI BUSINESS INTELLIGENCE AUTOMATION PIPELINE")
print("=" * 60)

steps = [
    ("Data Quality Check", "python 03_Python/data_quality_check.py"),
    ("Data Cleaning", "python 03_Python/clean_sales_data.py"),
    ("Data Validation", "python 03_Python/validate_clean_data.py"),
    ("Business Analysis", "python 05_AI/ai_business_analysis.py"),
    ("Decision Engine", "python 05_AI/decision_engine.py"),
    ("Gemini AI Insights", "python 05_AI/ai_insights_generator.py"),
    ("Power BI Export", "python 05_AI/ai_powerbi_export.py"),
]

start_time = datetime.now()

for name, command in steps:
    print(f"\n▶ Running: {name}")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✅ {name} completed successfully")
    else:
        print(f"❌ {name} failed")
        print(result.stderr)
        break

else:
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 60)
    print("✅ AUTOMATION PIPELINE COMPLETED SUCCESSFULLY")
    print(f"⏱ Duration: {duration}")
    print("=" * 60)