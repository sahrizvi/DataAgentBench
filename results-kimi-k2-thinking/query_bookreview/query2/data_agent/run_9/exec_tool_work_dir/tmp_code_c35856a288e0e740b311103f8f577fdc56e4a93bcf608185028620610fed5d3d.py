code = """# Access the stored result properly
import json
import os

# The result should be accessible via the variable name
books_data = var_functions.query_db:5

print(f"Type of books_data: {type(books_data)}")
if isinstance(books_data, str) and books_data.endswith('.json'):
    # It's a file path
    with open(books_data, 'r') as f:
        books_list = json.load(f)
    print(f"Loaded {len(books_list)} books from file")
    print(f"Columns: {list(books_list[0].keys())}")
    # Filter for perfect rating
    perfect_books = [book for book in books_list if float(book.get('rating_number', 0)) == 5.0]
    print(f"\nBooks with 5.0 rating: {len(perfect_books)}")
    for book in perfect_books[:10]:
        print(f"- {book['title']}")
else:
    print("Books data is not a file path string")

print('__RESULT__:')
print(json.dumps(f"Found preliminary data: {len(books_list)} books total"))"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.query_db:5': 'file_storage/functions.query_db:5.json'}

exec(code, env_args)
