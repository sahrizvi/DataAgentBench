code = """import json
import re
import pandas as pd

# Load data from storage file paths
books_path = var_call_Zj8yKwYRbRsCgNcVmijtPaTc
reviews_path = var_call_CpfnhHR6EUPJlSUcPHuAHqvK

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract year from details using regex for 4-digit years
def extract_year(text):
    if not isinstance(text, str):
        return None
    years = re.findall(r"\b(\d{4})\b", text)
    for y in years:
        yi = int(y)
        if 1500 <= yi <= 2023:
            return yi
    return None

books_df['year'] = books_df['details'].apply(extract_year)
books_df['decade'] = books_df['year'].apply(lambda y: f"{(y//10)*10}s" if pd.notnull(y) else None)

# Normalize ratings in reviews
# Some ratings may be strings; coerce to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
# Map purchase_id to book_id by replacing prefix
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Compute per-book average rating
book_avg = reviews_df.groupby('book_id', dropna=True)['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

# Join with books to get decade
merged = pd.merge(book_avg, books_df[['book_id','decade']], on='book_id', how='left')

# Keep only books with known decade
merged = merged[merged['decade'].notna()]

# For each decade, count distinct books and compute average of book average ratings
decade_stats = merged.groupby('decade').agg(num_books=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10]

if eligible.empty:
    result = 'No decade has at least 10 distinct rated books.'
else:
    # Find decade with highest average rating; if tie, choose the one with more books, then earliest decade
    best = eligible.sort_values(['decade_avg_rating','num_books'], ascending=[False,False]).iloc[0]
    result = best['decade']

# Print result in required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_WFM4a4mO1u1oUwDKxN3pHU4v': ['books_info'], 'var_call_Zj8yKwYRbRsCgNcVmijtPaTc': 'file_storage/call_Zj8yKwYRbRsCgNcVmijtPaTc.json', 'var_call_zDjqcyji5fYMtuED9ELxiQ53': ['review'], 'var_call_CpfnhHR6EUPJlSUcPHuAHqvK': 'file_storage/call_CpfnhHR6EUPJlSUcPHuAHqvK.json'}

exec(code, env_args)
