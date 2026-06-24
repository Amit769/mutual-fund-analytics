import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File Paths
# --------------------------------------------------
RAW_FILE = Path("data/raw/08_investor_transactions.csv")
OUTPUT_FILE = Path("data/processed/investor_transactions.csv")

# Create processed directory if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv(RAW_FILE)

original_rows = len(df)

print(f"Original rows: {original_rows}")

# --------------------------------------------------
# Fix Date Format
# --------------------------------------------------
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

# Remove rows with invalid dates
df = df.dropna(subset=["transaction_date"])

# --------------------------------------------------
# Standardize Transaction Type
# --------------------------------------------------
df["transaction_type"] = (
    df["transaction_type"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Replace common variations
transaction_mapping = {
    "Sip": "SIP",
    "Lumpsum": "Lumpsum",
    "Lumpsum ": "Lumpsum",
    "Redemption": "Redemption"
}

df["transaction_type"] = (
    df["transaction_type"]
    .replace(transaction_mapping)
)

# Keep only valid transaction types
valid_transaction_types = [
    "SIP",
    "Lumpsum",
    "Redemption"
]

invalid_transactions = (
    ~df["transaction_type"]
    .isin(valid_transaction_types)
).sum()

print(f"Invalid transaction types: {invalid_transactions}")

df = df[
    df["transaction_type"]
    .isin(valid_transaction_types)
]

# --------------------------------------------------
# Validate Amount
# --------------------------------------------------
df["amount_inr"] = pd.to_numeric(
    df["amount_inr"],
    errors="coerce"
)

invalid_amounts = (
    (df["amount_inr"] <= 0) |
    (df["amount_inr"].isna())
).sum()

print(f"Invalid amounts: {invalid_amounts}")

df = df[
    df["amount_inr"] > 0
]

# --------------------------------------------------
# Validate KYC Status
# --------------------------------------------------
df["kyc_status"] = (
    df["kyc_status"]
    .astype(str)
    .str.strip()
    .str.title()
)

valid_kyc = [
    "Verified",
    "Pending",
    "Rejected"
]

invalid_kyc = (
    ~df["kyc_status"]
    .isin(valid_kyc)
).sum()

print(f"Invalid KYC values: {invalid_kyc}")

# --------------------------------------------------
# Remove Duplicate Rows
# --------------------------------------------------
duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates}")

df = df.drop_duplicates()

# --------------------------------------------------
# Sort Records
# --------------------------------------------------
df = df.sort_values(
    by=[
        "transaction_date",
        "investor_id"
    ]
).reset_index(drop=True)

# --------------------------------------------------
# Save Cleaned Dataset
# --------------------------------------------------
df.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# Summary
# --------------------------------------------------
print("\n========== Cleaning Summary ==========")
print(f"Original rows           : {original_rows}")
print(f"Duplicate rows          : {duplicates}")
print(f"Invalid transaction type: {invalid_transactions}")
print(f"Invalid amounts         : {invalid_amounts}")
print(f"Invalid KYC values      : {invalid_kyc}")
print(f"Final rows              : {len(df)}")
print(f"Saved file              : {OUTPUT_FILE}")