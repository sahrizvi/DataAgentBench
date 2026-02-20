code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_wfYsDFuJsFxoZYOc34Hr0fpF)
reviews = load_records(var_call_urnwc8xLJ8FU3q5FpXcTYecw)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# extract year from details text
pat1 = re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+(\d{4})\b', re.I)
pat2 = re.compile(r'\b(\d{4})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat1.search(s)
    if m:
        return int(m.group(1))
    # fallback: look for 'Published' near a year, else first plausible year 1500-2026
    years = [int(y) for y in pat2.findall(s)]
    years = [y for y in years if 1500 <= y <= 2026]
    if not years:
        return None
    # if multiple years, prefer one following 'Published'/'released'
    m2 = re.search(r'(?i)(published|released|publication)[^\d]{0,30}(\d{4})', s)
    if m2:
        y = int(m2.group(2))
        if 1500 <= y <= 2026:
            return y
    return years[0]

df_b['year'] = df_b['details'].map(extract_year)
df_b = df_b.dropna(subset=['year']).copy()
df_b['year'] = df_b['year'].astype(int)

# join via numeric suffix mapping (bookid_123 <-> purchaseid_123)
get_num = lambda x: int(re.search(r'(\d+)$', str(x)).group(1)) if re.search(r'(\d+)$', str(x)) else None

df_b['num'] = df_b['book_id'].map(get_num)
df_r['num'] = df_r['purchase_id'].map(get_num)
df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['num','rating']).copy()
df_r['num'] = df_r['num'].astype(int)

# determine which books have been rated (at least one review)
rated_books = df_r.groupby('num', as_index=False).size()[['num']]

df = pd.merge(df_b[['num','year']], rated_books, on='num', how='inner')
df['decade_start'] = (df['year'] // 10) * 10

# average rating per book (across reviews)
book_avg = df_r.groupby('num', as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})

# attach decade
book_dec = pd.merge(df[['num','decade_start']], book_avg, on='num', how='inner').drop_duplicates('num')

dec_stats = book_dec.groupby('decade_start').agg(distinct_books=('num','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()
dec_stats = dec_stats[dec_stats['distinct_books']>=10].copy()
if dec_stats.empty:
    ans = None
else:
    top = dec_stats.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
    ans = f"{int(top['decade_start'])}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_wfYsDFuJsFxoZYOc34Hr0fpF': 'file_storage/call_wfYsDFuJsFxoZYOc34Hr0fpF.json', 'var_call_urnwc8xLJ8FU3q5FpXcTYecw': 'file_storage/call_urnwc8xLJ8FU3q5FpXcTYecw.json'}

exec(code, env_args)
