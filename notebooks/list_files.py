from pathlib import Path

processed_path = Path("data/processed")

files = list(processed_path.glob("*.csv"))

for f in files:
    print(f.name)