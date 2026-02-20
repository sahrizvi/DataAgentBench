code = """import json, re, pandas as pd

def load_tool_result(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_tool_result(var_call_yRRzdA5BzwFYjghcQdVj5Ijs)
reviews = load_tool_result(var_call_hyFFG2Yo3Ewl1ZyRcgAaz70j)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# parse publication year from details
pat1 = re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*(\d{4})\b', re.IGNORECASE)
pat2 = re.compile(r'\b(?:Published\s+on|published\s+on|Published\s+by|published\s+by|Published)\b.*?\b(\d{4})\b', re.IGNORECASE)
pat3 = re.compile(r'\b(\d{4})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat1.search(s)
    if m:
        return int(m.group(1))
    m = pat2.search(s)
    if m:
        return int(m.group(1))
    # fallback: first plausible year 1500-2026
    for m in pat3.finditer(s):
        y = int(m.group(1))
        if 1500 <= y <= 2026:
            return y
    return None

bdf['pub_year'] = bdf['details'].map(extract_year)
# keep plausible years
bdf = bdf[(bdf['pub_year'].notna()) & (bdf['pub_year']>=1500) & (bdf['pub_year']<=2026)].copy()

# fuzzy join: normalize ids by extracting trailing digits
id_pat = re.compile(r'(\d+)$')

def norm_id(x):
    if x is None:
        return None
    s = str(x)
    m = id_pat.search(s)
    return m.group(1) if m else s

bdf['nid'] = bdf['book_id'].map(norm_id)
rdf['nid'] = rdf['purchase_id'].map(norm_id)

# ratings to float
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf[rdf['rating'].notna()].copy()

m = rdf.merge(bdf[['nid','pub_year']], on='nid', how='inner')
# distinct books that have been rated per decade: use nid
m['decade_start'] = (m['pub_year']//10)*10
m['decade'] = m['decade_start'].astype(int).astype(str) + 's'

# average rating across all reviews within decade
agg = m.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('nid','nunique'),
    n_reviews=('rating','size')
).reset_index()

eligible = agg[agg['distinct_books']>=10].copy()
if eligible.empty:
    result = None
else:
    top = eligible.sort_values(['avg_rating','distinct_books','n_reviews'], ascending=[False,False,False]).iloc[0]
    result = top['decade']

print('__RESULT__:')
print(json.dumps({'decade': result}))"""

env_args = {'var_call_yRRzdA5BzwFYjghcQdVj5Ijs': 'file_storage/call_yRRzdA5BzwFYjghcQdVj5Ijs.json', 'var_call_hyFFG2Yo3Ewl1ZyRcgAaz70j': 'file_storage/call_hyFFG2Yo3Ewl1ZyRcgAaz70j.json'}

exec(code, env_args)
