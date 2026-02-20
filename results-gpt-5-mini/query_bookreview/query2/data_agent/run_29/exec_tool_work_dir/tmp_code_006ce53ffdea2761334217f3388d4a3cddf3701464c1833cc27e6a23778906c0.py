code = """import json

# Load the stored JSON result path from previous execute_python
res_path = var_call_I67q2nxAGspFSdyXVR2BuxGH
with open(res_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# We'll produce a concise final text listing titles and book_ids
lines = []
for d in data:
    lines.append({
        'book_id': d.get('book_id'),
        'title': d.get('title'),
        'author': d.get('author'),
        'avg_rating': d.get('avg_rating'),
        'rating_count': d.get('rating_count')
    })

print("__RESULT__:")
print(json.dumps(lines))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json', 'var_call_I67q2nxAGspFSdyXVR2BuxGH': 'file_storage/call_I67q2nxAGspFSdyXVR2BuxGH.json'}

exec(code, env_args)
