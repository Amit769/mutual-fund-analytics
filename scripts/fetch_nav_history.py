import os
import time
import requests
import pandas as pd

# ---------------- CONFIG ---------------- #
INPUT_FILE = "data/raw/01_fund_master.csv"
OUTPUT_FILE = "data/raw/02_nav_history.csv"
FAILED_FILE = "reports/failed_scheme_codes.txt"

BASE_URL = "https://api.mfapi.in/mf/"

# Number of schemes to download
# Change to None to download all schemes
MAX_SCHEMES = 100

# Save progress after every N schemes
SAVE_INTERVAL = 25

# Delay between API calls (seconds)
REQUEST_DELAY = 0.25
# ---------------------------------------- #


def fetch_nav(scheme_code):
    """Fetch NAV history for one scheme."""

    try:
        response = requests.get(
            BASE_URL + str(scheme_code),
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if "data" not in data:
            return None

        df = pd.DataFrame(data["data"])
        df["schemeCode"] = scheme_code

        return df

    except Exception as e:
        print(f"❌ {scheme_code}: {e}")

        with open(FAILED_FILE, "a") as f:
            f.write(str(scheme_code) + "\n")

        return None


def load_existing_codes():
    """Read already downloaded scheme codes."""

    if not os.path.exists(OUTPUT_FILE):
        return set()

    df = pd.read_csv(OUTPUT_FILE)

    return set(df["schemeCode"].unique())


def save_data(dataframes):
    """Append downloaded NAV data to CSV."""

    if len(dataframes) == 0:
        return

    final_df = pd.concat(dataframes, ignore_index=True)

    write_header = not os.path.exists(OUTPUT_FILE)

    final_df.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=write_header,
        index=False
    )


def main():

    os.makedirs("reports", exist_ok=True)

    schemes = pd.read_csv(INPUT_FILE)

    if MAX_SCHEMES is not None:
        schemes = schemes.head(MAX_SCHEMES)

    downloaded = load_existing_codes()

    print("=" * 60)
    print(f"Total schemes to process : {len(schemes)}")
    print(f"Already downloaded       : {len(downloaded)}")
    print("=" * 60)

    batch = []
    count = 0

    for _, row in schemes.iterrows():

        scheme = row["schemeCode"]

        if scheme in downloaded:
            continue

        print(f"Fetching {scheme}")

        nav = fetch_nav(scheme)

        if nav is not None:
            batch.append(nav)

        count += 1

        if count % SAVE_INTERVAL == 0:

            save_data(batch)

            batch = []

            print(f"💾 Saved after {count} schemes")

        time.sleep(REQUEST_DELAY)

    save_data(batch)

    print("\n✅ NAV download completed!")


if __name__ == "__main__":
    main()