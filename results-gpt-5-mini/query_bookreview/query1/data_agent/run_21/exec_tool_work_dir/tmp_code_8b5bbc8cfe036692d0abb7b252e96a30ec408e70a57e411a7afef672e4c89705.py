code = """import json
import pandas as pd
import re

# Load query results from storage variables
# var_call_7FJ9IMMgIMHkvLUrf4c303HD and var_call_Gj1sMenyHy1SfsivQvI5Vnz3 are available

# Determine if they are file paths or data
books_path = var_call_7FJ9IMMgIMHkvLUrf4c303HD
reviews_path = var_call_Gj1sMenyHy1SfsivQvI5Vnz3

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Clean review avg_rating
reviews_df['avg_rating'] = reviews_df['avg_rating'].astype(float)
# Map purchase_id to book_id by replacing prefix
reviews_df['book_id'] = reviews_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_')

# Extract year from details in books_df
def extract_year(text):
    if not isinstance(text, str):
        return None
    # find first 4-digit year between 1000 and 2099
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", text)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)

# Merge averaged reviews with books on book_id
merged = pd.merge(reviews_df[['book_id','avg_rating']], books_df[['book_id','title','year']], on='book_id', how='left')

# Keep only rows with year and avg_rating
merged = merged[merged['year'].notnull()].copy()
merged['year'] = merged['year'].astype(int)

# Compute decade label
merged['decade'] = merged['year'].apply(lambda y: f"{(y//10)*10}s")

# For each book there might be multiple review aggregates? reviews_df has one row per purchase_id so unique by book_id
# But ensure distinct books by book_id; group by book_id take first avg_rating (there should be one)
book_level = merged.drop_duplicates(subset=['book_id']).copy()

# Group by decade
grp = book_level.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('avg_rating','mean')).reset_index()

# Filter decades with at least 10 distinct books
eligible = grp[grp['num_books'] >= 10]

if eligible.empty:
    result = None
else:
    # Find decade with highest average rating; if tie, choose the one with more books then lexicographically
    max_avg = eligible['avg_rating'].max()
    candidates = eligible[eligible['avg_rating'] == max_avg].copy()
    if len(candidates) > 1:
        candidates = candidates.sort_values(by=['num_books','decade'], ascending=[False,True])
    best = candidates.iloc[0]
    result = best['decade']

# Print result in required format
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_FSwmNwxkbsM9XsVSeLxTynuU': ['books_info'], 'var_call_xNukcDXZlRQMiVAO8i7iK71g': ['review'], 'var_call_7FJ9IMMgIMHkvLUrf4c303HD': 'file_storage/call_7FJ9IMMgIMHkvLUrf4c303HD.json', 'var_call_Gj1sMenyHy1SfsivQvI5Vnz3': 'file_storage/call_Gj1sMenyHy1SfsivQvI5Vnz3.json'}

exec(code, env_args)
