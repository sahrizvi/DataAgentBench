code = """import json
import pandas as pd
import re

# Load data from the stored JSON files (paths provided in variables)
with open(var_call_SGBK6hZl0e7oYwMlkrTe7x9t, 'r') as f:
    books = json.load(f)
with open(var_call_90EnN3axLy62ce2YnQdFmZQG, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize and extract numeric IDs
def extract_num(s):
    if pd.isna(s):
        return None
    m = re.search(r"(\d+)$", str(s))
    return int(m.group(1)) if m else None

df_books['book_num'] = df_books['book_id'].apply(extract_num)
df_reviews['purchase_num'] = df_reviews['purchase_id'].apply(extract_num)

# Convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Keep reviews from 2020 onwards - the query already filtered but ensure types
# Convert review_time to datetime
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'], errors='coerce')
df_reviews = df_reviews[df_reviews['review_time'] >= pd.to_datetime('2020-01-01')]

# Group reviews by purchase_num and compute average rating and count
grp = df_reviews.groupby('purchase_num').agg(average_rating=('rating', 'mean'), review_count=('rating', 'count')).reset_index()

# Filter for average_rating >= 4.5
highly_rated = grp[grp['average_rating'] >= 4.5]

# Join with books on numeric id
merged = pd.merge(highly_rated, df_books, left_on='purchase_num', right_on='book_num', how='inner')

# Prepare final results
if not merged.empty:
    merged['average_rating'] = merged['average_rating'].round(3)
    merged = merged.sort_values(by=['average_rating', 'review_count'], ascending=[False, False])
    result = []
    for _, row in merged.iterrows():
        result.append({
            'book_id': row['book_id'],
            'title': row.get('title'),
            'average_rating': float(row['average_rating']),
            'review_count': int(row['review_count']),
            'categories': row.get('categories')
        })
else:
    result = []

# Print in required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_SEv5u3xUp1fOIt96fexCnCJu': ['books_info'], 'var_call_KRVUg6aIfY0aN5gUEnPJjzzm': ['review'], 'var_call_SGBK6hZl0e7oYwMlkrTe7x9t': 'file_storage/call_SGBK6hZl0e7oYwMlkrTe7x9t.json', 'var_call_90EnN3axLy62ce2YnQdFmZQG': 'file_storage/call_90EnN3axLy62ce2YnQdFmZQG.json'}

exec(code, env_args)
