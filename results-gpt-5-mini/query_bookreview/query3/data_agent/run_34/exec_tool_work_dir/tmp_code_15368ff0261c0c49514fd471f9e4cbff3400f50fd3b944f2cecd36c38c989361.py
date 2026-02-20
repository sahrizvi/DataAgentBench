code = """import json
import pandas as pd

# Load data from storage file paths
with open(var_call_SimpA06dt5RaDc35kN1qJ4Cx, 'r') as f:
    books = json.load(f)
with open(var_call_wQPw2fgJXAbet4r995pYeSuD, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure necessary columns exist
if 'book_id' not in df_books.columns:
    df_books['book_id'] = None

# Clean and convert ratings
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = pd.NA

# Drop reviews without numeric rating
df_reviews = df_reviews.dropna(subset=['rating']).copy()

# Map purchase_id to book_id by replacing prefix
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')
else:
    df_reviews['book_id'] = None

# Aggregate average rating and counts since reviews were already filtered in SQL
agg = (
    df_reviews.groupby('book_id')
    .agg(avg_rating=('rating', 'mean'), review_count=('rating', 'count'))
    .reset_index()
)

# Filter for average rating >= 4.5
agg_filtered = agg[agg['avg_rating'] >= 4.5]

# Join with books info (books list was already filtered for Children's Books in SQL)
result = pd.merge(agg_filtered, df_books[['book_id', 'title', 'author', 'categories', 'details']], on='book_id', how='inner')

# Prepare final output list
if not result.empty:
    result = result.sort_values(['avg_rating', 'review_count'], ascending=[False, False])
    output = []
    for _, row in result.iterrows():
        output.append({
            'book_id': row['book_id'],
            'title': row.get('title', None),
            'author': row.get('author', None),
            'avg_rating': round(float(row['avg_rating']), 3),
            'review_count': int(row['review_count']),
            'categories': row.get('categories', None)
        })
else:
    output = []

import json as _json
print("__RESULT__:")
print(_json.dumps(output))"""

env_args = {'var_call_0C8uwpKxowvKhWAtQ9COH81A': ['books_info'], 'var_call_SimpA06dt5RaDc35kN1qJ4Cx': 'file_storage/call_SimpA06dt5RaDc35kN1qJ4Cx.json', 'var_call_63Llc1wtT8Vnf7jIFuUKPat5': ['review'], 'var_call_wQPw2fgJXAbet4r995pYeSuD': 'file_storage/call_wQPw2fgJXAbet4r995pYeSuD.json'}

exec(code, env_args)
