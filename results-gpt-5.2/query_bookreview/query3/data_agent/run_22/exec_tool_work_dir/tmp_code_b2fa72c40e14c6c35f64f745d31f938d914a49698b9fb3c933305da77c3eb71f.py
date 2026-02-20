code = """import json, pandas as pd

def load(var):
    if isinstance(var, str) and var.endswith('.json'):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load(var_call_rQv5nHdsVH9XVmiPwBNUuncV)
revs = load(var_call_BuIHgCvU7z8TT9rRLs5ITn1f)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(revs)

# normalize ids: bookid_123 vs purchaseid_123
import re

def norm_id(x):
    if pd.isna(x):
        return None
    m = re.search(r'(?:bookid|purchaseid)_(\d+)', str(x))
    return m.group(1) if m else str(x)

dfb['id_norm'] = dfb['book_id'].map(norm_id)
dfr['id_norm'] = dfr['purchase_id'].map(norm_id)

# coerce rating
dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

agg = dfr.groupby('id_norm', dropna=True).agg(avg_rating=('rating','mean'), n_reviews=('rating','count')).reset_index()

merged = dfb.merge(agg, on='id_norm', how='inner')

# ensure truly categorized as Children's Books
merged = merged[merged['categories'].str.contains("Children's Books", na=False)]

res = merged[merged['avg_rating'] >= 4.5].copy()
res = res.sort_values(['avg_rating','n_reviews','title'], ascending=[False, False, True])

out = res[['title','author','avg_rating','n_reviews']].to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_rQv5nHdsVH9XVmiPwBNUuncV': 'file_storage/call_rQv5nHdsVH9XVmiPwBNUuncV.json', 'var_call_BuIHgCvU7z8TT9rRLs5ITn1f': 'file_storage/call_BuIHgCvU7z8TT9rRLs5ITn1f.json'}

exec(code, env_args)
