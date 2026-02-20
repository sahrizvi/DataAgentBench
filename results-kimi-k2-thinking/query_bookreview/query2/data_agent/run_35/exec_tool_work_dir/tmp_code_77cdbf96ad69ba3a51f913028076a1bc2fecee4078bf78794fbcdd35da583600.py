code = """import json

# Access the books data from storage
books_data = locals()['var_functions.query_db:2']

# Check categories structure
print('Checking categories structure:')
for i, book in enumerate(books_data[:5]):
    print(f"Book {i}: {book['title']}")
    print(f"Categories: {book['categories']}")
    print(f"Type: {type(book['categories'])}")
    print()

# Look for Literature & Fiction category
print('Looking for Literature & Fiction books:')
fiction_books = []
for book in books_data:
    if book['categories'] and 'Literature & Fiction' in str(book['categories']):
        fiction_books.append(book)
        
print(f"Total Literature & Fiction books: {len(fiction_books)}")
print()

# Check details field for language info
print('Sample details fields:')
for i, book in enumerate(books_data[:5]):
    if book['details']:
        print(f"Book {i}: {book['title']}")
        print(f"Details: {book['details'][:100]}...")
        print()"""

env_args = {'var_functions.list_db:0': ['books_info'], 'var_functions.query_db:2': 'file_storage/functions.query_db:2.json', 'var_functions.list_db:5': ['review']}

exec(code, env_args)
