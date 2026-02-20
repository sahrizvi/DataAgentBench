code = """import json
import pandas as pd
from datetime import datetime

# Load the large query results from files whose paths are in the storage variables
with open(var_call_ytWvym9BzBoHsVn0Mh0kaUG3, 'r', encoding='utf-8') as f:
    reviews = json.load(f)
with open(var_call_UDZxYF1Rx43iIEXyFsXIuwji, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Create DataFrames
df_reviews = pd.DataFrame(reviews)
df_books = pd.DataFrame(books)

# Normalize and clean reviews
# Ensure rating numeric
df_reviews = df_reviews[df_reviews['rating'].notnull()].copy()
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Parse review_time
df_reviews['review_time'] = pd.to_datetime(df_reviews['review_time'], errors='coerce')
# Keep reviews from 2020 onwards (just in case)
df_reviews = df_reviews[df_reviews['review_time'] >= pd.to_datetime('2020-01-01')]

# Map purchase_id to book_id by replacing prefix 'purchaseid_' with 'bookid_'
# If different patterns exist, try to extract trailing numeric suffix
def to_bookid(pid):
    if not isinstance(pid, str):
        return None
    if pid.startswith('purchaseid_'):
        return pid.replace('purchaseid_', 'bookid_')
    # try to extract digits at end
    import re
    m = re.search(r'(\d+)$', pid)
    if m:
        return 'bookid_' + m.group(1)
    return pid

df_reviews['book_id'] = df_reviews['purchase_id'].apply(to_bookid)

# Aggregate reviews per book
agg = df_reviews.groupby('book_id').agg(avg_rating=('rating', 'mean'), review_count=('rating', 'count')).reset_index()

# Clean books categories and filter for Children's Books
# categories field is a string representation of a list
# We'll treat it as string and search for "Children's Books"

def is_children(cat):
    if pd.isna(cat):
        return False
    return "Children's Books" in cat

df_books['is_children'] = df_books['categories'].apply(is_children)
children_books = df_books[df_books['is_children']].copy()

# Merge aggregated ratings with books
merged = pd.merge(children_books, agg, on='book_id', how='inner')
# Filter avg_rating >= 4.5
result_df = merged[merged['avg_rating'] >= 4.5].copy()
# Select relevant columns
result_df = result_df[['book_id', 'title', 'categories', 'avg_rating', 'review_count']]
# Sort
result_df = result_df.sort_values(by=['avg_rating', 'review_count'], ascending=[False, False])

# Convert to JSON-serializable list of dicts
result_list = []
for _, row in result_df.iterrows():
    result_list.append({
        'book_id': str(row['book_id']),
        'title': str(row['title']),
        'avg_rating': round(float(row['avg_rating']), 3),
        'review_count': int(row['review_count']),
        'categories': str(row['categories'])
    })

import json
print("__RESULT__:")
print(json.dumps(result_list))"""

env_args = {'var_call_CTFrnWlW6LPX5Fzs4AV9MZ2d': ['books_info'], 'var_call_ytWvym9BzBoHsVn0Mh0kaUG3': 'file_storage/call_ytWvym9BzBoHsVn0Mh0kaUG3.json', 'var_call_UDZxYF1Rx43iIEXyFsXIuwji': 'file_storage/call_UDZxYF1Rx43iIEXyFsXIuwji.json'}

exec(code, env_args)
