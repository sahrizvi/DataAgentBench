code = """import json, pandas as pd

def load_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_result(var_call_pq4JLdaQIQjDPq2rv1zZvyl8)
reviews = load_result(var_call_xmOI7FuGbjSjeOuxXgyRHWzm)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# normalize ids: bookid_123 vs purchaseid_123
import re

def id_num(s):
    if s is None:
        return None
    m = re.search(r'(\d+)$', str(s))
    return int(m.group(1)) if m else None

dfb['idn'] = dfb['book_id'].map(id_num)
dfr['idn'] = dfr['purchase_id'].map(id_num)

# ratings are strings in sqlite extract
dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

agg = dfr.groupby('idn', dropna=True).agg(avg_rating=('rating','mean'), review_count=('rating','count')).reset_index()

merged = dfb.merge(agg, on='idn', how='inner')
res = merged[merged['avg_rating'] >= 4.5].copy()
res = res.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])

out = res[['title','author','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_pq4JLdaQIQjDPq2rv1zZvyl8': 'file_storage/call_pq4JLdaQIQjDPq2rv1zZvyl8.json', 'var_call_xmOI7FuGbjSjeOuxXgyRHWzm': 'file_storage/call_xmOI7FuGbjSjeOuxXgyRHWzm.json'}

exec(code, env_args)
