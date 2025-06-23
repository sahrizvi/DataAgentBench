import pandas as pd
import ast
from collections import defaultdict

def get_2016_user_category_stats(user_path, review_path, business_path):
    """
    For users who registered in 2016:
      - Count number of such users
      - Count total reviews they wrote since then
      - Identify top 5 business categories reviewed by them

    Args:
        user_path (str): Path to user JSONL
        review_path (str): Path to review JSONL
        business_path (str): Path to business JSONL

    Returns:
        tuple: (user_count, total_review_count, pd.DataFrame with top 5 categories)
    """
    df_user = pd.read_json(user_path, lines=True)
    df_review = pd.read_json(review_path, lines=True)
    df_business = pd.read_json(business_path, lines=True)

    # Parse registration year
    df_user["yelping_since"] = pd.to_datetime(df_user["yelping_since"])
    df_user["registration_year"] = df_user["yelping_since"].dt.year
    df_2016_users = df_user[df_user["registration_year"] == 2016]
    user_ids = set(df_2016_users["user_id"])

    # Filter reviews by those users
    df_review_2016 = df_review[df_review["user_id"].isin(user_ids)]

    # Count
    user_count = len(user_ids)
    total_review_count = len(df_review_2016)

    # Merge with business info to get categories
    df_merged = df_review_2016.merge(df_business[["business_id", "categories"]], on="business_id", how="left")

    # Parse categories (comma-separated string to list)
    def parse_categories(cat_str):
        if isinstance(cat_str, str):
            return [c.strip() for c in cat_str.split(",") if c.strip()]
        return []

    df_merged["category_list"] = df_merged["categories"].apply(parse_categories)

    # Count all categories
    category_counter = defaultdict(int)
    for cats in df_merged["category_list"]:
        for cat in cats:
            category_counter[cat] += 1

    top_categories = sorted(category_counter.items(), key=lambda x: x[1], reverse=True)[:5]
    df_top = pd.DataFrame(top_categories, columns=["category", "review_count"])

    return user_count, total_review_count, df_top


if __name__ == "__main__":
    user_file = "../ground_truth_dataset/user_gt.json"
    review_file = "../ground_truth_dataset/review_gt.json"
    business_file = "../ground_truth_dataset/business_gt.json"

    user_count, review_count, top_categories = get_2016_user_category_stats(
        user_path=user_file,
        review_path=review_file,
        business_path=business_file
    )

    # ✅ Output
    print(f"Number of users who registered in 2016: {user_count}")
    print(f"Total reviews written by them since then: {review_count}")
    print("Top 5 most-reviewed business categories by these users:")

    print(top_categories.to_string(index=False))

    # Optional: save to CSV
    # top_categories.to_csv("top5_categories_by_2016_users.csv", index=False)
