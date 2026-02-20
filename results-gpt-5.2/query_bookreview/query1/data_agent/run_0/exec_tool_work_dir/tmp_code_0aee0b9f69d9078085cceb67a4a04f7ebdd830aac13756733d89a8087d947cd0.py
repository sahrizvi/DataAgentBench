code = """import json, re, pandas as pd

def load_var(v):
    if isinstance(v, str) and v.endswith('.json'):
        with open(v, 'r', encoding='utf-8') as f:
            return json.load(f)
    return v

books = load_var(var_call_XoYnvxOPLY9VHnqTfDG0UtfW)
reviews = load_var(var_call_11ksGZ7Es4f02ryiOdid5TfD)

book_df = pd.DataFrame(books)
rev_df = pd.DataFrame(reviews)

# Parse year from details
year_re = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(text):
    if not isinstance(text, str):
        return None
    keywords = ['publication date', 'published', 'publication', 'released', 'release', 'edition']
    lt = text.lower()
    pos = None
    for k in keywords:
        p = lt.find(k)
        if p != -1:
            pos = p if pos is None else min(pos, p)
    if pos is not None:
        window = text[pos:pos+250]
        m = year_re.search(window)
        if m:
            return int(m.group(1))
    m = year_re.search(text)
    return int(m.group(1)) if m else None

book_df['year'] = book_df['details'].apply(extract_year)
book_year_df = book_df[['book_id','year']].dropna().copy()
book_year_df['year'] = book_year_df['year'].astype(int)

rev_df['rating'] = pd.to_numeric(rev_df['rating'], errors='coerce')
rev_df = rev_df.dropna(subset=['purchase_id','rating'])

# Determine actual mapping by comparing numeric suffix overlap
rev_df['suffix'] = rev_df['purchase_id'].astype(str).str.extract(r'(\d+)$')[0]
book_year_df['suffix'] = book_year_df['book_id'].astype(str).str.extract(r'(\d+)$')[0]

merged = rev_df.merge(book_year_df, on='suffix', how='inner', suffixes=('_rev','_book'))

if merged.empty:
    out = {'error':'No joined records after suffix join.'}
else:
    merged['decade_start'] = (merged['year']//10)*10
    # distinct books: use book_id
    books_per_dec = merged.groupby('decade_start')['book_id'].nunique().reset_index(name='distinct_books')
    dec_mean = merged.groupby('decade_start')['rating'].mean().reset_index(name='avg_rating')
    summary = books_per_dec.merge(dec_mean, on='decade_start')
    eligible = summary[summary['distinct_books']>=10].copy()
    if eligible.empty:
        out = {'error':'No decade has at least 10 distinct rated books with publication years found.',
               'decade_counts': summary.sort_values('distinct_books', ascending=False).head(20).to_dict('records')}
    else:
        best = eligible.sort_values(['avg_rating','distinct_books','decade_start'], ascending=[False,False,True]).iloc[0]
        out = {'decade': f"{int(best['decade_start'])}s"}

print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_QqDVm6lqurwGWZaHnS2ilELt': 'file_storage/call_QqDVm6lqurwGWZaHnS2ilELt.json', 'var_call_g4ClZN2EulTFP1FiDwEyUDJ7': 'file_storage/call_g4ClZN2EulTFP1FiDwEyUDJ7.json', 'var_call_J4xdAJOYJQr74DDOlya56Ndr': {'error': 'No joined records with publication year and ratings.'}, 'var_call_XoYnvxOPLY9VHnqTfDG0UtfW': 'file_storage/call_XoYnvxOPLY9VHnqTfDG0UtfW.json', 'var_call_11ksGZ7Es4f02ryiOdid5TfD': 'file_storage/call_11ksGZ7Es4f02ryiOdid5TfD.json'}

exec(code, env_args)
