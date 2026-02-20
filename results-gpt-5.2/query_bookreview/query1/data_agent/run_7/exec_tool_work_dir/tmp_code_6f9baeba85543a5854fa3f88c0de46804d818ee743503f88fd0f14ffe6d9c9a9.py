code = """import json, re, pandas as pd

def load_result(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_result(var_call_wYkdheag7xdl1Q0TPyxAq7pH)
reviews = load_result(var_call_llJX4tcRFqdsxatVcjPiLI43)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# extract 4-digit year from details
pattern = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pattern.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)

# fuzzy join via numeric suffix id mapping: bookid_123 <-> purchaseid_123
suffix_pat = re.compile(r'(\d+)$')

def suffix_num(x):
    if not isinstance(x, str):
        return None
    m = suffix_pat.search(x)
    return int(m.group(1)) if m else None

df_books['k'] = df_books['book_id'].map(suffix_num)
df_reviews['k'] = df_reviews['purchase_id'].map(suffix_num)

df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['k','rating'])
df_books = df_books.dropna(subset=['k'])

merged = df_reviews.merge(df_books[['k','year']], on='k', how='inner')

# decade label
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# decades with at least 10 distinct books (k)
agg = merged.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('k', pd.Series.nunique)
).reset_index()

eligible = agg[agg['distinct_books']>=10].copy()
if eligible.empty:
    out = {"decade": None}
else:
    best = eligible.sort_values(['avg_rating','distinct_books','decade'], ascending=[False, False, True]).iloc[0]
    out = {"decade": best['decade'], "avg_rating": float(best['avg_rating']), "distinct_books": int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_wYkdheag7xdl1Q0TPyxAq7pH': 'file_storage/call_wYkdheag7xdl1Q0TPyxAq7pH.json', 'var_call_llJX4tcRFqdsxatVcjPiLI43': 'file_storage/call_llJX4tcRFqdsxatVcjPiLI43.json'}

exec(code, env_args)
