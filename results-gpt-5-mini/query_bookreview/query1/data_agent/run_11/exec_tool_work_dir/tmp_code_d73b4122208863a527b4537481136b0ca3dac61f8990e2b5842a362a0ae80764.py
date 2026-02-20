code = """import json, re
from collections import defaultdict
with open(var_call_fDrG1sc4I2e3ps9omdd3uqCt, 'r') as f:
    books = json.load(f)
with open(var_call_y8EP5NY7Cqa0I0WOjhMv4wET, 'r') as f:
    reviews = json.load(f)

# helper
year_pattern = re.compile(r"\b(1\d{3}|20\d{2})\b")
book_year = {}
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    m = year_pattern.search(details)
    if m:
        try:
            y = int(m.group(1))
            if 1000 <= y <= 2023:
                book_year[bid] = y
        except:
            pass

# process reviews
unique_purchase_ids = set()
mapped_ids = set()
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    rating = r.get('rating')
    if pid is None or rating is None:
        continue
    unique_purchase_ids.add(pid)
    try:
        rv = float(rating)
    except:
        continue
    mapped = pid
    if isinstance(pid, str) and pid.startswith('purchaseid_'):
        mapped = 'bookid_' + pid.split('_',1)[1]
    mapped_ids.add(mapped)
    if mapped in book_year:
        book_ratings[mapped].append(rv)

# per-book avg
book_avg = {bid: sum(vals)/len(vals) for bid, vals in book_ratings.items() if len(vals)>0}

# decades
decade_books = defaultdict(list)
for bid, avg in book_avg.items():
    year = book_year.get(bid)
    decade = f"{(year//10)*10}s"
    decade_books[decade].append((bid, avg))

# stats
decades_all = {}
for dec, items in decade_books.items():
    decades_all[dec] = {'num_books': len(items), 'average_rating': round(sum(x[1] for x in items)/len(items),4)}

out = {
    'total_books_in_books_table': len(books),
    'books_with_extracted_year': len(book_year),
    'total_review_records': len(reviews),
    'unique_purchase_ids_in_reviews': len(unique_purchase_ids),
    'unique_mapped_ids_from_reviews': len(mapped_ids),
    'matched_books_with_reviews_and_year': len(book_avg),
    'decades_all': decades_all
}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_fDrG1sc4I2e3ps9omdd3uqCt': 'file_storage/call_fDrG1sc4I2e3ps9omdd3uqCt.json', 'var_call_y8EP5NY7Cqa0I0WOjhMv4wET': 'file_storage/call_y8EP5NY7Cqa0I0WOjhMv4wET.json', 'var_call_eOXevsxizXoe8OeIplYqdnjD': {'decade': None, 'average_rating': None, 'num_books': 0}}

exec(code, env_args)
