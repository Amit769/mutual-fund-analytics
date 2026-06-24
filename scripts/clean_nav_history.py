import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File Paths
# --------------------------------------------------
RAW_FILE = Path("data/raw/02_nav_history.csv")
OUTPUT_FILE = Path("data/processed/nav_history.csv")

# Create processed directory if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv(RAW_FILE)

print(f"Original rows: {len(df)}")

# --------------------------------------------------
# Parse Date Column
# --------------------------------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Remove rows with invalid dates
df = df.dropna(subset=["date"])

# --------------------------------------------------
# Remove Duplicate Records
# --------------------------------------------------
duplicates = df.duplicated().sum()
print(f"Duplicate rows found: {duplicates}")

df = df.drop_duplicates()

# --------------------------------------------------
# Sort by Fund and Date
# --------------------------------------------------
df = df.sort_values(
    by=["amfi_code", "date"]
).reset_index(drop=True)

# --------------------------------------------------
# Forward Fill Missing NAV
# (within each fund only)
# --------------------------------------------------
df["nav"] = (
    df.groupby("amfi_code")["nav"]
      .ffill()
)

# --------------------------------------------------
# Validate NAV Values
# --------------------------------------------------
invalid_nav = (df["nav"] <= 0).sum()

print(f"Invalid NAV values: {invalid_nav}")

df = df[df["nav"] > 0]

# --------------------------------------------------
# Save Cleaned Dataset
# --------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False)

# --------------------------------------------------
# Summary
# --------------------------------------------------
print("\nCleaning Completed Successfully!")

print(f"Final rows : {len(df)}")
print(f"Saved file : {OUTPUT_FILE}")