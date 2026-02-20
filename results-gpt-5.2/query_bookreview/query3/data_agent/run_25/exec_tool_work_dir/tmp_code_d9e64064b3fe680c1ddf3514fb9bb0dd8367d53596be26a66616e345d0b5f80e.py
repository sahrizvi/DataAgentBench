code = """import json, pandas as pd

# load books
books_src = var_call_fygKqm1K278tOM5s8NiYrC67
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# load reviews from 2020 onwards
rev_src = var_call_uqM0CgKTjWiFfYjA7K2XltXg
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = rev_src

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# filter children's books by categories string containing "Children's Books"
# categories stored as string representation of list
bdf['is_childrens'] = bdf['categories'].fillna('').astype(str).str.contains("Children's Books", regex=False)
cb = bdf[bdf['is_childrens']].copy()

# fuzzy join: bookid_X <-> purchaseid_X by extracting trailing numeric id
cb['num'] = cb['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# ratings to numeric
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

merged = pd.merge(cb[['book_id','title','num']], rdf[['purchase_id','rating','num']], on='num', how='inner')
agg = merged.groupby(['book_id','title'], as_index=False).agg(avg_rating=('rating','mean'), review_count=('rating','count'))
res = agg[agg['avg_rating']>=4.5].sort_values(['avg_rating','review_count'], ascending=[False,False])

out = res.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_fygKqm1K278tOM5s8NiYrC67': 'file_storage/call_fygKqm1K278tOM5s8NiYrC67.json', 'var_call_uqM0CgKTjWiFfYjA7K2XltXg': 'file_storage/call_uqM0CgKTjWiFfYjA7K2XltXg.json'}

exec(code, env_args)
