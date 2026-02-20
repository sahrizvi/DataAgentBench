code = """import json, re, pandas as pd

def load_result(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_result(var_call_UJRQALROpa3f6M7EDBOmQrPH)
reviews = load_result(var_call_U5Ytq4CTU1WQYXwBHz8o2zGO)

books_df = pd.DataFrame(books)
reviews_df = pd.DataFrame(reviews)

# extract first 4-digit year from details
year_re = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = year_re.search(s)
    return int(m.group(1)) if m else None

books_df['year'] = books_df['details'].map(extract_year)
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade_start'] = (books_df['year'] // 10) * 10
books_df['decade'] = books_df['decade_start'].astype(str) + 's'

# fuzzy join: bookid_123 <-> purchaseid_123 by numeric suffix
id_num_re = re.compile(r'(\d+)$')

def id_suffix(x):
    if not isinstance(x, str):
        return None
    m = id_num_re.search(x)
    return m.group(1) if m else None

books_df['id_suffix'] = books_df['book_id'].map(id_suffix)
reviews_df['id_suffix'] = reviews_df['purchase_id'].map(id_suffix)

reviews_df['rating'] = pd.to_numeric(reviews_df['rating'], errors='coerce')
reviews_df = reviews_df.dropna(subset=['rating','id_suffix'])

merged = reviews_df.merge(books_df[['id_suffix','decade','book_id']], on='id_suffix', how='inner')

# restrict to decades with at least 10 distinct books that have been rated
agg = merged.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('book_id', pd.Series.nunique)
).reset_index()
agg = agg[agg['distinct_books'] >= 10]

if len(agg)==0:
    out = {"decade": None, "reason": "No decade has at least 10 distinct rated books with extractable publication year."}
else:
    top = agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    out = {"decade": str(top['decade']), "avg_rating": float(top['avg_rating']), "distinct_books": int(top['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_UJRQALROpa3f6M7EDBOmQrPH': 'file_storage/call_UJRQALROpa3f6M7EDBOmQrPH.json', 'var_call_U5Ytq4CTU1WQYXwBHz8o2zGO': 'file_storage/call_U5Ytq4CTU1WQYXwBHz8o2zGO.json'}

exec(code, env_args)
