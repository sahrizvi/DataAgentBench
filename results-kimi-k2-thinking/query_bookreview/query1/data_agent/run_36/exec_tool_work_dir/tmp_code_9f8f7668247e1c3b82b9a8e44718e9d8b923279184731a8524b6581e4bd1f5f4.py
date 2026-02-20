code = """import json
import re

# Get the full result from query_db:2
r = locals().get('var_functions.query_db:2', 'no_result')
if isinstance(r, str) and r.endswith('.json'):
    with open(r, 'r') as f:
        books = json.load(f)
else:
    books = []

# Get the full result from query_db:6
r2 = locals().get('var_functions.query_db:6', 'no_result')
if isinstance(r2, str) and r2.endswith('.json'):
    with open(r2, 'r') as f:
        reviews = json.load(f)
else:
    reviews = []

print('__RESULT__:')
print(json.dumps({
    'books_count': len(books),
    'reviews_count': len(reviews),
    'sample_book': books[0] if books else None,
    'sample_review': reviews[0] if reviews else None
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:11': 'Read records'}

exec(code, env_args)
