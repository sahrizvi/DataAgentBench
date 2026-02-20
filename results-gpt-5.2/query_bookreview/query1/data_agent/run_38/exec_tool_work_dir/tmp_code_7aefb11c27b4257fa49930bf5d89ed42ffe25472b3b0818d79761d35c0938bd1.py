code = """import json, re, pandas as pd

def load(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = pd.DataFrame(load(var_call_vN8IIkHjnhFFzDg3qQt85tjf))
reviews = pd.DataFrame(load(var_call_soWJP3KTuHrEVXHkUjv3zAJr))

# extract first 4-digit year from details near published/publication if possible
pattern = re.compile(r'(?i)(?:publish(?:ed|er|ing)?|publication)\D{0,40}((?:19|20)\d{2})|\b((?:19|20)\d{2})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    m = pattern.search(text)
    if not m:
        return None
    y = m.group(1) or m.group(2)
    try:
        y = int(y)
    except:
        return None
    if 1500 <= y <= 2026:
        return y
    return None

books['year'] = books['details'].map(extract_year)
books = books.dropna(subset=['year'])
books['year'] = books['year'].astype(int)

# join by numeric suffix: bookid_123 <-> purchaseid_123
books['idnum'] = books['book_id'].str.extract(r'(\d+)$').astype(float)
reviews['idnum'] = reviews['purchase_id'].str.extract(r'(\d+)$').astype(float)
reviews['rating'] = pd.to_numeric(reviews['rating'], errors='coerce')
reviews = reviews.dropna(subset=['idnum','rating'])
books = books.dropna(subset=['idnum'])

merged = reviews.merge(books[['idnum','year']], on='idnum', how='inner')
merged['decade_start'] = (merged['year']//10)*10
merged['decade'] = merged['decade_start'].astype(int).astype(str) + 's'

# decades with at least 10 distinct books rated
books_per_decade = merged.groupby('decade')['idnum'].nunique().rename('distinct_books')
avg_rating = merged.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).reset_index()
summary = summary[summary['distinct_books'] >= 10]
summary = summary.sort_values(['avg_rating','distinct_books'], ascending=[False,False])

top_decade = None
if len(summary):
    top_decade = summary.iloc[0]['decade']

out = {'decade_with_highest_avg_rating': top_decade}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_vN8IIkHjnhFFzDg3qQt85tjf': 'file_storage/call_vN8IIkHjnhFFzDg3qQt85tjf.json', 'var_call_soWJP3KTuHrEVXHkUjv3zAJr': 'file_storage/call_soWJP3KTuHrEVXHkUjv3zAJr.json'}

exec(code, env_args)
