code = """import json, re, pandas as pd

def load_records(obj):
    if isinstance(obj, str) and obj.endswith('.json'):
        with open(obj, 'r', encoding='utf-8') as f:
            return json.load(f)
    return obj

books = load_records(var_call_OyQ7d54MYhHmvLSWXsYekRqJ)
reviews = load_records(var_call_tKwcqm5mWOIJsRMvGMZJiL0X)

df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

# Extract a 4-digit year from details (use earliest plausible year 1400-2026)
pat = re.compile(r'\b(1[4-9]\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    years = [int(y) for y in pat.findall(s)]
    if not years:
        return None
    # Prefer years that appear near 'released'/'published' if possible
    # simple heuristic: choose minimum year as publication year (captures first edition year)
    y = min(years)
    if y < 1400 or y > 2026:
        return None
    return y

df_books['year'] = df_books['details'].map(extract_year)
df_books = df_books.dropna(subset=['year']).copy()
df_books['year'] = df_books['year'].astype(int)

def decade_label(y):
    d = (y // 10) * 10
    return f"{d}s"

df_books['decade'] = df_books['year'].map(decade_label)

# Fuzzy join between purchase_id and book_id: if both have digits, match by numeric part

def id_num(x):
    if not isinstance(x, str):
        return None
    m = re.search(r'(\d+)', x)
    return int(m.group(1)) if m else None

df_books['idnum'] = df_books['book_id'].map(id_num)
df_reviews['idnum'] = df_reviews['purchase_id'].map(id_num)

# Clean ratings

df_reviews['rating'] = pd.to_numeric(df_reviews['rating'], errors='coerce')
df_reviews = df_reviews.dropna(subset=['rating','idnum'])
df_books = df_books.dropna(subset=['idnum'])

merged = df_reviews.merge(df_books[['idnum','decade']], on='idnum', how='inner')

# Distinct books rated per decade
books_per_decade = merged[['decade','idnum']].drop_duplicates().groupby('decade').size().rename('distinct_books')
ratings_per_decade = merged.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, ratings_per_decade], axis=1).dropna().reset_index()
summary = summary[summary['distinct_books'] >= 10].copy()

if summary.empty:
    result = None
else:
    top = summary.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = top['decade']

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_OyQ7d54MYhHmvLSWXsYekRqJ': 'file_storage/call_OyQ7d54MYhHmvLSWXsYekRqJ.json', 'var_call_tKwcqm5mWOIJsRMvGMZJiL0X': 'file_storage/call_tKwcqm5mWOIJsRMvGMZJiL0X.json'}

exec(code, env_args)
