code = """import json, re
import pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_hMcgAeC4fKNuYSYnJNuEWoRy)
reviews = load_records(var_call_UJTZrax6oim9MVkpOIehHAwu)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# extract 4-digit year from details
pattern = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pattern.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1800 <= y <= 2026:
        return y
    return None

bdf['year'] = bdf['details'].map(extract_year)
# fuzzy join purchase_id -> book_id by numeric suffix

def suffix_num(x):
    if not isinstance(x, str):
        return None
    m = re.search(r'(\d+)$', x)
    return int(m.group(1)) if m else None

bdf['sid'] = bdf['book_id'].map(suffix_num)
rdf['sid'] = rdf['purchase_id'].map(suffix_num)

# keep only rated reviews and valid years
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')

merged = pd.merge(rdf.dropna(subset=['sid','rating']), bdf.dropna(subset=['sid','year']), on='sid', how='inner')

# decade
merged['decade_start'] = (merged['year'] // 10) * 10
merged['decade'] = merged['decade_start'].astype('Int64').astype(str) + 's'

# count distinct books rated per decade
books_per_decade = merged.groupby('decade')['sid'].nunique().rename('distinct_books')
avg_rating = merged.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).reset_index()
summary = summary[summary['distinct_books'] >= 10]

if summary.empty:
    result = None
else:
    top = summary.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = {'decade': top['decade'], 'avg_rating': float(top['avg_rating']), 'distinct_books': int(top['distinct_books'])}

print('__RESULT__:')
print(json.dumps(result))"""

env_args = {'var_call_hMcgAeC4fKNuYSYnJNuEWoRy': 'file_storage/call_hMcgAeC4fKNuYSYnJNuEWoRy.json', 'var_call_UJTZrax6oim9MVkpOIehHAwu': 'file_storage/call_UJTZrax6oim9MVkpOIehHAwu.json'}

exec(code, env_args)
