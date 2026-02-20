code = """import json, re
import pandas as pd

def load_records(obj):
    if isinstance(obj, str):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

books = load_records(var_call_x6BRW0x0EBHaUK6NdlOzQeCt)
reviews = load_records(var_call_N5pRYW9qeGasiqnbL1D2iGcK)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1500 <= y <= 2026:
        return y
    return None

bdf['year'] = bdf['details'].map(extract_year)
# fuzzy join: map purchaseid_N -> bookid_N

def norm_id(x):
    if not isinstance(x, str):
        return None
    m = re.search(r'(\d+)$', x)
    return m.group(1) if m else None

bdf['idnum'] = bdf['book_id'].map(norm_id)
rdf['idnum'] = rdf['purchase_id'].map(norm_id)

# keep rated books with known year
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
joined = pd.merge(rdf[['idnum','rating']], bdf[['idnum','year']], on='idnum', how='inner')
joined = joined.dropna(subset=['rating','year'])
joined['year'] = joined['year'].astype(int)
joined['decade'] = (joined['year']//10)*10

# require at least 10 distinct books that have been rated in that decade
# distinct books = distinct idnum present in joined
books_per_decade = joined.groupby('decade')['idnum'].nunique().rename('distinct_books')
avg_rating_per_decade = joined.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating_per_decade], axis=1).reset_index()
summary = summary[summary['distinct_books']>=10]
if summary.empty:
    result = None
else:
    top = summary.sort_values(['avg_rating','distinct_books','decade'], ascending=[False, False, True]).iloc[0]
    result = f"{int(top['decade'])}s"

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_x6BRW0x0EBHaUK6NdlOzQeCt': 'file_storage/call_x6BRW0x0EBHaUK6NdlOzQeCt.json', 'var_call_N5pRYW9qeGasiqnbL1D2iGcK': 'file_storage/call_N5pRYW9qeGasiqnbL1D2iGcK.json'}

exec(code, env_args)
