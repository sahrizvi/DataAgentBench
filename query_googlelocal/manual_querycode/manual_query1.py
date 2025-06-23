import mysql.connector
import sqlite3
import pandas as pd
import openai
import time
from openai import AzureOpenAI

# ========== Configuration ========== #
client = AzureOpenAI(
    api_key="609ced4d971240b8a08f7fb0e6d846ea",
    api_version="2024-08-01-preview",
    azure_endpoint="https://promptdelta-nc.openai.azure.com",  # 不要加 /v1
)
deployment_name = "gpt-4o-mini" 

#mysql_password = "your_mysql_password"  # Replace with your MySQL root password
mysql_db = "ucb_db"
mysql_table = "business_descriptions"
mysql_password = "20041025"

# ========== Connect to MySQL ========== #
def fetch_business_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database=mysql_db
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {mysql_table}")
        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return rows, column_names
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return [], []
    
rows, column_names = fetch_business_data()

# ========== GPT-based Filter for Los Angeles ========== #
def is_los_angeles(description, client, deployment_name):
    prompt = (
        "Does the following business description mention that it is located in Los Angeles?\n"
        "Just answer 'yes' or 'no'.\n\n"
        f"Description: {description}"
    )
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts geographic location from business descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=5
        )
        return response.choices[0].message.content.strip().lower().startswith("yes")
    except Exception as e:
        print(f"GPT error: {e}")
        return False

# ========== Filter Businesses by GPT ========== #
la_data = []
for i, row in enumerate(rows):
    record = dict(zip(column_names, row))
    description = record.get("description", "")
    if description and is_los_angeles(description, client, deployment_name):
        la_data.append(record)
        print(f"✅ [{i}] Los Angeles business: {description}")
    else:
        print(f"❌ [{i}] Not in Los Angeles")

print(f"\n Total Los Angeles businesses retained: {len(la_data)}")

# ========== Load Ratings from review_query.db ========== #
la_df = pd.DataFrame(la_data)
gmap_ids = la_df["gmap_id"].tolist()

# Connect to review database and extract ratings
review_conn = sqlite3.connect("../query_dataset/review_query.db")
placeholder = ','.join('?' for _ in gmap_ids)
query = f"""
    SELECT gmap_id, rating
    FROM review
    WHERE gmap_id IN ({placeholder})
"""
review_df = pd.read_sql_query(query, review_conn, params=gmap_ids)

# Compute average rating per business
avg_rating = review_df.groupby("gmap_id")["rating"].mean().reset_index()
avg_rating.rename(columns={"rating": "avg_rating"}, inplace=True)

# Merge average rating with LA business data
la_with_rating = la_df.merge(avg_rating, on="gmap_id", how="left")

# ========== Select Top 5 Businesses ========== #
top5 = la_with_rating.sort_values(by="avg_rating", ascending=False).head(5)

# Output the result
print("\n Top 5 Los Angeles Businesses by Average Rating:\n")
print(top5)
