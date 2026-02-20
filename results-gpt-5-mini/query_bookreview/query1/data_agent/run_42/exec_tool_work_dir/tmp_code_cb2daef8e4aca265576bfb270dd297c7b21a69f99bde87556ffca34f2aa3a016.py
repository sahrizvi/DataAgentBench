code = """import json
import pandas as pd
import re

# Load data from storage-provided file paths
with open(var_call_gFlNznSq6Utee2SjS70Yk8dE, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_JhD0OJJ6ZMLDhjEXdlyza15K, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize ratings to float
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Extract numeric id suffix from book_id and purchase_id
def extract_num(s):
    if pd.isna(s):
        return None
    m = re.search(r"(\d+)", str(s))
    return int(m.group(1)) if m else None

books_df['book_num'] = books_df['book_id'].apply(extract_num)
reviews_df['purchase_num'] = reviews_df['purchase_id'].apply(extract_num)

# Extract publication year from details using regex for 4-digit year
def extract_year(s):
    if pd.isna(s):
        return None
    # look for years from 1500 to 2023
    m = re.search(r"(1[5-9]\d{2}|20\d{2})", str(s))
    if not m:
        return None
    year = int(m.group(1))
    if year > 2023:
        return None
    return year

books_df['year'] = books_df['details'].apply(extract_year)
books_df = books_df.dropna(subset=['book_num'])

# Merge average rating per book
book_avg = reviews_df.dropna(subset=['purchase_num','rating']).groupby('purchase_num', as_index=False).agg({'rating':'mean'})
book_avg.rename(columns={'purchase_num':'book_num','rating':'avg_rating'}, inplace=True)

merged = pd.merge(book_avg, books_df[['book_num','year','book_id','title']], on='book_num', how='left')

# Drop entries without year
merged = merged.dropna(subset=['year'])
merged['year'] = merged['year'].astype(int)
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s")

# For each decade, compute number of distinct books (based on book_num) and average of per-book averages
agg = merged.groupby('decade').agg(num_books=('book_num','nunique'),
                                   decade_avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
agg_filtered = agg[agg['num_books'] >= 10]

if agg_filtered.empty:
    result = {"decade": None, "average_rating": None, "num_books": 0}
else:
    # pick decade with highest average rating; in tie, pick the earliest decade by alphabetical? we'll pick the max avg then smallest decade string
    best = agg_filtered.sort_values(['decade_avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = {"decade": best['decade'], "average_rating": round(float(best['decade_avg_rating']), 4), "num_books": int(best['num_books'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_GahRlqIjAykkMimdusXpPvR2': ['books_info'], 'var_call_gFlNznSq6Utee2SjS70Yk8dE': 'file_storage/call_gFlNznSq6Utee2SjS70Yk8dE.json', 'var_call_Zb6EdVlbKfYcgudCchNKPMDU': ['review'], 'var_call_JhD0OJJ6ZMLDhjEXdlyza15K': 'file_storage/call_JhD0OJJ6ZMLDhjEXdlyza15K.json'}

exec(code, env_args)
