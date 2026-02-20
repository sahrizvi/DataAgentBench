code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_kX2iy5PxrnLaJtTdPH5E76dB)
reviews = load_records(var_call_bbonYhFIfYSyCzI9WsOeLFpV)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract 4-digit publication year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)
df_books['decade_start'] = (df_books['year'] // 10) * 10

# Fuzzy join: purchaseid_X -> bookid_X
# Extract numeric suffix
num_pat = re.compile(r'(\d+)$')

def suffix_num(x):
    if not isinstance(x, str):
        return None
    m = num_pat.search(x)
    return int(m.group(1)) if m else None

df_books['id_num'] = df_books['book_id'].map(suffix_num)
df_reviews['id_num'] = df_reviews['purchase_id'].map(suffix_num)

# Ratings as float
# Some ratings stored as strings

df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating','id_num'])
df_books = df_books.dropna(subset=['id_num'])

merged = df_reviews.merge(df_books[['id_num','book_id','decade_start']], on='id_num', how='inner')

# Consider only distinct books that have been rated in each decade
books_per_decade = merged[['decade_start','book_id']].drop_duplicates().groupby('decade_start').size().rename('distinct_books')
ratings_per_decade = merged.groupby('decade_start')['rating'].mean().rename('avg_rating')

decade_stats = pd.concat([books_per_decade, ratings_per_decade], axis=1).dropna().reset_index()
eligible = decade_stats[decade_stats['distinct_books'] >= 10]
if eligible.empty:
    best = None
else:
    best_row = eligible.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False, False, True]).iloc[0]
    best = f"{int(best_row['decade_start'])}s"

out = {'decade': best}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_kX2iy5PxrnLaJtTdPH5E76dB': 'file_storage/call_kX2iy5PxrnLaJtTdPH5E76dB.json', 'var_call_bbonYhFIfYSyCzI9WsOeLFpV': 'file_storage/call_bbonYhFIfYSyCzI9WsOeLFpV.json'}

exec(code, env_args)
