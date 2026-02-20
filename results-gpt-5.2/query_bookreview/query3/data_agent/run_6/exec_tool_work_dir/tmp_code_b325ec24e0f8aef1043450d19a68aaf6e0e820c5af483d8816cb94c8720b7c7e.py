code = """import json, pandas as pd, re

def load_tool_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_tool_result(var_call_DXQVgeruDohRbsUQ7y5jaZc3)
reviews = load_tool_result(var_call_KyuZbjj3gUVjJO1ppLTevWkF)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# keep only explicitly Children's Books category
mask_child = dfb['categories'].astype(str).str.contains("Children's Books", case=False, na=False)
dfb = dfb[mask_child].copy()

# parse numeric ids for fuzzy join purchaseid_X <-> bookid_X
pat = re.compile(r'(?:bookid|purchaseid)_(\d+)')
dfb['id_num'] = dfb['book_id'].astype(str).str.extract(pat)[0].astype('Int64')
dfr['id_num'] = dfr['purchase_id'].astype(str).str.extract(pat)[0].astype('Int64')

# rating to float
# filter from 2020 onwards already done in SQL, but ensure parseable
# compute stats
for col in ['rating']:
    dfr[col] = pd.to_numeric(dfr[col], errors='coerce')

dfr = dfr.dropna(subset=['id_num','rating'])

stats = dfr.groupby('id_num').agg(avg_rating=('rating','mean'), review_count=('rating','size')).reset_index()

merged = pd.merge(dfb, stats, on='id_num', how='inner')
res = merged[merged['avg_rating'] >= 4.5].copy()
res = res.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = res[['book_id','title','author','avg_rating','review_count']].to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_DXQVgeruDohRbsUQ7y5jaZc3': 'file_storage/call_DXQVgeruDohRbsUQ7y5jaZc3.json', 'var_call_KyuZbjj3gUVjJO1ppLTevWkF': 'file_storage/call_KyuZbjj3gUVjJO1ppLTevWkF.json'}

exec(code, env_args)
