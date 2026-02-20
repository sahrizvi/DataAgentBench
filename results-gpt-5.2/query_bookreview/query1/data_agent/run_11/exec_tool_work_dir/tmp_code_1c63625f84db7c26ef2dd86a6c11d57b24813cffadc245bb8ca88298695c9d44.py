code = """import json, re, pandas as pd

# Load books details
books_src = var_call_F4dGZv08wVTRxoo7bWOCiY4T
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# Load reviews
rev_src = var_call_BdI2GLTnqhsMNUjirhO1niXQ
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = rev_src

# Extract publication year from details
# Prefer explicit 4-digit years 1500-2029; take the last such year (often publication date is the last year in string)
year_pat = re.compile(r'\b(1[5-9]\d{2}|20[0-2]\d)\b')
rows = []
for r in books:
    d = r.get('details') or ''
    ys = year_pat.findall(d)
    if not ys:
        continue
    year = int(ys[-1])
    rows.append({'book_id': r.get('book_id'), 'year': year})

books_year = pd.DataFrame(rows).dropna().drop_duplicates('book_id')

# Fuzzy join bookid_X <-> purchaseid_X by shared numeric suffix
suffix_pat = re.compile(r'(\d+)')
books_year['suffix'] = books_year['book_id'].astype(str).str.extract(suffix_pat)[0]

rev_df = pd.DataFrame(reviews)
rev_df = rev_df.dropna(subset=['purchase_id','rating']).copy()
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['rating'])
rev_df['suffix'] = rev_df['purchase_id'].astype(str).str.extract(suffix_pat)[0]

merged = rev_df.merge(books_year[['suffix','year']], on='suffix', how='inner')
merged = merged.dropna(subset=['year','rating'])
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# Count distinct books per decade (by suffix)
dec_stats = merged.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('suffix', lambda x: x.nunique())
).reset_index()

dec_stats = dec_stats[dec_stats['distinct_books'] >= 10].copy()
if dec_stats.empty:
    ans = None
else:
    top = dec_stats.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    ans = str(top['decade'])

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_F4dGZv08wVTRxoo7bWOCiY4T': 'file_storage/call_F4dGZv08wVTRxoo7bWOCiY4T.json', 'var_call_BdI2GLTnqhsMNUjirhO1niXQ': 'file_storage/call_BdI2GLTnqhsMNUjirhO1niXQ.json'}

exec(code, env_args)
