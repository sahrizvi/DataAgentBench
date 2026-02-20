code = """import json

# Load final results
res_path = var_call_xwTMMONjpZBkO8zTaZtsJqCe
with open(res_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build final plain-text answer listing each matching book on its own line with key fields
lines = []
for d in data:
    lines.append(f"{d['title']} (book_id: {d['book_id']}) - author: {d['author']} - avg_rating: {d['avg_rating']} - rating_count: {d['rating_count']}")

answer = "\n".join(lines)

print("__RESULT__:")
print(json.dumps(answer))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json', 'var_call_I67q2nxAGspFSdyXVR2BuxGH': 'file_storage/call_I67q2nxAGspFSdyXVR2BuxGH.json', 'var_call_xwTMMONjpZBkO8zTaZtsJqCe': 'file_storage/call_xwTMMONjpZBkO8zTaZtsJqCe.json'}

exec(code, env_args)
