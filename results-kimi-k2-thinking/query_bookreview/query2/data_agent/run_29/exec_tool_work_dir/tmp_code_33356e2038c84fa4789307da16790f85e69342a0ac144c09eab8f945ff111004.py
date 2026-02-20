code = """import json
import pandas as pd
import re

# Load books data
books_file = locals()['var_functions.query_db:6']
with open(books_file, 'r') as f:
    books = json.load(f)

# Load reviews data
reviews_file = locals()['var_functions.query_db:16']
with open(reviews_file, 'r') as f:
    reviews = json.load(f)

# Convert to DataFrames
df_books = pd.DataFrame(books)
df_reviews = pd.DataFrame(reviews)

print('__RESULT__:')
print(json.dumps({
    "books_count": len(df_books),
    "reviews_count": len(df_reviews),
    "books_columns": list(df_books.columns),
    "reviews_columns": list(df_reviews.columns)
}, ensure_ascii=False))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review'], 'var_functions.query_db:6': 'file_storage/functions.query_db:6.json', 'var_functions.execute_python:12': {'type': "<class 'str'>", 'is_string': True, 'preview': 'file_storage/functions.query_db:6.json'}, 'var_functions.execute_python:14': {'num_books': 40, 'columns': ['book_id', 'title', 'author', 'categories', 'details'], 'sample_categories': ['["Books", "Literature & Fiction", "History & Criticism"]', '["Books", "Literature & Fiction", "Genre Fiction"]', '["Books", "Literature & Fiction", "Poetry"]']}, 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json'}

exec(code, env_args)
