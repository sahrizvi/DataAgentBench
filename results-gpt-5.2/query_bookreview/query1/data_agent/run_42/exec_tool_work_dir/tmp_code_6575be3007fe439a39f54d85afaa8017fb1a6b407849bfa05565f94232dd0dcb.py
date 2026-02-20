code = """import json, re, pandas as pd

def load_records(x):
    if isinstance(x, str):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_rhTEMdMppQ7vfMj9jIKskS7h)
reviews = load_records(var_call_BUTCYTiVkwk71qUMjHvy7LEY)

books_df = pd.DataFrame(books)
rev_df = pd.DataFrame(reviews)

# extract 4-digit year from details
pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

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

books_df['year'] = books_df['details'].map(extract_year)
books_df = books_df.dropna(subset=['year']).copy()
books_df['year'] = books_df['year'].astype(int)

# fuzzy join rule hinted: bookid_N <-> purchaseid_N
books_df['key'] = books_df['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rev_df['key'] = rev_df['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['key','rating'])
books_df = books_df.dropna(subset=['key'])

merged = rev_df.merge(books_df[['key','year']], on='key', how='inner')
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# distinct books per decade among rated books
books_per_decade = merged[['decade','key']].drop_duplicates().groupby('decade').size().reset_index(name='distinct_books')
ratings_per_decade = merged.groupby('decade', as_index=False)['rating'].mean().rename(columns={'rating':'avg_rating'})
summary = ratings_per_decade.merge(books_per_decade, on='decade', how='inner')
summary = summary[summary['distinct_books']>=10]

if summary.empty:
    ans = None
else:
    top = summary.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    ans = str(top['decade'])

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_rhTEMdMppQ7vfMj9jIKskS7h': 'file_storage/call_rhTEMdMppQ7vfMj9jIKskS7h.json', 'var_call_BUTCYTiVkwk71qUMjHvy7LEY': 'file_storage/call_BUTCYTiVkwk71qUMjHvy7LEY.json'}

exec(code, env_args)
