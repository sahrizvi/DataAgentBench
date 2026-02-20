code = """import json
import pandas as pd
import re

# Load data from storage file paths
books_path = var_call_mgh9ob5dcKUeDO89uHrr4IUc
reviews_path = var_call_8c7MOoJAmwZLvXCKT3ZbfT1q

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Clean reviews: convert rating to float
reviews_df = reviews_df[reviews_df['rating'].notnull()].copy()
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df[reviews_df['rating'].notnull()]

# Map purchase_id to book_id by replacing prefix
reviews_df['book_id'] = reviews_df['purchase_id'].str.replace('purchaseid_', 'bookid_')

# Compute per-book average rating
book_ratings = reviews_df.groupby('book_id')['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

# Merge with books to get details
merged = pd.merge(book_ratings, books_df[['book_id','details']], on='book_id', how='left')

# Function to extract year from details
def extract_year(s):
    if not isinstance(s, str):
        return None
    # find all 4-digit numbers
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", s)
    if not years:
        return None
    # convert to int and filter reasonable range
    years_int = [int(y) for y in years if 1500 <= int(y) <= 2023]
    if not years_int:
        return None
    # choose the earliest year (min)
    return min(years_int)

merged['year'] = merged['details'].apply(extract_year)
merged = merged[merged['year'].notnull()].copy()
merged['year'] = merged['year'].astype(int)
merged['decade'] = merged['year'].floordiv(10).mul(10).astype(int).astype(str) + 's'

# Aggregate per-decade: average of book avg_ratings, and count distinct books
decade_stats = merged.groupby('decade').agg(book_count=('book_id','nunique'), decade_avg_rating=('avg_rating','mean')).reset_index()
# Filter decades with at least 10 distinct books
decade_stats = decade_stats[decade_stats['book_count'] >= 10]

result = None
if not decade_stats.empty:
    # pick decade with highest decade_avg_rating; tie-breaker: larger book_count, then earliest decade
    decade_stats = decade_stats.sort_values(by=['decade_avg_rating','book_count','decade'], ascending=[False, False, True])
    best = decade_stats.iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['decade_avg_rating']), 4),
        'book_count': int(best['book_count'])
    }
else:
    result = None

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_olewwEUuShxXJ2uEYtMawO89': ['books_info'], 'var_call_ZzgS1iTAYTwhiKjy61oq2Gth': ['review'], 'var_call_mgh9ob5dcKUeDO89uHrr4IUc': 'file_storage/call_mgh9ob5dcKUeDO89uHrr4IUc.json', 'var_call_8c7MOoJAmwZLvXCKT3ZbfT1q': 'file_storage/call_8c7MOoJAmwZLvXCKT3ZbfT1q.json'}

exec(code, env_args)
