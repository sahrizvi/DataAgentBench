code = """import json
import pandas as pd
import re

# Load data from previous query results stored as files
with open(var_call_onTXloM0JQ8THyzHEIvSCvyL, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_i2r86ES2VKbfFW4QYqXV4VIQ, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Normalize columns
if 'book_id' not in df_books.columns:
    df_books['book_id'] = None
if 'details' not in df_books.columns:
    df_books['details'] = None

# Extract year from details
year_re = re.compile(r"\b(1[6-9]\d{2}|17\d{2}|18\d{2}|19\d{2}|20\d{2})\b")

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

df_books['year'] = df_books['details'].apply(extract_year)

# Extract numeric suffix from book_id and purchase_id
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    if m:
        return m.group(1)
    # fallback: any digits
    m2 = re.search(r'(\d+)', s)
    if m2:
        return m2.group(1)
    return None

df_books['num_id'] = df_books['book_id'].apply(extract_num_id)
df_reviews['num_id'] = df_reviews['purchase_id'].apply(extract_num_id)

# Convert ratings to numeric
if 'rating' in df_reviews.columns:
    df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
else:
    df_reviews['rating'] = None

# Drop rows without numeric id or rating
df_reviews = df_reviews.dropna(subset=['num_id','rating'])
df_books = df_books.dropna(subset=['num_id'])

# Merge on num_id
merged = pd.merge(df_reviews, df_books, on='num_id', how='inner', suffixes=('_rev','_book'))

# For each distinct book (by book_id), compute average rating and associated year
# Use book_id and year from books table
merged = merged[merged['year'].notna()]

if merged.empty:
    result = {"decade": None, "average_rating": None, "book_count": 0}
else:
    book_avg = merged.groupby('book_id').agg({'rating':'mean','year':'first'}).reset_index()
    # Compute decade label
    book_avg['decade_start'] = (book_avg['year'].astype(int) // 10) * 10
    book_avg['decade'] = book_avg['decade_start'].astype(int).astype(str) + 's'

    # Group by decade and consider decades with at least 10 distinct books
    dec_group = book_avg.groupby('decade').agg(book_count=('book_id','nunique'), average_rating=('rating','mean')).reset_index()
    dec_group = dec_group[dec_group['book_count'] >= 10]

    if dec_group.empty:
        result = {"decade": None, "average_rating": None, "book_count": 0}
    else:
        # Find decade with highest average_rating
        best = dec_group.sort_values(['average_rating','book_count'], ascending=[False, False]).iloc[0]
        result = {"decade": best['decade'], "average_rating": float(round(best['average_rating'],4)), "book_count": int(best['book_count'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_Ds69D7v9q73Ptqi0dt7mcxZm': ['books_info'], 'var_call_mhV3EIUYKkPOMykxiM8Sqmxy': ['review'], 'var_call_onTXloM0JQ8THyzHEIvSCvyL': 'file_storage/call_onTXloM0JQ8THyzHEIvSCvyL.json', 'var_call_i2r86ES2VKbfFW4QYqXV4VIQ': 'file_storage/call_i2r86ES2VKbfFW4QYqXV4VIQ.json'}

exec(code, env_args)
