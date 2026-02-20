code = """import json

# Load the stored JSON result from previous execute_python
res_path = var_call_6Umb6wy7J8BJ4hd7kX2VWNT8
with open(res_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build plain-text listing
lines = []
for item in data:
    book_id = item.get('book_id')
    title = item.get('title')
    author = item.get('author')
    avg = item.get('avg_rating')
    count = item.get('rating_count')
    lines.append(f"{book_id} | {title} | author: {author} | avg_rating: {avg} | rating_count: {count}")

text = "\n".join(lines)

# Print according to required format as a JSON string
print("__RESULT__:")
print(json.dumps(text))"""

env_args = {'var_call_Gwl29776B3spFUVJy0XOWR2s': 'file_storage/call_Gwl29776B3spFUVJy0XOWR2s.json', 'var_call_d6tcXqfzwT750p14StHuVi0e': 'file_storage/call_d6tcXqfzwT750p14StHuVi0e.json', 'var_call_rUvg1ayTTJxMiUUF85jjs7SO': 'file_storage/call_rUvg1ayTTJxMiUUF85jjs7SO.json', 'var_call_6Umb6wy7J8BJ4hd7kX2VWNT8': 'file_storage/call_6Umb6wy7J8BJ4hd7kX2VWNT8.json'}

exec(code, env_args)
