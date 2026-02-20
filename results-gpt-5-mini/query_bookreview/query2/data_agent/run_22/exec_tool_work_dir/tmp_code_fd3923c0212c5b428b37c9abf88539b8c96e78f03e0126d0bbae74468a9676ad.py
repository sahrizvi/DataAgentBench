code = """import json
p = var_call_KHFNEv4rZFMGA5cDL8hOhrYj
with open(p, 'r', encoding='utf-8') as f:
    items = json.load(f)

# Build a plain-text answer: one line per book with key fields
lines = []
for it in items:
    bid = it.get('book_id')
    title = it.get('title')
    author = it.get('author')
    avg = it.get('avg_rating')
    cnt = it.get('review_count')
    lines.append(f"{title} ({bid}) — Author: {author} — avg_rating: {avg} — review_count: {cnt}")

answer_text = "\n".join(lines)
print('__RESULT__:')
print(json.dumps(answer_text))"""

env_args = {'var_call_fQJ43iL9WRBrzYH151dwck8J': ['books_info'], 'var_call_BimRhIEXuOcnegIOf9CYUrzv': 'file_storage/call_BimRhIEXuOcnegIOf9CYUrzv.json', 'var_call_h2NXKvYEWzdhYXATgXeYdkyk': ['review'], 'var_call_G4Yh8T6gc6ljRE3NRnR1XgYT': 'file_storage/call_G4Yh8T6gc6ljRE3NRnR1XgYT.json', 'var_call_9jxVGhr7A1ebYVecyQvkSEIg': 'file_storage/call_9jxVGhr7A1ebYVecyQvkSEIg.json', 'var_call_KHFNEv4rZFMGA5cDL8hOhrYj': 'file_storage/call_KHFNEv4rZFMGA5cDL8hOhrYj.json'}

exec(code, env_args)
