code = """import json, re, pandas as pd

def load_records(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_TtAcGKMIgjz4Ne8jJyWKEtCb)
reviews = load_records(var_call_uStOVK4dXoiU5UA7CAE2fH7C)

# parse year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

years = []
for r in books:
    det = r.get('details') or ''
    m = pat.search(det)
    y = int(m.group(1)) if m else None
    years.append({'book_id': r.get('book_id'), 'year': y})

df_year = pd.DataFrame(years).dropna(subset=['book_id','year'])

# fuzzy join bookid_X <-> purchaseid_X using numeric suffix
suffix_pat = re.compile(r'(\d+)$')

def suffix(s):
    if s is None:
        return None
    m = suffix_pat.search(str(s))
    return m.group(1) if m else None

rev_rows = []
for r in reviews:
    rev_rows.append({
        'purchase_id': r.get('purchase_id'),
        'avg_rating': float(r.get('avg_rating')),
        'n_reviews': int(r.get('n_reviews')),
        'suffix': suffix(r.get('purchase_id'))
    })

df_rev = pd.DataFrame(rev_rows).dropna(subset=['suffix'])
df_year['suffix'] = df_year['book_id'].map(suffix)

df = pd.merge(df_year[['suffix','year']], df_rev[['suffix','avg_rating']], on='suffix', how='inner')

# decade and aggregate; require at least 10 distinct books rated -> 10 distinct suffixes
# here each suffix corresponds to a book entity

df['decade_start'] = (df['year'] // 10) * 10
agg = df.groupby('decade_start').agg(
    avg_rating=('avg_rating','mean'),
    n_books=('suffix','nunique')
).reset_index()

eligible = agg[agg['n_books'] >= 10].copy()
if eligible.empty:
    result = {'decade': None}
else:
    best = eligible.sort_values(['avg_rating','n_books','decade_start'], ascending=[False, False, True]).iloc[0]
    decade_label = f"{int(best['decade_start'])}s"
    result = {'decade': decade_label, 'avg_rating': float(best['avg_rating']), 'n_books': int(best['n_books'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_TtAcGKMIgjz4Ne8jJyWKEtCb': 'file_storage/call_TtAcGKMIgjz4Ne8jJyWKEtCb.json', 'var_call_uStOVK4dXoiU5UA7CAE2fH7C': 'file_storage/call_uStOVK4dXoiU5UA7CAE2fH7C.json'}

exec(code, env_args)
