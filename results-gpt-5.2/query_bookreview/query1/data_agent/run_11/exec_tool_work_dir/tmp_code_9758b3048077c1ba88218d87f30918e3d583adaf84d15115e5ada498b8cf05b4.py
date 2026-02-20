code = """import json, re, pandas as pd

# load full books
p = var_call_fcK4nOUOoOAYgxrqJ6cpIzsP
if isinstance(p, str):
    with open(p, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = p

# load reviews
rev_src = var_call_BdI2GLTnqhsMNUjirhO1niXQ
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = rev_src

year_pat = re.compile(r'\b(1[5-9]\d{2}|20[0-2]\d)\b')
rows=[]
for r in books:
    bid = r.get('book_id')
    d = r.get('details') or ''
    ys = year_pat.findall(d)
    if bid and ys:
        rows.append({'book_id': bid, 'year': int(ys[-1])})
books_year = pd.DataFrame(rows).drop_duplicates('book_id')
books_year['suffix'] = books_year['book_id'].str.extract(r'(\d+)$')[0]

rev_df = pd.DataFrame(reviews)
rev_df = rev_df.dropna(subset=['purchase_id','rating']).copy()
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['rating'])
rev_df['suffix'] = rev_df['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

merged = rev_df.merge(books_year[['suffix','year']], on='suffix', how='inner').dropna(subset=['year','suffix','rating'])
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str)+'s'

stats = merged.groupby('decade').agg(avg_rating=('rating','mean'), distinct_books=('suffix','nunique')).reset_index()
stats = stats[stats['distinct_books']>=10]
if stats.empty:
    ans=None
else:
    ans=str(stats.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]['decade'])

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_F4dGZv08wVTRxoo7bWOCiY4T': 'file_storage/call_F4dGZv08wVTRxoo7bWOCiY4T.json', 'var_call_BdI2GLTnqhsMNUjirhO1niXQ': 'file_storage/call_BdI2GLTnqhsMNUjirhO1niXQ.json', 'var_call_o80sWzY0dunwTD8q5fsPSBbF': {'decade': None}, 'var_call_fcK4nOUOoOAYgxrqJ6cpIzsP': 'file_storage/call_fcK4nOUOoOAYgxrqJ6cpIzsP.json'}

exec(code, env_args)
