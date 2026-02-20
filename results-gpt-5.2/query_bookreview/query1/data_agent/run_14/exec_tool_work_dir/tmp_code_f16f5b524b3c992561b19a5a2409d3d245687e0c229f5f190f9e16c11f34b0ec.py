code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_cyUT3WRdGkUahI4mr6ozmmlE)
reviews = load_records(var_call_usmWgyApMIZK71Zo4CmbIBLc)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# parse year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.findall(s)
    if not m:
        return None
    # choose earliest plausible year as publication year
    yrs = [int(x) for x in m]
    return min(yrs)

df_b['year'] = df_b['details'].map(extract_year)
df_b = df_b.dropna(subset=['year'])
df_b['year'] = df_b['year'].astype(int)
df_b['decade'] = (df_b['year']//10)*10

# fuzzy join by numeric suffix in ids (bookid_123 <-> purchaseid_123)

def id_num(x):
    if not isinstance(x, str):
        return None
    m = re.search(r'(\d+)$', x)
    return int(m.group(1)) if m else None

df_b['idnum'] = df_b['book_id'].map(id_num)
df_r['idnum'] = df_r['purchase_id'].map(id_num)

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['idnum','rating'])
df_b = df_b.dropna(subset=['idnum'])
df_b['idnum'] = df_b['idnum'].astype(int)
df_r['idnum'] = df_r['idnum'].astype(int)

# average rating per book (so decades average across distinct books)
rb = df_r.groupby('idnum', as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})

bd = df_b[['idnum','decade']].drop_duplicates()
merged = bd.merge(rb, on='idnum', how='inner')

agg = merged.groupby('decade').agg(distinct_books=('idnum','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()
agg = agg[agg['distinct_books']>=10].sort_values(['avg_rating','distinct_books'], ascending=[False, False])

if agg.empty:
    out = {"decade": None, "message": "No decade found with at least 10 distinct rated books and a parsed publication year."}
else:
    top = agg.iloc[0]
    out = {"decade": f"{int(top['decade'])}s", "avg_rating": float(top['avg_rating']), "distinct_books": int(top['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_cyUT3WRdGkUahI4mr6ozmmlE': 'file_storage/call_cyUT3WRdGkUahI4mr6ozmmlE.json', 'var_call_usmWgyApMIZK71Zo4CmbIBLc': 'file_storage/call_usmWgyApMIZK71Zo4CmbIBLc.json'}

exec(code, env_args)
