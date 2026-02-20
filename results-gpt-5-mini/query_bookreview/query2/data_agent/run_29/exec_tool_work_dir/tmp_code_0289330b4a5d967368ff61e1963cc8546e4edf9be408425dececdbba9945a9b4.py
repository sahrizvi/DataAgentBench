code = """import json

# Read the stored JSON result from previous successful execute_python
path = var_call_I67q2nxAGspFSdyXVR2BuxGH
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a plain-text answer string listing each matching book on its own line
lines = []
for d in data:
    book_id = d.get('book_id')
    title = d.get('title')
    author = d.get('author')
    avg = d.get('avg_rating')
    count = d.get('rating_count')
    # Use json.dumps for author to safely represent complex strings
    author_repr = json.dumps(author)
    lines.append(f"{title} (book_id: {book_id}) - author: {author_repr} - avg_rating: {avg} - rating_count: {count}")

answer_text = "\n".join(lines)

print("__RESULT__:")
print(json.dumps(answer_text))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json', 'var_call_I67q2nxAGspFSdyXVR2BuxGH': 'file_storage/call_I67q2nxAGspFSdyXVR2BuxGH.json', 'var_call_xwTMMONjpZBkO8zTaZtsJqCe': 'file_storage/call_xwTMMONjpZBkO8zTaZtsJqCe.json'}

exec(code, env_args)
