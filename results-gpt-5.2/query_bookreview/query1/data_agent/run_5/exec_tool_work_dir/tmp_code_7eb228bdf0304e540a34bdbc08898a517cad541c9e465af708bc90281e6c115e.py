code = """import json, re, pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_rvEY34VwXPJFP80xzkVbgEOU)
reviews = load_records(var_call_MYllaSLvynz1J0Jlq8VZ7eGr)

year_re = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')
book_year = []
for r in books:
    bid = r.get('book_id')
    det = r.get('details') or ''
    years = [int(y) for y in year_re.findall(det)]
    y = min(years) if years else None
    if bid is not None and y is not None:
        book_year.append({'book_id': bid, 'year': y})

bdf = pd.DataFrame(book_year)

rdf = pd.DataFrame(reviews)
rdf['rating'] = pd.to_numeric(rdf.get('rating'), errors='coerce')
rdf['purchase_id'] = rdf.get('purchase_id')
rdf = rdf.dropna(subset=['rating','purchase_id'])

if bdf.empty or rdf.empty:
    out = None
else:
    def suffix_num(s):
        if s is None:
            return None
        m = re.search(r'(\d+)$', str(s))
        return int(m.group(1)) if m else None
    bdf['num'] = bdf['book_id'].map(suffix_num)
    rdf['num'] = rdf['purchase_id'].map(suffix_num)
    jdf = rdf.merge(bdf, on='num', how='inner')
    if jdf.empty:
        out = None
    else:
        jdf['decade_start'] = (jdf['year']//10)*10
        g = jdf.groupby('decade_start').agg(avg_rating=('rating','mean'), distinct_books=('book_id','nunique'))
        g = g[g['distinct_books']>=10]
        if g.empty:
            out = None
        else:
            best = g.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).head(1)
            decade = int(best.index[0])
            out = f"{decade}s"

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_rvEY34VwXPJFP80xzkVbgEOU': 'file_storage/call_rvEY34VwXPJFP80xzkVbgEOU.json', 'var_call_MYllaSLvynz1J0Jlq8VZ7eGr': 'file_storage/call_MYllaSLvynz1J0Jlq8VZ7eGr.json'}

exec(code, env_args)
