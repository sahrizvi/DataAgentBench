code = """import json
from collections import defaultdict
import re

# Load data from provided storage file paths
books_path = var_call_4NszdXKpfdAfd0EpsxCg8nym
reviews_path = var_call_9RGIbMjT5HHzYF8wZZtwb12R

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Build book_id -> publication year mapping by extracting first 4-digit year between 1500 and 2023 from details
book_year = {}
year_regex = re.compile(r"(1[5-9]\d{2}|20\d{2})")
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    years = year_regex.findall(details)
    year = None
    if years:
        # years is list of matched strings; pick first that is <=2023
        for y in years:
            try:
                yi = int(y)
                if 1500 <= yi <= 2023:
                    year = yi
                    break
            except:
                continue
    if year is not None:
        book_year[bid] = year

# Map reviews to book_id by converting purchaseid_X -> bookid_X
# Compute per-book average rating
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    rating = r.get('rating')
    if pid is None or rating is None:
        continue
    # Normalize rating to float
    try:
        rating_val = float(rating)
    except:
        continue
    # Convert purchaseid to bookid if format matches
    if isinstance(pid, str) and pid.startswith('purchaseid_'):
        bid = 'bookid_' + pid.split('purchaseid_')[-1]
    else:
        # fallback: try to replace purchase with book
        bid = pid.replace('purchase', 'book') if isinstance(pid, str) else None
    if bid and bid in book_year:
        book_ratings[bid].append(rating_val)

# Compute per-book average and group by decade
decade_book_avgs = defaultdict(list)
for bid, ratings in book_ratings.items():
    if not ratings:
        continue
    avg = sum(ratings) / len(ratings)
    year = book_year.get(bid)
    if year is None:
        continue
    decade_start = (year // 10) * 10
    decade_label = f"{decade_start}s"
    decade_book_avgs[decade_label].append(avg)

# Filter decades with at least 10 distinct books and compute decade average
decade_avg = {}
for decade, avgs in decade_book_avgs.items():
    if len(avgs) >= 10:
        decade_avg[decade] = sum(avgs) / len(avgs)

# Find decade with highest average
if not decade_avg:
    result = None
else:
    best_decade = max(decade_avg.items(), key=lambda x: (x[1], x[0]))[0]
    result = best_decade

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_fMivTRd5loHTbxgzuIZNNkL0': ['books_info'], 'var_call_IO3Faees83fTubyC4L94cJ3W': ['review'], 'var_call_4NszdXKpfdAfd0EpsxCg8nym': 'file_storage/call_4NszdXKpfdAfd0EpsxCg8nym.json', 'var_call_9RGIbMjT5HHzYF8wZZtwb12R': 'file_storage/call_9RGIbMjT5HHzYF8wZZtwb12R.json'}

exec(code, env_args)
