code = """import json, re
import pandas as pd

def load_records(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_records(var_call_JSko08SaUv7w2SXgj9QasWd0)
reviews = load_records(var_call_rlK788v7lEOQzXxXpDPYfJCx)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract publication year from details (take first plausible 4-digit year)
years = []
for s in df_books['details'].fillna(''):
    m = re.findall(r'\b(18\d{2}|19\d{2}|20\d{2})\b', s)
    years.append(int(m[0]) if m else None)
df_books['pub_year'] = years

# Fuzzy join: ids share numeric suffix
extract_num = lambda x: int(re.search(r'(\d+)$', str(x)).group(1)) if re.search(r'(\d+)$', str(x)) else None

df_books['id_num'] = df_books['book_id'].map(extract_num)
df_reviews['id_num'] = df_reviews['purchase_id'].map(extract_num)

df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')

df = df_reviews.merge(df_books[['id_num','pub_year']], on='id_num', how='inner')
# only books that have been rated and have pub_year

df = df.dropna(subset=['rating','pub_year'])

df['decade_start'] = (df['pub_year']//10)*10

# distinct books per decade with at least one rating
books_per_decade = df.groupby('decade_start')['id_num'].nunique()
eligible_decades = books_per_decade[books_per_decade >= 10].index

df_elig = df[df['decade_start'].isin(eligible_decades)]

avg_rating = df_elig.groupby('decade_start')['rating'].mean().sort_values(ascending=False)
if len(avg_rating)==0:
    result = None
else:
    top_decade = int(avg_rating.index[0])
    result = f"{top_decade}s"

print('__RESULT__:')
print(json.dumps({'top_decade': result}))"""

env_args = {'var_call_JSko08SaUv7w2SXgj9QasWd0': 'file_storage/call_JSko08SaUv7w2SXgj9QasWd0.json', 'var_call_rlK788v7lEOQzXxXpDPYfJCx': 'file_storage/call_rlK788v7lEOQzXxXpDPYfJCx.json'}

exec(code, env_args)
