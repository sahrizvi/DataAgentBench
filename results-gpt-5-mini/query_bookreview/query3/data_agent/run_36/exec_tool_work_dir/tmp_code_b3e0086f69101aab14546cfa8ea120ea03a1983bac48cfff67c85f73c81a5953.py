code = """import json
# Read the stored final list
with open(var_call_r3yvebHri30HWlyPYfeIj9Dl, 'r') as f:
    data = json.load(f)

# We'll extract top N where titles present
results = []
for item in data:
    title = item.get('title')
    if not title:
        continue
    results.append({
        'title': title,
        'author': item.get('author') if item.get('author') is not None else 'Unknown',
        'avg_rating': item.get('avg_rating'),
        'review_count': item.get('review_count')
    })

# Limit to unique titles
seen = set()
unique = []
for r in results:
    if r['title'] in seen:
        continue
    seen.add(r['title'])
    unique.append(r)

# Build answer string
lines = ["Books in 'Children\'s Books' with average rating >= 4.5 (reviews from 2020 onwards):"]
for it in unique:
    lines.append(f"- {it['title']} — Author: {it['author']} — Avg Rating: {it['avg_rating']:.3f} — Review Count: {it['review_count']}")

answer = "\n".join(lines)
print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json', 'var_call_rMGnyCj91wylDF6dDbrD2YV4': 'file_storage/call_rMGnyCj91wylDF6dDbrD2YV4.json', 'var_call_KqHxhlPlLmvwRQunN4FWFL8q': 'file_storage/call_KqHxhlPlLmvwRQunN4FWFL8q.json', 'var_call_r3yvebHri30HWlyPYfeIj9Dl': 'file_storage/call_r3yvebHri30HWlyPYfeIj9Dl.json'}

exec(code, env_args)
