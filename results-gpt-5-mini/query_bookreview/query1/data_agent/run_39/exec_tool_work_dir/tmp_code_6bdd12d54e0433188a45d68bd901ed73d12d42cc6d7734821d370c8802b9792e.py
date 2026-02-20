code = """import json
import re
import pandas as pd

# Load data from previous tool results
with open(var_call_wH4Hl9v9HJaphYQUk8Ctw6wN, 'r', encoding='utf-8') as f:
    review_aggs = json.load(f)
with open(var_call_V6AnT36wTL1cNBXWgaG8OkF5, 'r', encoding='utf-8') as f:
    books = json.load(f)

# Create DataFrames
df_rev = pd.DataFrame(review_aggs)
df_books = pd.DataFrame(books)

# Convert avg_rating to float
df_rev['avg_rating'] = df_rev['avg_rating'].astype(float)

# Map purchase_id to book_id by replacing prefix
# Some purchase_id may already match bookid pattern; handle safely
def purchase_to_book(pid):
    if pd.isna(pid):
        return pid
    return pid.replace('purchaseid_', 'bookid_')

df_rev['book_id'] = df_rev['purchase_id'].apply(purchase_to_book)

# Function to extract publication year from details
def extract_year(details):
    if not isinstance(details, str):
        return None
    # try to find year after 'published' keyword
    m = re.search(r'published[^\d]{0,50}?(\d{4})', details, flags=re.I)
    if m:
        y = int(m.group(1))
        if 1500 <= y <= 2023:
            return y
    # fallback: find any 4-digit year in plausible range
    allyears = re.findall(r'\b(\d{4})\b', details)
    for ys in allyears:
        y = int(ys)
        if 1500 <= y <= 2023:
            return y
    return None

# Extract years for books
df_books['year'] = df_books['details'].apply(extract_year)

# Merge on book_id
merged = pd.merge(df_rev, df_books[['book_id','title','year']], on='book_id', how='inner')

# Keep rows with a valid year
merged = merged[merged['year'].notna()].copy()
merged['year'] = merged['year'].astype(int)

# Compute decade string
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype(str) + 's'

# For each distinct book (book_id), we have avg_rating already. Group by decade across distinct books.
books_per_decade = merged.groupby('decade').agg(
    num_books=('book_id', lambda x: x.nunique()),
    avg_rating=('avg_rating', 'mean')
).reset_index()

# Filter decades with at least 10 distinct books
eligible = books_per_decade[books_per_decade['num_books'] >= 10].copy()

result = None
if not eligible.empty:
    # find decade with highest average rating
    best = eligible.sort_values(['avg_rating','num_books'], ascending=[False, False]).iloc[0]
    result = {
        'decade': best['decade'],
        'avg_rating': round(float(best['avg_rating']), 4),
        'num_books': int(best['num_books'])
    }
else:
    result = {'decade': None, 'avg_rating': None, 'num_books': 0}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_wH4Hl9v9HJaphYQUk8Ctw6wN': 'file_storage/call_wH4Hl9v9HJaphYQUk8Ctw6wN.json', 'var_call_ZhDl5Ukh9lwtVtRdoSBT8Bw7': ['books_info'], 'var_call_V6AnT36wTL1cNBXWgaG8OkF5': 'file_storage/call_V6AnT36wTL1cNBXWgaG8OkF5.json'}

exec(code, env_args)
