code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_TtPjHTJg0oEAeCS9t1tIdJFn)
reviews = load_records(var_call_QInls4Vw6dDEN6Eb6KOHPSbZ)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Extract publication year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    # Prefer years near 'published'/'publication'
    lower = s.lower()
    idxs = [lower.find('published'), lower.find('publication')]
    idxs = [i for i in idxs if i != -1]
    if idxs:
        i = min(idxs)
        window = s[max(0,i-80):i+120]
        m = pat.search(window)
        if m:
            return int(m.group(1))
    m = pat.search(s)
    return int(m.group(1)) if m else None

bdf['year'] = bdf['details'].map(extract_year)
bdf = bdf.dropna(subset=['year'])

# Fuzzy join: map purchaseid_X -> bookid_X by extracting trailing integer
id_pat = re.compile(r'(\d+)$')

def extract_num(x):
    if not isinstance(x, str):
        return None
    m = id_pat.search(x)
    return int(m.group(1)) if m else None

bdf['idnum'] = bdf['book_id'].map(extract_num)
rdf['idnum'] = rdf['purchase_id'].map(extract_num)

# Clean rating
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['rating','idnum'])

# Only books that have been rated (at least 1 review)
merged = pd.merge(rdf[['idnum','rating']], bdf[['idnum','year']], on='idnum', how='inner')

merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# compute decade stats among decades with at least 10 distinct books rated
# distinct books per decade
books_per_decade = merged[['decade','idnum']].drop_duplicates().groupby('decade').size().rename('distinct_books')
avg_rating = merged.groupby('decade')['rating'].mean().rename('avg_rating')
stat = pd.concat([books_per_decade, avg_rating], axis=1).dropna()
stat = stat[stat['distinct_books']>=10]

if stat.empty:
    ans = None
else:
    best = stat.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    ans = best.name

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_TtPjHTJg0oEAeCS9t1tIdJFn': 'file_storage/call_TtPjHTJg0oEAeCS9t1tIdJFn.json', 'var_call_QInls4Vw6dDEN6Eb6KOHPSbZ': 'file_storage/call_QInls4Vw6dDEN6Eb6KOHPSbZ.json'}

exec(code, env_args)
