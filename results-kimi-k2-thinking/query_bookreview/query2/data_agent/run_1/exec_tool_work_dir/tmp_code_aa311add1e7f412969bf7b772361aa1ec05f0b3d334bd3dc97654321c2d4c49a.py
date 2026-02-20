code = """import json
import pandas as pd
import ast
import os

# Check what files are available in /tmp/
print("Files in /tmp/:")
for f in os.listdir('/tmp'):
    if f.endswith('.json'):
        print(f)

# Since the files might have different names, let's check the storage
# Try to find the correct file paths
try:
    # Look for files containing the data
    files = os.listdir('/tmp')
    books_file = None
    reviews_file = None
    
    for f in files:
        if 'books' in f.lower() or 'query' in f.lower():
            books_file = f
        if 'review' in f.lower():
            reviews_file = f
    
    print(f"Potential books file: {books_file}")
    print(f"Potential reviews file: {reviews_file}")
    
except Exception as e:
    print(f"Error: {e}")

# Let's just read all JSON files and see which one looks right
for f in os.listdir('/tmp'):
    if f.endswith('.json'):
        print(f"\nContents of {f}:")
        with open(f'/tmp/{f}', 'r') as file:
            try:
                data = json.load(file)
                if isinstance(data, list) and len(data) > 0:
                    print(f"First item keys: {list(data[0].keys())}")
            except:
                print("Could not parse")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
