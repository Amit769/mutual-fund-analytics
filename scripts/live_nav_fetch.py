import os
import requests
import pandas as pd

BASE_URL = "https://api.mfapi.in/mf/"

SCHEMES = {
    "HDFC_Top100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_LargeCap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841",
}

SAVE_FOLDER = "data/raw"


def fetch_nav_data(fund_name, scheme_code):
    """Fetch NAV history for a mutual fund scheme and save it as CSV."""

    url = BASE_URL + scheme_code

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        filename = os.path.join(SAVE_FOLDER, f"{fund_name}.csv")
        nav_df.to_csv(filename, index=False)

        print(f"✅ Saved: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {fund_name}: {e}")


def main():

    os.makedirs(SAVE_FOLDER, exist_ok=True)

    print("=" * 60)
    print("Fetching Live Mutual Fund NAV Data")
    print("=" * 60)

    for fund_name, scheme_code in SCHEMES.items():
        fetch_nav_data(fund_name, scheme_code)

    print("\n🎉 All downloads completed.")


if __name__ == "__main__":
    main()
    