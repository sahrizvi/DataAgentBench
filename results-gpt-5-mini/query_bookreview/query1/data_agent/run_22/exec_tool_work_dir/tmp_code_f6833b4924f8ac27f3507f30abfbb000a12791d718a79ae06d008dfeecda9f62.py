code = """import json
import pandas as pd
import re

# Load data from storage-provided file paths
with open(var_call_AG1ZZGGNIQrP8nzfD6SXWOFQ, 'r') as f:
    books = json.load(f)
with open(var_call_ZpJXgAtJnk75JklU6IZ5afnk, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize review ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id like 'purchaseid_123' to book_id 'bookid_123'
def map_purchase_to_book(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r'(\d+)$', pid)
    return f"bookid_{m.group(1)}" if m else None

df_reviews['book_id'] = df_reviews['purchase_id'].apply(map_purchase_to_book)

# Extract publication year from details in books
def extract_year(details):
    if not isinstance(details, str):
        return None
    # find first 4-digit year between 1000 and 2023
    m = re.search(r'\b(1[0-9]{3}|20[0-9]{2})\b', details)
    if not m:
        return None
    y = int(m.group(0))
    if y > 2023:
        return None
    return y

df_books['year'] = df_books['details'].apply(extract_year)

# Merge reviews with books on book_id
merged = df_reviews.merge(df_books[['book_id', 'year']], on='book_id', how='inner')

# Drop rows without year or rating
merged = merged.dropna(subset=['year', 'rating'])
merged['year'] = merged['year'].astype(int)

# Compute decade label
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s")

# Group by decade
grp = merged.groupby('decade').agg(
    avg_rating=('rating', 'mean'),
    distinct_books=('book_id', pd.Series.nunique)
).reset_index()

# Filter decades with at least 10 distinct books
grp_filtered = grp[grp['distinct_books'] >= 10]

if grp_filtered.empty:
    result = None
else:
    # Find decade with highest average rating; if tie, take the one with more distinct books, then earliest decade
    max_avg = grp_filtered['avg_rating'].max()
    candidates = grp_filtered[grp_filtered['avg_rating'] == max_avg]
    if len(candidates) > 1:
        candidates = candidates.sort_values(['distinct_books', 'decade'], ascending=[False, True])
    best = candidates.iloc[0]
    result = best['decade']

import json as _json
print("__RESULT__:")
print(_json.dumps(result))"""

env_args = {'var_call_AG1ZZGGNIQrP8nzfD6SXWOFQ': 'file_storage/call_AG1ZZGGNIQrP8nzfD6SXWOFQ.json', 'var_call_ZpJXgAtJnk75JklU6IZ5afnk': 'file_storage/call_ZpJXgAtJnk75JklU6IZ5afnk.json'}

exec(code, env_args)
