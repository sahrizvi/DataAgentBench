import pandas as pd
import ast

def get_parking_business_count(business_path, review_path, target_year=2018):
    """
    Count how many businesses that received reviews in a given year
    offer either BusinessParking or BikeParking.

    Args:
        business_path (str): Path to business JSONL file.
        review_path (str): Path to review JSONL file.
        target_year (int): The year to filter reviews by.

    Returns:
        int: Number of businesses matching the condition.
    """
    # Load data
    df_business = pd.read_json(business_path, lines=True)
    df_review = pd.read_json(review_path, lines=True)

    # Parse review date and filter by year
    df_review["date"] = pd.to_datetime(df_review["date"])
    df_review_year = df_review[df_review["date"].dt.year == target_year].copy()

    # Get unique business_ids reviewed in that year
    reviewed_ids = df_review_year["business_id"].unique()

    # Filter businesses that received reviews in that year
    df_active = df_business[df_business["business_id"].isin(reviewed_ids)].copy()

    # Parse attributes safely
    def parse_attributes(attr):
        if isinstance(attr, dict):
            return attr
        try:
            return ast.literal_eval(attr)
        except:
            return {}

    df_active["attributes_parsed"] = df_active["attributes"].apply(parse_attributes)

    # Check for either BusinessParking or BikeParking
    def has_parking(attrs):
        return "BusinessParking" in attrs or "BikeParking" in attrs

    df_active["has_parking_attr"] = df_active["attributes_parsed"].apply(has_parking)

    return df_active["has_parking_attr"].sum()


if __name__ == "__main__":
    business_file = "../ground_truth_dataset/business_gt.json"
    review_file = "../ground_truth_dataset/review_gt.json"

    count = get_parking_business_count(business_file, review_file, target_year=2018)

    print(count)
