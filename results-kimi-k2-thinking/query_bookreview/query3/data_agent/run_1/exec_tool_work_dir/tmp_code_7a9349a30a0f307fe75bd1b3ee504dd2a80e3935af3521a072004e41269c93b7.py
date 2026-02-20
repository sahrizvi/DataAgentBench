code = """import json
import os

# Try to access the variable directly
try:
    # Access the result from the variable (if it's a list)
    children_books_data = var_functions.query_db:4
    print("Loaded children's books directly")
except:
    # Try to read from file
    try:
        with open('/tmp/tmp0e5vhf4x.json', 'r') as f:
            children_books_data = json.load(f)
        print("Loaded children's books from file")
    except:
        children_books_data = []
        print("Could not load children's books data")

print(f"Children's books count: {len(children_books_data)}")
print("First book:", children_books_data[0] if children_books_data else "None")

# Read the reviews file for 2020 onwards
try:
    with open('/tmp/tmpxf5c0b0y.json', 'r') as f:
        reviews_2020 = json.load(f)
    print(f"Loaded {len(reviews_2020)} reviews from 2020 onwards")
except Exception as e:
    print(f"Error reading reviews file: {e}")
    reviews_2020 = []

# Debug: show first few reviews
print("First few reviews:", reviews_2020[:3] if reviews_2020 else "None")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.list_db:2': ['review'], 'var_functions.query_db:4': 'file_storage/functions.query_db:4.json', 'var_functions.query_db:14': 'file_storage/functions.query_db:14.json'}

exec(code, env_args)
