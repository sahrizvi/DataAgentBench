code = """import pandas as pd
import json
import re

# Load data from storage variables (file paths)
def load_storage(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    else:
        return pd.DataFrame(var)

df_books = load_storage(var_call_UK6PjG5FNGy5ZnCSpyQ0HyhS)
df_reviews = load_storage(var_call_c3ph57AaYefZWOncbLX8fx91)

# Clean and prepare
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
# Map purchase_id to book_id by replacing prefix
df_reviews['book_id'] = df_reviews['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

# Compute per-book mean rating (consider only books with at least one rating)
book_mean = df_reviews.groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating': 'mean_rating'})

# Merge with books_info to get publication details
if 'details' not in df_books.columns:
    df_books['details'] = None

df_merged = pd.merge(book_mean, df_books[['book_id', 'details']], on='book_id', how='inner')

# Extract year from details text

def extract_year(s):
    if not isinstance(s, str):
        return None
    # Prefer a reasonable year between 1000 and 2023
    m = re.search(r"(1[0-9]{3}|20[0-9]{2}|17[0-9]{2}|18[0-9]{2})", s)
    if m:
        try:
            y = int(m.group(0))
            if 1000 <= y <= 2023:
                return y
        except:
            return None
    # fallback any 4-digit
    m2 = re.search(r"(\d{4})", s)
    if m2:
        try:
            y = int(m2.group(0))
            if 1000 <= y <= 2023:
                return y
        except:
            return None
    return None

df_merged['year'] = df_merged['details'].apply(extract_year)
# Drop if year not found
df_merged = df_merged.dropna(subset=['year'])
# Compute decade label
df_merged['decade'] = (df_merged['year'].astype(int) // 10 * 10).astype(int).astype(str) + 's'

# Group by decade: count distinct books and average of book mean ratings
grp = df_merged.groupby('decade').agg(num_books=('book_id', 'nunique'), avg_book_rating=('mean_rating', 'mean')).reset_index()
# Filter decades with at least 10 distinct books
grp2 = grp[grp['num_books'] >= 10]

if grp2.empty:
    result = {'decade': None, 'avg_rating': None, 'num_books': 0}
else:
    best = grp2.loc[grp2['avg_book_rating'].idxmax()]
    result = {'decade': best['decade'], 'avg_rating': round(float(best['avg_book_rating']), 4), 'num_books': int(best['num_books'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_1nJNQ6C9d9kuLO0Z8hYYb9tf': ['books_info'], 'var_call_UK6PjG5FNGy5ZnCSpyQ0HyhS': 'file_storage/call_UK6PjG5FNGy5ZnCSpyQ0HyhS.json', 'var_call_gzprLoJnV0hQMtGoowtY5lSJ': ['review'], 'var_call_c3ph57AaYefZWOncbLX8fx91': 'file_storage/call_c3ph57AaYefZWOncbLX8fx91.json'}

exec(code, env_args)
