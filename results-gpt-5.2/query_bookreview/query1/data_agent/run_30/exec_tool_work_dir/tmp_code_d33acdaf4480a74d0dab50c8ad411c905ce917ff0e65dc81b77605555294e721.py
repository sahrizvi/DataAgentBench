code = """import json, re
import pandas as pd

def load_records(x):
    if isinstance(x, str):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_mJtle4mvJlZIvd6IJp8V5Xx4)
reviews = load_records(var_call_GbcjiCQuv1eGgFyjN6t4KknO)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# parse year from details
pat = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

df_b['year'] = df_b['details'].map(extract_year)
df_b = df_b.dropna(subset=['year'])

# fuzzy join approach hinted: map purchaseid_N -> bookid_N
# extract numeric suffix
bnum = df_b['book_id'].astype(str).str.extract(r'(\d+)$')[0]
df_b = df_b.assign(num=pd.to_numeric(bnum, errors='coerce')).dropna(subset=['num'])

rnum = df_r['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
df_r = df_r.assign(num=pd.to_numeric(rnum, errors='coerce'))

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['num','rating'])

# only consider books that have been rated (at least one review)
merged = pd.merge(df_r[['num','rating']], df_b[['num','year']], on='num', how='inner')
# decade
merged['decade_start'] = (merged['year']//10)*10

# distinct books per decade (based on num) with at least one rating
books_per_decade = merged.groupby('decade_start')['num'].nunique().rename('distinct_books')
avg_rating = merged.groupby('decade_start')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).reset_index()
summary = summary[summary['distinct_books']>=10]

if summary.empty:
    ans = None
else:
    best = summary.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
    ans = f"{int(best['decade_start'])}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_mJtle4mvJlZIvd6IJp8V5Xx4': 'file_storage/call_mJtle4mvJlZIvd6IJp8V5Xx4.json', 'var_call_GbcjiCQuv1eGgFyjN6t4KknO': 'file_storage/call_GbcjiCQuv1eGgFyjN6t4KknO.json'}

exec(code, env_args)
