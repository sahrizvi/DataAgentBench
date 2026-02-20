code = """import json
import pandas as pd
import re

# Load the data from the files
books_file = var_functions.query_db:1
reviews_file = var_functions.query_db:2

# Read the full data from files
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

print('__RESULT__:')
print(json.dumps({
    "books_count": len(books_data),
    "reviews_count": len(reviews_data),
    "sample_books": books_data[:2],
    "sample_reviews": reviews_data[:2]
}))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:3': 'file_storage/functions.query_db:3.json'}

exec(code, env_args)
