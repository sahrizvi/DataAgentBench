code = """import json
import pandas as pd
import re

# Load data from storage paths
with open(var_call_NVoEnkMvFVyDYFIhkNKQFyML, 'r') as f:
    books = json.load(f)
with open(var_call_yhdg6aG3UawDmz5sv6LZzVf5, 'r') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Clean reviews: ensure rating is numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Normalize purchase_id to book_id format: purchaseid_123 -> bookid_123
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Extract publication year from details in books
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    # find all 4-digit numbers
    matches = re.findall(r"\b(1[5-9][0-9]{2}|20[0-9]{2})\b", detail)
    for m in matches:
        try:
            y = int(m)
            if 1500 <= y <= 2023:
                return y
        except:
            continue
    return None

if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

# Compute per-book average rating from reviews (only for reviews that map to a book)
# Join reviews to books by book_id
# Some books in reviews may not have a corresponding books_info entry because of the LIMIT; keep only those that have pub_year

# Compute mean rating per book based on reviews
book_mean = df_reviews.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'mean_rating'})

# Merge with books to get publication year
df_book_ratings = pd.merge(book_mean, df_books[['book_id','pub_year']], on='book_id', how='left')

# Filter to books with a publication year
df_book_ratings = df_book_ratings[df_book_ratings['pub_year'].notna()].copy()

# Compute decade label
df_book_ratings['pub_year'] = df_book_ratings['pub_year'].astype(int)

def decade_label(y):
    return f"{(y//10)*10}s"

df_book_ratings['decade'] = df_book_ratings['pub_year'].apply(decade_label)

# Group by decade: count distinct books and average of book mean ratings
decade_grp = df_book_ratings.groupby('decade').agg(book_count=('book_id','nunique'), avg_book_rating=('mean_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
decade_filtered = decade_grp[decade_grp['book_count'] >= 10]

result = None
if not decade_filtered.empty:
    # find decade with highest avg_book_rating
    best = decade_filtered.sort_values(['avg_book_rating','book_count'], ascending=[False, False]).iloc[0]
    result = {'decade': best['decade'], 'avg_rating': round(float(best['avg_book_rating']), 4), 'book_count': int(best['book_count'])}
else:
    result = {'decade': None, 'avg_rating': None, 'book_count': 0}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_WjxSnom9ZZcw1f2zfM8y68hn': ['books_info'], 'var_call_Qgq3KUZEryaZofz9J0cBHUJB': ['review'], 'var_call_NVoEnkMvFVyDYFIhkNKQFyML': 'file_storage/call_NVoEnkMvFVyDYFIhkNKQFyML.json', 'var_call_yhdg6aG3UawDmz5sv6LZzVf5': 'file_storage/call_yhdg6aG3UawDmz5sv6LZzVf5.json'}

exec(code, env_args)
