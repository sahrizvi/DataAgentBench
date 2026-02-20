code = """import json, re, statistics
# Load data from previous tool results
books_path = var_call_TBvhAnBOC2ADBXPSHAAa4VUN
reviews_path = var_call_szOwRX6nGoZrRCyPaYPuD7Jo
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)
with open(reviews_path, 'r', encoding='utf-8') as f:
    reviews = json.load(f)
# Helper to extract numeric id from strings like 'bookid_123' or 'purchaseid_123'
def extract_num(s):
    if s is None:
        return None
    m = re.search(r"(\d+)", str(s))
    return m.group(1) if m else None
# Build review aggregates by numeric id
ratings_by_id = {}
for r in reviews:
    pid = r.get('purchase_id')
    num = extract_num(pid)
    if num is None:
        continue
    # convert rating to float safely
    rating_raw = r.get('rating')
    try:
        rating = float(rating_raw)
    except:
        try:
            rating = float(str(rating_raw).strip())
        except:
            continue
    ratings_by_id.setdefault(num, []).append(rating)
# compute average ratings
avg_by_num = {}
for num, vals in ratings_by_id.items():
    if len(vals) == 0:
        continue
    avg = sum(vals)/len(vals)
    avg_by_num[num] = {'average': avg, 'count': len(vals)}
# Filter books: already from books_info where categories include Literature & Fiction
# Further require details contain 'English' (case-insensitive) to be English-language
matches = []
for b in books:
    bid = b.get('book_id')
    num = extract_num(bid)
    if num is None:
        continue
    # check details mention English
    details = b.get('details') or ''
    if not re.search(r"\bEnglish\b", details, flags=re.IGNORECASE):
        continue
    # check average rating == 5.0
    stats = avg_by_num.get(num)
    if not stats:
        continue
    if abs(stats['average'] - 5.0) < 1e-9:
        matches.append({
            'book_id': bid,
            'title': b.get('title'),
            'author': b.get('author'),
            'average_rating': stats['average'],
            'ratings_count': stats['count']
        })
# Prepare output
result = matches
print("__RESULT__:")
print(json.dumps(result))"""

env_args = {'var_call_G3S80j8KCGOhR4vjQ9DtlO2o': ['books_info'], 'var_call_TBvhAnBOC2ADBXPSHAAa4VUN': 'file_storage/call_TBvhAnBOC2ADBXPSHAAa4VUN.json', 'var_call_YGZmw3GRt1QzcxbbmhCe4SUL': ['review'], 'var_call_szOwRX6nGoZrRCyPaYPuD7Jo': 'file_storage/call_szOwRX6nGoZrRCyPaYPuD7Jo.json'}

exec(code, env_args)
