import pandas as pd
from pathlib import Path

# Load the raw sales data
data_file = Path(__file__).resolve().parent.parent / "01_Data" / "raw_sales_data.csv"
df = pd.read_csv(data_file)

# Show basic information
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())


print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nNegative quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero quantities:")
print((df["Quantity"] == 0).sum())

print("\nUnique regions:")
print(df["Region"].value_counts(dropna=False))

print("\nUnique payment methods:")
print(df["Payment_Method"].value_counts(dropna=False))

print("\nSales validation:")

df["Expected_Sales"] = (
    df["Quantity"]
    * df["Unit_Price"]
    * (1 - df["Discount"].fillna(0))
).round(2)

df["Sales_Difference"] = (
    df["Sales"] - df["Expected_Sales"]
).round(2)

print("Rows with sales mismatch:")
print((df["Sales_Difference"].abs() > 0.01).sum())