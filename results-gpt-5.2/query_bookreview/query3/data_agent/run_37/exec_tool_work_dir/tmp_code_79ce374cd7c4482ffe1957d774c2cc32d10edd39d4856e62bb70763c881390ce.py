code = """import json, pandas as pd, re

# Load books (may be file path)
books_src = var_call_EdAWrgeosZLhYPf9vtDUS5T8
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

reviews_src = var_call_SU1DIgG6u7rTQRZomNngXmwS
if isinstance(reviews_src, str):
    with open(reviews_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = reviews_src

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Ensure Children's Books category (exact phrase)
bdf = bdf[bdf['categories'].fillna('').str.contains("Children's Books", case=False, regex=False)].copy()

# Fuzzy join via numeric suffix in ids (bookid_#, purchaseid_#)

def extract_num(x):
    if x is None:
        return None
    m = re.search(r'(\d+)$', str(x))
    return int(m.group(1)) if m else None

bdf['id_num'] = bdf['book_id'].apply(extract_num)
rdf['id_num'] = rdf['purchase_id'].apply(extract_num)

# ratings as float
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

# group by id_num from 2020 onwards (already filtered in SQL), compute avg
agg = rdf.groupby('id_num', dropna=True).agg(avg_rating=('rating','mean'), review_count=('rating','count')).reset_index()

merged = bdf.merge(agg, on='id_num', how='inner')
res = merged[merged['avg_rating'] >= 4.5].copy()

# prepare output
res = res.sort_values(['avg_rating','review_count','title'], ascending=[False, False, True])
res_out = res[['title','author','book_id','avg_rating','review_count']].to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(res_out, ensure_ascii=False))"""

env_args = {'var_call_EdAWrgeosZLhYPf9vtDUS5T8': 'file_storage/call_EdAWrgeosZLhYPf9vtDUS5T8.json', 'var_call_SU1DIgG6u7rTQRZomNngXmwS': 'file_storage/call_SU1DIgG6u7rTQRZomNngXmwS.json'}

exec(code, env_args)
