code = """import json

# Load the stored JSON result path from previous execute_python
res_path = var_call_6Umb6wy7J8BJ4hd7kX2VWNT8
with open(res_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build simplified output list
out = []
for d in data:
    out.append({
        'book_id': d.get('book_id'),
        'title': d.get('title'),
        'author': str(d.get('author')) if d.get('author') is not None else None,
        'avg_rating': float(d.get('avg_rating')) if d.get('avg_rating') is not None else None,
        'rating_count': int(d.get('rating_count')) if d.get('rating_count') is not None else None
    })

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json'}

exec(code, env_args)
