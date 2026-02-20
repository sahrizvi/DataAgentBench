code = """import json
p = var_call_KHFNEv4rZFMGA5cDL8hOhrYj
with open(p, 'r', encoding='utf-8') as f:
    items = json.load(f)

lines = []
for it in items:
    title = it.get('title') or ''
    bid = it.get('book_id') or ''
    author = it.get('author') or ''
    avg = it.get('avg_rating')
    cnt = it.get('review_count')
    author_str = json.dumps(author, ensure_ascii=False)
    avg_str = str(avg) if avg is not None else 'None'
    cnt_str = str(cnt) if cnt is not None else '0'
    line = title + ' (' + bid + ') - Author: ' + author_str + ' - avg_rating: ' + avg_str + ' - review_count: ' + cnt_str
    lines.append(line)

answer = '\n'.join(lines)
print('__RESULT__:')
print(json.dumps(answer))"""

env_args = {'var_call_fQJ43iL9WRBrzYH151dwck8J': ['books_info'], 'var_call_BimRhIEXuOcnegIOf9CYUrzv': 'file_storage/call_BimRhIEXuOcnegIOf9CYUrzv.json', 'var_call_h2NXKvYEWzdhYXATgXeYdkyk': ['review'], 'var_call_G4Yh8T6gc6ljRE3NRnR1XgYT': 'file_storage/call_G4Yh8T6gc6ljRE3NRnR1XgYT.json', 'var_call_9jxVGhr7A1ebYVecyQvkSEIg': 'file_storage/call_9jxVGhr7A1ebYVecyQvkSEIg.json', 'var_call_KHFNEv4rZFMGA5cDL8hOhrYj': 'file_storage/call_KHFNEv4rZFMGA5cDL8hOhrYj.json'}

exec(code, env_args)
