code = """import json
var = var_call_1xW6yc5bWnGneXfZNFp4IQMv
if isinstance(var, str):
    with open(var, 'r', encoding='utf-8') as f:
        results = json.load(f)
else:
    results = var
# Prepare final plain-text answer listing titles, book_id, avg_rating, review_count
lines = []
for r in results:
    lines.append(f"{r['title']} (book_id: {r['book_id']}), avg_rating: {r['avg_rating']}, review_count: {r['review_count']}")
answer = "Books in 'Children\'s Books' with average rating >= 4.5 (from 2020 onwards):\n" + "\n".join(lines)

print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_BzGxqLfZYGSIYmwjaeqOWbMN': 'file_storage/call_BzGxqLfZYGSIYmwjaeqOWbMN.json', 'var_call_a9hoV5PypFPLvU2R6UWeBGLN': 'file_storage/call_a9hoV5PypFPLvU2R6UWeBGLN.json', 'var_call_1xW6yc5bWnGneXfZNFp4IQMv': 'file_storage/call_1xW6yc5bWnGneXfZNFp4IQMv.json'}

exec(code, env_args)
