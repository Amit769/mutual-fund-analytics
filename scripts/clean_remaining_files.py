import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

files = [
    "01_fund_master.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in files:

    print(f"\nCleaning {file}...")

    df = pd.read_csv(RAW_DIR / file)

    original_rows = len(df)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Trim spaces from text columns
    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].str.strip()

    output_name = file.replace("01_", "") \
                      .replace("03_", "") \
                      .replace("04_", "") \
                      .replace("05_", "") \
                      .replace("06_", "") \
                      .replace("09_", "") \
                      .replace("10_", "")

    df.to_csv(PROCESSED_DIR / output_name, index=False)

    print(f"Rows before : {original_rows}")
    print(f"Duplicates  : {duplicates}")
    print(f"Rows after  : {len(df)}")

print("\nAll remaining datasets cleaned successfully!")