code = """import json
var = var_call_1xW6yc5bWnGneXfZNFp4IQMv
if isinstance(var, str):
    with open(var, 'r', encoding='utf-8') as f:
        results = json.load(f)
else:
    results = var
out = []
for r in results:
    out.append({
        'title': r.get('title'),
        'book_id': r.get('book_id'),
        'avg_rating': r.get('avg_rating'),
        'review_count': r.get('review_count')
    })
print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_BzGxqLfZYGSIYmwjaeqOWbMN': 'file_storage/call_BzGxqLfZYGSIYmwjaeqOWbMN.json', 'var_call_a9hoV5PypFPLvU2R6UWeBGLN': 'file_storage/call_a9hoV5PypFPLvU2R6UWeBGLN.json', 'var_call_1xW6yc5bWnGneXfZNFp4IQMv': 'file_storage/call_1xW6yc5bWnGneXfZNFp4IQMv.json'}

exec(code, env_args)
