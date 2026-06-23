import os
import pandas as pd

# Path containing all raw datasets
DATA_FOLDER = "data/raw"


def print_line():
    print("=" * 90)


def load_datasets(folder):
    """
    Load all CSV files from the given folder.
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

            print(f"\n📁 Dataset: {file}")
            print("-" * 90)

            print(f"Shape: {df.shape}")

            print("\nColumns:")
            print(df.columns.tolist())

            print("\nData Types:")
            print(df.dtypes)

            print("\nMissing Values:")
            print(df.isnull().sum())

            print(f"\nDuplicate Rows: {df.duplicated().sum()}")

            print("\nFirst 5 Rows:")
            print(df.head())

            print("\n")

        except Exception as e:

            print(f"❌ Error loading {file}")
            print(e)

    return datasets


def dataset_summary(datasets):

    print_line()
    print("PROJECT DATASET SUMMARY")
    print_line()

    summary = []

    for name, df in datasets.items():

        summary.append({

            "Dataset": name,
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Missing Values": df.isnull().sum().sum(),
            "Duplicate Rows": df.duplicated().sum()

        })

    summary_df = pd.DataFrame(summary)

    print(summary_df)


def main():

    datasets = load_datasets(DATA_FOLDER)

    dataset_summary(datasets)

    print_line()
    print("✅ Data ingestion completed successfully.")
    print_line()


if __name__ == "__main__":
    main()