code = """import json, re, pandas as pd

def load_result(x):
    if isinstance(x, str) and x.endswith('.json'):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_result(var_call_5lMYJld6NjNFQc8lqbBF0tch)
reviews = load_result(var_call_Mw6HkXYjefJcSV364ODkRONa)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

# extract a 4-digit publication year from details
pat = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.findall(s)
    if not m:
        return None
    # choose earliest plausible year in text (often includes reprint year); use min
    yrs = [int(y) for y in m]
    # guard bounds
    yrs = [y for y in yrs if 1800 <= y <= 2026]
    return min(yrs) if yrs else None

df_b['year'] = df_b['details'].map(extract_year)
df_b = df_b.dropna(subset=['year'])
df_b['year'] = df_b['year'].astype(int)

# fuzzy join: map purchaseid_N -> bookid_N
# extract trailing integer from ids

def id_num(s):
    if not isinstance(s, str):
        return None
    m = re.search(r'(\d+)$', s)
    return int(m.group(1)) if m else None

df_b['idnum'] = df_b['book_id'].map(id_num)
df_r['idnum'] = df_r['purchase_id'].map(id_num)

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['idnum','rating'])
df_b = df_b.dropna(subset=['idnum'])

# only consider books that have been rated (at least 1 review)
df = df_r.merge(df_b[['idnum','year']], on='idnum', how='inner')

# decade label
df['decade_start'] = (df['year'] // 10) * 10
df['decade'] = df['decade_start'].astype(int).astype(str) + 's'

# distinct books per decade with at least 1 rating
books_per_decade = df.groupby('decade')['idnum'].nunique()

# average rating per decade over all reviews
avg_rating = df.groupby('decade')['rating'].mean()

eligible = books_per_decade[books_per_decade >= 10].index
res = (avg_rating.loc[eligible].sort_values(ascending=False))
if len(res)==0:
    answer = None
else:
    answer = res.index[0]

print('__RESULT__:')
print(json.dumps({'decade': answer}))"""

env_args = {'var_call_5lMYJld6NjNFQc8lqbBF0tch': 'file_storage/call_5lMYJld6NjNFQc8lqbBF0tch.json', 'var_call_Mw6HkXYjefJcSV364ODkRONa': 'file_storage/call_Mw6HkXYjefJcSV364ODkRONa.json'}

exec(code, env_args)
