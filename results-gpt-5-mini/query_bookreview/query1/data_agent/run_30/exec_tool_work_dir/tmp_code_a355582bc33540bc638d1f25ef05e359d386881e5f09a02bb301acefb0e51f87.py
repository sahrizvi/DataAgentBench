code = """import json,re
import pandas as pd

# Load data from previous tool outputs (file paths are provided in these variables)
with open(var_call_tPb7ZoB5VeuBJu4tQ3yrxhcL, 'r') as f:
    reviews = json.load(f)
with open(var_call_ZT3UXpy2cYHNPKX7PkprxNoh, 'r') as f:
    books = json.load(f)

# Reviews dataframe
df_r = pd.DataFrame(reviews)
# Ensure rating numeric
df_r['rating'] = pd.to_numeric(df_r.get('rating', []), errors='coerce')
# Map purchase_id -> book_id by replacing prefix
if 'purchase_id' in df_r.columns:
    df_r['book_id'] = df_r['purchase_id'].str.replace('purchaseid_', 'bookid_', regex=False)
else:
    df_r['book_id'] = None

# Compute per-book average rating
book_avg = df_r.groupby('book_id', as_index=False)['rating'].mean().rename(columns={'rating': 'avg_rating'})

# Books dataframe
df_b = pd.DataFrame(books)

# Function to extract year from details text
year_re = re.compile(r"\b(17|18|19|20)\d{2}\b")

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = year_re.search(s)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

if 'details' in df_b.columns:
    df_b['year'] = df_b['details'].apply(extract_year)
else:
    df_b['year'] = None

# Keep only books with a detected year
df_b = df_b[df_b['year'].notnull()]

# Merge per-book averages with book years
df = pd.merge(book_avg, df_b[['book_id', 'year']], on='book_id', how='inner')
# Drop any missing avg_rating
df = df[df['avg_rating'].notnull()]

# Compute decade label
df['decade'] = (df['year'] // 10 * 10).astype(int).astype(str) + 's'

# Aggregate by decade: number of distinct books and average of book average ratings
decade_stats = df.groupby('decade').agg(book_count=('book_id', 'nunique'), avg_rating=('avg_rating', 'mean')).reset_index()
# Filter decades with at least 10 distinct books
decade_stats = decade_stats[decade_stats['book_count'] >= 10]

import math
if decade_stats.empty:
    result_obj = {"decade": None, "average_rating": None, "book_count": 0}
else:
    best = decade_stats.sort_values(['avg_rating', 'decade'], ascending=[False, True]).iloc[0]
    result_obj = {"decade": best['decade'], "average_rating": round(float(best['avg_rating']), 4), "book_count": int(best['book_count'])}

result = json.dumps(result_obj)
print("__RESULT__:")
print(result)"""

env_args = {'var_call_F9BpyJDbnHTDLykTiWqkUNrM': ['books_info'], 'var_call_5pvvj2WxGaL3AaZiJUctYr2I': ['review'], 'var_call_tPb7ZoB5VeuBJu4tQ3yrxhcL': 'file_storage/call_tPb7ZoB5VeuBJu4tQ3yrxhcL.json', 'var_call_ZT3UXpy2cYHNPKX7PkprxNoh': 'file_storage/call_ZT3UXpy2cYHNPKX7PkprxNoh.json'}

exec(code, env_args)
