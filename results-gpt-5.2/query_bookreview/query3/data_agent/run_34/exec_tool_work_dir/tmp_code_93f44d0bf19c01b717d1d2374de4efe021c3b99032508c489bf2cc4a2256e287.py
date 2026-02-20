code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load(var_call_ygnxXSPAGS5GH9gBsYhssmcx)
revs = load(var_call_EarXTGzKkZ9KIEMXcrpXjZTM)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(revs)
if dfr.empty or dfb.empty:
    out = []
else:
    # normalize ids: bookid_4 vs purchaseid_4
    dfb['id_num'] = dfb['book_id'].astype(str).str.extract(r'(\d+)$')[0]
    dfr['id_num'] = dfr['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
    dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')
    grp = dfr.dropna(subset=['id_num','rating']).groupby('id_num').agg(avg_rating=('rating','mean'), review_count=('rating','size')).reset_index()
    m = dfb.merge(grp, on='id_num', how='inner')
    m = m[m['avg_rating'] >= 4.5].copy()
    m = m.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])
    out = m[['book_id','title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_ygnxXSPAGS5GH9gBsYhssmcx': 'file_storage/call_ygnxXSPAGS5GH9gBsYhssmcx.json', 'var_call_EarXTGzKkZ9KIEMXcrpXjZTM': 'file_storage/call_EarXTGzKkZ9KIEMXcrpXjZTM.json'}

exec(code, env_args)
