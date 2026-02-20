code = """import json, pandas as pd, re

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_xq7UQLxFmadi7LYXNyevVkyU)
reviews = load_records(var_call_mFlN8wd6p9q5kAQbhHOu8kYp)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# numeric ids from strings like 'bookid_32' and 'purchaseid_32'

def extract_num(s):
    if s is None or pd.isna(s):
        return None
    m = re.search(r'(\d+)', str(s))
    return int(m.group(1)) if m else None

dfb['join_id'] = dfb['book_id'].map(extract_num)
dfr['join_id'] = dfr['purchase_id'].map(extract_num)

# parse rating

dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

df = pd.merge(dfb, dfr, on='join_id', how='inner', suffixes=('_book','_review'))

agg = (df.groupby(['book_id','title','author'], dropna=False)
         .agg(avg_rating=('rating','mean'), review_count=('rating','size'))
         .reset_index())

res = agg[agg['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False, False])

out = res.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_xq7UQLxFmadi7LYXNyevVkyU': 'file_storage/call_xq7UQLxFmadi7LYXNyevVkyU.json', 'var_call_mFlN8wd6p9q5kAQbhHOu8kYp': 'file_storage/call_mFlN8wd6p9q5kAQbhHOu8kYp.json'}

exec(code, env_args)
