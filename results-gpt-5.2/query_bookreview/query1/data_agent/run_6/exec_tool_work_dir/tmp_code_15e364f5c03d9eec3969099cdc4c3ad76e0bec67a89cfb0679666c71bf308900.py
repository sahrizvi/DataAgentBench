code = """import json, re, pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_Kq9I6jjsl8702CD49K19i70y)
reviews = load_records(var_call_2aR6OB2KDP9kbGQA4TqeYySZ)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract year from details
year_pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = year_pat.findall(s)
    if not m:
        return None
    # choose earliest plausible year mentioned (often publication date)
    years = [int(x) for x in m]
    years = [y for y in years if 1500 <= y <= 2026]
    if not years:
        return None
    return min(years)

bdf['year'] = bdf['details'].map(extract_year)

# fuzzy join: both ids have numeric suffix; map by that
num_pat = re.compile(r'(\d+)')

def extract_num(x):
    if not isinstance(x, str):
        return None
    m = num_pat.findall(x)
    return int(m[-1]) if m else None

bdf['id_num'] = bdf['book_id'].map(extract_num)
rdf['id_num'] = rdf['purchase_id'].map(extract_num)

# clean ratings
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['rating','id_num'])

mdf = rdf.merge(bdf[['id_num','year']], on='id_num', how='inner')
mdf = mdf.dropna(subset=['year'])
mdf['year'] = mdf['year'].astype(int)

mdf['decade_start'] = (mdf['year']//10)*10
mdf['decade'] = mdf['decade_start'].astype(str) + 's'

# ensure at least 10 distinct books with ratings in decade
books_per_decade = mdf.groupby('decade')['id_num'].nunique().rename('distinct_books')
avg_rating = mdf.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).reset_index()
summary = summary[summary['distinct_books']>=10]
if summary.empty:
    result = None
else:
    best = summary.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = {'decade': best['decade'], 'average_rating': float(best['avg_rating']), 'distinct_books': int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_Kq9I6jjsl8702CD49K19i70y': 'file_storage/call_Kq9I6jjsl8702CD49K19i70y.json', 'var_call_2aR6OB2KDP9kbGQA4TqeYySZ': 'file_storage/call_2aR6OB2KDP9kbGQA4TqeYySZ.json'}

exec(code, env_args)
