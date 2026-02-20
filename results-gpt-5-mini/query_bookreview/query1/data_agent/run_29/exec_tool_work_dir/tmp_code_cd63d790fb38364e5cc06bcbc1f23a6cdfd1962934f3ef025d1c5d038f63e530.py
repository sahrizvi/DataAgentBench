code = """import json
import pandas as pd
import re
with open(var_call_fCXKjFuQR0KVnKs5USPd527y,'r',encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_0WiZXUQS5sLYvZ5ccFLAWezZ,'r',encoding='utf-8') as f:
    reviews = json.load(f)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract numeric id
df_books['id_num'] = df_books['book_id'].astype(str).str.extract(r'(\d+)')
df_reviews['id_num'] = df_reviews['purchase_id'].astype(str).str.extract(r'(\d+)')
# Drop rows without numeric ids
df_books = df_books[df_books['id_num'].notna()].copy()
df_reviews = df_reviews[df_reviews['id_num'].notna()].copy()
# convert to int
df_books['id_num'] = df_books['id_num'].astype(int)
df_reviews['id_num'] = df_reviews['id_num'].astype(int)

# Extract publication year from details (first valid year between 1800 and 2023)
year_re = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    matches = year_re.findall(text)
    if not matches:
        return None
    for m in matches:
        try:
            y = int(m)
            if 1800 <= y <= 2023:
                return y
        except:
            continue
    return None

df_books['pub_year'] = df_books['details'].apply(extract_year)
# Drop books without pub_year
df_books = df_books[df_books['pub_year'].notna()].copy()
df_books['pub_year'] = df_books['pub_year'].astype(int)
# Create decade label
df_books['decade'] = (df_books['pub_year'] // 10 * 10).astype(int).astype(str) + 's'

# Clean ratings
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews[df_reviews['rating'].notna()].copy()

# Merge
merged = pd.merge(df_reviews, df_books, on='id_num', how='inner', suffixes=('_rev','_book'))

if merged.empty:
    out = {"error": "No matched reviews and books after join."}
    print('__RESULT__:')
    print(json.dumps(out))
else:
    # Compute per-book average rating
    book_avg = merged.groupby(['book_id','decade'], as_index=False)['rating'].mean()
    # Per-decade stats
    per_decade = book_avg.groupby('decade', as_index=False).agg(book_count=('book_id','nunique'), average_rating=('rating','mean'))
    # Filter decades with at least 10 distinct books
    per_decade = per_decade[per_decade['book_count'] >= 10].copy()
    if per_decade.empty:
        out = {"error": "No decade has at least 10 distinct rated books."}
        print('__RESULT__:')
        print(json.dumps(out))
    else:
        # choose decade with highest average_rating, tie-breaker by decade ascending
        per_decade = per_decade.sort_values(['average_rating','decade'], ascending=[False, True]).reset_index(drop=True)
        best = per_decade.iloc[0]
        out = {"decade": str(best['decade']), "average_rating": round(float(best['average_rating']),4), "book_count": int(best['book_count'])}
        print('__RESULT__:')
        print(json.dumps(out))"""

env_args = {'var_call_igXNZFokW0Vgy87s2Yc02xki': ['books_info'], 'var_call_WvRkgUDcO28qseDky23cQ2B6': ['review'], 'var_call_fCXKjFuQR0KVnKs5USPd527y': 'file_storage/call_fCXKjFuQR0KVnKs5USPd527y.json', 'var_call_0WiZXUQS5sLYvZ5ccFLAWezZ': 'file_storage/call_0WiZXUQS5sLYvZ5ccFLAWezZ.json', 'var_call_aR6UX9hpPPFJp9mKhHqshRo4': {'error': 'No matched reviews and books after fuzzy numeric id join.'}, 'var_call_kZWI5G5YvvZNgvtJ34upADAx': {'books_total': 200, 'reviews_total': 1833, 'books_with_num': 200, 'reviews_with_num': 200, 'books_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'reviews_num_min_max_sample': [1, 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], 'intersection_count': 200, 'sample_book_ids': ['bookid_1', 'bookid_2', 'bookid_3', 'bookid_4', 'bookid_5', 'bookid_6', 'bookid_7', 'bookid_8', 'bookid_9', 'bookid_10', 'bookid_11', 'bookid_12', 'bookid_13', 'bookid_14', 'bookid_15', 'bookid_16', 'bookid_17', 'bookid_18', 'bookid_19', 'bookid_20'], 'sample_purchase_ids': ['purchaseid_186', 'purchaseid_191', 'purchaseid_190', 'purchaseid_8', 'purchaseid_178', 'purchaseid_76', 'purchaseid_115', 'purchaseid_167', 'purchaseid_188', 'purchaseid_23', 'purchaseid_196', 'purchaseid_3', 'purchaseid_48', 'purchaseid_154', 'purchaseid_99', 'purchaseid_169', 'purchaseid_145', 'purchaseid_194', 'purchaseid_81', 'purchaseid_199']}}

exec(code, env_args)
