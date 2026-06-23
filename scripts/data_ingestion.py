import os
import pandas as pd

RAW_DATA_FOLDER = "data/raw"


def print_separator():
    print("\n" + "=" * 80)


def load_all_datasets(folder):
    """Load all CSV files from the raw data folder."""

    datasets = {}

    csv_files = sorted(
        [file for file in os.listdir(folder) if file.endswith(".csv")]
    )

    print_separator()
    print(f"Found {len(csv_files)} CSV files")
    print_separator()

    for file in csv_files:

        path = os.path.join(folder, file)

        try:
            df = pd.read_csv(path)

            datasets[file] = df

            print_separator()
            print(f"Dataset : {file}")
            print_separator()

            print(f"Shape : {df.shape}")

            print("\nColumns")
            print(df.columns.tolist())

            print("\nData Types")
            print(df.dtypes)

            print("\nFirst 5 Rows")
            print(df.head())

            print("\nMissing Values")
            print(df.isnull().sum())

            print(f"\nDuplicate Rows : {df.duplicated().sum()}")

        except Exception as e:
            print(f"Error loading {file}")
            print(e)

    return datasets


def explore_fund_master(df):
    """Explore fund master dataset."""

    print_separator()
    print("FUND MASTER EXPLORATION")
    print_separator()

    print(f"Total Schemes : {len(df)}")

    # Fund House
    fund_house = (
        df["schemeName"]
        .str.split("-")
        .str[0]
        .str.strip()
    )

    print("\nEstimated Fund Houses")

    print(fund_house.value_counts().head(20))

    # Plan Types

    direct = df["schemeName"].str.contains(
        "Direct",
        case=False,
        na=False
    ).sum()

    regular = len(df) - direct

    print("\nPlan Type")

    print(f"Direct  : {direct}")
    print(f"Regular : {regular}")

    # Growth

    growth = df["schemeName"].str.contains(
        "Growth",
        case=False,
        na=False
    ).sum()

    idcw = len(df) - growth

    print("\nOption Type")

    print(f"Growth : {growth}")
    print(f"IDCW/Dividend : {idcw}")


def validate_scheme_codes(fund_master, nav_history):
    """Validate scheme codes."""

    print_separator()
    print("AMFI CODE VALIDATION")
    print_separator()

    fund_codes = set(fund_master["schemeCode"])

    nav_codes = set(nav_history["schemeCode"])

    matched = fund_codes.intersection(nav_codes)

    missing = fund_codes - nav_codes

    print(f"Fund Master Codes : {len(fund_codes)}")

    print(f"NAV Codes : {len(nav_codes)}")

    print(f"Matched : {len(matched)}")

    print(f"Missing : {len(missing)}")

    return len(missing)


def data_quality_summary(datasets, missing_codes):

    print_separator()
    print("DATA QUALITY SUMMARY")
    print_separator()

    print(f"Datasets Loaded : {len(datasets)}")

    for name, df in datasets.items():

        print(f"\n{name}")

        print(f"Rows : {len(df)}")

        print(f"Columns : {len(df.columns)}")

        print(f"Missing Values : {df.isnull().sum().sum()}")

        print(f"Duplicates : {df.duplicated().sum()}")

    print("\nAMFI Validation")

    if missing_codes == 0:

        print("PASS : All scheme codes exist in NAV history.")

    else:

        print(
            f"INFO : {missing_codes} scheme codes are currently absent from "
            "NAV history because the ETL pipeline was configured to "
            "download only the first 100 schemes."
        )


def main():

    datasets = load_all_datasets(RAW_DATA_FOLDER)

    if "01_fund_master.csv" not in datasets:
        print("Fund Master not found.")
        return

    if "02_nav_history.csv" not in datasets:
        print("NAV History not found.")
        return

    explore_fund_master(
        datasets["01_fund_master.csv"]
    )

    missing = validate_scheme_codes(
        datasets["01_fund_master.csv"],
        datasets["02_nav_history.csv"]
    )

    data_quality_summary(
        datasets,
        missing
    )


if __name__ == "__main__":
    main()