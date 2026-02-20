code = """import json
import pandas as pd
import re

# Load data from storage-provided file paths
with open(var_call_OimII5j9k2tZ5HDcUn13uCBx, 'r') as f:
    books = json.load(f)

with open(var_call_KqPm25Nf38VUKTaY4xocMxJC, 'r') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize ratings
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Map purchase_id -> book_id by extracting number and prefixing with 'bookid_'
def map_purchase_to_book(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r'(\d+)', pid)
    if m:
        return f"bookid_{m.group(1)}"
    return None

df_reviews['book_id'] = df_reviews['purchase_id'].apply(map_purchase_to_book)

# Extract publication year from books.details
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    years = re.findall(r'(\d{4})', detail)
    for y in years:
        yi = int(y)
        if 1000 <= yi <= 2023:
            return yi
    return None

if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

# Compute per-book average rating using reviews
# Join reviews to books via book_id
# First, filter reviews with valid book_id and rating
df_reviews_valid = df_reviews.dropna(subset=['book_id', 'rating']).copy()

# Compute per-book mean rating and count of reviews
book_rating = df_reviews_valid.groupby('book_id')['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

# Merge with books to get publication year
books_with_ratings = pd.merge(book_rating, df_books[['book_id','pub_year']], on='book_id', how='left')

# Keep only books with a valid pub_year
books_with_ratings = books_with_ratings.dropna(subset=['pub_year']).copy()
books_with_ratings['pub_year'] = books_with_ratings['pub_year'].astype(int)

# Compute decade label
books_with_ratings['decade'] = books_with_ratings['pub_year'].floordiv(10).mul(10).astype(int).astype(str) + 's'

# For each decade compute number of distinct books and average of per-book avg_rating
decade_stats = books_with_ratings.groupby('decade').agg(
    books_count=('book_id','nunique'),
    decade_avg_rating=('avg_rating','mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['books_count'] >= 10].copy()

if eligible.empty:
    result = "No decade has at least 10 distinct rated books."
else:
    # Find decade with highest average rating; in tie, pick the decade with highest avg (first occurrence)
    best = eligible.sort_values(['decade_avg_rating','decade'], ascending=[False, True]).iloc[0]
    result = best['decade']

import json as _json
print("__RESULT__:")
print(_json.dumps(result))"""

env_args = {'var_call_OimII5j9k2tZ5HDcUn13uCBx': 'file_storage/call_OimII5j9k2tZ5HDcUn13uCBx.json', 'var_call_KqPm25Nf38VUKTaY4xocMxJC': 'file_storage/call_KqPm25Nf38VUKTaY4xocMxJC.json'}

exec(code, env_args)
