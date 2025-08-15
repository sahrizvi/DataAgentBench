import pandas as pd
import json

# Read input datasets
df_pub = pd.read_csv("../ground_truth_dataset/PUBLICATIONS.csv")
df_cpc_def = pd.read_csv("../ground_truth_dataset/CPC_DEFINITION.csv")

# -------------------------------
# 1. Filtering criteria
# -------------------------------
# Keep only rows where application_number is not empty
df_pub = df_pub[df_pub["application_number"].notna() & (df_pub["application_number"] != "")]

# Keep only patents from Germany
df_pub = df_pub[df_pub["country_code"] == "DE"]

# Keep only patents granted in the second half of 2019
df_pub = df_pub[df_pub["grant_date"].between(20190701, 20191231)]

# For each application_number, keep the record with the latest filing_date
df_pub = df_pub.sort_values("filing_date", ascending=False).drop_duplicates(subset=["application_number"])

# -------------------------------
# 2. Extract cpc_list where "first" = True
# -------------------------------
def extract_first_cpcs(cpc_str):
    try:
        cpcs = json.loads(cpc_str)
        return [c["code"] for c in cpcs if c.get("first") is True]
    except:
        return []

df_pub["cpc_list"] = df_pub["cpc"].apply(extract_first_cpcs)

# -------------------------------
# 3. Join with CPC_DEFINITION to get parent groups
# -------------------------------
df_cpc = df_pub.explode("cpc_list").merge(
    df_cpc_def,
    left_on="cpc_list",
    right_on="symbol",
    how="inner"
)

# Parse parents JSON
def parse_parents(parents_str):
    try:
        return json.loads(parents_str)
    except:
        return []

# Expand parent list into separate rows
df_cpc["parents_list"] = df_cpc["parents"].apply(parse_parents)
df_cpc = df_cpc.explode("parents_list").rename(columns={"parents_list": "cpc_group"})

# -------------------------------
# 4. Extract filing year
# -------------------------------
df_cpc["filing_year"] = (df_cpc["filing_date"] // 10000).astype(int)
df_cpc = df_cpc[df_cpc["filing_year"] > 0]

# -------------------------------
# 5. Calculate yearly counts per CPC group
# -------------------------------
yearly_counts = (
    df_cpc.groupby(["cpc_group", "filing_year"])
    .size()
    .reset_index(name="cnt")
    .sort_values(["cpc_group", "filing_year"])
)

# -------------------------------
# 6. Compute Exponential Moving Average (EMA) with alpha = 0.1
# -------------------------------
alpha = 0.1
ema_results = []
for group, subdf in yearly_counts.groupby("cpc_group"):
    ema_prev = 0
    for _, row in subdf.iterrows():
        ema = row["cnt"] * alpha + ema_prev * (1 - alpha)
        ema_results.append((group, row["filing_year"], ema))
        ema_prev = ema

ema_df = pd.DataFrame(ema_results, columns=["cpc_group", "filing_year", "ema"])

# -------------------------------
# 7. Select the year with the highest EMA for each CPC group
#    (break ties by taking the latest year)
# -------------------------------
best_years = (
    ema_df.sort_values(["cpc_group", "ema", "filing_year"], ascending=[True, False, False])
    .drop_duplicates(subset=["cpc_group"])
)

# -------------------------------
# 8. Merge title and filter by level = 4
# -------------------------------
best_years = best_years.merge(df_cpc_def, left_on="cpc_group", right_on="symbol")
best_years = best_years[best_years["level"] == 4]

# -------------------------------
# 9. Output full title, CPC group, and best year
# -------------------------------
output = best_years[["titleFull", "cpc_group", "filing_year"]].rename(columns={"filing_year": "best_year"})

# Save the final ground truth file
output.to_csv("ground_truth.csv", index=False, encoding="utf-8")

print("✅ Ground truth generated and saved to ground_truth.csv")
print(output.head(10))
