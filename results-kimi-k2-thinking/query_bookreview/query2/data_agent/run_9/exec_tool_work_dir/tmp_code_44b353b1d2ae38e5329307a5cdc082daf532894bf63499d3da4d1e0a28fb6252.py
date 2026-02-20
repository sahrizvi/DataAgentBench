code = """import json
import os

# Get the stored result
books_path = locals()['var_functions.query_db:5']

# Load data from the file
with open(books_path, 'r') as f:
    books = json.load(f)

print("Successfully loaded data")
print(f"Number of books: {len(books)}")
print(f"First book keys: {list(books[0].keys())}")
print("Sample ratings:")
for i, book in enumerate(books[:5]):
    rating = book.get('rating_number', 'N/A')
    print(f"  {book['title']}: {rating}")"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
