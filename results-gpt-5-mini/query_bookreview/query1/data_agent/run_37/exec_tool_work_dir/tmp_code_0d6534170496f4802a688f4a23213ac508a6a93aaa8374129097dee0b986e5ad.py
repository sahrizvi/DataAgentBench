code = """import json, re
with open(var_call_0obRIXKOWqtuchR2OVJHvKU7, 'r', encoding='utf-8') as f:
    books = json.load(f)

pattern_any = re.compile(r"\d{4}")
matches = []
for i,b in enumerate(books[:30]):
    d = b.get('details')
    matches.append({'i':i,'book_id':b.get('book_id'),'details_type':type(d).__name__,'details_repr': repr(d)[:200], 'has_4digits': bool(pattern_any.search(d)) if isinstance(d,str) else False})

res={'matches': matches}
print("__RESULT__:")
import json
print(json.dumps(res))"""

env_args = {'var_call_JzElwp0nBhaFszYaTyRXQASr': ['books_info'], 'var_call_HQx3OeaNbloAEYAsG6o5rLqr': ['review'], 'var_call_0obRIXKOWqtuchR2OVJHvKU7': 'file_storage/call_0obRIXKOWqtuchR2OVJHvKU7.json', 'var_call_IuGPOjM1WdkWZ5XslbM99Ftx': 'file_storage/call_IuGPOjM1WdkWZ5XslbM99Ftx.json', 'var_call_YcBGkBCTgB5McoXe7Wt83vG3': {'decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_Uo7tbf2nSVNWdrWSk08m0LQO': {'total_books_with_reviews': 200, 'books_with_pub_year': 0, 'books_without_pub_year': 200, 'decade_counts': {}, 'decade_avg': {}, 'sample_per_book_head': []}, 'var_call_TCJ2Wo5r6tTbZsnNCSEShaFk': 'file_storage/call_TCJ2Wo5r6tTbZsnNCSEShaFk.json', 'var_call_TiD7X7ZOg4vqNyxFUxz0JkOJ': {'total_books': 200, 'books_with_year_in_details': 0, 'samples': []}}

exec(code, env_args)
