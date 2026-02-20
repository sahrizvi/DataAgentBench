code = """import json, re
from collections import Counter

books_path = var_call_0obRIXKOWqtuchR2OVJHvKU7
with open(books_path, 'r', encoding='utf-8') as f:
    books = json.load(f)

pattern = re.compile(r"\b(1[0-9]{3}|20[0-2][0-9])\b")
count_with = 0
samples = []
for b in books:
    d = b.get('details','')
    if isinstance(d, str) and pattern.search(d):
        count_with += 1
        if len(samples) < 20:
            samples.append({'book_id': b.get('book_id'), 'details': d, 'year': int(pattern.search(d).group(0))})

res = {'total_books': len(books), 'books_with_year_in_details': count_with, 'samples': samples[:20]}
print("__RESULT__:")
import json
print(json.dumps(res))"""

env_args = {'var_call_JzElwp0nBhaFszYaTyRXQASr': ['books_info'], 'var_call_HQx3OeaNbloAEYAsG6o5rLqr': ['review'], 'var_call_0obRIXKOWqtuchR2OVJHvKU7': 'file_storage/call_0obRIXKOWqtuchR2OVJHvKU7.json', 'var_call_IuGPOjM1WdkWZ5XslbM99Ftx': 'file_storage/call_IuGPOjM1WdkWZ5XslbM99Ftx.json', 'var_call_YcBGkBCTgB5McoXe7Wt83vG3': {'decade': None, 'average_rating': None, 'book_count': 0}, 'var_call_Uo7tbf2nSVNWdrWSk08m0LQO': {'total_books_with_reviews': 200, 'books_with_pub_year': 0, 'books_without_pub_year': 200, 'decade_counts': {}, 'decade_avg': {}, 'sample_per_book_head': []}, 'var_call_TCJ2Wo5r6tTbZsnNCSEShaFk': 'file_storage/call_TCJ2Wo5r6tTbZsnNCSEShaFk.json'}

exec(code, env_args)
