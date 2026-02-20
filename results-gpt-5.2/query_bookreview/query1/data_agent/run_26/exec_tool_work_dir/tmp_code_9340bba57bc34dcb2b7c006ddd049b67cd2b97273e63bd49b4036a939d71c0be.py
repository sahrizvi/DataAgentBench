code = """import json, re, pandas as pd

def load_records(x):
    if isinstance(x, str):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_nEPTPObXvTHsyPPciJyTq9wE)
reviews = load_records(var_call_4V75iLCBhHlDi5zGeODSuYu8)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# Extract a 4-digit year from details (prefer explicit 'released on'/'published' etc; fallback any 4-digit year 1500-2026)
year_pat = re.compile(r'\b(1[5-9]\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    # prioritize patterns like 'released on ... 2004' by taking last year (often publication year)??
    yrs = [int(y) for y in year_pat.findall(s)]
    if not yrs:
        return None
    # Heuristic: choose the year closest to 2000? better choose max year not in future
    yrs2 = [y for y in yrs if y <= 2026]
    if not yrs2:
        return None
    return max(yrs2)

df_b['year'] = df_b['details'].apply(extract_year)
df_b = df_b.dropna(subset=['year'])
df_b['year'] = df_b['year'].astype(int)
df_b['decade_start'] = (df_b['year'] // 10) * 10

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['rating'])

# fuzzy join: map purchaseid_N -> bookid_N by extracting trailing integer
idnum_pat = re.compile(r'(\d+)\b')

def extract_num(s):
    if not isinstance(s, str):
        return None
    m = idnum_pat.findall(s)
    if not m:
        return None
    return int(m[-1])

df_b['id_num'] = df_b['book_id'].apply(extract_num)
df_r['id_num'] = df_r['purchase_id'].apply(extract_num)

df = df_r.merge(df_b[['id_num','decade_start']], on='id_num', how='inner')

# aggregate per book: average rating per distinct book (id_num)
book_avg = df.groupby(['id_num','decade_start'], as_index=False)['rating'].mean()

# per decade: average across books; require at least 10 distinct books
per_decade = book_avg.groupby('decade_start').agg(
    distinct_books=('id_num','nunique'),
    avg_rating=('rating','mean')
).reset_index()
per_decade = per_decade[per_decade['distinct_books']>=10]

if per_decade.empty:
    ans = None
else:
    top = per_decade.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
    ans = f"{int(top['decade_start'])}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_nEPTPObXvTHsyPPciJyTq9wE': 'file_storage/call_nEPTPObXvTHsyPPciJyTq9wE.json', 'var_call_4V75iLCBhHlDi5zGeODSuYu8': 'file_storage/call_4V75iLCBhHlDi5zGeODSuYu8.json'}

exec(code, env_args)
