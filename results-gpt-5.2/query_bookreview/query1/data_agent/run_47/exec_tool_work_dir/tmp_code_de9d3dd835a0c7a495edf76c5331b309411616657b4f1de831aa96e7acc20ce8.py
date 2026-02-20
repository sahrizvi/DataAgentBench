code = """import json, re, pandas as pd

def load_any(v):
    if isinstance(v, str):
        # assume it's a json file path
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_any(var_call_Ae2lKNnAGmsWnzlH1YT1YkaP)
reviews = load_any(var_call_ZKvEfHi8yl1OvB8fK5NLEuzG)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# parse year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    years = [int(y) for y in pat.findall(s)]
    if not years:
        return None
    # pick earliest plausible publication year
    return min(years)

bdf['year'] = bdf['details'].map(extract_year)
# decade label
bdf = bdf.dropna(subset=['year'])
bdf['decade_start'] = (bdf['year']//10)*10
bdf['decade'] = bdf['decade_start'].astype(int).astype(str) + 's'

# fuzzy join: purchaseid_123 <-> bookid_123
bdf['num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# ratings numeric
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['rating','num'])
bdf = bdf.dropna(subset=['num','decade'])

joined = rdf.merge(bdf[['num','book_id','decade']], on='num', how='inner')

# consider distinct books that have been rated
# average rating per decade across all reviews for books in that decade
# and ensure at least 10 distinct books with >=1 rating
agg = joined.groupby('decade').agg(avg_rating=('rating','mean'), distinct_books=('book_id', pd.Series.nunique))
agg = agg[agg['distinct_books']>=10]

if agg.empty:
    out = {'decade': None}
else:
    top = agg.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).head(1)
    out = {'decade': top.index[0], 'avg_rating': float(top['avg_rating'].iloc[0]), 'distinct_books': int(top['distinct_books'].iloc[0])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_Ae2lKNnAGmsWnzlH1YT1YkaP': 'file_storage/call_Ae2lKNnAGmsWnzlH1YT1YkaP.json', 'var_call_ZKvEfHi8yl1OvB8fK5NLEuzG': 'file_storage/call_ZKvEfHi8yl1OvB8fK5NLEuzG.json'}

exec(code, env_args)
