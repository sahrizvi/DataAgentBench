code = """import json, re, pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_RQithu3NPmXr4OQ3mUhPud0w)
reviews = load_records(var_call_AkoQa3VClCe5UUb4KT4iWiXi)

df_b = pd.DataFrame(books)
df_r = pd.DataFrame(reviews)

df_r['rating'] = pd.to_numeric(df_r['rating'], errors='coerce')
df_r = df_r.dropna(subset=['rating'])

# Map purchase_id -> book_id by extracting trailing integer and matching bookid_<n>
# This leverages the dataset's synthetic ids.
def id_num(s):
    m = re.search(r'(\d+)$', str(s))
    return int(m.group(1)) if m else None

df_b['id_num'] = df_b['book_id'].map(id_num)
df_r['id_num'] = df_r['purchase_id'].map(id_num)

# Extract publication year from details text
pat_year = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(txt):
    if txt is None:
        return None
    years = [int(y) for y in pat_year.findall(str(txt))]
    if not years:
        return None
    # Prefer plausible publication year: choose the earliest year >= 1400 and <=2026
    years = [y for y in years if 1400 <= y <= 2026]
    if not years:
        return None
    return min(years)

df_b['pub_year'] = df_b['details'].map(extract_year)
df_b = df_b.dropna(subset=['pub_year'])
df_b['pub_year'] = df_b['pub_year'].astype(int)
df_b['decade'] = (df_b['pub_year'] // 10) * 10

# Join reviews to books via id_num
joined = df_r.merge(df_b[['id_num','book_id','decade']], on='id_num', how='inner')

# Only consider distinct books that have at least one rating (implicit)
# Compute book-level average rating, then decade average across books
book_avg = joined.groupby(['book_id','decade'], as_index=False)['rating'].mean().rename(columns={'rating':'book_avg_rating'})

decade_stats = book_avg.groupby('decade').agg(distinct_books=('book_id','nunique'), avg_rating=('book_avg_rating','mean')).reset_index()

decade_stats_eligible = decade_stats[decade_stats['distinct_books'] >= 10].copy()
if decade_stats_eligible.empty:
    result = None
else:
    top = decade_stats_eligible.sort_values(['avg_rating','distinct_books','decade'], ascending=[False, False, True]).iloc[0]
    result = f"{int(top['decade'])}s"

print('__RESULT__:')
print(json.dumps({'decade': result}))"""

env_args = {'var_call_RQithu3NPmXr4OQ3mUhPud0w': 'file_storage/call_RQithu3NPmXr4OQ3mUhPud0w.json', 'var_call_AkoQa3VClCe5UUb4KT4iWiXi': 'file_storage/call_AkoQa3VClCe5UUb4KT4iWiXi.json'}

exec(code, env_args)
