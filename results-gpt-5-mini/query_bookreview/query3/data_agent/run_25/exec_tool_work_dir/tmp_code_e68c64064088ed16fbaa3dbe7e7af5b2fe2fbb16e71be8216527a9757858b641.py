code = """import json
var = var_call_1xW6yc5bWnGneXfZNFp4IQMv
if isinstance(var, str):
    with open(var, 'r', encoding='utf-8') as f:
        results = json.load(f)
else:
    results = var
lines = []
for r in results:
    title = (r.get('title') or '').replace('\n', ' ').strip()
    bid = r.get('book_id', '')
    avg = r.get('avg_rating', '')
    cnt = r.get('review_count', '')
    lines.append(f"{title} (book_id: {bid}), avg_rating: {avg}, review_count: {cnt}")
header = "Books in Children's Books with average rating >= 4.5 (from 2020 onwards):"
answer = header + "\n" + "\n".join(lines)
print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_BzGxqLfZYGSIYmwjaeqOWbMN': 'file_storage/call_BzGxqLfZYGSIYmwjaeqOWbMN.json', 'var_call_a9hoV5PypFPLvU2R6UWeBGLN': 'file_storage/call_a9hoV5PypFPLvU2R6UWeBGLN.json', 'var_call_1xW6yc5bWnGneXfZNFp4IQMv': 'file_storage/call_1xW6yc5bWnGneXfZNFp4IQMv.json'}

exec(code, env_args)
