code = """import json
import os

# Get the file path from storage
file_path = '/tmp/tmpq4h1t3_2.json'

# Check if file exists and load it
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        books_data = json.load(f)
    print(f"Loaded {len(books_data)} books")
    print(f"Sample book keys: {list(books_data[0].keys())}")
else:
    print(f"File not found: {file_path}")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
