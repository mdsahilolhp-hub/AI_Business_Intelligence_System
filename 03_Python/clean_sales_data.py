import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. File locations
# --------------------------------------------------

project_dir = Path(__file__).resolve().parent.parent

raw_file = project_dir / "01_Data" / "raw_sales_data.csv"
clean_file = project_dir / "01_Data" / "clean_sales_data.csv"


# --------------------------------------------------
# 2. Load raw data
# --------------------------------------------------

df = pd.read_csv(raw_file)

print("Original rows:", len(df))


# --------------------------------------------------
# 3. Remove exact duplicate rows
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates().copy()

print("Duplicate rows removed:", duplicate_count)


# --------------------------------------------------
# 4. Standardize text columns
# --------------------------------------------------

text_columns = [
    "Customer_Name",
    "Product_Name",
    "Category",
    "Region",
    "Payment_Method",
    "Sales_Channel",
    "Customer_Segment"
]

for column in text_columns:
    df[column] = df[column].str.strip()


# Standardize Region
df["Region"] = df["Region"].str.title()


# Standardize Payment Method
df["Payment_Method"] = (
    df["Payment_Method"]
    .str.strip()
    .str.title()
)


# --------------------------------------------------
# 5. Fix missing customer names
# --------------------------------------------------

# A customer can appear in multiple transactions.
# We use the known customer name from another transaction
# when the same Customer_ID has a missing name.

customer_name_map = (
    df.dropna(subset=["Customer_Name"])
    .drop_duplicates("Customer_ID")
    .set_index("Customer_ID")["Customer_Name"]
)

df["Customer_Name"] = (
    df["Customer_Name"]
    .fillna(df["Customer_ID"].map(customer_name_map))
)

# Any remaining missing names become "Unknown Customer"
df["Customer_Name"] = df["Customer_Name"].fillna("Unknown Customer")


# --------------------------------------------------
# 6. Handle missing discounts
# --------------------------------------------------

# Business rule:
# Missing discount = no discount = 0%

df["Discount"] = df["Discount"].fillna(0)


# --------------------------------------------------
# 7. Handle invalid quantities
# --------------------------------------------------

# Negative and zero quantities are invalid for our
# sales transaction dataset.

invalid_quantity = df["Quantity"] <= 0

invalid_quantity_count = invalid_quantity.sum()

df = df.loc[~invalid_quantity].copy()

print("Invalid quantity rows removed:", invalid_quantity_count)


# --------------------------------------------------
# 8. Convert date to proper datetime
# --------------------------------------------------

df["Order_Date"] = pd.to_datetime(df["Order_Date"])


# --------------------------------------------------
# 9. Recalculate Sales
# --------------------------------------------------

df["Sales"] = (
    df["Quantity"]
    * df["Unit_Price"]
    * (1 - df["Discount"])
).round(2)


# --------------------------------------------------
# 10. Recalculate Profit
# --------------------------------------------------

df["Profit"] = (
    df["Sales"] - df["Cost"]
).round(2)


# --------------------------------------------------
# 11. Handle missing Region
# --------------------------------------------------

# Region cannot be reliably inferred from our current
# transaction data, so we use "Unknown".

df["Region"] = df["Region"].fillna("Unknown")


# --------------------------------------------------
# 12. Final validation
# --------------------------------------------------

print("\n--- Final Validation ---")

print("Final rows:", len(df))

print("Final columns:", len(df.columns))

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nRegions:")
print(df["Region"].value_counts())

print("\nPayment methods:")
print(df["Payment_Method"].value_counts())

print("\nQuantity check:")
print("Negative quantities:", (df["Quantity"] < 0).sum())
print("Zero quantities:", (df["Quantity"] == 0).sum())


# --------------------------------------------------
# 13. Save cleaned data
# --------------------------------------------------

df.to_csv(clean_file, index=False)

print("\nCleaned file saved to:")
print(clean_file)