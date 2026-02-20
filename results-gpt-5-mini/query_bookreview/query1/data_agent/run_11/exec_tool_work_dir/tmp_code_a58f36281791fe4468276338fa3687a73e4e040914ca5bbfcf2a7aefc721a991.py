code = """import json, re

# Load data from previous query results stored as files
with open(var_call_fDrG1sc4I2e3ps9omdd3uqCt, 'r') as f:
    books = json.load(f)
with open(var_call_y8EP5NY7Cqa0I0WOjhMv4wET, 'r') as f:
    reviews = json.load(f)

# Build book dict and extract publication year
book_year = {}
book_title = {}
year_pattern = re.compile(r"\b(1\d{3}|20\d{2})\b")
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    title = b.get('title') or ''
    m = year_pattern.search(details)
    year = None
    if m:
        try:
            y = int(m.group(1))
            if 1000 <= y <= 2023:
                year = y
        except:
            year = None
    if year:
        book_year[bid] = year
        book_title[bid] = title

# Map reviews to book ids (replace purchaseid_ -> bookid_)
from collections import defaultdict
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    rating = r.get('rating')
    if pid is None or rating is None:
        continue
    # convert rating to float
    try:
        rating_val = float(rating)
    except:
        continue
    # map purchaseid_N -> bookid_N
    mapped = None
    if isinstance(pid, str) and pid.startswith('purchaseid_'):
        mapped = 'bookid_' + pid.split('_',1)[1]
    else:
        # fallback: try direct
        mapped = pid
    if mapped in book_year:
        book_ratings[mapped].append(rating_val)

# Compute per-book average ratings for books with at least one review
book_avg = {}
for bid, ratings in book_ratings.items():
    if len(ratings) > 0:
        book_avg[bid] = sum(ratings)/len(ratings)

# Group by decade and compute average of per-book averages
decade_books = defaultdict(list)
for bid, avg in book_avg.items():
    year = book_year.get(bid)
    if not year:
        continue
    decade = f"{(year//10)*10}s"
    decade_books[decade].append((bid, avg))

# Filter decades with at least 10 distinct books
decade_stats = {}
for dec, items in decade_books.items():
    num_books = len(items)
    if num_books >= 10:
        avg_of_avgs = sum(x[1] for x in items)/num_books
        decade_stats[dec] = {'num_books': num_books, 'average_rating': avg_of_avgs}

# Find decade with highest average rating
result = None
if decade_stats:
    best_dec = max(decade_stats.items(), key=lambda x: (x[1]['average_rating'], -int(x[0].rstrip('s'))))
    dec, stats = best_dec
    result = {'decade': dec, 'average_rating': round(stats['average_rating'], 4), 'num_books': stats['num_books']}
else:
    result = {'decade': None, 'average_rating': None, 'num_books': 0}

print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_fDrG1sc4I2e3ps9omdd3uqCt': 'file_storage/call_fDrG1sc4I2e3ps9omdd3uqCt.json', 'var_call_y8EP5NY7Cqa0I0WOjhMv4wET': 'file_storage/call_y8EP5NY7Cqa0I0WOjhMv4wET.json'}

exec(code, env_args)
