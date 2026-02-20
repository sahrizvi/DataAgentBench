code = """import json
import pandas as pd
import re

# Load data from stored JSON files
with open(var_call_PeVQ4D9wMF3EZHsvUrq8X9qT, 'r') as f:
    reviews = json.load(f)
with open(var_call_in7KHwwIZ3NUwY8ADIgL9jcb, 'r') as f:
    books = json.load(f)

# Create DataFrame for reviews
rev_df = pd.DataFrame(reviews)
# Normalize columns
rev_df = rev_df.rename(columns={
    'purchase_id': 'purchase_id',
    'rating': 'rating',
    'review_time': 'review_time'
})
# Convert rating to numeric
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
# Parse review_time
rev_df['review_time'] = pd.to_datetime(rev_df['review_time'], errors='coerce')
# Filter reviews from 2020 onwards
rev_df = rev_df[rev_df['review_time'] >= pd.to_datetime('2020-01-01')]

# Extract numeric id from purchase_id and map to book_id
def map_purchase_to_book(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r"_(\d+)$", pid)
    if m:
        return 'bookid_' + m.group(1)
    # fallback: try to replace prefix 'purchaseid' with 'bookid'
    if pid.startswith('purchaseid'):
        return pid.replace('purchaseid', 'bookid')
    return None

rev_df['book_id'] = rev_df['purchase_id'].apply(map_purchase_to_book)
rev_df = rev_df.dropna(subset=['book_id'])

# Aggregate average rating and count per book_id
agg = rev_df.groupby('book_id').agg(avg_rating=('rating', 'mean'), review_count=('rating', 'count')).reset_index()

# Create books DataFrame
books_df = pd.DataFrame(books)
# Filter books that have "Children's Books" in categories
books_df['categories'] = books_df['categories'].fillna('')
mask_children = books_df['categories'].astype(str).str.contains("Children's Books", na=False)
children_books = books_df[mask_children][['book_id', 'title', 'categories']]

# Join with aggregated ratings
merged = pd.merge(children_books, agg, on='book_id', how='left')
# Keep those with avg_rating >= 4.5
result_df = merged[merged['avg_rating'] >= 4.5].copy()
# Round avg_rating
result_df['avg_rating'] = result_df['avg_rating'].round(3)

# Prepare result list
result = []
for _, row in result_df.sort_values(['avg_rating', 'review_count'], ascending=[False, False]).iterrows():
    result.append({
        'book_id': row['book_id'],
        'title': row['title'],
        'avg_rating': None if pd.isna(row['avg_rating']) else float(row['avg_rating']),
        'review_count': int(row['review_count']) if not pd.isna(row['review_count']) else 0,
        'categories': row['categories']
    })

# Print according to required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_PeVQ4D9wMF3EZHsvUrq8X9qT': 'file_storage/call_PeVQ4D9wMF3EZHsvUrq8X9qT.json', 'var_call_in7KHwwIZ3NUwY8ADIgL9jcb': 'file_storage/call_in7KHwwIZ3NUwY8ADIgL9jcb.json'}

exec(code, env_args)
