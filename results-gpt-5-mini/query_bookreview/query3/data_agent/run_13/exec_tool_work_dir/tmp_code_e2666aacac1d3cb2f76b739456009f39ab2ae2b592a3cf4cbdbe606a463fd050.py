code = """import json
import pandas as pd

# Load data from storage-provided file paths
with open(var_call_8fVwZTnTtGyVVGpOyMbVTkKA, 'r') as f:
    reviews = json.load(f)
with open(var_call_ZwBzbF3xrkCfpiNmxfTvA3G4, 'r') as f:
    books = json.load(f)

# Create DataFrames
df_rev = pd.DataFrame(reviews)
df_books = pd.DataFrame(books)

# Normalize and clean review data
df_rev['rating'] = pd.to_numeric(df_rev['rating'], errors='coerce')
# Parse dates
df_rev['review_time'] = pd.to_datetime(df_rev['review_time'], errors='coerce')
# Filter reviews from 2020-01-01 onwards
df_rev = df_rev[df_rev['review_time'] >= pd.to_datetime('2020-01-01')]

# Group by purchase_id and compute average rating and count
grp = df_rev.groupby('purchase_id').agg(avg_rating=('rating', 'mean'), review_count=('rating','count')).reset_index()
# Map purchase_id to book_id by replacing prefix
grp['book_id'] = grp['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Prepare books data: ensure categories is string
df_books['categories'] = df_books['categories'].astype(str)

# Merge grouped review stats with books
merged = pd.merge(grp, df_books, on='book_id', how='left')

# Filter for Children's Books in categories
mask_child = merged['categories'].str.contains("Children's Books", na=False)
merged_child = merged[mask_child].copy()

# Filter for average rating >= 4.5
result_df = merged_child[merged_child['avg_rating'] >= 4.5].copy()

# Prepare output
output = []
for _, row in result_df.iterrows():
    output.append({
        'book_id': row.get('book_id'),
        'title': row.get('title'),
        'avg_rating': round(float(row.get('avg_rating')), 3) if pd.notna(row.get('avg_rating')) else None,
        'review_count': int(row.get('review_count')) if pd.notna(row.get('review_count')) else 0,
        'categories': row.get('categories')
    })

# Sort output by avg_rating desc then review_count desc
output = sorted(output, key=lambda x: (-x['avg_rating'], -x['review_count']))

import json as _json
print("__RESULT__:")
print(_json.dumps(output))"""

env_args = {'var_call_8fVwZTnTtGyVVGpOyMbVTkKA': 'file_storage/call_8fVwZTnTtGyVVGpOyMbVTkKA.json', 'var_call_ZwBzbF3xrkCfpiNmxfTvA3G4': 'file_storage/call_ZwBzbF3xrkCfpiNmxfTvA3G4.json'}

exec(code, env_args)
