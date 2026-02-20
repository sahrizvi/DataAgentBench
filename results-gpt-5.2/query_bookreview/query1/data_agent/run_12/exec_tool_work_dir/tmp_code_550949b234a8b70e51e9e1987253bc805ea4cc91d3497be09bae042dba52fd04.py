code = """import json, re, pandas as pd

def load(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load(var_call_hUDn4mAdDecvDozwuvCYiC5h)
reviews = load(var_call_2acwakoA64xEDHfsDo3vCqYK)

# Parse year from details
pat_year = re.compile(r'\b(18\d{2}|19\d{2}|20\d{2})\b')

def extract_year(s):
    if not s:
        return None
    # prioritize patterns like 'on Month dd, yyyy' or 'on yyyy' by taking last year in string
    yrs = pat_year.findall(s)
    if not yrs:
        return None
    y = int(yrs[-1])
    if 1800 <= y <= 2026:
        return y
    return None

book_year = {}
for r in books:
    y = extract_year(r.get('details'))
    if y is not None:
        book_year[r['book_id']] = y

# Build review stats per purchase_id
rev_df = pd.DataFrame(reviews)
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['purchase_id','rating'])

# fuzzy join: purchaseid_XXX -> bookid_XXX
rev_df['book_id'] = rev_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

rev_df = rev_df[rev_df['book_id'].isin(book_year.keys())].copy()
rev_df['year'] = rev_df['book_id'].map(book_year)
rev_df = rev_df.dropna(subset=['year'])
rev_df['decade_start'] = (rev_df['year']//10)*10
rev_df['decade'] = rev_df['decade_start'].astype(int).astype(str) + 's'

# compute average rating per distinct book within decade: first avg per book, then average those
book_avg = rev_df.groupby(['decade','book_id'], as_index=False)['rating'].mean()
decade_stats = book_avg.groupby('decade', as_index=False).agg(distinct_books=('book_id','nunique'), avg_rating=('rating','mean'))
decade_stats = decade_stats[decade_stats['distinct_books']>=10]

if len(decade_stats)==0:
    ans = None
else:
    top = decade_stats.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    ans = {'decade': top['decade'], 'avg_rating': float(top['avg_rating']), 'distinct_books': int(top['distinct_books'])}

print('__RESULT__:')
print(json.dumps(ans))"""

env_args = {'var_call_hUDn4mAdDecvDozwuvCYiC5h': 'file_storage/call_hUDn4mAdDecvDozwuvCYiC5h.json', 'var_call_2acwakoA64xEDHfsDo3vCqYK': 'file_storage/call_2acwakoA64xEDHfsDo3vCqYK.json'}

exec(code, env_args)
