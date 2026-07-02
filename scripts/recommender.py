import pandas as pd

# Load datasets
funds_df = pd.read_csv("data/processed/fund_master.csv")

sharpe_df = pd.read_csv("outputs/reports/sharpe_ratio.csv")

# Merge datasets
recommend_df = funds_df.merge(
    sharpe_df[["amfi_code", "sharpe_ratio"]],
    on="amfi_code",
    how="inner"
)

print("\nAvailable Risk Categories:")
print(sorted(recommend_df["risk_category"].dropna().unique()))

# User input
risk = input("\nEnter Risk Appetite (Low / Moderate / High): ").strip().lower()

# Risk mapping
risk_mapping = {
    "low": ["Low"],
    "moderate": ["Moderate", "Moderately High"],
    "high": ["High", "Very High"]
}

if risk not in risk_mapping:
    print("\nInvalid risk appetite!")
    exit()

# Filter recommendations
recommendations = recommend_df[
    recommend_df["risk_category"].isin(risk_mapping[risk])
]

# Top 3 by Sharpe Ratio
recommendations = (
    recommendations
    .sort_values("sharpe_ratio", ascending=False)
    .head(3)
)

print("\n========== TOP 3 RECOMMENDED FUNDS ==========\n")

print(
    recommendations[
        [
            "scheme_name",
            "risk_category",
            "sharpe_ratio"
        ]
    ].to_string(index=False)
)