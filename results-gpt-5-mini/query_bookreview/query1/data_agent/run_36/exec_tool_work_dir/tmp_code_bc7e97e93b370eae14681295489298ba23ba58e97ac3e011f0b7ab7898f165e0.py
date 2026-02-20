code = """import pandas as pd
import json
import re

# Load data from provided storage file paths
books_path = var_call_ubiAjTGaPeAApREZF4pbINoZ
reviews_path = var_call_DV3mCUoQAsq8CUOHOlNaUlS5

books = pd.read_json(books_path)
reviews = pd.read_json(reviews_path)

# Normalize column names
books = books[['book_id', 'details']].drop_duplicates(subset=['book_id'])
reviews = reviews[['purchase_id', 'rating']]

# Extract numeric id from book_id and purchase_id
books['id_num'] = books['book_id'].astype(str).str.extract(r'(\d+)$', expand=False)
reviews['id_num'] = reviews['purchase_id'].astype(str).str.extract(r'(\d+)$', expand=False)

# Drop rows where id_num is missing
books = books[books['id_num'].notna()].copy()
reviews = reviews[reviews['id_num'].notna()].copy()

books['id_num'] = books['id_num'].astype(int)
reviews['id_num'] = reviews['id_num'].astype(int)

# Convert ratings to numeric
reviews['rating'] = pd.to_numeric(reviews['rating'], errors='coerce')
reviews = reviews[reviews['rating'].notna()].copy()

# Merge reviews with books on id_num to get publication details
merged = reviews.merge(books, on='id_num', how='left', suffixes=('_rev','_book'))

# Function to extract year from details
year_re = re.compile(r"(?<!\d)(1[5-9]\d{2}|20[0-2]\d|2023)(?!\d)")

def extract_year(text):
    if not isinstance(text, str):
        return None
    m = year_re.search(text)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

merged['year'] = merged['details'].apply(extract_year)

# Drop rows without year
merged = merged[merged['year'].notna()].copy()
merged['year'] = merged['year'].astype(int)

# Compute per-book average rating (across its reviews)
book_stats = merged.groupby(['id_num','book_id','year'], as_index=False).agg(
    book_avg_rating = ('rating','mean'),
    review_count = ('rating','count')
)

# Compute decade label
book_stats['decade_start'] = (book_stats['year'] // 10) * 10
book_stats['decade'] = book_stats['decade_start'].astype(int).astype(str) + 's'

# For each decade, consider distinct books (book_stats rows are per book)
decade_stats = book_stats.groupby('decade', as_index=False).agg(
    books_count = ('book_id','nunique'),
    decade_avg = ('book_avg_rating','mean')
)

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['books_count'] >= 10].copy()

# If no eligible decades, return None
if eligible.empty:
    result = None
else:
    # Find decade with highest average rating; if tie, take the one with highest avg then any
    best_row = eligible.sort_values(['decade_avg','decade'], ascending=[False, True]).iloc[0]
    result = best_row['decade']

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_a6DElWwDlywpenRqcQVcMr2l': ['books_info'], 'var_call_0cCfFhQGuCDa7c2lrjSrf8l1': ['review'], 'var_call_ubiAjTGaPeAApREZF4pbINoZ': 'file_storage/call_ubiAjTGaPeAApREZF4pbINoZ.json', 'var_call_DV3mCUoQAsq8CUOHOlNaUlS5': 'file_storage/call_DV3mCUoQAsq8CUOHOlNaUlS5.json'}

exec(code, env_args)
