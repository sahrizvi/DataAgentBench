code = """import json

# Load the file paths
books_file = locals()['var_functions.query_db:2']
reviews_file = locals()['var_functions.query_db:3']

# Read the full data
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

# Count the records
books_count = len(books_data)
reviews_count = len(reviews_data)

# Sample for debugging
sample_book = books_data[0] if books_data else None
sample_review = reviews_data[0] if reviews_data else None

print('__RESULT__:')
print(json.dumps({
    "books_count": books_count,
    "reviews_count": reviews_count,
    "sample_book_keys": list(sample_book.keys()) if sample_book else [],
    "sample_review_keys": list(sample_review.keys()) if sample_review else []
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:3': 'file_storage/functions.query_db:3.json', 'var_functions.execute_python:10': {'available_vars': ['var_functions.list_db:0', 'var_functions.query_db:2', 'var_functions.query_db:3', '__builtins__', 'json', 'pd', 're'], 'var_types': {'var_functions.list_db:0': "<class 'list'>", 'var_functions.query_db:2': "<class 'str'>", 'var_functions.query_db:3': "<class 'str'>", '__builtins__': "<class 'dict'>", 'json': "<class 'module'>"}}}

exec(code, env_args)
