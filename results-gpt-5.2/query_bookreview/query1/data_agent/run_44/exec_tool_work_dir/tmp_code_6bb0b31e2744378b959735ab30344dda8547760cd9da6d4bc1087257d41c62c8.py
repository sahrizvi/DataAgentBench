code = """import json, re
import pandas as pd

# load large json files
with open(var_call_Nrd0JbOPSOEOYpfUhTLVIJWC, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_ZGmXUh7YQLkOizea1lQes7fG, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# parse year from details
year_re = re.compile(r'\b(?:19|20)\d{2}\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = year_re.findall(s)
    if not m:
        return None
    # choose earliest plausible year mentioned
    years = [int(x) for x in m]
    years = [y for y in years if 1500 <= y <= 2026]
    return min(years) if years else None

bdf['year'] = bdf['details'].map(extract_year)
# decade label
bdf['decade_start'] = (bdf['year'] // 10) * 10
bdf['decade'] = bdf['decade_start'].apply(lambda x: f"{int(x)}s" if pd.notna(x) else None)

# fuzzy join via numeric suffix
bdf['id_num'] = bdf['book_id'].astype(str).str.extract(r'(\d+)$')[0]
rdf['id_num'] = rdf['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]

# clean rating
rdf['rating'] = pd.to_numeric(rdf['rating'], errors='coerce')
rdf = rdf.dropna(subset=['rating','id_num'])

# distinct books that have been rated: based on id_num present in reviews
rated_books = rdf[['id_num']].drop_duplicates()
merged = rated_books.merge(bdf[['id_num','decade']], on='id_num', how='left').dropna(subset=['decade'])

# map each review to decade via id_num
rev_with_decade = rdf.merge(bdf[['id_num','decade']], on='id_num', how='left').dropna(subset=['decade'])

# compute avg rating per decade, but only decades with >=10 distinct rated books
book_counts = merged.groupby('decade')['id_num'].nunique().reset_index(name='distinct_books')
avg_ratings = rev_with_decade.groupby('decade')['rating'].mean().reset_index(name='avg_rating')
stats = book_counts.merge(avg_ratings, on='decade', how='inner')
stats = stats[stats['distinct_books']>=10]

if stats.empty:
    result = None
else:
    top = stats.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = top['decade']

print('__RESULT__:')
print(json.dumps({'decade': result}))"""

env_args = {'var_call_Nrd0JbOPSOEOYpfUhTLVIJWC': 'file_storage/call_Nrd0JbOPSOEOYpfUhTLVIJWC.json', 'var_call_ZGmXUh7YQLkOizea1lQes7fG': 'file_storage/call_ZGmXUh7YQLkOizea1lQes7fG.json'}

exec(code, env_args)
