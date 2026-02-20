code = """import json, pandas as pd

# Load books
books_src = var_call_kF382lWp3SOh2h05IBnnvzZ5
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# Load reviews
reviews_src = var_call_606cSpwU57bNWSqXO9YkOaoc
if isinstance(reviews_src, str):
    with open(reviews_src, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = reviews_src

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Ensure only Children's Books explicitly
bdf = bdf[bdf['categories'].fillna('').str.contains("Children's Books", case=False, regex=False)].copy()

# Fuzzy join hint: purchase_id like 'purchaseid_4' corresponds to book_id 'bookid_4'
# We'll map both to numeric suffix
bdf['id_num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['id_num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# ratings to float
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

# keep valid mapped rows
merged = pd.merge(rdf.dropna(subset=['id_num','rating']), bdf.dropna(subset=['id_num']), on='id_num', how='inner')

agg = (merged.groupby(['book_id','title','author'], dropna=False)
            .agg(avg_rating=('rating','mean'), review_count=('rating','size'))
            .reset_index())

res = agg[agg['avg_rating'] >= 4.5].sort_values(['avg_rating','review_count'], ascending=[False, False])

out = res.to_dict(orient='records')
print('__RESULT__:')
print(json.dumps(out, ensure_ascii=False))"""

env_args = {'var_call_kF382lWp3SOh2h05IBnnvzZ5': 'file_storage/call_kF382lWp3SOh2h05IBnnvzZ5.json', 'var_call_606cSpwU57bNWSqXO9YkOaoc': 'file_storage/call_606cSpwU57bNWSqXO9YkOaoc.json'}

exec(code, env_args)
