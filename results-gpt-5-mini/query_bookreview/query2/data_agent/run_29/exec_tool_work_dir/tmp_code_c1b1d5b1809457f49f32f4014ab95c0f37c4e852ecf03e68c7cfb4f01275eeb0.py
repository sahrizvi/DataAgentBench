code = """import json
import pandas as pd

# Load the query results from the provided storage file paths
books_path = var_call_Gwl29776B3spFUVJy0XOWR2s
reviews_path = var_call_d6tcXqfzwT750p14StHuVi0e

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Create DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize reviews: ensure rating numeric and map purchaseid_N -> bookid_N
# Some ratings may be strings; coerce to float
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = None

# Extract numeric suffix from purchase_id and build corresponding book_id
import re

def purchase_to_bookid(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r'_(\d+)$', pid)
    if m:
        return 'bookid_' + m.group(1)
    return None

df_reviews['book_id'] = df_reviews['purchase_id'].apply(purchase_to_bookid)

# Compute average rating and count per book_id
ratings = df_reviews.dropna(subset=['book_id', 'rating']).groupby('book_id').rating.agg(['mean','count']).reset_index()
ratings = ratings.rename(columns={'mean':'avg_rating','count':'rating_count'})

# Filter books for Literature & Fiction and English language
# categories and details are strings that may contain 'Literature & Fiction' and 'English'

def contains_lit_fic(cat):
    if not isinstance(cat, str):
        return False
    return 'literature & fiction' in cat.lower()

def contains_english(det):
    if not isinstance(det, str):
        return False
    return 'english' in det.lower()

if 'categories' not in df_books.columns:
    df_books['categories'] = ''
if 'details' not in df_books.columns:
    df_books['details'] = ''

df_books['is_lit_fic'] = df_books['categories'].apply(contains_lit_fic)
df_books['is_english'] = df_books['details'].apply(contains_english)

df_books_filtered = df_books[(df_books['is_lit_fic']) & (df_books['is_english'])]

# Merge with ratings
merged = pd.merge(df_books_filtered, ratings, on='book_id', how='left')

# Select those with perfect average rating of 5.0
# Use exact equality with tolerance
merged['avg_rating'] = pd.to_numeric(merged['avg_rating'], errors='coerce')
perfect = merged[merged['avg_rating'].notna() & (abs(merged['avg_rating'] - 5.0) < 1e-9)]

# Prepare output list of dicts
output = []
for _, row in perfect.iterrows():
    output.append({
        'book_id': row.get('book_id'),
        'title': row.get('title'),
        'author': row.get('author'),
        'avg_rating': float(row.get('avg_rating')),
        'rating_count': int(row.get('rating_count'))
    })

# Print result in required format as JSON string
print("__RESULT__:")
print(json.dumps(output))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json'}

exec(code, env_args)
