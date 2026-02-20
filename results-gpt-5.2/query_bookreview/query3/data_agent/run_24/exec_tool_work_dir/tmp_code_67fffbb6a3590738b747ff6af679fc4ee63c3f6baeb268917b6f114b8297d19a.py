code = """import json, pandas as pd

def load(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load(var_call_nC144DvUfh0RHZM2NL4RmKYn)
reviews = load(var_call_oJXrpHmh6TDGpUTQUM87hD8P)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# normalize ids: bookid_123 <-> purchaseid_123
if not dfb.empty:
    dfb['join_id'] = dfb['book_id'].astype(str).str.replace('bookid_', '', regex=False)
if not dfr.empty:
    dfr['join_id'] = dfr['purchase_id'].astype(str).str.replace('purchaseid_', '', regex=False)
    dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

merged = dfb.merge(dfr, on='join_id', how='inner')

agg = (merged.groupby(['book_id','title','author'], dropna=False)
       .agg(avg_rating=('rating','mean'), review_count=('rating','count'))
       .reset_index())

res = agg[(agg['avg_rating']>=4.5) & (agg['review_count']>0)].sort_values(['avg_rating','review_count'], ascending=[False,False])

out = res.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_nC144DvUfh0RHZM2NL4RmKYn': 'file_storage/call_nC144DvUfh0RHZM2NL4RmKYn.json', 'var_call_oJXrpHmh6TDGpUTQUM87hD8P': 'file_storage/call_oJXrpHmh6TDGpUTQUM87hD8P.json'}

exec(code, env_args)
