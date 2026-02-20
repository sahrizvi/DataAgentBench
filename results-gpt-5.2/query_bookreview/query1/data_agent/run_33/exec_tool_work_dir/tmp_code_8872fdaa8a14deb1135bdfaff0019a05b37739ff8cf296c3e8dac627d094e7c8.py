code = """import json, re
import pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_gI60eTZlfbi4DnOiV1YjOXIC)
reviews = load_records(var_call_FnSrmENZvvxAhOs1ZVAOLIRJ)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# parse year from details text
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.findall(s)
    if not m:
        return None
    # take the first plausible publication year; often appears after 'released on' or 'published' etc.
    return int(m[0])

bdf['year'] = bdf['details'].map(extract_year)
# fuzzy join: purchaseid_X <-> bookid_X by extracting numeric suffix

def extract_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

bdf['num'] = bdf['book_id'].map(extract_num)
rdf['num'] = rdf['purchase_id'].map(extract_num)

# ensure rating numeric
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

merged = rdf.merge(bdf[['num','year']], on='num', how='inner')
merged = merged.dropna(subset=['year','rating'])
merged['decade_start'] = (merged['year']//10)*10

# distinct books rated per decade: count unique num with at least one rating
books_per_decade = merged.groupby('decade_start')['num'].nunique()
eligible = books_per_decade[books_per_decade >= 10].index

eligible_df = merged[merged['decade_start'].isin(eligible)]
# average rating per decade across all reviews (not per-book)
avg_by_decade = eligible_df.groupby('decade_start')['rating'].mean()
if avg_by_decade.empty:
    ans = None
else:
    best_decade = int(avg_by_decade.idxmax())
    ans = f"{best_decade}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_gI60eTZlfbi4DnOiV1YjOXIC': 'file_storage/call_gI60eTZlfbi4DnOiV1YjOXIC.json', 'var_call_FnSrmENZvvxAhOs1ZVAOLIRJ': 'file_storage/call_FnSrmENZvvxAhOs1ZVAOLIRJ.json'}

exec(code, env_args)
