code = """import json, re, pandas as pd

def load_json_maybe(path_or_obj):
    if isinstance(path_or_obj, str) and path_or_obj.endswith('.json'):
        with open(path_or_obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return path_or_obj

books = load_json_maybe(var_call_FPs0BHBAf1VPqMCvtLMYY77O)
reviews = load_json_maybe(var_call_sVR7zBK0tiEa8GKAGvztiJYt)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Extract 4-digit year from details
pattern = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if s is None:
        return None
    m = pattern.search(str(s))
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

bdf['year'] = bdf['details'].map(extract_year)
# Fuzzy join hint: ids differ by prefix bookid_ vs purchaseid_
# Map purchase_id numeric suffix to book_id suffix
bdf['suffix'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['suffix'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

j = rdf.merge(bdf[['suffix','year']], on='suffix', how='inner')
# only keep rows with year and rating
j = j.dropna(subset=['year','rating'])
j['year'] = j['year'].astype(int)

# decade label
j['decade_start'] = (j['year']//10)*10
j['decade'] = j['decade_start'].astype(str) + 's'

# compute distinct books with at least one rating in that decade
books_per_decade = j.groupby('decade')['suffix'].nunique()
mean_rating = j.groupby('decade')['rating'].mean()
res = pd.DataFrame({'distinct_books': books_per_decade, 'avg_rating': mean_rating}).reset_index()
res = res[res['distinct_books']>=10]
if len(res)==0:
    out = {'decade': None}
else:
    top = res.sort_values(['avg_rating','distinct_books'], ascending=[False,False]).iloc[0]
    out = {'decade': top['decade'], 'avg_rating': float(top['avg_rating']), 'distinct_books': int(top['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_FPs0BHBAf1VPqMCvtLMYY77O': 'file_storage/call_FPs0BHBAf1VPqMCvtLMYY77O.json', 'var_call_sVR7zBK0tiEa8GKAGvztiJYt': 'file_storage/call_sVR7zBK0tiEa8GKAGvztiJYt.json'}

exec(code, env_args)
