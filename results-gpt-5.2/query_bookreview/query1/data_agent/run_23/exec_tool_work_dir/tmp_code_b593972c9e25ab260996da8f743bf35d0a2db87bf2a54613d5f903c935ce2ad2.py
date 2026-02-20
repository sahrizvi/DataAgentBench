code = """import json, re, pandas as pd

# load books
books_src = var_call_pxLzKnM75iRx8aaEEGquFr68
if isinstance(books_src, str):
    with open(books_src, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_src

# load reviews
rev_src = var_call_u6Bu3E4RmvRaLWggCuK7fp05
if isinstance(rev_src, str):
    with open(rev_src, 'r', encoding='utf-8') as f:
        revs = json.load(f)
else:
    revs = rev_src

books_df = pd.DataFrame(books)
revs_df = pd.DataFrame(revs)

# parse year from details
pat = re.compile(r"\b(19\d{2}|20\d{2})\b")

def extract_year(s):
    if not isinstance(s, str):
        return None
    years = [int(y) for y in pat.findall(s)]
    if not years:
        return None
    # prefer plausible publication years (earliest year often publication)
    # Keep within 1400-2026 just in case
    years = [y for y in years if 1400 <= y <= 2026]
    if not years:
        return None
    return min(years)

books_df['year'] = books_df['details'].map(extract_year)
books_df = books_df.dropna(subset=['year']).copy()
books_df['year'] = books_df['year'].astype(int)
books_df['decade_start'] = (books_df['year']//10)*10
books_df['decade'] = books_df['decade_start'].astype(str) + 's'

# fuzzy join by numeric id extracted
id_pat = re.compile(r"(\d+)")

def num_id(x):
    if not isinstance(x, str):
        return None
    m = id_pat.search(x)
    return int(m.group(1)) if m else None

books_df['num'] = books_df['book_id'].map(num_id)
revs_df['num'] = revs_df['purchase_id'].map(num_id)
revs_df['rating'] = pd.to_numeric(revs_df['rating'], errors='coerce')
revs_df = revs_df.dropna(subset=['num','rating'])

merged = revs_df.merge(books_df[['num','decade','book_id']], on='num', how='inner')

# distinct books with at least one rating per decade
books_per_decade = merged[['decade','book_id']].drop_duplicates().groupby('decade').size().rename('n_books')
ratings_per_decade = merged.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, ratings_per_decade], axis=1).dropna().reset_index()
summary = summary[summary['n_books']>=10]

if summary.empty:
    ans = None
else:
    top = summary.sort_values(['avg_rating','n_books','decade'], ascending=[False, False, True]).iloc[0]
    ans = str(top['decade'])

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_pxLzKnM75iRx8aaEEGquFr68': 'file_storage/call_pxLzKnM75iRx8aaEEGquFr68.json', 'var_call_u6Bu3E4RmvRaLWggCuK7fp05': 'file_storage/call_u6Bu3E4RmvRaLWggCuK7fp05.json'}

exec(code, env_args)
