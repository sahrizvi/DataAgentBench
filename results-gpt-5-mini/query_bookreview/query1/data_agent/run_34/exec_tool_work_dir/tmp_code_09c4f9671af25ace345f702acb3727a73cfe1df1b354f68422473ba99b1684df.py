code = """import json
import pandas as pd
import re

def load_var(v):
    # if v is a string path, open it as json, else return directly
    if isinstance(v, str):
        try:
            with open(v, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            # maybe it's a plain string result
            return v
    return v

var_books = load_var(var_call_dOsYB2n2kr5V0l8bOLQxogDs)
var_reviews = load_var(var_call_CVeLRD8fUFwmEjPn3iCck5Wr)

df_books = pd.DataFrame(var_books)
df_reviews = pd.DataFrame(var_reviews)

# extract numeric id
df_books['num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)')
df_reviews['num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)')

# drop rows without numeric id
df_books = df_books[df_books['num'].notna()].copy()
df_reviews = df_reviews[df_reviews['num'].notna()].copy()

# convert to int
df_books['num'] = df_books['num'].astype(int)
df_reviews['num'] = df_reviews['num'].astype(int)

# convert rating to numeric
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

# join
df = df_reviews.merge(df_books[['book_id','details','num']], on='num', how='inner')

# extract year from details

def extract_year(s):
    if not isinstance(s, str):
        return None
    # find all 4-digit years
    years = re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", s)
    if not years:
        return None
    # take first and ensure <=2023
    for y in years:
        yint = int(y)
        if 1500 <= yint <= 2023:
            return yint
    return None

df['year'] = df['details'].apply(extract_year)
# drop rows without year
df = df[df['year'].notna()].copy()

# compute per-book average rating
book_avg = df.groupby(['book_id','year'], dropna=False)['rating'].mean().reset_index()
# compute decade label
book_avg['decade'] = (book_avg['year'] // 10 * 10).astype(int).astype(str) + 's'

# per-decade stats
decade_stats = book_avg.groupby('decade').agg(num_books=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()
# filter decades with at least 10 distinct books
cands = decade_stats[decade_stats['num_books'] >= 10].copy()

result = None
if not cands.empty:
    # find decade with highest average rating
    top = cands.loc[cands['avg_rating'].idxmax()]
    result = {
        'decade': top['decade'],
        'average_rating': round(float(top['avg_rating']), 4),
        'num_books': int(top['num_books'])
    }
else:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_qoq6xLoRpRaYiC9iitcBW3tT': ['books_info'], 'var_call_FMdczEQjaAmx0ogH4hcyKh3z': ['review'], 'var_call_dOsYB2n2kr5V0l8bOLQxogDs': 'file_storage/call_dOsYB2n2kr5V0l8bOLQxogDs.json', 'var_call_CVeLRD8fUFwmEjPn3iCck5Wr': 'file_storage/call_CVeLRD8fUFwmEjPn3iCck5Wr.json'}

exec(code, env_args)
