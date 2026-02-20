code = """import json, re
with open(var_call_nIZtqYm1WnlSxW3jofWcK6ID, 'r') as f:
    books = json.load(f)

samples = []
for b in books[:20]:
    d = b.get('details')
    matches = []
    if isinstance(d, str):
        matches = re.findall(r"\b(1[5-9][0-9]{2}|20[0-2][0-9]|2023)\b", d)
    samples.append({'book_id': b.get('book_id'), 'details_sample': d[:200] if isinstance(d, str) else None, 'matches': matches})

out = {'num_books': len(books), 'samples': samples}
print('__RESULT__:')
print(json.dumps(out))"""

env_args = {'var_call_WjxSnom9ZZcw1f2zfM8y68hn': ['books_info'], 'var_call_Qgq3KUZEryaZofz9J0cBHUJB': ['review'], 'var_call_NVoEnkMvFVyDYFIhkNKQFyML': 'file_storage/call_NVoEnkMvFVyDYFIhkNKQFyML.json', 'var_call_yhdg6aG3UawDmz5sv6LZzVf5': 'file_storage/call_yhdg6aG3UawDmz5sv6LZzVf5.json', 'var_call_UIXpxuBL5mV0zLs0iHxlnjQu': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'var_call_nIZtqYm1WnlSxW3jofWcK6ID': 'file_storage/call_nIZtqYm1WnlSxW3jofWcK6ID.json', 'var_call_2Ajd2K3gfeO0QAv9ozU1eszn': {'decade': None, 'avg_rating': None, 'book_count': 0}, 'var_call_7T44ie4sxpubTLaTSjdzX47g': {'total_reviews': 1833, 'unique_review_books': 200, 'total_books': 200, 'books_with_pubyear': 0, 'unique_books_with_rating': 200, 'matched_with_pubyear': 0, 'decades': []}}

exec(code, env_args)
