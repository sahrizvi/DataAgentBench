code = """import json, pandas as pd

def load(obj):
    if isinstance(obj, str):
        with open(obj,'r',encoding='utf-8') as f:
            return json.load(f)
    return obj

rows = load(var_call_TY33cErXwj9JAPEdiUD3JP8h)
# parse author name where possible
out_rows = []
for r in rows:
    author = r.get('author')
    name = None
    if isinstance(author, str):
        a = author.strip()
        if a and a != 'None':
            if a.startswith('{'):
                try:
                    name = json.loads(a).get('name')
                except Exception:
                    name = a
            else:
                name = a
    out_rows.append({
        'title': r.get('title'),
        'author': name,
        'book_id': r.get('book_id'),
        'avg_rating': float(r.get('avg_rating')) if r.get('avg_rating') is not None else None,
        'review_count': int(r.get('review_count')) if r.get('review_count') is not None else None,
    })

# create plain text answer
lines = []
for r in out_rows:
    a = r['author'] if r['author'] else 'Unknown'
    lines.append(f"{r['title']} — {a} (avg rating since 2020: {r['avg_rating']:.2f}, reviews: {r['review_count']})")
answer = "\n".join(lines) if lines else "No Children's Books found with average rating >= 4.5 from reviews since 2020."

print('__RESULT__:')
print(json.dumps(answer))"""

env_args = {'var_call_tFwfl2gBcvpeWZ6GO2eyYpJy': 'file_storage/call_tFwfl2gBcvpeWZ6GO2eyYpJy.json', 'var_call_3WqlC1LZKUKQgbrK7s2oulWA': 'file_storage/call_3WqlC1LZKUKQgbrK7s2oulWA.json', 'var_call_TY33cErXwj9JAPEdiUD3JP8h': 'file_storage/call_TY33cErXwj9JAPEdiUD3JP8h.json'}

exec(code, env_args)
