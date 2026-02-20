code = """import json
import pandas as pd
import re

# Load query results from storage file paths
books_path = var_call_IYtacIxSFBTYJw97vct4mvsq
reviews_path = var_call_xbNtMZkJ3hL1hFsQa1OA77iD

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract numeric suffix from book_id and purchase_id for fuzzy join
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)$", s)
    return m.group(1) if m else None

df_books['num_id'] = df_books['book_id'].apply(extract_num)
df_reviews['num_id'] = df_reviews['purchase_id'].apply(extract_num)

# Normalize avg_rating to float and n_reviews to int
# avg_rating in reviews query may be strings; convert safely
df_reviews['avg_rating'] = pd.to_numeric(df_reviews['avg_rating'], errors='coerce')
df_reviews['n_reviews'] = pd.to_numeric(df_reviews['n_reviews'], errors='coerce').fillna(0).astype(int)

# Filter books to Literature & Fiction category and English language in details
mask_lit = df_books['categories'].str.contains('Literature & Fiction', case=False, na=False)
mask_english = df_books['details'].str.contains('English', case=False, na=False)
df_books_filtered = df_books[mask_lit & mask_english].copy()

# Merge on numeric id
merged = pd.merge(df_books_filtered, df_reviews, on='num_id', how='inner', suffixes=('_book', '_rev'))

# Select rows with perfect average rating 5.0
perfect = merged[merged['avg_rating'].notna() & (merged['avg_rating'] == 5.0)].copy()

# Prepare output records
if perfect.empty:
    output = []
else:
    cols = ['book_id', 'title', 'author' if 'author' in perfect.columns else None, 'purchase_id', 'avg_rating', 'n_reviews', 'categories', 'details']
    # Clean columns list
    cols = [c for c in cols if c is not None and c in perfect.columns]
    records = perfect[cols].to_dict(orient='records')
    # Ensure JSON-serializable types
    for r in records:
        if 'avg_rating' in r:
            r['avg_rating'] = float(r['avg_rating'])
        if 'n_reviews' in r:
            r['n_reviews'] = int(r['n_reviews'])
    output = records

print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_Y8ZqwwTLhcXx4Rc6fjvtt2k5': ['books_info'], 'var_call_IYtacIxSFBTYJw97vct4mvsq': 'file_storage/call_IYtacIxSFBTYJw97vct4mvsq.json', 'var_call_xbNtMZkJ3hL1hFsQa1OA77iD': 'file_storage/call_xbNtMZkJ3hL1hFsQa1OA77iD.json'}

exec(code, env_args)
