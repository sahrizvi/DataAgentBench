code = """import json

with open(var_call_Qxuw05rvUjND9SrR7ZrMoFcJ, 'r') as f:
    data = json.load(f)

# Build a plain-text summary safely
lines = []
for item in data:
    title = item.get('title') if item.get('title') is not None else ''
    author = item.get('author') if item.get('author') is not None else ''
    # Truncate long author strings for readability
    if isinstance(author, str) and len(author) > 200:
        author = author[:197] + '...'
    avg = item.get('avg_rating')
    cnt = item.get('review_count')
    lines.append(f"{title} — {author} — {avg} ({cnt} reviews)")

summary = "Books in 'Children\'s Books' with average rating >= 4.5 (from 2020 onwards):\n" + "\n".join(lines)

print("__RESULT__:")
print(json.dumps(summary))"""

env_args = {'var_call_0C8uwpKxowvKhWAtQ9COH81A': ['books_info'], 'var_call_SimpA06dt5RaDc35kN1qJ4Cx': 'file_storage/call_SimpA06dt5RaDc35kN1qJ4Cx.json', 'var_call_63Llc1wtT8Vnf7jIFuUKPat5': ['review'], 'var_call_wQPw2fgJXAbet4r995pYeSuD': 'file_storage/call_wQPw2fgJXAbet4r995pYeSuD.json', 'var_call_tLgGZXXhjmb6Lj8euRf6k2DA': 'file_storage/call_tLgGZXXhjmb6Lj8euRf6k2DA.json', 'var_call_Qxuw05rvUjND9SrR7ZrMoFcJ': 'file_storage/call_Qxuw05rvUjND9SrR7ZrMoFcJ.json'}

exec(code, env_args)
