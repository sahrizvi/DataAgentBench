code = """import json, re, pandas as pd

# load reviews per book
rev_src = var_call_gHFDTzzAhVbl28RxQSCg7uCX
if isinstance(rev_src, str):
    with open(rev_src, 'r') as f:
        rev = json.load(f)
else:
    rev = rev_src

df_rev = pd.DataFrame(rev)
if df_rev.empty:
    out = {"decade": None}
    print('__RESULT__:')
    print(json.dumps(out))
    raise SystemExit

df_rev['purchase_id'] = df_rev['purchase_id'].astype(str)
df_rev['book_id'] = df_rev['purchase_id'].str.replace('purchaseid_', 'bookid_', regex=False)
df_rev['avg_rating'] = pd.to_numeric(df_rev['avg_rating'], errors='coerce')

# load books details
books_src = var_call_SGJhVuZNBFeEFOXsLI98F3Hs
if isinstance(books_src, str):
    with open(books_src, 'r') as f:
        books = json.load(f)
else:
    books = books_src

df_books = pd.DataFrame(books)
df_books['book_id'] = df_books['book_id'].astype(str)
df_books['details'] = df_books['details'].astype(str)

# extract year from details
year_re = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not s or s=='nan':
        return None
    m = year_re.findall(s)
    if not m:
        return None
    # heuristic: use first year mentioned (usually publication date)
    return int(m[0])

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year'])
df_books['year'] = df_books['year'].astype(int)
df_books['decade_start'] = (df_books['year']//10)*10

# join
m = df_rev.merge(df_books[['book_id','decade_start']], on='book_id', how='inner')
m = m.dropna(subset=['avg_rating','decade_start'])

# decade stats: distinct books with ratings
stats = (m.groupby('decade_start')
           .agg(distinct_books=('book_id','nunique'),
                avg_rating=('avg_rating','mean'))
           .reset_index())

stats = stats[stats['distinct_books']>=10]
if stats.empty:
    out = {"decade": None}
else:
    best = stats.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
    out = {"decade": f"{int(best['decade_start'])}s"}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_qcKLvVrbwn3bH9Nsp4zV7kvU': 'file_storage/call_qcKLvVrbwn3bH9Nsp4zV7kvU.json', 'var_call_xGXqGkyNwU0SoUCjKIy9kYr6': [{'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_191', 'rating': '4'}, {'purchase_id': 'purchaseid_190', 'rating': '4'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '4'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_186', 'rating': '4'}, {'purchase_id': 'purchaseid_115', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '2'}, {'purchase_id': 'purchaseid_188', 'rating': '1'}, {'purchase_id': 'purchaseid_23', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_154', 'rating': '3'}, {'purchase_id': 'purchaseid_99', 'rating': '2'}, {'purchase_id': 'purchaseid_190', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_169', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_194', 'rating': '4'}, {'purchase_id': 'purchaseid_81', 'rating': '5'}, {'purchase_id': 'purchaseid_199', 'rating': '1'}, {'purchase_id': 'purchaseid_48', 'rating': '5'}, {'purchase_id': 'purchaseid_96', 'rating': '5'}, {'purchase_id': 'purchaseid_167', 'rating': '4'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '5'}, {'purchase_id': 'purchaseid_196', 'rating': '4'}, {'purchase_id': 'purchaseid_148', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_145', 'rating': '5'}, {'purchase_id': 'purchaseid_200', 'rating': '5'}, {'purchase_id': 'purchaseid_8', 'rating': '5'}, {'purchase_id': 'purchaseid_178', 'rating': '1'}, {'purchase_id': 'purchaseid_20', 'rating': '5'}, {'purchase_id': 'purchaseid_52', 'rating': '5'}, {'purchase_id': 'purchaseid_159', 'rating': '2'}, {'purchase_id': 'purchaseid_83', 'rating': '5'}, {'purchase_id': 'purchaseid_67', 'rating': '3'}, {'purchase_id': 'purchaseid_3', 'rating': '5'}, {'purchase_id': 'purchaseid_58', 'rating': '4'}, {'purchase_id': 'purchaseid_196', 'rating': '4'}, {'purchase_id': 'purchaseid_95', 'rating': '5'}, {'purchase_id': 'purchaseid_76', 'rating': '5'}, {'purchase_id': 'purchaseid_3', 'rating': '3'}, {'purchase_id': 'purchaseid_62', 'rating': '5'}], 'var_call_gHFDTzzAhVbl28RxQSCg7uCX': 'file_storage/call_gHFDTzzAhVbl28RxQSCg7uCX.json', 'var_call_SGJhVuZNBFeEFOXsLI98F3Hs': 'file_storage/call_SGJhVuZNBFeEFOXsLI98F3Hs.json'}

exec(code, env_args)
