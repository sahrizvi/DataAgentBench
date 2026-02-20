code = """import json, re, pandas as pd

def load_var(v):
    if isinstance(v, str):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_lAQlC1UPuR4kfRyIpwxvfVGJ)
reviews = load_var(var_call_cBQRx6yFDVXTrDsU6F1M9qp1)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract 4-digit year from details with preference for publication/published contexts
pattern = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(details):
    if details is None:
        return None
    s = str(details)
    # Prefer dates like 'on ... , 2004' or 'January 1, 2004'
    m = re.search(r'(?:on|released on|publication date|published(?: on)?|first edition .*? on)\s+[^\n,]*?,\s*(19\d{2}|20\d{2})', s, flags=re.I)
    if m:
        return int(m.group(1))
    # Otherwise first year occurrence
    m2 = pattern.search(s)
    if m2:
        return int(m2.group(1))
    return None

bdf['year'] = bdf['details'].apply(extract_year)
bdf = bdf.dropna(subset=['year'])

# map purchase_id_X to bookid_X (fuzzy join via numeric suffix)

def suffix_num(x):
    if x is None:
        return None
    m = re.search(r'(\d+)$', str(x))
    return int(m.group(1)) if m else None

bdf['num'] = bdf['book_id'].apply(suffix_num)
rdf['num'] = rdf['purchase_id'].apply(suffix_num)
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['num','rating'])

mdf = rdf.merge(bdf[['num','year']], on='num', how='inner')
mdf['decade'] = (mdf['year']//10)*10

# only decades with at least 10 distinct books that have been rated
books_per_decade = mdf.groupby('decade')['num'].nunique().reset_index(name='distinct_books')
eligible = books_per_decade[books_per_decade['distinct_books']>=10]

if eligible.empty:
    result = None
else:
    elig_decades = set(eligible['decade'].tolist())
    avg_by_decade = mdf[mdf['decade'].isin(elig_decades)].groupby('decade')['rating'].mean().reset_index(name='avg_rating')
    top = avg_by_decade.sort_values(['avg_rating','decade'], ascending=[False, True]).head(1)
    decade = int(top.iloc[0]['decade'])
    result = f"{decade}s"

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_lAQlC1UPuR4kfRyIpwxvfVGJ': 'file_storage/call_lAQlC1UPuR4kfRyIpwxvfVGJ.json', 'var_call_cBQRx6yFDVXTrDsU6F1M9qp1': 'file_storage/call_cBQRx6yFDVXTrDsU6F1M9qp1.json'}

exec(code, env_args)
