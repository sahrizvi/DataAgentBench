import pandas as pd
import json

# 读取数据
df_pub = pd.read_csv("../ground_truth_dataset/PUBLICATIONS.csv")
df_cpc_def = pd.read_csv("../ground_truth_dataset/CPC_DEFINITION.csv")

# 确保 application_number 不为空
df_pub = df_pub[df_pub["application_number"].notna() & (df_pub["application_number"] != "")]

# 每个 application_number 取一条记录（取 filing_date 最大的那条）
df_pub = df_pub.sort_values("filing_date", ascending=False).drop_duplicates(subset=["application_number"])

# 展开 cpc JSON
def extract_first_cpcs(cpc_str):
    try:
        cpcs = json.loads(cpc_str)
        return [c["code"] for c in cpcs if c.get("first") is True]
    except:
        return []

df_pub["cpc_list"] = df_pub["cpc"].apply(extract_first_cpcs)

# 与 CPC_DEFINITION 表关联
df_cpc = df_pub.explode("cpc_list").merge(
    df_cpc_def,
    left_on="cpc_list",
    right_on="symbol",
    how="inner"
)

# 展开 parents 作为 cpc_group
def parse_parents(parents_str):
    try:
        return json.loads(parents_str)
    except:
        return []

df_cpc["parents_list"] = df_cpc["parents"].apply(parse_parents)
df_cpc = df_cpc.explode("parents_list").rename(columns={"parents_list": "cpc_group"})

# 提取 filing_year
df_cpc["filing_year"] = (df_cpc["filing_date"] // 10000).astype(int)
df_cpc = df_cpc[df_cpc["filing_year"] > 0]

# 每年计数
yearly_counts = df_cpc.groupby(["cpc_group", "filing_year"]).size().reset_index(name="cnt")
yearly_counts = yearly_counts.sort_values(["cpc_group", "filing_year"])

# 计算 EMA
alpha = 0.2
ema_results = []
for group, subdf in yearly_counts.groupby("cpc_group"):
    ema_prev = 0
    for _, row in subdf.iterrows():
        ema = row["cnt"] * alpha + ema_prev * (1 - alpha)
        ema_results.append((group, row["filing_year"], ema))
        ema_prev = ema
ema_df = pd.DataFrame(ema_results, columns=["cpc_group", "filing_year", "ema"])

# 找出 EMA 最大的年份（年份相同取更大年份）
best_years = (
    ema_df.sort_values(["cpc_group", "ema", "filing_year"], ascending=[True, False, False])
    .drop_duplicates(subset=["cpc_group"])
)

# 过滤 level=5
best_years = best_years.merge(df_cpc_def, left_on="cpc_group", right_on="symbol")
best_years = best_years[best_years["level"] == 5]

# 选择输出列
output = best_years[["titleFull", "cpc_group", "filing_year"]].rename(columns={"filing_year": "best_filing_year"})

# 保存
output.to_csv("ground_truth_cpc_best_year.csv", index=False, encoding="utf-8")

print("✅ Ground truth 生成完成，保存到 ground_truth_cpc_best_year.csv")
print(output.head(10))
