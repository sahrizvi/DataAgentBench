code = """import json, re, pandas as pd

def load_records(x):
    if isinstance(x, str):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_w5WH4GopaCLc2Q48MurMH0L8)
reviews = load_records(var_call_NuKTxXFTWTtFxa8rD7Ncy4PC)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# Extract year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if s is None:
        return None
    m = pat.findall(str(s))
    if not m:
        return None
    # choose earliest plausible publication year mentioned
    years = sorted({int(y) for y in m})
    return years[0]

dfb['year'] = dfb['details'].map(extract_year)
# decade label
mask_year = dfb['year'].between(1800, 2026, inclusive='both')
dfb = dfb[mask_year].copy()
dfb['decade_start'] = (dfb['year']//10)*10

def num_from_id(s):
    m = re.search(r'(\d+)$', str(s))
    return int(m.group(1)) if m else None

dfb['id_num'] = dfb['book_id'].map(num_from_id)
dfr['id_num'] = dfr['purchase_id'].map(num_from_id)

dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')
dfr = dfr.dropna(subset=['id_num','rating'])
dfb = dfb.dropna(subset=['id_num'])

# fuzzy join via numeric suffix
joined = dfr.merge(dfb[['id_num','decade_start']], on='id_num', how='inner')

# decades with at least 10 distinct books that have been rated
agg = joined.groupby('decade_start').agg(
    avg_rating=('rating','mean'),
    distinct_books=('id_num', pd.Series.nunique),
    n_ratings=('rating','size')
).reset_index()
agg = agg[agg['distinct_books']>=10]
agg = agg.sort_values(['avg_rating','distinct_books','n_ratings'], ascending=False)

if agg.empty:
    res = None
else:
    top = agg.iloc[0]
    decade_label = f"{int(top['decade_start'])}s"
    res = decade_label

print("__RESULT__:")
print(json.dumps(res))"""

env_args = {'var_call_w5WH4GopaCLc2Q48MurMH0L8': 'file_storage/call_w5WH4GopaCLc2Q48MurMH0L8.json', 'var_call_NuKTxXFTWTtFxa8rD7Ncy4PC': 'file_storage/call_NuKTxXFTWTtFxa8rD7Ncy4PC.json'}

exec(code, env_args)
