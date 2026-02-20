code = """import json, re, pandas as pd

def load_result(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_result(var_call_ijzCZwaG77DIRdQVdshIcPUU)
reviews = load_result(var_call_4vApzzRwVLNQndQVHiKaqGls)

books_df = pd.DataFrame(books)
rev_df = pd.DataFrame(reviews)

# Extract 4-digit year from details; take first plausible year 1500-2026
pat = re.compile(r'\b(1[5-9]\d{2}|20\d{2})\b')

def extract_year(s):
    if not isinstance(s, str):
        return None
    m = pat.search(s)
    if not m:
        return None
    y = int(m.group(1))
    if 1500 <= y <= 2026:
        return y
    return None

books_df['year'] = books_df['details'].map(extract_year)
books_df = books_df.dropna(subset=['year'])
books_df['year'] = books_df['year'].astype(int)
books_df['decade_start'] = (books_df['year'] // 10) * 10
books_df['decade'] = books_df['decade_start'].astype(str) + 's'

# Fuzzy join: purchaseid_N corresponds to bookid_N
rev_df['purchase_id'] = rev_df['purchase_id'].astype(str)
rev_df['book_id'] = rev_df['purchase_id'].str.replace('purchaseid_', 'bookid_', regex=False)
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['rating'])

merged = rev_df.merge(books_df[['book_id','decade']], on='book_id', how='inner')

# Only decades with at least 10 distinct books that have been rated (appear in merged)
books_per_decade = merged.groupby('decade')['book_id'].nunique()
eligible = books_per_decade[books_per_decade >= 10].index
eligible_df = merged[merged['decade'].isin(eligible)]

decade_avg = eligible_df.groupby('decade')['rating'].mean().sort_values(ascending=False)
if len(decade_avg)==0:
    ans = None
else:
    ans = decade_avg.index[0]

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_ijzCZwaG77DIRdQVdshIcPUU': 'file_storage/call_ijzCZwaG77DIRdQVdshIcPUU.json', 'var_call_4vApzzRwVLNQndQVHiKaqGls': 'file_storage/call_4vApzzRwVLNQndQVHiKaqGls.json'}

exec(code, env_args)
