code = """import json
import pandas as pd
import re

# Load data from previous query results stored as file paths
with open(var_call_oRLfpblvuHnbxMglsJqCCWkA, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_sCFbDngcG7GfjvdhqwmavrrK, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Clean and convert ratings
reviews_df = reviews_df.dropna(subset=['purchase_id', 'rating']).copy()
# ratings may be strings like "4" or "4.0"
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating'])

# Map purchase_id -> book_id by extracting digits and prefixing with 'bookid_'
def purchase_to_book(purchase_id):
    m = re.search(r"(\d+)", str(purchase_id))
    if not m:
        return None
    return f"bookid_{m.group(1)}"

reviews_df['book_id'] = reviews_df['purchase_id'].apply(purchase_to_book)
reviews_df = reviews_df.dropna(subset=['book_id'])

# Compute per-book average rating
book_avg = reviews_df.groupby('book_id', as_index=False)['rating'].mean()
book_avg.rename(columns={'rating': 'avg_rating'}, inplace=True)

# Extract year from books.details
def extract_year(details):
    if not isinstance(details, str):
        return None
    # find all 4-digit numbers
    years = re.findall(r"(\d{4})", details)
    if not years:
        return None
    # choose first plausible year between 1000 and 2023
    for y in years:
        yi = int(y)
        if 1000 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_df = books_df.dropna(subset=['book_id'])

# Merge book_avg with books to get year
merged = pd.merge(book_avg, books_df[['book_id', 'year']], on='book_id', how='left')
merged = merged.dropna(subset=['year'])
merged['year'] = merged['year'].astype(int)
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(str) + 's'

# For each decade, compute number of distinct books and average of book avg_ratings
decade_stats = merged.groupby('decade').agg(books_count=('book_id', 'nunique'),
                                             decade_avg_rating=('avg_rating', 'mean')).reset_index()

# Filter decades with at least 10 distinct books
valid_decades = decade_stats[decade_stats['books_count'] >= 10].copy()

result = None
if valid_decades.empty:
    result = {'decade': None, 'average_rating': None, 'books_count': 0}
else:
    # find decade with highest average rating; if tie, choose the one with more books, then earliest decade
    valid_decades = valid_decades.sort_values(by=['decade_avg_rating', 'books_count', 'decade'],
                                              ascending=[False, False, True])
    top = valid_decades.iloc[0]
    result = {'decade': top['decade'], 'average_rating': round(float(top['decade_avg_rating']), 4), 'books_count': int(top['books_count'])}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_TRKc0E15yTRdJu4kI3GPt0Kx': ['books_info'], 'var_call_Vat6wUfUBzIBCEpK5De8PZLo': ['review'], 'var_call_oRLfpblvuHnbxMglsJqCCWkA': 'file_storage/call_oRLfpblvuHnbxMglsJqCCWkA.json', 'var_call_sCFbDngcG7GfjvdhqwmavrrK': 'file_storage/call_sCFbDngcG7GfjvdhqwmavrrK.json'}

exec(code, env_args)
