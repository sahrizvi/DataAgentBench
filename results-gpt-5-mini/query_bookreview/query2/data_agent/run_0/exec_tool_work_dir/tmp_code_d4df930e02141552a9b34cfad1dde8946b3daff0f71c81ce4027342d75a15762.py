code = """import json
from collections import defaultdict

# Load review data
with open(var_call_jWLnIzcvOYNihhGirovQ0cAi, 'r') as f:
    reviews = json.load(f)

# Load books data
with open(var_call_vhPkybGtfIBe6ysQofGklOYQ, 'r') as f:
    books = json.load(f)

# Compute average rating per purchase_id
ratings = defaultdict(list)
for r in reviews:
    pid = r.get('purchase_id')
    if pid is None:
        continue
    # rating may be string or number
    try:
        rating = float(r.get('rating'))
    except Exception:
        continue
    ratings[pid].append(rating)

avg_ratings = {}
for pid, vals in ratings.items():
    if len(vals) == 0:
        continue
    avg = sum(vals) / len(vals)
    avg_ratings[pid] = {'average': avg, 'count': len(vals)}

# Build book_id -> book record map
book_map = {b.get('book_id'): b for b in books}

# Find purchase_ids with perfect average 5.0
perfect_pids = [pid for pid, stats in avg_ratings.items() if abs(stats['average'] - 5.0) < 1e-9]

results = []
for pid in perfect_pids:
    # map purchaseid_x to bookid_x
    bid = pid.replace('purchaseid_', 'bookid_')
    book = book_map.get(bid)
    if not book:
        continue
    categories = (book.get('categories') or '').lower()
    details = (book.get('details') or '').lower()
    # check category contains 'literature & fiction' and details or categories indicate English language
    if 'literature & fiction' in categories and 'english' in details:
        stats = avg_ratings[pid]
        results.append({
            'book_id': book.get('book_id'),
            'title': book.get('title'),
            'categories': book.get('categories'),
            'details': book.get('details'),
            'average_rating': stats['average'],
            'review_count': stats['count']
        })

# Convert results to JSON
output = json.dumps(results)
print("__RESULT__:")
print(output)"""

env_args = {'var_call_pjCtQvecYsH4jHPnp1Li6D7Y': ['books_info'], 'var_call_vhPkybGtfIBe6ysQofGklOYQ': 'file_storage/call_vhPkybGtfIBe6ysQofGklOYQ.json', 'var_call_jWLnIzcvOYNihhGirovQ0cAi': 'file_storage/call_jWLnIzcvOYNihhGirovQ0cAi.json'}

exec(code, env_args)
