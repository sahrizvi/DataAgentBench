code = """import json
import pandas as pd

# Load data from storage variables (file paths)
with open(var_call_VKUsLtEq541W58Eu1L2QIe1s, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_keA1DJWUxzozhhW8tSewqXho, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract year from details using regex
import re

def extract_year(text):
    if not isinstance(text, str):
        return None
    # find all 4-digit numbers
    matches = re.findall(r"(1[0-9]{3}|20[0-2][0-9]|2030)", text)
    # broader approach: also allow 19xx and 2000-2029 etc
    if not matches:
        # fallback generic 4-digit
        m2 = re.findall(r"(\d{4})", text)
        matches = m2
    for m in matches:
        try:
            y = int(m)
            if 1000 <= y <= 2023:
                return y
        except:
            continue
    return None

# Apply extraction
df_books['pub_year'] = df_books['details'].apply(extract_year)
# Create decade label
def year_to_decade(y):
    if pd.isna(y):
        return None
    return f"{int(y)//10*10}s"

df_books['decade'] = df_books['pub_year'].apply(year_to_decade)

# Map purchase_id to book_id by numeric suffix replacement
# e.g., purchaseid_186 -> bookid_186
if 'purchase_id' in df_reviews.columns:
    df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
else:
    df_reviews['book_id'] = None

# Convert rating to float
# Some ratings may be strings; coerce errors
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# Merge reviews with books on book_id
df_merged = df_reviews.merge(df_books[['book_id', 'decade']], on='book_id', how='left')

# Filter to rows with valid decade and rating
df_merged = df_merged[df_merged['decade'].notna() & df_merged['rating'].notna()]

# For distinct books counted per decade, consider unique book_ids that have at least one review
books_per_decade = df_merged.groupby('decade')['book_id'].nunique().reset_index().rename(columns={'book_id':'distinct_books_rated'})
# Compute average rating per decade (across all reviews)
avg_rating_per_decade = df_merged.groupby('decade')['rating'].mean().reset_index().rename(columns={'rating':'avg_rating'})

df_stats = books_per_decade.merge(avg_rating_per_decade, on='decade')
# Filter decades with at least 10 distinct books
df_stats = df_stats[df_stats['distinct_books_rated'] >= 10]

result = None
if not df_stats.empty:
    # find decade with highest avg_rating; if tie take the one with more books, then lexicographically
    df_stats = df_stats.sort_values(by=['avg_rating','distinct_books_rated'], ascending=[False, False])
    top = df_stats.iloc[0]
    result = {
        'decade': top['decade'],
        'avg_rating': round(float(top['avg_rating']), 4),
        'distinct_books_rated': int(top['distinct_books_rated'])
    }
else:
    result = None

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_xAJgSeuixCeU92RffivHYbL1': ['books_info'], 'var_call_VKUsLtEq541W58Eu1L2QIe1s': 'file_storage/call_VKUsLtEq541W58Eu1L2QIe1s.json', 'var_call_hBmQboQ9CfIABYm36kgjpRQK': ['review'], 'var_call_keA1DJWUxzozhhW8tSewqXho': 'file_storage/call_keA1DJWUxzozhhW8tSewqXho.json'}

exec(code, env_args)
