code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_itAmERabVqYVODFMyamnyj4d)
reviews = load_records(var_call_IaPadoEfCtbfuMTF6UfrdZlE)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

def extract_year(details):
    if not isinstance(details, str):
        return None
    m = re.search(r'\b(?:19|20)\d{2}\b', details)
    return int(m.group(0)) if m else None

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year'])
# Map purchaseid_123 -> bookid_123

def pid_to_bid(pid):
    if not isinstance(pid, str):
        return None
    m = re.search(r'(\d+)$', pid)
    return f"bookid_{m.group(1)}" if m else None

df_reviews['book_id'] = df_reviews['purchase_id'].map(pid_to_bid)
df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['book_id','rating'])

# join
joined = df_reviews.merge(df_books[['book_id','year']], on='book_id', how='inner')
joined['decade_start'] = (joined['year'] // 10) * 10
joined['decade'] = joined['decade_start'].astype(int).astype(str) + 's'

# decades with at least 10 distinct rated books
books_per_decade = joined.groupby('decade')['book_id'].nunique().reset_index(name='distinct_books')
valid_decades = books_per_decade[books_per_decade['distinct_books'] >= 10]['decade']
valid = joined[joined['decade'].isin(valid_decades)]

decade_avg = valid.groupby('decade')['rating'].mean().reset_index(name='avg_rating')
if len(decade_avg)==0:
    res = None
else:
    top = decade_avg.sort_values(['avg_rating','decade'], ascending=[False, True]).iloc[0]
    res = {'decade': top['decade'], 'avg_rating': float(top['avg_rating'])}

print('__RESULT__:')
print(json.dumps(res))"""

env_args = {'var_call_itAmERabVqYVODFMyamnyj4d': 'file_storage/call_itAmERabVqYVODFMyamnyj4d.json', 'var_call_IaPadoEfCtbfuMTF6UfrdZlE': 'file_storage/call_IaPadoEfCtbfuMTF6UfrdZlE.json'}

exec(code, env_args)
