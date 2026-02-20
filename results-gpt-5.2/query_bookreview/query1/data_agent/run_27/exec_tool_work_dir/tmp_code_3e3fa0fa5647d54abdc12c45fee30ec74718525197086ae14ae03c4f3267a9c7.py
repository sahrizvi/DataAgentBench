code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_UjulA7o27SQ7U5ZMcr03QUCp)
reviews = load_records(var_call_Y4ylfZ6KsLcp6X2T8ZbsrzJY)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# parse publication year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(txt):
    if not isinstance(txt, str):
        return None
    # prioritize patterns around Published/Publication
    m = re.search(r'(?i)(published|publication date|first edition|released on)[^\d]{0,40}(19\d{2}|20\d{2})', txt)
    if m:
        return int(m.group(2))
    # fallback: earliest plausible year in string (often publication year)
    years = [int(y) for y in pat.findall(txt)]
    if not years:
        return None
    # choose min year in range 1400-2026
    years = [y for y in years if 1400 <= y <= 2026]
    return min(years) if years else None

df_b['year'] = df_b['details'].apply(extract_year)
df_b = df_b.dropna(subset=['year']).copy()

df_b['book_num'] = df_b['book_id'].str.extract(r'(\d+)$').astype(float)
df_r['book_num'] = df_r['purchase_id'].str.extract(r'(\d+)$').astype(float)

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['book_num','rating'])

df = df_r.merge(df_b[['book_num','year']], on='book_num', how='inner')

df['decade_start'] = (df['year']//10)*10

g = df.groupby('decade_start').agg(
    avg_rating=('rating','mean'),
    distinct_books=('book_num','nunique')
).reset_index()

g = g[g['distinct_books']>=10].copy()
if g.empty:
    ans = None
else:
    best = g.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
    ans = f"{int(best['decade_start'])}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_UjulA7o27SQ7U5ZMcr03QUCp': 'file_storage/call_UjulA7o27SQ7U5ZMcr03QUCp.json', 'var_call_Y4ylfZ6KsLcp6X2T8ZbsrzJY': 'file_storage/call_Y4ylfZ6KsLcp6X2T8ZbsrzJY.json'}

exec(code, env_args)
