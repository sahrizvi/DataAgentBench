code = """import json, re, pandas as pd
from pathlib import Path

def load_records(var):
    if isinstance(var, str) and var.endswith('.json'):
        return json.loads(Path(var).read_text())
    return var

books = load_records(var_call_funTcbZlEEtSdgNp58sDIHta)
reviews = load_records(var_call_2LLVP7tIYlkRhWAZkXKuE5Z1)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Extract 4-digit year from details
pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if s is None:
        return None
    m = pat.search(str(s))
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

bdf['year'] = bdf['details'].map(extract_year)
# Fuzzy join approach per hint: ids differ by 'bookid_' vs 'purchaseid_'
# Map numeric suffix
bdf['id_num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['id_num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# Keep only rated reviews
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['rating','id_num'])

# Join
j = pd.merge(rdf, bdf[['id_num','year']], on='id_num', how='inner')
j = j.dropna(subset=['year'])
j['year'] = j['year'].astype(int)

# decade label
def decade_label(y):
    d = (y//10)*10
    return f"{d}s"

j['decade'] = j['year'].map(decade_label)

# Only decades with at least 10 distinct books that have been rated (i.e., appear in j)
# Count distinct id_num per decade
agg_books = j.groupby('decade')['id_num'].nunique().rename('distinct_books')
agg_rating = j.groupby('decade')['rating'].mean().rename('avg_rating')
agg = pd.concat([agg_books, agg_rating], axis=1).reset_index()
agg = agg[agg['distinct_books']>=10]

if agg.empty:
    best = None
else:
    best_row = agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    best = best_row['decade']

print('__RESULT__:')
print(json.dumps({'best_decade': best}))"""

env_args = {'var_call_funTcbZlEEtSdgNp58sDIHta': 'file_storage/call_funTcbZlEEtSdgNp58sDIHta.json', 'var_call_2LLVP7tIYlkRhWAZkXKuE5Z1': 'file_storage/call_2LLVP7tIYlkRhWAZkXKuE5Z1.json'}

exec(code, env_args)
