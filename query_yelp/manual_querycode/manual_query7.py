import duckdb
import pandas as pd
from pymongo import MongoClient
from openai import AzureOpenAI
import json

# === Step 0: Setup Connections ===
con_duck = duckdb.connect("../query_dataset/yelp_user.db")
client_mongo = MongoClient("mongodb://localhost:27017/")
biz_collection = client_mongo["yelp_business"]["business"]

deployment_name = "gpt-4o-mini"
client = AzureOpenAI(
    api_key="609ced4d971240b8a08f7fb0e6d846ea",
    api_version="2024-08-01-preview",
    azure_endpoint="https://promptdelta-nc.openai.azure.com"
)


# === Step 1: Load user and review data ===
df_user = con_duck.execute("SELECT * FROM user").fetchdf()
df_review = con_duck.execute("SELECT * FROM review").fetchdf()
df_review["date"] = pd.to_datetime(df_review["date"], unit="ms", errors="coerce")

# === Step 2: Filter users who registered in 2016 ===
df_user["yelping_since"] = pd.to_datetime(df_user["yelping_since"], errors="coerce")
df_user_2016 = df_user[df_user["yelping_since"].dt.year == 2016].copy()
user_ids_2016 = df_user_2016["user_id"].unique().tolist()

# === Step 3: Filter reviews by those users since their registration ===
df_reviews_from_2016_users = df_review[df_review["user_id"].isin(user_ids_2016)].copy()

# === Step 4: Map business_ref to business_id ===
business_refs = df_reviews_from_2016_users["business_ref"].dropna().unique().tolist()
business_docs = list(biz_collection.find({}, {"business_id": 1, "description": 1}))
business_ids = [b["business_id"] for b in business_docs if "business_id" in b]

# === Step 5: GPT infer mapping rule ===
def get_mapping_rule(business_ids, business_refs):
    prompt = (
        "You are given two complete ID columns from two different datasets:\n"
        f"- The first column is `business_ref` from a review dataset: {json.dumps(business_refs, indent=2)}\n"
        f"- The second column is `business_id` from a business metadata dataset: {json.dumps(business_ids, indent=2)}\n\n"
        "Each business_ref corresponds to a business_id, but the mapping rule is not provided.\n"
        "Determine the mapping relationship between the two sets of IDs.\n"
        "Please respond with:\n"
        "1. The exact mapping rule in plain English\n"
        "2. An explanation of why you think this rule holds."
    )
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a data engineer analyzing ID columns from different datasets to infer a mapping rule."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

mapping_rule_explanation = get_mapping_rule(business_ids, business_refs)
print("\n🧠 GPT-inferred mapping rule:\n", mapping_rule_explanation)

# === Step 6: Resolve business_ref → business_id ===
def resolve_ref_to_id(business_ref):
    prompt = (
        f"The inferred mapping rule is:\n\n{mapping_rule_explanation}\n\n"
        f"Now determine the business_id for:\n"
        f"- business_ref: {business_ref}\n\n"
        "Only respond with the business_id (e.g., 'biz_001')."
    )
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a data assistant mapping business_ref to business_id."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=20
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT error on {business_ref}: {e}")
        return None

ref_to_id_map = {}
predicted_business_ids = []

for i, row in df_reviews_from_2016_users.iterrows():
    business_ref = row["business_ref"]
    if pd.isna(business_ref):
        predicted_business_ids.append(None)
        continue

    if business_ref not in ref_to_id_map:
        ref_to_id_map[business_ref] = resolve_ref_to_id(business_ref)

    business_id = ref_to_id_map[business_ref]
    predicted_business_ids.append(business_id)
    print(f"[{i}] business_ref = {business_ref} → business_id = {business_id}")

df_reviews_from_2016_users = df_reviews_from_2016_users.copy()
df_reviews_from_2016_users["business_id"] = predicted_business_ids

# === Step 7: Extract name + category from description ===
def extract_categories(description):
    prompt = (
        "Based on the following business description, identify one or more likely business categories.\n"
        "Respond with a comma-separated list (e.g., 'Nail Salon, Spa').\n\n"
        f"Description: {description}"
    )
    try:
        res = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You extract business categories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=30
        )
        return res.choices[0].message.content.strip()
    except:
        return "Unknown"

biz_id_to_desc = {b["business_id"]: b.get("description", "") for b in business_docs}
category_records = []
for biz_id in df_reviews_from_2016_users["business_id"].dropna().unique():
    desc = biz_id_to_desc.get(biz_id, "")
    if not desc:
        continue
    cats = extract_categories(desc)
    for cat in [c.strip() for c in cats.split(",") if c.strip()]:
        category_records.append({"business_id": biz_id, "category": cat})
    print({biz_id}, {desc}, (cats))
df_category_map = pd.DataFrame(category_records)

# === Step 8: Merge category info with review counts ===
df_review_counts = df_reviews_from_2016_users.groupby("business_id").size().reset_index(name="review_count")
df_merge = df_category_map.merge(df_review_counts, on="business_id", how="inner")
df_top = df_merge.groupby("category")["review_count"].sum().reset_index()
df_top = df_top.sort_values(by="review_count", ascending=False).head(5)

# === Step 9: Output ===
print("\n Top 5 Categories (2016 users):")
print(df_top)