code = """import json
import pandas as pd
import re

# Load the query results from storage file paths
books_path = var_call_ywfWlhaEjWqgVCdI3tyPhrMx
reviews_path = var_call_LJElszQ2DuGKJXeywwtRzGEW

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract numeric id from book_id and purchase_id
df_books['book_num'] = df_books['book_id'].astype(str).str.extract(r"(\d+)")
df_reviews['book_num'] = df_reviews['purchase_id'].astype(str).str.extract(r"(\d+)")

# Drop rows without numeric id
df_books = df_books[df_books['book_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['book_num'].notna()].copy()

# Convert to int for join
df_books['book_num'] = df_books['book_num'].astype(int)
df_reviews['book_num'] = df_reviews['book_num'].astype(int)

# Extract publication year from details (first occurrence of 19xx or 20xx)
def extract_year(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"\b(19|20)\d{2}\b", s)
    if m:
        return int(m.group(0))
    return None

df_books['pub_year'] = df_books['details'].apply(extract_year)
# Drop books without a publication year
df_books = df_books[df_books['pub_year'].notna()].copy()

def year_to_decade(y):
    y = int(y)
    decade = (y // 10) * 10
    return f"{decade}s"

df_books['decade'] = df_books['pub_year'].apply(year_to_decade)

# Clean ratings and convert to float
# Some ratings may be strings like "4"; coerce errors
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Drop reviews without rating
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

# Merge reviews with books on numeric id
merged = pd.merge(df_reviews, df_books, on='book_num', how='inner', suffixes=('_rev', '_book'))

# Now compute per-book average rating and associated decade
per_book = merged.groupby(['book_num', 'book_id', 'decade'], as_index=False)['rating'].mean()
per_book = per_book.rename(columns={'rating': 'avg_rating'})

# Compute number of distinct books per decade and average of per-book averages
decade_stats = per_book.groupby('decade').agg(
    num_books=('book_id', 'nunique'),
    mean_of_book_avgs=('avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = decade_stats[decade_stats['num_books'] >= 10].copy()

if eligible.empty:
    result = None
else:
    # Find decade with highest mean_of_book_avgs
    best_row = eligible.loc[eligible['mean_of_book_avgs'].idxmax()]
    result = {
        'decade': best_row['decade'],
        'average_rating': round(float(best_row['mean_of_book_avgs']), 4),
        'num_books': int(best_row['num_books'])
    }

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_4LszRktKDlz6Xx2RyChTbvWN': ['books_info'], 'var_call_6vlS6UJUOhp7xO9lN4DKuoda': ['review'], 'var_call_ywfWlhaEjWqgVCdI3tyPhrMx': 'file_storage/call_ywfWlhaEjWqgVCdI3tyPhrMx.json', 'var_call_LJElszQ2DuGKJXeywwtRzGEW': 'file_storage/call_LJElszQ2DuGKJXeywwtRzGEW.json'}

exec(code, env_args)
