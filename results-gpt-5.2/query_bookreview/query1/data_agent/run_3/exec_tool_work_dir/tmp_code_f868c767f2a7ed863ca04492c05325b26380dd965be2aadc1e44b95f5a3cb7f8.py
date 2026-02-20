code = """import json, re, pandas as pd

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_QFnidg1QilCURJVFDsXrK6Hw)  # filtered details
reviews = load_var(var_call_C6zgSVRgtmiCDpwavHeGrcKw)  # per purchase avg

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# parse year from details
year_pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    # prioritize patterns near 'released on' or 'published'
    m = re.search(r'(released on|published on|publication date|published)\s+[^\d]*(19\d{2}|20\d{2})', s, flags=re.I)
    if m:
        return int(m.group(2))
    yrs = [int(x) for x in year_pat.findall(s)]
    if not yrs:
        return None
    # heuristic: take first year mentioned
    return yrs[0]

bdf['year'] = bdf['details'].map(extract_year)
# join by numeric suffix (bookid_123 <-> purchaseid_123)
get_num = lambda x: int(re.search(r'(\d+)$', str(x)).group(1)) if re.search(r'(\d+)$', str(x)) else None
bdf['num'] = bdf['book_id'].map(get_num)
rdf['num'] = rdf['purchase_id'].map(get_num)

# keep rated books (at least 1 review)
rdf['avg_rating'] = pd.to_numeric(rdf['avg_rating'], errors='coerce')

j = pd.merge(bdf[['num','year']], rdf[['num','avg_rating']], on='num', how='inner')
j = j.dropna(subset=['year','avg_rating'])
j['decade'] = (j['year'] // 10) * 10

# decades with at least 10 distinct books rated
agg = j.groupby('decade').agg(n_books=('num','nunique'), avg_rating=('avg_rating','mean')).reset_index()
agg = agg[agg['n_books'] >= 10].sort_values(['avg_rating','n_books','decade'], ascending=[False, False, True])

if agg.empty:
    res = None
else:
    top = agg.iloc[0]
    res = f"{int(top['decade'])}s"

print('__RESULT__:')
print(json.dumps({'decade': res}))"""

env_args = {'var_call_QFnidg1QilCURJVFDsXrK6Hw': 'file_storage/call_QFnidg1QilCURJVFDsXrK6Hw.json', 'var_call_C6zgSVRgtmiCDpwavHeGrcKw': 'file_storage/call_C6zgSVRgtmiCDpwavHeGrcKw.json', 'var_call_H0efNVFj6KqhiH5285nHwEt3': 'file_storage/call_H0efNVFj6KqhiH5285nHwEt3.json', 'var_call_xs8urfo7aZyfQTziFUMxthxk': [{'n': '200'}]}

exec(code, env_args)
