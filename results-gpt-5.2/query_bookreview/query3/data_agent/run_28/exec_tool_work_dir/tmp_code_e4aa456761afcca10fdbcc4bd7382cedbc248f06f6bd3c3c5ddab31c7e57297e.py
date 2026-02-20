code = """import json, pandas as pd, re

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_gcNpdv5zgLv5oLQOs0fohwQT)
reviews = load_var(var_call_9ggSiybxgY6W7v6s2wBwP9WL)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Normalize ids: fuzzy join via numeric suffix
bdf['num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)').astype(int)
rdf['num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)').astype(int)

rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
# review_time already filtered >=2020 in SQL; keep valid ratings
rdf = rdf.dropna(subset=['rating','num'])

avg = rdf.groupby('num')['rating'].agg(['mean','count']).reset_index()
merged = bdf.merge(avg, on='num', how='inner')
res = merged[merged['mean']>=4.5].copy()
res = res.sort_values(['mean','count','title'], ascending=[False, False, True])

out = res[['title','author','book_id','mean','count']].rename(columns={'mean':'avg_rating_2020_onwards','count':'review_count_2020_onwards'}).to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_gcNpdv5zgLv5oLQOs0fohwQT': 'file_storage/call_gcNpdv5zgLv5oLQOs0fohwQT.json', 'var_call_9ggSiybxgY6W7v6s2wBwP9WL': 'file_storage/call_9ggSiybxgY6W7v6s2wBwP9WL.json'}

exec(code, env_args)
