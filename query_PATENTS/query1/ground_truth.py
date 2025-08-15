import pandas as pd
import json

# Read input datasets
df_pub = pd.read_csv("../ground_truth_dataset/PUBLICATIONS.csv")
df_cpc_def = pd.read_csv("../ground_truth_dataset/CPC_DEFINITION.csv")

# Keep only rows where application_number is not empty
df_pub = df_pub[df_pub["application_number"].notna() & (df_pub["application_number"] != "")]

# For each application_number, keep only the record with the latest filing_date
df_pub = df_pub.sort_values("filing_date", ascending=False).drop_duplicates(subset=["application_number"])

# Extract CPC codes where "first" = True from JSON string
def extract_first_cpcs(cpc_str):
    try:
        cpcs = json.loads(cpc_str)
        return [c["code"] for c in cpcs if c.get("first") is True]
    except:
        return []

df_pub["cpc_list"] = df_pub["cpc"].apply(extract_first_cpcs)

# Join with CPC_DEFINITION to enrich CPC details
df_cpc = df_pub.explode("cpc_list").merge(
    df_cpc_def,
    left_on="cpc_list",
    right_on="symbol",
    how="inner"
)

# Parse CPC parents JSON to get cpc_group
def parse_parents(parents_str):
    try:
        return json.loads(parents_str)
    except:
        return []

df_cpc["parents_list"] = df_cpc["parents"].apply(parse_parents)
df_cpc = df_cpc.explode("parents_list").rename(columns={"parents_list": "cpc_group"})

# Extract filing year from filing_date (YYYYMMDD format)
df_cpc["filing_year"] = (df_cpc["filing_date"] // 10000).astype(int)
df_cpc = df_cpc[df_cpc["filing_year"] > 0]

# Count patents per CPC group per year
yearly_counts = df_cpc.groupby(["cpc_group", "filing_year"]).size().reset_index(name="cnt")
yearly_counts = yearly_counts.sort_values(["cpc_group", "filing_year"])

# Compute Exponential Moving Average (EMA) with smoothing factor alpha
alpha = 0.2
ema_results = []
for group, subdf in yearly_counts.groupby("cpc_group"):
    ema_prev = 0
    for _, row in subdf.iterrows():
        ema = row["cnt"] * alpha + ema_prev * (1 - alpha)
        ema_results.append((group, row["filing_year"], ema))
        ema_prev = ema
ema_df = pd.DataFrame(ema_results, columns=["cpc_group", "filing_year", "ema"])

# For each CPC group, keep the year with the highest EMA (break ties by latest year)
best_years = (
    ema_df.sort_values(["cpc_group", "ema", "filing_year"], ascending=[True, False, False])
    .drop_duplicates(subset=["cpc_group"])
)

# Keep only CPC groups with level = 5
best_years = best_years.merge(df_cpc_def, left_on="cpc_group", right_on="symbol")
best_years = best_years[best_years["level"] == 5]

# Keep only results where the best year is 2022
best_years = best_years[best_years["filing_year"] == 2022]

# Output only the CPC group column, removing duplicates
output = best_years[["cpc_group"]].drop_duplicates()

# Save the final ground truth file
output.to_csv("ground_truth.csv", index=False, encoding="utf-8")

print("✅ Ground truth generated and saved to ground_truth.csv")
print(output.head(10))
