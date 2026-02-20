code = """import json, re, statistics

# Load data from storage file paths
with open(var_call_2rfRCGFTyeN5Y2SVZLOtGtab, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(var_call_rHepLLAEJ8Y766eGKf2P6VPQ, 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# Helper to extract first numeric id from strings like 'bookid_123' or 'purchaseid_123'
def extract_num(s):
    if not s or not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else None

# Helper to extract a publication year from the details string
# We'll look for 4-digit years between 1400 and 2025 and pick the first occurrence

def extract_year(details):
    if not details or not isinstance(details, str):
        return None
    years = re.findall(r"(\d{4})", details)
    for y in years:
        y_int = int(y)
        if 1400 <= y_int <= 2025:
            return y_int
    return None

# Build mapping from numeric book id -> publication year
book_year = {}
for b in books:
    bid = b.get('book_id')
    num = extract_num(bid)
    if num is None:
        continue
    year = extract_year(b.get('details','') or b.get('description','') or '')
    if year is not None:
        book_year[num] = year

# Aggregate reviews by numeric book id
from collections import defaultdict
book_ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    num = extract_num(pid)
    if num is None:
        continue
    # convert rating to float if possible
    rating = r.get('rating')
    try:
        rating_f = float(rating)
    except Exception:
        continue
    book_ratings[num].append(rating_f)

# For books that have both a year and at least one rating, compute per-book average
book_avg = {}
for num, ratings in book_ratings.items():
    if num in book_year and len(ratings) > 0:
        book_avg[num] = sum(ratings) / len(ratings)

# Group books by decade
decade_books = defaultdict(list)
for num, avg in book_avg.items():
    year = book_year.get(num)
    if year is None:
        continue
    decade_start = (year // 10) * 10
    decade_label = f"{decade_start}s"
    decade_books[decade_label].append(avg)

# Compute average per decade (average of book averages), and count distinct books
decade_stats = []
for decade, avgs in decade_books.items():
    count = len(avgs)
    avg_decade = sum(avgs) / count if count>0 else None
    decade_stats.append({'decade': decade, 'average_rating': avg_decade, 'book_count': count})

# Filter decades with at least 10 distinct books
eligible = [d for d in decade_stats if d['book_count'] >= 10]

if not eligible:
    result = {'decade': None, 'average_rating': None, 'book_count': 0, 'message': 'No decade has at least 10 distinct rated books.'}
else:
    # find max average_rating, break ties by highest book_count then by decade label
    eligible.sort(key=lambda x: (x['average_rating'], x['book_count'], x['decade']), reverse=True)
    top = eligible[0]
    # Round average for readability
    top['average_rating'] = round(top['average_rating'], 4)
    result = top

import json
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_UkqJdQJKPxzi6X4LT8jd9yzC': ['books_info'], 'var_call_CItpzJz2j7bXp4bLZuYzioya': ['review'], 'var_call_2rfRCGFTyeN5Y2SVZLOtGtab': 'file_storage/call_2rfRCGFTyeN5Y2SVZLOtGtab.json', 'var_call_rHepLLAEJ8Y766eGKf2P6VPQ': 'file_storage/call_rHepLLAEJ8Y766eGKf2P6VPQ.json'}

exec(code, env_args)
