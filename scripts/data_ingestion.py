import os
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

DATA_FOLDER = "data/raw"


def print_line():
    """Print a separator line."""
    print("=" * 90)


# ==========================================================
# Load all CSV datasets
# ==========================================================

def load_datasets(folder):
    """
    Load all CSV files from the specified folder.
    """

    datasets = {}

    csv_files = sorted(
        [file for file in os.listdir(folder) if file.endswith(".csv")]
    )

    print_line()
    print(f"Found {len(csv_files)} CSV files")
    print_line()

    for file in csv_files:

        path = os.path.join(folder, file)

        try:
            df = pd.read_csv(path)

            datasets[file] = df

            print(f"\n📁 Dataset : {file}")
            print("-" * 90)

            print(f"Shape : {df.shape}")

            print("\nColumns:")
            print(df.columns.tolist())

            print("\nData Types:")
            print(df.dtypes)

            print("\nMissing Values:")
            print(df.isnull().sum())

            print(f"\nDuplicate Rows : {df.duplicated().sum()}")

            print("\nFirst 5 Rows:")
            print(df.head())

            print("\n")

        except Exception as e:

            print(f"❌ Error loading {file}")
            print(e)

    return datasets


# ==========================================================
# Dataset Summary
# ==========================================================

def dataset_summary(datasets):
    """
    Print summary of all datasets.
    """

    print_line()
    print("PROJECT DATASET SUMMARY")
    print_line()

    summary = []

    for name, df in datasets.items():

        summary.append({

            "Dataset": name,
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum())

        })

    summary_df = pd.DataFrame(summary)

    print(summary_df)


# ==========================================================
# Explore Fund Master
# ==========================================================

def explore_fund_master():
    """
    Display important statistics from the fund master dataset.
    """

    fund_master = pd.read_csv("data/raw/01_fund_master.csv")

    print_line()
    print("FUND MASTER EXPLORATION")
    print_line()

    print(f"Total Schemes : {len(fund_master)}")

    print("\nUnique Fund Houses:")
    print(fund_master["fund_house"].unique())

    print(f"\nTotal Fund Houses : {fund_master['fund_house'].nunique()}")

    print("\nCategories:")
    print(fund_master["category"].unique())

    print(f"\nTotal Categories : {fund_master['category'].nunique()}")

    print("\nSub Categories:")
    print(fund_master["sub_category"].unique())

    print(f"\nTotal Sub Categories : {fund_master['sub_category'].nunique()}")

    print("\nRisk Categories:")
    print(fund_master["risk_category"].unique())

    print(f"\nTotal Risk Categories : {fund_master['risk_category'].nunique()}")


# ==========================================================
# Validate AMFI Codes
# ==========================================================

def validate_amfi_codes():
    """
    Validate that every AMFI code in fund_master
    exists in nav_history.
    """

    fund_master = pd.read_csv("data/raw/01_fund_master.csv")
    nav_history = pd.read_csv("data/raw/02_nav_history.csv")

    fund_codes = set(fund_master["amfi_code"])
    nav_codes = set(nav_history["amfi_code"])

    matched = fund_codes.intersection(nav_codes)
    missing = fund_codes - nav_codes

    print_line()
    print("AMFI CODE VALIDATION")
    print_line()

    print(f"Total Fund Master Codes : {len(fund_codes)}")
    print(f"Total NAV History Codes : {len(nav_codes)}")
    print(f"Matching Codes          : {len(matched)}")
    print(f"Missing Codes           : {len(missing)}")

    if len(missing) == 0:
        print("\n✅ PASS: Every AMFI code in fund_master exists in nav_history.")
    else:
        print("\n⚠️ WARNING: Some AMFI codes are missing from nav_history.")
        print("\nMissing Codes:")
        print(sorted(missing))


# ==========================================================
# Main Function
# ==========================================================

def main():

    datasets = load_datasets(DATA_FOLDER)

    dataset_summary(datasets)

    explore_fund_master()

    validate_amfi_codes()

    print_line()
    print("✅ Data ingestion completed successfully.")
    print_line()


if __name__ == "__main__":
    main()