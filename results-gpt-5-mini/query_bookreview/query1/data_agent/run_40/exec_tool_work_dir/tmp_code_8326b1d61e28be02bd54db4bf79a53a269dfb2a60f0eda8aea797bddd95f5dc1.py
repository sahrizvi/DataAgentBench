code = """import json
import re
import statistics
from pathlib import Path

# Load data from storage-provided file paths
books_path = var_call_xlaKIYoWY0rk19h3jhMKb24b
reviews_path = var_call_VcxEBSkv9IcTbvoRrM9s5LFM

with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Normalize review purchase_id to book_id
for r in reviews:
    pid = r.get('purchase_id')
    if isinstance(pid, str) and pid.startswith('purchaseid_'):
        r['book_id'] = pid.replace('purchaseid_', 'bookid_')
    else:
        r['book_id'] = pid

# Convert rating to float
for r in reviews:
    try:
        r['rating'] = float(r.get('rating'))
    except Exception:
        r['rating'] = None

# Extract publication year from details in books
year_pattern = re.compile(r"(1[89]\d{2}|20\d{2})")
books_by_id = {}
for b in books:
    bid = b.get('book_id')
    details = b.get('details') or ''
    years = year_pattern.findall(details)
    years = [int(y) for y in years]
    pub_year = None
    if years:
        pub_year = min(years)  # choose earliest year found
    b['pub_year'] = pub_year
    books_by_id[bid] = b

# Join reviews to books based on book_id
# Keep reviews that have a matching book with a publication year
joined = []
for r in reviews:
    bid = r.get('book_id')
    if bid in books_by_id and books_by_id[bid].get('pub_year'):
        jr = {
            'book_id': bid,
            'rating': r.get('rating'),
            'pub_year': books_by_id[bid].get('pub_year')
        }
        joined.append(jr)

# Compute per-book average rating
from collections import defaultdict
book_ratings = defaultdict(list)
book_year = {}
for j in joined:
    if j['rating'] is None:
        continue
    book_ratings[j['book_id']].append(j['rating'])
    book_year[j['book_id']] = j['pub_year']

book_avg = {}
for bid, ratings in book_ratings.items():
    if len(ratings) > 0:
        book_avg[bid] = {
            'avg_rating': sum(ratings)/len(ratings),
            'pub_year': book_year.get(bid)
        }

# Group by decade
decade_books = defaultdict(list)
for bid, info in book_avg.items():
    year = info['pub_year']
    if not year:
        continue
    decade_start = (year // 10) * 10
    decade_label = f"{decade_start}s"
    decade_books[decade_label].append(info['avg_rating'])

# Filter decades with at least 10 distinct books
decade_stats = []
for dec, ratings_list in decade_books.items():
    num_books = len(ratings_list)
    if num_books >= 10:
        avg_of_books = sum(ratings_list)/num_books
        decade_stats.append((dec, avg_of_books, num_books))

# Find decade with highest average rating
if not decade_stats:
    result = None
else:
    # sort by avg desc, then by num_books desc
    decade_stats.sort(key=lambda x: (x[1], x[2]), reverse=True)
    best = decade_stats[0]
    result = {
        'decade': best[0],
        'average_rating': round(best[1], 4),
        'num_books': best[2]
    }

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_6KvhM7fJ8d9P75SBqnGGpDcx': ['books_info'], 'var_call_kbMCCMHEsPaV7MXjXhMNbtPi': ['review'], 'var_call_xlaKIYoWY0rk19h3jhMKb24b': 'file_storage/call_xlaKIYoWY0rk19h3jhMKb24b.json', 'var_call_VcxEBSkv9IcTbvoRrM9s5LFM': 'file_storage/call_VcxEBSkv9IcTbvoRrM9s5LFM.json'}

exec(code, env_args)
