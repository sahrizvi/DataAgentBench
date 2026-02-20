code = """import json, pandas as pd

def load_result(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_result(var_call_RjpT8Z1zunfb9lBKDcdZ28cl)
reviews = load_result(var_call_QFhkcVDqicay7U1fezZPe7P4)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# Ensure Children's Books specifically
child_mask = dfb['categories'].astype(str).str.contains("Children's Books", case=False, na=False)
dfb = dfb[child_mask].copy()

# Fuzzy join: purchaseid_XX <-> bookid_XX by extracting trailing number
for col in ['book_id']:
    dfb['id_num'] = dfb[col].astype(str).str.extract(r'(\d+)$')[0]

dfr['id_num'] = dfr['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# Ratings numeric
# Some ratings are strings
if 'rating' in dfr.columns:
    dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

# Filter reviews 2020+ already, but ensure
if 'review_time' in dfr.columns:
    dfr = dfr[dfr['review_time'].astype(str).str.slice(0,4) >= '2020']

# Aggregate
agg = dfr.groupby('id_num', dropna=True).agg(avg_rating=('rating','mean'), review_count=('rating','count')).reset_index()

merged = pd.merge(dfb, agg, on='id_num', how='inner')
res = merged[merged['avg_rating'] >= 4.5].copy()
res = res.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = res[['title','author','book_id','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_RjpT8Z1zunfb9lBKDcdZ28cl': 'file_storage/call_RjpT8Z1zunfb9lBKDcdZ28cl.json', 'var_call_QFhkcVDqicay7U1fezZPe7P4': 'file_storage/call_QFhkcVDqicay7U1fezZPe7P4.json'}

exec(code, env_args)
