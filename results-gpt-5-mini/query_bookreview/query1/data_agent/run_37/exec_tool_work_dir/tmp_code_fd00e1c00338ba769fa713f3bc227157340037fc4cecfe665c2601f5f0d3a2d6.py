code = """import json
import pandas as pd
import re

# Load data from storage variables
books_path = var_call_0obRIXKOWqtuchR2OVJHvKU7
reviews_path = var_call_IuGPOjM1WdkWZ5XslbM99Ftx

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Ensure columns exist
# Extract numeric id suffix from book_id and purchase_id
def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)$", s)
    return m.group(1) if m else None

df_books['id_num'] = df_books['book_id'].apply(extract_num)
df_reviews['id_num'] = df_reviews['purchase_id'].apply(extract_num)

# Extract year from details using regex (first occurrence)
def extract_year(detail):
    if not isinstance(detail, str):
        return None
    m = re.search(r"\b(1[0-9]{3}|20[0-2][0-9])\b", detail)
    return int(m.group(0)) if m else None

# Some books may have publication info also in categories or title, try details first
if 'details' in df_books.columns:
    df_books['pub_year'] = df_books['details'].apply(extract_year)
else:
    df_books['pub_year'] = None

# Drop rows without numeric id or pub_year
df_books = df_books[df_books['id_num'].notnull()]
# Keep books even if pub_year missing for now but we'll drop later

# Convert rating to float
# Some ratings are strings; convert safely

def to_float(x):
    try:
        return float(x)
    except:
        return None

if 'rating' in df_reviews.columns:
    df_reviews['rating_f'] = df_reviews['rating'].apply(to_float)
else:
    df_reviews['rating_f'] = None

# Merge reviews with books on id_num
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))

# Keep rows with a publication year and a rating
merged = merged[merged['pub_year'].notnull() & merged['rating_f'].notnull()]

# Compute per-book average rating
per_book = merged.groupby('book_id').agg({
    'rating_f':'mean',
    'pub_year':'first'
}).reset_index().rename(columns={'rating_f':'avg_rating'})

# Compute decade string
per_book['decade_start'] = (per_book['pub_year'].astype(int) // 10) * 10
per_book['decade'] = per_book['decade_start'].astype(str) + 's'

# Compute per-decade average of book-level averages and distinct book counts
decade_stats = per_book.groupby('decade').agg(
    decade_avg_rating = ('avg_rating', 'mean'),
    book_count = ('book_id', 'nunique')
).reset_index()

# Filter decades with at least 10 distinct books
decade_stats_filtered = decade_stats[decade_stats['book_count'] >= 10]

# If no decades meet threshold, return None
if decade_stats_filtered.empty:
    result = {'decade': None, 'average_rating': None, 'book_count': 0}
else:
    # Find decade with highest average rating; in tie take the one with most books then smallest decade
    best = decade_stats_filtered.sort_values(
        by=['decade_avg_rating','book_count','decade'],
        ascending=[False, False, True]
    ).iloc[0]
    result = {
        'decade': best['decade'],
        'average_rating': round(float(best['decade_avg_rating']), 4),
        'book_count': int(best['book_count'])
    }

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_JzElwp0nBhaFszYaTyRXQASr': ['books_info'], 'var_call_HQx3OeaNbloAEYAsG6o5rLqr': ['review'], 'var_call_0obRIXKOWqtuchR2OVJHvKU7': 'file_storage/call_0obRIXKOWqtuchR2OVJHvKU7.json', 'var_call_IuGPOjM1WdkWZ5XslbM99Ftx': 'file_storage/call_IuGPOjM1WdkWZ5XslbM99Ftx.json'}

exec(code, env_args)
