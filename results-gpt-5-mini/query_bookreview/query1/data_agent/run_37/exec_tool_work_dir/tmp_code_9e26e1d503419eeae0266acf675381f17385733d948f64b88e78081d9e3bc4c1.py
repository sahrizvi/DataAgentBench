code = """import json
with open(var_call_0obRIXKOWqtuchR2OVJHvKU7, 'r', encoding='utf-8') as f:
    books = json.load(f)

out = []
for i, b in enumerate(books[:50]):
    out.append({'i': i, 'book_id': b.get('book_id'), 'title': b.get('title'), 'details': b.get('details')})

print("__RESULT__:")
print(json.dumps(out))"""

env_args = {'var_call_JzElwp0nBhaFszYaTyRXQASr': ['books_info'], 'var_call_HQx3OeaNbloAEYAsG6o5rLqr': ['review'], 'var_call_0obRIXKOWqtuchR2OVJHvKU7': 'file_storage/call_0obRIXKOWqtuchR2OVJHvKU7.json', 'var_call_IuGPOjM1WdkWZ5XslbM99Ftx': 'file_storage/call_IuGPOjM1WdkWZ5XslbM99Ftx.json', 'var_call_YcBGkBCTgB5McoXe7Wt83vG3': {'decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_Uo7tbf2nSVNWdrWSk08m0LQO': {'total_books_with_reviews': 200, 'books_with_pub_year': 0, 'books_without_pub_year': 200, 'decade_counts': {}, 'decade_avg': {}, 'sample_per_book_head': []}}

exec(code, env_args)
