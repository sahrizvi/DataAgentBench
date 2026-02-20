code = """import json, re, pandas as pd

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_QqDVm6lqurwGWZaHnS2ilELt)
reviews = load_var(var_call_g4ClZN2EulTFP1FiDwEyUDJ7)

# Parse publication year from details text
# Look for patterns like 'on January 1, 2004', 'on May 20, 1996', 'released on ... 2004', 'from January 1, 1994', etc.
year_re = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(text):
    if text is None:
        return None
    # Prefer year near keywords
    keywords = ['publication', 'published', 'released', 'release', 'edition']
    lt = text.lower()
    positions = [lt.find(k) for k in keywords if lt.find(k) != -1]
    # if keyword found, search in window after earliest keyword
    if positions:
        p = min(positions)
        window = text[p:p+200]
        m = year_re.search(window)
        if m:
            return int(m.group(1))
    # fallback: first 4-digit year
    m = year_re.search(text)
    return int(m.group(1)) if m else None

book_year = []
for r in books:
    y = extract_year(r.get('details'))
    if y is not None:
        book_year.append({'book_id': r.get('book_id'), 'year': y})

book_year_df = pd.DataFrame(book_year).dropna()

rev_df = pd.DataFrame(reviews)
if not rev_df.empty:
    rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
    rev_df = rev_df.dropna(subset=['purchase_id','rating'])

# Fuzzy join: purchaseid_XXX -> bookid_XXX
rev_df['book_id'] = rev_df['purchase_id'].astype(str).str.replace('purchaseid_', 'bookid_', regex=False)

merged = rev_df.merge(book_year_df, on='book_id', how='inner')

if merged.empty:
    out = {'error':'No joined records with publication year and ratings.'}
else:
    merged['decade_start'] = (merged['year']//10)*10
    # only consider decades with at least 10 distinct books that have at least one rating
    books_per_dec = merged.groupby('decade_start')['book_id'].nunique().reset_index(name='distinct_books')
    dec_mean = merged.groupby('decade_start')['rating'].mean().reset_index(name='avg_rating')
    summary = books_per_dec.merge(dec_mean, on='decade_start')
    eligible = summary[summary['distinct_books']>=10].copy()
    if eligible.empty:
        out = {'error':'No decade has at least 10 distinct rated books with publication years found.'}
    else:
        best = eligible.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
        decade_label = f"{int(best['decade_start'])}s"
        out = {'decade': decade_label, 'avg_rating': float(best['avg_rating']), 'distinct_books': int(best['distinct_books'])}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_QqDVm6lqurwGWZaHnS2ilELt': 'file_storage/call_QqDVm6lqurwGWZaHnS2ilELt.json', 'var_call_g4ClZN2EulTFP1FiDwEyUDJ7': 'file_storage/call_g4ClZN2EulTFP1FiDwEyUDJ7.json'}

exec(code, env_args)
