code = """import json, pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_7Pd9ZRzPSleASAQEENVZonsG)
reviews = load_records(var_call_HB5MBFbyCpynho7sEuw6VLyx)

dfb = pd.DataFrame(books)
dfr = pd.DataFrame(reviews)

# filter to those explicitly categorized as Children's Books (not just substring)
# categories is a string like ["Books", "Children's Books", ...]
dfb['is_children'] = dfb['categories'].fillna('').str.contains("Children's Books", regex=False)
dfb = dfb[dfb['is_children']].copy()

# fuzzy join hint: purchase_id like purchaseid_XXX corresponds to bookid_XXX
# Extract numeric suffix

dfb['id_num'] = dfb['book_id'].astype(str).str.extract(r'(\d+)$')[0]
dfr['id_num'] = dfr['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# ratings are strings sometimes

dfr['rating'] = pd.to_numeric(dfr['rating'], errors='coerce')

m = pd.merge(dfb, dfr, on='id_num', how='inner', suffixes=('_book','_review'))

agg = (m.groupby(['book_id','title','author'], dropna=False)
         .agg(avg_rating=('rating','mean'), review_count=('rating','count'))
         .reset_index())

res = agg[agg['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False, False])

# format output
out = res.assign(avg_rating=res['avg_rating'].round(3)).to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_7Pd9ZRzPSleASAQEENVZonsG': 'file_storage/call_7Pd9ZRzPSleASAQEENVZonsG.json', 'var_call_HB5MBFbyCpynho7sEuw6VLyx': 'file_storage/call_HB5MBFbyCpynho7sEuw6VLyx.json'}

exec(code, env_args)
