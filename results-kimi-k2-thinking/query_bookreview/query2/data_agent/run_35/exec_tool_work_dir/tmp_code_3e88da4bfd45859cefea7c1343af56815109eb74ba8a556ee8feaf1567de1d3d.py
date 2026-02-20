code = """import json

# Access the books data from storage
books_data = var_functions.query_db:2

print("Checking categories structure:")
for i, book in enumerate(books_data[:5]):
    print(f"Book {i}: {book['title']}")
    print(f"Categories: {book['categories']}")
    print(f"Type of categories: {type(book['categories'])}")
    print()

print("Looking for Literature & Fiction in categories:")
fiction_books = []
for i, book in enumerate(books_data):
    if book['categories'] and 'Literature & Fiction' in str(book['categories']):
        fiction_books.append(book)
        if len(fiction_books) <= 5:
            print(f"Found: {book['title']}")
            print(f"Categories: {book['categories']}")

print(f"\nTotal books with 'Literature & Fiction' in categories: {len(fiction_books)}")

# Check details field for language info
print("\nSample details fields:")
for i, book in enumerate(books_data[:5]):
    if book['details']:
        print(f"Book {i}: {book['title']}")
        print(f"Details snippet: {str(book['details'])[:200]}...")
        print()"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review']}

exec(code, env_args)
