code = """import json
import pandas as pd
import re

# Load data from storage-provided file paths
with open(var_call_gIrUhVzAe4Pfq3yKAzhzVxW6, 'r') as f:
    books = json.load(f)
with open(var_call_mtGCbjxvLbqmkWHrHDpxSpdv, 'r') as f:
    reviews = json.load(f)

# Create dataframes
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure rating numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = df_reviews['rating'].astype(float)

# Extract numeric id from book_id/purchase_id
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

df_books['num_id'] = df_books['book_id'].apply(extract_num)
df_reviews['num_id'] = df_reviews['purchase_id'].apply(extract_num)

# Filter books to those in Literature & Fiction and English-language in details
mask_cat = df_books['categories'].str.contains('Literature & Fiction', case=False, na=False)
mask_lang = df_books['details'].str.contains('English', case=False, na=False)
df_books_filtered = df_books[mask_cat & mask_lang].copy()

# Compute average rating per num_id
rating_stats = df_reviews.groupby('num_id', dropna=True).agg(avg_rating=('rating','mean'), review_count=('rating','count')).reset_index()

# Select those with perfect average 5.0 (allow tiny floating tolerance)
perfect = rating_stats[rating_stats['avg_rating'].round(3) == 5.0]

# Join with books
result = pd.merge(df_books_filtered, perfect, on='num_id', how='inner')

# Prepare output list of dicts
out = []
for _, row in result.iterrows():
    out.append({
        'title': row['title'],
        'book_id': row['book_id'],
        'categories': row['categories'],
        'details': row['details'],
        'avg_rating': float(round(row['avg_rating'], 3)),
        'review_count': int(row['review_count'])
    })

# If none, return empty list
json_out = json.dumps(out)
print("__RESULT__:")
print(json_out)"""

env_args = {'var_call_7lY2nYRo78k7sxnvaH8tjp4Z': ['books_info'], 'var_call_gIrUhVzAe4Pfq3yKAzhzVxW6': 'file_storage/call_gIrUhVzAe4Pfq3yKAzhzVxW6.json', 'var_call_qbeJhuRqPrAvZC7hFxq8Vq06': ['review'], 'var_call_mtGCbjxvLbqmkWHrHDpxSpdv': 'file_storage/call_mtGCbjxvLbqmkWHrHDpxSpdv.json'}

exec(code, env_args)
