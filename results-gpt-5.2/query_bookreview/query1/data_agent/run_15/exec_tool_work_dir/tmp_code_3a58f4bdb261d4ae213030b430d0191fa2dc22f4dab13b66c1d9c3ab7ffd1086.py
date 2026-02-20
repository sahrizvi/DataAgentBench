code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_4ITQ7BT6czaSpolyehdjgXMV)
revs = load_records(var_call_wneurvLbgAj1zwLofZLdwu3O)

df_books = pd.DataFrame(books)
df_revs = pd.DataFrame(revs)

# extract year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    years = [int(m.group(1)) for m in pat.finditer(s)]
    if not years:
        return None
    # prefer plausible publication years 1500-2026
    years = [y for y in years if 1500 <= y <= 2026]
    return min(years) if years else None

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)

# fuzzy join purchase_id_X to bookid_X via numeric suffix

def suffix_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

df_books['sid'] = df_books['book_id'].map(suffix_num)
df_revs['sid'] = df_revs['purchase_id'].map(suffix_num)

# cast avg_rating
for c in ['avg_rating','review_count']:
    if c in df_revs.columns:
        df_revs[c] = pd.to_numeric(df_revs[c], errors='coerce')

df = pd.merge(df_books[['book_id','year','sid']], df_revs[['purchase_id','avg_rating','sid']], on='sid', how='inner')
# only books that have been rated (avg_rating not null)
df = df.dropna(subset=['avg_rating'])

# decade
df['decade_start'] = (df['year'] // 10) * 10
# compute per decade: distinct books and avg of book avg_ratings
agg = df.groupby('decade_start').agg(distinct_books=('sid','nunique'), avg_rating=('avg_rating','mean')).reset_index()
agg = agg[agg['distinct_books'] >= 10]
if agg.empty:
    out = None
else:
    best = agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    out = f"{int(best['decade_start'])}s"

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_4ITQ7BT6czaSpolyehdjgXMV': 'file_storage/call_4ITQ7BT6czaSpolyehdjgXMV.json', 'var_call_wneurvLbgAj1zwLofZLdwu3O': 'file_storage/call_wneurvLbgAj1zwLofZLdwu3O.json'}

exec(code, env_args)
