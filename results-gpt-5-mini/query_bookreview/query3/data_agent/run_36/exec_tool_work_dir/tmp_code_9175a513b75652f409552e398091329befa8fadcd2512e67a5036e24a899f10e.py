code = """import json, math

# Load the merged results from previous step
with open(var_call_rMGnyCj91wylDF6dDbrD2YV4, 'r') as f:
    data = json.load(f)

filtered = []
for item in data:
    title = item.get('title')
    # skip missing titles
    if title is None:
        continue
    if isinstance(title, float) and math.isnan(title):
        continue
    author = item.get('author')
    avg = item.get('avg_rating')
    rc = item.get('review_count')
    # normalize types
    try:
        avg = float(avg) if avg is not None else None
    except:
        avg = None
    try:
        rc = int(rc) if rc is not None else 0
    except:
        rc = 0
    filtered.append({
        'title': title,
        'author': author,
        'avg_rating': avg,
        'review_count': rc
    })

# sort
filtered.sort(key=lambda x: (-(x['avg_rating'] if x['avg_rating'] is not None else 0), -x['review_count']))

# Prepare final result: only include avg_rating >= 4.5
final = [
    { 'title': i['title'], 'author': i['author'], 'avg_rating': round(i['avg_rating'],3) if i['avg_rating'] is not None else None, 'review_count': i['review_count'] }
    for i in filtered if i['avg_rating'] is not None and i['avg_rating'] >= 4.5
]

print("__RESULT__:")
print(json.dumps(final))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json', 'var_call_rMGnyCj91wylDF6dDbrD2YV4': 'file_storage/call_rMGnyCj91wylDF6dDbrD2YV4.json'}

exec(code, env_args)
