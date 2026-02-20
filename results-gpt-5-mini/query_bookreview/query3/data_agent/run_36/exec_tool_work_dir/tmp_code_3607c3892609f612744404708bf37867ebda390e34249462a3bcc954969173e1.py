code = """import json
with open(var_call_r3yvebHri30HWlyPYfeIj9Dl, "r") as f:
    data = json.load(f)
lines = ["Books in Childrens Books with average rating >= 4.5 (reviews from 2020 onwards):"]
for item in data:
    title = item.get("title")
    if not title:
        continue
    author = item.get("author") or "Unknown"
    avg = item.get("avg_rating") or 0
    rc = item.get("review_count") or 0
    lines.append("- " + str(title) + " — Author: " + str(author) + " — Avg Rating: " + "{:.3f}".format(avg) + " — Review Count: " + str(rc))
answer = "\n".join(lines)
print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_w1SPxF15aUMjLaPLoXjNpKEp': 'file_storage/call_w1SPxF15aUMjLaPLoXjNpKEp.json', 'var_call_HWaRHUBz912QRuu4YzVVlzYU': 'file_storage/call_HWaRHUBz912QRuu4YzVVlzYU.json', 'var_call_rMGnyCj91wylDF6dDbrD2YV4': 'file_storage/call_rMGnyCj91wylDF6dDbrD2YV4.json', 'var_call_KqHxhlPlLmvwRQunN4FWFL8q': 'file_storage/call_KqHxhlPlLmvwRQunN4FWFL8q.json', 'var_call_r3yvebHri30HWlyPYfeIj9Dl': 'file_storage/call_r3yvebHri30HWlyPYfeIj9Dl.json'}

exec(code, env_args)
