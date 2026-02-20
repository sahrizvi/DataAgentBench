code = """import json, re, pandas as pd

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_9Imk4t4zwgo6ICYdQnKwIi3I)
reviews = load_var(var_call_C6zgSVRgtmiCDpwavHeGrcKw)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

year_pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(released on|published on|publication date|published)\s+[^\d]*(19\d{2}|20\d{2})', s, flags=re.I)
    if m:
        return int(m.group(2))
    yrs = [int(x) for x in year_pat.findall(s)]
    return yrs[0] if yrs else None

bdf['year'] = bdf['details'].map(extract_year)
get_num = lambda x: int(re.search(r'(\d+)$', str(x)).group(1)) if re.search(r'(\d+)$', str(x)) else None
bdf['num'] = bdf['book_id'].map(get_num)
rdf['num'] = rdf['purchase_id'].map(get_num)
rdf['avg_rating'] = pd.to_numeric(rdf['avg_rating'], errors='coerce')

j = pd.merge(bdf[['num','year']], rdf[['num','avg_rating']], on='num', how='inner')
j = j.dropna(subset=['year','avg_rating'])
j['decade'] = (j['year']//10)*10

agg = j.groupby('decade').agg(n_books=('num','nunique'), avg_rating=('avg_rating','mean')).reset_index()
agg2 = agg[agg['n_books']>=10].sort_values(['avg_rating','n_books','decade'], ascending=[False, False, True])
res = None if agg2.empty else f"{int(agg2.iloc[0]['decade'])}s"

print('__RESULT__:')
print(json.dumps({'decade': res, 'table': agg2.to_dict(orient='records')}))"""

env_args = {'var_call_QFnidg1QilCURJVFDsXrK6Hw': 'file_storage/call_QFnidg1QilCURJVFDsXrK6Hw.json', 'var_call_C6zgSVRgtmiCDpwavHeGrcKw': 'file_storage/call_C6zgSVRgtmiCDpwavHeGrcKw.json', 'var_call_H0efNVFj6KqhiH5285nHwEt3': 'file_storage/call_H0efNVFj6KqhiH5285nHwEt3.json', 'var_call_xs8urfo7aZyfQTziFUMxthxk': [{'n': '200'}], 'var_call_NysYIHRsHzaDMcWLoqnmdWg0': {'decade': None}, 'var_call_9Imk4t4zwgo6ICYdQnKwIi3I': 'file_storage/call_9Imk4t4zwgo6ICYdQnKwIi3I.json'}

exec(code, env_args)
