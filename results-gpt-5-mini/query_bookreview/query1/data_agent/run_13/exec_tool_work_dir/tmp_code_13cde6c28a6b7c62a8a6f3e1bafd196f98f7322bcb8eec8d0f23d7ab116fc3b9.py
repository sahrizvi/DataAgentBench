code = """import json
import re
import pandas as pd

# Load the large query results from the stored file paths
with open(var_call_7P2SmO3JNepcChWE4v7n0SIt, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_bBhY5e5laNPxozZ4Q5Fd8fiv, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Normalize rating in reviews to float
reviews_df = reviews_df[reviews_df['rating'].notnull()].copy()
reviews_df['rating'] = reviews_df['rating'].astype(float)

# Map purchase_id to book_id by replacing prefix 'purchaseid_' with 'bookid_' if possible
# Also try extracting numeric suffix and forming bookid_<num>

def map_purchase_to_book(purchase_id):
    if not isinstance(purchase_id, str):
        return None
    if purchase_id.startswith('purchaseid_'):
        return 'bookid_' + purchase_id.split('_',1)[1]
    # try extract digits
    m = re.search(r'(\d+)', purchase_id)
    if m:
        return 'bookid_' + m.group(1)
    return None

reviews_df['book_id'] = reviews_df['purchase_id'].apply(map_purchase_to_book)

# Keep only reviews that map to an existing book_id
book_ids_set = set(books_df['book_id'].astype(str))
reviews_df = reviews_df[reviews_df['book_id'].isin(book_ids_set)].copy()

# Extract publication year from books_df.details using regex for 4-digit years between 1500 and 2025

def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # find all 4-digit numbers
    years = re.findall(r'([1-2][0-9]{3})', detail)
    for y in years:
        try:
            yi = int(y)
            if 1500 <= yi <= 2025:
                return yi
        except:
            continue
    return None

books_df['year'] = books_df['details'].apply(extract_year)
# derive decade string
books_df['decade'] = books_df['year'].dropna().astype(int).apply(lambda y: f"{y//10*10}s")

# Merge reviews with books on book_id
merged = reviews_df.merge(books_df[['book_id','year','decade']], on='book_id', how='left')
# Drop rows without decade
merged = merged[merged['decade'].notnull()].copy()

# Group by decade: compute distinct books count and average rating (across reviews)
agg = merged.groupby('decade').agg(
    distinct_books=pd.NamedAgg(column='book_id', aggfunc=lambda x: x.nunique()),
    average_rating=pd.NamedAgg(column='rating', aggfunc='mean')
).reset_index()

# Filter decades with at least 10 distinct books
agg_filtered = agg[agg['distinct_books'] >= 10].copy()

if agg_filtered.empty:
    result = {'decade': None, 'average_rating': None, 'distinct_books': 0}
else:
    # find decade with highest average_rating; in tie, take highest average then most books then earliest decade
    agg_filtered = agg_filtered.sort_values(by=['average_rating','distinct_books','decade'], ascending=[False,False,True])
    top = agg_filtered.iloc[0]
    result = {
        'decade': str(top['decade']),
        'average_rating': round(float(top['average_rating']), 4),
        'distinct_books': int(top['distinct_books'])
    }

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_9bq6MMm72DLrgn96E7rVzzqe': ['books_info'], 'var_call_jFuu0jp2wCPqqYK2MWECgn8p': ['review'], 'var_call_7P2SmO3JNepcChWE4v7n0SIt': 'file_storage/call_7P2SmO3JNepcChWE4v7n0SIt.json', 'var_call_bBhY5e5laNPxozZ4Q5Fd8fiv': 'file_storage/call_bBhY5e5laNPxozZ4Q5Fd8fiv.json'}

exec(code, env_args)
