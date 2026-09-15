import pandas as pd
from pathlib import Path

# Find project folder
project_dir = Path(__file__).resolve().parent.parent

# Location of cleaned data
clean_file = project_dir / "01_Data" / "clean_sales_data.csv"

# Load cleaned data
df = pd.read_csv(clean_file)

print("=== CLEAN DATA VALIDATION ===")

# 1. Dataset size
print("\nRows:", len(df))
print("Columns:", len(df.columns))

# 2. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 3. Duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# 4. Invalid quantities
print("\nNegative quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero quantities:")
print((df["Quantity"] == 0).sum())

# 5. Date validation
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

print("\nInvalid dates:")
print(df["Order_Date"].isna().sum())

# 6. Sales validation
expected_sales = (
    df["Quantity"]
    * df["Unit_Price"]
    * (1 - df["Discount"])
).round(2)

sales_difference = (
    df["Sales"] - expected_sales
).abs()

print("\nSales mismatches:")
print((sales_difference > 0.01).sum())

# 7. Profit validation
expected_profit = (
    df["Sales"] - df["Cost"]
).round(2)

profit_difference = (
    df["Profit"] - expected_profit
).abs()

print("\nProfit mismatches:")
print((profit_difference > 0.01).sum())

# 8. Region check
print("\nRegions:")
print(df["Region"].value_counts())

# 9. Payment method check
print("\nPayment methods:")
print(df["Payment_Method"].value_counts())

print("\n=== VALIDATION COMPLETE ===")