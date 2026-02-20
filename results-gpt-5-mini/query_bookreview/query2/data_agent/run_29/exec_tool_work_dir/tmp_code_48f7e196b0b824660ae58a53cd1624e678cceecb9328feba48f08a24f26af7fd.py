code = """import json

path = var_call_vUXuGOtR7QGObp3aBafQAnJY
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build answer lines
lines = []
for d in data:
    title = d.get('title') or ''
    bid = d.get('book_id') or ''
    author = d.get('author')
    # make author safe string
    if author is None:
        author_str = 'None'
    else:
        author_str = str(author)
    avg = d.get('avg_rating')
    cnt = d.get('rating_count')
    lines.append(f"{title} (book_id: {bid}) - author: {author_str} - avg_rating: {avg} - rating_count: {cnt}")

answer_text = '\n'.join(lines)

print("__RESULT__:")
print(json.dumps(answer_text))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json', 'var_call_I67q2nxAGspFSdyXVR2BuxGH': 'file_storage/call_I67q2nxAGspFSdyXVR2BuxGH.json', 'var_call_xwTMMONjpZBkO8zTaZtsJqCe': 'file_storage/call_xwTMMONjpZBkO8zTaZtsJqCe.json', 'var_call_vUXuGOtR7QGObp3aBafQAnJY': 'file_storage/call_vUXuGOtR7QGObp3aBafQAnJY.json'}

exec(code, env_args)
