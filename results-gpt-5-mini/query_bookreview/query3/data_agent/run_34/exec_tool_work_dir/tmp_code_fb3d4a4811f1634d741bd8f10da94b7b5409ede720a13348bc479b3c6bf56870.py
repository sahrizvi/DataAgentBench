code = """import json

with open(var_call_5X7uOsfgNWK4u3GbZA2QkIW9, 'r') as f:
    output = json.load(f)

# Compose final plain-text answer
lines = []
for item in output:
    title = item.get('title','')
    author = item.get('author','')
    avg = item.get('avg_rating')
    cnt = item.get('review_count')
    lines.append(f"{title} — {author} — {avg} ({cnt} reviews)")

answer = "Books in 'Children\'s Books' with average rating >= 4.5 (from 2020 onwards):\n" + "\n".join(lines)

print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_0C8uwpKxowvKhWAtQ9COH81A': ['books_info'], 'var_call_SimpA06dt5RaDc35kN1qJ4Cx': 'file_storage/call_SimpA06dt5RaDc35kN1qJ4Cx.json', 'var_call_63Llc1wtT8Vnf7jIFuUKPat5': ['review'], 'var_call_wQPw2fgJXAbet4r995pYeSuD': 'file_storage/call_wQPw2fgJXAbet4r995pYeSuD.json', 'var_call_tLgGZXXhjmb6Lj8euRf6k2DA': 'file_storage/call_tLgGZXXhjmb6Lj8euRf6k2DA.json', 'var_call_Qxuw05rvUjND9SrR7ZrMoFcJ': 'file_storage/call_Qxuw05rvUjND9SrR7ZrMoFcJ.json', 'var_call_5X7uOsfgNWK4u3GbZA2QkIW9': 'file_storage/call_5X7uOsfgNWK4u3GbZA2QkIW9.json'}

exec(code, env_args)
