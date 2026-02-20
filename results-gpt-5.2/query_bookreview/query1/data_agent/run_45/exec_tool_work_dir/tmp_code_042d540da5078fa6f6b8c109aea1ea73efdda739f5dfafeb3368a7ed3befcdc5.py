code = """import json, re, pandas as pd

books_src = var_call_PfosPUuGQj93AMlUWgB2POIv
if isinstance(books_src, str):
    with open(books_src, 'r') as f:
        books = json.load(f)
else:
    books = books_src

reviews_src = var_call_EwE3Ao33qYrTv280d5AocnVc
if isinstance(reviews_src, str):
    with open(reviews_src, 'r') as f:
        reviews = json.load(f)
else:
    reviews = reviews_src

year_pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not s:
        return None
    years = [int(x) for x in year_pat.findall(str(s))]
    years = [y for y in years if 1800 <= y <= 2026]
    return min(years) if years else None

book_rows = []
for r in books:
    bid = r.get('book_id')
    y = extract_year(r.get('details'))
    if bid and y:
        book_rows.append({'book_id': str(bid), 'year': y})

books_df = pd.DataFrame(book_rows)
if not books_df.empty:
    books_df = books_df.drop_duplicates('book_id')

num_pat = re.compile(r'(\d+)$')

def suffix_num(x):
    if x is None:
        return None
    m = num_pat.search(str(x))
    return m.group(1) if m else None

books_df['num'] = books_df['book_id'].map(suffix_num)

rev_df = pd.DataFrame(reviews)
rev_df = rev_df.dropna(subset=['purchase_id','rating'])
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['rating'])
rev_df['num'] = rev_df['purchase_id'].map(suffix_num)

joined = rev_df.merge(books_df[['book_id','year','num']], on='num', how='inner')
joined['decade_start'] = (joined['year']//10)*10
joined['decade'] = joined['decade_start'].astype(int).astype(str) + 's'

agg = joined.groupby('decade').agg(distinct_books=('book_id','nunique'), avg_rating=('rating','mean')).reset_index()
agg = agg[agg['distinct_books'] >= 10]

if agg.empty:
    result = None
else:
    best = agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = {'decade': best['decade'], 'avg_rating': float(best['avg_rating']), 'distinct_books': int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_LzalIqB510Mg5NVQmMLxkmOw': 'file_storage/call_LzalIqB510Mg5NVQmMLxkmOw.json', 'var_call_EwE3Ao33qYrTv280d5AocnVc': 'file_storage/call_EwE3Ao33qYrTv280d5AocnVc.json', 'var_call_vi1Yk3ghVhrdHq3aE0UDf3TU': None, 'var_call_PfosPUuGQj93AMlUWgB2POIv': 'file_storage/call_PfosPUuGQj93AMlUWgB2POIv.json'}

exec(code, env_args)
