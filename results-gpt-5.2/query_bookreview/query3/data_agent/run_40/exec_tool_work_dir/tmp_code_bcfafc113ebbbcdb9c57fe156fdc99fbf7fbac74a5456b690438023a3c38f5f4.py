code = """import json, pandas as pd

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_vy07jqTpl3MmEDqGJyw5pS5D)
reviews = load_var(var_call_6TCS7s6GHWTwiAhzqTdc3Bpo)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# normalize ids: bookid_123 vs purchaseid_123
for col in ['book_id']:
    dfb[col] = dfb[col].astype(str)
dfr['purchase_id'] = dfr['purchase_id'].astype(str)

dfb['id_num'] = dfb['book_id'].str.extract(r'(\d+)$')[0]
dfr['id_num'] = dfr['purchase_id'].str.extract(r'(\d+)$')[0]

# ratings numeric
dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

# aggregate from 2020 onwards already filtered in SQL
agg = dfr.dropna(subset=['id_num','rating']).groupby('id_num').agg(avg_rating=('rating','mean'), review_count=('rating','size')).reset_index()

merged = dfb.merge(agg, on='id_num', how='inner')

# Ensure category specifically includes Children's Books (not just Children)
merged = merged[merged['categories'].str.contains("Children's Books", na=False)]

result = merged[merged['avg_rating'] >= 4.5].copy()
result = result.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = result[['title','author','book_id','avg_rating','review_count']].to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_vy07jqTpl3MmEDqGJyw5pS5D': 'file_storage/call_vy07jqTpl3MmEDqGJyw5pS5D.json', 'var_call_6TCS7s6GHWTwiAhzqTdc3Bpo': 'file_storage/call_6TCS7s6GHWTwiAhzqTdc3Bpo.json'}

exec(code, env_args)
