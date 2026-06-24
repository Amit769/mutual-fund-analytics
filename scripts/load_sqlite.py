import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# --------------------------------------------------
# Paths
# --------------------------------------------------
PROCESSED_DIR = Path("data/processed")
DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "bluestock_mf.db"

# --------------------------------------------------
# SQLite Connection
# --------------------------------------------------
engine = create_engine(f"sqlite:///{DB_PATH}")

print("Connected to SQLite database.\n")

# --------------------------------------------------
# Files to Load
# --------------------------------------------------
files = {
    "fund_master": "fund_master.csv",
    "nav_history": "nav_history.csv",
    "aum_by_fund_house": "aum_by_fund_house.csv",
    "monthly_sip_inflows": "monthly_sip_inflows.csv",
    "category_inflows": "category_inflows.csv",
    "industry_folio_count": "industry_folio_count.csv",
    "scheme_performance": "scheme_performance.csv",
    "investor_transactions": "investor_transactions.csv",
    "portfolio_holdings": "portfolio_holdings.csv",
    "benchmark_indices": "benchmark_indices.csv"
}

# --------------------------------------------------
# Load Each Dataset
# --------------------------------------------------
print("Loading datasets into SQLite...\n")

for table_name, file_name in files.items():

    file_path = PROCESSED_DIR / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f"{table_name:<30} {len(df)} rows loaded")

print("\nAll datasets loaded successfully!")

# --------------------------------------------------
# Verify Row Counts
# --------------------------------------------------
print("\n========== Row Count Verification ==========\n")

for table_name, file_name in files.items():

    csv_rows = len(pd.read_csv(PROCESSED_DIR / file_name))

    db_rows = pd.read_sql(
        f"SELECT COUNT(*) AS count FROM {table_name}",
        engine
    ).iloc[0]["count"]

    status = "PASS" if csv_rows == db_rows else "FAIL"

    print(
        f"{table_name:<30} "
        f"CSV={csv_rows:<8} "
        f"DB={db_rows:<8} "
        f"{status}"
    )

print("\nDatabase loading completed successfully.")