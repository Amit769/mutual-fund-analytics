import pandas as pd
import requests
import os

URL = "https://api.mfapi.in/mf"

SAVE_PATH = "data/raw/01_fund_master.csv"


def fetch_fund_master():

    print("Downloading Fund Master...")

    response = requests.get(URL)

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data)

    os.makedirs("data/raw", exist_ok=True)

    df.to_csv(SAVE_PATH, index=False)

    print(f"Saved {len(df)} schemes")

    print(df.head())


if __name__ == "__main__":
    fetch_fund_master()