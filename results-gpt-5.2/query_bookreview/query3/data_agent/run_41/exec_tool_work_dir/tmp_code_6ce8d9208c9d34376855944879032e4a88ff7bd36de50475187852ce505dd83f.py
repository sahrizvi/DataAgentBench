code = """import json, pandas as pd

def load_records(obj):
    if isinstance(obj, str):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

books = load_records(var_call_tFwfl2gBcvpeWZ6GO2eyYpJy)
revs = load_records(var_call_3WqlC1LZKUKQgbrK7s2oulWA)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(revs)
if dfr.empty or dfb.empty:
    out = []
else:
    dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')
    # fuzzy join: extract trailing numeric id
    dfb['id_num'] = dfb['book_id'].astype(str).str.extract(r'(\d+)$')[0]
    dfr['id_num'] = dfr['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
    # aggregate reviews from 2020 onwards
    agg = dfr.dropna(subset=['id_num','rating']).groupby('id_num').agg(
        avg_rating=('rating','mean'),
        review_count=('rating','size')
    ).reset_index()
    merged = dfb.merge(agg, on='id_num', how='inner')
    filtered = merged[merged['avg_rating'] >= 4.5].copy()
    filtered = filtered.sort_values(['avg_rating','review_count','title'], ascending=[False,False,True])
    out = filtered[['book_id','title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_tFwfl2gBcvpeWZ6GO2eyYpJy': 'file_storage/call_tFwfl2gBcvpeWZ6GO2eyYpJy.json', 'var_call_3WqlC1LZKUKQgbrK7s2oulWA': 'file_storage/call_3WqlC1LZKUKQgbrK7s2oulWA.json'}

exec(code, env_args)
