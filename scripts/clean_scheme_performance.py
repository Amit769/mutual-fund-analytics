import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File Paths
# --------------------------------------------------
RAW_FILE = Path("data/raw/07_scheme_performance.csv")   # Change if your filename is different
OUTPUT_FILE = Path("data/processed/scheme_performance.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv(RAW_FILE)

original_rows = len(df)

print(f"Original rows: {original_rows}")

# --------------------------------------------------
# Columns that must be numeric
# --------------------------------------------------
numeric_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct"
]

# Convert all numeric columns
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Count rows with any missing numeric values
invalid_numeric = df[numeric_columns].isna().any(axis=1).sum()

print(f"Rows with invalid numeric values: {invalid_numeric}")

# Remove rows containing invalid numeric values
df = df.dropna(subset=numeric_columns)

# --------------------------------------------------
# Validate Expense Ratio
# Allowed Range: 0.1% to 2.5%
# --------------------------------------------------
expense_anomalies = (
    (df["expense_ratio_pct"] < 0.1) |
    (df["expense_ratio_pct"] > 2.5)
).sum()

print(f"Expense ratio anomalies: {expense_anomalies}")

# Remove invalid expense ratios
df = df[
    (df["expense_ratio_pct"] >= 0.1) &
    (df["expense_ratio_pct"] <= 2.5)
]

# --------------------------------------------------
# Flag Return Anomalies
# (Outside -100% to +200%)
# --------------------------------------------------
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

anomaly_mask = (
    (df[return_columns] < -100) |
    (df[return_columns] > 200)
).any(axis=1)

return_anomalies = anomaly_mask.sum()

print(f"Return anomalies: {return_anomalies}")

# Add anomaly flag column
df["return_anomaly"] = anomaly_mask

# --------------------------------------------------
# Remove Duplicate Rows
# --------------------------------------------------
duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates}")

df = df.drop_duplicates()

# --------------------------------------------------
# Sort Dataset
# --------------------------------------------------
df = df.sort_values(
    by=["fund_house", "scheme_name"]
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
print(f"Original rows              : {original_rows}")
print(f"Invalid numeric rows       : {invalid_numeric}")
print(f"Expense ratio anomalies    : {expense_anomalies}")
print(f"Return anomalies flagged   : {return_anomalies}")
print(f"Duplicate rows             : {duplicates}")
print(f"Final rows                 : {len(df)}")
print(f"Saved file                 : {OUTPUT_FILE}")