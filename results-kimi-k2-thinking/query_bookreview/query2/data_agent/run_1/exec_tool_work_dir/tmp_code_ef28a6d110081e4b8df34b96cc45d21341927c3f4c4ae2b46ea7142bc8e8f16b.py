code = """import json
import pandas as pd
import ast
import os

# Look for the actual result files
result_dir = '/tmp'
files = os.listdir(result_dir)
print('Available files:', files)

# Find the correct result files
books_file = None
reviews_file = None

for f in files:
    # Check file size to identify which is which
    file_path = os.path.join(result_dir, f)
    if os.path.getsize(file_path) > 1000:  # Larger file is likely books
        if books_file is None:
            books_file = file_path
        else:
            reviews_file = file_path
    else:
        reviews_file = file_path

print('Books file:', books_file)
print('Reviews file:', reviews_file)

# Read the data
with open(books_file, 'r') as f:
    books_data = json.load(f)

with open(reviews_file, 'r') as f:
    reviews_data = json.load(f)

print('Books count:', len(books_data))
print('Reviews count:', len(reviews_data))

# Show first few records
print('First book:', books_data[0] if books_data else 'No data')
print('First review:', reviews_data[0] if reviews_data else 'No data')"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': []}

exec(code, env_args)
