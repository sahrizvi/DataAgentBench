code = """import json
with open(var_call_KqHxhlPlLmvwRQunN4FWFL8q, 'r') as f:
    final = json.load(f)
# Build a concise plain-text answer string
lines = ["Books in 'Children\'s Books' with average rating >= 4.5 (reviews from 2020 onwards):"]
for item in final:
    title = item.get('title')
    author = item.get('author') if item.get('author') is not None else 'Unknown'
    avg = item.get('avg_rating')
    rc = item.get('review_count')
    lines.append(f"- {title} — Author: {author} — Avg Rating: {avg:.3f} — Review Count: {rc}")

answer_text = "\n".join(lines)
import json
print("__RESULT__:")
print(json.dumps(answer_text))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json', 'var_call_rMGnyCj91wylDF6dDbrD2YV4': 'file_storage/call_rMGnyCj91wylDF6dDbrD2YV4.json', 'var_call_KqHxhlPlLmvwRQunN4FWFL8q': 'file_storage/call_KqHxhlPlLmvwRQunN4FWFL8q.json'}

exec(code, env_args)
