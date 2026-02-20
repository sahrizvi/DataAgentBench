code = """import json, pandas as pd

# load books
books_src = var_call_DCq3Dq04KeSS7Vvwy43FuJcF
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# load reviews
rev_src = var_call_8Q0EnG1k1bAgn81yXla1UUb7
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        revs = json.load(f)
else:
    revs = rev_src

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(revs)

# ensure Children's Books category specifically
bdf = bdf[bdf['categories'].fillna('').str.contains("Children's Books", case=False, regex=False)]

# fuzzy join heuristic: map purchaseid_X -> bookid_X by taking numeric suffix
bdf['id_num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)').astype(float)
rdf['id_num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)').astype(float)

# ratings numeric
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

j = pd.merge(rdf, bdf[['id_num','book_id','title','author','categories']], on='id_num', how='inner')

agg = (j.groupby(['book_id','title','author'], dropna=False)
         .agg(avg_rating=('rating','mean'), review_count=('rating','count'))
         .reset_index())

res = agg[agg['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False,False])

out = res.assign(avg_rating=res['avg_rating'].round(3))
records = out.to_dict(orient='records')

print('__RESULT__:')
print(json.dumps(records, ensure_ascii=False))"""

env_args = {'var_call_DCq3Dq04KeSS7Vvwy43FuJcF': 'file_storage/call_DCq3Dq04KeSS7Vvwy43FuJcF.json', 'var_call_8Q0EnG1k1bAgn81yXla1UUb7': 'file_storage/call_8Q0EnG1k1bAgn81yXla1UUb7.json'}

exec(code, env_args)
