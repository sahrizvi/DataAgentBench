code = """import json, re, pandas as pd

def load_result(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_result(var_call_bKA0KQKqIHfr2FyHNpTRwiko)
reviews = load_result(var_call_Pee87P1YUGZLq4r8CxbTHFRg)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract 4-digit year from details near 'published'
pat = re.compile(r'(?i)\b(?:published|publication(?:\s+date)?)\b[^\d]{0,40}(\d{4})')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if m:
        y = int(m.group(1))
        if 1000 <= y <= 2026:
            return y
    # fallback: any 4-digit year
    m2 = re.search(r'\b(1[5-9]\d{2}|20\d{2})\b', s)
    if m2:
        y = int(m2.group(1))
        if 1000 <= y <= 2026:
            return y
    return None

bdf['year'] = bdf['details'].map(extract_year)
# fuzzy join assumption: purchase_id like 'purchaseid_123' corresponds to 'bookid_123'
rdf['book_id'] = rdf['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

merged = rdf.merge(bdf[['book_id','year']], on='book_id', how='inner')
merged = merged.dropna(subset=['year','rating'])
merged['decade_start'] = (merged['year']//10)*10

# decades with at least 10 distinct rated books
by_dec = merged.groupby('decade_start').agg(
    avg_rating=('rating','mean'),
    distinct_books=('book_id', pd.Series.nunique),
    n_ratings=('rating','size')
).reset_index()
by_dec = by_dec[by_dec['distinct_books']>=10]
by_dec = by_dec.sort_values(['avg_rating','distinct_books','n_ratings'], ascending=False)

best = None
if len(by_dec):
    row = by_dec.iloc[0]
    best = f"{int(row['decade_start'])}s"

out = {'decade': best}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_bKA0KQKqIHfr2FyHNpTRwiko': 'file_storage/call_bKA0KQKqIHfr2FyHNpTRwiko.json', 'var_call_Pee87P1YUGZLq4r8CxbTHFRg': 'file_storage/call_Pee87P1YUGZLq4r8CxbTHFRg.json'}

exec(code, env_args)
