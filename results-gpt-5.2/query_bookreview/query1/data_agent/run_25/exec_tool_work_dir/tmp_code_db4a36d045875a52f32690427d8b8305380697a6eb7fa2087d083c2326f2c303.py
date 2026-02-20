code = """import json, re
import pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_36znDMBtOkeNr9riqxGiO73s)
reviews = load_records(var_call_5EZpQJjRpjY83aPPrihDAjyi)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# year extraction
month = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
patterns = [
    re.compile(r'\b(?:Published|published)\b[^\d]{0,40}(\d{4})'),
    re.compile(r'\b(?:Publication|publication)\b[^\d]{0,40}(\d{4})'),
    re.compile(r'\b(?:Released|released)\b[^\d]{0,40}(\d{4})'),
    re.compile(r'\b(?:on|On)\s+'+month+r'\s+\d{1,2},\s*(\d{4})'),
    re.compile(r'\b'+month+r'\s+\d{1,2},\s*(\d{4})'),
]
year_pat = re.compile(r'\b(\d{4})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    for pat in patterns:
        m = pat.search(text)
        if m:
            y = int(m.group(1))
            if 1500 <= y <= 2026:
                return y
    years = [int(y) for y in year_pat.findall(text)]
    years = [y for y in years if 1500 <= y <= 2026]
    return years[0] if years else None

bdf['year'] = bdf['details'].apply(extract_year)
bdf = bdf.dropna(subset=['year']).copy()
bdf['year'] = bdf['year'].astype(int)

bdf['key'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['key'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['key','rating'])

j = rdf.merge(bdf[['key','year']], on='key', how='inner')

j['decade_start'] = (j['year']//10)*10
j['decade'] = j['decade_start'].astype(int).astype(str) + 's'

grp = j.groupby('decade').agg(
    avg_rating=('rating','mean'),
    distinct_books=('key', pd.Series.nunique)
).reset_index()

eligible = grp[grp['distinct_books']>=10].copy()
if eligible.empty:
    out = {"decade": None, "note": "No decade has >=10 distinct rated books after join."}
else:
    top = eligible.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    out = {"decade": str(top['decade'])}

print('__RESULT__:')
print(json.dumps({"top": out, "eligible": eligible.sort_values('avg_rating', ascending=False).to_dict(orient='records'), "all": grp.sort_values('distinct_books', ascending=False).to_dict(orient='records')}))"""

env_args = {'var_call_nuWYADeHCSdr0FMNeOqFkvJt': 'file_storage/call_nuWYADeHCSdr0FMNeOqFkvJt.json', 'var_call_5EZpQJjRpjY83aPPrihDAjyi': 'file_storage/call_5EZpQJjRpjY83aPPrihDAjyi.json', 'var_call_jWREfBZxjbuos3PeCJPKppLu': {'decade': None}, 'var_call_36znDMBtOkeNr9riqxGiO73s': 'file_storage/call_36znDMBtOkeNr9riqxGiO73s.json'}

exec(code, env_args)
