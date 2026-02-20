code = """import json, pandas as pd, re

def load_records(obj):
    if isinstance(obj, str) and obj.endswith('.json'):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

books = load_records(var_call_qa3W5cMz8ihg1yvYmD3kiRP1)
revs = load_records(var_call_khHHf4pVkHSTyF1IQTdKf1Nb)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(revs)

# ensure actual Children's Books category
mask_children = dfb['categories'].fillna('').str.contains("Children's Books", case=False, regex=False)
dfb = dfb[mask_children].copy()

# fuzzy join: normalize ids by taking trailing digits
get_num = lambda s: re.search(r'(\d+)$', str(s)).group(1) if re.search(r'(\d+)$', str(s)) else None

dfb['id_num'] = dfb['book_id'].map(get_num)
dfr['id_num'] = dfr['purchase_id'].map(get_num)

dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')
# review_time already filtered to >=2020 in SQL; keep non-null ratings

dfr = dfr.dropna(subset=['id_num','rating'])

merged = pd.merge(dfb, dfr, on='id_num', how='inner')

agg = (merged.groupby(['book_id','title','author'], dropna=False)
       .agg(avg_rating=('rating','mean'), review_count=('rating','size'))
       .reset_index())

res = agg[agg['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False, False])

# format
res['avg_rating'] = res['avg_rating'].round(3)
res_out = res.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(res_out, ensure_ascii=False))"""

env_args = {'var_call_qa3W5cMz8ihg1yvYmD3kiRP1': 'file_storage/call_qa3W5cMz8ihg1yvYmD3kiRP1.json', 'var_call_khHHf4pVkHSTyF1IQTdKf1Nb': 'file_storage/call_khHHf4pVkHSTyF1IQTdKf1Nb.json'}

exec(code, env_args)
