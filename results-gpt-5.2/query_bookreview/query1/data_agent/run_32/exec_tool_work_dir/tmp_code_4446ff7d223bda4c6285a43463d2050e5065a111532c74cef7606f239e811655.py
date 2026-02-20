code = """import json, re, pandas as pd

def load_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_result(var_call_oyGGy89C46Hn7zquWxlWpHIM)
reviews = load_result(var_call_EhkHLBhdLFefkNnA2QyOE3J1)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Extract 4-digit year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

bdf['year'] = bdf['details'].map(extract_year)

# Fuzzy join: normalize ids by extracting trailing integer
id_pat = re.compile(r'(\d+)$')

def norm_id(s):
    if not isinstance(s, str):
        return None
    m = id_pat.search(s)
    return m.group(1) if m else None

bdf['nid'] = bdf['book_id'].map(norm_id)
rdf['nid'] = rdf['purchase_id'].map(norm_id)

# Clean rating
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

j = rdf.merge(bdf[['nid','year']], on='nid', how='inner')
j = j.dropna(subset=['rating','year'])
j['year'] = j['year'].astype(int)
j['decade'] = (j['year']//10)*10

# Only decades with at least 10 distinct books that have been rated
# Count distinct nid per decade
books_per_decade = j.groupby('decade')['nid'].nunique()
eligible = books_per_decade[books_per_decade >= 10].index
j2 = j[j['decade'].isin(eligible)]

avg_rating = j2.groupby('decade')['rating'].mean()
if len(avg_rating)==0:
    ans = None
else:
    best_decade = int(avg_rating.idxmax())
    ans = f"{best_decade}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_oyGGy89C46Hn7zquWxlWpHIM': 'file_storage/call_oyGGy89C46Hn7zquWxlWpHIM.json', 'var_call_EhkHLBhdLFefkNnA2QyOE3J1': 'file_storage/call_EhkHLBhdLFefkNnA2QyOE3J1.json'}

exec(code, env_args)
