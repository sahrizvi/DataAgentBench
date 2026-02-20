code = """import json
import re
import pandas as pd

# Load the query results from storage files
books_path = var_call_aE85BI9zBOhyeuQ3cn2Y2xGr
reviews_path = var_call_Ho9UE0URx5HbmwVUOrnTHfxb

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# Extract numeric suffix from ids
books_df['id_num'] = books_df['book_id'].astype(str).str.extract(r'(\d+)$')
reviews_df['id_num'] = reviews_df['purchase_id'].astype(str).str.extract(r'(\d+)$')

# Convert ratings to numeric
reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')

# Extract year from details using regex (capture 4-digit years 1500-2029-ish)
def extract_year(text):
    if not isinstance(text, str):
        return None
    m = re.search(r'(1[5-9]\d{2}|20\d{2})', text)
    if m:
        try:
            y = int(m.group(0))
            return y
        except:
            return None
    return None

books_df['year'] = books_df['details'].apply(extract_year)

# Drop rows without numeric id or year for books
books_df = books_df[books_df['id_num'].notna()]
books_df = books_df[books_df['year'].notna()]
books_df['id_num'] = books_df['id_num'].astype(int)
books_df['year'] = books_df['year'].astype(int)

# Reviews: drop without numeric id or rating
reviews_df = reviews_df[reviews_df['id_num'].notna()]
reviews_df['id_num'] = reviews_df['id_num'].astype(int)
reviews_df = reviews_df[reviews_df['rating'].notna()]

# Compute per-book average rating (only for books present in books_df)
# Join reviews to books on id_num
merged = pd.merge(reviews_df, books_df[['id_num','book_id','title','year']], on='id_num', how='inner')

# For each distinct book (book_id) compute mean rating
book_avg = merged.groupby(['book_id','id_num','title','year'], as_index=False)['rating'].mean()
book_avg.rename(columns={'rating':'avg_rating'}, inplace=True)

# Compute decade label
book_avg['decade_start'] = (book_avg['year'] // 10) * 10
book_avg['decade'] = book_avg['decade_start'].astype(str) + 's'

# For each decade, consider only decades with at least 10 distinct books
decade_stats = book_avg.groupby('decade').agg(num_books=('book_id','nunique'),
                                                 mean_of_book_avgs=('avg_rating','mean')).reset_index()
eligible = decade_stats[decade_stats['num_books'] >= 10]

# If no eligible decades, return None
if eligible.empty:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}
else:
    # pick decade with highest mean_of_book_avgs
    top = eligible.sort_values(['mean_of_book_avgs','decade'], ascending=[False, True]).iloc[0]
    result = {'decade': top['decade'], 'average_rating': round(float(top['mean_of_book_avgs']),4), 'num_books': int(top['num_books'])}

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_dgAN3tt4OLzFzGSofQtfaMlA': ['books_info'], 'var_call_aE85BI9zBOhyeuQ3cn2Y2xGr': 'file_storage/call_aE85BI9zBOhyeuQ3cn2Y2xGr.json', 'var_call_N38VPIerwWBBWxh2KmnaaD4A': ['review'], 'var_call_Ho9UE0URx5HbmwVUOrnTHfxb': 'file_storage/call_Ho9UE0URx5HbmwVUOrnTHfxb.json'}

exec(code, env_args)
