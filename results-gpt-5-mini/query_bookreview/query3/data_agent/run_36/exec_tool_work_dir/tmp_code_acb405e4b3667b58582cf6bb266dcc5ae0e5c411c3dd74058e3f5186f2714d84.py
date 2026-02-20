code = """import json, math

# Load the merged results from previous step
with open(var_call_rMGnyCj91wylDF6dDbrD2YV4, 'r') as f:
    data = json.load(f)

# Filter entries that have valid titles (not NaN and not None)
filtered = []
for item in data:
    title = item.get('title')
    if title is None:
        continue
    if isinstance(title, float) and math.isnan(title):
        continue
    filtered.append({
        'title': title,
        'author': item.get('author'),
        'avg_rating': item.get('avg_rating'),
        'review_count': item.get('review_count')
    })

# Sort by avg_rating desc then review_count desc
filtered.sort(key=lambda x: (-(x['avg_rating'] if x['avg_rating'] is not None else 0), -x['review_count']))

# Build a plain-text answer
lines = []
lines.append("Books in Children's Books with average rating >= 4.5 (reviews from 2020 onwards):")
for it in filtered:
    author = it['author'] if it['author'] is not None else 'Unknown'
    avg = it['avg_rating'] if it['avg_rating'] is not None else 0
    lines.append(f"- {it['title']} — Author: {author} — Avg Rating: {avg:.3f} — Review Count: {it['review_count']}")

answer_text = "\n".join(lines)

print("__RESULT__:")
print(json.dumps(answer_text))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json', 'var_call_rMGnyCj91wylDF6dDbrD2YV4': 'file_storage/call_rMGnyCj91wylDF6dDbrD2YV4.json'}

exec(code, env_args)
