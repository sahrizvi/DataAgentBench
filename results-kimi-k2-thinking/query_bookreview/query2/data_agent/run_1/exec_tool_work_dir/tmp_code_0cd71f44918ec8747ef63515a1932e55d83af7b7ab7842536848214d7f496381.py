code = """import json
import pandas as pd
import ast
import os

# Get all JSON files from /tmp
json_files = []
for root, dirs, files in os.walk('/tmp'):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

print(f"Found JSON files: {len(json_files)}")
for i, f in enumerate(json_files):
    print(f"  {i}: {f} (size: {os.path.getsize(f)} bytes)")

# Try to identify which file is which based on content
books_data = None
reviews_data = None

for file_path in json_files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                keys = list(first_item.keys())
                print(f"\nFile {file_path} keys: {keys}")
                
                # Check if it's books data (has book_id, title, categories)
                if 'book_id' in keys and 'title' in keys and 'categories' in keys:
                    books_data = data
                    print("  -> Identified as books data")
                # Check if it's reviews data (has purchase_id, rating)
                elif 'purchase_id' in keys and 'rating' in keys:
                    reviews_data = data
                    print("  -> Identified as reviews data")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if books_data is None or reviews_data is None:
    print("ERROR: Could not identify both datasets")
    exit(1)

print(f"\nBooks loaded: {len(books_data)}")
print(f"Reviews loaded: {len(reviews_data)}")

# Create DataFrames
df_books = pd.DataFrame(books_data)
df_reviews = pd.DataFrame(reviews_data)

# Show sample data
print("\nBooks sample:")
print(df_books[['book_id', 'title', 'categories']].head(3))

print("\nReviews sample:")
print(df_reviews[['purchase_id', 'rating']].head(3))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json', 'var_functions.execute_python:10': [], 'var_functions.query_db:16': 'file_storage/functions.query_db:16.json'}

exec(code, env_args)
