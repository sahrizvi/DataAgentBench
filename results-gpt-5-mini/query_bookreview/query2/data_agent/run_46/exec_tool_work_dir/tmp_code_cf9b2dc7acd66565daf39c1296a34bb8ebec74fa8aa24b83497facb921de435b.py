code = """import json
import pandas as pd

# Load stored query results from files
with open(var_call_PQc0MqYnjZsec9IBk3itp1Ak, 'r') as f:
    books = json.load(f)
with open(var_call_BwU6rmtiWJgwxQvbK4Ii4D47, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize and filter books: categories contains 'Literature & Fiction' and details mentions 'English'
def has_lit_and_english(cat, det):
    try:
        cat_ok = isinstance(cat, str) and 'literature & fiction' in cat.lower()
    except:
        cat_ok = False
    try:
        det_ok = isinstance(det, str) and 'english' in det.lower()
    except:
        det_ok = False
    return cat_ok and det_ok

mask = df_books.apply(lambda r: has_lit_and_english(r.get('categories',''), r.get('details','')), axis=1)
df_books_filtered = df_books[mask].copy()

# Prepare reviews: convert rating to numeric and map purchase_id -> book_id
if not df_reviews.empty:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')
else:
    df_reviews['rating'] = pd.Series(dtype=float)
    df_reviews['book_id'] = pd.Series(dtype=str)

# Compute average rating per book_id
grp = df_reviews.groupby('book_id')['rating'].agg(['mean','count']).reset_index()
# Select books with perfect average 5.0
perfect = grp[grp['mean'] == 5.0]

# Join with filtered books to ensure category and language
result = pd.merge(perfect, df_books_filtered, on='book_id', how='inner')

# Build output list
out = []
for _, row in result.iterrows():
    out.append({
        'book_id': row['book_id'],
        'title': row.get('title', None),
        'average_rating': float(row['mean']),
        'rating_count': int(row['count'])
    })

# Print result in required format
print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_gamWCFI6DL7eZIaJD7dEVs80': [], 'var_call_jOSfuDH5qWhjqhKyL61DfJ97': ['books_info'], 'var_call_PQc0MqYnjZsec9IBk3itp1Ak': 'file_storage/call_PQc0MqYnjZsec9IBk3itp1Ak.json', 'var_call_Um9IU9sjvLaZ7om0m36R5PRP': ['review'], 'var_call_BwU6rmtiWJgwxQvbK4Ii4D47': 'file_storage/call_BwU6rmtiWJgwxQvbK4Ii4D47.json'}

exec(code, env_args)
