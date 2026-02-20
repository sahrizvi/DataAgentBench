code = """import json, pandas as pd, re

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_JyYgk4vt6lsd5zXM4bjvPjYU)
reviews = load_records(var_call_G8lt0q73Fq5vRRIBHFCIer5a)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# normalize ids: extract numeric suffix
id_num_b = dfb['book_id'].astype(str).str.extract(r'(\d+)$')[0]
id_num_r = dfr['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

dfb = dfb.assign(id_num=id_num_b)
dfr = dfr.assign(id_num=id_num_r)

# coerce rating
# ratings sometimes are strings

dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

# already filtered to 2020+ in SQL, but ensure parseable
# group by id_num
agg = dfr.dropna(subset=['id_num','rating']).groupby('id_num').agg(avg_rating=('rating','mean'), review_count=('rating','size')).reset_index()

# join with books
out = pd.merge(dfb, agg, on='id_num', how='inner')

# filter avg>=4.5
out = out[out['avg_rating'] >= 4.5].copy()

# sort by avg desc then review_count desc then title
out = out.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

res = out[['title','author','avg_rating','review_count','book_id']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(res, ensure_ascii=False))"""

env_args = {'var_call_JyYgk4vt6lsd5zXM4bjvPjYU': 'file_storage/call_JyYgk4vt6lsd5zXM4bjvPjYU.json', 'var_call_G8lt0q73Fq5vRRIBHFCIer5a': 'file_storage/call_G8lt0q73Fq5vRRIBHFCIer5a.json'}

exec(code, env_args)
