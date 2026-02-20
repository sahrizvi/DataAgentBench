code = """import json, re, pandas as pd

def load_records(var):
    if isinstance(var, str):
        with open(var, 'r', encoding='utf-8') as f:
            return json.load(f)
    return var

books = load_records(var_call_pitvumPA8nVnhlrOsAyTcKfE)
reviews = load_records(var_call_VWTMSwyp7k0Eh3e77QjXqhuH)

# Map purchase_id -> book_id by replacing prefix, as datasets use aligned numbering
# purchaseid_123 <-> bookid_123

def to_book_id(purchase_id):
    if purchase_id is None:
        return None
    return re.sub(r'^purchaseid_', 'bookid_', str(purchase_id))

# Extract publication year from details text
year_re = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year(details):
    if details is None:
        return None
    s = str(details)
    # Prefer year near 'released on' or 'published' or 'edition'
    candidates = [(m.start(), int(m.group(1))) for m in year_re.finditer(s)]
    if not candidates:
        return None
    # heuristic: take first plausible year between 1900 and 2026
    for _, y in candidates:
        if 1900 <= y <= 2026:
            return y
    return None

book_year = {}
for r in books:
    bid = r.get('book_id')
    y = extract_year(r.get('details'))
    if bid and y:
        book_year[bid] = y

# Aggregate ratings per book
from collections import defaultdict
sum_r = defaultdict(float)
cnt_r = defaultdict(int)
for rr in reviews:
    bid = to_book_id(rr.get('purchase_id'))
    if bid is None:
        continue
    try:
        rating = float(rr.get('rating'))
    except Exception:
        continue
    if 1.0 <= rating <= 5.0:
        sum_r[bid] += rating
        cnt_r[bid] += 1

# Compute average rating per decade across distinct books with >=1 rating and known year
dec_sum = defaultdict(float)
dec_books = defaultdict(int)
for bid, n in cnt_r.items():
    if n <= 0:
        continue
    y = book_year.get(bid)
    if not y:
        continue
    decade = (y // 10) * 10
    avg_book = sum_r[bid] / n
    dec_sum[decade] += avg_book
    dec_books[decade] += 1

# Filter decades with at least 10 distinct rated books
eligible = [(dec, dec_sum[dec]/dec_books[dec], dec_books[dec]) for dec in dec_books if dec_books[dec] >= 10]
eligible.sort(key=lambda x: (x[1], x[2], x[0]), reverse=True)

best = eligible[0][0] if eligible else None
ans = None if best is None else f"{best}s"

print('__RESULT__:')
print(json.dumps({'decade': ans}))"""

env_args = {'var_call_pitvumPA8nVnhlrOsAyTcKfE': 'file_storage/call_pitvumPA8nVnhlrOsAyTcKfE.json', 'var_call_VWTMSwyp7k0Eh3e77QjXqhuH': 'file_storage/call_VWTMSwyp7k0Eh3e77QjXqhuH.json'}

exec(code, env_args)
