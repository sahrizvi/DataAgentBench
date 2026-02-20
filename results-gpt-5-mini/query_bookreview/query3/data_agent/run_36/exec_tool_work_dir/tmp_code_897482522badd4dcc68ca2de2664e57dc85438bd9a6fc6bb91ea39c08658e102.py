code = """import json
import pandas as pd

# Load data from stored JSON file paths
with open(var_call_w1SPxF15aUMjLaPLoXjNpKEp, 'r') as f:
    books = json.load(f)
with open(var_call_HWaRHUBz912QRuu4YzVVlzYU, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# Clean and prepare reviews
if 'rating' in df_r.columns:
    df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
else:
    df_r['rating'] = pd.Series(dtype=float)

# Map purchase_id -> book_id by replacing prefix
if 'purchase_id' in df_r.columns:
    df_r['book_id'] = df_r['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')
else:
    df_r['book_id'] = pd.Series(dtype=str)

# Aggregate reviews from 2020 onwards (already filtered by query)
grp = df_r.groupby('book_id', dropna=True).agg(avg_rating=('rating', 'mean'), review_count=('rating', 'count')).reset_index()

# Filter for avg_rating >= 4.5
top = grp[grp['avg_rating'] >= 4.5]

# Merge with books info to get titles and authors
df_merged = pd.merge(top, df_b, on='book_id', how='left')

# Round avg_rating
df_merged['avg_rating'] = df_merged['avg_rating'].round(3)

# Build result list
result = []
for _, row in df_merged.sort_values(['avg_rating', 'review_count'], ascending=[False, False]).iterrows():
    result.append({
        'book_id': row.get('book_id', None),
        'title': row.get('title', None),
        'author': row.get('author', None),
        'avg_rating': float(row['avg_rating']) if pd.notna(row['avg_rating']) else None,
        'review_count': int(row['review_count']) if pd.notna(row['review_count']) else 0
    })

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json'}

exec(code, env_args)
