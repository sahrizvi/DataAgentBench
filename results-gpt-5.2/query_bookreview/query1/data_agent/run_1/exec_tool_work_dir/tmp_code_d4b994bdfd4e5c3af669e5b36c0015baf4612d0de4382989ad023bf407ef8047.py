code = """import json, re, pandas as pd

def load_records(x):
    if isinstance(x, str):
        with open(x, 'r', encoding='utf-8') as f:
            return json.load(f)
    return x

books = load_records(var_call_QtUFBVW9BGWUBlZjhh6ht1rd)
reviews = load_records(var_call_8EVoBuWRQm00BAQDqMw236IZ)

# Extract 4-digit year from details
year_re = re.compile(r'\b(1[6-9]\d{2}|20\d{2})\b')

book_year = {}
for r in books:
    bid = r.get('book_id')
    det = r.get('details') or ''
    yrs = [int(m.group(0)) for m in year_re.finditer(det)]
    if not yrs:
        continue
    # heuristic: choose year near words published/released/edition/date if possible; else smallest plausible recent? We'll pick first occurrence.
    # But to reduce noise from ISBNs (which can include 2013 etc but also 978...), regex avoids 978 by requiring 4-digit year.
    year = yrs[0]
    book_year[bid] = year

# Map purchase_id -> book_id via numeric suffix heuristic
# purchaseid_186 -> bookid_186
pid_re = re.compile(r'^(purchaseid_)')

rows = []
for rv in reviews:
    pid = str(rv.get('purchase_id'))
    rating = rv.get('rating')
    try:
        rating_f = float(rating)
    except Exception:
        continue
    if pid.startswith('purchaseid_'):
        bid = 'bookid_' + pid.split('_',1)[1]
    else:
        bid = pid
    y = book_year.get(bid)
    if y is None:
        continue
    decade = (y // 10) * 10
    rows.append((bid, decade, rating_f))

if not rows:
    out = {"error":"No matched rated books with publication year found."}
    print('__RESULT__:')
    print(json.dumps(out))
    raise SystemExit

df = pd.DataFrame(rows, columns=['book_id','decade','rating'])
# Ensure distinct books rated: at least one rating per book
book_decade = df[['book_id','decade']].drop_duplicates()
books_per_decade = book_decade.groupby('decade')['book_id'].nunique().rename('distinct_books')
# Average rating across all reviews for books in decade
avg_rating = df.groupby('decade')['rating'].mean().rename('avg_rating')
summary = pd.concat([books_per_decade, avg_rating], axis=1).dropna().reset_index()
summary = summary[summary['distinct_books']>=10]
if summary.empty:
    out = {"error":"No decade has at least 10 distinct rated books with publication year extracted (from sampled books)."}
    print('__RESULT__:')
    print(json.dumps(out))
    raise SystemExit
best = summary.sort_values(['avg_rating','distinct_books'], ascending=[False,False]).iloc[0]
out = {"decade": f"{int(best['decade'])}s", "avg_rating": float(best['avg_rating']), "distinct_books": int(best['distinct_books'])}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_QtUFBVW9BGWUBlZjhh6ht1rd': 'file_storage/call_QtUFBVW9BGWUBlZjhh6ht1rd.json', 'var_call_8EVoBuWRQm00BAQDqMw236IZ': 'file_storage/call_8EVoBuWRQm00BAQDqMw236IZ.json'}

exec(code, env_args)
