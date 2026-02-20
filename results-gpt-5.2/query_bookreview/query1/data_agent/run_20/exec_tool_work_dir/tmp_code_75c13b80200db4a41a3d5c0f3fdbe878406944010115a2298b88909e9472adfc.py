code = """import json, re, pandas as pd

def load_result(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_result(var_call_pH1t6h6Z75YVtLPcb3hqSx3O)
reviews = load_result(var_call_ZgAOSeavChgIdqUfXbrlIOvx)

# Parse publication year from details text
pat = re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*(\d{4})\b|\b(\d{4})\b')

def extract_year(s):
    if not s:
        return None
    # prefer year that appears after typical 'on' or 'released/published'
    # first find explicit month day, year
    m = re.search(r'(?:released|published|publication date|pub\.|pub date|first edition|edition)\D{0,40}(?:on\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s*(\d{4})', s, flags=re.I)
    if m:
        return int(m.group(1))
    # else first 4-digit year between 1500 and 2026
    for m in re.finditer(r'\b(\d{4})\b', s):
        y = int(m.group(1))
        if 1500 <= y <= 2026:
            return y
    return None

book_rows = []
for r in books:
    y = extract_year(r.get('details'))
    if y is not None:
        book_rows.append({'book_id': r.get('book_id'), 'year': y})

books_df = pd.DataFrame(book_rows).dropna().drop_duplicates('book_id')

rev_df = pd.DataFrame(reviews)
rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['purchase_id','rating'])

# fuzzy join: map purchaseid_123 -> bookid_123
rev_df['book_id'] = rev_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

merged = rev_df.merge(books_df, on='book_id', how='inner')
merged['decade_start'] = (merged['year'] // 10) * 10

# Only decades with at least 10 distinct books rated
by_decade = merged.groupby('decade_start').agg(
    avg_rating=('rating','mean'),
    distinct_books=('book_id','nunique')
).reset_index()
by_decade = by_decade[by_decade['distinct_books'] >= 10]

if by_decade.empty:
    result = None
else:
    top = by_decade.sort_values(['avg_rating','distinct_books'], ascending=[False, False]).iloc[0]
    result = f"{int(top['decade_start'])}s"

print('__RESULT__:')
print(json.dumps({'decade': result}))"""

env_args = {'var_call_pH1t6h6Z75YVtLPcb3hqSx3O': 'file_storage/call_pH1t6h6Z75YVtLPcb3hqSx3O.json', 'var_call_ZgAOSeavChgIdqUfXbrlIOvx': 'file_storage/call_ZgAOSeavChgIdqUfXbrlIOvx.json'}

exec(code, env_args)
