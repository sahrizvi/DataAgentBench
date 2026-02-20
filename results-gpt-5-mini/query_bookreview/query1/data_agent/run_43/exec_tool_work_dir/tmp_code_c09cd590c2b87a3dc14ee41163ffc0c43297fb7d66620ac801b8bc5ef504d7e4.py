code = """import json
import re

# Load data from previous tool calls (file paths)
books_path = var_call_e6IqxnYU7V7L1z7WGV1FkOfH
reviews_path = var_call_CtKCR6DQFjLIDGVMnbdKZHao

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Build book_id -> year mapping by extracting first 4-digit year in details
year_regex = re.compile(r'\b(1[5-9]\d{2}|20\d{2})\b')
book_year = {}
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    m = year_regex.search(details)
    if m:
        year = int(m.group(0))
        book_year[bid] = year

# Map reviews to book ids: convert purchaseid_N -> bookid_N
# Normalize ratings to float
from collections import defaultdict
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id') or ''
    rating = r.get('rating')
    # try to convert rating to float
    try:
        rating_val = float(rating)
    except:
        continue
    # extract number suffix
    m = re.search(r'(\d+)$', pid)
    if not m:
        continue
    num = m.group(1)
    bid = f'bookid_{num}'
    if bid in book_year:
        book_ratings[bid].append(rating_val)

# Compute per-book average ratings and map to decades
book_avg = {}
for bid, ratings in book_ratings.items():
    if len(ratings) == 0:
        continue
    avg = sum(ratings)/len(ratings)
    book_avg[bid] = avg

# Aggregate by decade
decade_books = defaultdict(list)
for bid, avg in book_avg.items():
    year = book_year.get(bid)
    if not year:
        continue
    decade_start = (year // 10) * 10
    decade_str = f"{decade_start}s"
    decade_books[decade_str].append((bid, avg))

# For decades with at least 10 distinct books, compute decade average (mean of per-book averages)
decade_stats = {}
for decade, items in decade_books.items():
    num_books = len(items)
    if num_books >= 10:
        avg_of_avgs = sum(a for (_, a) in items) / num_books
        decade_stats[decade] = {
            'decade': decade,
            'average_rating': avg_of_avgs,
            'num_books': num_books
        }

# Determine decade with highest average rating
if not decade_stats:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}
else:
    best = max(decade_stats.values(), key=lambda x: (x['average_rating'], x['num_books']))
    # round average to 4 decimal places
    best['average_rating'] = round(best['average_rating'], 4)
    result = best

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_y20SGbas66C84S9S6awtQ1en': ['books_info'], 'var_call_Zdau28aAbT3znqSfwZI8lTZL': ['review'], 'var_call_e6IqxnYU7V7L1z7WGV1FkOfH': 'file_storage/call_e6IqxnYU7V7L1z7WGV1FkOfH.json', 'var_call_CtKCR6DQFjLIDGVMnbdKZHao': 'file_storage/call_CtKCR6DQFjLIDGVMnbdKZHao.json'}

exec(code, env_args)
