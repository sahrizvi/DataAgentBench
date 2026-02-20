code = """import json, re
# Load books data
books_var = var_call_BzGxqLfZYGSIYmwjaeqOWbMN
if isinstance(books_var, str):
    with open(books_var, 'r', encoding='utf-8') as f:
        books = json.load(f)
else:
    books = books_var
# Load reviews data
reviews_var = var_call_a9hoV5PypFPLvU2R6UWeBGLN
if isinstance(reviews_var, str):
    with open(reviews_var, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
else:
    reviews = reviews_var

# Helper to extract numeric id
def extract_num_id(s):
    if not isinstance(s, str):
        return None
    m = re.search(r"(\d+)", s)
    return m.group(1) if m else None

# Aggregate reviews by numeric id
from collections import defaultdict
agg = defaultdict(lambda: {'sum':0.0, 'count':0})
for r in reviews:
    pid = r.get('purchase_id')
    rid = extract_num_id(pid)
    if rid is None:
        continue
    # rating may be string
    try:
        rating = float(r.get('rating'))
    except:
        continue
    agg[rid]['sum'] += rating
    agg[rid]['count'] += 1

# Prepare result list by joining with books (which are already filtered to children's books)
results = []
for b in books:
    bid = b.get('book_id')
    num = extract_num_id(bid)
    if num is None:
        continue
    stats = agg.get(num)
    if not stats:
        continue
    avg = stats['sum'] / stats['count']
    if avg >= 4.5:
        results.append({
            'book_id': bid,
            'title': b.get('title'),
            'author': b.get('author'),
            'avg_rating': round(avg, 3),
            'review_count': stats['count']
        })

# Sort by avg_rating desc, then review_count desc
results.sort(key=lambda x: (-x['avg_rating'], -x['review_count']))

print("__RESULT__:")
print(json.dumps(results))"""

env_args = {'var_call_BzGxqLfZYGSIYmwjaeqOWbMN': 'file_storage/call_BzGxqLfZYGSIYmwjaeqOWbMN.json', 'var_call_a9hoV5PypFPLvU2R6UWeBGLN': 'file_storage/call_a9hoV5PypFPLvU2R6UWeBGLN.json'}

exec(code, env_args)
